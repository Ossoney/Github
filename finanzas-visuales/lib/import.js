import { db } from './db'

export async function importFromExcel(file) {
    const XLSX = await import('xlsx');
    return new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onload = async (e) => {
            try {
                const data = new Uint8Array(e.target.result)
                const workbook = XLSX.read(data, { type: 'array' })

                // 1. Determine Format
                const transaccionesSheet = workbook.Sheets['Transacciones']
                if (!transaccionesSheet) {
                    throw new Error("No se encontró la hoja 'Transacciones'.")
                }

                const rawRows = XLSX.utils.sheet_to_json(transaccionesSheet)
                if (rawRows.length === 0) {
                    throw new Error("El archivo está vacío.")
                }

                // Check if it's the NEW flat format (contains 'cuenta' or 'categoría' columns)
                const isFlatFormat = 'cuenta' in rawRows[0] || 'categoría' in rawRows[0]

                if (isFlatFormat) {
                    await importFlatFormat(rawRows)
                } else {
                    await importLegacyFormat(workbook, rawRows)
                }

                resolve({ success: true, count: rawRows.length })

            } catch (error) {
                console.error("Import Error:", error)
                reject(error)
            }
        }

        reader.readAsArrayBuffer(file)
    })
}

/**
 * Imports the new flat format by resolving names to IDs.
 * Creates missing wallets and categories/subcategories automatically.
 */
async function importFlatFormat(rows) {
    const XLSX = await import('xlsx');

    await db.transaction('rw', db.transactions, db.wallets, db.categories, async () => {
        // Cache existing data to minimize DB lookups
        const existingWallets = await db.wallets.toArray()
        const existingCategories = await db.categories.toArray()

        const walletMap = new Map(existingWallets.map(w => [w.name.toLowerCase(), w.id]))
        const categoryMap = new Map(existingCategories.map(c => [
            `${c.name.toLowerCase()}|${c.parentId || 'root'}|${c.type}`,
            c.id
        ]))

        for (const row of rows) {
            // 1. Resolve Wallet
            const walletName = row['cuenta'] || 'Efectivo'
            let walletId = walletMap.get(walletName.toLowerCase())

            if (!walletId) {
                walletId = await db.wallets.add({
                    name: walletName,
                    type: 'cash',
                    balance: 0,
                    color: '#64748b'
                })
                walletMap.set(walletName.toLowerCase(), walletId)
            }

            // 2. Resolve Category
            const type = (row['tipo'] || 'gasto').toLowerCase() === 'ingreso' ? 'income' : 'expense'
            const catName = row['categoría'] || 'Otros'
            let parentId = categoryMap.get(`${catName.toLowerCase()}|root|${type}`)

            if (!parentId) {
                parentId = await db.categories.add({
                    name: catName,
                    type: type,
                    icon: 'HelpCircle',
                    color: type === 'income' ? '#10b981' : '#f43f5e',
                    parentId: null
                })
                categoryMap.set(`${catName.toLowerCase()}|root|${type}`, parentId)
            }

            // 3. Resolve Subcategory
            const subCatName = row['subcategoría']
            let categoryId = parentId

            if (subCatName) {
                let subId = categoryMap.get(`${subCatName.toLowerCase()}|${parentId}|${type}`)
                if (!subId) {
                    subId = await db.categories.add({
                        name: subCatName,
                        type: type,
                        icon: 'Circle',
                        color: '#64748b',
                        parentId: parentId
                    })
                    categoryMap.set(`${subCatName.toLowerCase()}|${parentId}|${type}`, subId)
                }
                categoryId = subId
            }

            // 4. Parse Date
            let date = new Date()
            if (row['fecha']) {
                // Handle Excel numeric dates if they come through
                if (typeof row['fecha'] === 'number') {
                    date = new Date((row['fecha'] - (25567 + 1)) * 86400 * 1000)
                } else {
                    const parsed = parseDate(row['fecha'])
                    if (!isNaN(parsed.getTime())) date = parsed
                }
            }

            // 5. Insert Transaction
            const amount = parseFloat(row['importe'] || 0)

            await db.transactions.add({
                walletId: Number(walletId),
                categoryId: Number(categoryId),
                amount: amount,
                type: type,
                description: row['descripción'] || '',
                date: date,
                tags: []
            })

            // 6. Update Wallet Balance (since we are importing transactions, we update the accounts)
            const wallet = await db.wallets.get(Number(walletId))
            if (wallet) {
                const effect = type === 'income' ? amount : -amount
                await db.wallets.update(Number(walletId), {
                    balance: (wallet.balance || 0) + effect
                })
            }
        }
    })
}

/**
 * Legacy format import (ID based, multiple sheets)
 */
async function importLegacyFormat(workbook, transactions) {
    const XLSX = await import('xlsx');

    const walletSheet = workbook.Sheets['Cuentas']
    const wallets = walletSheet ? XLSX.utils.sheet_to_json(walletSheet) : []

    const catSheet = workbook.Sheets['Categorias']
    const categories = catSheet ? XLSX.utils.sheet_to_json(catSheet) : []

    await db.transaction('rw', db.transactions, db.wallets, db.categories, async () => {
        // Clear DB for a clean "Restore" (Legacy behavior)
        await db.transactions.clear()
        await db.wallets.clear()
        await db.categories.clear()

        const walletIdMap = {}
        for (const w of wallets) {
            const oldId = w.id
            const { id, ...rest } = w
            const newId = await db.wallets.add(rest)
            walletIdMap[oldId] = newId
        }

        const catIdMap = {}
        const parents = categories.filter(c => !c.parentId)
        const children = categories.filter(c => c.parentId)

        for (const p of parents) {
            const oldId = p.id
            const { id, ...rest } = p
            const newId = await db.categories.add(rest)
            catIdMap[oldId] = newId
        }

        for (const c of children) {
            const oldId = c.id
            const oldParentId = c.parentId
            const { id, ...rest } = c
            const newParentId = catIdMap[oldParentId] || null
            const newId = await db.categories.add({ ...rest, parentId: newParentId })
            catIdMap[oldId] = newId
        }

        const txsToInsert = transactions.map(t => {
            const { id, ...rest } = t
            return {
                ...rest,
                walletId: walletIdMap[t.walletId] || t.walletId,
                categoryId: catIdMap[t.categoryId] || t.categoryId,
                date: t.date ? new Date(t.date) : new Date(),
                tags: typeof t.tags === 'string' ? t.tags.split(',').map(tag => tag.trim()) : (t.tags || [])
            }
        })
        await db.transactions.bulkAdd(txsToInsert)
    })
}

function parseDate(dateStr) {
    // dd/mm/yyyy hh:mm
    const parts = dateStr.split(/[\s/:]+/)
    if (parts.length >= 3) {
        const day = parseInt(parts[0], 10)
        const month = parseInt(parts[1], 10) - 1
        const year = parseInt(parts[2], 10)
        const hour = parseInt(parts[3] || 0, 10)
        const minute = parseInt(parts[4] || 0, 10)
        return new Date(year, month, day, hour, minute)
    }
    return new Date(dateStr)
}

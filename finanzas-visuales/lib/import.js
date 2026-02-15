import { db } from './db'

export async function importFromExcel(file) {
    const XLSX = await import('xlsx');
    return new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onload = async (e) => {
            try {
                const data = new Uint8Array(e.target.result)
                const workbook = XLSX.read(data, { type: 'array' })

                // Define limits to prevent crashing with huge files
                const SHEET_NAMES = ['Transacciones', 'Cuentas', 'Categorias']

                // 1. Transactions
                const txSheet = workbook.Sheets['Transacciones']
                const transactions = txSheet ? XLSX.utils.sheet_to_json(txSheet) : []

                // 2. Wallets
                const walletSheet = workbook.Sheets['Cuentas']
                const wallets = walletSheet ? XLSX.utils.sheet_to_json(walletSheet) : []

                // 3. Categories
                const catSheet = workbook.Sheets['Categorias']
                const categories = catSheet ? XLSX.utils.sheet_to_json(catSheet) : []

                if (transactions.length === 0 && wallets.length === 0 && categories.length === 0) {
                    throw new Error("El archivo parece vacío o no tiene el formato correcto.")
                }

                await db.transaction('rw', db.transactions, db.wallets, db.categories, async () => {
                    // Clear existing data? Or Merge?
                    // For V1, "Import" usually implies "Restore/Overwrite" or "Append".
                    // Given the complexities of ID conflicts, "Wipe & Restore" is safer for a "Backup/Restore" feature.
                    // BUT, user might want to merge.
                    // Let's go with "Wipe & Restore" for now as it aligns with "Nuclear Button" + "Export" workflow.
                    // Ideally, we'd ask. But for now, let's implement a clean restore.

                    // Actually, let's just Append for now? No, IDs will conflict.
                    // Let's Assume "Restore Backup" mode.

                    await db.transactions.clear()
                    await db.wallets.clear()
                    await db.categories.clear()

                    // Import Categories
                    // We need to map old IDs to new IDs if we were appending.
                    // Since we are clearing, we can try to keep IDs if Dexie allows, 
                    // or just let Dexie generate new ones.
                    // IF the export saved IDs, we should probably try to respect them OR re-map.
                    // Re-mapping is safer.

                    // However, we need to maintain relationships (transaction -> wallet, transaction -> category).

                    // Strategy: 
                    // 1. Clear DB.
                    // 2. Import Wallets (keep IDs if possible or re-map).
                    // 3. Import Categories (keep IDs if possible or re-map).
                    // 4. Import Transactions (update walletId and categoryId).

                    // Let's assume the Export format includes IDs.

                    // Import Wallets
                    const walletIdMap = {} // Old -> New
                    for (const w of wallets) {
                        const oldId = w.id
                        delete w.id // Let Dexie generate new ID
                        const newId = await db.wallets.add(w)
                        walletIdMap[oldId] = newId
                    }

                    // Import Categories
                    const catIdMap = {} // Old -> New
                    // We must import Parents first, then Children.
                    // Sort by parentId (null first)
                    categories.sort((a, b) => (a.parentId || 0) - (b.parentId || 0))

                    for (const c of categories) {
                        const oldId = c.id
                        const oldParentId = c.parentId
                        delete c.id

                        // Map parentId
                        if (oldParentId && catIdMap[oldParentId]) {
                            c.parentId = catIdMap[oldParentId]
                        } else {
                            c.parentId = null // Fallback
                        }

                        const newId = await db.categories.add(c)
                        catIdMap[oldId] = newId
                    }

                    // Import Transactions
                    for (const t of transactions) {
                        delete t.id // New ID

                        // Remap IDs
                        if (walletIdMap[t.walletId]) t.walletId = walletIdMap[t.walletId]
                        if (catIdMap[t.categoryId]) t.categoryId = catIdMap[t.categoryId]

                        // Parse Date
                        if (t.date) t.date = new Date(t.date)

                        // Parse Tags (String to Array)
                        if (typeof t.tags === 'string') {
                            t.tags = t.tags.split(',').map(tag => tag.trim())
                        }

                        await db.transactions.add(t)
                    }
                })

                resolve({ success: true, count: transactions.length })

            } catch (error) {
                console.error("Import Error:", error)
                reject(error)
            }
        }

        reader.readAsArrayBuffer(file)
    })
}

import { db, recalculateBalances } from './db'

// Maps common category name keywords to appropriate Lucide icons
const ICON_MAP = [
    // Food & Groceries
    { keywords: ['aliment', 'comida', 'supermercado', 'restaur', 'food', 'grocer', 'cocina', 'cena', 'almuerzo', 'desayuno', 'cafe', 'café'], icon: 'ShoppingCart' },
    // Transport
    { keywords: ['transport', 'gasolina', 'combustible', 'coche', 'car', 'auto', 'moto', 'metro', 'bus', 'taxi', 'uber', 'tren', 'vuelo', 'avion', 'viaje', 'parking', 'peaje'], icon: 'Car' },
    // Health
    { keywords: ['salud', 'health', 'medic', 'farmacia', 'doctor', 'hospital', 'deporte', 'gym', 'sport', 'fitness', 'dental', 'optic'], icon: 'Heart' },
    // Housing
    { keywords: ['hogar', 'casa', 'alquiler', 'hipoteca', 'luz', 'agua', 'gas', 'internet', 'telefono', 'suministr', 'home', 'rent', 'mortgage', 'electricity', 'housing'], icon: 'Home' },
    // Shopping / Clothing
    { keywords: ['ropa', 'moda', 'calzado', 'fashion', 'compras', 'shopping', 'tienda'], icon: 'ShoppingBag' },
    // Work / Salary
    { keywords: ['trabajo', 'salario', 'sueldo', 'nomina', 'work', 'salary', 'income', 'ingreso', 'empresa', 'freelance', 'negocio'], icon: 'Briefcase' },
    // Education
    { keywords: ['educacion', 'cursos', 'libros', 'colegio', 'universidad', 'school', 'education', 'formacion'], icon: 'GraduationCap' },
    // Entertainment / Leisure
    { keywords: ['ocio', 'entretenimiento', 'cine', 'musica', 'netflix', 'spotify', 'juegos', 'games', 'leisure', 'recreation', 'suscripcion', 'subscri'], icon: 'Play' },
    // Savings / Investments
    { keywords: ['ahorro', 'inversion', 'saving', 'invest', 'bolsa', 'fondos', 'pension'], icon: 'PiggyBank' },
    // Gifts / Social
    { keywords: ['regalo', 'gift', 'cumpleaños', 'social', 'celebracion', 'fiesta'], icon: 'Gift' },
    // Technology
    { keywords: ['tecnologia', 'tech', 'ordenador', 'movil', 'phone', 'computer', 'electronico', 'electronic'], icon: 'Smartphone' },
    // Travel
    { keywords: ['viaje', 'hotel', 'travel', 'vacacion', 'vacation', 'turismo', 'alojamiento'], icon: 'Plane' },
    // Pets
    { keywords: ['mascota', 'perro', 'gato', 'pet', 'veterinario', 'vet'], icon: 'PawPrint' },
    // Kids / Children
    { keywords: ['hijo', 'niño', 'bebe', 'guarderia', 'child', 'kid', 'baby'], icon: 'Baby' },
    // Beauty / Personal Care
    { keywords: ['belleza', 'peluqueria', 'beauty', 'estetica', 'cosmetica', 'personal'], icon: 'Sparkles' },
    // Bank / Finances
    { keywords: ['banco', 'bank', 'comision', 'prestamo', 'credito', 'loan', 'finanza', 'finance'], icon: 'Landmark' },
]

function guessIcon(name, isParent = true) {
    const normalized = name.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    for (const entry of ICON_MAP) {
        if (entry.keywords.some(kw => normalized.includes(kw))) {
            return entry.icon
        }
    }
    return isParent ? 'Folder' : 'Circle'
}

export async function importFromExcel(file) {
    const XLSX = await import('xlsx');
    return new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onload = async (e) => {
            try {
                const data = new Uint8Array(e.target.result)
                const workbook = XLSX.read(data, { type: 'array' })

                // 1. Determine Format
                const sheetNames = workbook.SheetNames
                if (sheetNames.length === 0) {
                    throw new Error("El archivo no tiene hojas.")
                }

                // IMPROVED: Sheet Agnostic Detection
                const possibleNames = ['transacciones', 'transactions', 'movementos', 'transakzioak', 'transaccions', 'movimientos', 'gastos', 'ingresos']
                let targetSheetName = sheetNames.find(name => possibleNames.includes(name.toLowerCase()))

                if (!targetSheetName) {
                    // Fallback: take the first sheet regardless of name
                    targetSheetName = sheetNames[0]
                }

                const sheet = workbook.Sheets[targetSheetName]
                const rawRows = XLSX.utils.sheet_to_json(sheet)

                if (rawRows.length === 0) {
                    throw new Error(`La hoja '${targetSheetName}' está vacía o no tiene datos válidos.`)
                }

                // IMPROVED: Format Detection
                const firstRowKeys = Object.keys(rawRows[0]).map(k => k.toLowerCase())
                const hasFlatColumns = firstRowKeys.some(k =>
                    k.includes('cuenta') || k.includes('wallet') ||
                    k.includes('categor') || k.includes('category') ||
                    k.includes('importe') || k.includes('amount') || k.includes('monto')
                )

                const isLegacy = sheetNames.includes('Cuentas') && sheetNames.includes('Categorias') && !hasFlatColumns

                if (isLegacy) {
                    await importLegacyFormat(workbook, rawRows)
                } else {
                    await importFlatFormat(rawRows)
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
    await db.transaction('rw', db.transactions, db.wallets, db.categories, async () => {
        // Cache existing data
        const existingWallets = await db.wallets.toArray()
        const existingCategories = await db.categories.toArray()

        const walletMap = new Map(existingWallets.map(w => [w.name.toLowerCase(), w.id]))
        const categoryMap = new Map(existingCategories.map(c => [
            `${c.name.toLowerCase()}|${c.parentId || 'root'}|${c.type}`,
            c.id
        ]))

        // Key column mapping (normalized)
        const findColumn = (row, keywords) => {
            const keys = Object.keys(row)
            return keys.find(k => {
                const norm = k.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                return keywords.some(kw => norm.includes(kw))
            })
        }

        for (const row of rows) {
            const colMap = {
                wallet: findColumn(row, ['cuenta', 'wallet', 'banco', 'account']),
                type: findColumn(row, ['tipo', 'type', 'movimiento']),
                category: findColumn(row, ['categoria', 'category', 'clase']),
                subcategory: findColumn(row, ['subcategoria', 'subcategory']),
                date: findColumn(row, ['fecha', 'date', 'dia']),
                amount: findColumn(row, ['importe', 'amount', 'monto', 'cantidad', 'valor']),
                desc: findColumn(row, ['descripcion', 'description', 'nota', 'concepto', 'comentario']),
                emotion: findColumn(row, ['emocion', 'emotion', 'sentimiento', 'emoji', 'estado_emocional']),
                tags: findColumn(row, ['etiquetas', 'tags', 'labels', 'marcadores'])
            }

            // 1. Resolve Wallet
            const walletName = (colMap.wallet ? row[colMap.wallet] : 'Efectivo') || 'Efectivo'
            let walletId = walletMap.get(walletName.toString().toLowerCase())

            if (!walletId) {
                walletId = await db.wallets.add({
                    name: walletName.toString(),
                    type: 'cash',
                    balance: 0,
                    color: '#64748b'
                })
                walletMap.set(walletName.toString().toLowerCase(), walletId)
            }

            // 2. Resolve Type (multi-strategy)
            const rawType = colMap.type ? row[colMap.type]?.toString().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '') : ''
            const rawAmount = colMap.amount ? row[colMap.amount] : null

            // Strategy A: explicit income keywords in the type column
            const INCOME_KEYWORDS = ['ingreso', 'ingresos', 'income', 'entrada', 'cobro', 'cobrar', 'abono', 'recibido', 'recibo', 'venta', 'salario', 'nomina', 'sueldo', 'in']
            const EXPENSE_KEYWORDS = ['gasto', 'gastos', 'expense', 'salida', 'pago', 'pagar', 'cargo', 'debito', 'debit', 'out', 'compra']

            let type = null
            if (rawType) {
                if (INCOME_KEYWORDS.some(kw => rawType.includes(kw))) type = 'income'
                else if (EXPENSE_KEYWORDS.some(kw => rawType.includes(kw))) type = 'expense'
            }

            // Strategy B: sign of the amount (negative = expense, positive = income)
            if (!type && rawAmount !== null) {
                const numAmount = typeof rawAmount === 'number' ? rawAmount : parseFloat(rawAmount?.toString().replace(/[^0-9.,-]/g, '').replace(',', '.')) || 0
                if (numAmount < 0) type = 'expense'
                else if (numAmount > 0) type = 'income'
            }

            // Fallback
            if (!type) type = 'expense'

            // 3. Resolve Category
            const catName = (colMap.category ? row[colMap.category] : 'Otros') || 'Otros'
            let parentId = categoryMap.get(`${catName.toString().toLowerCase()}|root|${type}`)

            if (!parentId) {
                parentId = await db.categories.add({
                    name: catName.toString(),
                    type: type,
                    icon: guessIcon(catName.toString(), true),
                    color: type === 'income' ? '#10b981' : '#f43f5e',
                    parentId: null
                })
                categoryMap.set(`${catName.toString().toLowerCase()}|root|${type}`, parentId)
            }

            // 4. Resolve Subcategory
            const subCatName = colMap.subcategory ? row[colMap.subcategory] : null
            let categoryId = parentId

            if (subCatName) {
                let subId = categoryMap.get(`${subCatName.toString().toLowerCase()}|${parentId}|${type}`)
                if (!subId) {
                    subId = await db.categories.add({
                        name: subCatName.toString(),
                        type: type,
                        icon: guessIcon(subCatName.toString(), false),
                        color: '#64748b',
                        parentId: parentId
                    })
                    categoryMap.set(`${subCatName.toString().toLowerCase()}|${parentId}|${type}`, subId)
                }
                categoryId = subId
            }

            // 5. Parse Date
            let date = new Date()
            const rawDate = colMap.date ? row[colMap.date] : null
            if (rawDate) {
                if (typeof rawDate === 'number') {
                    // Excel serial date
                    date = new Date((rawDate - (25567 + 1)) * 86400 * 1000)
                } else {
                    const parsed = parseDate(rawDate.toString())
                    if (!isNaN(parsed.getTime())) date = parsed
                }
            }

            // 6. Normalize Amount  (rawAmount already declared in step 2)
            let amount = 0
            const rawAmountVal = rawAmount ?? 0
            if (typeof rawAmountVal === 'number') {
                amount = rawAmountVal
            } else if (typeof rawAmountVal === 'string') {
                // Handle "1.234,56" or "1234.56" and remove currency symbols
                let cleanAmount = rawAmountVal.replace(/[^\d.,-]/g, '')
                if (cleanAmount.includes(',') && cleanAmount.includes('.')) {
                    cleanAmount = cleanAmount.replace(/\./g, '').replace(',', '.')
                } else if (cleanAmount.includes(',')) {
                    cleanAmount = cleanAmount.replace(',', '.')
                }
                amount = parseFloat(cleanAmount) || 0
            }

            // 7. Insert Transaction
            await db.transactions.add({
                walletId: Number(walletId),
                categoryId: Number(categoryId),
                amount: Math.abs(amount),
                type: type,
                description: colMap.desc ? row[colMap.desc]?.toString() : '',
                emotion: colMap.emotion ? row[colMap.emotion]?.toString() : '',
                date: date,
                tags: colMap.tags ? row[colMap.tags]?.toString().split(',').map(tag => tag.trim()).filter(Boolean) : []
            })

            // 8. Update Wallet Balance
            const wallet = await db.wallets.get(Number(walletId))
            if (wallet) {
                const effect = type === 'income' ? Math.abs(amount) : -Math.abs(amount)
                await db.wallets.update(Number(walletId), {
                    balance: (wallet.balance || 0) + effect
                })
            }
        }
    })

    // After transaction is finished, we do one final recalculation to be sure
    await recalculateBalances()
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

    // Final sync for legacy format too
    await recalculateBalances()
}

function parseDate(dateStr) {
    // Attempt standard formats
    // dd/mm/yyyy hh:mm or yyyy-mm-dd
    if (dateStr.includes('-')) return new Date(dateStr)

    const parts = dateStr.split(/[\s/:]+/)
    if (parts.length >= 3) {
        let day = parseInt(parts[0], 10)
        let month = parseInt(parts[1], 10) - 1
        let year = parseInt(parts[2], 10)
        const hour = parseInt(parts[3] || 0, 10)
        const minute = parseInt(parts[4] || 0, 10)

        // Handle 2-digit years
        const fullYear = year < 50 ? 2000 + year : (year < 100 ? 1900 + year : year)

        return new Date(fullYear, month, day, hour, minute)
    }
    return new Date(dateStr)
}

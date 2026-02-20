import { format } from 'date-fns'
import { db } from './db'

export const exportToExcel = async (transactions, wallets, categories) => {
    // Dynamic import to reduce initial bundle size
    const XLSX = await import('xlsx');

    // Fetch global currency
    const settings = await db.settings.get('global')
    const currency = settings?.currency || 'EUR'

    // 1. Prepare Data
    const data = transactions.map(tx => {
        const wallet = wallets.find(w => w.id === Number(tx.walletId))
        const category = categories.find(c => c.id === Number(tx.categoryId))

        let catName = 'Sin Categoría'
        let subCatName = ''

        if (category) {
            if (category.parentId) {
                const parent = categories.find(c => c.id === Number(category.parentId))
                catName = parent?.name || 'Sin Categoría'
                subCatName = category.name
            } else {
                catName = category.name
            }
        }

        return {
            'fecha': format(new Date(tx.date), 'dd/MM/yyyy HH:mm'),
            'cuenta': wallet?.name || 'Desconocido',
            'tipo': tx.type === 'expense' ? 'gasto' : 'ingreso',
            'categoría': catName,
            'subcategoría': subCatName,
            'importe': tx.amount,
            'moneda': currency,
            'descripción': tx.description || ''
        }
    })

    // 2. Create Sheet
    const worksheet = XLSX.utils.json_to_sheet(data)

    // 3. Create Workbook
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, "Transacciones")

    // 4. Generate File Name
    const fileName = `visualis_${format(new Date(), 'yyyyMMdd_HHmmss')}.xlsx`

    // 5. Download
    XLSX.writeFile(workbook, fileName)
}

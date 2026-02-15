import { format } from 'date-fns'

export const exportToExcel = async (transactions, wallets, categories) => {
    // Dynamic import to reduce initial bundle size
    const XLSX = await import('xlsx');

    // 1. Prepare Data
    const data = transactions.map(tx => {
        const wallet = wallets.find(w => w.id === tx.walletId)
        const category = categories.find(c => c.id === tx.categoryId)

        return {
            Fecha: format(new Date(tx.date), 'dd/MM/yyyy HH:mm'),
            Tipo: tx.type === 'expense' ? 'Gasto' : 'Ingreso',
            Categoría: category?.name || 'Sin Categoría',
            Wallet: wallet?.name || 'Desconocido',
            Descripción: tx.description || '',
            Monto: tx.amount,
            Moneda: 'EUR' // Harcoded for now based on wallet currency default
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

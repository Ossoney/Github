import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { db } from './db'
import { format } from 'date-fns'

// ----------------------------------------------------------------------
// UI UTILS
// ----------------------------------------------------------------------
export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

export const formatCurrency = (amount, currency = 'EUR') => {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: currency,
    }).format(amount);
};

// ----------------------------------------------------------------------
// EXPORT DATA
// ----------------------------------------------------------------------
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

// ----------------------------------------------------------------------
// IMPORT DATA
// ----------------------------------------------------------------------
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
                    // Wipe existing data to ensure clean restore
                    await db.transactions.clear()
                    await db.wallets.clear()
                    await db.categories.clear()

                    // --- 1. Import Wallets (Batch) ---
                    const walletIdMap = {} // Old ID -> New ID

                    // Prepare wallets for bulkAdd (remove old IDs to let auto-increment work)
                    const walletsToInsert = wallets.map(w => {
                        const oldId = w.id;
                        // Create a clean copy without ID
                        const { id, ...rest } = w;
                        return { ...rest, _oldId: oldId }; // Store old ID temporarily if needed, or rely on index
                    });

                    // Bulk add wallets
                    // Dexie bulkAdd returns the last key, not all keys. 
                    // To map old IDs to new IDs, we must iterate if we can't trust order.
                    // However, we can use bulkAdd and then re-fetch if names are unique? 
                    // No, names might not be unique.

                    // Optimization: For small number of wallets (usually < 10), sequential add is fine and safer for ID mapping.
                    // But for consistency with "bulk" plan, let's try to be efficient.
                    // Actually, simple loop for wallets is negligible performance hit.
                    for (const w of wallets) {
                        const oldId = w.id
                        const { id, ...rest } = w
                        const newId = await db.wallets.add(rest)
                        walletIdMap[oldId] = newId
                    }

                    // --- 2. Import Categories (Batch with Topological Sort) ---
                    const catIdMap = {} // Old ID -> New ID

                    // Separate parents (no parentId or null) and children
                    const parents = categories.filter(c => !c.parentId);
                    const children = categories.filter(c => c.parentId);

                    // Insert Parents
                    for (const p of parents) {
                        const oldId = p.id
                        const { id, ...rest } = p
                        const newId = await db.categories.add(rest)
                        catIdMap[oldId] = newId
                    }

                    // Insert Children (mapping their parentId)
                    const childrenToInsert = children.map(c => {
                        const oldId = c.id
                        const oldParentId = c.parentId
                        const { id, ...rest } = c

                        // Map parentId
                        const newParentId = catIdMap[oldParentId] || null; // Fallback to null if parent not found

                        // We can't easily map the NEW ID back to the OLD ID if we use bulkAdd here 
                        // unless we rely on order. 
                        // BUT, transactions need the NEW Category ID.
                        // So we MUST know the new ID for every old category ID.
                        // Thus, we must iterate children too to build the map.
                        return { ...rest, parentId: newParentId, _oldId: oldId }
                    });

                    // Inserting children loop to build map
                    for (const c of childrenToInsert) {
                        const { _oldId, ...rest } = c;
                        const newId = await db.categories.add(rest);
                        catIdMap[_oldId] = newId;
                    }

                    // --- 3. Import Transactions (Bulk) ---
                    // Now we have all maps, we can prepare transactions for ONE big bulkAdd.

                    const txsToInsert = transactions.map(t => {
                        const { id, ...rest } = t;

                        // Remap Foreign Keys
                        const newWalletId = walletIdMap[t.walletId] || t.walletId; // Fallback to old if not found (risky but better than null?)
                        const newCategoryId = catIdMap[t.categoryId] || t.categoryId;

                        // Clean up data
                        const date = t.date ? new Date(t.date) : new Date();
                        const tags = typeof t.tags === 'string' ? t.tags.split(',').map(tag => tag.trim()) : (t.tags || []);

                        return {
                            ...rest,
                            walletId: newWalletId,
                            categoryId: newCategoryId,
                            date,
                            tags
                        };
                    });

                    // THIS is where the performance gain is massive (1000+ items)
                    await db.transactions.bulkAdd(txsToInsert);
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

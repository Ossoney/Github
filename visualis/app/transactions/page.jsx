'use client'

import { useState, useMemo } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { TransactionFilters } from '@/components/transactions/TransactionFilters'
import { FullTransactionList } from '@/components/transactions/FullTransactionList'
import { TransactionForm } from '@/components/dashboard/TransactionForm'
import { Button } from '@/components/ui/UI'
import { ChevronLeft, Plus } from 'lucide-react'
import Link from 'next/link'
import { useLanguage } from '@/lib/i18n'
import { useStore } from '@/hooks/useStore'

export default function TransactionsPage() {
    const { t } = useLanguage()
    const { openTransactionModal } = useStore()

    // Filters State
    const [filters, setFilters] = useState({
        search: '',
        walletId: 'all',
        categoryId: 'all',
        type: 'all',
        startDate: '', // YYYY-MM-DD
        endDate: '',   // YYYY-MM-DD
        minAmount: '', // numeric string
        maxAmount: ''  // numeric string
    })

    // Fetch Lists for Dropdowns
    const wallets = useLiveQuery(() => db.wallets.toArray()) || []
    const categories = useLiveQuery(() => db.categories.toArray()) || []

    // Fetch & Filter Transactions
    const transactions = useLiveQuery(async () => {
        let collection = db.transactions.orderBy('date').reverse()

        // 1. Date Range Filter using indexes (fastest)
        if (filters.startDate && filters.endDate) {
            // Dexie 'between' is [lower, upper]
            // We need to handle time, so end date should be end of day
            const start = new Date(filters.startDate)
            const end = new Date(filters.endDate)
            end.setHours(23, 59, 59, 999)

            collection = db.transactions.where('date').between(start, end, true, true).reverse()
        } else if (filters.startDate) {
            const start = new Date(filters.startDate)
            collection = db.transactions.where('date').aboveOrEqual(start).reverse()
        }

        let results = await collection.toArray()

        // 2. Manual Filters for the rest
        // Dexie doesn't support complex AND queries natively efficiently without multiple indexes/compound indexes
        // For a local app, filtering in-memory 10-20k items is instant.

        // Enrich first (needed for Search)
        const catMap = new Map(categories.map(c => [c.id, c]))
        const walletMap = new Map(wallets.map(w => [w.id, w]))

        const enriched = results.map(tx => ({
            ...tx,
            category: catMap.get(tx.categoryId),
            wallet: walletMap.get(tx.walletId),
            toWallet: tx.toWalletId ? walletMap.get(tx.toWalletId) : null
        }))

        return enriched.filter(tx => {
            // Type
            if (filters.type !== 'all' && tx.type !== filters.type) return false

            // Wallet
            if (filters.walletId !== 'all' && Number(tx.walletId) !== Number(filters.walletId) && Number(tx.toWalletId) !== Number(filters.walletId)) return false

            // Category
            if (filters.categoryId !== 'all' && Number(tx.categoryId) !== Number(filters.categoryId)) return false

            // Amount Range
            if (filters.minAmount !== '' && tx.amount < Number(filters.minAmount)) return false
            if (filters.maxAmount !== '' && tx.amount > Number(filters.maxAmount)) return false

            // Search (Text)
            if (filters.search) {
                const searchLower = filters.search.toLowerCase()
                const desc = (tx.description || '').toLowerCase()
                const catName = (tx.category?.name || '').toLowerCase()
                const amount = String(tx.amount)

                // Search tags too
                const tagsMatch = tx.tags && tx.tags.some(tag => tag.toLowerCase().includes(searchLower))

                if (!desc.includes(searchLower) && !catName.includes(searchLower) && !amount.includes(searchLower) && !tagsMatch) {
                    return false
                }
            }

            return true
        })

    }, [filters, wallets, categories]) // Re-run when filters or meta-data changes

    return (
        <main className="pb-24 min-h-screen bg-slate-950">
            {/* Header */}
            <header className="flex items-center justify-between gap-4 mb-6 pt-6 sticky top-0 bg-slate-950/80 backdrop-blur-xl z-30 p-4 -mx-4 border-b border-white/5">
                <div className="flex items-center gap-2">
                    <Link href="/">
                        <Button variant="ghost" size="icon" className="rounded-full hover:bg-slate-800">
                            <ChevronLeft className="w-6 h-6 text-slate-400" />
                        </Button>
                    </Link>
                    <h1 className="text-xl font-bold text-slate-100">{t('transaction_history') || 'History'}</h1>
                </div>
                <Button onClick={openTransactionModal} size="sm" className="bg-sky-500 hover:bg-sky-600 rounded-full h-9 w-9 p-0">
                    <Plus className="w-5 h-5" />
                </Button>
            </header>

            <div className="space-y-6">
                <TransactionFilters
                    filters={filters}
                    onFilterChange={setFilters}
                    wallets={wallets}
                    categories={categories}
                />

                <FullTransactionList transactions={transactions} />
            </div>

            <TransactionForm />
        </main>
    )
}

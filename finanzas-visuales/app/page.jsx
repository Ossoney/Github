'use client'

import { useState, useEffect } from 'react'
import { WalletList } from '@/components/dashboard/WalletList'
import { TransactionList } from '@/components/dashboard/TransactionList'
import { MonthSelector } from '@/components/dashboard/MonthSelector'
import { TransactionForm } from '@/components/dashboard/TransactionForm'
import { BudgetList } from '@/components/dashboard/BudgetList'
import { MonthSummary } from '@/components/dashboard/MonthSummary'
import { EmotionSummary } from '@/components/dashboard/EmotionSummary'

import { Button } from '@/components/ui/UI'
import { useStore } from '@/hooks/useStore'
import { Plus, Download, User, Calendar, Search } from 'lucide-react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { formatCurrency } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

import Link from 'next/link'
import { WalletSummary } from '@/components/dashboard/WalletSummary'
import { PrivacyToggle } from '@/components/ui/PrivacyToggle'

export default function Dashboard() {
    const { openTransactionModal } = useStore()
    const { t } = useLanguage()

    // Fetch Settings for Avatar
    const settings = useLiveQuery(() => db.settings.get('global'))

    // Calculate total balance across all wallets
    const wallets = useLiveQuery(() => db.wallets.toArray())
    const totalBalance = wallets?.reduce((acc, curr) => acc + curr.balance, 0) || 0

    // Lifted State from MonthSummary for Contextual FAB
    const [expandedType, setExpandedType] = useState(null)


    return (
        <main className="pb-24">
            {/* Header */}
            <header className="flex justify-between items-center mb-6 pt-4">
                <div>
                    <div className="flex items-center gap-3">
                        <h1 className="text-3xl font-bold text-slate-100 tracking-tight">{t('app_title')}</h1>
                        <PrivacyToggle />
                    </div>

                    <p className="text-sm text-slate-500 font-medium -mt-1 ml-0.5">
                        {settings?.customizeHome && settings?.username
                            ? t('finances_of').replace('{name}', settings.username)
                            : t('app_subtitle')
                        }
                    </p>
                </div>

                <div className="flex items-center gap-3">
                    <Link href="/calendar">
                        <Button variant="ghost" size="icon" className="text-slate-400 hover:text-white">
                            <Calendar className="w-6 h-6" />
                        </Button>
                    </Link>

                    <Link href="/settings">
                        <div className="w-12 h-12 rounded-full bg-slate-800 border-2 border-slate-700 overflow-hidden hover:border-sky-500 transition-colors cursor-pointer flex items-center justify-center relative shadow-lg shadow-black/50">
                            {settings?.avatar ? (
                                <img src={settings.avatar} alt="Perfil" className="w-full h-full object-cover" />
                            ) : (
                                <span className="text-xl font-bold text-slate-400">
                                    {settings?.username ? settings.username.charAt(0).toUpperCase() : 'V'}
                                </span>
                            )}
                            {!settings?.username && !settings?.avatar && (
                                <div className="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full border-2 border-slate-900 animate-pulse" />
                            )}
                        </div>
                    </Link>
                </div>
            </header>

            {/* Wallet Summary (Accounts + Total) - MOVED TO TOP */}
            <section className="mb-6">
                <WalletSummary />
            </section>

            {/* Month Selector - MOVED BELOW */}
            <div className="mb-8">
                <MonthSelector />
            </div>

            {/* Month Summary (Income vs Expense vs Result) */}
            <section>
                <MonthSummary expandedType={expandedType} onExpand={setExpandedType} />
                <div className="mt-4">
                    <EmotionSummary />
                </div>
            </section>

            {/* Wallets Section (Hidden per user request, but kept in code) */}
            <section className="mb-8 hidden">
                <WalletList />
            </section>

            {/* Budgets & Transactions Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                {/* Recent Transactions (Left) */}
                <section className="h-full flex flex-col">
                    <div className="flex items-center justify-between mb-4 min-h-[3rem]">
                        <h2 className="text-lg font-semibold text-slate-200">{t('dashboard_recent_activity')}</h2>
                        <Link href="/transactions">
                            <Button variant="ghost" className="hover:bg-slate-800/50 hover:text-sky-400 transition-colors flex items-center gap-3 h-auto py-2 px-3">
                                <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">{t('advanced_search')}</span>
                                <Search className="w-8 h-8 text-slate-400" />
                            </Button>
                        </Link>
                    </div>
                    <div className="flex-1">
                        <TransactionList />
                    </div>
                </section>

                {/* Budgets Section (Right) */}
                <section className="h-full flex flex-col">
                    <div className="flex items-center justify-between mb-4 min-h-[3rem]">
                        <h2 className="text-lg font-semibold text-slate-200">{t('dashboard_monthly_budget')}</h2>
                    </div>
                    <div className="flex-1">
                        <BudgetList />
                    </div>
                </section>
            </div>

            {/* Floating Action Button (XL Size) */}
            <div className="fixed bottom-8 right-8 z-40">
                <Button
                    onClick={() => {
                        // Contextual Default: If expanded is 'income', default to income. Else expense.
                        // If expanded is 'result', we default to 'expense' (safest).
                        const defaultType = expandedType === 'income' ? 'income' : 'expense'
                        openTransactionModal(null, defaultType)
                    }}
                    className="h-20 w-20 rounded-full shadow-2xl shadow-sky-500/30 p-0 hover:scale-105 transition-transform bg-gradient-to-br from-sky-500 to-indigo-600 border-2 border-white/10"
                >
                    <Plus className="w-10 h-10 text-white" />
                </Button>
            </div>

            <TransactionForm />


        </main>
    )
}

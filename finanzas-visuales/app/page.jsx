'use client'

import { useState, useEffect } from 'react'
import { WalletList } from '@/components/dashboard/WalletList'
import { TransactionList } from '@/components/dashboard/TransactionList'
import { MonthSelector } from '@/components/dashboard/MonthSelector'
import { TransactionForm } from '@/components/dashboard/TransactionForm'
import { BudgetList } from '@/components/dashboard/BudgetList'
import { MonthSummary } from '@/components/dashboard/MonthSummary'

import { Button } from '@/components/ui/UI'
import { useStore } from '@/hooks/useStore'
import { Plus, Download, User } from 'lucide-react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { formatCurrency } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

import Link from 'next/link'
import { WalletSummary } from '@/components/dashboard/WalletSummary'

export default function Dashboard() {
    const { openTransactionModal } = useStore()
    const { t } = useLanguage()

    // Fetch Settings for Avatar
    const settings = useLiveQuery(() => db.settings.get('global'))

    // Calculate total balance across all wallets
    const wallets = useLiveQuery(() => db.wallets.toArray())
    const totalBalance = wallets?.reduce((acc, curr) => acc + curr.balance, 0) || 0



    return (
        <main className="pb-24">
            {/* Header */}
            <header className="flex justify-between items-center mb-6 pt-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 tracking-tight">{t('app_title')}</h1>

                    <p className="text-sm text-slate-500 font-medium -mt-1 ml-0.5">
                        {settings?.customizeHome && settings?.username
                            ? t('finances_of').replace('{name}', settings.username)
                            : t('app_subtitle')
                        }
                    </p>
                </div>

                <div className="flex items-center gap-3">
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
                <MonthSummary />
            </section>

            {/* Wallets Section (Hidden per user request, but kept in code) */}
            <section className="mb-8 hidden">
                <WalletList />
            </section>

            {/* Budgets & Transactions Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Recent Transactions (Left) */}
                <section>
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold text-slate-200">{t('dashboard_recent_activity')}</h2>
                        <Link href="/transactions" className="text-xs text-sky-400 font-medium hover:text-sky-300 transition-colors">
                            {t('see_all') || 'See All'}
                        </Link>
                    </div>
                    <TransactionList />
                </section>

                {/* Budgets Section (Right) */}
                <section>
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold text-slate-200">{t('dashboard_monthly_budget')}</h2>
                    </div>
                    <BudgetList />
                </section>
            </div>

            {/* Floating Action Button (XL Size) */}
            <div className="fixed bottom-8 right-8 z-40">
                <Button
                    onClick={openTransactionModal}
                    className="h-20 w-20 rounded-full shadow-2xl shadow-sky-500/30 p-0 hover:scale-105 transition-transform bg-gradient-to-br from-sky-500 to-indigo-600 border-2 border-white/10"
                >
                    <Plus className="w-10 h-10 text-white" />
                </Button>
            </div>

            <TransactionForm />


        </main>
    )
}

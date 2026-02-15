'use client'

import { useState } from 'react'
import { ChevronLeft, User, LayoutGrid, Calculator, Repeat, Tag, Wallet, Palette, Database } from 'lucide-react'
import { ProfileSettings, ThemeSettings, DataSettings, LanguageSettings, CurrencySettings } from '@/components/settings/SystemSettings'
import { AccountManager } from '@/components/settings/AccountManager'
import { CategoryManager } from '@/components/settings/CategoryManager'
import { RecurringManager } from '@/components/settings/RecurringManager'
import { TagManager } from '@/components/settings/TagManager'
import { BudgetManager } from '@/components/settings/BudgetManager'
import { Button } from '@/components/ui/Button'
import Link from 'next/link'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

export default function SettingsPage() {
    const [activeTab, setActiveTab] = useState('profile')
    const { t } = useLanguage()

    const menuItems = [
        { id: 'profile', label: t('profile'), icon: User },
        { id: 'appearance', label: t('appearance'), icon: Palette },
        { id: 'accounts', label: t('accounts'), icon: Wallet },
        { id: 'categories', label: t('categories'), icon: LayoutGrid },
        { id: 'budgets', label: t('budgets'), icon: Calculator },
        { id: 'recurring', label: t('recurring'), icon: Repeat },
        { id: 'tags', label: t('tags'), icon: Tag },
        { id: 'data', label: t('data'), icon: Database },
    ]

    return (
        <div className="pb-24">
            {/* Header */}
            <header className="flex items-center gap-4 mb-8 pt-4">
                <Link href="/">
                    <Button variant="ghost" size="icon" className="rounded-full">
                        <ChevronLeft className="w-6 h-6" />
                    </Button>
                </Link>
                <h1 className="text-2xl font-bold text-slate-100">{t('settings')}</h1>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">

                {/* Sidebar Menu */}
                <nav className="md:col-span-1 flex md:flex-col gap-2 overflow-x-auto pb-2 md:pb-0 hide-scrollbar">
                    {menuItems.map(item => {
                        const Icon = item.icon
                        const isActive = activeTab === item.id
                        return (
                            <button
                                key={item.id}
                                onClick={() => setActiveTab(item.id)}
                                className={cn(
                                    "flex items-center gap-3 px-4 py-3 rounded-xl transition-all whitespace-nowrap",
                                    isActive
                                        ? "bg-sky-500/10 text-sky-400 border border-sky-500/20"
                                        : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
                                )}
                            >
                                <Icon className="w-5 h-5" />
                                <span className="font-medium">{item.label}</span>
                            </button>
                        )
                    })}
                </nav>

                {/* Content Area */}
                <section className="md:col-span-3 space-y-6">
                    {activeTab === 'profile' && (
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
                            <ProfileSettings className="w-full lg:max-w-md" />
                            <div className="space-y-6">
                                <LanguageSettings />
                                <CurrencySettings />
                            </div>
                        </div>
                    )}
                    {activeTab === 'appearance' && <ThemeSettings />}
                    {activeTab === 'accounts' && <AccountManager />}
                    {activeTab === 'categories' && <CategoryManager />}
                    {activeTab === 'recurring' && <RecurringManager />}
                    {activeTab === 'tags' && <TagManager />}
                    {activeTab === 'budgets' && <BudgetManager />}
                    {activeTab === 'data' && <DataSettings />}
                </section>

            </div>
        </div>
    )
}

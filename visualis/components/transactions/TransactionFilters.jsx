'use client'

import { useState } from 'react'
import { useLanguage } from '@/lib/i18n'
import { Search, Filter, X, DollarSign } from 'lucide-react'
import { Button } from '@/components/ui/UI'
import { format } from 'date-fns'
import { es, enUS, gl, eu } from 'date-fns/locale'

export function TransactionFilters({ filters, onFilterChange, wallets, categories }) {
    const { t, language } = useLanguage()
    const [showFilters, setShowFilters] = useState(false)

    // Helper to clear all filters
    const clearFilters = () => {
        onFilterChange({
            search: '',
            walletId: 'all',
            categoryId: 'all',
            type: 'all',
            startDate: '',
            endDate: '',
            minAmount: '',
            maxAmount: ''
        })
    }

    const activeFiltersCount = [
        filters.walletId !== 'all',
        filters.categoryId !== 'all',
        filters.type !== 'all',
        filters.startDate,
        filters.endDate,
        filters.minAmount,
        filters.maxAmount
    ].filter(Boolean).length

    return (
        <div className="space-y-4">
            {/* Search Bar & Toggle */}
            <div className="flex gap-2">
                <div className="relative flex-1">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">
                        <Search className="w-4 h-4" />
                    </div>
                    <input
                        type="text"
                        placeholder={t('search_placeholder') || 'Search transactions...'}
                        value={filters.search}
                        onChange={(e) => onFilterChange({ ...filters, search: e.target.value })}
                        className="w-full pl-9 pr-4 py-2 bg-slate-900/50 border border-slate-800 rounded-xl focus:outline-none focus:border-sky-500 transition-colors text-sm"
                    />
                </div>
                <Button
                    variant="outline"
                    onClick={() => setShowFilters(!showFilters)}
                    className={`border-slate-800 hover:bg-slate-800 ${showFilters || activeFiltersCount > 0 ? 'bg-sky-500/10 border-sky-500/50 text-sky-400' : 'text-slate-400'}`}
                >
                    <Filter className="w-4 h-4 mr-2" />
                    {t('filters') || 'Filters'}
                    {activeFiltersCount > 0 && (
                        <span className="ml-1 bg-sky-500 text-white text-[10px] px-1.5 py-0.5 rounded-full">
                            {activeFiltersCount}
                        </span>
                    )}
                </Button>
            </div>

            {/* Collapsible Filters */}
            {showFilters && (
                <div className="p-4 bg-slate-900/30 border border-slate-800 rounded-xl space-y-4 animate-in slide-in-from-top-2">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

                        {/* Type Filter */}
                        <div className="space-y-1">
                            <label className="text-xs font-medium text-slate-500 uppercase">{t('type') || 'Type'}</label>
                            <select
                                value={filters.type}
                                onChange={(e) => onFilterChange({ ...filters, type: e.target.value })}
                                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-sky-500"
                            >
                                <option value="all">{t('all') || 'All'}</option>
                                <option value="income">{t('income')}</option>
                                <option value="expense">{t('expense')}</option>
                            </select>
                        </div>

                        {/* Wallet Filter */}
                        <div className="space-y-1">
                            <label className="text-xs font-medium text-slate-500 uppercase">{t('wallet')}</label>
                            <select
                                value={filters.walletId}
                                onChange={(e) => onFilterChange({ ...filters, walletId: e.target.value })}
                                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-sky-500"
                            >
                                <option value="all">{t('all') || 'All'}</option>
                                {wallets.map(w => (
                                    <option key={w.id} value={w.id}>{w.name}</option>
                                ))}
                            </select>
                        </div>

                        {/* Category Filter */}
                        <div className="space-y-1">
                            <label className="text-xs font-medium text-slate-500 uppercase">{t('category')}</label>
                            <select
                                value={filters.categoryId}
                                onChange={(e) => onFilterChange({ ...filters, categoryId: e.target.value })}
                                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-sky-500"
                            >
                                <option value="all">{t('all') || 'All'}</option>
                                {categories.map(c => (
                                    <option key={c.id} value={c.id}>{c.name}</option>
                                ))}
                            </select>
                        </div>

                        {/* Date Range */}
                        <div className="space-y-1">
                            <label className="text-xs font-medium text-slate-500 uppercase">{t('date')}</label>
                            <div className="flex items-center gap-2">
                                <input
                                    type="date"
                                    value={filters.startDate}
                                    onChange={(e) => onFilterChange({ ...filters, startDate: e.target.value })}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-sky-500"
                                />
                                <span className="text-slate-500">-</span>
                                <input
                                    type="date"
                                    value={filters.endDate}
                                    onChange={(e) => onFilterChange({ ...filters, endDate: e.target.value })}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-sky-500"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Amount Range */}
                    <div className="space-y-1">
                        <label className="text-xs font-medium text-slate-500 uppercase flex items-center gap-1">
                            <DollarSign className="w-3 h-3" />
                            {t('amount') || 'Amount'}
                        </label>
                        <div className="flex items-center gap-2">
                            <div className="relative flex-1">
                                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-xs">min</span>
                                <input
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    placeholder="0"
                                    value={filters.minAmount}
                                    onChange={(e) => onFilterChange({ ...filters, minAmount: e.target.value })}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:border-sky-500 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                />
                            </div>
                            <span className="text-slate-500 shrink-0">—</span>
                            <div className="relative flex-1">
                                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-xs">max</span>
                                <input
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    placeholder="∞"
                                    value={filters.maxAmount}
                                    onChange={(e) => onFilterChange({ ...filters, maxAmount: e.target.value })}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:border-sky-500 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                />
                            </div>
                        </div>
                    </div>

                    <div className="flex justify-end border-t border-slate-800 pt-3">
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={clearFilters}
                            className="text-red-400 hover:text-red-300 hover:bg-red-900/20"
                        >
                            <X className="w-4 h-4 mr-2" />
                            {t('clear_filters') || 'Clear Filters'}
                        </Button>
                    </div>
                </div>
            )}
        </div>
    )
}

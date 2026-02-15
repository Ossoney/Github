import { useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { startOfMonth, endOfMonth, subMonths, format } from 'date-fns'
import { ArrowUpCircle, ArrowDownCircle, ChevronDown, ChevronUp, BarChart3, PieChart } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useStore } from '@/hooks/useStore'
import { useLanguage } from '@/lib/i18n'

export function MonthSummary() {
    const { currentDate } = useStore()
    const { formatMoney, t, tCategory, locale } = useLanguage()

    // UI State
    const [expandedType, setExpandedType] = useState(null) // 'income', 'expense', 'result'
    const [viewMode, setViewMode] = useState('breakdown') // 'breakdown', 'history'
    const [historyLimit, setHistoryLimit] = useState(6) // 6, 12, 24

    // 1. Current Month Stats
    const stats = useLiveQuery(async () => {
        const start = startOfMonth(currentDate)
        const end = endOfMonth(currentDate)
        const transactions = await db.transactions
            .where('date')
            .between(start, end, true, true)
            .toArray()

        const income = transactions.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0)
        const expense = transactions.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0)

        // Group by Category for Breakdown
        const categories = await db.categories.toArray()
        const breakdown = { income: [], expense: [] }

        // Helper to group
        const groupByCategory = (type) => {
            const relevantTx = transactions.filter(t => t.type === type)
            const grouped = relevantTx.reduce((acc, tx) => {
                const cat = categories.find(c => c.id === tx.categoryId) || { name: 'Sin Categoría', color: '#cbd5e1' }
                // Handle subcategories? For now just direct category
                if (!acc[cat.name]) acc[cat.name] = { name: cat.name, amount: 0, color: cat.color, count: 0 }
                acc[cat.name].amount += tx.amount
                acc[cat.name].count += 1
                return acc
            }, {})
            return Object.values(grouped).sort((a, b) => b.amount - a.amount)
        }

        breakdown.income = groupByCategory('income')
        breakdown.expense = groupByCategory('expense')

        return { income, expense, result: income - expense, breakdown }
    }, [currentDate])

    // 2. Historical Stats (Dynamic Limit)
    const history = useLiveQuery(async () => {
        const data = []
        for (let i = historyLimit - 1; i >= 0; i--) {
            const date = subMonths(currentDate, i)
            const start = startOfMonth(date)
            const end = endOfMonth(date)
            const txs = await db.transactions.where('date').between(start, end, true, true).toArray()

            const inc = txs.filter(t => t.type === 'income').reduce((s, t) => s + t.amount, 0)
            const exp = txs.filter(t => t.type === 'expense').reduce((s, t) => s + t.amount, 0)

            data.push({
                month: format(date, 'MMM', { locale }), // e.g., "Feb"
                fullDate: date,
                income: inc,
                expense: exp,
                result: inc - exp
            })
        }
        return data
    }, [currentDate, locale, historyLimit])

    const handleExpand = (type) => {
        if (expandedType === type) {
            setExpandedType(null)
        } else {
            setExpandedType(type)
            setViewMode('breakdown')
        }
    }

    const renderBreakdown = (type) => {
        if (!stats?.breakdown) return null

        let data = []
        let total = 0

        if (type === 'income') {
            data = stats.breakdown.income
            total = data.reduce((sum, item) => sum + item.amount, 0)
        } else if (type === 'expense') {
            data = stats.breakdown.expense
            total = data.reduce((sum, item) => sum + item.amount, 0)
        } else {
            // Result View: Show Income vs Expenses on one bar
            data = [
                { name: t('income'), amount: stats.income, color: '#10b981', count: 1 }, // emerald-500
                { name: t('expense'), amount: stats.expense, color: '#f43f5e', count: 1 }   // rose-500
            ]
            total = stats.income + stats.expense // Total volume for percentage calculation
        }

        if (total === 0) return <p className="text-center text-slate-500 py-4">No hay datos para este mes.</p>

        return (
            <div className="space-y-6 pt-2">
                {/* Single Stacked Bar */}
                <div className="h-8 w-full bg-slate-800 rounded-full overflow-hidden flex shadow-inner">
                    {data.map((item, idx) => {
                        const pct = (item.amount / total) * 100
                        if (pct < 1) return null // Hide tiny segments
                        return (
                            <div
                                key={idx}
                                style={{ width: `${pct}%`, backgroundColor: item.color }}
                                className="h-full border-r border-slate-900/50 last:border-0 hover:brightness-110 transition-all relative group first:rounded-l-full last:rounded-r-full"
                            >
                                {/* Tooltip on hover */}
                                <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-900 border border-slate-700 px-2 py-1 rounded text-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10 shadow-xl font-bold">
                                    {tCategory(item.name)}: {formatMoney(item.amount)} ({Math.round(pct)}%)
                                </div>
                            </div>
                        )
                    })}
                </div>

                {/* Legend Below */}
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    {data.map((item, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-sm">
                            <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: item.color }} />
                            <div className="flex flex-col">
                                <span className="text-slate-300 font-medium truncate max-w-[120px]" title={tCategory(item.name)}>
                                    {tCategory(item.name)}
                                </span>
                                <span className="text-slate-500 text-xs">
                                    {formatMoney(item.amount)} ({Math.round((item.amount / total) * 100)}%)
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        )
    }

    const renderHistory = (type) => {
        if (!history) return null
        // Find max value for scaling
        const maxVal = Math.max(...history.map(h =>
            type === 'result' ? Math.abs(h.result) : (type === 'income' ? h.income : h.expense)
        )) || 1

        return (
            <div className="flex justify-between items-end h-32 pt-4 px-2 gap-2">
                {history.map((h, i) => {
                    const val = type === 'result' ? h.result : (type === 'income' ? h.income : h.expense)
                    const height = Math.abs(val) / maxVal * 100
                    const isCurrent = i === historyLimit - 1 // Last one is current

                    let barColor = 'bg-slate-700'
                    if (type === 'income') barColor = isCurrent ? 'bg-emerald-500' : 'bg-emerald-500/30'
                    if (type === 'expense') barColor = isCurrent ? 'bg-rose-500' : 'bg-rose-500/30'
                    if (type === 'result') barColor = val >= 0
                        ? (isCurrent ? 'bg-sky-500' : 'bg-sky-500/30')
                        : (isCurrent ? 'bg-orange-500' : 'bg-orange-500/30')

                    return (
                        <div key={i} className="flex-1 flex flex-col items-center gap-1 group relative">
                            {/* Tooltip */}
                            <div className="absolute -top-8 bg-slate-800 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10 border border-slate-700">
                                {formatMoney(val)}
                            </div>

                            <div className="w-full bg-slate-800/50 rounded-t-lg relative flex items-end h-full overflow-hidden">
                                <div
                                    className={cn("w-full transition-all duration-500", barColor)}
                                    style={{ height: `${height || 0}%` }}
                                />
                            </div>
                            <span className={cn("text-[10px] font-medium uppercase", isCurrent ? "text-slate-200" : "text-slate-500")}>
                                {h.month}
                            </span>
                        </div>
                    )
                })}
            </div>
        )
    }

    return (
        <div className="mb-8 space-y-4">
            {/* MAIN CARDS */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Income */}
                <button
                    onClick={() => handleExpand('income')}
                    className={cn(
                        "p-4 rounded-2xl flex flex-col items-center justify-center gap-2 transition-all border",
                        expandedType === 'income' ? "bg-emerald-500/20 border-emerald-500 ring-1 ring-emerald-500/50" : "bg-emerald-500/10 border-emerald-500/20 hover:bg-emerald-500/15"
                    )}
                >
                    <span className="text-emerald-400 text-sm font-medium flex items-center gap-2">
                        <ArrowUpCircle className="w-4 h-4" /> {t('income')}
                        {expandedType === 'income' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    </span>
                    <span className="text-2xl font-bold text-emerald-100">
                        {formatMoney(stats?.income || 0)}
                    </span>
                </button>

                {/* Expenses */}
                <button
                    onClick={() => handleExpand('expense')}
                    className={cn(
                        "p-4 rounded-2xl flex flex-col items-center justify-center gap-2 transition-all border",
                        expandedType === 'expense' ? "bg-rose-500/20 border-rose-500 ring-1 ring-rose-500/50" : "bg-rose-500/10 border-rose-500/20 hover:bg-rose-500/15"
                    )}
                >
                    <span className="text-rose-400 text-sm font-medium flex items-center gap-2">
                        <ArrowDownCircle className="w-4 h-4" /> {t('expense')}
                        {expandedType === 'expense' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    </span>
                    <span className="text-2xl font-bold text-rose-100">
                        {formatMoney(stats?.expense || 0)}
                    </span>
                </button>

                {/* Result (Net) */}
                <button
                    onClick={() => handleExpand('result')}
                    className={cn(
                        "border p-4 rounded-2xl flex flex-col items-center justify-center gap-2 transition-all",
                        (stats?.result || 0) >= 0
                            ? (expandedType === 'result' ? "bg-sky-500/20 border-sky-500 ring-1 ring-sky-500/50" : "bg-sky-500/10 border-sky-500/20 hover:bg-sky-500/15")
                            : (expandedType === 'result' ? "bg-orange-500/20 border-orange-500 ring-1 ring-orange-500/50" : "bg-orange-500/10 border-orange-500/20 hover:bg-orange-500/15")
                    )}
                >
                    <span className={cn(
                        "text-sm font-medium flex items-center gap-2",
                        (stats?.result || 0) >= 0 ? "text-sky-400" : "text-orange-400"
                    )}>
                        {t('total_balance')}
                        {expandedType === 'result' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    </span>
                    <span className={cn(
                        "text-2xl font-bold",
                        (stats?.result || 0) >= 0 ? "text-sky-100" : "text-orange-100"
                    )}>
                        {(stats?.result || 0) > 0 ? '+' : ''}{formatMoney(stats?.result || 0)}
                    </span>
                </button>
            </div>

            {/* EXPANDED SECTION */}
            {expandedType && (
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 animate-in slide-in-from-top-4 fade-in duration-300">
                    {/* Tabs */}
                    <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                        <h3 className="text-lg font-semibold capitalize text-slate-200">
                            {expandedType === 'result' ? t('total_balance') : (expandedType === 'income' ? t('income') : t('expense'))}
                        </h3>
                        <div className="flex gap-2 bg-slate-950 p-1 rounded-lg">
                            <button
                                onClick={() => setViewMode('breakdown')}
                                className={cn("px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-2 transition-all", viewMode === 'breakdown' ? "bg-slate-800 text-white shadow" : "text-slate-500 hover:text-slate-300")}
                            >
                                <PieChart className="w-3 h-3" /> Desglose
                            </button>
                            <div className="flex gap-1 ml-2 border-l border-slate-800 pl-2">
                                {[6, 12, 24].map(limit => (
                                    <button
                                        key={limit}
                                        onClick={() => {
                                            setViewMode('history')
                                            setHistoryLimit(limit)
                                        }}
                                        className={cn(
                                            "px-2 py-1.5 rounded-md text-[10px] font-bold transition-all",
                                            viewMode === 'history' && historyLimit === limit
                                                ? "bg-slate-700 text-white shadow"
                                                : "text-slate-500 hover:text-slate-300 hover:bg-slate-800/50"
                                        )}
                                    >
                                        {limit}M
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Content */}
                    <div className="min-h-[150px]">
                        {viewMode === 'breakdown' ? renderBreakdown(expandedType) : renderHistory(expandedType)}
                    </div>
                </div>
            )}
        </div>
    )
}

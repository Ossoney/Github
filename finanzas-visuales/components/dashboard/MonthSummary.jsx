import { useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { startOfMonth, endOfMonth, subMonths, format } from 'date-fns'
import { ArrowUpCircle, ArrowDownCircle, ChevronDown, ChevronUp, BarChart3, PieChart, TrendingUp, TrendingDown, Trophy, Flame, Target, Minus, Zap, Infinity as InfinityIcon } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useStore } from '@/hooks/useStore'
import { useLanguage } from '@/lib/i18n'
import { Money } from '@/components/ui/Money'

export function MonthSummary({ expandedType, onExpand }) {
    const { currentDate, selectedWalletId } = useStore()
    const { t, tCategory, locale } = useLanguage()

    // UI State
    // expandedType is now controlled by parent
    const [viewMode, setViewMode] = useState('breakdown') // 'breakdown', 'history'
    const [historyLimit, setHistoryLimit] = useState(6) // 6, 12, 24, '∞'
    const [drillCategory, setDrillCategory] = useState(null) // { name, subcategories } or null

    // 0. Check data availability for Smart Intervals
    const availableMonths = useLiveQuery(async () => {
        let firstTx;
        if (selectedWalletId) {
            // Get all transactions for this wallet and sort by date to find the earliest
            const walletTxs = await db.transactions.where('walletId').equals(selectedWalletId).sortBy('date')
            firstTx = walletTxs[0]
        } else {
            // Global earliest transaction
            firstTx = await db.transactions.orderBy('date').first()
        }

        if (!firstTx) return 0
        const now = new Date()
        const first = new Date(firstTx.date)
        const months = (now.getFullYear() - first.getFullYear()) * 12 + (now.getMonth() - first.getMonth())
        return Math.max(0, months)
    }, [selectedWalletId])

    const showHistoryOptions = availableMonths >= 6

    // 1. Current Month Stats
    const stats = useLiveQuery(async () => {
        const start = startOfMonth(currentDate)
        const end = endOfMonth(currentDate)

        let query = db.transactions.where('date').between(start, end, true, true)

        const transactions = await query.toArray()
        // Filter by wallet after fetching or use compound index if available
        // For simplicity and since month volume is usually low, we filter the array:
        const filteredTxs = selectedWalletId
            ? transactions.filter(t => t.walletId === selectedWalletId)
            : transactions

        const income = filteredTxs.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0)
        const expense = filteredTxs.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0)


        // Group by Category for Breakdown
        const categories = await db.categories.toArray()
        const breakdown = { income: [], expense: [] }

        // Helper to group by TOP-LEVEL parent category
        const groupByCategory = (type) => {
            const relevantTx = filteredTxs.filter(t => t.type === type)
            const grouped = relevantTx.reduce((acc, tx) => {
                const cat = categories.find(c => String(c.id) === String(tx.categoryId)) || { name: 'Sin Categoría', color: '#cbd5e1', parentId: null }
                // Walk up to the top-level parent
                const parent = cat.parentId
                    ? (categories.find(c => String(c.id) === String(cat.parentId)) || cat)
                    : cat

                if (!acc[parent.name]) {
                    acc[parent.name] = {
                        name: parent.name,
                        amount: 0,
                        color: parent.color || '#cbd5e1',
                        count: 0,
                        id: parent.id,
                        subcategories: {}
                    }
                }
                acc[parent.name].amount += tx.amount
                acc[parent.name].count += 1

                // Track subcategory (the direct category of the tx, if different from parent)
                const subName = cat.parentId ? cat.name : null
                if (subName) {
                    if (!acc[parent.name].subcategories[subName]) {
                        acc[parent.name].subcategories[subName] = { name: subName, amount: 0, color: cat.color || parent.color || '#cbd5e1', count: 0 }
                    }
                    acc[parent.name].subcategories[subName].amount += tx.amount
                    acc[parent.name].subcategories[subName].count += 1
                }

                return acc
            }, {})

            return Object.values(grouped)
                .map(g => ({ ...g, subcategories: Object.values(g.subcategories).sort((a, b) => b.amount - a.amount) }))
                .sort((a, b) => b.amount - a.amount)
        }

        breakdown.income = groupByCategory('income')
        breakdown.expense = groupByCategory('expense')

        // 1.1 Previous Month Stats for comparison
        const prevStart = startOfMonth(subMonths(currentDate, 1))
        const prevEnd = endOfMonth(subMonths(currentDate, 1))
        const prevTxsRaw = await db.transactions.where('date').between(prevStart, prevEnd, true, true).toArray()
        const prevTxs = selectedWalletId
            ? prevTxsRaw.filter(t => t.walletId === selectedWalletId)
            : prevTxsRaw

        const prevIncome = prevTxs.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0)
        const prevExpense = prevTxs.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0)
        const prevResult = prevIncome - prevExpense

        return { income, expense, result: income - expense, breakdown, prevIncome, prevExpense, prevResult }
    }, [currentDate, selectedWalletId])

    // 2. Historical Stats (Dynamic Limit)
    const history = useLiveQuery(async () => {
        if (!showHistoryOptions && viewMode === 'history') return []

        const limit = historyLimit === '∞' ? (availableMonths + 1) : historyLimit
        const data = []
        for (let i = limit - 1; i >= 0; i--) {
            const date = subMonths(currentDate, i)
            const start = startOfMonth(date)
            const end = endOfMonth(date)
            const txsRaw = await db.transactions.where('date').between(start, end, true, true).toArray()
            const txs = selectedWalletId
                ? txsRaw.filter(t => t.walletId === selectedWalletId)
                : txsRaw

            const inc = txs.filter(t => t.type === 'income').reduce((s, t) => s + t.amount, 0)
            const exp = txs.filter(t => t.type === 'expense').reduce((s, t) => s + t.amount, 0)

            const monthLabel = (historyLimit === '∞' || historyLimit >= 12)
                ? format(date, 'MMM yy', { locale })
                : format(date, 'MMM', { locale })

            data.push({
                month: monthLabel,
                fullDate: date,
                income: inc,
                expense: exp,
                result: inc - exp
            })
        }
        return data
    }, [currentDate, locale, historyLimit, viewMode, showHistoryOptions, selectedWalletId, availableMonths])

    const handleExpand = (type) => {
        if (onExpand) {
            onExpand(expandedType === type ? null : type)
        }
        if (expandedType !== type) {
            setViewMode('breakdown')
            setDrillCategory(null)
        }
    }

    const renderBreakdown = (type) => {
        if (!stats?.breakdown) return null

        let data = []
        let total = 0

        if (type === 'result') {
            data = [
                { name: t('income'), amount: stats.income, color: '#10b981', subcategories: [] },
                { name: t('expense'), amount: stats.expense, color: '#f43f5e', subcategories: [] }
            ]
            total = stats.income + stats.expense
        } else {
            data = type === 'income' ? stats.breakdown.income : stats.breakdown.expense
            total = data.reduce((s, d) => s + d.amount, 0)
        }

        if (total === 0) return <p className="text-center text-slate-500 py-4">No hay datos para este mes.</p>

        return (
            <div className="space-y-4 pt-2">

                {/* Stacked Bar — always top-level */}
                <div className="h-8 w-full bg-slate-800 rounded-full overflow-hidden flex shadow-inner">
                    {data.map((item, idx) => {
                        const pct = (item.amount / total) * 100
                        if (pct < 1) return null
                        const hasChildren = item.subcategories?.length > 0
                        return (
                            <div
                                key={idx}
                                onClick={hasChildren ? () => setDrillCategory(drillCategory === item.name ? null : item.name) : undefined}
                                style={{ width: `${pct}%`, backgroundColor: item.color }}
                                className={cn(
                                    'h-full border-r border-slate-900/50 last:border-0 transition-all relative group first:rounded-l-full last:rounded-r-full',
                                    hasChildren ? 'cursor-pointer hover:brightness-125' : 'hover:brightness-110',
                                    drillCategory === item.name ? 'brightness-125 ring-1 ring-white/20' : ''
                                )}
                            >
                                <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-900 border border-slate-700 px-2 py-1 rounded text-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10 shadow-xl font-bold flex items-center gap-1">
                                    {tCategory(item.name)}: <Money amount={item.amount} showDecimals={false} /> ({Math.round(pct)}%)
                                </div>
                            </div>
                        )
                    })}
                </div>

                {/* Legend with inline accordion */}
                <div className="space-y-1">
                    {data.map((item, idx) => {
                        const pct = Math.round((item.amount / total) * 100)
                        const hasChildren = item.subcategories?.length > 0
                        const isExpanded = drillCategory === item.name
                        return (
                            <div key={idx}>
                                {/* Parent row */}
                                <div
                                    onClick={hasChildren ? () => setDrillCategory(isExpanded ? null : item.name) : undefined}
                                    className={cn(
                                        'flex items-center gap-2 text-sm rounded-lg px-2 py-1.5 transition-colors',
                                        hasChildren ? 'cursor-pointer hover:bg-slate-800/60' : '',
                                        isExpanded ? 'bg-slate-800/60' : ''
                                    )}
                                >
                                    <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: item.color }} />
                                    <div className="flex flex-col min-w-0 flex-1">
                                        <span className="text-slate-300 font-medium truncate" title={tCategory(item.name)}>
                                            {tCategory(item.name)}
                                        </span>
                                        <span className="text-slate-500 text-xs">
                                            <Money amount={item.amount} showDecimals={false} /> ({pct}%)
                                        </span>
                                    </div>
                                    {hasChildren && (
                                        <ChevronDown className={cn('w-3.5 h-3.5 text-slate-500 transition-transform shrink-0', isExpanded ? 'rotate-180' : '')} />
                                    )}
                                </div>

                                {/* Subcategories (inline accordion) */}
                                {isExpanded && hasChildren && (
                                    <div className="ml-5 mt-0.5 mb-1 space-y-0.5 border-l-2 border-slate-700 pl-3">
                                        {item.subcategories.map((sub, sIdx) => {
                                            const subPct = Math.round((sub.amount / item.amount) * 100)
                                            return (
                                                <div key={sIdx} className="flex items-center gap-2 text-xs py-1 px-1.5 rounded hover:bg-slate-800/40 transition-colors">
                                                    <div className="w-2 h-2 rounded-full shrink-0 opacity-70" style={{ backgroundColor: item.color }} />
                                                    <span className="text-slate-400 truncate flex-1">{tCategory(sub.name)}</span>
                                                    <span className="text-slate-500 shrink-0"><Money amount={sub.amount} showDecimals={false} /></span>
                                                    <span className="text-slate-600 shrink-0 w-8 text-right">{subPct}%</span>
                                                </div>
                                            )
                                        })}
                                    </div>
                                )}
                            </div>
                        )
                    })}
                </div>
            </div>
        )
    }


    const renderHistory = (type) => {
        if (!history || history.length === 0) return null

        const getValue = (h) => type === 'result' ? h.result : (type === 'income' ? h.income : h.expense)
        const values = history.map(getValue)

        // Computed stats
        const total = type === 'expense' ? -Math.abs(values.reduce((a, b) => a + b, 0)) : values.reduce((a, b) => a + b, 0)
        const avgIncome = history.reduce((s, h) => s + h.income, 0) / history.length
        const avgExpense = history.reduce((s, h) => s + h.expense, 0) / history.length

        // Best/Worst Logic: for expenses, "best" is less spending (min), "worst" is more spending (max)
        const bestIdx = type === 'expense'
            ? values.indexOf(Math.min(...values))
            : values.indexOf(Math.max(...values))
        const worstIdx = type === 'expense'
            ? values.indexOf(Math.max(...values))
            : values.indexOf(Math.min(...values))

        // Positive months count: based on net result (income > expense)
        // BUT if viewing expenses, we count months where expense > income
        const positiveMonths = type === 'expense'
            ? history.filter(h => h.expense > h.income).length
            : history.filter(h => h.result > 0).length
        const streakPositive = positiveMonths > 0


        // Period aggregate totals for stacked bar
        const totalIncome = history.reduce((s, h) => s + h.income, 0)
        const totalExpense = history.reduce((s, h) => s + h.expense, 0)
        const barData = type === 'result'
            ? [
                { label: 'Ingresos', amount: totalIncome, color: '#10b981' },
                { label: 'Gastos', amount: totalExpense, color: '#f43f5e' },
            ]
            : [
                {
                    label: type === 'income' ? 'Ingresos' : 'Gastos',
                    amount: Math.abs(total),
                    color: type === 'income' ? '#10b981' : '#f43f5e'
                },
            ]
        const barDataTotal = barData.reduce((s, b) => s + b.amount, 0) || 1

        return (
            <div className="space-y-3">

                {/* Period aggregate stacked bar */}
                <div className="space-y-2">
                    <div className="h-7 w-full bg-slate-800 rounded-full overflow-hidden flex shadow-inner">
                        {barData.map((seg, idx) => {
                            const pct = (seg.amount / barDataTotal) * 100
                            if (pct < 1) return null
                            return (
                                <div
                                    key={idx}
                                    style={{ width: `${pct}%`, backgroundColor: seg.color }}
                                    className="h-full border-r border-slate-900/50 last:border-0 hover:brightness-110 transition-all relative group first:rounded-l-full last:rounded-r-full"
                                >
                                    <div className="absolute -top-9 left-1/2 -translate-x-1/2 bg-slate-900 border border-slate-700 px-2 py-1 rounded text-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10 shadow-xl font-bold">
                                        {seg.label}: <Money amount={seg.amount} showDecimals={false} /> ({Math.round(pct)}%)
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                    <div className="flex gap-4 justify-end">
                        {barData.map((seg, idx) => (
                            <div key={idx} className="flex items-center gap-1.5 text-xs text-slate-400">
                                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: seg.color }} />
                                <span>{seg.label}:</span>
                                <span className="font-semibold text-slate-200"><Money amount={seg.amount} showDecimals={false} /></span>
                            </div>
                        ))}
                    </div>
                </div>


                {/* Stats Grid - Adjust columns based on visible cards */}
                <div className={cn(
                    "grid gap-2",
                    type === 'result' ? "grid-cols-4" : "grid-cols-3"
                )}>

                    {/* 1 - Media mensual ingresos - Only for income or result */}
                    {(type === 'income' || type === 'result') && (
                        <div className="flex flex-col items-center gap-1.5 p-2.5 rounded-xl bg-slate-800/60 border border-slate-700/50">
                            <div className="w-7 h-7 rounded-full bg-emerald-500/20 flex items-center justify-center">
                                <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                            </div>
                            <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider text-center leading-tight">Media<br />ingresos</span>
                            <span className="text-xs font-bold text-center text-emerald-300">
                                <Money amount={avgIncome} showPlus={true} showDecimals={false} />
                            </span>
                        </div>
                    )}

                    {/* 2 - Media mensual gastos - Only for expense or result */}
                    {(type === 'expense' || type === 'result') && (
                        <div className="flex flex-col items-center gap-1.5 p-2.5 rounded-xl bg-slate-800/60 border border-slate-700/50">
                            <div className="w-7 h-7 rounded-full bg-rose-500/20 flex items-center justify-center">
                                <TrendingDown className="w-3.5 h-3.5 text-rose-400" />
                            </div>
                            <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider text-center leading-tight">Media<br />gastos</span>
                            <span className="text-xs font-bold text-center text-rose-300">
                                <Money amount={avgExpense} forceSign="-" showDecimals={false} />
                            </span>
                        </div>
                    )}



                    {/* 5 - Total acumulado */}
                    <div className="flex flex-col items-center gap-1.5 p-2.5 rounded-xl bg-slate-800/60 border border-slate-700/50">
                        <div className={cn('w-7 h-7 rounded-full flex items-center justify-center', (type === 'expense' || total < 0) ? 'bg-rose-500/20' : 'bg-emerald-500/20')}>
                            {(type === 'expense' || total < 0)
                                ? <TrendingDown className="w-3.5 h-3.5 text-rose-400" />
                                : <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />}
                        </div>
                        <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider text-center leading-tight">Total<br />{historyLimit === '∞' ? 'hist.' : `${historyLimit}m`}</span>
                        <span className={cn('text-xs font-bold text-center', (type === 'expense' || total < 0) ? 'text-rose-300' : 'text-emerald-300')}>
                            <Money amount={total} showPlus={type !== 'expense'} forceSign={type === 'expense' ? '-' : null} showDecimals={false} />
                        </span>
                    </div>

                    {/* 6 - Racha positiva/negativa */}
                    <div className="flex flex-col items-center gap-1.5 p-2.5 rounded-xl bg-slate-800/60 border border-slate-700/50">
                        <div className={cn(
                            "w-7 h-7 rounded-full flex items-center justify-center",
                            type === 'expense' ? "bg-rose-500/20" : "bg-emerald-500/20"
                        )}>
                            <div className="relative">
                                <Zap className={cn("w-3.5 h-3.5", type === 'expense' ? "text-rose-400" : "text-emerald-400")} />
                                {streakPositive && (
                                    <span className={cn(
                                        "absolute -top-1 -right-1 w-2 h-2 rounded-full animate-pulse",
                                        type === 'expense' ? "bg-rose-500" : "bg-emerald-500"
                                    )} />
                                )}
                            </div>
                        </div>
                        <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider text-center leading-tight">
                            {type === 'expense' ? 'Racha\nnegativa' : 'Racha\npositiva'}
                        </span>
                        <span className={cn("text-xs font-bold", type === 'expense' ? "text-rose-300" : "text-emerald-300")}>
                            {positiveMonths} {positiveMonths === 1 ? 'mes' : 'meses'}
                        </span>
                    </div>


                </div>
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
                        <Money amount={stats?.income || 0} showDecimals={false} showPlus={true} />
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
                        <Money amount={stats?.expense || 0} showDecimals={false} forceSign="-" />
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
                        "text-2xl font-bold flex items-center gap-1",
                        (stats?.result || 0) >= 0 ? "text-emerald-500" : "text-rose-500"
                    )}>
                        {(stats?.result || 0) > 0 ? '+' : ''}
                        <Money amount={stats?.result || 0} showDecimals={false} />
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

                            {/* SMART INTERVALS */}
                            {(availableMonths >= 6) && (
                                <div className="flex gap-1 ml-2 border-l border-slate-800 pl-2">
                                    <button
                                        onClick={() => {
                                            setViewMode('history')
                                            setHistoryLimit(6)
                                        }}
                                        className={cn(
                                            "px-2 py-1.5 rounded-md text-[10px] font-bold transition-all",
                                            viewMode === 'history' && historyLimit === 6
                                                ? "bg-slate-700 text-white shadow"
                                                : "text-slate-500 hover:text-slate-300 hover:bg-slate-800/50"
                                        )}
                                    >
                                        6M
                                    </button>

                                    {availableMonths >= 12 && (
                                        <button
                                            onClick={() => {
                                                setViewMode('history')
                                                setHistoryLimit(12)
                                            }}
                                            className={cn(
                                                "px-2 py-1.5 rounded-md text-[10px] font-bold transition-all",
                                                viewMode === 'history' && historyLimit === 12
                                                    ? "bg-slate-700 text-white shadow"
                                                    : "text-slate-500 hover:text-slate-300 hover:bg-slate-800/50"
                                            )}
                                        >
                                            12M
                                        </button>
                                    )}

                                    {availableMonths >= 24 && (
                                        <button
                                            onClick={() => {
                                                setViewMode('history')
                                                setHistoryLimit(24)
                                            }}
                                            className={cn(
                                                "px-2 py-1.5 rounded-md text-[10px] font-bold transition-all",
                                                viewMode === 'history' && historyLimit === 24
                                                    ? "bg-slate-700 text-white shadow"
                                                    : "text-slate-500 hover:text-slate-300 hover:bg-slate-800/50"
                                            )}
                                        >
                                            24M
                                        </button>
                                    )}

                                    <button
                                        onClick={() => {
                                            setViewMode('history')
                                            setHistoryLimit('∞')
                                        }}
                                        className={cn(
                                            "px-2 py-1.5 rounded-md text-[10px] font-bold transition-all flex items-center justify-center",
                                            viewMode === 'history' && historyLimit === '∞'
                                                ? "bg-slate-700 text-white shadow"
                                                : "text-slate-500 hover:text-slate-300 hover:bg-slate-800/50"
                                        )}
                                        title="Todo el historial"
                                    >
                                        <InfinityIcon className="w-3.5 h-3.5" />
                                    </button>
                                </div>
                            )}
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

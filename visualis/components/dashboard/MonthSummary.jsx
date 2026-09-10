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
        if (!showHistoryOptions && viewMode === 'history') return { months: [], topCategories: [] }

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

        // Calculate Top Categories for the entire period
        const startPeriod = startOfMonth(subMonths(currentDate, limit - 1))
        const endPeriod = endOfMonth(currentDate)
        const periodTxsRaw = await db.transactions.where('date').between(startPeriod, endPeriod, true, true).toArray()
        const periodTxs = selectedWalletId
            ? periodTxsRaw.filter(t => t.walletId === selectedWalletId)
            : periodTxsRaw

        const categories = await db.categories.toArray()
        const catMap = new Map(categories.map(c => [String(c.id), c]))
        
        const catCounts = {}
        const targetType = (expandedType === 'result' || !expandedType) ? 'expense' : expandedType
        const filteredPeriodTxs = periodTxs.filter(t => t.type === targetType)
        
        filteredPeriodTxs.forEach(tx => {
            const cat = catMap.get(String(tx.categoryId)) || { name: 'Sin Categoría', color: '#cbd5e1', parentId: null }
            const parent = cat.parentId
                ? (categories.find(c => String(c.id) === String(cat.parentId)) || cat)
                : cat
            
            if (!catCounts[parent.name]) {
                catCounts[parent.name] = {
                    name: parent.name,
                    amount: 0,
                    color: parent.color || '#cbd5e1'
                }
            }
            catCounts[parent.name].amount += tx.amount
        })
        
        const totalAmount = Object.values(catCounts).reduce((s, c) => s + c.amount, 0) || 1
        const topCategories = Object.values(catCounts)
            .map(c => ({
                ...c,
                percentage: Math.round((c.amount / totalAmount) * 100)
            }))
            .sort((a, b) => b.amount - a.amount)
            .slice(0, 4)

        return {
            months: data,
            topCategories
        }
    }, [currentDate, locale, historyLimit, viewMode, showHistoryOptions, selectedWalletId, availableMonths, expandedType])

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
        if (!history || !history.months || history.months.length === 0) return null

        const monthsData = history.months
        const topCategories = history.topCategories || []
        const getValue = (h) => type === 'result' ? h.result : (type === 'income' ? h.income : h.expense)
        const values = monthsData.map(getValue)

        // Computed stats
        const total = type === 'expense' ? -Math.abs(values.reduce((a, b) => a + b, 0)) : values.reduce((a, b) => a + b, 0)
        const avgIncome = monthsData.reduce((s, h) => s + h.income, 0) / monthsData.length
        const avgExpense = monthsData.reduce((s, h) => s + h.expense, 0) / monthsData.length
        const avgResult = monthsData.reduce((s, h) => s + h.result, 0) / monthsData.length

        // Peak month: for expenses, the month with the MOST spending (max); for income/result, the highest value (max)
        // Only consider months with actual data (value > 0 for expense/income)
        const nonZeroValues = type === 'expense'
            ? values.map((v, i) => ({ v, i })).filter(x => x.v > 0)
            : values.map((v, i) => ({ v, i }))
        const bestMonthIdx = nonZeroValues.length > 0
            ? nonZeroValues.reduce((best, cur) => cur.v > best.v ? cur : best, nonZeroValues[0]).i
            : values.indexOf(Math.max(...values))
        const bestMonth = monthsData[bestMonthIdx]

        // Positive months count
        const positiveMonths = type === 'expense'
            ? monthsData.filter(h => h.expense > h.income).length
            : monthsData.filter(h => h.result > 0).length

        // Total income/expense for saving rates
        const totalIncome = monthsData.reduce((s, h) => s + h.income, 0)
        const totalExpense = monthsData.reduce((s, h) => s + h.expense, 0)
        const savingsRate = totalIncome > 0 ? Math.round(((totalIncome - totalExpense) / totalIncome) * 100) : 0

        // Trend logic
        const mid = Math.floor(monthsData.length / 2)
        const firstHalf = monthsData.slice(0, mid)
        const secondHalf = monthsData.slice(mid)
        const getHalfAvg = (half) => half.reduce((s, h) => s + getValue(h), 0) / (half.length || 1)
        const avgFirst = getHalfAvg(firstHalf)
        const avgSecond = getHalfAvg(secondHalf)
        
        let trendMsg = ''
        let trendColor = 'text-slate-400'
        
        if (monthsData.length >= 4) {
            // For trend, always compare the last 6 months vs the 6 before that (if available),
            // so the metric stays relevant regardless of how long the total history is.
            const trendWindowSize = Math.min(6, Math.floor(monthsData.length / 2))
            const trendSecond = monthsData.slice(-trendWindowSize)
            const trendFirst = monthsData.slice(-(trendWindowSize * 2), -trendWindowSize)
            const avgTrendFirst = trendFirst.length > 0
                ? trendFirst.reduce((s, h) => s + getValue(h), 0) / trendFirst.length
                : 0
            const avgTrendSecond = trendSecond.reduce((s, h) => s + getValue(h), 0) / trendSecond.length
            
            const rawTrendPct = avgTrendFirst > 0
                ? Math.round(((avgTrendSecond - avgTrendFirst) / avgTrendFirst) * 100)
                : 0
            // Cap at ±999% to avoid absurd numbers
            const trendPct = Math.max(-999, Math.min(999, rawTrendPct))

            if (trendPct > 5) {
                trendMsg = `+${trendPct}% vs ant.`
                trendColor = type === 'expense' ? 'text-rose-400' : 'text-emerald-400'
            } else if (trendPct < -5) {
                trendMsg = `${trendPct}% vs ant.`
                trendColor = type === 'expense' ? 'text-emerald-400' : 'text-rose-400'
            } else {
                trendMsg = 'Estable'
            }
        }


        const renderHistoryChart = () => {
            const isNet = type === 'result'
            
            if (isNet) {
                // SVG bidirectional chart — positive bars above baseline, negative below
                const W = 600
                const H = 130
                const padX = 8
                const padTop = 8
                const padBottom = 26
                const midY = padTop + (H - padTop - padBottom) / 2  // baseline (zero line)
                const halfH = (H - padTop - padBottom) / 2
                const chartW = W - padX * 2

                const values = monthsData.map(h => h.result)
                const maxAbs = Math.max(...values.map(v => Math.abs(v)), 1)

                const pts = values.map((v, i) => {
                    const x = padX + (i / Math.max(values.length - 1, 1)) * chartW
                    return { x, v, month: monthsData[i].month }
                })

                // Max labels
                const maxLabels = Math.min(6, pts.length)
                const step = pts.length <= maxLabels ? 1 : Math.ceil(pts.length / maxLabels)
                const labelIndices = new Set(
                    pts.map((_, i) => i).filter((i) => i % step === 0 || i === pts.length - 1)
                )

                // Build smooth SVG line path through zero-anchored points
                const linePts = pts.map(pt => ({
                    x: pt.x,
                    y: midY - (pt.v / maxAbs) * halfH * 0.92
                }))
                const tension = 0.3
                const splinePath = linePts.reduce((path, pt, i) => {
                    if (i === 0) return `M ${pt.x},${pt.y}`
                    const prev = linePts[i - 1]
                    const cp1x = prev.x + (pt.x - prev.x) * tension
                    const cp2x = pt.x - (pt.x - prev.x) * tension
                    return `${path} C ${cp1x},${prev.y} ${cp2x},${pt.y} ${pt.x},${pt.y}`
                }, '')

                // Positive area (above midY)
                const posClipId = 'clip-pos-result'
                const negClipId = 'clip-neg-result'

                return (
                    <div className="mt-2 mb-4 bg-slate-950/40 rounded-2xl border border-slate-800/80 px-3 pt-3 pb-1">
                        <svg viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ overflow: 'visible' }}>
                            <defs>
                                {/* Clip positive area (above midY) */}
                                <clipPath id={posClipId}>
                                    <rect x={padX} y={padTop} width={chartW} height={midY - padTop} />
                                </clipPath>
                                {/* Clip negative area (below midY) */}
                                <clipPath id={negClipId}>
                                    <rect x={padX} y={midY} width={chartW} height={halfH} />
                                </clipPath>
                                <linearGradient id="grad-pos" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stopColor="rgba(16,185,129,0.35)" />
                                    <stop offset="100%" stopColor="rgba(16,185,129,0.0)" />
                                </linearGradient>
                                <linearGradient id="grad-neg" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stopColor="rgba(244,63,94,0.0)" />
                                    <stop offset="100%" stopColor="rgba(244,63,94,0.35)" />
                                </linearGradient>
                            </defs>

                            {/* Subtle grid lines */}
                            {[0.5].map(pct => (
                                <line key={pct}
                                    x1={padX} y1={padTop + (H - padTop - padBottom) * (1 - pct)}
                                    x2={W - padX} y2={padTop + (H - padTop - padBottom) * (1 - pct)}
                                    stroke="rgba(148,163,184,0.06)" strokeWidth="1"
                                />
                            ))}

                            {/* Zero baseline */}
                            <line x1={padX} y1={midY} x2={W - padX} y2={midY}
                                stroke="rgba(148,163,184,0.25)" strokeWidth="1" strokeDasharray="3,3" />

                            {/* Positive fill area */}
                            {splinePath && (
                                <path
                                    d={`${splinePath} L ${linePts[linePts.length - 1].x},${midY} L ${linePts[0].x},${midY} Z`}
                                    fill="url(#grad-pos)"
                                    clipPath={`url(#${posClipId})`}
                                />
                            )}

                            {/* Negative fill area */}
                            {splinePath && (
                                <path
                                    d={`${splinePath} L ${linePts[linePts.length - 1].x},${midY} L ${linePts[0].x},${midY} Z`}
                                    fill="url(#grad-neg)"
                                    clipPath={`url(#${negClipId})`}
                                />
                            )}

                            {/* Line — green above zero, red below (drawn twice with clip) */}
                            {splinePath && (<>
                                <path d={splinePath} fill="none" stroke="#10b981" strokeWidth="2"
                                    strokeLinecap="round" strokeLinejoin="round" opacity="0.9"
                                    clipPath={`url(#${posClipId})`} />
                                <path d={splinePath} fill="none" stroke="#f43f5e" strokeWidth="2"
                                    strokeLinecap="round" strokeLinejoin="round" opacity="0.9"
                                    clipPath={`url(#${negClipId})`} />
                            </>)}

                            {/* Dots on each data point colored by sign */}
                            {linePts.map((pt, i) => {
                                const v = values[i]
                                if (Math.abs(v) < maxAbs * 0.02) return null // skip near-zero dots
                                const color = v >= 0 ? '#10b981' : '#f43f5e'
                                return (
                                    <circle key={i} cx={pt.x} cy={pt.y}
                                        r="2.5" fill={color} opacity="0.8" />
                                )
                            })}

                            {/* Month labels */}
                            {pts.map((pt, i) => {
                                if (!labelIndices.has(i)) return null
                                return (
                                    <text key={i} x={pt.x} y={H - 3}
                                        textAnchor="middle" fontSize="9"
                                        fill="rgba(148,163,184,0.50)" fontWeight="bold"
                                        style={{ textTransform: 'uppercase', fontFamily: 'inherit' }}>
                                        {pt.month}
                                    </text>
                                )
                            })}
                        </svg>
                    </div>
                )
            } else {
                // SVG Area Chart — scales to 100% width, works for any number of months
                const W = 600
                const H = 120
                const padX = 8
                const padTop = 12
                const padBottom = 26
                const chartH = H - padTop - padBottom
                const chartW = W - padX * 2

                const rawValues = monthsData.map(getValue)
                const maxVal = Math.max(...rawValues, 1)
                const peakIdx = rawValues.indexOf(Math.max(...rawValues))

                const pts = rawValues.map((v, i) => {
                    const x = padX + (i / Math.max(rawValues.length - 1, 1)) * chartW
                    const y = padTop + chartH - (v / maxVal) * chartH
                    return { x, y, v, month: monthsData[i].month }
                })

                const tension = 0.3
                const splinePath = pts.reduce((path, pt, i) => {
                    if (i === 0) return `M ${pt.x},${pt.y}`
                    const prev = pts[i - 1]
                    const cp1x = prev.x + (pt.x - prev.x) * tension
                    const cp1y = prev.y
                    const cp2x = pt.x - (pt.x - prev.x) * tension
                    const cp2y = pt.y
                    return `${path} C ${cp1x},${cp1y} ${cp2x},${cp2y} ${pt.x},${pt.y}`
                }, '')

                const baselineY = padTop + chartH
                const fillPath = pts.length > 0
                    ? `${splinePath} L ${pts[pts.length - 1].x},${baselineY} L ${pts[0].x},${baselineY} Z`
                    : ''

                const strokeColor = type === 'income' ? '#10b981' : '#f43f5e'
                const fillId = type === 'income' ? 'grad-income' : 'grad-expense'
                const fillColorTop = type === 'income' ? 'rgba(16,185,129,0.30)' : 'rgba(244,63,94,0.30)'
                const fillColorBot = type === 'income' ? 'rgba(16,185,129,0.0)' : 'rgba(244,63,94,0.0)'

                const maxLabels = Math.min(6, pts.length)
                const step = pts.length <= maxLabels ? 1 : Math.ceil(pts.length / maxLabels)
                const labelIndices = new Set(
                    pts.map((_, i) => i).filter((i) => i % step === 0 || i === pts.length - 1)
                )

                return (
                    <div className="mt-2 mb-4 bg-slate-950/40 rounded-2xl border border-slate-800/80 px-3 pt-3 pb-1">
                        <svg viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ overflow: 'visible' }}>
                            <defs>
                                <linearGradient id={fillId} x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stopColor={fillColorTop} />
                                    <stop offset="100%" stopColor={fillColorBot} />
                                </linearGradient>
                            </defs>

                            {[0.25, 0.5, 0.75].map(pct => {
                                const y = padTop + chartH - pct * chartH
                                return <line key={pct} x1={padX} y1={y} x2={W - padX} y2={y} stroke="rgba(148,163,184,0.07)" strokeWidth="1" />
                            })}

                            <line x1={padX} y1={baselineY} x2={W - padX} y2={baselineY} stroke="rgba(148,163,184,0.15)" strokeWidth="1" />

                            {fillPath && <path d={fillPath} fill={`url(#${fillId})`} />}

                            {splinePath && (
                                <path d={splinePath} fill="none" stroke={strokeColor} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" opacity="0.9" />
                            )}

                            {pts[peakIdx] && (
                                <>
                                    <circle cx={pts[peakIdx].x} cy={pts[peakIdx].y} r="7" fill={strokeColor} opacity="0.15" />
                                    <circle cx={pts[peakIdx].x} cy={pts[peakIdx].y} r="3.5" fill={strokeColor} opacity="0.95" />
                                </>
                            )}

                            {pts.map((pt, i) => {
                                if (!labelIndices.has(i)) return null
                                return (
                                    <text key={i} x={pt.x} y={H - 3} textAnchor="middle" fontSize="9"
                                        fill="rgba(148,163,184,0.50)" fontWeight="bold"
                                        style={{ textTransform: 'uppercase', fontFamily: 'inherit' }}>
                                        {pt.month}
                                    </text>
                                )
                            })}
                        </svg>
                    </div>
                )
            }
        }

        return (
            <div className="space-y-4">
                {/* 1. Area Chart */}
                {renderHistoryChart()}

                {/* 2. Key Insights Panel */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                    {/* Media mensual */}
                    <div className="flex flex-col p-2.5 rounded-xl bg-slate-800/40 border border-slate-800">
                        <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider">Media mensual</span>
                        <span className={cn("text-sm font-bold mt-1", 
                            type === 'result' ? (avgResult >= 0 ? "text-emerald-400" : "text-rose-400") : 
                            (type === 'income' ? "text-emerald-400" : "text-rose-400")
                        )}>
                            <Money amount={type === 'result' ? avgResult : (type === 'income' ? avgIncome : avgExpense)} showDecimals={false} forceSign={type === 'expense' ? '-' : null} />
                        </span>
                    </div>

                    {/* Mes pico */}
                    <div className="flex flex-col p-2.5 rounded-xl bg-slate-800/40 border border-slate-800">
                        <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider">Mes Máximo</span>
                        {bestMonth ? (
                            <div className="flex flex-col mt-0.5">
                                <span className="text-xs font-bold text-slate-200 truncate">
                                    <Money amount={getValue(bestMonth)} showDecimals={false} forceSign={type === 'expense' ? '-' : null} />
                                </span>
                                <span className="text-[8px] text-slate-500 font-bold uppercase">{bestMonth.month}</span>
                            </div>
                        ) : (
                            <span className="text-xs font-bold text-slate-400 mt-1">-</span>
                        )}
                    </div>

                    {/* Tasa de ahorro / total */}
                    <div className="flex flex-col p-2.5 rounded-xl bg-slate-800/40 border border-slate-800">
                        {type === 'expense' ? (
                            <>
                                <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider">Total periodo</span>
                                <span className="text-sm font-bold text-rose-400 mt-1">
                                    <Money amount={total} showDecimals={false} forceSign="-" />
                                </span>
                            </>
                        ) : (
                            <>
                                <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider">Tasa Ahorro</span>
                                <span className={cn("text-sm font-bold mt-1", savingsRate >= 15 ? "text-emerald-400" : (savingsRate >= 0 ? "text-sky-400" : "text-orange-400"))}>
                                    {savingsRate}%
                                </span>
                            </>
                        )}
                    </div>

                    {/* Tendencia */}
                    <div className="flex flex-col p-2.5 rounded-xl bg-slate-800/40 border border-slate-800">
                        <span className="text-[9px] text-slate-500 uppercase font-bold tracking-wider">Tendencia</span>
                        {trendMsg ? (
                            <span className={cn("text-[11px] font-bold mt-2.5 leading-none", trendColor)}>
                                {trendMsg}
                            </span>
                        ) : (
                            <span className="text-[11px] font-bold text-slate-500 mt-2.5 leading-none">
                                {positiveMonths} {positiveMonths === 1 ? 'mes act.' : 'meses act.'}
                            </span>
                        )}
                    </div>
                </div>

                {/* 3. Top Categories of Period */}
                {topCategories.length > 0 && (
                    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-3">
                        <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
                            <PieChart className="w-3.5 h-3.5 text-slate-500" />
                            {type === 'income' ? 'Principales Fuentes' : 'Mayores Gastos'} (Acumulado)
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {topCategories.map((c, i) => (
                                <div key={i} className="flex items-center justify-between p-2 rounded-xl bg-slate-950/40 border border-slate-800/40">
                                    <div className="flex items-center gap-2 min-w-0">
                                        <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: c.color }} />
                                        <span className="text-xs text-slate-300 truncate">{tCategory(c.name)}</span>
                                    </div>
                                    <span className="text-xs font-semibold text-slate-400 ml-2 shrink-0">
                                        <Money amount={c.amount} showDecimals={false} /> <span className="text-[9px] text-slate-600">({c.percentage}%)</span>
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
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

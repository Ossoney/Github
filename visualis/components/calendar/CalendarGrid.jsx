import { useState, useMemo } from 'react'
import { startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, isSameMonth, isSameDay, addMonths, subMonths, format, isBefore, startOfDay } from 'date-fns'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { useLanguage } from '@/lib/i18n'
import { Money } from '@/components/ui/Money'
import { DayDetailsModal } from './DayDetailsModal'
import { cn } from '@/lib/utils'

export function CalendarGrid() {
    const { locale, t } = useLanguage()
    const [currentDate, setCurrentDate] = useState(new Date())
    const [selectedDate, setSelectedDate] = useState(null)
    const [isModalOpen, setIsModalOpen] = useState(false)

    const monthStart = startOfMonth(currentDate)
    const monthEnd = endOfMonth(monthStart)
    const startDate = startOfWeek(monthStart, { locale })
    const endDate = endOfWeek(monthEnd, { locale })

    const data = useLiveQuery(async () => {
        const txs = await db.transactions
            .where('date')
            .between(startDate, endDate, true, true)
            .toArray()

        const categories = await db.categories.toArray()
        const catMap = new Map(categories.map(c => [c.id, c]))

        const enhancedTxs = txs.map(tx => ({
            ...tx,
            category: catMap.get(tx.categoryId)
        }))

        const recurring = await db.recurring.where('active').equals('true').toArray()
        const enhancedRecurring = recurring.map(r => ({
            ...r,
            category: catMap.get(r.categoryId)
        }))

        return { transactions: enhancedTxs, recurring: enhancedRecurring }
    }, [startDate, endDate])

    const prevMonth = () => setCurrentDate(subMonths(currentDate, 1))
    const nextMonth = () => setCurrentDate(addMonths(currentDate, 1))

    const calendarDays = useMemo(() => {
        if (!data) return []

        const days = eachDayOfInterval({ start: startDate, end: endDate })

        return days.map(day => {
            const dayTxs = data.transactions.filter(tx => isSameDay(new Date(tx.date), day))
            const income = dayTxs.filter(t => t.type === 'income').reduce((acc, t) => acc + t.amount, 0)
            const expense = dayTxs.filter(t => t.type === 'expense').reduce((acc, t) => acc + t.amount, 0)
            const balance = income - expense

            const isFutureOrToday = !isBefore(day, startOfDay(new Date()))
            let projectedTxs = []
            if (isFutureOrToday) {
                const dayOfMonth = day.getDate()
                projectedTxs = data.recurring.filter(r => r.dayOfMonth === dayOfMonth)
            }

            return {
                date: day,
                isCurrentMonth: isSameMonth(day, monthStart),
                isToday: isSameDay(day, new Date()),
                actualTransactions: dayTxs,
                projectedTransactions: projectedTxs,
                income,
                expense,
                balance,
                hasActivity: dayTxs.length > 0 || projectedTxs.length > 0
            }
        })
    }, [data, startDate, endDate, monthStart])

    // Monthly totals (current month only)
    const monthlyTotals = useMemo(() => {
        const monthDays = calendarDays.filter(d => d.isCurrentMonth)
        const totalIncome = monthDays.reduce((acc, d) => acc + d.income, 0)
        const totalExpense = monthDays.reduce((acc, d) => acc + d.expense, 0)
        return { totalIncome, totalExpense, net: totalIncome - totalExpense }
    }, [calendarDays])

    const handleDayClick = (dayData) => {
        setSelectedDate(dayData)
        setIsModalOpen(true)
    }

    const weekDays = eachDayOfInterval({ start: startDate, end: endOfWeek(startDate, { locale }) })

    return (
        <div className="space-y-3">
            {/* Header / Navigation */}
            <div className="flex items-center justify-between bg-slate-900/50 px-4 py-3 rounded-2xl border border-slate-800">
                <button onClick={prevMonth} className="p-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors">
                    <ChevronLeft className="w-5 h-5" />
                </button>

                <div className="flex flex-col items-center gap-0.5">
                    <h2 className="text-lg font-bold capitalize text-slate-100 leading-tight">
                        {format(currentDate, 'MMMM', { locale })}
                    </h2>
                    <span className="text-xs text-slate-500 font-medium">
                        {format(currentDate, 'yyyy')}
                    </span>
                </div>

                <button onClick={nextMonth} className="p-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors">
                    <ChevronRight className="w-5 h-5" />
                </button>
            </div>

            {/* Monthly Summary Pills */}
            <div className="grid grid-cols-3 gap-2">
                <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-2.5 text-center">
                    <div className="text-[10px] text-emerald-500/70 font-semibold uppercase tracking-wider mb-0.5">{t('income') || 'Ingresos'}</div>
                    <div className="text-sm font-bold text-emerald-400">
                        <Money amount={monthlyTotals.totalIncome} showDecimals={false} />
                    </div>
                </div>
                <div className={cn(
                    "border rounded-xl p-2.5 text-center",
                    monthlyTotals.net >= 0
                        ? "bg-sky-500/10 border-sky-500/20"
                        : "bg-rose-500/10 border-rose-500/20"
                )}>
                    <div className={cn("text-[10px] font-semibold uppercase tracking-wider mb-0.5",
                        monthlyTotals.net >= 0 ? "text-sky-400/70" : "text-rose-400/70"
                    )}>Balance</div>
                    <div className={cn("text-sm font-bold", monthlyTotals.net >= 0 ? "text-sky-400" : "text-rose-400")}>
                        <Money amount={monthlyTotals.net} showDecimals={false} showPlus />
                    </div>
                </div>
                <div className="bg-rose-500/10 border border-rose-500/20 rounded-xl p-2.5 text-center">
                    <div className="text-[10px] text-rose-500/70 font-semibold uppercase tracking-wider mb-0.5">{t('expense') || 'Gastos'}</div>
                    <div className="text-sm font-bold text-rose-400">
                        <Money amount={monthlyTotals.totalExpense} showDecimals={false} />
                    </div>
                </div>
            </div>

            {/* Grid */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl overflow-hidden">
                {/* Day Headers — single letter */}
                <div className="grid grid-cols-7 border-b border-slate-800">
                    {weekDays.map(day => (
                        <div key={day.toString()} className="py-2 text-center text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                            {format(day, 'EEEEE', { locale })}
                        </div>
                    ))}
                </div>

                {/* Days Grid */}
                <div className="grid grid-cols-7 gap-px bg-slate-800/40">
                    {calendarDays.map((day, idx) => {
                        const hasIncome = day.income > 0
                        const hasExpense = day.expense > 0
                        const hasProjected = day.projectedTransactions.length > 0

                        return (
                            <button
                                key={idx}
                                onClick={() => handleDayClick(day)}
                                className={cn(
                                    'min-h-[72px] p-1.5 flex flex-col items-center gap-1 transition-all group relative',
                                    day.isCurrentMonth ? 'bg-slate-900' : 'bg-slate-950/60',
                                    day.isToday
                                        ? 'bg-sky-950/40 ring-1 ring-inset ring-sky-500/40'
                                        : 'hover:bg-slate-800/70',
                                )}
                            >
                                {/* Day Number */}
                                <span className={cn(
                                    'text-sm font-semibold w-7 h-7 flex items-center justify-center rounded-full transition-all',
                                    day.isToday
                                        ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/30'
                                        : day.isCurrentMonth
                                            ? 'text-slate-200 group-hover:text-white'
                                            : 'text-slate-600'
                                )}>
                                    {format(day.date, 'd')}
                                </span>

                                {/* Dot indicators for activity type */}
                                {(hasIncome || hasExpense || hasProjected) && (
                                    <div className="flex gap-0.5 items-center justify-center">
                                        {hasIncome && (
                                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50" />
                                        )}
                                        {hasExpense && (
                                            <span className="w-1.5 h-1.5 rounded-full bg-rose-400 shadow-sm shadow-rose-400/50" />
                                        )}
                                        {hasProjected && (
                                            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 shadow-sm shadow-indigo-400/50" />
                                        )}
                                    </div>
                                )}

                                {/* Balance — without decimals, only for current month with real activity */}
                                {day.isCurrentMonth && day.balance !== 0 && day.actualTransactions.length > 0 && (
                                    <div className={cn(
                                        'text-[10px] font-bold leading-none',
                                        day.balance > 0 ? 'text-emerald-400' : 'text-rose-400'
                                    )}>
                                        {day.balance > 0 ? '+' : ''}
                                        <Money amount={day.balance} showDecimals={false} />
                                    </div>
                                )}
                            </button>
                        )
                    })}
                </div>
            </div>

            {/* Legend */}
            <div className="flex items-center justify-center gap-4 text-[11px] text-slate-500">
                <span className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-400" />
                    {t('income') || 'Ingresos'}
                </span>
                <span className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-rose-400" />
                    {t('expense') || 'Gastos'}
                </span>
                <span className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-indigo-400" />
                    {t('projected') || 'Recurrente'}
                </span>
            </div>

            <DayDetailsModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                date={selectedDate?.date}
                actualTransactions={selectedDate?.actualTransactions}
                projectedTransactions={selectedDate?.projectedTransactions}
            />
        </div>
    )
}

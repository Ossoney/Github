import { useState, useMemo } from 'react'
import { startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, isSameMonth, isSameDay, addMonths, subMonths, format, isAfter, isBefore, startOfDay } from 'date-fns'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { useLanguage } from '@/lib/i18n'
import { Money } from '@/components/ui/Money'
import { DayDetailsModal } from './DayDetailsModal'

export function CalendarGrid() {
    const { locale, t } = useLanguage()
    const [currentDate, setCurrentDate] = useState(new Date())
    const [selectedDate, setSelectedDate] = useState(null)
    const [isModalOpen, setIsModalOpen] = useState(false)

    // Range for the calendar grid
    const monthStart = startOfMonth(currentDate)
    const monthEnd = endOfMonth(monthStart)
    const startDate = startOfWeek(monthStart, { locale })
    const endDate = endOfWeek(monthEnd, { locale })

    // Fetch Data
    const data = useLiveQuery(async () => {
        // 1. Actual Transactions
        const txs = await db.transactions
            .where('date')
            .between(startDate, endDate, true, true)
            .toArray()

        // Enhance with category info
        const categories = await db.categories.toArray()
        const catMap = new Map(categories.map(c => [c.id, c])) // Use Map for O(1) lookup

        const enhancedTxs = txs.map(tx => ({
            ...tx,
            category: catMap.get(tx.categoryId)
        }))

        // 2. Recruiting Transactions
        const recurring = await db.recurring.where('active').equals('true').toArray()
        // Enhance recurring with category
        const enhancedRecurring = recurring.map(r => ({
            ...r,
            category: catMap.get(r.categoryId)
        }))

        return {
            transactions: enhancedTxs,
            recurring: enhancedRecurring
        }
    }, [startDate, endDate]) // Dependencies for query

    // Navigation Handlers
    const prevMonth = () => setCurrentDate(subMonths(currentDate, 1))
    const nextMonth = () => setCurrentDate(addMonths(currentDate, 1))
    const goToToday = () => setCurrentDate(new Date())

    // Process Days
    const calendarDays = useMemo(() => {
        if (!data) return []

        const days = eachDayOfInterval({ start: startDate, end: endDate })

        return days.map(day => {
            const dayStart = startOfDay(day)

            // Actual Transactions for this day
            const dayTxs = data.transactions.filter(tx => isSameDay(new Date(tx.date), day))

            // Calculate Daily Balance
            const income = dayTxs.filter(t => t.type === 'income').reduce((acc, t) => acc + t.amount, 0)
            const expense = dayTxs.filter(t => t.type === 'expense').reduce((acc, t) => acc + t.amount, 0)
            const balance = income - expense

            // Projected Recurring
            // Logic: If day >= today AND matches recurrence day
            const isFutureOrToday = !isBefore(day, startOfDay(new Date()))

            let projectedTxs = []
            if (isFutureOrToday) {
                const dayOfMonth = day.getDate()
                // Simple projection: Day matches. 
                // Advanced: Handle months with fewer days (28/30/31) - simplifying for V1 to exact match or last day

                projectedTxs = data.recurring.filter(r => {
                    // Check if already run? 
                    // If we have an actual transaction for this recurring item on this day/month, don't project.
                    // But matching "recurring item" to "transaction" is hard without a link ID.
                    // For now, just show projection if it's in the future.
                    if (isSameDay(day, new Date())) {
                        // If today, maybe check if a similar transaction exists?
                        // Let's keep it simple: Show as projected. User can mark as done by adding it.
                        return r.dayOfMonth === dayOfMonth
                    }
                    return r.dayOfMonth === dayOfMonth
                })

                // Handle end of month overflow (e.g. recurrence on 31st, but month has 30)
                // If r.dayOfMonth > daysInMonth, show on last day? 
                // Standard banking usually moves to last day or first or next month. 
                // Let's skip for V1 or assume simple matching.
            }

            return {
                date: day,
                isCurrentMonth: isSameMonth(day, monthStart),
                isToday: isSameDay(day, new Date()),
                actualTransactions: dayTxs,
                projectedTransactions: projectedTxs,
                balance,
                hasActivity: dayTxs.length > 0 || projectedTxs.length > 0
            }
        })
    }, [data, startDate, endDate, monthStart])

    const handleDayClick = (dayData) => {
        setSelectedDate(dayData)
        setIsModalOpen(true)
    }

    // Weekday Headers
    const weekDays = eachDayOfInterval({ start: startDate, end: endOfWeek(startDate, { locale }) })

    return (
        <div className="space-y-4">
            {/* Header / Navigation */}
            <div className="flex items-center justify-between bg-slate-900/50 p-4 rounded-2xl border border-slate-800">
                <button onClick={prevMonth} className="p-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors">
                    <ChevronLeft className="w-6 h-6" />
                </button>

                <div className="flex flex-col items-center">
                    <h2 className="text-xl font-bold capitalize text-slate-100">
                        {format(currentDate, 'MMMM yyyy', { locale })}
                    </h2>
                </div>

                <button onClick={nextMonth} className="p-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors">
                    <ChevronRight className="w-6 h-6" />
                </button>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-7 gap-px bg-slate-800/50 rounded-2xl overflow-hidden border border-slate-800">
                {/* Headers */}
                {weekDays.map(day => (
                    <div key={day.toString()} className="bg-slate-900/80 p-3 text-center text-sm font-semibold text-slate-500 capitalize">
                        {format(day, 'EEE', { locale })}
                    </div>
                ))}

                {/* Days */}
                {calendarDays.map((day, idx) => {
                    // Logic for balance coloring
                    const isPositive = day.balance > 0
                    const isNegative = day.balance < 0
                    const balanceColor = isPositive ? 'text-emerald-400' : isNegative ? 'text-rose-400' : 'text-slate-500'

                    return (
                        <div
                            key={idx}
                            onClick={() => handleDayClick(day)}
                            className={`
                                min-h-[100px] p-2 flex flex-col justify-between transition-colors cursor-pointer group
                                ${day.isCurrentMonth ? 'bg-slate-900' : 'bg-slate-950/50'}
                                ${day.isToday ? 'bg-slate-800/80 ring-1 ring-inset ring-sky-500/50' : 'hover:bg-slate-800'}
                            `}
                        >
                            <div className="flex justify-between items-start">
                                <span className={`
                                    text-sm font-medium w-7 h-7 flex items-center justify-center rounded-full
                                    ${day.isToday ? 'bg-sky-500 text-white' : day.isCurrentMonth ? 'text-slate-300' : 'text-slate-600'}
                                `}>
                                    {format(day.date, 'd')}
                                </span>
                                {day.projectedTransactions.length > 0 && (
                                    <span className="text-[10px] bg-indigo-500/20 text-indigo-400 px-1.5 py-0.5 rounded-full border border-indigo-500/20">
                                        ★
                                    </span>
                                )}
                            </div>

                            {day.hasActivity && (
                                <div className="space-y-1 mt-1">
                                    {day.balance !== 0 && (
                                        <div className={`text-xs text-right font-medium ${balanceColor}`}>
                                            {day.balance > 0 ? '+' : ''}<Money amount={day.balance} />
                                        </div>
                                    )}

                                    {/* Mini indicators for transaction density/type if needed */}
                                    {/* For V1, balance is strong enough */}
                                </div>
                            )}
                        </div>
                    )
                })}
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

'use client'

import { useMemo, useState } from 'react'
import { Modal, Card, Button } from '@/components/ui/UI'
import { 
    Trophy, Flame, Calendar as CalendarIcon, 
    TrendingUp, Activity, Clock, 
    CheckCircle2, XCircle, Star,
    ChevronLeft, ChevronRight
} from 'lucide-react'
import { 
    format, subMonths, addMonths, startOfMonth, endOfMonth, 
    eachDayOfInterval, isSameDay, differenceInDays, 
    subDays, startOfDay, subWeeks, addDays, startOfWeek, getMonth, getYear
} from 'date-fns'
import { useLanguage } from '@/lib/i18n'
import { cn } from '@/lib/utils'

export function HabitStatsModal({ isOpen, onClose, habit, logs = [] }) {
    const { t, locale } = useLanguage()
    const [calendarMonth, setCalendarMonth] = useState(new Date())

    // Calculate Statistics
    const stats = useMemo(() => {
        if (!habit || !logs) return null

        const habitLogs = logs.filter(l => l.habitId === habit.id).map(l => startOfDay(new Date(l.date)).getTime())
        const total = habitLogs.length
        
        // Compliance % (Last 30 days)
        const last30Days = [...Array(30)].map((_, i) => subDays(startOfDay(new Date()), i).getTime())
        const completedLast30 = last30Days.filter(d => habitLogs.includes(d)).length
        const score = Math.round((completedLast30 / 30) * 100)

        // ──────────────────────────────────────────────
        // STREAKS — context-aware (daily vs weekly goal)
        // ──────────────────────────────────────────────
        const isWeeklyHabit = habit.goal < 7  // goal is days-per-week

        let currentStreak = 0
        let bestStreak = 0

        if (!isWeeklyHabit) {
            // Daily habit: count consecutive days
            let checkDay = startOfDay(new Date())
            while (habitLogs.includes(checkDay.getTime())) {
                currentStreak++
                checkDay = subDays(checkDay, 1)
            }
            if (currentStreak === 0) {
                checkDay = subDays(startOfDay(new Date()), 1)
                while (habitLogs.includes(checkDay.getTime())) {
                    currentStreak++
                    checkDay = subDays(checkDay, 1)
                }
            }

            const allDaysSorted = [...new Set(habitLogs)].sort((a, b) => a - b)
            if (allDaysSorted.length > 0) {
                let tempStreak = 1
                for (let i = 1; i < allDaysSorted.length; i++) {
                    const diff = differenceInDays(allDaysSorted[i], allDaysSorted[i - 1])
                    if (diff === 1) {
                        tempStreak++
                    } else {
                        bestStreak = Math.max(bestStreak, tempStreak)
                        tempStreak = 1
                    }
                }
                bestStreak = Math.max(bestStreak, tempStreak)
            }
        } else {
            // Weekly habit: count consecutive weeks where goal was met
            const weeksToCheck = 52 // look back up to 1 year
            const weekResults = []
            for (let w = 0; w < weeksToCheck; w++) {
                const weekStart = startOfWeek(subWeeks(startOfDay(new Date()), w), { weekStartsOn: 1 })
                const weekEnd = addDays(weekStart, 6)
                const count = eachDayOfInterval({ start: weekStart, end: weekEnd })
                    .filter(d => habitLogs.includes(startOfDay(d).getTime())).length
                weekResults.push(count >= habit.goal)
            }
            // Current streak (from this week backwards)
            for (let i = 0; i < weekResults.length; i++) {
                if (weekResults[i]) currentStreak++
                else break
            }
            // Best streak
            let temp = 0
            for (let i = 0; i < weekResults.length; i++) {
                if (weekResults[i]) { temp++; bestStreak = Math.max(bestStreak, temp) }
                else temp = 0
            }
        }

        // ──────────────────────────────────────────────
        // Last 8 weeks evolution (completions per week)
        // ──────────────────────────────────────────────
        const weeklyEvolution = []
        for (let w = 7; w >= 0; w--) {
            const weekStart = startOfWeek(subWeeks(startOfDay(new Date()), w), { weekStartsOn: 1 })
            const weekEnd = addDays(weekStart, 6)
            const count = eachDayOfInterval({ start: weekStart, end: weekEnd })
                .filter(d => habitLogs.includes(startOfDay(d).getTime())).length
            weeklyEvolution.push({
                label: format(weekStart, 'd/M'),
                count,
                isCurrentWeek: w === 0
            })
        }

        return {
            total,
            score,
            currentStreak,
            bestStreak,
            weeklyEvolution,
            habitLogs,
            isWeeklyHabit,
        }
    }, [habit, logs])

    if (!habit || !stats) return null

    const streakUnit = stats.isWeeklyHabit ? 'sem.' : 'd'
    const maxWeekly = Math.max(...stats.weeklyEvolution.map(w => w.count), habit.goal, 1)

    return (
        <Modal 
            isOpen={isOpen} 
            onClose={onClose} 
            title={habit.name}
            className="max-w-2xl"
        >
            <div className="space-y-6 pb-4">
                
                {/* 1. Overview Header Stats */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <Card className="p-3 bg-slate-900 border-slate-800 flex flex-col items-center justify-center gap-1">
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{t('score')}</span>
                        <div className="flex items-center gap-2">
                            <div className="relative w-8 h-8 rounded-full border-2 border-slate-800 flex items-center justify-center">
                                <svg className="absolute inset-0 w-full h-full -rotate-90">
                                    <circle cx="16" cy="16" r="14" fill="transparent" stroke={habit.color} strokeWidth="2" strokeDasharray={88} strokeDashoffset={88 - (88 * stats.score) / 100} />
                                </svg>
                                <TrendingUp className="w-3.5 h-3.5 text-sky-400" />
                            </div>
                            <span className="text-xl font-bold text-slate-100">{stats.score}%</span>
                        </div>
                    </Card>

                    <Card className="p-3 bg-slate-900 border-slate-800 flex flex-col items-center justify-center gap-1">
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{t('total')}</span>
                        <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                            <span className="text-xl font-bold text-slate-100">{stats.total}</span>
                        </div>
                    </Card>

                    {/* Best Streak — with unit label */}
                    <Card className="p-3 bg-slate-900 border-slate-800 flex flex-col items-center justify-center gap-1">
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{t('best')}</span>
                        <div className="flex items-center gap-1.5">
                            <Star className="w-5 h-5 text-yellow-500 shrink-0" />
                            <span className="text-xl font-bold text-slate-100">{stats.bestStreak}</span>
                            <span className="text-[10px] font-black text-slate-500 mt-1">{streakUnit}</span>
                        </div>
                    </Card>

                    {/* Current Streak — with unit label */}
                    <Card className="p-3 bg-slate-900 border-slate-800 flex flex-col items-center justify-center gap-1">
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{t('streak')}</span>
                        <div className="flex items-center gap-1.5">
                            <Flame className={cn("w-5 h-5 shrink-0", stats.currentStreak > 0 ? "text-orange-500" : "text-slate-700")} />
                            <span className="text-xl font-bold text-slate-100">{stats.currentStreak}</span>
                            <span className="text-[10px] font-black text-slate-500 mt-1">{streakUnit}</span>
                        </div>
                    </Card>
                </div>

                {/* 2. Frequency Heatmap (Calendar) — with month navigation */}
                <Card className="p-4 bg-slate-900 border-slate-800 space-y-3">
                    <div className="flex items-center justify-between">
                        <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                            <CalendarIcon className="w-4 h-4 text-sky-500" />
                            {t('monthly_consistency')}
                        </h3>
                        <div className="flex items-center gap-1">
                            <button
                                onClick={() => setCalendarMonth(prev => subMonths(prev, 1))}
                                className="w-7 h-7 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-all"
                            >
                                <ChevronLeft className="w-4 h-4" />
                            </button>
                            <span className="text-xs font-bold text-slate-300 min-w-[80px] text-center">
                                {format(calendarMonth, 'MMM yyyy', { locale })}
                            </span>
                            <button
                                onClick={() => setCalendarMonth(prev => {
                                    const next = addMonths(prev, 1)
                                    return next > new Date() ? prev : next
                                })}
                                className={cn(
                                    "w-7 h-7 rounded-lg flex items-center justify-center transition-all",
                                    getMonth(calendarMonth) === getMonth(new Date()) && getYear(calendarMonth) === getYear(new Date())
                                        ? "text-slate-700 cursor-not-allowed"
                                        : "text-slate-400 hover:text-slate-100 hover:bg-slate-800"
                                )}
                            >
                                <ChevronRight className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                    <div className="grid grid-cols-7 gap-2">
                        {[
                            t('day_m'), t('day_t'), t('day_w'), t('day_th'), t('day_f'), t('day_s'), t('day_su')
                        ].map((d, i) => (
                            <div key={i} className="text-[9px] font-black text-slate-600 text-center uppercase">{d}</div>
                        ))}
                        {(() => {
                            const start = startOfMonth(calendarMonth)
                            const end = endOfMonth(calendarMonth)
                            const startPadding = (start.getDay() + 6) % 7
                            const days = eachDayOfInterval({ start, end })
                            
                            const items = []
                            for (let i = 0; i < startPadding; i++) items.push(<div key={`pad-${i}`} />)
                            
                            days.forEach(day => {
                                const isCompleted = stats.habitLogs.includes(startOfDay(day).getTime())
                                const isToday = isSameDay(day, new Date())
                                const isFuture = day > new Date()
                                items.push(
                                    <div 
                                        key={day.getTime()} 
                                        className={cn(
                                            "aspect-square rounded-lg flex items-center justify-center text-[10px] font-bold transition-all relative",
                                            isFuture ? "text-slate-700 bg-slate-800/20" :
                                            isCompleted ? "text-white" : "text-slate-600 bg-slate-800/40",
                                            isToday ? "ring-2 ring-sky-500 ring-offset-2 ring-offset-slate-900" : ""
                                        )}
                                        style={isCompleted ? { backgroundColor: habit.color } : {}}
                                    >
                                        {format(day, 'd')}
                                        {isCompleted && (
                                            <span className="absolute -top-0.5 -right-0.5 w-1.5 h-1.5 bg-white rounded-full shadow-sm" />
                                        )}
                                    </div>
                                )
                            })
                            return items
                        })()}
                    </div>
                </Card>

                {/* 3. Weekly Evolution with goal line + Reminder */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* 8-Week Evolution Chart with goal line */}
                    <Card className="p-4 bg-slate-900 border-slate-800 space-y-3">
                        <div className="flex items-center justify-between">
                            <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                                <Activity className="w-4 h-4 text-emerald-500" />
                                {t('weekly_evolution')}
                            </h3>
                            {/* Goal indicator legend */}
                            <div className="flex items-center gap-1.5">
                                <div className="w-4 border-t-2 border-dashed border-rose-500/70" />
                                <span className="text-[9px] font-black text-rose-400/80 uppercase">meta {habit.goal}d</span>
                            </div>
                        </div>
                        <div className="relative flex items-end justify-between gap-1 h-28">
                            {/* Goal line overlay */}
                            <div 
                                className="absolute left-0 right-0 border-t-2 border-dashed border-rose-500/50 pointer-events-none z-10"
                                style={{ bottom: `${(habit.goal / maxWeekly) * 100}%` }}
                            />
                            {stats.weeklyEvolution.map((week, i) => {
                                const height = Math.max((week.count / maxWeekly) * 100, week.count > 0 ? 8 : 0)
                                const metGoal = week.count >= habit.goal
                                return (
                                    <div key={i} className="flex flex-col items-center gap-1.5 flex-1 group">
                                        {week.count > 0 && (
                                            <span className={cn(
                                                "text-[9px] font-black",
                                                metGoal ? "text-emerald-400" : "text-slate-400"
                                            )}>{week.count}</span>
                                        )}
                                        <div className="w-full flex-1 flex items-end">
                                            <div
                                                className="w-full rounded-t-sm transition-all duration-700"
                                                style={{
                                                    height: week.count === 0 ? '3px' : `${height}%`,
                                                    backgroundColor: week.isCurrentWeek
                                                        ? habit.color
                                                        : metGoal
                                                            ? `${habit.color}90`
                                                            : `${habit.color}40`,
                                                    boxShadow: week.isCurrentWeek && week.count > 0
                                                        ? `0 0 12px ${habit.color}55`
                                                        : 'none',
                                                    opacity: week.count === 0 ? 0.2 : 1,
                                                }}
                                            />
                                        </div>
                                        <span className={cn(
                                            "text-[8px] font-black uppercase leading-none",
                                            week.isCurrentWeek ? "text-slate-300" : "text-slate-700"
                                        )}>{week.label}</span>
                                    </div>
                                )
                            })}
                        </div>
                        <p className="text-[9px] text-slate-600 italic">
                            <span className="text-emerald-500">■</span> meta cumplida &nbsp;
                            <span style={{ color: `${habit.color}40` }}>■</span> sin cumplir
                        </p>
                    </Card>

                    {/* Reminder Settings */}
                    <Card className="p-4 bg-slate-900 border-slate-800 space-y-4">
                        <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                            <Clock className="w-4 h-4 text-sky-500" />
                            {t('reminder')}
                        </h3>
                        <div className="flex flex-col gap-3 py-2">
                            {habit.reminderTime ? (
                                <div className="flex items-center justify-between p-3 rounded-xl bg-sky-500/10 border border-sky-500/20">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-sky-500 flex items-center justify-center text-white font-bold text-sm">
                                            {habit.reminderTime}
                                        </div>
                                        <div>
                                            <p className="text-sm font-bold text-slate-200">{t('activated')}</p>
                                            <p className="text-[10px] text-slate-500 uppercase font-black">{t('daily_reminder')}</p>
                                        </div>
                                    </div>
                                    <CheckCircle2 className="w-6 h-6 text-sky-500" />
                                </div>
                            ) : (
                                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-800/40 border border-slate-700/50">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-600 font-bold">
                                            --
                                        </div>
                                        <div>
                                            <p className="text-sm font-bold text-slate-500">{t('not_set')}</p>
                                            <p className="text-[10px] text-slate-600 uppercase font-black">{t('daily_reminder')}</p>
                                        </div>
                                    </div>
                                    <XCircle className="w-6 h-6 text-slate-700" />
                                </div>
                            )}
                            <p className="text-[10px] text-slate-500 leading-relaxed italic">
                                {t('notification_info')}
                            </p>
                        </div>
                    </Card>
                </div>

                <div className="flex gap-3">
                    <Button 
                        onClick={onClose}
                        className="w-full bg-slate-800 hover:bg-slate-700 text-white rounded-xl py-3 font-bold border-2 border-slate-700"
                    >
                        {t('close')}
                    </Button>
                </div>
            </div>
        </Modal>
    )
}

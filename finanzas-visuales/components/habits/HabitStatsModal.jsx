'use client'

import { useMemo } from 'react'
import { Modal, Card, Button } from '@/components/ui/UI'
import { 
    Trophy, Flame, Calendar as CalendarIcon, 
    TrendingUp, Activity, Clock, ChevronDown,
    CheckCircle2, XCircle, Star
} from 'lucide-react'
import { format, subMonths, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay, startOfWeek, endOfWeek, differenceInDays, isAfter, subDays, startOfDay } from 'date-fns'
import { useLanguage } from '@/lib/i18n'
import { cn } from '@/lib/utils'

export function HabitStatsModal({ isOpen, onClose, habit, logs = [] }) {
    const { t, locale } = useLanguage()

    // Calculate Statistics
    const stats = useMemo(() => {
        if (!habit || !logs) return null

        const habitLogs = logs.filter(l => l.habitId === habit.id).map(l => startOfDay(new Date(l.date)).getTime())
        const total = habitLogs.length
        
        // Compliance % (Last 30 days)
        const last30Days = [...Array(30)].map((_, i) => subDays(startOfDay(new Date()), i).getTime())
        const completedLast30 = last30Days.filter(d => habitLogs.includes(d)).length
        const score = Math.round((completedLast30 / 30) * 100)

        // Streaks
        let currentStreak = 0
        let bestStreak = 0
        let tempStreak = 0
        
        // To calculate streaks, we need a sorted list of unique days
        const sortedDays = [...new Set(habitLogs)].sort((a, b) => b - a) // Latest first
        
        // Current Streak
        let checkDay = startOfDay(new Date())
        while (habitLogs.includes(checkDay.getTime())) {
            currentStreak++
            checkDay = subDays(checkDay, 1)
        }
        // If not today, check if it was yesterday
        if (currentStreak === 0) {
            checkDay = subDays(startOfDay(new Date()), 1)
            while (habitLogs.includes(checkDay.getTime())) {
                currentStreak++
                checkDay = subDays(checkDay, 1)
            }
        }

        // Best Streak (All time)
        const allDaysSorted = [...new Set(habitLogs)].sort((a, b) => a - b) // Oldest first
        if (allDaysSorted.length > 0) {
            tempStreak = 1
            for (let i = 1; i < allDaysSorted.length; i++) {
                const diff = differenceInDays(allDaysSorted[i], allDaysSorted[i-1])
                if (diff === 1) {
                    tempStreak++
                } else {
                    bestStreak = Math.max(bestStreak, tempStreak)
                    tempStreak = 1
                }
            }
            bestStreak = Math.max(bestStreak, tempStreak)
        }

        // Frequency by Day of Week
        const weekdayFreq = [0, 0, 0, 0, 0, 0, 0] // Sun-Sat
        habitLogs.forEach(d => {
            weekdayFreq[new Date(d).getDay()]++
        })

        return {
            total,
            score,
            currentStreak,
            bestStreak,
            weekdayFreq,
            habitLogs
        }
    }, [habit, logs])

    if (!habit || !stats) return null

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

                    <Card className="p-3 bg-slate-900 border-slate-800 flex flex-col items-center justify-center gap-1">
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{t('best')}</span>
                        <div className="flex items-center gap-2">
                            <Star className="w-5 h-5 text-yellow-500" />
                            <span className="text-xl font-bold text-slate-100">{stats.bestStreak}</span>
                        </div>
                    </Card>

                    <Card className="p-3 bg-slate-900 border-slate-800 flex flex-col items-center justify-center gap-1">
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{t('streak')}</span>
                        <div className="flex items-center gap-2">
                            <Flame className={cn("w-5 h-5", stats.currentStreak > 0 ? "text-orange-500" : "text-slate-700")} />
                            <span className="text-xl font-bold text-slate-100">{stats.currentStreak}</span>
                        </div>
                    </Card>
                </div>

                {/* 2. Frequency Heatmap (Calendar) */}
                <Card className="p-4 bg-slate-900 border-slate-800 space-y-4">
                    <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                        <CalendarIcon className="w-4 h-4 text-sky-500" />
                        {t('monthly_consistency')}
                    </h3>
                    <div className="grid grid-cols-7 gap-2">
                        {[
                            t('day_m'), t('day_t'), t('day_w'), t('day_th'), t('day_f'), t('day_s'), t('day_su')
                        ].map(d => (
                            <div key={d} className="text-[9px] font-black text-slate-600 text-center uppercase">{d}</div>
                        ))}
                        {(() => {
                            const today = new Date()
                            const start = startOfMonth(today)
                            const end = endOfMonth(today)
                            const startPadding = (start.getDay() + 6) % 7 // Adjusted for Monday start
                            const days = eachDayOfInterval({ start, end })
                            
                            const items = []
                            for (let i = 0; i < startPadding; i++) items.push(<div key={`pad-${i}`} />)
                            
                            days.forEach(day => {
                                const isCompleted = stats.habitLogs.includes(startOfDay(day).getTime())
                                const isToday = isSameDay(day, new Date())
                                items.push(
                                    <div 
                                        key={day.getTime()} 
                                        className={cn(
                                            "aspect-square rounded-lg flex items-center justify-center text-[10px] font-bold transition-all relative",
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

                {/* 3. Distribution & Streaks */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Weekday Distribution */}
                    <Card className="p-4 bg-slate-900 border-slate-800 space-y-4">
                        <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                            <Activity className="w-4 h-4 text-emerald-500" />
                        {t('weekly_progress')}
                        </h3>
                        <div className="flex items-end justify-between h-32 pt-2">
                            {[
                                t('day_su'), t('day_m'), t('day_t'), t('day_w'), t('day_th'), t('day_f'), t('day_s')
                            ].map((day, i) => {
                                const max = Math.max(...stats.weekdayFreq, 1)
                                const height = (stats.weekdayFreq[i] / max) * 100
                                return (
                                    <div key={day} className="flex flex-col items-center gap-2 flex-1 group">
                                        <div className="w-full px-1.5 h-full flex items-end">
                                            <div 
                                                className="w-full rounded-t-md transition-all duration-500 group-hover:brightness-125"
                                                style={{ 
                                                    height: `${height}%`, 
                                                    backgroundColor: `${habit.color}cc`,
                                                    boxShadow: stats.weekdayFreq[i] > 0 ? `0 0 10px ${habit.color}33` : 'none'
                                                }}
                                            />
                                        </div>
                                        <span className="text-[10px] font-black text-slate-600 uppercase">{day}</span>
                                    </div>
                                )
                            })}
                        </div>
                    </Card>

                    {/* Notification/Reminder Settings Placeholder Info */}
                    <Card className="p-4 bg-slate-900 border-slate-800 space-y-4">
                        <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                            <Clock className="w-4 h-4 text-sky-500" />
                            {t('reminder')}
                        </h3>
                        <div className="flex flex-col gap-3 py-2">
                            {habit.reminderTime ? (
                                <div className="flex items-center justify-between p-3 rounded-xl bg-sky-500/10 border border-sky-500/20">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-sky-500 flex items-center justify-center text-white font-bold">
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

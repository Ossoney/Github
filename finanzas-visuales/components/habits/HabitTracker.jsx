'use client'

import { useState, useEffect } from 'react'
import { Card, Button } from '@/components/ui/UI'
import { 
    Plus, Check, X, ChevronLeft, Trash2, Edit2, Target, 
    Book, Activity, BookOpen, Dumbbell, GlassWater, 
    Brain, Utensils, Heart, GripVertical, BarChart3
} from 'lucide-react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { useLanguage } from '@/lib/i18n'
import { format, subDays, startOfDay } from 'date-fns'
import { cn } from '@/lib/utils'
import { HabitForm } from './HabitForm'
import { HabitStatsModal } from './HabitStatsModal'
import { Reorder, useDragControls, motion, AnimatePresence } from 'framer-motion'

// Icon mapping helper
const IconMap = {
    Book,
    Activity,
    BookOpen,
    Dumbbell,
    GlassWater,
    Brain,
    Utensils,
    Heart,
    Target
}

export function HabitTracker() {
    const { t, locale } = useLanguage()
    const [isFormOpen, setIsFormOpen] = useState(false)
    const [editingHabit, setEditingHabit] = useState(null)
    const [statsHabit, setStatsHabit] = useState(null)
    const [localHabits, setLocalHabits] = useState([])

    const habits = useLiveQuery(() => db.habits.orderBy('order').toArray())
    const habitLogs = useLiveQuery(() => db.habitLogs.toArray())

    // Update local state when habits change from DB
    useEffect(() => {
        if (habits) {
            setLocalHabits(habits)
        }
    }, [habits])

    // Get last 7 days
    const days = [...Array(7)].map((_, i) => subDays(startOfDay(new Date()), i))

    const toggleHabit = async (habitId, date) => {
        const existing = await db.habitLogs
            .where({ habitId, date: date.getTime() })
            .first()

        const isCompleting = !existing

        if (existing) {
            await db.habitLogs.delete(existing.id)
        } else {
            await db.habitLogs.add({ habitId, date: date.getTime() })
        }

        return isCompleting
    }

    const deleteHabit = async (id) => {
        if (confirm(t('confirm_delete_habit'))) {
            await db.habits.delete(id)
            await db.habitLogs.where('habitId').equals(id).delete()
        }
    }

    const getWeeklyProgress = (habitId) => {
        const last7Days = [...Array(7)].map((_, i) => subDays(startOfDay(new Date()), i).getTime())
        const logs = habitLogs?.filter(l => l.habitId === habitId && last7Days.includes(l.date)) || []
        return logs.length
    }

    const handleReorder = async (newOrder) => {
        setLocalHabits(newOrder)
        // Persist to DB
        try {
            await db.transaction('rw', db.habits, async () => {
                for (let i = 0; i < newOrder.length; i++) {
                    await db.habits.update(newOrder[i].id, { order: i + 1 })
                }
            })
        } catch (err) {
            console.error("Failed to save new order:", err)
        }
    }

    if (!habits) return null

    return (
        <div className="space-y-6 px-1">
            <header className="flex justify-between items-center">
                <div className="flex items-center gap-4">
                    <Button variant="ghost" size="icon" onClick={() => window.history.back()} className="text-slate-400">
                        <ChevronLeft className="w-6 h-6" />
                    </Button>
                    <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
                        <Target className="w-6 h-6 text-sky-500" />
                        {t('habit_tracker')}
                    </h1>
                </div>
                <Button 
                    onClick={() => { setEditingHabit(null); setIsFormOpen(true); }}
                    className="bg-sky-500 hover:bg-sky-600 text-white rounded-xl flex items-center gap-2"
                >
                    <Plus className="w-5 h-5" />
                    <span className="hidden sm:inline">{t('new_habit')}</span>
                </Button>
            </header>

            {/* List Header (Hidden on small mobile) */}
            <div className="hidden md:grid grid-cols-[1fr_auto] gap-4 px-6 text-[10px] font-black text-slate-500 uppercase tracking-widest">
                <div className="flex gap-4">
                    <div className="w-8"></div> {/* Spacer for drag */}
                    <div className="w-12 text-center">Icon</div>
                    <div>{t('habit_name')}</div>
                </div>
                <div className="flex gap-2">
                    {days.map(day => (
                        <div key={day.getTime()} className="w-10 text-center">
                            {format(day, 'EEE', { locale })}
                        </div>
                    ))}
                    <div className="w-20 text-center">{t('habit_goal')}</div>
                    <div className="w-16"></div>
                </div>
            </div>

            <Reorder.Group axis="y" values={localHabits} onReorder={handleReorder} className="space-y-3">
                {localHabits.length === 0 ? (
                    <Card className="p-12 text-center text-slate-500 bg-slate-900/50 border-slate-800">
                        <Target className="w-12 h-12 mx-auto mb-4 opacity-20" />
                        <p>{t('no_habits')}</p>
                    </Card>
                ) : (
                    localHabits.map(habit => (
                        <HabitItem 
                            key={habit.id} 
                            habit={habit} 
                            days={days} 
                            habitLogs={habitLogs}
                            t={t}
                            locale={locale}
                            weeklyProgress={getWeeklyProgress(habit.id)}
                            onToggle={toggleHabit}
                            onEdit={() => { setEditingHabit(habit); setIsFormOpen(true); }}
                            onDelete={() => deleteHabit(habit.id)}
                            onOpenStats={() => setStatsHabit(habit)}
                        />
                    ))
                )}
            </Reorder.Group>

            <HabitForm 
                isOpen={isFormOpen} 
                onClose={() => setIsFormOpen(false)} 
                habit={editingHabit} 
            />

            <HabitStatsModal 
                isOpen={!!statsHabit}
                onClose={() => setStatsHabit(null)}
                habit={statsHabit}
                logs={habitLogs}
            />
        </div>
    )
}

function HabitItem({ habit, days, habitLogs, t, locale, weeklyProgress, onToggle, onEdit, onDelete, onOpenStats }) {
    const progressPercent = Math.min(100, (weeklyProgress / habit.goal) * 100)
    const controls = useDragControls()
    const [explosions, setExplosions] = useState([])

    // Calculate mini heatmap (14 days / 2 weeks)
    const miniHeatmap = [...Array(14)].map((_, i) => {
        const d = subDays(startOfDay(new Date()), 13 - i).getTime()
        return habitLogs?.some(l => l.habitId === habit.id && l.date === d)
    })

    const handleToggle = async (day) => {
        const isCompleting = await onToggle(habit.id, day)
        if (isCompleting) {
            const newId = Date.now()
            setExplosions(prev => [...prev, { id: newId, day: day.getTime() }])
            setTimeout(() => {
                setExplosions(prev => prev.filter(e => e.id !== newId))
            }, 1000)
        }
    }

    return (
        <Reorder.Item 
            value={habit} 
            dragListener={false} 
            dragControls={controls}
            className=""
        >
            <Card className="bg-slate-900/50 border-slate-800 group hover:border-slate-700 transition-all overflow-hidden relative">
                <div className="p-3 sm:p-4 flex flex-col xl:flex-row xl:items-center justify-between gap-4">
                    
                    {/* Left Section: Drag + Icon + Name + Heatmap */}
                    <div className="flex items-start gap-3 sm:gap-4">
                        {/* Drag Handle */}
                        <div 
                            className="cursor-grab active:cursor-grabbing p-1 text-slate-600 hover:text-slate-400 mt-2 shrink-0 touch-none select-none"
                            onPointerDown={(e) => controls.start(e)}
                        >
                            <GripVertical className="w-5 h-5" />
                        </div>

                        {/* Habit Icon & Progress Ring */}
                        <div 
                            className="w-12 h-12 rounded-2xl flex items-center justify-center relative shrink-0"
                            style={{ backgroundColor: `${habit.color}15`, border: `2px solid ${habit.color}30` }}
                        >
                            <svg className="absolute inset-0 w-full h-full -rotate-90">
                                <circle
                                    cx="24" cy="24" r="21"
                                    fill="transparent"
                                    stroke={habit.color}
                                    strokeWidth="3"
                                    strokeDasharray={132}
                                    strokeDashoffset={132 - (132 * progressPercent) / 100}
                                    strokeLinecap="round"
                                />
                            </svg>
                            <span className="relative z-10">
                                {(() => {
                                    const IconComp = IconMap[habit.icon] || Target
                                    return <IconComp className="w-6 h-6" style={{ color: habit.color }} />
                                })()}
                            </span>
                        </div>

                        {/* Name & Heatmap */}
                        <div className="flex-1 min-w-0">
                            <div className="mb-2">
                                <div 
                                    className="font-bold text-slate-100 group-hover:text-sky-400 transition-colors truncate text-base leading-tight cursor-pointer"
                                    onClick={onOpenStats}
                                >
                                    {habit.name}
                                </div>
                                <div className="text-[10px] text-slate-500 uppercase font-black tracking-tighter mt-1">
                                    {weeklyProgress} / {habit.goal} {t('week')}
                                </div>
                            </div>
                            
                            {/* Mini Heatmap: BELOW and LEFT */}
                            <div className="flex flex-wrap gap-1 mt-1 opacity-70">
                                {miniHeatmap.map((done, i) => (
                                    <div 
                                        key={i} 
                                        className={cn(
                                            "w-2 h-2 rounded-full transition-all duration-300",
                                            done ? "shadow-[0_0_8px] shadow-current scale-110" : "bg-slate-800"
                                        )}
                                        style={done ? { backgroundColor: habit.color, color: habit.color } : {}}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Right Section: Checks + Actions */}
                    <div className="flex items-center justify-between xl:justify-end gap-2 sm:gap-3 border-t border-slate-800/50 xl:border-0 pt-3 xl:pt-0">
                        {/* Days Grid - 7 Days now */}
                        <div className="flex gap-1.5 sm:gap-2 overflow-x-auto pb-1 sm:pb-0 scrollbar-hide">
                            {days.map(day => {
                                const isDone = habitLogs?.some(l => l.habitId === habit.id && l.date === day.getTime())
                                const isExploding = explosions.some(e => e.day === day.getTime())

                                return (
                                    <div key={day.getTime()} className="flex flex-col items-center gap-1 shrink-0 relative">
                                        <div className="text-[8px] font-black text-slate-600 uppercase">
                                            {format(day, 'EEE', { locale })}
                                        </div>
                                        <button
                                            onClick={() => handleToggle(day)}
                                            className={cn(
                                                "w-9 h-9 sm:w-10 sm:h-10 rounded-xl flex items-center justify-center transition-all border-2 relative overflow-hidden",
                                                isDone 
                                                    ? "bg-slate-100 border-white shadow-lg active:scale-95" 
                                                    : "bg-slate-800/40 border-slate-700/50 hover:border-slate-500 text-slate-600 active:scale-95"
                                            )}
                                            style={isDone ? { backgroundColor: habit.color, borderColor: 'white' } : {}}
                                        >
                                            <AnimatePresence>
                                                {isDone && (
                                                    <motion.div
                                                        initial={{ scale: 0, rotate: -20 }}
                                                        animate={{ scale: 1, rotate: 0 }}
                                                        exit={{ scale: 0 }}
                                                        className="relative z-10"
                                                    >
                                                        <Check className="w-5 h-5 text-white stroke-[3.5px]" />
                                                    </motion.div>
                                                )}
                                            </AnimatePresence>
                                        </button>

                                        {/* Particle Explosion */}
                                        <AnimatePresence>
                                            {isExploding && (
                                                <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
                                                    {[...Array(8)].map((_, i) => (
                                                        <motion.div
                                                            key={i}
                                                            initial={{ x: 0, y: 0, scale: 1, opacity: 1 }}
                                                            animate={{ 
                                                                x: (Math.random() - 0.5) * 60, 
                                                                y: (Math.random() - 0.5) * 60, 
                                                                scale: 0,
                                                                opacity: 0,
                                                                rotate: Math.random() * 360
                                                            }}
                                                            transition={{ duration: 0.6, ease: "easeOut" }}
                                                            className="absolute w-2 h-2 rounded-full"
                                                            style={{ backgroundColor: habit.color }}
                                                        />
                                                    ))}
                                                </div>
                                            )}
                                        </AnimatePresence>
                                    </div>
                                )
                            })}
                        </div>

                        {/* Action Buttons */}
                        <div className="flex items-center gap-1 pl-1">
                            <Button 
                                variant="ghost" 
                                size="icon" 
                                className="h-9 w-9 text-slate-500 hover:text-sky-400"
                                onClick={onOpenStats}
                            >
                                <BarChart3 className="w-4 h-4" />
                            </Button>
                            <Button 
                                variant="ghost" 
                                size="icon" 
                                className="h-9 w-9 text-slate-500 hover:text-sky-400"
                                onClick={onEdit}
                            >
                                <Edit2 className="w-4 h-4" />
                            </Button>
                            <Button 
                                variant="ghost" 
                                size="icon" 
                                className="h-9 w-9 text-slate-500 hover:text-red-500 bg-slate-800/50 md:bg-transparent"
                                onClick={onDelete}
                            >
                                <Trash2 className="w-4 h-4" />
                            </Button>
                        </div>
                    </div>
                </div>
            </Card>
        </Reorder.Item>
    )
}

'use client'

import { useState, useEffect } from 'react'
import { Modal, Button, Input } from '@/components/ui/UI'
import { db } from '@/lib/db'
import { useLanguage } from '@/lib/i18n'
import { NotificationRequestModal } from '@/components/ui/NotificationRequestModal'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

const PRESET_COLORS = [
    '#3b82f6', '#ef4444', '#10b981', '#f59e0b', 
    '#8b5cf6', '#a855f7', '#ec4899', '#06b6d4',
    '#f97316', '#64748b'
]

export function HabitForm({ isOpen, onClose, habit }) {
    const { t } = useLanguage()
    const [name, setName] = useState('')
    const [goal, setGoal] = useState(3)
    const [color, setColor] = useState(PRESET_COLORS[0])
    const [reminderTime, setReminderTime] = useState(null)
    const [reminderEnabled, setReminderEnabled] = useState(false)
    const [isNotifModalOpen, setIsNotifModalOpen] = useState(false)

    useEffect(() => {
        if (habit) {
            setName(habit.name)
            setGoal(habit.goal)
            setColor(habit.color || PRESET_COLORS[0])
            setReminderTime(habit.reminderTime || null)
            setReminderEnabled(habit.reminderEnabled || false)
        } else {
            setName('')
            setGoal(3)
            setColor(PRESET_COLORS[0])
            setReminderTime(null)
            setReminderEnabled(false)
        }
    }, [habit, isOpen])

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!name.trim()) return

        const data = {
            name: name.trim(),
            goal: parseInt(goal),
            frequency: 'week',
            color,
            reminderTime,
            reminderEnabled
        }

        if (habit) {
            await db.habits.update(habit.id, data)
        } else {
            // Get max order to put new habit at the end
            const lastHabit = await db.habits.orderBy('order').last()
            const newOrder = lastHabit ? (lastHabit.order || 0) + 1 : 1
            await db.habits.add({ ...data, order: newOrder })
        }

        onClose()
    }

    return (
        <Modal isOpen={isOpen} onClose={onClose} title={habit ? t('edit_habit') : t('new_habit')}>
            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">{t('habit_name')}</label>
                    <Input 
                        placeholder="Ej: Meditar, Beber agua..." 
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        autoFocus
                        className="bg-slate-800 border-slate-700 text-lg py-6 focus:border-sky-500 rounded-xl"
                    />
                </div>

                <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">{t('habit_goal')}</label>
                        <div className="flex items-center gap-3">
                            <Input 
                                type="number" 
                                min="1" 
                                max="7" 
                                value={goal}
                                onChange={(e) => setGoal(e.target.value)}
                                className="bg-slate-800 border-slate-700 text-center text-xl font-bold rounded-xl"
                            />
                            <span className="text-sm font-medium text-slate-400">{t('week')}</span>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Recordatorio</label>
                            <button
                                type="button"
                                onClick={() => {
                                    if (!reminderEnabled) {
                                        // Turning ON: Show our beautiful modal
                                        setIsNotifModalOpen(true);
                                    } else {
                                        // Turning OFF
                                        setReminderEnabled(false);
                                    }
                                }}
                                className={cn(
                                    "relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none",
                                    reminderEnabled ? "bg-sky-500" : "bg-slate-700"
                                )}
                            >
                                <span
                                    className={cn(
                                        "inline-block h-4 w-4 transform rounded-full bg-white transition-transform",
                                        reminderEnabled ? "translate-x-6" : "translate-x-1"
                                    )}
                                />
                            </button>
                        </div>
                        
                        {reminderEnabled && (
                            <div className="animate-in fade-in slide-in-from-top-2 duration-200">
                                <Input 
                                    type="time" 
                                    value={reminderTime || '09:00'}
                                    onChange={(e) => setReminderTime(e.target.value)}
                                    className="bg-slate-800 border-slate-700 text-center text-xl font-bold rounded-xl"
                                />
                            </div>
                        )}
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">{t('color')}</label>
                    <div className="grid grid-cols-5 gap-2">
                        {PRESET_COLORS.map(c => (
                            <button
                                key={c}
                                type="button"
                                onClick={() => setColor(c)}
                                className={cn(
                                    "w-8 h-8 rounded-full transition-transform hover:scale-110 flex items-center justify-center",
                                    color === c ? "ring-2 ring-white ring-offset-2 ring-offset-slate-900" : ""
                                )}
                                style={{ backgroundColor: c }}
                            >
                                {color === c && <Check className="w-4 h-4 text-white" />}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="flex gap-3 pt-4">
                    <Button 
                        type="button" 
                        variant="ghost" 
                        onClick={onClose} 
                        className="flex-1 border-2 border-slate-800 hover:bg-slate-800 rounded-xl"
                    >
                        {t('cancel')}
                    </Button>
                    <Button 
                        type="submit" 
                        className="flex-1 bg-sky-500 hover:bg-sky-600 text-white rounded-xl shadow-lg shadow-sky-500/20 font-bold"
                    >
                        {t('save')}
                    </Button>
                </div>
            </form>

            <NotificationRequestModal 
                isOpen={isNotifModalOpen}
                onClose={() => setIsNotifModalOpen(false)}
                onPermissionGranted={() => {
                    setReminderEnabled(true);
                    if (!reminderTime) setReminderTime('09:00');
                }}
            />
        </Modal>
    )
}

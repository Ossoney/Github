'use client'

import { useEffect } from 'react'
import { processRecurringTransactions } from '@/lib/recurring'
import { checkHabitReminders } from '@/lib/notifications'
import { db } from '@/lib/db'
import { useStore } from '@/hooks/useStore'

export function InitApp() {
    const { setSelectedWalletId } = useStore()

    useEffect(() => {
        // Check for recurring transactions on app mount
        processRecurringTransactions()
        
        // Habit Reminders
        checkHabitReminders(db)
        const reminderInterval = setInterval(() => checkHabitReminders(db), 60000) // Check every minute

        return () => clearInterval(reminderInterval)

        // Load last selected account
        const loadSettings = async () => {
            try {
                const settings = await db.settings.get('global')
                if (settings?.lastSelectedWalletId !== undefined) {
                    setSelectedWalletId(settings.lastSelectedWalletId)
                }
            } catch (err) {
                console.error("Error loading initial settings:", err)
            }
        }
        loadSettings()
    }, [])

    return null
}

'use client'

import { useEffect } from 'react'
import { processRecurringTransactions } from '@/lib/recurring'
import { db } from '@/lib/db'
import { useStore } from '@/hooks/useStore'

export function InitApp() {
    const { setSelectedWalletId } = useStore()

    useEffect(() => {
        // Check for recurring transactions on app mount
        processRecurringTransactions()

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

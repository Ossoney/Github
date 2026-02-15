'use client'

import { useEffect } from 'react'
import { processRecurringTransactions } from '@/lib/recurring'

export function InitApp() {
    useEffect(() => {
        // Check for recurring transactions on app mount
        processRecurringTransactions()
    }, [])

    return null
}

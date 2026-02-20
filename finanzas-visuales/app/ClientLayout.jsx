'use client'

import { useEffect } from 'react'
import { processRecurringTransactions } from '@/lib/recurring'
import { processAutosave } from '@/lib/autosave'
import { LanguageProvider, useLanguage } from '@/lib/i18n'
import { PrivacyProvider } from '@/lib/privacy'
import { ToastProvider } from '@/components/ui/UI'

export function ClientLayout({ children }) {
    // ... (keep existing useEffect)
    // Check for recurring transactions & Theme on mount
    useEffect(() => {
        processRecurringTransactions()
        processAutosave()

        // Load Theme
        const loadTheme = async () => {
            const settings = await import('@/lib/db').then(m => m.db.settings.get('global'))
            if (settings?.theme) {
                document.documentElement.setAttribute('data-theme', settings.theme)
            }
        }
        loadTheme()
    }, [])

    return (
        <LanguageProvider>
            <PrivacyProvider>
                <ToastProvider>
                    <DynamicTitle />
                    {children}
                </ToastProvider>
            </PrivacyProvider>
        </LanguageProvider>
    )
}

function DynamicTitle() {
    const { t } = useLanguage()
    useEffect(() => {
        document.title = t('meta_title') || 'Visualis | tus Finanzas'
    }, [t])
    return null
}

'use client'

import { useEffect } from 'react'
import { processRecurringTransactions } from '@/lib/recurring'
import { processAutosave } from '@/lib/autosave'
import { LanguageProvider, useLanguage } from '@/lib/i18n'
import { PrivacyProvider } from '@/lib/privacy'
import { ToastProvider } from '@/components/ui/UI'
import { useStore } from '@/hooks/useStore'
import { db } from '@/lib/db'
import { WhatsNewModal } from '@/components/ui/WhatsNewModal'

export function ClientLayout({ children }) {
    const { setSelectedWalletId } = useStore()

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

    return (
        <LanguageProvider>
            <PrivacyProvider>
                <ToastProvider>
                    <DynamicTitle />
                    <WhatsNewModal />
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

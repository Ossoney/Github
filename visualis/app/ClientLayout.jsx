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
import { logger } from '@/lib/logger'

export function ClientLayout({ children }) {
    const { setSelectedWalletId } = useStore()

    // ... (keep existing useEffect)
    // Check for recurring transactions & Theme on mount
    useEffect(() => {
        logger.info('Visualis iniciado en el cliente')

        const handleGlobalError = (event) => {
            logger.error('Error no controlado en la aplicación', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error ? event.error.stack : null
            }, 'window.onerror')
        }

        const handleUnhandledRejection = (event) => {
            logger.error('Promesa rechazada no controlada', {
                reason: event.reason instanceof Error ? event.reason.stack : event.reason
            }, 'unhandledrejection')
        }

        window.addEventListener('error', handleGlobalError)
        window.addEventListener('unhandledrejection', handleUnhandledRejection)

        processRecurringTransactions()
        processAutosave()

        // Load Theme
        const loadTheme = async () => {
            const settings = await import('@/lib/db').then(m => m.db.settings.get('global'))
            if (settings?.theme) {
                let theme = settings.theme
                if (theme === 'forest') theme = 'cyberpunk'
                if (theme === 'light-mint') theme = 'ukiyo-e'
                if (theme === 'light-sky') theme = 'bauhaus'
                if (theme === 'light-warm') theme = 'brutalist'
                if (theme === 'sky') theme = 'futurism'
                if (theme === 'gold') theme = 'fauvism'
                document.documentElement.setAttribute('data-theme', theme)
            } else {
                document.documentElement.setAttribute('data-theme', 'futurism')
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

        return () => {
            window.removeEventListener('error', handleGlobalError)
            window.removeEventListener('unhandledrejection', handleUnhandledRejection)
        }
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

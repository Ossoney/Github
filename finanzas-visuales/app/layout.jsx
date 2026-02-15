'use client'

import './globals.css'
import { Outfit } from 'next/font/google'
import clsx from 'clsx'
import { useEffect } from 'react'
import { processRecurringTransactions } from '@/lib/recurring'
import { LanguageProvider } from '@/lib/i18n'
import { ToastProvider } from '@/components/ui/UI'

const outfit = Outfit({
    subsets: ['latin'],
    variable: '--font-outfit',
    display: 'swap',
})

// ... metadata ...

export default function RootLayout({ children }) {

    // Check for recurring transactions & Theme on mount
    useEffect(() => {
        processRecurringTransactions()

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
        <html lang="es" className={clsx(outfit.variable)}>


            <body className="bg-slate-950 text-slate-50 min-h-screen font-sans antialiased selection:bg-sky-500/30">
                <main className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
                    <LanguageProvider>
                        <ToastProvider>
                            {children}
                        </ToastProvider>
                    </LanguageProvider>
                </main>
            </body>
        </html>
    )
}


import './globals.css'
import { Outfit } from 'next/font/google'
import clsx from 'clsx'
import { ClientLayout } from './ClientLayout'

const outfit = Outfit({
    subsets: ['latin'],
    variable: '--font-outfit',
    display: 'swap',
})

export const viewport = {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
    themeColor: '#0f172a',
}

export const metadata = {
    title: 'Visualis | tus Finanzas',
    description: 'Controla tus gastos e ingresos de forma visual, privada y sencilla. Tu gestor de finanzas personales local-first.',
    manifest: '/manifest.json',
    icons: {
        icon: '/icon.svg',
        apple: '/icon.svg',
    },
    appleWebApp: {
        capable: true,
        statusBarStyle: 'black-translucent',
        title: 'Visualis',
    },
    formatDetection: {
        telephone: false,
    },
}

export default function RootLayout({ children }) {
    return (
        <html lang="es" className={clsx(outfit.variable)}>


            <body className="bg-slate-950 text-slate-50 min-h-screen font-sans antialiased selection:bg-sky-500/30">
                <main className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
                    <ClientLayout>
                        {children}
                    </ClientLayout>
                </main>
            </body>
        </html>
    )
}


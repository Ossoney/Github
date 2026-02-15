'use client'

import { useLanguage } from '@/lib/i18n'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/UI'
import { Languages, Check } from 'lucide-react'
import { cn } from '@/lib/utils'

export function LanguageSettings() {
    const { language, setLanguage, t } = useLanguage()

    const languages = [
        { code: 'es', name: 'Español', flag: '🇪🇸' },
        { code: 'en', name: 'English', flag: '🇬🇧' },
        { code: 'gl', name: 'GL Galego', flag: null }, // Requested specific format
        { code: 'eu', name: 'EU Euskara', flag: null }, // Using text code instead of flag
        { code: 'ca', name: 'CA Català', flag: null },
    ]

    return (
        <Card className="border-slate-800 bg-slate-900/50">
            <CardHeader>
                <CardTitle className="text-slate-200 flex items-center gap-2">
                    <Languages className="w-5 h-5 text-sky-500" />
                    {t('language')}
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    {languages.map((lang) => (
                        <button
                            key={lang.code}
                            onClick={() => setLanguage(lang.code)}
                            className={cn(
                                "flex items-center gap-2 p-2 rounded-lg border transition-all justify-center sm:justify-start",
                                language === lang.code
                                    ? "bg-sky-500/10 border-sky-500 text-sky-400"
                                    : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700 hover:bg-slate-900"
                            )}
                        >
                            {lang.flag && <span className="text-lg">{lang.flag}</span>}
                            <span className="font-medium text-xs sm:text-sm whitespace-nowrap">{lang.name}</span>
                        </button>
                    ))}
                </div>
            </CardContent>
        </Card>
    )
}

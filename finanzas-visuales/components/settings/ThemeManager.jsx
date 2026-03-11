import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/UI'
import { Check, Palette } from 'lucide-react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

// 9 Sophisticated Themes
const themes = [
    { id: 'sky', color: '#0ea5e9' },
    { id: 'gold', color: '#f59e0b' },
    { id: 'forest', color: '#10b981' },
    { id: 'nebula', color: '#8b5cf6' },
    { id: 'mondrian', color: '#2563eb' },
    { id: 'wine', color: '#f43f5e' },
    { id: 'light-sky', color: '#e0f2fe' },
    { id: 'light-mint', color: '#d1fae5' },
    { id: 'light-warm', color: '#ffe4e6' },
]

export function ThemeManager() {
    const settings = useLiveQuery(() => db.settings.get('global'))
    const { t } = useLanguage()
    const [currentTheme, setCurrentTheme] = useState('sky')

    useEffect(() => {
        if (settings?.theme) {
            setCurrentTheme(settings.theme)
            // Apply to document
            document.documentElement.setAttribute('data-theme', settings.theme)
        }
    }, [settings])

    const handleThemeChange = async (themeId) => {
        setCurrentTheme(themeId)
        document.documentElement.setAttribute('data-theme', themeId)

        // Save to DB
        const currentSettings = await db.settings.get('global') || { id: 'global' }
        await db.settings.put({ ...currentSettings, theme: themeId })
    }

    return (
        <Card className="w-full bg-slate-900/50 border-slate-800 animate-in fade-in">
            {/* Header */}
            <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50 rounded-t-xl">
                <h2 className="text-lg font-bold text-slate-200 flex items-center gap-2">
                    <Palette className="w-5 h-5 text-sky-500" /> {t('appearance')}
                </h2>
            </div>

            <div className="p-6">
                <p className="text-slate-400 mb-6 text-sm">{t('choose_theme')}</p>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 gap-4">
                    {themes.map(theme => (
                        <button
                            key={theme.id}
                            onClick={() => handleThemeChange(theme.id)}
                            className={cn(
                                "flex items-center gap-3 p-3 rounded-xl border transition-all text-left group",
                                currentTheme === theme.id
                                    ? "bg-slate-800 border-sky-500 ring-1 ring-sky-500 shadow-lg shadow-sky-500/10"
                                    : "bg-slate-800/50 border-slate-800 hover:border-slate-700 hover:bg-slate-800"
                            )}
                        >
                            <div
                                className="w-8 h-8 rounded-full shadow-inner flex items-center justify-center"
                                style={{ backgroundColor: theme.color }}
                            >
                                {currentTheme === theme.id && <Check className="w-4 h-4 text-white drop-shadow-md" />}
                            </div>
                            <span className={cn(
                                "font-medium text-sm",
                                currentTheme === theme.id ? "text-slate-100" : "text-slate-400 group-hover:text-slate-300"
                            )}>
                                {t('theme_names')?.[theme.id] || theme.id}
                            </span>
                        </button>
                    ))}
                </div>
            </div>
        </Card>
    )
}

'use client'

import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent, Button, Input, Switch, useToast, ConfirmDialog } from '@/components/ui/UI'
import { Languages, Check, Banknote, Palette, Trash2, AlertTriangle, Database, Download, FileSpreadsheet, Upload, User, Camera, Save } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useLanguage, CURRENCIES } from '@/lib/i18n'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { exportToExcel, importFromExcel } from '@/lib/utils'

// ----------------------------------------------------------------------
// LANGUAGE SETTINGS
// ----------------------------------------------------------------------
export function LanguageSettings() {
    const { language, setLanguage, t } = useLanguage()

    const languages = [
        { code: 'es', name: 'Español', flag: '🇪🇸' },
        { code: 'en', name: 'English', flag: '🇬🇧' },
        { code: 'gl', name: 'GL Galego', flag: null },
        { code: 'eu', name: 'EU Euskara', flag: null },
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

// ----------------------------------------------------------------------
// CURRENCY SETTINGS
// ----------------------------------------------------------------------
export function CurrencySettings() {
    const { currency, setCurrency, t } = useLanguage()

    return (
        <Card className="border-slate-800 bg-slate-900/50">
            <CardHeader>
                <CardTitle className="text-slate-200 flex items-center gap-2">
                    <Banknote className="w-5 h-5 text-emerald-500" />
                    {t('main_currency')}
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2">
                    {CURRENCIES.map((curr) => (
                        <button
                            key={curr.code}
                            onClick={() => setCurrency(curr.code)}
                            className={cn(
                                "flex flex-col items-center justify-center p-2 rounded-lg border transition-all aspect-square",
                                currency === curr.code
                                    ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                    : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700 hover:bg-slate-900"
                            )}
                            title={curr.name}
                        >
                            <span className="font-bold text-lg">{curr.symbol}</span>
                            <span className="text-xs opacity-70">{curr.code}</span>
                        </button>
                    ))}
                </div>
            </CardContent>
        </Card>
    )
}

// ----------------------------------------------------------------------
// THEME SETTINGS (Renamed from ThemeManager)
// ----------------------------------------------------------------------
const themes = [
    { id: 'sky', color: '#0ea5e9' },
    { id: 'gold', color: '#f59e0b' },
    { id: 'forest', color: '#10b981' },
    { id: 'nebula', color: '#8b5cf6' },
    { id: 'cyber', color: '#06b6d4' },
    { id: 'wine', color: '#f43f5e' },
    { id: 'coffee', color: '#f97316' },
    { id: 'royal', color: '#3b82f6' },
    { id: 'minimal', color: '#ffffff' },
]

export function ThemeSettings() {
    const settings = useLiveQuery(() => db.settings.get('global'))
    const { t } = useLanguage()
    const [currentTheme, setCurrentTheme] = useState('sky')

    useEffect(() => {
        if (settings?.theme) {
            setCurrentTheme(settings.theme)
            document.documentElement.setAttribute('data-theme', settings.theme)
        }
    }, [settings])

    const handleThemeChange = async (themeId) => {
        setCurrentTheme(themeId)
        document.documentElement.setAttribute('data-theme', themeId)

        const currentSettings = await db.settings.get('global') || { id: 'global' }
        await db.settings.put({ ...currentSettings, theme: themeId })
    }

    return (
        <Card className="w-full bg-slate-900/50 border-slate-800 animate-in fade-in">
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



// ----------------------------------------------------------------------
// PROFILE SETTINGS
// ----------------------------------------------------------------------

// ... (imports remain mostly same, just ensuring Switch is imported)

// ...

export function ProfileSettings({ className }) {
    const settings = useLiveQuery(() => db.settings.get('global'))
    const { addToast } = useToast()
    const { t } = useLanguage()
    const [name, setName] = useState('')
    const [avatar, setAvatar] = useState(null)
    const [customizeHome, setCustomizeHome] = useState(false)
    const [isSaving, setIsSaving] = useState(false)

    useEffect(() => {
        if (settings) {
            setName(settings.username || '')
            setAvatar(settings.avatar || null)
            setCustomizeHome(settings.customizeHome || false)
        }
    }, [settings])

    const handleFileChange = (e) => {
        const file = e.target.files[0]
        if (file) {
            const reader = new FileReader()
            reader.onloadend = () => {
                setAvatar(reader.result)
            }
            reader.readAsDataURL(file)
        }
    }

    const handleSave = async () => {
        setIsSaving(true)
        try {
            await db.settings.put({
                ...(settings || {}),
                id: 'global',
                username: name,
                avatar: avatar,
                customizeHome: customizeHome,
            })
            addToast(t('profile_saved'), 'success')
        } catch (err) {
            console.error("Error saving profile", err)
            addToast(t('error_saving'), 'error')
        } finally {
            setIsSaving(false)
        }
    }

    return (
        <Card className={cn("border-slate-800 bg-slate-900/50", className)}>
            <CardHeader>
                <CardTitle className="text-lg text-slate-200 flex items-center gap-2">
                    <User className="w-5 h-5 text-sky-500" /> {t('user_profile')}
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="flex flex-col items-center gap-4">
                    <div className="relative w-24 h-24 rounded-full overflow-hidden border-2 border-slate-700 bg-slate-800 group">
                        {avatar ? (
                            <img src={avatar} alt="Avatar" className="w-full h-full object-cover" />
                        ) : (
                            <div className="w-full h-full flex items-center justify-center text-slate-500">
                                <User className="w-10 h-10" />
                            </div>
                        )}
                        <label className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                            <Camera className="w-8 h-8 text-white/80" />
                            <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
                        </label>
                    </div>
                    <span className="text-xs text-slate-500">{t('change_photo')}</span>
                </div>

                <div className="space-y-2">
                    <label className="text-xs font-medium text-slate-400 uppercase">{t('name')}</label>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder={t('your_name')}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-sky-500"
                    />
                </div>

                {/* Customize Home Toggle */}
                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/50 border border-slate-800">
                    <div className="space-y-0.5">
                        <label className="text-sm font-medium text-slate-200">{t('customize_home')}</label>
                        <p className="text-xs text-slate-500">{t('customize_home_desc')}</p>
                    </div>
                    <Switch
                        checked={customizeHome}
                        onCheckedChange={setCustomizeHome}
                    />
                </div>

                <Button onClick={handleSave} disabled={isSaving} className="w-full">
                    {isSaving ? t('saving') : t('save_profile')} <Save className="w-4 h-4 ml-2" />
                </Button>
            </CardContent>
        </Card>
    )
}

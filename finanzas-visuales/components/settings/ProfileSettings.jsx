'use client'

import { useState, useEffect } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Button, Card, CardContent, CardHeader, CardTitle, Input, useToast } from '@/components/ui/UI'
import { User, Camera, Save } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'
import { cn } from '@/lib/utils'

export function ProfileSettings({ className }) {
    const settings = useLiveQuery(() => db.settings.get('global'))
    const { addToast } = useToast()
    const { t } = useLanguage()
    const [name, setName] = useState('')
    const [avatar, setAvatar] = useState(null)
    const [isSaving, setIsSaving] = useState(false)

    useEffect(() => {
        if (settings) {
            setName(settings.username || '')
            setAvatar(settings.avatar || null)
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
                ...(settings || {}), // 1. Spread existing FIRST
                id: 'global',
                username: name, // 2. Overwrite with new values
                avatar: avatar,
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

                {/* Avatar Upload */}
                <div className="flex flex-col items-center gap-4">
                    <div className="relative w-24 h-24 rounded-full overflow-hidden border-2 border-slate-700 bg-slate-800 group">
                        {avatar ? (
                            <img src={avatar} alt="Avatar" className="w-full h-full object-cover" />
                        ) : (
                            <div className="w-full h-full flex items-center justify-center text-slate-500">
                                <User className="w-10 h-10" />
                            </div>
                        )}

                        {/* Overlay for clicking */}
                        <label className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                            <Camera className="w-8 h-8 text-white/80" />
                            <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
                        </label>
                    </div>
                    <span className="text-xs text-slate-500">{t('change_photo')}</span>
                </div>

                {/* Name Input */}
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

                <Button onClick={handleSave} disabled={isSaving} className="w-full">
                    {isSaving ? t('saving') : t('save_profile')} <Save className="w-4 h-4 ml-2" />
                </Button>

            </CardContent>
        </Card>
    )
}

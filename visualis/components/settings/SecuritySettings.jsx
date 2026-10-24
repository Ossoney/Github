'use client'

import { useState } from 'react'
import { Card, CardHeader, CardTitle, CardContent, Button, Input, Switch, useToast, ConfirmDialog } from '@/components/ui/UI'
import { ShieldCheck, Lock, KeyRound, Trash2 } from 'lucide-react'
import { usePin } from '@/lib/pin'
import { useLanguage } from '@/lib/i18n'

export function SecuritySettings() {
    const { isPinSet, setNewPin, removePin, lockApp } = usePin()
    const { t } = useLanguage()
    const { addToast } = useToast()

    const [isConfiguring, setIsConfiguring] = useState(false)
    const [isRemoving, setIsRemoving] = useState(false)
    const [pinInput, setPinInput] = useState('')
    const [pinConfirm, setPinConfirm] = useState('')
    const [currentPinInput, setCurrentPinInput] = useState('')

    const handleSaveNewPin = async (e) => {
        e.preventDefault()
        if (pinInput.length < 4 || pinInput.length > 8) {
            addToast(t('pin_length_error'), 'error')
            return
        }
        if (pinInput !== pinConfirm) {
            addToast(t('pin_mismatch_error'), 'error')
            return
        }
        const ok = await setNewPin(pinInput)
        if (ok) {
            addToast(t('pin_saved_success'), 'success')
            setIsConfiguring(false)
            setPinInput('')
            setPinConfirm('')
        } else {
            addToast(t('error_saving'), 'error')
        }
    }

    const handleRemovePin = async (e) => {
        e.preventDefault()
        const ok = await removePin(currentPinInput)
        if (ok) {
            addToast(t('pin_removed_success'), 'success')
            setIsRemoving(false)
            setCurrentPinInput('')
        } else {
            addToast(t('pin_error_wrong'), 'error')
        }
    }

    return (
        <Card className="border-slate-800 bg-slate-900/50">
            <CardHeader>
                <CardTitle className="text-slate-200 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Lock className="w-5 h-5 text-sky-500" />
                        {t('pin_security_title')}
                    </div>
                    {isPinSet && (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                            <ShieldCheck className="w-3.5 h-3.5" /> {t('pin_status_active')}
                        </span>
                    )}
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <p className="text-xs text-slate-400 leading-relaxed">
                    {t('pin_security_desc')}
                </p>

                {!isPinSet && !isConfiguring && (
                    <Button onClick={() => setIsConfiguring(true)} className="w-full sm:w-auto">
                        <KeyRound className="w-4 h-4 mr-2" />
                        {t('pin_create_button')}
                    </Button>
                )}

                {isConfiguring && (
                    <form onSubmit={handleSaveNewPin} className="space-y-3 p-4 rounded-xl bg-slate-950/70 border border-slate-800">
                        <h4 className="text-sm font-semibold text-slate-200">{t('pin_form_title')}</h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <div>
                                <label className="text-xs text-slate-400 font-medium block mb-1">{t('pin_field_new')}</label>
                                <input
                                    type="password"
                                    inputMode="numeric"
                                    pattern="[0-9]*"
                                    maxLength={8}
                                    value={pinInput}
                                    onChange={(e) => setPinInput(e.target.value.replace(/\D/g, ''))}
                                    placeholder="4 - 8 dígitos"
                                    className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 text-sm focus:outline-none focus:border-sky-500 tracking-widest text-center"
                                />
                            </div>
                            <div>
                                <label className="text-xs text-slate-400 font-medium block mb-1">{t('pin_field_confirm')}</label>
                                <input
                                    type="password"
                                    inputMode="numeric"
                                    pattern="[0-9]*"
                                    maxLength={8}
                                    value={pinConfirm}
                                    onChange={(e) => setPinConfirm(e.target.value.replace(/\D/g, ''))}
                                    placeholder="Repite el PIN"
                                    className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 text-sm focus:outline-none focus:border-sky-500 tracking-widest text-center"
                                />
                            </div>
                        </div>
                        <div className="flex gap-2 justify-end pt-2">
                            <Button type="button" variant="ghost" onClick={() => { setIsConfiguring(false); setPinInput(''); setPinConfirm('') }}>
                                {t('cancel')}
                            </Button>
                            <Button type="submit" disabled={pinInput.length < 4 || pinInput !== pinConfirm}>
                                {t('save')}
                            </Button>
                        </div>
                    </form>
                )}

                {isPinSet && !isRemoving && (
                    <div className="flex flex-wrap gap-2 pt-2">
                        <Button variant="outline" onClick={lockApp} className="border-slate-800 hover:bg-slate-850">
                            <Lock className="w-4 h-4 mr-2 text-sky-400" />
                            {t('pin_lock_now')}
                        </Button>
                        <Button variant="ghost" onClick={() => setIsRemoving(true)} className="text-rose-400 hover:text-rose-300 hover:bg-rose-500/10">
                            <Trash2 className="w-4 h-4 mr-2" />
                            {t('pin_remove_button')}
                        </Button>
                    </div>
                )}

                {isRemoving && (
                    <form onSubmit={handleRemovePin} className="space-y-3 p-4 rounded-xl bg-slate-950/70 border border-rose-950/50">
                        <h4 className="text-sm font-semibold text-rose-300">{t('pin_remove_title')}</h4>
                        <div>
                            <label className="text-xs text-slate-400 font-medium block mb-1">{t('pin_enter_current')}</label>
                            <input
                                type="password"
                                inputMode="numeric"
                                pattern="[0-9]*"
                                maxLength={8}
                                value={currentPinInput}
                                onChange={(e) => setCurrentPinInput(e.target.value.replace(/\D/g, ''))}
                                placeholder="PIN actual"
                                className="w-full max-w-xs bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 text-sm focus:outline-none focus:border-rose-500 tracking-widest"
                            />
                        </div>
                        <div className="flex gap-2 justify-start pt-2">
                            <Button type="button" variant="ghost" onClick={() => { setIsRemoving(false); setCurrentPinInput('') }}>
                                {t('cancel')}
                            </Button>
                            <Button type="submit" variant="destructive" disabled={!currentPinInput}>
                                {t('delete')}
                            </Button>
                        </div>
                    </form>
                )}
            </CardContent>
        </Card>
    )
}

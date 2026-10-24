'use client'

import { useState } from 'react'
import { usePin } from '@/lib/pin'
import { useLanguage } from '@/lib/i18n'
import { ShieldCheck, Delete, Lock } from 'lucide-react'

export function PinLockScreen() {
    const { isPinSet, isLocked, unlock, isLoading } = usePin()
    const { t } = useLanguage()
    const [pin, setPin] = useState('')
    const [error, setError] = useState(false)
    const [verifying, setVerifying] = useState(false)

    if (isLoading || !isPinSet || !isLocked) {
        return null
    }

    const handleDigit = async (digit) => {
        if (pin.length >= 6 || verifying) return
        const nextPin = pin + digit
        setPin(nextPin)
        setError(false)

        // Comprobación automática cuando alcanza longitud típica (4 a 6 dígitos)
        if (nextPin.length >= 4) {
            setVerifying(true)
            const ok = await unlock(nextPin)
            if (!ok && nextPin.length === 6) {
                setError(true)
                setTimeout(() => {
                    setPin('')
                    setError(false)
                    setVerifying(false)
                }, 600)
            } else if (!ok) {
                setVerifying(false)
            } else {
                setPin('')
                setVerifying(false)
            }
        }
    }

    const handleDelete = () => {
        setPin(prev => prev.slice(0, -1))
        setError(false)
    }

    const handleManualSubmit = async () => {
        if (pin.length < 4) return
        setVerifying(true)
        const ok = await unlock(pin)
        if (!ok) {
            setError(true)
            setTimeout(() => {
                setPin('')
                setError(false)
                setVerifying(false)
            }, 600)
        } else {
            setPin('')
            setVerifying(false)
        }
    }

    return (
        <div className="fixed inset-0 z-50 bg-slate-950 flex flex-col items-center justify-center p-4 select-none backdrop-blur-xl">
            <div className="w-full max-w-xs flex flex-col items-center space-y-6">
                
                {/* Logo / Icono */}
                <div className="w-16 h-16 rounded-2xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center shadow-lg shadow-sky-500/20">
                    <Lock className="w-8 h-8 text-sky-400" />
                </div>

                <div className="text-center space-y-1">
                    <h2 className="text-xl font-bold text-slate-100">{t('pin_locked_title')}</h2>
                    <p className="text-xs text-slate-400">{t('pin_locked_desc')}</p>
                </div>

                {/* Indicador de dígitos */}
                <div className={`flex items-center gap-3 py-2 ${error ? 'animate-shake' : ''}`}>
                    {[0, 1, 2, 3].map((idx) => (
                        <div
                            key={idx}
                            className={`w-4 h-4 rounded-full transition-all duration-200 border ${
                                pin.length > idx
                                    ? 'bg-sky-400 border-sky-400 scale-110 shadow-sm shadow-sky-400/50'
                                    : 'border-slate-700 bg-slate-900'
                            }`}
                        />
                    ))}
                    {pin.length > 4 && (
                        <span className="text-xs font-mono text-sky-400">+{pin.length - 4}</span>
                    )}
                </div>

                {error && (
                    <p className="text-xs text-rose-400 font-medium">{t('pin_error_wrong')}</p>
                )}

                {/* Teclado numérico */}
                <div className="grid grid-cols-3 gap-3 w-full pt-2">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
                        <button
                            key={num}
                            onClick={() => handleDigit(String(num))}
                            className="h-14 rounded-2xl bg-slate-900 border border-slate-800 text-xl font-semibold text-slate-200 hover:bg-slate-800 active:scale-95 transition-all shadow-sm"
                        >
                            {num}
                        </button>
                    ))}
                    <button
                        onClick={handleDelete}
                        className="h-14 rounded-2xl bg-slate-900/40 border border-slate-800/60 flex items-center justify-center text-slate-400 hover:text-slate-200 active:scale-95 transition-all"
                        aria-label="Borrar"
                    >
                        <Delete className="w-6 h-6" />
                    </button>
                    <button
                        onClick={() => handleDigit('0')}
                        className="h-14 rounded-2xl bg-slate-900 border border-slate-800 text-xl font-semibold text-slate-200 hover:bg-slate-800 active:scale-95 transition-all shadow-sm"
                    >
                        0
                    </button>
                    <button
                        onClick={handleManualSubmit}
                        disabled={pin.length < 4}
                        className="h-14 rounded-2xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 hover:bg-sky-500/20 active:scale-95 transition-all disabled:opacity-40 disabled:hover:bg-sky-500/10"
                        aria-label="Entrar"
                    >
                        <ShieldCheck className="w-6 h-6" />
                    </button>
                </div>
            </div>
        </div>
    )
}

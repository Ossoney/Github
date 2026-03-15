'use client'

import { useState, useEffect } from 'react'
import { Modal, Button } from '@/components/ui/UI'
import { Sparkles, Palette, Zap } from 'lucide-react'
import { db } from '@/lib/db'

const CURRENT_VERSION = '1.4.10'

export function WhatsNewModal() {
    const [isOpen, setIsOpen] = useState(false)

    useEffect(() => {
        const checkVersion = async () => {
            const storedVersion = localStorage.getItem('visualis_last_version')
            
            if (storedVersion !== CURRENT_VERSION) {
                // Show modal after a small delay to let the app load
                setTimeout(() => setIsOpen(true), 1000)
                localStorage.setItem('visualis_last_version', CURRENT_VERSION)
            }
        }
        checkVersion()
    }, [])

    const handleApplyTheme = async () => {
        // Automatically switch to Mondrian theme
        document.documentElement.setAttribute('data-theme', 'mondrian')
        const currentSettings = await db.settings.get('global') || { id: 'global' }
        await db.settings.put({ ...currentSettings, theme: 'mondrian' })
        setIsOpen(false)
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-4">
            <div className="absolute inset-0 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200" onClick={() => setIsOpen(false)}></div>
            
            <div className="relative w-full max-w-md bg-slate-900 border-4 border-white shadow-2xl animate-in slide-in-from-bottom-10 fade-in duration-300 rounded-none flex flex-col overflow-hidden ring-4 ring-blue-600">
                
                {/* Header Area with Mondrian inspired background */}
                <div className="relative h-40 bg-black flex items-center justify-center border-b-4 border-white">
                    {/* Mondrian shapes */}
                    <div className="absolute top-0 w-1/3 h-full bg-blue-600 border-r-4 border-white left-0" />
                    <div className="absolute bottom-0 right-0 w-1/4 h-1/2 bg-yellow-400 border-t-4 border-l-4 border-white" />
                    <div className="absolute top-0 right-1/4 w-1/6 h-1/3 bg-red-500 border-b-4 border-l-4 border-white" />
                    
                    <div className="relative z-10 px-6 py-3 bg-black border-4 border-white shadow-[8px_8px_0px_rgba(37,99,235,1)]">
                        <h2 className="text-lg sm:text-2xl font-black text-white tracking-widest uppercase flex items-center gap-2">
                            <Sparkles className="w-5 h-5 sm:w-6 sm:h-6 text-yellow-500" />
                            Visualis 1.4.10
                        </h2>
                    </div>
                </div>

                <div className="p-6 space-y-6">
                    <div className="space-y-4">
                        <div>
                            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-1">
                                <Palette className="w-5 h-5 text-sky-500" />
                                Estilo Mondrian y Más
                            </h3>
                            <p className="text-slate-400 text-sm leading-relaxed">
                                ¡El nuevo tema **Mondrian** ya está aquí! Contraste puro inspirado en el arte de De Stijl. Además, hemos rediseñado los paneles de ayuda con una estética premium.
                            </p>
                        </div>

                        <div>
                            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-1">
                                <Zap className="w-5 h-5 text-amber-500" />
                                Hábitos con Recordatorios
                            </h3>
                            <p className="text-slate-400 text-sm leading-relaxed">
                                Ahora puedes activar **recordatorios diarios** en tus hábitos con un nuevo sistema de notificaciones elegante y integrado. ¡No pierdas ni un solo día de tu racha!
                            </p>
                        </div>
                    </div>

                    <div className="flex gap-3 pt-2">
                        <Button 
                            variant="ghost" 
                            onClick={() => setIsOpen(false)} 
                            className="flex-1 border-2 border-slate-700 hover:bg-slate-800 rounded-none text-slate-300"
                        >
                            Lo veré luego
                        </Button>
                        <Button 
                            onClick={handleApplyTheme} 
                            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white rounded-none border-2 border-white shadow-[4px_4px_0px_rgba(255,255,255,1)] transition-all hover:translate-y-1 hover:shadow-none font-bold"
                        >
                            ¡Pruébalo ahora!
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    )
}

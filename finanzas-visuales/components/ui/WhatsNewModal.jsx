'use client'

import { useState, useEffect } from 'react'
import { Modal, Button } from '@/components/ui/UI'
import { Sparkles, Palette, Zap } from 'lucide-react'
import { db } from '@/lib/db'

const CURRENT_VERSION = '1.4.25'

export function WhatsNewModal() {
    const [isOpen, setIsOpen] = useState(false)

    useEffect(() => {
        const checkVersion = async () => {
            const storedVersion = localStorage.getItem('visualis_last_version')
            
            if (storedVersion !== CURRENT_VERSION) {
                // Show modal after a small delay to let the app load
                setTimeout(() => setIsOpen(true), 1200)
                localStorage.setItem('visualis_last_version', CURRENT_VERSION)
            }
        }
        checkVersion()
    }, [])

    const handleApplyTheme = async (themeName = 'mondrian') => {
        document.documentElement.setAttribute('data-theme', themeName)
        const currentSettings = await db.settings.get('global') || { id: 'global' }
        await db.settings.put({ ...currentSettings, theme: themeName })
        setIsOpen(false)
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-4">
            <div className="absolute inset-0 bg-black/90 backdrop-blur-md animate-in fade-in duration-300" onClick={() => setIsOpen(false)}></div>
            
            <div className="relative w-full max-w-lg bg-slate-900 border-4 border-white shadow-[20px_20px_0px_rgba(37,99,235,0.4)] animate-in zoom-in-95 slide-in-from-bottom-20 duration-500 rounded-none flex flex-col overflow-hidden ring-4 ring-blue-600/50">
                
                {/* Header Area with Dynamic Mondrian background */}
                <div className="relative h-48 bg-black flex items-center justify-center border-b-4 border-white overflow-hidden">
                    <div className="absolute top-0 w-1/3 h-full bg-blue-600 border-r-4 border-white left-0 transition-all hover:w-1/2 duration-700" />
                    <div className="absolute bottom-0 right-0 w-1/4 h-1/2 bg-yellow-400 border-t-4 border-l-4 border-white animate-pulse" />
                    <div className="absolute top-0 right-1/4 w-1/6 h-1/3 bg-red-600 border-b-4 border-l-4 border-white" />
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-white border-2 border-black rotate-45" />

                    <div className="relative z-10 px-8 py-4 bg-black/80 backdrop-blur-sm border-2 border-white/30 shadow-[10px_10px_0px_rgba(239,68,68,1)]">
                        <h2 className="text-xl sm:text-3xl font-black text-white tracking-[0.2em] uppercase flex flex-col items-center gap-1">
                            <span className="text-xs font-bold text-sky-400 tracking-[0.5em] -mb-1">VERSION</span>
                            <span className="flex items-center gap-3">
                                <Sparkles className="w-6 h-6 sm:w-8 sm:h-8 text-yellow-400" />
                                1.4.25
                            </span>
                        </h2>
                    </div>
                </div>

                <div className="p-8 space-y-8 max-h-[60vh] overflow-y-auto custom-scrollbar">
                    <div className="space-y-6">
                        <div className="group">
                            <h3 className="text-xl font-black text-white flex items-center gap-3 mb-2 group-hover:text-sky-400 transition-colors">
                                <Palette className="w-6 h-6 text-sky-500" />
                                <span className="uppercase tracking-widest">Apariencia Neoplástica</span>
                            </h3>
                            <p className="text-slate-400 text-sm leading-relaxed border-l-2 border-slate-800 pl-4 py-1">
                                El nuevo tema **Mondrian** transforma tu app en una obra maestra de De Stijl. Líneas negras puras y colores primarios para una gestión financiera artística.
                            </p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-4 bg-slate-800/50 border-2 border-slate-700 hover:border-amber-500/50 transition-colors">
                                <h4 className="font-bold text-amber-500 text-xs uppercase tracking-widest mb-1">🎞️ ART DÉCO</h4>
                                <p className="text-[11px] text-slate-500 leading-tight">Elegancia geométrica, simetría y contrastes dorados para un toque premium.</p>
                            </div>
                            <div className="p-4 bg-slate-800/50 border-2 border-slate-700 hover:border-fuchsia-500/50 transition-colors">
                                <h4 className="font-bold text-fuchsia-500 text-xs uppercase tracking-widest mb-1">🍿 POP ART</h4>
                                <p className="text-[11px] text-slate-500 leading-tight">Colores planos saturados y estética de cómic para un look divertido y vibrante.</p>
                            </div>
                        </div>

                        <div>
                            <h3 className="text-xl font-black text-white flex items-center gap-3 mb-2">
                                <Zap className="w-6 h-6 text-amber-500" />
                                <span className="uppercase tracking-widest">Smart Core v1.4</span>
                            </h3>
                            <p className="text-slate-400 text-sm leading-relaxed border-l-2 border-slate-800 pl-4 py-1">
                                Hemos reconstruido el motor de idiomas **(i18n)** para mayor fluidez y corregido errores de inconsistencia en el diccionario.
                            </p>
                        </div>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-4 pt-2">
                        <button 
                            onClick={() => setIsOpen(false)} 
                            className="flex-1 py-3 px-6 text-sm font-bold border-2 border-slate-700 hover:bg-slate-800 text-slate-400 transition-all active:scale-95 uppercase tracking-widest"
                        >
                            Saltar aviso
                        </button>
                        <button 
                            onClick={() => handleApplyTheme('mondrian')} 
                            className="flex-1 py-3 px-6 text-sm font-black bg-blue-600 hover:bg-blue-700 text-white shadow-[6px_6px_0px_rgba(255,255,255,1)] hover:translate-x-1 hover:translate-y-1 hover:shadow-none transition-all active:scale-90 uppercase tracking-[0.2em]"
                        >
                            ¡ESTRENAR TEMA!
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

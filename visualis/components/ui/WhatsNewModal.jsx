'use client'

import { useState, useEffect } from 'react'
import { Sparkles, Palette, Layers, Zap, X } from 'lucide-react'
import { APP_VERSION, APP_VERSION_DATE } from '@/lib/version'

export function WhatsNewModal() {
    const [isOpen, setIsOpen] = useState(false)

    useEffect(() => {
        const handleOpen = () => setIsOpen(true)
        window.addEventListener('open-whats-new-modal', handleOpen)

        const checkVersion = async () => {
            const storedVersion = localStorage.getItem('visualis_last_version')
            
            if (storedVersion !== APP_VERSION) {
                // Show modal after a small delay to let the app load
                setTimeout(() => setIsOpen(true), 1200)
                localStorage.setItem('visualis_last_version', APP_VERSION)
            }
        }
        checkVersion()

        return () => window.removeEventListener('open-whats-new-modal', handleOpen)
    }, [])

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-4">
            <div className="absolute inset-0 bg-black/90 backdrop-blur-md animate-in fade-in duration-300" onClick={() => setIsOpen(false)} />
            
            <div className="relative w-full max-w-lg bg-slate-900 border border-slate-700 shadow-2xl animate-in zoom-in-95 slide-in-from-bottom-20 duration-500 rounded-2xl flex flex-col overflow-hidden ring-1 ring-sky-500/20">
                
                {/* Header */}
                <div className="relative h-40 bg-gradient-to-br from-slate-950 via-slate-900 to-sky-950 flex items-center justify-center border-b border-slate-800 overflow-hidden">
                    {/* Close button */}
                    <button 
                        onClick={() => setIsOpen(false)}
                        className="absolute top-3 right-3 p-1.5 rounded-full bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors z-20"
                        aria-label="Cerrar"
                    >
                        <X className="w-5 h-5" />
                    </button>

                    {/* Background glow */}
                    <div className="absolute inset-0 opacity-30">
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-32 bg-sky-500 rounded-full blur-3xl" />
                    </div>
                    <div className="relative z-10 text-center px-6">
                        <div className="flex items-center justify-center gap-2 mb-1">
                            <span className="text-[10px] font-black text-sky-400 tracking-[0.5em] uppercase">Novedades en</span>
                        </div>
                        <h2 className="text-4xl font-black text-white tracking-wider flex items-center justify-center gap-3">
                            <Sparkles className="w-7 h-7 text-yellow-400" />
                            v{APP_VERSION}
                        </h2>
                        <p className="text-xs text-slate-500 mt-1 uppercase tracking-widest">{APP_VERSION_DATE}</p>
                    </div>
                </div>

                <div className="p-6 space-y-4 max-h-[62vh] overflow-y-auto">

                    {/* Feature 1: Art Themes */}
                    <div className="flex gap-4 p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:border-sky-500/30 transition-colors">
                        <div className="w-10 h-10 rounded-xl bg-sky-500/10 border border-sky-500/20 flex items-center justify-center shrink-0">
                            <Palette className="w-5 h-5 text-sky-400" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-100 text-sm">Nuevos Temas Artísticos</h3>
                            <p className="text-[12px] text-slate-400 mt-1 leading-relaxed">
                                Estreno de <span className="text-cyan-400 font-semibold">Cyberpunk Neón</span> (negro abisal y cian láser con resplandor) y <span className="text-amber-400 font-semibold">Ukiyo-e Gran Ola</span> (papel washi, azul índigo de Hokusai y bermellón Torii), junto a la restauración de <span className="text-yellow-400 font-semibold">Eclipse Dorado</span>.
                            </p>
                        </div>
                    </div>

                    {/* Feature 2: Recurring Subcategories */}
                    <div className="flex gap-4 p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:border-emerald-500/30 transition-colors">
                        <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shrink-0">
                            <Layers className="w-5 h-5 text-emerald-400" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-100 text-sm">Subcategorías en Recurrentes</h3>
                            <p className="text-[12px] text-slate-400 mt-1 leading-relaxed">
                                Ahora puedes asignar tanto la categoría padre como la <span className="text-emerald-400 font-semibold">subcategoría específica</span> (ej. <em>Suministros &gt; Luz</em>, <em>Automóvil &gt; Combustible</em>) a tus cobros y pagos fijos automáticos.
                            </p>
                        </div>
                    </div>

                    {/* Feature 3: Smart Icons */}
                    <div className="flex gap-4 p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:border-amber-500/30 transition-colors">
                        <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center shrink-0">
                            <Zap className="w-5 h-5 text-amber-400" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-100 text-sm">Iconos Inteligentes y Reserva</h3>
                            <p className="text-[12px] text-slate-400 mt-1 leading-relaxed">
                                Detección semántica automática para nuevas categorías (<span className="text-amber-400 font-semibold">Electricidad, Automóvil, Deporte, Viajes, Alquiler...</span>) y catálogo ampliado de iconos de reserva.
                            </p>
                        </div>
                    </div>

                    {/* Feature 4: Performance */}
                    <div className="flex gap-4 p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:border-violet-500/30 transition-colors">
                        <div className="w-10 h-10 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center shrink-0">
                            <Sparkles className="w-5 h-5 text-violet-400" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-100 text-sm">Rendimiento y Arranque Rápido</h3>
                            <p className="text-[12px] text-slate-400 mt-1 leading-relaxed">
                                Optimización de empaquetado en Next.js para <span className="text-violet-400 font-semibold">aligerar el código en el cliente</span> y acelerar la navegación y apertura inicial de la aplicación.
                            </p>
                        </div>
                    </div>

                    <button 
                        onClick={() => setIsOpen(false)} 
                        className="w-full py-3 px-6 text-sm font-bold bg-sky-500 hover:bg-sky-600 text-white rounded-xl transition-all active:scale-95 uppercase tracking-widest shadow-lg shadow-sky-500/20"
                    >
                        ¡Entendido!
                    </button>
                </div>
            </div>
        </div>
    )
}

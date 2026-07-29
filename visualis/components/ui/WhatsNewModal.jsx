'use client'

import { useState, useEffect } from 'react'
import { Modal, Button } from '@/components/ui/UI'
import { Sparkles, BarChart3, Filter, Calendar } from 'lucide-react'

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

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-4">
            <div className="absolute inset-0 bg-black/90 backdrop-blur-md animate-in fade-in duration-300" onClick={() => setIsOpen(false)} />
            
            <div className="relative w-full max-w-lg bg-slate-900 border border-slate-700 shadow-2xl animate-in zoom-in-95 slide-in-from-bottom-20 duration-500 rounded-2xl flex flex-col overflow-hidden ring-1 ring-sky-500/20">
                
                {/* Header */}
                <div className="relative h-40 bg-gradient-to-br from-slate-950 via-slate-900 to-sky-950 flex items-center justify-center border-b border-slate-800 overflow-hidden">
                    {/* Background glow */}
                    <div className="absolute inset-0 opacity-30">
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-32 bg-sky-500 rounded-full blur-3xl" />
                    </div>
                    <div className="relative z-10 text-center px-6">
                        <div className="flex items-center justify-center gap-2 mb-1">
                            <span className="text-[10px] font-black text-sky-400 tracking-[0.5em] uppercase">Novedades en</span>
                        </div>
                        <h2 className="text-4xl font-black text-white tracking-wider flex items-center gap-3">
                            <Sparkles className="w-7 h-7 text-yellow-400" />
                            v1.4.25
                        </h2>
                        <p className="text-xs text-slate-500 mt-1 uppercase tracking-widest">Agosto 2026</p>
                    </div>
                </div>

                <div className="p-6 space-y-5 max-h-[60vh] overflow-y-auto">

                    {/* Feature 1: Habit Stats */}
                    <div className="flex gap-4 p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:border-orange-500/30 transition-colors">
                        <div className="w-10 h-10 rounded-xl bg-orange-500/10 border border-orange-500/20 flex items-center justify-center shrink-0">
                            <BarChart3 className="w-5 h-5 text-orange-400" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-100 text-sm">Estadísticas de hábitos mejoradas</h3>
                            <p className="text-[12px] text-slate-400 mt-1 leading-relaxed">
                                La racha ahora distingue entre hábitos diarios (días) y semanales (semanas). 
                                El gráfico de evolución muestra una <span className="text-rose-400 font-semibold">línea de objetivo</span> para saber de un vistazo si cumpliste la meta cada semana.
                            </p>
                        </div>
                    </div>

                    {/* Feature 2: Calendar history */}
                    <div className="flex gap-4 p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:border-sky-500/30 transition-colors">
                        <div className="w-10 h-10 rounded-xl bg-sky-500/10 border border-sky-500/20 flex items-center justify-center shrink-0">
                            <Calendar className="w-5 h-5 text-sky-400" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-100 text-sm">Historial mensual de hábitos</h3>
                            <p className="text-[12px] text-slate-400 mt-1 leading-relaxed">
                                El calendario de consistencia ahora tiene <span className="text-sky-400 font-semibold">navegación mes a mes</span>. Consulta cualquier mes pasado para ver tu progreso histórico.
                            </p>
                        </div>
                    </div>

                    {/* Feature 3: Amount filter */}
                    <div className="flex gap-4 p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:border-emerald-500/30 transition-colors">
                        <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shrink-0">
                            <Filter className="w-5 h-5 text-emerald-400" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-100 text-sm">Filtro por importe en búsqueda avanzada</h3>
                            <p className="text-[12px] text-slate-400 mt-1 leading-relaxed">
                                Ahora puedes filtrar transacciones por <span className="text-emerald-400 font-semibold">rango de importe</span> (mínimo y máximo) directamente desde el panel de filtros avanzados.
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

'use client'

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/UI'
import { HelpCircle, BarChart3, Wallet, CalendarRange, Palette, Shield, Coffee, Heart, Zap, Sparkles, Smile, Fingerprint, Layers, Paintbrush } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function VersionHelp() {
    const { t } = useLanguage()

    const modernFeatures = [
        {
            id: 'finance',
            title: t('help_financial_title'),
            icon: <Zap className="w-6 h-6 text-sky-500" />,
            glow: 'group-hover:shadow-[0_0_20px_rgba(14,165,233,0.3)]',
            bg: 'bg-sky-500/10',
            borderColor: 'border-sky-500/20',
            items: [
                { name: 'Dashboard Global', desc: t('help_dashboard_desc') },
                { name: 'Smart Context', desc: t('help_context_desc') },
                { name: 'Gasto Emocional', desc: t('help_emotional_desc') },
                { name: 'Multidivisión', desc: t('help_split_desc') }
            ]
        },
        {
            id: 'structure',
            title: t('help_structure_title'),
            icon: <Layers className="w-6 h-6 text-emerald-500" />,
            glow: 'group-hover:shadow-[0_0_20px_rgba(16,185,129,0.3)]',
            bg: 'bg-emerald-500/10',
            borderColor: 'border-emerald-500/20',
            items: [
                { name: 'Multicuentas', desc: t('help_accounts_desc') },
                { name: 'Categorización jerárquica', desc: t('help_categories_desc') },
                { name: 'Etiquetas transversales (#)', desc: t('help_tags_desc') }
            ]
        },
        {
            id: 'planning',
            title: t('help_planning_title'),
            icon: <CalendarRange className="w-6 h-6 text-amber-500" />,
            glow: 'group-hover:shadow-[0_0_20px_rgba(245,158,11,0.3)]',
            bg: 'bg-amber-500/10',
            borderColor: 'border-amber-500/20',
            items: [
                { name: 'Límites de Presupuesto', desc: t('help_budgets_desc') },
                { name: 'Cobros y Pagos Fijos', desc: t('help_recurring_desc') }
            ]
        },
        {
            id: 'customization',
            title: t('help_customization_title'),
            icon: <Paintbrush className="w-6 h-6 text-purple-500" />,
            glow: 'group-hover:shadow-[0_0_20px_rgba(168,85,247,0.3)]',
            bg: 'bg-purple-500/10',
            borderColor: 'border-purple-500/20',
            items: [
                { name: 'Temas OLED/Claros Premium', desc: t('help_themes_desc') },
                { name: 'Identidad Visual', desc: t('help_profile_desc') },
                { name: 'Soporte Multilingüe', desc: t('help_languages_desc') }
            ]
        },
        {
            id: 'privacy',
            title: t('help_data_title'),
            icon: <Fingerprint className="w-6 h-6 text-rose-500" />,
            glow: 'group-hover:shadow-[0_0_20px_rgba(244,63,94,0.3)]',
            bg: 'bg-rose-500/10',
            borderColor: 'border-rose-500/20',
            items: [
                { name: 'Arquitectura Privada', desc: t('help_privacy_desc') },
                { name: 'Exportación Absoluta', desc: t('help_backups_desc') },
                { name: 'Vía de Escape Total', desc: t('help_safe_zone_desc') }
            ]
        }
    ]

    return (
        <Card className="border-slate-800 bg-slate-900/50 backdrop-blur-xl">
            <CardHeader className="pb-4 border-b border-slate-800/50">
                <CardTitle className="text-xl font-bold text-slate-100 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-indigo-500/20 rounded-xl">
                            <Sparkles className="w-6 h-6 text-indigo-400" />
                        </div>
                        <span className="bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                            Conoce Visualis
                        </span>
                    </div>
                </CardTitle>
                <p className="text-sm text-slate-400 mt-2">
                    Tu motor financiero privado, local y altamente personalizable.
                </p>
            </CardHeader>
            <CardContent className="space-y-6 pt-6">

                {/* Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {modernFeatures.map((feat) => (
                        <div key={feat.id} className={`group flex flex-col p-5 rounded-2xl border ${feat.borderColor} ${feat.bg} transition-all duration-300 ${feat.glow} cursor-default`}>
                            <div className="flex items-center gap-3 mb-4">
                                <div className="p-2 bg-slate-900/50 rounded-lg shadow-inner">
                                    {feat.icon}
                                </div>
                                <h3 className="font-bold text-slate-100 group-hover:text-white transition-colors">{feat.title}</h3>
                            </div>
                            <ul className="space-y-2 flex-1">
                                {feat.items.map((item, idx) => (
                                    <li key={idx} className="text-sm">
                                        <div className="font-semibold text-slate-300">{item.name}</div>
                                        <div className="text-xs text-slate-400/80 leading-relaxed mt-0.5">{item.desc}</div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>

                {/* Contact & Support Section */}
                <div className="flex flex-col md:flex-row gap-4 pt-4 border-t border-slate-800">
                    <div className="flex-1 p-5 rounded-xl border border-slate-800 bg-slate-900/30 flex flex-col justify-between">
                        <div>
                            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2 mb-2">
                                <Heart className="w-4 h-4 text-pink-500" />
                                {t('suggestions_title')}
                            </h3>
                            <p className="text-xs text-slate-400 mb-3 leading-relaxed">
                                {t('suggestions_desc')}
                            </p>
                        </div>
                        <code className="px-3 py-2 bg-slate-950 text-pink-400 rounded-lg text-sm font-medium border border-slate-800/80 select-all block text-center shadow-inner">
                            visualis@visualis.app
                        </code>
                    </div>

                    <div className="flex-1 p-5 rounded-xl border border-slate-800 bg-slate-900/30 flex flex-col justify-between">
                        <div>
                            <h3 className="text-sm font-semibold text-amber-400 flex items-center gap-2 mb-2">
                                <Coffee className="w-4 h-4" />
                                Apoya el Proyecto
                            </h3>
                            <p className="text-xs text-slate-400 mb-3 leading-relaxed">
                                Finanzas Visuales se sustenta por el cariño de sus usuarios. Si te aporta valor en tu día a día, invítame a un café.
                            </p>
                        </div>
                        <a
                            href="https://paypal.me/ossoney"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex w-full justify-center items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-[#003087] to-[#0070BA] hover:from-[#002060] hover:to-[#00509a] text-white rounded-lg transition-all font-medium text-sm shadow-md"
                        >
                            <Heart className="w-4 h-4 fill-current" />
                            {t('donate_button')}
                        </a>
                    </div>
                </div>

                {/* Version Footer */}
                <div className="pt-6 mt-6 border-t border-slate-800 text-center flex flex-col items-center justify-center">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700/50">
                        <span className="flex h-2 w-2 relative">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                        </span>
                        <p className="text-xs text-slate-300 font-mono tracking-wider font-semibold">VISUALIS v1.3.05</p>
                    </div>
                    <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-2">{t('version_date') || 'Marzo 2026'}</p>
                </div>
            </CardContent>
        </Card>
    )
}

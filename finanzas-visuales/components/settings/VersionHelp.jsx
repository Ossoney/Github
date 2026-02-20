'use client'

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/UI'
import { HelpCircle, BarChart3, Wallet, CalendarRange, Tag, Palette, Shield, Coffee, Heart } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function VersionHelp() {
    const { t } = useLanguage()

    return (
        <Card className="border-slate-800 bg-slate-900/50">
            <CardHeader className="pb-4 border-b border-slate-800/50">
                <CardTitle className="text-slate-200 flex items-center gap-2">
                    <HelpCircle className="w-5 h-5 text-indigo-500" />
                    {t('version_help')}
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-8 pt-6">

                {/* 1. Gestión Financiera */}
                <section className="space-y-3">
                    <h3 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
                        <BarChart3 className="w-5 h-5 text-sky-500" />
                        {t('help_financial_title')}
                    </h3>
                    <ul className="space-y-2 text-sm text-slate-400 pl-7 list-disc">
                        <li><strong className="text-slate-300">Dashboard:</strong> {t('help_dashboard_desc')}</li>
                        <li><strong className="text-slate-300">{t('transaction_history')}:</strong> {t('help_transactions_desc')}</li>
                        <li><strong className="text-slate-300">{t('help_split_title')}:</strong> {t('help_split_desc')}</li>
                        <li><strong className="text-slate-300">{t('help_context_title')}:</strong> {t('help_context_desc')}</li>
                        <li><strong className="text-slate-300">{t('help_emotional_title')}:</strong> {t('help_emotional_desc')}</li>
                    </ul>
                </section>

                {/* 2. Estructura */}
                <section className="space-y-3">
                    <h3 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
                        <Wallet className="w-5 h-5 text-emerald-500" />
                        {t('help_structure_title')}
                    </h3>
                    <ul className="space-y-2 text-sm text-slate-400 pl-7 list-disc">
                        <li><strong className="text-slate-300">{t('accounts')}:</strong> {t('help_accounts_desc')}</li>
                        <li><strong className="text-slate-300">{t('categories')}:</strong> {t('help_categories_desc')}</li>
                        <li><strong className="text-slate-300">{t('tags')}:</strong> {t('help_tags_desc')}</li>
                    </ul>
                </section>

                {/* 3. Planificación */}
                <section className="space-y-3">
                    <h3 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
                        <CalendarRange className="w-5 h-5 text-amber-500" />
                        {t('help_planning_title')}
                    </h3>
                    <ul className="space-y-2 text-sm text-slate-400 pl-7 list-disc">
                        <li><strong className="text-slate-300">{t('budgets')}:</strong> {t('help_budgets_desc')}</li>
                        <li><strong className="text-slate-300">{t('recurring')}:</strong> {t('help_recurring_desc')}</li>
                    </ul>
                </section>

                {/* 4. Personalización */}
                <section className="space-y-3">
                    <h3 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
                        <Palette className="w-5 h-5 text-purple-500" />
                        {t('help_customization_title')}
                    </h3>
                    <ul className="space-y-2 text-sm text-slate-400 pl-7 list-disc">
                        <li><strong className="text-slate-300">{t('theme')}:</strong> {t('help_themes_desc')}</li>
                        <li><strong className="text-slate-300">{t('profile')}:</strong> {t('help_profile_desc')}</li>
                        <li><strong className="text-slate-300">{t('language')}:</strong> {t('help_languages_desc')}</li>
                    </ul>
                </section>

                {/* 5. Datos y Privacidad */}
                <section className="space-y-3">
                    <h3 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
                        <Shield className="w-5 h-5 text-rose-500" />
                        {t('help_data_title')}
                    </h3>
                    <ul className="space-y-2 text-sm text-slate-400 pl-7 list-disc">
                        <li><strong className="text-slate-300">{t('security_title')}:</strong> {t('help_privacy_desc')}</li>
                        <li><strong className="text-slate-300">{t('backups')}:</strong> {t('help_backups_desc')}</li>
                        <li><strong className="text-slate-300">Excel:</strong> {t('help_excel_desc')}</li>
                        <li><strong className="text-slate-300">{t('danger_zone')}:</strong> {t('help_safe_zone_desc')}</li>
                    </ul>
                </section>

                {/* 6. Suggestions & Bugs */}
                <section className="space-y-3 pt-4 border-t border-slate-800">
                    <h3 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
                        <Heart className="w-5 h-5 text-pink-500" />
                        {t('suggestions_title')}
                    </h3>
                    <p className="text-sm text-slate-400">
                        {t('suggestions_desc')}
                    </p>
                    <div className="pt-2">
                        <code className="px-3 py-1.5 bg-slate-800 text-pink-400 rounded-lg text-sm font-medium border border-slate-700 select-all">
                            visualis@visualis.app
                        </code>
                    </div>
                </section>

                {/* 7. Donaciones */}
                <section className="space-y-3 pt-4 border-t border-slate-800">
                    <h3 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                        <Coffee className="w-5 h-5" />
                        {t('donation_title')}
                    </h3>
                    <p className="text-sm text-slate-400">
                        {t('donation_desc')}
                    </p>
                    <a
                        href="https://paypal.me/ossoney"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-2 px-4 py-2 bg-[#0070BA] hover:bg-[#003087] text-white rounded-xl transition-colors font-medium text-sm"
                    >
                        <Heart className="w-4 h-4 fill-current" />
                        {t('donate_button')}
                    </a>
                </section>

                <div className="pt-6 border-t border-slate-800 text-center">
                    <p className="text-xs text-slate-500 font-mono">VISUALIS v1.1.33 • {t('version_date')}</p>
                </div>
            </CardContent>
        </Card>
    )
}

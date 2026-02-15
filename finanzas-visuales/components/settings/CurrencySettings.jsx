'use client'

import { useLanguage, CURRENCIES } from '@/lib/i18n'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/UI'
import { Banknote, Check } from 'lucide-react'
import { cn } from '@/lib/utils'

export function CurrencySettings() {
    const { currency, setCurrency, t } = useLanguage()

    // CURRENCIES imported from i18n

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

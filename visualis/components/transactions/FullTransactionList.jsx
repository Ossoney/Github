'use client'

import { useLanguage } from '@/lib/i18n'
import { useStore } from '@/hooks/useStore'
import { DynamicIcon } from '@/components/ui/UI'
import { format } from 'date-fns'
import { es, enUS, gl, eu } from 'date-fns/locale'

export function FullTransactionList({ transactions }) {
    const { openTransactionModal } = useStore()
    const { t, tCategory, formatMoney, locale } = useLanguage()

    if (!transactions?.length) {
        return (
            <div className="text-center py-20 text-slate-500 bg-slate-900/20 rounded-2xl border-2 border-dashed border-slate-800">
                <p className="text-lg font-medium">{t('no_transactions_found') || 'No transactions found matching your criteria.'}</p>
                <p className="text-sm mt-2">{t('try_adjusting_filters') || 'Try adjusting your filters.'}</p>
            </div>
        )
    }

    // Group by Date for better readability
    const grouped = transactions.reduce((acc, tx) => {
        const dateKey = format(new Date(tx.date), 'yyyy-MM-dd')
        if (!acc[dateKey]) acc[dateKey] = []
        acc[dateKey].push(tx)
        return acc
    }, {})

    // Sort dates desc
    const sortedDates = Object.keys(grouped).sort((a, b) => new Date(b) - new Date(a))

    return (
        <div className="space-y-6">
            {sortedDates.map(dateKey => {
                const dateObj = new Date(dateKey)
                const dayName = format(dateObj, 'EEEE', { locale })
                const dayDate = format(dateObj, 'd MMMM', { locale })

                return (
                    <div key={dateKey} className="space-y-2">
                        <h3 className="text-sm font-semibold text-slate-500 px-2 capitalize flex items-center gap-2">
                            <span className="text-slate-300">{dayName}</span>
                            <span className="w-1 h-1 bg-slate-600 rounded-full" />
                            {dayDate}
                        </h3>

                        <div className="space-y-2">
                            {grouped[dateKey].map(tx => {
                                const isExpense = tx.type === 'expense'
                                return (
                                    <div
                                        key={tx.id}
                                        onClick={() => openTransactionModal(tx)}
                                        className="flex flex-col gap-2 p-4 rounded-xl bg-slate-900/30 border border-slate-800/50 hover:bg-slate-800/50 transition-colors group cursor-pointer hover:border-sky-500/30"
                                    >
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-4">
                                                {tx.type === 'transfer' ? (
                                                    <div className="w-10 h-10 min-w-[2.5rem] rounded-full flex items-center justify-center bg-sky-500/20 text-sky-400">
                                                        <DynamicIcon name="ArrowRightLeft" className="w-5 h-5" />
                                                    </div>
                                                ) : (
                                                    <div
                                                        className="w-10 h-10 min-w-[2.5rem] rounded-full flex items-center justify-center transition-colors"
                                                        style={{
                                                            backgroundColor: `${tx.category?.color}20`,
                                                            color: tx.category?.color
                                                        }}
                                                    >
                                                        <DynamicIcon name={tx.category?.icon} className="w-5 h-5" />
                                                    </div>
                                                )}
                                                <div className="min-w-0">
                                                    <div className="font-medium text-slate-200 truncate pr-2">
                                                        {tx.type === 'transfer' ? t('transfer') : (tx.description || tCategory(tx.category?.name) || t('uncategorized'))}
                                                    </div>
                                                    <div className="flex items-center gap-2 text-xs text-slate-500 flex-wrap">
                                                        {tx.type === 'transfer' ? (
                                                            <div className="flex items-center gap-1">
                                                                <span className="text-sky-400 font-medium">{tx.wallet?.name}</span>
                                                                <DynamicIcon name="ArrowRight" className="w-3 h-3 text-slate-600" />
                                                                <span className="text-sky-400 font-medium">{tx.toWallet?.name}</span>
                                                            </div>
                                                        ) : (
                                                            <>
                                                                {tx.category?.name && tx.description && (
                                                                    <span className="text-slate-400 bg-slate-800/50 px-1.5 rounded">{tCategory(tx.category?.name)}</span>
                                                                )}
                                                                {tx.wallet && (
                                                                    <span className="text-sky-400 font-medium">{tx.wallet.name}</span>
                                                                )}
                                                            </>
                                                        )}
                                                        {/* Tags */}
                                                        {tx.tags && tx.tags.length > 0 && (
                                                            <div className="flex gap-1">
                                                                {tx.tags.map(tag => (
                                                                    <span key={tag} className="text-[10px] text-slate-500">#{tag}</span>
                                                                ))}
                                                            </div>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                            <div className={`font-semibold whitespace-nowrap pl-2 ${tx.type === 'expense' ? 'text-slate-200' : (tx.type === 'transfer' ? 'text-sky-400' : 'text-emerald-400')}`}>
                                                {tx.type === 'expense' ? '- ' : (tx.type === 'transfer' ? '' : '+ ')}
                                                {formatMoney(tx.amount)}
                                            </div>
                                        </div>
                                    </div>
                                )
                            })}
                        </div>
                    </div>
                )
            })}
        </div>
    )
}

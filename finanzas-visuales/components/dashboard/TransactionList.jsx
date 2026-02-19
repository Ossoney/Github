import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { DynamicIcon } from '@/components/ui/UI'
import { useLanguage } from '@/lib/i18n'
import { Money } from '@/components/ui/Money' // Import Money

import { useStore } from '@/hooks/useStore'
import { startOfMonth, endOfMonth, isToday, isYesterday, format, formatDistanceToNow, differenceInCalendarDays } from 'date-fns'

export function TransactionList() {
    const { openTransactionModal, currentDate } = useStore()
    const { t, tCategory, locale, language } = useLanguage()

    const transactions = useLiveQuery(async () => {
        // ... (existing query logic)
        const start = startOfMonth(currentDate)
        const end = endOfMonth(currentDate)

        const txs = await db.transactions
            .where('date')
            .between(start, end, true, true)
            .reverse()
            .toArray()

        // Manual join since Dexie doesn't do SQL joins
        const categories = await db.categories.toArray();
        const wallets = await db.wallets.toArray();
        const catMap = new Map(categories.map(c => [c.id, c]));
        const walletMap = new Map(wallets.map(w => [w.id, w]));

        return txs.map(tx => ({
            ...tx,
            category: catMap.get(tx.categoryId),
            wallet: walletMap.get(tx.walletId)
        }));
    }, [currentDate])

    if (!transactions?.length) {
        return (
            <div className="text-center py-12 text-slate-500">
                <p>{t('no_recent_transactions')}</p>
            </div>
        )
    }

    return (
        <div className="space-y-3">
            {transactions.map((tx) => {
                const isExpense = tx.type === 'expense'

                return (
                    <div
                        key={tx.id}
                        onClick={() => openTransactionModal(tx)}
                        className="flex flex-col gap-2 p-4 rounded-xl bg-slate-900/30 border border-slate-800/50 hover:bg-slate-800/50 transition-colors group cursor-pointer hover:border-sky-500/30"
                    >
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <div
                                    className="w-10 h-10 rounded-full flex items-center justify-center transition-colors"
                                    style={{
                                        backgroundColor: `${tx.category?.color}20`,
                                        color: tx.category?.color
                                    }}
                                >
                                    <DynamicIcon name={tx.category?.icon} className="w-5 h-5" />
                                </div>
                                <div>
                                    <div className="font-medium text-slate-200">
                                        {tCategory(tx.category?.name) || t('uncategorized')}
                                    </div>
                                    <div className="flex items-center gap-2 text-xs text-slate-500">
                                        <span>
                                            {(() => {
                                                const date = new Date(tx.date)
                                                const diff = differenceInCalendarDays(new Date(), date)

                                                if (diff === 0) {
                                                    return formatDistanceToNow(date, { addSuffix: true, locale })
                                                } else if (diff === 1) {
                                                    return language === 'es' ? 'ayer' : 'yesterday'
                                                } else if (diff <= 7) {
                                                    return format(date, 'EEEE', { locale })
                                                } else {
                                                    return format(date, language === 'en' ? 'MMMM do' : "d 'de' MMMM", { locale })
                                                }
                                            })()}
                                        </span>
                                        {tx.wallet && (
                                            <>
                                                <span>•</span>
                                                <span className="text-sky-400 font-medium">{tx.wallet.name}</span>
                                            </>
                                        )}
                                    </div>
                                </div>
                            </div>
                            <div className={`font-semibold ${isExpense ? 'text-slate-200' : 'text-emerald-400'} flex items-center gap-2`}>
                                {tx.emotion && <span className="text-sm grayscale opacity-70">{tx.emotion}</span>}
                                {isExpense ? '- ' : '+ '}
                                <Money amount={tx.amount} />
                            </div>
                        </div>

                        {/* Optional Details: Description & Tags */}
                        {(tx.description || (tx.tags && tx.tags.length > 0)) && (
                            <div className="pl-14 space-y-1">
                                {tx.description && (
                                    <p className="text-xs text-slate-400 italic">"{tx.description}"</p>
                                )}
                                {tx.tags && tx.tags.length > 0 && (
                                    <div className="flex flex-wrap gap-1">
                                        {tx.tags.map(tag => (
                                            <span key={tag} className="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-800 text-slate-500 border border-slate-700/50">
                                                {tag}
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )
            })}
        </div>
    )
}

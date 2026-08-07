import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { useStore } from '@/hooks/useStore'
import { startOfMonth, endOfMonth } from 'date-fns'
import { cn } from '@/lib/utils'
import { Wallet, CreditCard, PiggyBank, TrendingUp, TrendingDown } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'
import { Money } from '@/components/ui/Money' // Import Money

const ICONS = {
    cash: Wallet,
    bank: CreditCard,
    savings: PiggyBank
}

export function WalletSummary() {
    const { currentDate, selectedWalletId, setSelectedWalletId } = useStore()
    const { t } = useLanguage()

    const data = useLiveQuery(async () => {
        const start = startOfMonth(currentDate)
        const end = endOfMonth(currentDate)

        const allWallets = await db.wallets.toArray()
        const wallets = allWallets
            .filter(w => !w.hidden)
            .sort((a, b) => (a.order ?? a.id) - (b.order ?? b.id))
        const monthTransactions = await db.transactions
            .where('date')
            .between(start, end, true, true)
            .toArray()

        return wallets.map(wallet => {
            const walletTx = monthTransactions.filter(tx => tx.walletId === wallet.id)
            const monthIncome = walletTx.filter(tx => tx.type === 'income').reduce((acc, tx) => acc + tx.amount, 0)
            const monthExpense = walletTx.filter(tx => tx.type === 'expense').reduce((acc, tx) => acc + tx.amount, 0)
            const monthBalance = monthIncome - monthExpense

            return {
                ...wallet,
                monthBalance,
                monthIncome,
                monthExpense
            }
        })
    }, [currentDate])

    if (!data || data.length === 0) return null

    const grandTotalBalance = data.reduce((acc, w) => acc + w.balance, 0)
    const grandTotalMonthBalance = data.reduce((acc, w) => acc + w.monthBalance, 0)
    const isPositiveGrandTotal = grandTotalMonthBalance >= 0

    return (
        <div className="flex gap-3 overflow-x-auto pb-2 custom-scrollbar">
            {/* TOTAL CARD (First Item) */}
            <div
                onClick={() => setSelectedWalletId(null)}
                className={cn(
                    'min-w-[200px] bg-gradient-to-br from-indigo-900/20 to-slate-900/50 border rounded-lg p-3 shrink-0 cursor-pointer transition-all',
                    selectedWalletId === null
                        ? 'border-indigo-400 ring-2 ring-indigo-500/40'
                        : 'border-indigo-500/30 hover:border-indigo-400/60'
                )}
            >
                <div className="flex items-center gap-2 mb-2">
                    <div className="p-1.5 bg-indigo-500/20 rounded-md text-indigo-400">
                        <TrendingUp className="w-4 h-4" />
                    </div>
                    <div>
                        <h3 className="font-bold text-indigo-100 text-xs">{t('global_total')}</h3>
                    </div>
                </div>

                <div className="space-y-2">
                    <div>
                        <p className="text-[10px] text-indigo-300/70 uppercase font-bold tracking-wider">{t('net_worth')}</p>
                        <p className="text-sm font-bold text-white tracking-tight">
                            <Money amount={grandTotalBalance} />
                        </p>
                    </div>
                    <div>
                        <p className="text-[10px] text-indigo-300/70 uppercase font-bold tracking-wider">{t('monthly_variation')}</p>
                        <div className={cn("flex items-center gap-1", isPositiveGrandTotal ? "text-emerald-400" : "text-rose-400")}>
                            {isPositiveGrandTotal ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                            <p className="text-sm font-bold tracking-tight">
                                <Money amount={grandTotalMonthBalance} />
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Individual Wallets */}
            {data.map(wallet => {
                const Icon = ICONS[wallet.type] || Wallet
                const isPositiveMonth = wallet.monthBalance >= 0

                return (
                    <div
                        key={wallet.id}
                        onClick={() => setSelectedWalletId(wallet.id)}
                        className={cn(
                            'min-w-[200px] bg-slate-900/30 border rounded-lg p-3 transition-all cursor-pointer shrink-0',
                            selectedWalletId === wallet.id
                                ? 'border-sky-400 ring-2 ring-sky-500/30'
                                : 'border-slate-800 hover:border-slate-600'
                        )}
                    >
                        {/* Header */}
                        <div className="flex items-center gap-2 mb-2">
                            <div className="p-1.5 bg-slate-800 rounded-md text-slate-400">
                                <Icon className="w-4 h-4" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-slate-200 text-xs truncate max-w-[120px]">{wallet.name}</h3>
                            </div>
                        </div>

                        {/* Stats Row */}
                        <div className="space-y-2">
                            {/* Total Balance */}
                            <div>
                                <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">{t('total')}</p>
                                <p className="text-sm font-bold text-white tracking-tight">
                                    <Money amount={wallet.balance} />
                                </p>
                            </div>

                            {/* Month Activity */}
                            <div>
                                <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">{t('this_month')}</p>
                                <div className={cn("flex items-center gap-1", isPositiveMonth ? "text-emerald-400" : "text-rose-400")}>
                                    {isPositiveMonth ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                                    <p className="text-sm font-bold tracking-tight">
                                        <Money amount={wallet.monthBalance} />
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })}


        </div>
    )
}

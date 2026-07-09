import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Card, CardContent } from '@/components/ui/UI'
import { Wallet, CreditCard, PiggyBank } from 'lucide-react'
import { Money } from '@/components/ui/Money' // Import Money

const ICONS = {
    cash: Wallet,
    bank: CreditCard,
    savings: PiggyBank
}

export function WalletList() {
    const wallets = useLiveQuery(async () => {
        const all = await db.wallets.toArray()
        return all.sort((a, b) => (a.order ?? a.id) - (b.order ?? b.id))
    })

    if (!wallets) return null

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            {wallets.map((wallet) => {
                const Icon = ICONS[wallet.type] || Wallet

                return (
                    <Card key={wallet.id} className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700/50 hover:border-slate-600 transition-colors cursor-pointer group">
                        <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-3 bg-slate-800 rounded-xl group-hover:bg-sky-500/20 group-hover:text-sky-400 transition-colors">
                                    <Icon className="w-6 h-6" />
                                </div>
                                {!wallet.excludeFromTotal && (
                                    <span className="text-xs font-medium px-2 py-1 rounded-full bg-emerald-500/10 text-emerald-400">
                                        Activa
                                    </span>
                                )}
                            </div>

                            <div className="space-y-1">
                                <p className="text-sm text-slate-400 font-medium">{wallet.name}</p>
                                <p className="text-2xl font-bold tracking-tight">
                                    <Money amount={wallet.balance} currency={wallet.currency} />
                                </p>
                            </div>
                        </CardContent>
                    </Card>
                )
            })}

            {/* Add Wallet Button Placeholder */}
            <button className="flex items-center justify-center p-6 rounded-2xl border border-dashed border-slate-700 hover:border-slate-500 hover:bg-slate-800/50 transition-all text-slate-500 hover:text-slate-300">
                <span className="text-sm font-medium">+ Añadir Wallet</span>
            </button>
        </div>
    )
}

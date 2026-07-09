import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Card } from '@/components/ui/UI'
import { Money } from '@/components/ui/Money'
import { useLanguage } from '@/lib/i18n'
import { startOfMonth, endOfMonth } from 'date-fns'
import { useStore } from '@/hooks/useStore'

export function EmotionSummary() {
    const { currentDate } = useStore()
    const { t, symbol } = useLanguage()

    const emotionStats = useLiveQuery(async () => {
        const start = startOfMonth(currentDate)
        const end = endOfMonth(currentDate)

        const txs = await db.transactions
            .where('date')
            .between(start, end, true, true)
            .toArray()

        // Filter for expenses only that have an emotion
        const expenses = txs.filter(tx => tx.type === 'expense' && tx.emotion)

        // Group by emotion
        const stats = {}
        let totalTracked = 0

        for (const tx of expenses) {
            if (!stats[tx.emotion]) {
                stats[tx.emotion] = 0
            }
            stats[tx.emotion] += tx.amount
            totalTracked += tx.amount
        }

        // Convert to array and sort by amount (desc)
        return Object.entries(stats)
            .map(([emotion, amount]) => ({
                emotion,
                amount,
                percentage: (amount / totalTracked) * 100
            }))
            .sort((a, b) => b.amount - a.amount)

    }, [currentDate])

    if (!emotionStats || emotionStats.length === 0) return null

    return (
        <Card className="p-4 bg-slate-900/50 border-slate-800 backdrop-blur-sm space-y-3">
            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">Gasto Emocional</h3>

            <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-5">
                {emotionStats.map(stat => (
                    <div key={stat.emotion} className="flex flex-col items-center p-2 rounded-xl bg-slate-800/50 border border-slate-700/30">
                        <div className="text-2xl mb-1">{stat.emotion}</div>
                        <div className="text-xs font-bold text-slate-200">
                            <Money amount={stat.amount} />
                        </div>
                        <div className="text-[10px] text-slate-500 font-medium">
                            {stat.percentage.toFixed(0)}%
                        </div>
                    </div>
                ))}
            </div>
        </Card>
    )
}

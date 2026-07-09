import { Modal, DynamicIcon } from "@/components/ui/UI"
import { Money } from "@/components/ui/Money"
import { useLanguage } from "@/lib/i18n"
import { format } from "date-fns"

export function DayDetailsModal({ isOpen, onClose, date, actualTransactions, projectedTransactions }) {
    const { t, tCategory, locale } = useLanguage()

    if (!isOpen || !date) return null

    const hasContent = actualTransactions?.length > 0 || projectedTransactions?.length > 0
    const title = format(date, 'EEEE, d MMMM', { locale })

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title={<span className="capitalize">{title}</span>}
            className="max-w-md"
        >
            <div className="space-y-6">
                {!hasContent && (
                    <p className="text-slate-500 text-center py-4 text-sm">
                        {t('no_transactions_found') || "No hay movimientos"}
                    </p>
                )}

                {/* Actual Transactions */}
                {actualTransactions?.length > 0 && (
                    <div className="space-y-3">
                        <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                            {t('transactions') || "Movimientos Reales"}
                        </h4>
                        <div className="space-y-2">
                            {actualTransactions.map((tx) => (
                                <TransactionItem key={tx.id} tx={tx} tCategory={tCategory} />
                            ))}
                        </div>
                    </div>
                )}

                {/* Projected Transactions */}
                {projectedTransactions?.length > 0 && (
                    <div className="space-y-3">
                        <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
                            <span>🔮 {t('projected') || "Proyecciones (Recurrentes)"}</span>
                        </h4>
                        <div className="space-y-2 opacity-80">
                            {projectedTransactions.map((tx) => (
                                <TransactionItem key={`proj-${tx.id}`} tx={tx} tCategory={tCategory} isProjected />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </Modal>
    )
}

function TransactionItem({ tx, tCategory, isProjected = false }) {
    const isExpense = tx.type === 'expense'

    return (
        <div className={`flex items-center justify-between p-3 rounded-xl border ${isProjected ? 'bg-indigo-950/10 border-indigo-500/20 border-dashed' : 'bg-slate-800/50 border-slate-700/50'}`}>
            <div className="flex items-center gap-3">
                <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center ${isProjected ? 'opacity-70' : ''}`}
                    style={{
                        backgroundColor: `${tx.category?.color}20`,
                        color: tx.category?.color
                    }}
                >
                    <DynamicIcon name={tx.category?.icon} className="w-4 h-4" />
                </div>
                <div>
                    <div className="font-medium text-sm text-slate-200">
                        {tCategory(tx.category?.name)}
                    </div>
                    {tx.description && (
                        <div className="text-xs text-slate-500 truncate max-w-[150px]">
                            {tx.description}
                        </div>
                    )}
                </div>
            </div>
            <div className={`font-semibold text-sm ${isProjected
                ? 'text-slate-400'
                : isExpense ? 'text-slate-200' : 'text-emerald-400'
                }`}>
                {isExpense ? '- ' : '+ '}
                <Money amount={tx.amount} />
            </div>
        </div>
    )
}

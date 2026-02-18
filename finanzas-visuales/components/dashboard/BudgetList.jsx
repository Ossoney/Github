import { useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Card, CardContent, CardHeader, CardTitle, Button } from '@/components/ui/UI'
import { cn } from '@/lib/utils'
import { startOfMonth, endOfMonth } from 'date-fns'
import { ChevronDown, ChevronRight, Settings } from 'lucide-react'
import * as LucideIcons from 'lucide-react'
import Link from 'next/link'
import { useStore } from '@/hooks/useStore'
import { useLanguage } from '@/lib/i18n'
import { Money } from '@/components/ui/Money' // Import Money

export function BudgetList() {
    const [expandedId, setExpandedId] = useState(null)
    const { currentDate } = useStore() // Use filtered date
    const { t } = useLanguage()

    const data = useLiveQuery(async () => {
        const start = startOfMonth(currentDate)
        const end = endOfMonth(currentDate)

        // 1. Get Budgets
        const budgets = await db.budgets.toArray()
        const globalBudget = budgets.find(b => b.type === 'global')?.amount || 0
        const budgetMap = new Map(budgets.filter(b => b.type === 'category').map(b => [b.categoryId, b.amount]))

        // 2. Get Expense Categories
        const allCategories = await db.categories
            .where('type').equals('expense')
            .toArray()

        const catMap = new Map(allCategories.map(c => [c.id, c]))

        // 3. Get Transactions
        const transactions = await db.transactions
            .where('date')
            .between(start, end, true, true) // Inclusive
            .filter(tx => tx.type === 'expense')
            .toArray()

        // 4. Aggregate by Parent
        const groups = {}
        let totalSpent = 0

        const ensureGroup = (id) => {
            if (!groups[id]) {
                const cat = catMap.get(id)
                if (!cat) return null
                groups[id] = {
                    category: cat,
                    spent: 0,
                    limit: budgetMap.get(id) || 0, // Get real limit
                    children: []
                }
            }
            return groups[id]
        }

        transactions.forEach(tx => {
            totalSpent += tx.amount
            const cat = catMap.get(tx.categoryId)
            if (!cat) return

            if (cat.parentId) {
                const parentGroup = ensureGroup(cat.parentId)
                if (parentGroup) {
                    parentGroup.spent += tx.amount
                    // Track child
                    let childStats = parentGroup.children.find(c => c.id === cat.id)
                    if (!childStats) {
                        childStats = { ...cat, spent: 0, limit: budgetMap.get(cat.id) || 0 }
                        parentGroup.children.push(childStats)
                    }
                    childStats.spent += tx.amount
                }
            } else {
                const group = ensureGroup(cat.id)
                if (group) group.spent += tx.amount
            }
        })

        // Sort by percentage filtered by limit presence, then by amount
        const sortedGroups = Object.values(groups).sort((a, b) => {
            // Prioritize those with limits
            if (a.limit > 0 && b.limit === 0) return -1
            if (b.limit > 0 && a.limit === 0) return 1
            return b.spent - a.spent
        })

        return {
            groups: sortedGroups,
            global: {
                spent: totalSpent,
                limit: globalBudget
            }
        }
    }, [currentDate])

    if (!data) return null
    const { groups, global } = data

    const toggleExpand = (id) => {
        setExpandedId(expandedId === id ? null : id)
    }

    // Helper for Progress Bar Color
    const getProgressColor = (percentage) => {
        if (percentage >= 100) return "bg-rose-500"
        if (percentage > 80) return "bg-amber-500"
        return "bg-emerald-500"
    }

    return (
        <Card className="border-slate-800 bg-slate-900/50 h-full">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-slate-200 text-lg">{t('budgets')}</CardTitle>

            </CardHeader>
            <CardContent className="space-y-6">

                {/* Global Budget Summary */}
                {global.limit > 0 && (
                    <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
                        <div className="flex justify-between items-end mb-2">
                            <div>
                                <p className="text-xs text-slate-400 uppercase font-bold tracking-wider mb-1">{t('monthly_total')}</p>
                                <p className="text-2xl font-bold text-slate-100">
                                    {Math.round((global.spent / global.limit) * 100)}%
                                </p>
                            </div>
                            <div className="text-right">
                                <p className="text-sm font-medium text-slate-300">
                                    <Money amount={global.spent} />
                                </p>
                                <p className="text-xs text-slate-500 flex items-center justify-end gap-1">
                                    {t('of')} <Money amount={global.limit} />
                                </p>
                            </div>
                        </div>
                        <div className="h-3 w-full bg-slate-900 rounded-full overflow-hidden">
                            <div
                                className={cn("h-full transition-all duration-500 rounded-full", getProgressColor((global.spent / global.limit) * 100))}
                                style={{ width: `${Math.min((global.spent / global.limit) * 100, 100)}%` }}
                            />
                        </div>
                    </div>
                )}

                {/* Categories List */}
                <div className="space-y-3">
                    {groups.map(group => {
                        const cat = group.category
                        const hasLimit = group.limit > 0
                        const percentage = hasLimit ? Math.min((group.spent / group.limit) * 100, 100) : 0
                        const isExpanded = expandedId === cat.id
                        const Icon = LucideIcons[cat.icon] || LucideIcons.HelpCircle
                        const hasChildren = group.children && group.children.length > 0

                        return (
                            <div key={cat.id} className="space-y-2">
                                <div
                                    className={cn("flex items-center justify-between p-2 rounded-xl transition-colors cursor-pointer", isExpanded ? "bg-slate-800" : "hover:bg-slate-800/50")}
                                    onClick={() => hasChildren && toggleExpand(cat.id)}
                                >
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full flex items-center justify-center bg-slate-800 border border-slate-700">
                                            <Icon className="w-5 h-5 text-slate-300" style={{ color: cat.color }} />
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-1">
                                                <span className="font-medium text-slate-200">{cat.name}</span>
                                                {hasChildren && (
                                                    isExpanded ? <ChevronDown className="w-3 h-3 text-slate-500" /> : <ChevronRight className="w-3 h-3 text-slate-500" />
                                                )}
                                            </div>
                                            <div className="text-xs text-slate-400 flex items-center gap-1">
                                                <Money amount={group.spent} />
                                                {hasLimit && <span className="text-slate-600 flex items-center gap-1"> / <Money amount={group.limit} /></span>}
                                            </div>
                                        </div>
                                    </div>

                                    {/* Percentage Badge */}
                                    {hasLimit && (
                                        <div className="text-right">
                                            <span className={cn("text-xs font-bold px-2 py-1 rounded-full",
                                                percentage >= 100 ? "bg-rose-500/20 text-rose-400" :
                                                    percentage > 80 ? "bg-amber-500/20 text-amber-400" : "bg-emerald-500/20 text-emerald-400"
                                            )}>
                                                {Math.round((group.spent / group.limit) * 100)}%
                                            </span>
                                        </div>
                                    )}
                                </div>

                                {/* Progress Bar */}
                                {hasLimit && (
                                    <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden mx-2 opacity-50">
                                        <div
                                            className={cn("h-full transition-all duration-500 rounded-full", getProgressColor((group.spent / group.limit) * 100))}
                                            style={{ width: `${percentage}%` }}
                                        />
                                    </div>
                                )}

                                {/* Children */}
                                {isExpanded && hasChildren && (
                                    <div className="pl-14 pr-2 pt-2 space-y-3 animate-in slide-in-from-top-2 fade-in duration-200">
                                        {group.children.sort((a, b) => b.spent - a.spent).map(child => {
                                            const childLimit = child.limit || 0
                                            const childPercentage = childLimit > 0 ? Math.min((child.spent / childLimit) * 100, 100) : 0

                                            return (
                                                <div key={child.id} className="space-y-1">
                                                    <div className="flex justify-between items-center text-sm group/child">
                                                        <span className="text-slate-400 group-hover/child:text-slate-300 transition-colors flex items-center gap-2">
                                                            <div className="w-1.5 h-1.5 rounded-full bg-slate-700" />
                                                            {child.name}
                                                        </span>
                                                        <div className="flex items-center gap-2">
                                                            <span className="text-slate-300"><Money amount={child.spent} /></span>
                                                            {childLimit > 0 && (
                                                                <span className="text-[10px] text-slate-500 flex items-center gap-1">/ <Money amount={childLimit} /></span>
                                                            )}
                                                        </div>
                                                    </div>
                                                    {childLimit > 0 && (
                                                        <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden ml-3.5 opacity-40">
                                                            <div
                                                                className={cn("h-full transition-all duration-500 rounded-full", getProgressColor((child.spent / childLimit) * 100))}
                                                                style={{ width: `${childPercentage}%` }}
                                                            />
                                                        </div>
                                                    )}
                                                </div>
                                            )
                                        })}
                                    </div>
                                )}
                            </div>
                        )
                    })}

                    {groups.length === 0 && (
                        <p className="text-center text-slate-500 py-6 text-sm">{t('no_expenses_this_month')}</p>
                    )}
                </div>
            </CardContent>
        </Card>
    )
}

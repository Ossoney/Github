'use client'

import { useState, useEffect } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Button, Card, CardContent, CardHeader, CardTitle, Input } from '@/components/ui/UI'
import { Calculator, Save, RotateCcw } from 'lucide-react'
import { cn } from '@/lib/utils'
import * as LucideIcons from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function BudgetManager() {
    const { t, tCategory, formatMoney, symbol, language } = useLanguage()

    // 1. Fetch Categories & Existing Budgets
    const categories = useLiveQuery(() => db.categories.where('type').equals('expense').toArray())
    const budgets = useLiveQuery(() => db.budgets.toArray())

    // 2. Local State for Form
    const [globalBudget, setGlobalBudget] = useState('')
    const [categoryBudgets, setCategoryBudgets] = useState({}) // { catId: amount }

    // 3. Load Data into State
    useEffect(() => {
        if (budgets) {
            // Global
            const global = budgets.find(b => b.type === 'global')
            if (global) setGlobalBudget(global.amount)

            // Categories
            const catMap = {}
            budgets.filter(b => b.type === 'category').forEach(b => {
                catMap[b.categoryId] = b.amount
            })
            setCategoryBudgets(catMap)
        }
    }, [budgets])

    // 4. Handlers
    const handleGlobalChange = async (val) => {
        setGlobalBudget(val)
        const amount = parseFloat(val)

        // Save immediately (debounce ideally, but direct for now)
        if (!isNaN(amount) && amount > 0) {
            await db.budgets.put({
                id: 'global',
                type: 'global',
                amount: amount
            })
        } else if (val === '') {
            // Optional: delete or set to 0? Let's delete if cleared
            await db.budgets.delete('global')
        }
    }

    const handleCategoryChange = async (catId, val) => {
        setCategoryBudgets(prev => ({ ...prev, [catId]: val }))
        const amount = parseFloat(val)

        if (!isNaN(amount) && amount > 0) {
            await db.budgets.put({
                id: `cat-${catId}`,
                type: 'category',
                categoryId: catId,
                amount: amount
            })
        } else if (val === '') {
            await db.budgets.delete(`cat-${catId}`)
        }
    }

    // Filter Parent Categories
    const rootCategories = (categories?.filter(c => !c.parentId) || [])
        .sort((a, b) => tCategory(a.name).localeCompare(tCategory(b.name), language))

    return (
        <Card className="border-slate-800 bg-slate-900/50">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-lg text-slate-200 flex items-center gap-2">
                    <Calculator className="w-5 h-5 text-sky-500" /> Gestor de Presupuestos
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-8 pt-6">

                {/* Global Budget Section */}
                <div className="bg-slate-800/30 p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-200 font-medium mb-4 flex items-center gap-2">
                        <span>🌍</span> Presupuesto Global Mensual
                    </h3>
                    <div className="flex gap-4 items-center">
                        <div className="relative flex-1 max-w-xs">
                            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">{symbol}</span>
                            <Input
                                type="number"
                                value={globalBudget}
                                onChange={(e) => handleGlobalChange(e.target.value)}
                                placeholder="Sin límite"
                                className="pl-8 text-lg font-semibold bg-slate-950 border-slate-700"
                            />
                        </div>
                        <p className="text-sm text-slate-500">
                            Este es el techo de gasto total para el mes.
                        </p>
                    </div>
                </div>

                {/* Category Budgets */}
                <div>
                    <h3 className="text-slate-200 font-medium mb-4 px-1">Presupuestos por Categoría</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {rootCategories.map(cat => {
                            const Icon = LucideIcons[cat.icon] || LucideIcons.HelpCircle
                            const amount = categoryBudgets[cat.id] || ''

                            return (
                                <div key={cat.id} className="flex items-center gap-4 p-3 rounded-xl bg-slate-800/20 border border-slate-800 hover:border-slate-700 transition-colors">
                                    <div
                                        className="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
                                        style={{ backgroundColor: `${cat.color}20`, color: cat.color }}
                                    >
                                        <Icon className="w-5 h-5" />
                                    </div>
                                    <div className="flex-1">
                                        <p className="font-medium text-slate-300 text-sm">{tCategory(cat.name)}</p>
                                    </div>
                                    <div className="w-32 relative">
                                        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-xs">{symbol}</span>
                                        <Input
                                            type="number"
                                            value={amount}
                                            onChange={(e) => handleCategoryChange(cat.id, e.target.value)}
                                            placeholder="Auto"
                                            className="pl-7 h-9 text-right text-sm bg-slate-950 border-slate-800 focus:border-sky-500"
                                        />
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                    {rootCategories.length === 0 && (
                        <p className="text-center text-slate-500 py-8">No hay categorías de gasto configuradas.</p>
                    )}
                </div>

            </CardContent>
        </Card>
    )
}

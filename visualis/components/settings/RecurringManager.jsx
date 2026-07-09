'use client'

import { useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Button, Card, CardContent, CardHeader, CardTitle, Input, ConfirmDialog } from '@/components/ui/UI'
import { Repeat, Plus, Trash2, CalendarClock } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function RecurringManager() {
    const recurring = useLiveQuery(() => db.recurring.toArray())
    const wallets = useLiveQuery(() => db.wallets.toArray())
    const allCategories = useLiveQuery(() => db.categories.toArray())
    const { t, formatMoney } = useLanguage()

    const [isCreating, setIsCreating] = useState(false)
    const [editingId, setEditingId] = useState(null)
    const [type, setType] = useState('expense')
    const [amount, setAmount] = useState('')
    const [day, setDay] = useState(1)
    const [walletId, setWalletId] = useState('')
    const [categoryId, setCategoryId] = useState('')
    const [description, setDescription] = useState('')

    // Confirm state
    const [deleteId, setDeleteId] = useState(null)

    const handleEdit = (item) => {
        setEditingId(item.id)
        setType(item.type)
        setAmount(item.amount)
        setDay(item.dayOfMonth)
        setWalletId(item.walletId)
        setCategoryId(item.categoryId)
        setDescription(item.description)
        setIsCreating(true)
    }

    const handleCreate = async () => {
        if (!amount || !walletId || !categoryId) return
        try {
            const data = {
                type,
                amount: parseFloat(amount),
                dayOfMonth: parseInt(day),
                walletId: parseInt(walletId),
                categoryId: parseInt(categoryId),
                description,
                active: true,
            }

            if (editingId) {
                await db.recurring.update(editingId, data)
                setEditingId(null)
            } else {
                await db.recurring.add({ ...data, lastRun: null })
            }

            setIsCreating(false)
            resetForm()
        } catch (err) {
            console.error(err)
        }
    }

    const resetForm = () => {
        setAmount('')
        setDay(1)
        setDescription('')
        setEditingId(null)
    }

    const handleDelete = () => {
        if (deleteId) {
            db.recurring.delete(deleteId)
            setDeleteId(null)
        }
    }

    return (
        <>
            <Card className="border-slate-800 bg-slate-900/50">
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="text-lg text-slate-200 flex items-center gap-2">
                        <Repeat className="w-5 h-5 text-sky-500" /> {t('recurring_transactions')}
                    </CardTitle>
                    <Button size="sm" onClick={() => { setIsCreating(true); resetForm(); }} disabled={isCreating}>
                        <Plus className="w-4 h-4 mr-2" /> {t('new_transaction').split(' ')[0]}
                    </Button>
                </CardHeader>
                <CardContent className="space-y-4">

                    {isCreating && (
                        <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700 space-y-3 animate-in fade-in slide-in-from-top-2">
                            <div className="flex justify-between items-center mb-2">
                                <h3 className="text-sm font-medium text-slate-300">{editingId ? t('edit_recurring') : t('new_recurring')}</h3>
                                {editingId && <Button variant="ghost" size="sm" className="h-6 text-xs" onClick={() => { setIsCreating(false); resetForm(); }}>{t('cancel')}</Button>}
                            </div>

                            <div className="grid grid-cols-2 gap-2">
                                <Button
                                    variant={type === 'expense' ? 'destructive' : 'outline'}
                                    onClick={() => setType('expense')}
                                    className={type !== 'expense' ? "border-slate-700 text-slate-400" : ""}
                                >{t('expense')}</Button>
                                <Button
                                    variant={type === 'income' ? 'default' : 'outline'}
                                    className={type === 'income' ? "bg-emerald-600 hover:bg-emerald-700" : "border-slate-700 text-slate-400"}
                                    onClick={() => setType('income')}
                                >{t('income')}</Button>
                            </div>

                            <div className="grid grid-cols-2 gap-2">
                                <Input
                                    placeholder={t('amount')}
                                    type="number"
                                    value={amount}
                                    onChange={e => setAmount(e.target.value)}
                                />
                                <div className="relative">
                                    <Input
                                        placeholder={t('day_of_month')}
                                        type="number"
                                        min="1" max="31"
                                        value={day}
                                        onChange={e => setDay(e.target.value)}
                                        className="pl-8"
                                    />
                                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-xs">#</span>
                                </div>
                            </div>

                            <select
                                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200"
                                value={walletId}
                                onChange={e => setWalletId(e.target.value)}
                            >
                                <option value="" disabled>{t('select_account')}</option>
                                {wallets?.map(w => <option key={w.id} value={w.id}>{w.name}</option>)}
                            </select>

                            <select
                                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200"
                                value={categoryId}
                                onChange={e => setCategoryId(e.target.value)}
                            >
                                <option value="" disabled>{t('select_category')}</option>
                                {allCategories?.filter(c => c.type === type && !c.parentId).map(c => (
                                    <option key={c.id} value={c.id}>{c.name}</option>
                                ))}
                            </select>

                            <Input
                                placeholder={`${t('description')} (ej. Spotify)`}
                                value={description}
                                onChange={e => setDescription(e.target.value)}
                            />

                            <div className="flex gap-2 justify-end">
                                <Button variant="ghost" size="sm" onClick={() => { setIsCreating(false); resetForm(); }}>{t('cancel')}</Button>
                                <Button size="sm" onClick={handleCreate}>{editingId ? t('update') : t('save')}</Button>
                            </div>
                        </div>
                    )}

                    <div className="space-y-2">
                        {recurring?.map(item => {
                            const wallet = wallets?.find(w => w.id === item.walletId)
                            const cat = allCategories?.find(c => c.id === item.categoryId)
                            return (
                                <div
                                    key={item.id}
                                    className="flex items-center justify-between p-3 bg-slate-800/30 rounded-xl border border-slate-800/50 hover:bg-slate-800/50 transition-colors cursor-pointer group"
                                    onClick={() => handleEdit(item)}
                                >
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 group-hover:text-sky-400 transition-colors">
                                            <CalendarClock className="w-5 h-5" />
                                        </div>
                                        <div>
                                            <p className="font-medium text-slate-200 group-hover:text-sky-300 transition-colors">{item.description || cat?.name}</p>
                                            <p className="text-xs text-slate-500">{t('day_of_month')} {item.dayOfMonth} • {wallet?.name}</p>
                                        </div>
                                    </div>
                                    <div className="text-right flex items-center gap-3">
                                        <span className={item.type === 'income' ? "text-emerald-400 font-bold" : "text-slate-200 font-bold"}>
                                            {item.type === 'expense' ? '-' : '+'}{formatMoney(item.amount)}
                                        </span>
                                        <Button
                                            size="icon"
                                            variant="ghost"
                                            onClick={(e) => { e.stopPropagation(); setDeleteId(item.id); }}
                                            className="text-slate-500 hover:text-rose-400 h-8 w-8"
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </Button>
                                    </div>
                                </div>
                            )
                        })}
                        {recurring?.length === 0 && (
                            <p className="text-center text-slate-500 py-4">{t('no_recurring')}</p>
                        )}
                    </div>

                </CardContent>
            </Card>

            <ConfirmDialog
                isOpen={!!deleteId}
                onClose={() => setDeleteId(null)}
                onConfirm={handleDelete}
                title={t('delete')}
                message={t('confirm_delete_recurring')}
            />
        </>
    )
}

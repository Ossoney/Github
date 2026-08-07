'use client'

import { useState, useEffect } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Button, Card, CardContent, CardHeader, CardTitle, Input, ConfirmDialog } from '@/components/ui/UI'
import { Wallet, Plus, Trash2, Edit2, Save, X, GripVertical, Eye, EyeOff } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'
import { Reorder } from 'framer-motion'

export function AccountManager() {
    const walletsFromDB = useLiveQuery(async () => {
        const all = await db.wallets.toArray()
        return all.sort((a, b) => (a.order ?? a.id) - (b.order ?? b.id))
    })
    const { t, formatMoney } = useLanguage()

    // Local ordered list — needed so Reorder.Group has a stable, controlled array
    const [items, setItems] = useState([])

    // Sync local state when DB changes (but only if not currently dragging)
    const [isDragging, setIsDragging] = useState(false)
    useEffect(() => {
        if (!isDragging && walletsFromDB) {
            setItems(walletsFromDB)
        }
    }, [walletsFromDB, isDragging])

    const [isEditing, setIsEditing] = useState(null)
    const [newAccountName, setNewAccountName] = useState('')
    const [newAccountType, setNewAccountType] = useState('bank')
    const [initialBalance, setInitialBalance] = useState('')
    const [isCreating, setIsCreating] = useState(false)

    // Edit State
    const [editName, setEditName] = useState('')
    const [editBalance, setEditBalance] = useState('')

    // Delete Confirmation State
    const [deleteId, setDeleteId] = useState(null)

    const handleCreate = async () => {
        if (!newAccountName) return
        try {
            const maxOrder = items.length > 0 ? Math.max(...items.map(w => w.order ?? w.id)) : 0
            await db.wallets.add({
                name: newAccountName,
                type: newAccountType,
                balance: parseFloat(initialBalance) || 0,
                currency: 'EUR',
                order: maxOrder + 1,
                hidden: false,
            })
            setNewAccountName('')
            setInitialBalance('')
            setIsCreating(false)
        } catch (err) {
            console.error("Error creating wallet", err)
        }
    }

    const handleDelete = async () => {
        if (deleteId) {
            await db.wallets.delete(deleteId)
            setDeleteId(null)
        }
    }

    const startEdit = (wallet) => {
        setIsEditing(wallet.id)
        setEditName(wallet.name)
        setEditBalance(wallet.balance.toString())
    }

    const saveEdit = async (id) => {
        await db.wallets.update(id, {
            name: editName,
            balance: parseFloat(editBalance) || 0
        })
        setIsEditing(null)
    }

    const handleToggleVisibility = async (wallet) => {
        await db.wallets.update(wallet.id, { hidden: !wallet.hidden })
    }

    // Called continuously while dragging — just update local state for smooth UI
    const handleReorderLocal = (newOrder) => {
        setItems(newOrder)
    }

    // Called when drag ends — persist new order to DB
    const handleDragEnd = async () => {
        setIsDragging(false)
        try {
            await db.transaction('rw', db.wallets, async () => {
                for (let i = 0; i < items.length; i++) {
                    await db.wallets.update(items[i].id, { order: i })
                }
            })
        } catch (err) {
            console.error("Error reordering wallets", err)
        }
    }

    return (
        <>
            <Card className="border-slate-800 bg-slate-900/50">
                <CardHeader className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <CardTitle className="text-lg text-slate-200 flex items-center gap-2">
                        <Wallet className="w-5 h-5 text-sky-500 shrink-0" /> {t('my_accounts')}
                    </CardTitle>
                    <Button size="sm" onClick={() => setIsCreating(true)} disabled={isCreating} className="w-full sm:w-auto">
                        <Plus className="w-4 h-4 mr-2" /> {t('create_account')}
                    </Button>
                </CardHeader>
                <CardContent className="space-y-4">

                    {/* Create Form */}
                    {isCreating && (
                        <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700 space-y-3 animate-in fade-in slide-in-from-top-2">
                            <Input
                                placeholder={t('account_name_placeholder')}
                                value={newAccountName}
                                onChange={(e) => setNewAccountName(e.target.value)}
                                autoFocus
                            />
                            <div className="flex gap-2">
                                <Input
                                    type="number"
                                    placeholder={t('initial_balance')}
                                    value={initialBalance}
                                    onChange={(e) => setInitialBalance(e.target.value)}
                                    className="w-full"
                                />
                            </div>
                            <div className="flex gap-2 justify-end">
                                <Button variant="ghost" size="sm" onClick={() => setIsCreating(false)}>{t('cancel')}</Button>
                                <Button size="sm" onClick={handleCreate}>{t('create_account')}</Button>
                            </div>
                        </div>
                    )}

                    {/* List */}
                    <Reorder.Group
                        axis="y"
                        values={items}
                        onReorder={handleReorderLocal}
                        className="space-y-2"
                    >
                        {items.map(wallet => (
                            <Reorder.Item
                                key={wallet.id}
                                value={wallet}
                                onDragStart={() => setIsDragging(true)}
                                onDragEnd={handleDragEnd}
                                dragListener={isEditing !== wallet.id}
                                className={`flex items-center justify-between p-3 rounded-xl border transition-colors ${
                                    wallet.hidden
                                        ? 'bg-slate-800/10 border-slate-800/30 opacity-50'
                                        : 'bg-slate-800/30 border-slate-800/50 hover:border-slate-700'
                                } ${isEditing !== wallet.id ? 'cursor-grab active:cursor-grabbing' : 'cursor-default'}`}
                            >
                                <div className="flex items-center gap-3 flex-1">
                                    <GripVertical className="w-4 h-4 text-slate-600 shrink-0" />

                                    {isEditing === wallet.id ? (
                                        <div className="flex flex-col gap-2 flex-1">
                                            <div className="flex items-center gap-2">
                                                <Input
                                                    value={editName}
                                                    onChange={(e) => setEditName(e.target.value)}
                                                    className="h-8 text-sm"
                                                    placeholder={t('name')}
                                                    autoFocus
                                                />
                                                <Button size="icon" variant="ghost" onClick={() => saveEdit(wallet.id)} className="text-emerald-400 shrink-0">
                                                    <Save className="w-4 h-4" />
                                                </Button>
                                                <Button size="icon" variant="ghost" onClick={() => setIsEditing(null)} className="text-slate-400 shrink-0">
                                                    <X className="w-4 h-4" />
                                                </Button>
                                            </div>
                                            <div className="flex items-center gap-2 px-1">
                                                <span className="text-[10px] text-slate-500 uppercase font-bold shrink-0">{t('current_balance')}:</span>
                                                <Input
                                                    type="number"
                                                    value={editBalance}
                                                    onChange={(e) => setEditBalance(e.target.value)}
                                                    className="h-6 text-[10px] border-slate-700 bg-slate-800/50"
                                                />
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="flex items-center gap-3">
                                            <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors ${wallet.hidden ? 'bg-slate-800/50 text-slate-600' : 'bg-slate-800 text-slate-400'}`}>
                                                <Wallet className="w-5 h-5" />
                                            </div>
                                            <div>
                                                <p className={`font-medium transition-colors ${wallet.hidden ? 'text-slate-500' : 'text-slate-200'}`}>{wallet.name}</p>
                                                <p className="text-xs text-slate-500 capitalize">{formatMoney(wallet.balance)}</p>
                                            </div>
                                        </div>
                                    )}
                                </div>

                                {isEditing !== wallet.id && (
                                    <div className="flex items-center gap-1">
                                        {/* Visibility toggle */}
                                        <Button
                                            size="icon"
                                            variant="ghost"
                                            onClick={() => handleToggleVisibility(wallet)}
                                            className={wallet.hidden ? 'text-slate-600 hover:text-slate-300' : 'text-sky-400 hover:text-sky-300'}
                                            title={wallet.hidden ? t('show_account') : t('hide_account')}
                                        >
                                            {wallet.hidden ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                        </Button>
                                        <Button size="icon" variant="ghost" onClick={() => startEdit(wallet)} className="text-slate-400 hover:text-sky-400">
                                            <Edit2 className="w-4 h-4" />
                                        </Button>
                                        <Button size="icon" variant="ghost" onClick={() => setDeleteId(wallet.id)} className="text-slate-400 hover:text-rose-400">
                                            <Trash2 className="w-4 h-4" />
                                        </Button>
                                    </div>
                                )}
                            </Reorder.Item>
                        ))}
                    </Reorder.Group>
                    {items.length === 0 && (
                        <p className="text-center text-slate-500 py-4">{t('no_accounts')}</p>
                    )}

                </CardContent>
            </Card>

            <ConfirmDialog
                isOpen={!!deleteId}
                onClose={() => setDeleteId(null)}
                onConfirm={handleDelete}
                title={t('delete')}
                message={t('confirm_delete_account')}
            />
        </>
    )
}

import { useState, useEffect } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { useStore } from '@/hooks/useStore'
import { Button, Card, useToast } from '@/components/ui/UI'
import { X, ChevronLeft, ChevronDown, Calendar as CalendarIcon, Tag, MessageSquare, Wallet, Trash2 } from 'lucide-react'
import * as LucideIcons from 'lucide-react'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

export function TransactionForm() {
    const { isTransactionModalOpen, closeTransactionModal, editingTransaction } = useStore()
    const { t, tCategory, symbol, language } = useLanguage()
    const { addToast } = useToast()
    const wallets = useLiveQuery(() => db.wallets.toArray())
    const allCategories = useLiveQuery(() => db.categories.toArray())

    // Form State
    const [type, setType] = useState('expense')
    const [amount, setAmount] = useState('')
    const [walletId, setWalletId] = useState('')

    // Category State
    const [categoryId, setCategoryId] = useState(null)
    const [selectedParentId, setSelectedParentId] = useState(null) // For category browsing

    // Details
    const [description, setDescription] = useState('')
    const [tagsInput, setTagsInput] = useState('')
    const [datetime, setDatetime] = useState(new Date().toISOString().slice(0, 16))

    // Reset on Open / Populate for Edit
    useEffect(() => {
        if (isTransactionModalOpen) {
            if (editingTransaction) {
                // POPULATE FOR EDIT
                setType(editingTransaction.type)
                setAmount(editingTransaction.amount !== undefined && editingTransaction.amount !== null ? editingTransaction.amount.toString() : '')
                setWalletId(editingTransaction.walletId)

                // Set Category (Parent or Child)
                setCategoryId(editingTransaction.categoryId)
                const category = allCategories?.find(c => c.id === editingTransaction.categoryId)
                if (category?.parentId) {
                    setSelectedParentId(category.parentId)
                } else {
                    setSelectedParentId(null)
                }

                setDescription(editingTransaction.description || '')
                setTagsInput(editingTransaction.tags ? editingTransaction.tags.join(' ') : '')

                // Date
                const date = new Date(editingTransaction.date)
                if (!isNaN(date.getTime())) {
                    date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
                    setDatetime(date.toISOString().slice(0, 16))
                } else {
                    const now = new Date()
                    now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
                    setDatetime(now.toISOString().slice(0, 16))
                }

            } else {
                // RESET FOR NEW
                setAmount('')
                setCategoryId(null)
                setSelectedParentId(null)
                setDescription('')
                setTagsInput('')

                const now = new Date()
                now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
                setDatetime(now.toISOString().slice(0, 16))

                if (wallets && wallets.length > 0 && !walletId) {
                    setWalletId(wallets[0].id)
                }
            }
        }
    }, [isTransactionModalOpen, editingTransaction, wallets, allCategories])

    const existingTags = useLiveQuery(() => db.tags.toArray())

    const handleTagClick = (tagName) => {
        const current = tagsInput.split(' ').filter(t => t)
        if (current.includes(tagName)) {
            setTagsInput(current.filter(t => t !== tagName).join(' '))
        } else {
            setTagsInput([...current, tagName].join(' '))
        }
    }

    const handleSubmit = async () => {
        // Explicit validation
        if (!amount) {
            addToast(t('validation_amount'), 'error')
            return
        }
        if (!walletId) {
            addToast(t('validation_wallet'), 'error')
            return
        }
        if (!categoryId) {
            addToast(t('validation_category'), 'error')
            return
        }

        const value = parseFloat(amount)
        if (isNaN(value)) {
            addToast(t('validation_amount_invalid'), 'error')
            return
        }

        const tags = tagsInput.split(/[\s,]+/).filter(t => t).map(t => t.startsWith('#') ? t : `#${t}`)
        const txDate = new Date(datetime)

        if (isNaN(txDate.getTime())) {
            addToast(t('validation_date_invalid'), 'error')
            return
        }

        try {
            await db.transaction('rw', db.transactions, db.wallets, async () => {

                // IF EDITING: Revert old transaction effect first
                if (editingTransaction && editingTransaction.walletId) {
                    const oldWallet = await db.wallets.get(editingTransaction.walletId)
                    if (oldWallet) {
                        const revertAmount = editingTransaction.type === 'income'
                            ? -editingTransaction.amount
                            : editingTransaction.amount

                        await db.wallets.update(editingTransaction.walletId, {
                            balance: oldWallet.balance + revertAmount
                        })
                    }

                    // Update the transaction record
                    await db.transactions.update(editingTransaction.id, {
                        walletId,
                        categoryId,
                        amount: value,
                        type,
                        description,
                        tags,
                        date: txDate,
                    })

                } else {
                    // NEW TRANSACTION
                    await db.transactions.add({
                        walletId,
                        categoryId,
                        amount: value,
                        type,
                        description,
                        tags,
                        date: txDate,
                    })
                }

                // Apply NEW transaction effect (always done for both New and Edit)
                // Note: For edit, we reverted the old effect, so now we just apply the new one as if it's new.
                // This handles cases where wallet, amount, or type changed seamlessly.
                const targetWallet = await db.wallets.get(walletId)
                if (targetWallet) {
                    const applyAmount = type === 'income' ? value : -value
                    await db.wallets.update(walletId, {
                        balance: targetWallet.balance + applyAmount
                    })
                }
            })

            closeTransactionModal()
        } catch (error) {
            console.error("Failed to save transaction:", error)
            addToast(`${t('error_saving')}: ${error.message}`, 'error')
        }
    }

    const handleDelete = async () => {
        if (!editingTransaction || !confirm(t('confirm_delete_transaction'))) return

    }

    if (!isTransactionModalOpen) return null

    // ------------------------------------------------------------------
    // Category Logic
    // ------------------------------------------------------------------
    const rootCategories = (allCategories?.filter(c => c.type === type && !c.parentId) || [])
        .sort((a, b) => tCategory(a.name).localeCompare(tCategory(b.name), language))
    const subCategories = (selectedParentId
        ? allCategories?.filter(c => c.parentId === selectedParentId)
        : [])
        .sort((a, b) => tCategory(a.name).localeCompare(tCategory(b.name), language))

    // Helper to get selected category object
    const selectedCategory = allCategories?.find(c => c.id === categoryId)
    // Helper to get selected category icon
    const SelectedIcon = selectedCategory ? (LucideIcons[selectedCategory.icon] || LucideIcons.HelpCircle) : null

    // ------------------------------------------------------------------
    // RENDER
    // ------------------------------------------------------------------
    return (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <Card className="w-full max-w-md bg-slate-900 border-slate-800 shadow-2xl animate-in slide-in-from-bottom-10 duration-300 max-h-[90vh] flex flex-col">

                {/* Header & Type Switcher (Fixed Top) */}
                <div className="p-4 border-b border-slate-800 space-y-4 shrink-0 bg-slate-900 z-10 rounded-t-xl">
                    <div className="flex justify-between items-center">
                        <h2 className="text-xl font-bold text-slate-200">{editingTransaction ? t('edit_transaction') : t('new_transaction')}</h2>
                        <button onClick={closeTransactionModal} className="text-slate-500 hover:text-slate-300">
                            <X className="w-6 h-6" />
                        </button>
                    </div>

                    <div className="grid grid-cols-2 gap-2 p-1 bg-slate-800/50 rounded-xl">
                        <button
                            onClick={() => { setType('expense'); setCategoryId(null); setSelectedParentId(null); }}
                            className={cn("py-2 px-4 rounded-lg text-sm font-medium transition-all", type === 'expense' ? "bg-rose-500 text-white shadow-lg shadow-rose-500/20" : "text-slate-400 hover:text-slate-200")}
                        >{t('expense')}</button>
                        <button
                            onClick={() => { setType('income'); setCategoryId(null); setSelectedParentId(null); }}
                            className={cn("py-2 px-4 rounded-lg text-sm font-medium transition-all", type === 'income' ? "bg-emerald-500 text-white shadow-lg shadow-emerald-500/20" : "text-slate-400 hover:text-slate-200")}
                        >{t('income')}</button>
                    </div>
                </div>

                {/* SCROLLABLE CONTENT */}
                <div className="p-4 space-y-6 overflow-y-auto custom-scrollbar">

                    {/* 1. Main Inputs Row (Amount + Date + Wallet) */}
                    <div className="space-y-4">
                        {/* Amount */}
                        <div className="relative">
                            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-2xl text-slate-500 font-light">{symbol}</span>
                            <input
                                type="number"
                                value={amount}
                                onChange={(e) => setAmount(e.target.value)}
                                placeholder="0.00"
                                autoFocus={!editingTransaction} // Don't autofocus on edit to prevent keyboard pop-up
                                className="w-full bg-slate-950 border border-slate-800 rounded-2xl py-4 pl-12 pr-4 text-3xl font-bold text-slate-100 placeholder:text-slate-700 focus:outline-none focus:border-sky-500 transition-all"
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                            {/* Date */}
                            <div className="relative">
                                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"><CalendarIcon className="w-4 h-4" /></span>
                                <input
                                    type="datetime-local"
                                    value={datetime}
                                    onChange={(e) => setDatetime(e.target.value)}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-9 pr-2 text-sm text-slate-200 focus:outline-none focus:border-sky-500 [color-scheme:dark]"
                                />
                            </div>

                            {/* Wallet */}
                            <div className="relative">
                                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"><Wallet className="w-4 h-4" /></span>
                                <select
                                    value={walletId}
                                    onChange={(e) => setWalletId(parseInt(e.target.value))}
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-9 pr-8 text-sm text-slate-200 focus:outline-none focus:border-sky-500 appearance-none"
                                >
                                    <option value="" disabled>{t('select_wallet')}</option>
                                    {wallets?.map(w => (
                                        <option key={w.id} value={w.id}>{w.name}</option>
                                    ))}
                                </select>
                                <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                            </div>
                        </div>
                    </div>

                    {/* 2. Category Selection (Integrated) */}
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-slate-500 uppercase tracking-wider block">{t('category')}</label>

                        {/* Current Selection Display */}
                        {selectedCategory ? (
                            <div
                                onClick={() => { setCategoryId(null); setSelectedParentId(null); }}
                                className="flex items-center justify-between p-3 rounded-xl bg-sky-500/10 border border-sky-500/30 cursor-pointer hover:bg-sky-500/20 transition-colors"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-full flex items-center justify-center bg-sky-500 text-white">
                                        <SelectedIcon className="w-4 h-4" />
                                    </div>
                                    <span className="font-medium text-sky-400">{tCategory(selectedCategory.name)}</span>
                                </div>
                                <span className="text-xs text-sky-400 font-medium">{t('change')}</span>
                            </div>
                        ) : (
                            <div className="bg-slate-900 border border-slate-800 rounded-xl p-3">
                                {/* Parent Categories List (Horizontal Scroll if needed, but grid for now) */}
                                {!selectedParentId ? (
                                    <div className="grid grid-cols-4 gap-2">
                                        {rootCategories.map(cat => {
                                            const Icon = LucideIcons[cat.icon] || LucideIcons.HelpCircle

                                            // Check validity for drill-down vs select
                                            const hasChildren = allCategories?.some(c => c.parentId === cat.id)

                                            return (
                                                <button
                                                    key={cat.id}
                                                    onClick={() => hasChildren ? setSelectedParentId(cat.id) : setCategoryId(cat.id)}
                                                    className="flex flex-col items-center gap-1 p-2 rounded-lg hover:bg-slate-800 transition-colors"
                                                >
                                                    <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-400" style={{ color: cat.color }}>
                                                        <Icon className="w-5 h-5" />
                                                    </div>
                                                    <span className="text-[10px] text-slate-400 truncate w-full text-center">{tCategory(cat.name)}</span>
                                                </button>
                                            )
                                        })}
                                    </div>
                                ) : (
                                    <div className="space-y-2 animate-in slide-in-from-right-4 fade-in duration-200">
                                        <button
                                            onClick={() => setSelectedParentId(null)}
                                            className="flex items-center gap-1 text-xs text-slate-500 hover:text-slate-300 mb-2"
                                        >
                                            <ChevronLeft className="w-3 h-3" /> {t('back_to_categories')}
                                        </button>
                                        <div className="grid grid-cols-3 gap-2">
                                            {subCategories.map(cat => (
                                                <button
                                                    key={cat.id}
                                                    onClick={() => setCategoryId(cat.id)}
                                                    className="p-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 text-xs text-slate-300 border border-slate-700/50 truncate"
                                                >
                                                    {tCategory(cat.name)}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>

                    {/* 3. Optional Details */}
                    <div className="space-y-4 pt-2 border-t border-slate-800">
                        {/* Tags */}
                        <div className="relative">
                            <input
                                type="text"
                                value={tagsInput}
                                onChange={(e) => setTagsInput(e.target.value)}
                                placeholder="#etiquetas"
                                className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-10 pr-3 text-sm text-slate-200 focus:outline-none focus:border-sky-500"
                            />
                            <Tag className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-600" />
                        </div>
                        {/* Suggestions: Show all predefined tags */}
                        {existingTags?.length > 0 && (
                            <div className="flex flex-wrap gap-2">
                                {existingTags.map(tag => {
                                    const isSelected = tagsInput.includes(tag.name)
                                    return (
                                        <button
                                            key={tag.id}
                                            onClick={() => handleTagClick(tag.name)}
                                            className={cn(
                                                "text-[10px] px-2 py-1.5 rounded-full border transition-all font-medium",
                                                isSelected
                                                    ? "bg-sky-500 text-white border-sky-500 shadow-lg shadow-sky-500/20"
                                                    : "bg-slate-900 border-slate-700 text-slate-400 hover:border-slate-500 hover:text-slate-200"
                                            )}
                                        >
                                            {tag.name}
                                        </button>
                                    )
                                })}
                            </div>
                        )}

                        {/* Comment */}
                        <div className="relative">
                            <textarea
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                placeholder={t('optional_note')}
                                rows={2}
                                className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-10 pr-3 text-sm text-slate-200 focus:outline-none focus:border-sky-500 resize-none"
                            />
                            <MessageSquare className="absolute left-3 top-3 w-4 h-4 text-slate-600" />
                        </div>
                    </div>

                </div>

                {/* Footer (Fixed Bottom) */}
                <div className="p-4 border-t border-slate-800 shrink-0 bg-slate-900 rounded-b-xl z-10 flex gap-3">
                    {editingTransaction && (
                        <Button
                            onClick={handleDelete}
                            className="py-6 rounded-xl bg-slate-800 hover:bg-rose-900/50 text-rose-500 border border-transparent hover:border-rose-900"
                            variant="ghost"
                        >
                            <Trash2 className="w-5 h-5" />
                        </Button>
                    )}
                    <Button
                        onClick={handleSubmit}
                        className="w-full py-6 text-lg rounded-xl flex-1"
                        variant={type === 'expense' ? 'danger' : 'default'}
                        // Allow saving if amount and category are present. Wallet should be defaulted or user selected.
                        disabled={!amount || !categoryId}
                    >
                        {editingTransaction ? t('update') : `${t('save')} ${type === 'expense' ? t('expense') : t('income')}`}
                    </Button>
                </div>

            </Card>
        </div>
    )
}

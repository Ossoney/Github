import { useState, useEffect, useRef } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { useStore } from '@/hooks/useStore'
import { Button, Card, useToast } from '@/components/ui/UI'
import { ConfirmDialog } from '@/components/ui/ConfirmDialog'
import { CalculatorModal } from '@/components/ui/CalculatorModal'
import { X, ChevronLeft, ChevronDown, Calendar as CalendarIcon, Tag, MessageSquare, Wallet, Trash2, Split, PlusCircle, MinusCircle, Smile, Repeat, ArrowRightLeft } from 'lucide-react'
import * as LucideIcons from 'lucide-react'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

export function TransactionForm() {
    const { isTransactionModalOpen, closeTransactionModal, editingTransaction, newTransactionType } = useStore()
    const { t, tCategory, symbol, language } = useLanguage()
    const { addToast } = useToast()
    const wallets = useLiveQuery(() => db.wallets.toArray())
    const allCategories = useLiveQuery(() => db.categories.toArray())

    // Form State
    const [type, setType] = useState('expense')
    const [amount, setAmount] = useState('')
    const [walletId, setWalletId] = useState('')
    const [toWalletId, setToWalletId] = useState('')
    const [isSubmitting, setIsSubmittingState] = useState(false)
    const isSubmittingRef = useRef(false)

    const setIsSubmitting = (val) => {
        isSubmittingRef.current = val
        setIsSubmittingState(val)
    }

    // Category State
    const [categoryId, setCategoryId] = useState(null)
    const [selectedParentId, setSelectedParentId] = useState(null) // For category browsing

    // Split State
    const [isSplitMode, setIsSplitMode] = useState(false)
    const [splits, setSplits] = useState([{ id: 1, categoryId: null, amount: '' }, { id: 2, categoryId: null, amount: '' }]) // Start with 2


    // Details
    const [description, setDescription] = useState('')
    const [tagsInput, setTagsInput] = useState('')
    const [datetime, setDatetime] = useState(new Date().toISOString().slice(0, 16))
    const [emotion, setEmotion] = useState(null) // New emotion state
    const [isRecurring, setIsRecurring] = useState(false) // New recurring state
    const [isCalculatorOpen, setIsCalculatorOpen] = useState(false)
    const [calculatorTarget, setCalculatorTarget] = useState(null) // 'main' or split.id

    // Reset on Open / Populate for Edit
    useEffect(() => {
        if (isTransactionModalOpen) {
            setIsSubmitting(false)
            if (editingTransaction) {
                // POPULATE FOR EDIT
                setType(editingTransaction.type)
                setAmount(editingTransaction.amount !== undefined && editingTransaction.amount !== null ? editingTransaction.amount.toString() : '')
                setWalletId(editingTransaction.walletId ? Number(editingTransaction.walletId) : '')
                setToWalletId(editingTransaction.toWalletId ? Number(editingTransaction.toWalletId) : '')

                // Set Category (Parent or Child)
                const currentCatId = editingTransaction.categoryId ? Number(editingTransaction.categoryId) : null
                setCategoryId(currentCatId)
                const category = allCategories?.find(c => c.id === editingTransaction.categoryId)
                if (category?.parentId) {
                    setSelectedParentId(category.parentId)
                } else {
                    setSelectedParentId(null)
                }

                setDescription(editingTransaction.description || '')
                setTagsInput(editingTransaction.tags ? editingTransaction.tags.join(' ') : '')
                setEmotion(editingTransaction.emotion || null)

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
                setType(newTransactionType || 'expense') // Use context-aware default
                setAmount('')
                setCategoryId(null)
                setSelectedParentId(null)
                setToWalletId('')
                setDescription('')
                setTagsInput('')
                setEmotion(null)
                setIsRecurring(false)
                setIsSplitMode(false)
                setSplits([{ id: 1, categoryId: null, amount: '' }, { id: 2, categoryId: null, amount: '' }])

                const now = new Date()
                now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
                setDatetime(now.toISOString().slice(0, 16))

                if (wallets && wallets.length > 0 && !walletId) {
                    setWalletId(wallets[0].id)
                }
            }
        }
    }, [isTransactionModalOpen, editingTransaction, wallets, allCategories, newTransactionType])

    const existingTags = useLiveQuery(async () => {
        const all = await db.tags.toArray()
        return all.sort((a, b) => a.name.localeCompare(b.name))
    })

    const handleTagClick = (tagName) => {
        const current = tagsInput.split(' ').filter(t => t)
        if (current.includes(tagName)) {
            setTagsInput(current.filter(t => t !== tagName).join(' '))
        } else {
            setTagsInput([...current, tagName].join(' '))
        }
    }

    const handleSubmit = async () => {
        if (isSubmittingRef.current) return

        // Explicit validation
        if (!amount) {
            addToast(t('validation_amount'), 'error')
            return
        }
        if (!walletId) {
            addToast(t('validation_wallet'), 'error')
            return
        }
        if (type === 'transfer' && !toWalletId) {
            addToast(t('select_destination'), 'error')
            return
        }

        const value = parseFloat(amount)
        if (isNaN(value)) {
            addToast(t('validation_amount_invalid'), 'error')
            return
        }

        // Validate Split Logic if active
        if (isSplitMode) {
            const totalSplits = splits.reduce((sum, s) => sum + (parseFloat(s.amount) || 0), 0)
            if (Math.abs(totalSplits - value) > 0.01) {
                addToast(`La suma del desglose (${totalSplits}) no coincide con el total (${value})`, 'error')
                return
            }
            if (splits.some(s => !s.categoryId)) {
                addToast(t('validation_category'), 'error')
                return
            }
        } else {
            if (!categoryId) {
                addToast(t('validation_category'), 'error')
                return
            }
        }

        const tags = tagsInput.split(/[\s,]+/).filter(t => t).map(t => t.startsWith('#') ? t : `#${t}`)
        const txDate = new Date(datetime)

        if (isNaN(txDate.getTime())) {
            addToast(t('validation_date_invalid'), 'error')
            return
        }

        setIsSubmitting(true)

        try {
            await db.transaction('rw', db.transactions, db.wallets, db.recurring, async () => {

                // IF EDITING: Revert old transaction effects first
                if (editingTransaction) {
                    // Revert Source Wallet
                    if (editingTransaction.walletId) {
                        const wallet = await db.wallets.get(Number(editingTransaction.walletId))
                        if (wallet) {
                            const revertAmount = editingTransaction.type === 'income' ? -editingTransaction.amount : editingTransaction.amount
                            await db.wallets.update(wallet.id, { balance: wallet.balance + revertAmount })
                        }
                    }
                    // Revert Destination Wallet (if it was a transfer)
                    if (editingTransaction.type === 'transfer' && editingTransaction.toWalletId) {
                        const toWallet = await db.wallets.get(Number(editingTransaction.toWalletId))
                        if (toWallet) {
                            await db.wallets.update(toWallet.id, { balance: toWallet.balance - editingTransaction.amount })
                        }
                    }

                    // Update the transaction record
                    await db.transactions.update(Number(editingTransaction.id), {
                        walletId: Number(walletId),
                        toWalletId: type === 'transfer' ? Number(toWalletId) : null,
                        categoryId: categoryId ? Number(categoryId) : null,
                        amount: value,
                        type,
                        description: description || '',
                        tags,
                        date: txDate,
                        emotion: emotion || null,
                    })
                } else {
                    // NEW TRANSACTION
                    if (isSplitMode) {
                        for (const split of splits) {
                            const splitValue = parseFloat(split.amount)
                            await db.transactions.add({
                                walletId: Number(walletId),
                                toWalletId: null, // Splits are usually expenses/income
                                categoryId: split.categoryId ? Number(split.categoryId) : null,
                                amount: splitValue,
                                type,
                                description: description ? `${description} (Split)` : '(Split)',
                                tags,
                                date: txDate,
                                emotion: emotion || null,
                            })
                        }
                    } else {
                        await db.transactions.add({
                            walletId: Number(walletId),
                            toWalletId: type === 'transfer' ? Number(toWalletId) : null,
                            categoryId: categoryId ? Number(categoryId) : null,
                            amount: value,
                            type,
                            description: description || '',
                            tags,
                            date: txDate,
                            emotion: emotion || null,
                        })
                    }
                }

                // Apply NEW effects
                if (type === 'transfer') {
                    const src = await db.wallets.get(Number(walletId))
                    if (src) await db.wallets.update(src.id, { balance: src.balance - value })
                    const dest = await db.wallets.get(Number(toWalletId))
                    if (dest) await db.wallets.update(dest.id, { balance: dest.balance + value })
                } else {
                    const targetWallet = await db.wallets.get(Number(walletId))
                    if (targetWallet) {
                        const applyAmount = type === 'income' ? value : -value
                        await db.wallets.update(targetWallet.id, { balance: targetWallet.balance + applyAmount })
                    }
                }

                // Handle Recurring Creation
                if (isRecurring && !isSplitMode) {
                    await db.recurring.add({
                        type,
                        amount: value,
                        dayOfMonth: txDate.getDate(),
                        walletId: Number(walletId),
                        categoryId: categoryId ? Number(categoryId) : null,
                        description: description || tCategory(allCategories?.find(c => c.id === Number(categoryId))?.name),
                        active: true,
                        lastRun: txDate
                        // Logic in RecurringManager usually creates it active. 
                        // If we create a transaction NOW, we might not want to duplicate it immediately if the recurring runner runs.
                        // But for simplicity, let's just add it. The recurring runner usually checks 'lastRun'.
                        // For this feature "Make Recurring", it implies "Also make this a recurring pattern".
                    })
                    addToast(t('recurring_added'), 'success')
                }
            })

            closeTransactionModal()
        } catch (error) {
            console.error("Failed to save transaction:", error)
            addToast(`${t('error_saving')}: ${error.message}`, 'error')
            setIsSubmitting(false)
        }
    }

    // Delete Confirmation State
    const [isDeleteConfirmOpen, setIsDeleteConfirmOpen] = useState(false)

    const handleDelete = () => {
        if (!editingTransaction) return
        setIsDeleteConfirmOpen(true)
    }

    const confirmDelete = async () => {
        if (!editingTransaction) return

        try {
            await db.transaction('rw', db.transactions, db.wallets, async () => {
                // 1. Revert Wallet Balances
                if (editingTransaction.walletId) {
                    const wallet = await db.wallets.get(Number(editingTransaction.walletId))
                    if (wallet) {
                        const revertAmount = editingTransaction.type === 'income' ? -editingTransaction.amount : editingTransaction.amount
                        await db.wallets.update(wallet.id, { balance: wallet.balance + revertAmount })
                    }
                }
                // Revert Destination Wallet if it was a transfer
                if (editingTransaction.type === 'transfer' && editingTransaction.toWalletId) {
                    const toWallet = await db.wallets.get(Number(editingTransaction.toWalletId))
                    if (toWallet) {
                        await db.wallets.update(toWallet.id, { balance: toWallet.balance - editingTransaction.amount })
                    }
                }

                // 2. Delete Transaction
                await db.transactions.delete(Number(editingTransaction.id))
            })

            addToast(t('transaction_deleted'), 'success')
            closeTransactionModal()
        } catch (error) {
            console.error("Failed to delete transaction:", error)
            addToast(`${t('error_deleting')}: ${error.message}`, 'error')
        } finally {
            setIsDeleteConfirmOpen(false)
        }
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

                    <div className="flex gap-2 p-1 bg-slate-800/50 rounded-xl">
                        <button
                            onClick={() => { setType('expense'); setCategoryId(null); setSelectedParentId(null); }}
                            className={cn("flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all", type === 'expense' ? "bg-rose-500 text-white shadow-lg shadow-rose-500/20" : "text-slate-400 hover:text-slate-200")}
                        >{t('expense')}</button>
                        <button
                            onClick={() => { setType('income'); setCategoryId(null); setSelectedParentId(null); }}
                            className={cn("flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all", type === 'income' ? "bg-emerald-500 text-white shadow-lg shadow-emerald-500/20" : "text-slate-400 hover:text-slate-200")}
                        >{t('income')}</button>
                        <button
                            onClick={() => { setType('transfer'); setCategoryId(null); setSelectedParentId(null); setIsSplitMode(false); }}
                            className={cn("flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all", type === 'transfer' ? "bg-sky-500 text-white shadow-lg shadow-sky-500/20" : "text-slate-400 hover:text-slate-200")}
                        >{t('transfer')}</button>
                    </div>

                    {!editingTransaction && type !== 'transfer' && (
                        <div className="flex items-center justify-between px-2">
                            <span className="text-xs text-slate-500 font-medium uppercase tracking-wider">Modo Desglose</span>
                            <button
                                onClick={() => setIsSplitMode(!isSplitMode)}
                                className={cn("flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full border transition-all", isSplitMode ? "bg-sky-500/20 border-sky-500 text-sky-400" : "bg-slate-800 border-slate-700 text-slate-500 hover:border-slate-500")}
                            >
                                <Split className="w-3 h-3" />
                                {isSplitMode ? 'Activado' : 'Dividir'}
                            </button>
                        </div>
                    )}
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
                                className="w-full bg-slate-950 border border-slate-800 rounded-2xl py-4 pl-12 pr-16 text-3xl font-bold text-slate-100 placeholder:text-slate-700 focus:outline-none focus:border-sky-500 transition-all"
                            />
                            <button
                                type="button"
                                onClick={() => { setCalculatorTarget('main'); setIsCalculatorOpen(true); }}
                                className="absolute right-3 top-1/2 -translate-y-1/2 p-2.5 text-slate-500 hover:text-sky-400 bg-slate-900 rounded-xl hover:bg-slate-800 transition-colors shadow-sm"
                            >
                                <LucideIcons.Calculator className="w-6 h-6" />
                            </button>
                        </div>

                        <div className={cn("grid gap-3", type === 'transfer' ? "grid-cols-1" : "grid-cols-2")}>
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

                            {/* Wallet Selection */}
                            {type !== 'transfer' ? (
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
                            ) : (
                                <div className="space-y-3 animate-in fade-in slide-in-from-top-2 duration-300">
                                    <div className="grid grid-cols-[1fr,auto,1fr] items-center gap-2">
                                        <div className="relative">
                                            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"><Wallet className="w-4 h-4" /></span>
                                            <select
                                                value={walletId}
                                                onChange={(e) => setWalletId(parseInt(e.target.value))}
                                                className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-9 pr-8 text-xs text-slate-200 focus:outline-none focus:border-sky-500 appearance-none"
                                            >
                                                <option value="" disabled>{t('wallet_source')}</option>
                                                {wallets?.map(w => (
                                                    <option key={w.id} value={w.id}>{w.name}</option>
                                                ))}
                                            </select>
                                        </div>
                                        <ArrowRightLeft className="w-4 h-4 text-sky-500" />
                                        <div className="relative">
                                            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"><Wallet className="w-4 h-4" /></span>
                                            <select
                                                value={toWalletId}
                                                onChange={(e) => setToWalletId(parseInt(e.target.value))}
                                                className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-9 pr-8 text-xs text-slate-200 focus:outline-none focus:border-sky-500 appearance-none"
                                            >
                                                <option value="" disabled>{t('wallet_destination')}</option>
                                                {wallets?.filter(w => w.id !== walletId).map(w => (
                                                    <option key={w.id} value={w.id}>{w.name}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* 2. Category Selection (Integrated or Split or Hidden for Transfer) */}
                    {type !== 'transfer' && (
                        <div className="space-y-3">
                            <label className="text-xs font-medium text-slate-500 uppercase tracking-wider block">{t('category')}</label>

                        {isSplitMode ? (
                            <div className="space-y-3 animate-in fade-in slide-in-from-top-2 duration-300">
                                {splits.map((split, index) => (
                                    <div key={split.id} className="flex gap-2 items-center">
                                        {/* Category Selector for Split Item */}
                                        <div className="flex-1 relative">
                                            <select
                                                value={split.categoryId || ''}
                                                onChange={(e) => {
                                                    const newSplits = [...splits]
                                                    newSplits[index].categoryId = e.target.value ? parseInt(e.target.value) : null
                                                    setSplits(newSplits)
                                                }}
                                                className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-2 pr-8 text-xs text-slate-200 focus:outline-none focus:border-sky-500 appearance-none"
                                            >
                                                <option value="">Seleccionar Categoría...</option>
                                                {allCategories?.filter(c => c.type === type).map(c => (
                                                    <option key={c.id} value={c.id}>
                                                        {tCategory(c.name)}
                                                    </option>
                                                ))}
                                            </select>
                                            <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 w-3 h-3 text-slate-500 pointer-events-none" />
                                        </div>

                                        {/* Amount Input for Split Item */}
                                        <div className="w-[120px] relative">
                                            <span className="absolute left-2 top-1/2 -translate-y-1/2 text-xs text-slate-500">{symbol}</span>
                                            <input
                                                type="number"
                                                value={split.amount}
                                                onChange={(e) => {
                                                    const newSplits = [...splits]
                                                    newSplits[index].amount = e.target.value
                                                    setSplits(newSplits)
                                                }}
                                                placeholder="0.00"
                                                className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-6 pr-8 text-xs text-slate-200 focus:outline-none focus:border-sky-500 font-mono"
                                            />
                                            <button
                                                type="button"
                                                onClick={() => { setCalculatorTarget('split-' + split.id); setIsCalculatorOpen(true); }}
                                                className="absolute right-1.5 top-1/2 -translate-y-1/2 p-1 text-slate-500 hover:text-sky-400 hover:bg-slate-800 rounded-md transition-colors"
                                            >
                                                <LucideIcons.Calculator className="w-3.5 h-3.5" />
                                            </button>
                                        </div>

                                        {/* Remove Button */}
                                        <button
                                            onClick={() => {
                                                if (splits.length > 2) {
                                                    const newSplits = splits.filter((_, i) => i !== index)
                                                    setSplits(newSplits)
                                                }
                                            }}
                                            disabled={splits.length <= 2}
                                            className="text-slate-500 hover:text-rose-500 disabled:opacity-30 disabled:hover:text-slate-500"
                                        >
                                            <MinusCircle className="w-5 h-5" />
                                        </button>
                                    </div>
                                ))}

                                <div className="flex justify-between items-center pt-2">
                                    <div className="text-xs text-slate-500">
                                        Total: <span className={cn("font-bold",
                                            Math.abs(splits.reduce((acc, s) => acc + (parseFloat(s.amount) || 0), 0) - (parseFloat(amount) || 0)) < 0.01
                                                ? (type === 'income' ? "text-emerald-500" : "text-rose-500")
                                                : "text-amber-500"
                                        )}>
                                            {symbol}{splits.reduce((acc, s) => acc + (parseFloat(s.amount) || 0), 0).toFixed(2)}
                                        </span>
                                        {' / '}{symbol}{parseFloat(amount || 0).toFixed(2)}
                                    </div>
                                    <button
                                        onClick={() => setSplits([...splits, { id: Date.now(), categoryId: null, amount: '' }])}
                                        className="flex items-center gap-1 text-xs text-sky-400 hover:text-sky-300 font-medium"
                                    >
                                        <PlusCircle className="w-4 h-4" /> Agregar línea
                                    </button>
                                </div>
                            </div>
                        ) : (
                            /* Classic Category Selection */ // Wrapped explicitly to separate branches
                            <>
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
                                            <div className="grid grid-cols-3 gap-3 sm:gap-4 sm:grid-cols-4">
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
                                                            <div className="w-14 h-14 rounded-full bg-slate-800 flex items-center justify-center text-slate-400" style={{ color: cat.color }}>
                                                                <Icon className="w-7 h-7" />
                                                            </div>
                                                            <span className="text-xs text-slate-400 truncate w-full text-center">{tCategory(cat.name)}</span>
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
                            </>
                        )}
                        </div>
                    )}

                    {/* 3. Optional Details */}
                    <div className="space-y-4 pt-2 border-t border-slate-800">

                        {/* Recurrence Toggle (Not available for split transactions) */}
                        {!isSplitMode && (
                            <div className="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
                                <div className="flex items-center gap-3">
                                    <div className={cn("w-8 h-8 rounded-full flex items-center justify-center transition-colors", isRecurring ? "bg-sky-500 text-white" : "bg-slate-800 text-slate-500")}>
                                        <Repeat className="w-4 h-4" />
                                    </div>
                                    <div className="flex flex-col">
                                        <span className={cn("text-sm font-medium transition-colors", isRecurring ? "text-sky-400" : "text-slate-300")}>
                                            {t('make_recurring')}
                                        </span>
                                        <span className="text-[10px] text-slate-500">
                                            {t(type === 'income' ? 'make_recurring_desc_income' : 'make_recurring_desc_expense')}
                                        </span>
                                    </div>
                                </div>
                                <button
                                    onClick={() => setIsRecurring(!isRecurring)}
                                    className={cn(
                                        "w-12 h-6 rounded-full transition-colors relative",
                                        isRecurring ? "bg-sky-500" : "bg-slate-700"
                                    )}
                                >
                                    <div className={cn(
                                        "absolute top-1 w-4 h-4 rounded-full bg-white transition-all shadow-sm",
                                        isRecurring ? "left-7" : "left-1"
                                    )} />
                                </button>
                            </div>
                        )}

                        {/* Emotion Selector */}
                        <div className="space-y-2">
                            <label className="text-xs font-medium text-slate-500 uppercase tracking-wider block flex items-center gap-2">
                                <Smile className="w-3 h-3" /> Estado de Ánimo
                            </label>
                            <div className="flex justify-between bg-slate-950 p-2 rounded-xl border border-slate-800">
                                {['😍', '🙂', '😐', '😰', '😠'].map((emoji) => (
                                    <button
                                        key={emoji}
                                        onClick={() => setEmotion(emotion === emoji ? null : emoji)}
                                        className={cn(
                                            "w-10 h-10 flex items-center justify-center text-xl rounded-full transition-all",
                                            emotion === emoji
                                                ? "bg-sky-500/20 scale-110 shadow-lg shadow-sky-500/10 border border-sky-500/50"
                                                : "hover:bg-slate-800 opacity-50 hover:opacity-100 grayscale hover:grayscale-0"
                                        )}
                                    >
                                        {emoji}
                                    </button>
                                ))}
                            </div>
                        </div>

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
                                                "text-sm px-3 py-2 rounded-full border transition-all font-bold",
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
                        variant={type === 'expense' ? 'danger' : (type === 'transfer' ? 'sky' : 'default')}
                        // Allow saving if amount is present. Category check happens inside handleSubmit depending on split mode
                        disabled={!amount || isSubmitting}
                    >
                        {isSubmitting ? 'Guardando...' : (editingTransaction ? t('update') : `${t('save')} ${type === 'expense' ? t('expense') : (type === 'income' ? t('income') : t('transfer'))}`)}
                    </Button>
                </div>

            </Card>

            <ConfirmDialog
                isOpen={isDeleteConfirmOpen}
                onClose={() => setIsDeleteConfirmOpen(false)}
                onConfirm={confirmDelete}
                title={t('confirm_delete_transaction')}
                message={t('confirm_delete_transaction_desc') || "¿Estás seguro de que quieres eliminar esta transacción? Esta acción no se puede deshacer y el saldo de la cuenta se actualizará."}
                type="danger"
            />

            <CalculatorModal
                isOpen={isCalculatorOpen}
                onClose={() => setIsCalculatorOpen(false)}
                initialValue={calculatorTarget === 'main' ? amount : (calculatorTarget?.startsWith('split-') ? splits.find(s => s.id === Number(calculatorTarget.replace('split-', '')))?.amount : '0')}
                onConfirm={(val) => {
                    if (calculatorTarget === 'main') {
                        setAmount(val)
                    } else if (calculatorTarget?.startsWith('split-')) {
                        const id = Number(calculatorTarget.replace('split-', ''))
                        setSplits(splits.map(s => s.id === id ? { ...s, amount: val } : s))
                    }
                    setIsCalculatorOpen(false)
                }}
            />
        </div>
    )
}

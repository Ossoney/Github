import { useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Button, Card, CardContent, CardHeader, CardTitle, Input, Modal, IconSelector, useToast, ConfirmDialog } from '@/components/ui/UI'
import { LayoutGrid, Plus, Trash2, Edit2, ChevronDown, ChevronRight, FolderPlus, AlertTriangle, ChevronsRight } from 'lucide-react'
import * as LucideIcons from 'lucide-react'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

// Tailwind Colors for presets
const COLOR_PRESETS = [
    '#ef4444', '#f97316', '#f59e0b', '#84cc16', '#22c55e', '#10b981',
    '#14b8a6', '#06b6d4', '#0ea5e9', '#3b82f6', '#6366f1', '#8b5cf6',
    '#d946ef', '#ec4899', '#f43f5e', '#64748b'
]

export function CategoryManager() {
    const data = useLiveQuery(async () => {
        const categories = await db.categories.toArray()
        const transactions = await db.transactions.toArray()

        // Precompute counts
        const counts = {}
        transactions.forEach(tx => {
            counts[tx.categoryId] = (counts[tx.categoryId] || 0) + 1
        })

        return { categories, counts }
    })

    const allCategories = data?.categories || []
    const transactionCounts = data?.counts || {}
    const { addToast } = useToast()
    const { t, tCategory, language } = useLanguage()

    const [activeType, setActiveType] = useState('expense') // 'expense' | 'income'
    const [expandedParents, setExpandedParents] = useState({}) // { parentId: boolean }

    // Create/Edit State
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [modalMode, setModalMode] = useState('create') // 'create' | 'edit'
    const [categoryType, setCategoryType] = useState('parent') // 'parent' | 'child'

    const [editingId, setEditingId] = useState(null)
    const [targetParentId, setTargetParentId] = useState(null) // If creating child

    const [newName, setNewName] = useState('')
    const [newIcon, setNewIcon] = useState('Circle') // Default Icon
    const [newColor, setNewColor] = useState('#3b82f6') // Default Blue

    // Confirm Delete - with migration support
    const [deleteTarget, setDeleteTarget] = useState(null) // { id, name, isParent }
    const [migrateTo, setMigrateTo] = useState('')        // categoryId to migrate to
    const [txCount, setTxCount] = useState(0)
    const [deleteStep, setDeleteStep] = useState(1)       // 1 = choose action, 2 = pick target
    const [expandedPickerParents, setExpandedPickerParents] = useState(new Set())

    // Filter by Type
    const parents = (allCategories?.filter(c => c.type === activeType && !c.parentId) || [])
        .sort((a, b) => tCategory(a.name).localeCompare(tCategory(b.name), language))

    const toggleExpand = (id) => {
        setExpandedParents(prev => ({ ...prev, [id]: !prev[id] }))
    }

    const openCreateParent = () => {
        setModalMode('create')
        setCategoryType('parent')
        setEditingId(null)
        setTargetParentId(null)
        setNewName('')
        setNewIcon('Circle')
        setNewColor('#3b82f6')
        setIsModalOpen(true)
    }

    const openCreateChild = (parentId, parentColor) => {
        setModalMode('create')
        setCategoryType('child')
        setEditingId(null)
        setTargetParentId(parentId)
        setNewName('')
        setNewIcon('Circle')
        setNewColor(parentColor) // Inherit parent color by default
        setIsModalOpen(true)
    }

    const openEdit = (category) => {
        setModalMode('edit')
        setCategoryType(category.parentId ? 'child' : 'parent')
        setEditingId(category.id)
        setTargetParentId(category.parentId || null)
        setNewName(category.name)
        setNewIcon(category.icon)
        setNewColor(category.color)
        setIsModalOpen(true)
    }

    const handleSave = async () => {
        if (!newName) {
            addToast(t('validation_category'), 'error')
            return
        }

        try {
            if (modalMode === 'edit' && editingId) {
                // UPDATE existing
                await db.categories.update(editingId, {
                    name: newName,
                    icon: newIcon,
                    color: newColor,
                })
                addToast(t('save'), 'success')
            } else {
                // CREATE new
                await db.categories.add({
                    name: newName,
                    type: activeType,
                    icon: newIcon,
                    color: newColor,
                    parentId: targetParentId
                })
                addToast(t('save'), 'success')
            }
            setIsModalOpen(false)
        } catch (err) {
            console.error("Error creating/updating category", err)
            addToast(t('error_saving'), 'error')
        }
    }

    const handleDeleteClick = async (category) => {
        const isParent = !category.parentId
        let idsToCheck = [category.id]
        if (isParent) {
            const children = allCategories.filter(c => c.parentId === category.id)
            idsToCheck = [category.id, ...children.map(c => c.id)]
        }
        const count = await db.transactions.where('categoryId').anyOf(idsToCheck).count()
        const parentName = !isParent
            ? allCategories.find(c => c.id === category.parentId)?.name || null
            : null
        setTxCount(count)
        setMigrateTo('')
        setDeleteStep(1)
        setDeleteTarget({ id: category.id, name: category.name, isParent, parentName })
    }

    const handleDelete = async (deleteTransactions = true) => {
        if (!deleteTarget) return
        try {
            const isParent = deleteTarget.isParent
            const children = isParent ? allCategories.filter(c => c.parentId === deleteTarget.id) : []
            const idsToDelete = [deleteTarget.id, ...children.map(c => c.id)]

            if (!deleteTransactions && migrateTo) {
                // Migrate transactions to the target category
                await db.transactions
                    .where('categoryId')
                    .anyOf(idsToDelete)
                    .modify({ categoryId: Number(migrateTo) })
            } else {
                // Delete the transactions
                const txToDelete = await db.transactions.where('categoryId').anyOf(idsToDelete).primaryKeys()
                await db.transactions.bulkDelete(txToDelete)
            }

            await db.categories.bulkDelete(idsToDelete)
            addToast(t('delete'), 'success')
            setDeleteTarget(null)
        } catch (err) {
            console.error("Error deleting category", err)
            addToast(t('error_deleting'), 'error')
        }
    }

    // Modal Title Helper
    const getModalTitle = () => {
        if (modalMode === 'edit') return t('edit')
        return categoryType === 'parent' ? t('new_category_parent') : t('new_category_child')
    }

    return (
        <>
            <Card className="border-slate-800 bg-slate-900/50">
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="text-lg text-slate-200 flex items-center gap-2">
                        <LayoutGrid className="w-5 h-5 text-sky-500" /> {t('categories')}
                    </CardTitle>
                    <div className="flex bg-slate-950 rounded-lg p-1 border border-slate-800">
                        <button
                            onClick={() => setActiveType('expense')}
                            className={cn("px-3 py-1 rounded text-sm transition-colors", activeType === 'expense' ? "bg-rose-500/20 text-rose-400 font-medium" : "text-slate-400 hover:text-slate-200")}
                        >{t('expense')}</button>
                        <button
                            onClick={() => setActiveType('income')}
                            className={cn("px-3 py-1 rounded text-sm transition-colors", activeType === 'income' ? "bg-emerald-500/20 text-emerald-400 font-medium" : "text-slate-400 hover:text-slate-200")}
                        >{t('income')}</button>
                    </div>
                </CardHeader>
                <CardContent className="space-y-4">

                    <Button
                        variant="outline"
                        className="w-full border-dashed border-slate-700 hover:bg-slate-800"
                        onClick={openCreateParent}
                    >
                        <Plus className="w-4 h-4 mr-2" /> {t('new_category_parent')}
                    </Button>

                    <div className="space-y-2">
                        {parents.map(parent => {
                            const children = (allCategories?.filter(c => c.parentId === parent.id) || [])
                                .sort((a, b) => tCategory(a.name).localeCompare(tCategory(b.name), language))
                            const isExpanded = expandedParents[parent.id]
                            const Icon = LucideIcons[parent.icon] || LucideIcons.Circle

                            return (
                                <div key={parent.id} className="border border-slate-800 rounded-xl overflow-hidden">
                                    {/* Parent Row */}
                                    <div className="flex items-center justify-between p-3 bg-slate-800/30 hover:bg-slate-800/50 transition-colors">
                                        <div
                                            className="flex items-center gap-3 flex-1 cursor-pointer"
                                            onClick={() => toggleExpand(parent.id)}
                                        >
                                            {children.length > 0 ? (
                                                isExpanded ? <ChevronDown className="w-4 h-4 text-slate-500" /> : <ChevronRight className="w-4 h-4 text-slate-500" />
                                            ) : <div className="w-4" />}

                                            <div className="w-8 h-8 rounded-full flex items-center justify-center bg-slate-800 border border-slate-700" style={{ borderColor: `${parent.color}50` }}>
                                                <Icon className="w-4 h-4" style={{ color: parent.color }} />
                                            </div>
                                            <span className="font-medium text-slate-200">{tCategory(parent.name)}</span>
                                            {transactionCounts[parent.id] > 0 && (
                                                <span className="text-[10px] bg-slate-700 text-slate-400 px-1.5 py-0.5 rounded-full font-bold">
                                                    {transactionCounts[parent.id]}
                                                </span>
                                            )}
                                        </div>

                                        <div className="flex items-center gap-1">
                                            <Button
                                                size="icon"
                                                variant="ghost"
                                                className="h-8 w-8 text-slate-400 hover:text-sky-400"
                                                onClick={() => openEdit(parent)}
                                                title={t('edit')}
                                            >
                                                <Edit2 className="w-4 h-4" />
                                            </Button>
                                            <Button
                                                size="icon"
                                                variant="ghost"
                                                className="h-8 w-8 text-slate-400 hover:text-emerald-400"
                                                onClick={() => openCreateChild(parent.id, parent.color)}
                                                title={t('add_subcategory')}
                                            >
                                                <FolderPlus className="w-4 h-4" />
                                            </Button>
                                            <Button
                                                size="icon"
                                                variant="ghost"
                                                className="h-8 w-8 text-slate-400 hover:text-rose-400"
                                                onClick={() => handleDeleteClick(parent)}
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    </div>

                                    {/* Children Rows */}
                                    {isExpanded && children.length > 0 && (
                                        <div className="bg-slate-950/30 border-t border-slate-800/50">
                                            {children.map(child => {
                                                const ChildIcon = LucideIcons[child.icon] || LucideIcons.Circle
                                                return (
                                                    <div key={child.id} className="flex items-center justify-between p-2 pl-12 pr-3 hover:bg-slate-800/20">
                                                        <div className="flex items-center gap-2">
                                                            <ChildIcon className="w-3.5 h-3.5 text-slate-500" />
                                                            <span className="text-sm text-slate-400">{tCategory(child.name)}</span>
                                                            {transactionCounts[child.id] > 0 && (
                                                                <span className="text-[10px] text-slate-600 font-bold">
                                                                    ({transactionCounts[child.id]})
                                                                </span>
                                                            )}
                                                        </div>
                                                        <div className="flex items-center">
                                                            <Button
                                                                size="icon"
                                                                variant="ghost"
                                                                className="h-6 w-6 text-slate-500 hover:text-sky-400"
                                                                onClick={() => openEdit(child)}
                                                            >
                                                                <Edit2 className="w-3 h-3" />
                                                            </Button>
                                                            <Button
                                                                size="icon"
                                                                variant="ghost"
                                                                className="h-6 w-6 text-slate-500 hover:text-rose-400"
                                                                onClick={() => handleDeleteClick(child)}
                                                            >
                                                                <Trash2 className="w-3 h-3" />
                                                            </Button>
                                                        </div>
                                                    </div>
                                                )
                                            })}
                                        </div>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </CardContent>
            </Card>

            {/* EDIT/CREATE MODAL */}
            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={getModalTitle()}
                className="max-w-md"
            >
                <div className="space-y-6">
                    {/* Name */}
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-slate-400 uppercase">{t('category_name')}</label>
                        <Input
                            placeholder={t('category_name')}
                            value={newName}
                            onChange={(e) => setNewName(e.target.value)}
                            className="bg-slate-950"
                        />
                    </div>

                    {/* Color Picker */}
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-slate-400 uppercase">{t('color')}</label>
                        <div className="flex flex-wrap gap-2">
                            {COLOR_PRESETS.map(color => (
                                <button
                                    key={color}
                                    onClick={() => setNewColor(color)}
                                    className={cn(
                                        "w-8 h-8 rounded-full border-2 transition-transform hover:scale-110",
                                        newColor === color ? "border-white scale-110" : "border-transparent"
                                    )}
                                    style={{ backgroundColor: color }}
                                />
                            ))}
                            {/* Custom Color Input */}
                            <div className="relative w-8 h-8 rounded-full overflow-hidden border-2 border-slate-700 hover:border-slate-500 transition-colors">
                                <input
                                    type="color"
                                    value={newColor}
                                    onChange={(e) => setNewColor(e.target.value)}
                                    className="absolute -top-2 -left-2 w-12 h-12 cursor-pointer p-0 border-0"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Icon Picker */}
                    <div className="space-y-2">
                        <label className="text-xs font-medium text-slate-400 uppercase">{t('icon')}</label>
                        <IconSelector
                            selectedIcon={newIcon}
                            onSelect={setNewIcon}
                            color={newColor}
                        />
                    </div>

                    <div className="pt-4 flex gap-3">
                        <Button
                            variant="ghost"
                            className="flex-1"
                            onClick={() => setIsModalOpen(false)}
                        >
                            {t('cancel')}
                        </Button>
                        <Button
                            className="flex-1 bg-sky-600 hover:bg-sky-700"
                            onClick={handleSave}
                        >
                            {t('save')}
                        </Button>
                    </div>
                </div>
            </Modal>

            {/* DELETE WITH MIGRATION DIALOG */}
            <Modal
                isOpen={!!deleteTarget}
                onClose={() => setDeleteTarget(null)}
                title={t('delete')}
                className="max-w-md"
            >
                <div className="space-y-4">
                    {/* Category name / breadcrumb */}
                    <div className="px-1">
                        <p className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-2">
                            {deleteTarget?.isParent ? 'Categor\u00eda a eliminar' : 'Subcategor\u00eda a eliminar'}
                        </p>
                        <p className="text-lg font-bold text-slate-100">
                            {deleteTarget?.parentName
                                ? <>{deleteTarget.parentName} <span className="text-slate-500">›</span> {deleteTarget.name}</>
                                : deleteTarget?.name
                            }
                        </p>
                        {txCount > 0 && (
                            <p className="text-xs text-amber-400 mt-1">
                                {txCount} movimiento{txCount !== 1 ? 's' : ''} vinculado{txCount !== 1 ? 's' : ''}
                            </p>
                        )}
                    </div>

                    {/* STEP 1: action buttons */}
                    {deleteStep === 1 && (
                        <div className="flex gap-2 pt-1">
                            <Button variant="ghost" className="flex-1" onClick={() => setDeleteTarget(null)}>
                                {t('cancel')}
                            </Button>
                            {txCount > 0 && (
                                <Button
                                    variant="outline"
                                    className="flex-1 border-sky-700 text-sky-400 hover:bg-sky-900/30"
                                    onClick={() => {
                                        setExpandedPickerParents(new Set())
                                        setDeleteStep(2)
                                    }}
                                >
                                    <ChevronsRight className="w-4 h-4 mr-1" /> Mover
                                </Button>
                            )}
                            <Button
                                className="flex-1 bg-rose-600 hover:bg-rose-700 text-white"
                                onClick={() => handleDelete(true)}
                            >
                                <Trash2 className="w-4 h-4 mr-1" /> {t('delete')}
                            </Button>
                        </div>
                    )}

                    {/* STEP 2: collapsible category tree picker */}
                    {deleteStep === 2 && (() => {
                        const treeParents = allCategories.filter(c => !c.parentId && c.id !== deleteTarget?.id && c.type === activeType)
                        return (
                            <>
                                <label className="text-xs font-medium text-slate-400 uppercase block">{t('move_transactions')}</label>
                                <div className="max-h-56 overflow-y-auto space-y-1 pr-1">
                                    {treeParents.map(parent => {
                                        const children = allCategories.filter(c => c.parentId === parent.id && c.id !== deleteTarget?.id)
                                        const isExpanded = expandedPickerParents.has(parent.id)
                                        const isSelected = migrateTo === String(parent.id)
                                        return (
                                            <div key={parent.id}>
                                                <button
                                                    type="button"
                                                    onClick={() => {
                                                        if (children.length > 0) {
                                                            setExpandedPickerParents(prev => {
                                                                const next = new Set(prev)
                                                                next.has(parent.id) ? next.delete(parent.id) : next.add(parent.id)
                                                                return next
                                                            })
                                                        } else {
                                                            setMigrateTo(String(parent.id))
                                                        }
                                                    }}
                                                    className={cn(
                                                        'w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm text-left transition-colors',
                                                        isSelected
                                                            ? 'bg-sky-600 text-white'
                                                            : 'hover:bg-slate-800 text-slate-200'
                                                    )}
                                                >
                                                    <span className="font-medium">{parent.name}</span>
                                                    {children.length > 0 && (
                                                        isExpanded
                                                            ? <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                                                            : <ChevronRight className="w-4 h-4 text-slate-400 shrink-0" />
                                                    )}
                                                </button>
                                                {isExpanded && children.map(child => (
                                                    <button
                                                        key={child.id}
                                                        type="button"
                                                        onClick={() => setMigrateTo(String(child.id))}
                                                        className={cn(
                                                            'w-full flex items-center gap-2 px-3 py-1.5 ml-4 rounded-lg text-sm text-left transition-colors',
                                                            migrateTo === String(child.id)
                                                                ? 'bg-sky-600 text-white'
                                                                : 'hover:bg-slate-800 text-slate-400'
                                                        )}
                                                    >
                                                        <span className="text-slate-500">↳</span>{child.name}
                                                    </button>
                                                ))}
                                            </div>
                                        )
                                    })}
                                </div>
                                <div className="flex gap-2">
                                    <Button variant="ghost" className="flex-1" onClick={() => setDeleteStep(1)}>
                                        {t('back_to_categories')}
                                    </Button>
                                    <Button
                                        className="flex-1 bg-sky-600 hover:bg-sky-700 text-white"
                                        onClick={() => handleDelete(false)}
                                        disabled={!migrateTo}
                                    >
                                        <ChevronsRight className="w-4 h-4 mr-1" /> {t('move_and_delete')}
                                    </Button>
                                </div>
                            </>
                        )
                    })()}
                </div>
            </Modal>
        </>
    )
}

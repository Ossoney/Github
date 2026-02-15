import { useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Button, Card, CardContent, CardHeader, CardTitle, Input, Modal, IconSelector, useToast, ConfirmDialog } from '@/components/ui/UI'
import { LayoutGrid, Plus, Trash2, Edit2, ChevronDown, ChevronRight, FolderPlus } from 'lucide-react'
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
    const allCategories = useLiveQuery(() => db.categories.toArray())
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

    // Confirm Delete
    const [deleteId, setDeleteId] = useState(null)

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

    const handleDelete = async () => {
        if (!deleteId) return

        try {
            // Find children
            const children = allCategories.filter(c => c.parentId === deleteId)
            const idsToDelete = [deleteId, ...children.map(c => c.id)]
            await db.categories.bulkDelete(idsToDelete)
            addToast(t('delete'), 'success')
            setDeleteId(null)
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
                                                onClick={() => setDeleteId(parent.id)}
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
                                                                onClick={() => setDeleteId(child.id)}
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

            <ConfirmDialog
                isOpen={!!deleteId}
                onClose={() => setDeleteId(null)}
                onConfirm={handleDelete}
                title={t('delete')}
                message={t('confirm_delete_category')}
            />
        </>
    )
}

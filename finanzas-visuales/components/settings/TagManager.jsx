'use client'

import { useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { db } from '@/lib/db'
import { Button, Card, Input, ConfirmDialog } from '@/components/ui/UI'
import { Tag, Plus, Trash2 } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

export function TagManager() {
    const tags = useLiveQuery(async () => {
        const all = await db.tags.toArray()
        return all.sort((a, b) => a.name.localeCompare(b.name))
    })
    const { t } = useLanguage()
    const [newTag, setNewTag] = useState('')
    const [deleteId, setDeleteId] = useState(null)

    const handleCreate = async () => {
        if (!newTag.trim()) return
        const tagName = newTag.startsWith('#') ? newTag.trim() : `#${newTag.trim()} `

        // Prevent duplicates
        if (tags?.some(t => t.name.toLowerCase() === tagName.toLowerCase())) {
            setNewTag('')
            return
        }

        try {
            await db.tags.add({ name: tagName })
            setNewTag('')
        } catch (err) {
            console.error(err)
        }
    }

    const handleDelete = async () => {
        if (deleteId) {
            await db.tags.delete(deleteId)
            setDeleteId(null)
        }
    }

    return (
        <Card className="w-full bg-slate-900/50 border-slate-800 animate-in fade-in">
            {/* Header */}
            <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50 rounded-t-xl">
                <h2 className="text-lg font-bold text-slate-200 flex items-center gap-2">
                    <Tag className="w-5 h-5 text-sky-500" /> {t('manage_tags')}
                </h2>
            </div>

            <div className="p-4 space-y-6">
                {/* Add Input */}
                <div className="flex gap-2 max-w-md">
                    <Input
                        placeholder={t('new_tag_placeholder')}
                        value={newTag}
                        onChange={e => setNewTag(e.target.value)}
                        onKeyDown={e => e.key === 'Enter' && handleCreate()}
                        className="bg-slate-950 border-slate-800 focus:border-sky-500"
                    />
                    <Button onClick={handleCreate} className="bg-sky-500 hover:bg-sky-600">
                        <Plus className="w-4 h-4" />
                    </Button>
                </div>

                {/* Tag List */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 max-h-[400px] overflow-y-auto custom-scrollbar pr-1">
                    {tags?.length === 0 && (
                        <p className="col-span-full text-center text-xs text-slate-500 py-6 italic">{t('no_tags')}</p>
                    )}
                    {tags?.map(tag => (
                        <div key={tag.id} className="flex items-center justify-between p-4 rounded-xl bg-slate-800/40 hover:bg-slate-800 transition-colors group border border-slate-800 hover:border-slate-700">
                            <span className="font-bold text-lg text-slate-200">{tag.name}</span>
                            <button
                                onClick={() => setDeleteId(tag.id)}
                                className="p-1.5 text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
                            >
                                <Trash2 className="w-4 h-4" />
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            <ConfirmDialog
                isOpen={!!deleteId}
                onClose={() => setDeleteId(null)}
                onConfirm={handleDelete}
                title={t('delete')}
                message={t('confirm_delete_tag')}
            />
        </Card>
    )
}

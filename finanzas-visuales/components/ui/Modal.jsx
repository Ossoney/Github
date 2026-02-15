'use client'

import { X } from 'lucide-react'
import { cn } from '@/lib/utils'

export function Modal({ isOpen, onClose, title, children, className }) {
    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <div className={cn(
                "w-full max-w-lg bg-slate-900 border border-slate-800 shadow-2xl animate-in slide-in-from-bottom-10 duration-300 rounded-xl flex flex-col max-h-[90vh]",
                className
            )}>
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-slate-800 shrink-0">
                    <h2 className="text-lg font-bold text-slate-200">{title}</h2>
                    <button onClick={onClose} className="text-slate-500 hover:text-slate-300 transition-colors">
                        <X className="w-6 h-6" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-4 overflow-y-auto custom-scrollbar">
                    {children}
                </div>
            </div>
        </div>
    )
}

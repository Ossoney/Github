'use client'

import { createContext, useContext, useState, useCallback } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Check, AlertCircle, X, Info } from 'lucide-react'
import { cn } from '@/lib/utils'

const ToastContext = createContext(null)

export function ToastProvider({ children }) {
    const [toasts, setToasts] = useState([])

    const addToast = useCallback((message, type = 'success') => {
        const id = Math.random().toString(36).substring(2, 9)
        setToasts((prev) => [...prev, { id, message, type }])

        // Auto remove after 3 seconds
        setTimeout(() => {
            setToasts((prev) => prev.filter((t) => t.id !== id))
        }, 3000)
    }, [])

    const removeToast = useCallback((id) => {
        setToasts((prev) => prev.filter((t) => t.id !== id))
    }, [])

    return (
        <ToastContext.Provider value={{ addToast }}>
            {children}
            <div className="fixed bottom-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none">
                <AnimatePresence>
                    {toasts.map((toast) => (
                        <Toast key={toast.id} {...toast} onRemove={() => removeToast(toast.id)} />
                    ))}
                </AnimatePresence>
            </div>
        </ToastContext.Provider>
    )
}

function Toast({ message, type, onRemove }) {
    const icons = {
        success: <Check className="w-5 h-5 text-emerald-400" />,
        error: <AlertCircle className="w-5 h-5 text-rose-400" />,
        info: <Info className="w-5 h-5 text-sky-400" />
    }

    const styles = {
        success: "bg-slate-900/90 border-emerald-500/30 text-emerald-100",
        error: "bg-slate-900/90 border-rose-500/30 text-rose-100",
        info: "bg-slate-900/90 border-sky-500/30 text-sky-100"
    }

    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
            className={cn(
                "pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl border shadow-xl backdrop-blur-md min-w-[300px] max-w-md",
                styles[type]
            )}
        >
            <div className={`p-1.5 rounded-full bg-white/5`}>
                {icons[type]}
            </div>
            <p className="text-sm font-medium flex-1">{message}</p>
            <button onClick={onRemove} className="text-white/40 hover:text-white transition-colors">
                <X className="w-4 h-4" />
            </button>
        </motion.div>
    )
}

export const useToast = () => {
    const context = useContext(ToastContext)
    if (!context) {
        throw new Error('useToast must be used within a ToastProvider')
    }
    return context
}

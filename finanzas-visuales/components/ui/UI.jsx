'use client'

import React, { createContext, useContext, useState, useCallback, forwardRef } from 'react'
import { m, LazyMotion, AnimatePresence, domAnimation } from 'framer-motion'
import * as LucideIcons from 'lucide-react'
import dynamic from 'next/dynamic'
import dynamicIconImports from 'lucide-react/dynamicIconImports'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

// ----------------------------------------------------------------------
// BUTTON
// ----------------------------------------------------------------------
export const Button = forwardRef(({ className, variant = "default", size = "default", as: Component = "button", ...props }, ref) => {
    const variants = {
        default: "bg-sky-500 text-primary-foreground hover:bg-sky-600 shadow-lg shadow-sky-500/25",
        outline: "border border-slate-700 bg-transparent hover:bg-slate-800 text-slate-100",
        ghost: "hover:bg-slate-800 text-slate-300 hover:text-slate-100",
        danger: "bg-rose-500 text-rose-50 hover:bg-rose-600 shadow-lg shadow-rose-500/25",
        destructive: "bg-rose-500 text-rose-50 hover:bg-rose-600 shadow-lg shadow-rose-500/25", // Alias for ConfirmDialog compatibility
    }

    const sizes = {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        icon: "h-10 w-10",
    }

    return (
        <Component
            className={cn(
                "inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-400 disabled:pointer-events-none disabled:opacity-50",
                variants[variant] || variants.default,
                sizes[size],
                className
            )}
            ref={ref}
            {...props}
        />
    )
})
Button.displayName = "Button"

// ----------------------------------------------------------------------
// CARD
// ----------------------------------------------------------------------
export function Card({ className, ...props }) {
    return (
        <div
            className={cn(
                "rounded-2xl border border-slate-800 bg-slate-900/50 text-slate-100 shadow-sm backdrop-blur-sm",
                className
            )}
            {...props}
        />
    )
}

export function CardHeader({ className, ...props }) {
    return <div className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
}

export function CardTitle({ className, ...props }) {
    return <h3 className={cn("text-lg font-semibold leading-none tracking-tight", className)} {...props} />
}

export function CardContent({ className, ...props }) {
    return <div className={cn("p-6 pt-0", className)} {...props} />
}

// ----------------------------------------------------------------------
// INPUT
// ----------------------------------------------------------------------
export function Input({ className, ...props }) {
    return (
        <input
            className={cn(
                "flex h-12 w-full rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-sm ring-offset-slate-950 file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-slate-500 focus-visible:outline-none focus-visible:border-sky-500 disabled:cursor-not-allowed disabled:opacity-50 text-slate-100 transition-colors",
                className
            )}
            {...props}
        />
    )
}

// ----------------------------------------------------------------------
// MODAL
// ----------------------------------------------------------------------
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
                        <LucideIcons.X className="w-6 h-6" />
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

// ----------------------------------------------------------------------
// SWITCH
// ----------------------------------------------------------------------
export function Switch({ checked, onCheckedChange, id, className }) {
    return (
        <button
            type="button"
            role="switch"
            aria-checked={checked}
            id={id}
            onClick={() => onCheckedChange(!checked)}
            className={cn(
                "peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 disabled:cursor-not-allowed disabled:opacity-50",
                checked ? "bg-sky-500" : "bg-slate-700",
                className
            )}
        >
            <span
                className={cn(
                    "pointer-events-none block h-5 w-5 rounded-full bg-slate-100 shadow-lg ring-0 transition-transform",
                    checked ? "translate-x-5" : "translate-x-0"
                )}
            />
        </button>
    )
}

// ----------------------------------------------------------------------
const ToastContext = createContext(null)

export function ToastProvider({ children }) {
    const [toasts, setToasts] = useState([])

    const addToast = useCallback((message, type = 'success') => {
        const id = Math.random().toString(36).substring(2, 9)
        setToasts((prev) => [...prev, { id, message, type }])
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
                <LazyMotion features={domAnimation}>
                    <AnimatePresence>
                        {toasts.map((toast) => (
                            <Toast key={toast.id} {...toast} onRemove={() => removeToast(toast.id)} />
                        ))}
                    </AnimatePresence>
                </LazyMotion>
            </div>
        </ToastContext.Provider>
    )
}

function Toast({ message, type, onRemove }) {
    const icons = {
        success: <LucideIcons.CheckCircle2 className="w-5 h-5 text-emerald-500" />,
        error: <LucideIcons.AlertCircle className="w-5 h-5 text-rose-500" />,
        info: <LucideIcons.Info className="w-5 h-5 text-sky-500" />,
        warning: <LucideIcons.AlertTriangle className="w-5 h-5 text-amber-500" />
    }

    const styles = {
        success: "border-emerald-500/20 bg-emerald-500/10 text-emerald-200",
        error: "border-rose-500/20 bg-rose-500/10 text-rose-200",
        info: "border-sky-500/20 bg-sky-500/10 text-sky-200",
        warning: "border-amber-500/20 bg-amber-500/10 text-amber-200"
    }
    // ... icons and styles

    return (
        <m.div
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
                <LucideIcons.X className="w-4 h-4" />
            </button>
        </m.div>
    )
}

export const useToast = () => {
    const context = useContext(ToastContext)
    if (!context) throw new Error('useToast must be used within a ToastProvider')
    return context
}


// ----------------------------------------------------------------------
// CONFIRM DIALOG
// ----------------------------------------------------------------------
export function ConfirmDialog({ isOpen, onClose, onConfirm, title, message, type = 'danger' }) {
    const { t } = useLanguage()

    return (
        <Modal isOpen={isOpen} onClose={onClose} title={title || t('confirm_action')} className="max-w-sm">
            <div className="space-y-4">
                <div className="flex items-start gap-4">
                    <div className="p-2 bg-rose-500/10 rounded-full text-rose-500 shrink-0">
                        <LucideIcons.AlertTriangle className="w-6 h-6" />
                    </div>
                    <div className="space-y-1">
                        <p className="text-sm text-slate-300 leading-relaxed">
                            {message}
                        </p>
                    </div>
                </div>

                <div className="flex gap-3 justify-end pt-2">
                    <Button variant="ghost" onClick={onClose}>
                        {t('cancel')}
                    </Button>
                    <Button
                        variant={type === 'danger' ? 'destructive' : 'default'}
                        onClick={() => {
                            onConfirm()
                            onClose()
                        }}
                    >
                        {t('confirm')}
                    </Button>
                </div>
            </div>
        </Modal>
    )
}

// ----------------------------------------------------------------------
// DYNAMIC ICON
// ----------------------------------------------------------------------
const IconLoading = () => <div className="w-5 h-5 bg-slate-800/50 rounded animate-pulse" />
const iconCache = {}

export const DynamicIcon = ({ name, ...props }) => {
    // 1. Fallback for valid inputs
    if (!name) return <LucideIcons.HelpCircle {...props} />

    // 2. Convert PascalCase (DB) to kebab-case (Files)
    // e.g. ShoppingBag -> shopping-bag
    const iconName = name.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()

    // 3. Check if icon exists in dynamic imports
    if (!dynamicIconImports[iconName]) {
        // Fallback to HelpCircle if not found (Handle potential renaming in Lucide)
        const Fallback = LucideIcons.HelpCircle || LucideIcons.AlertCircle
        return <Fallback {...props} />
    }

    // 4. Load Dynamically
    if (!iconCache[iconName]) {
        iconCache[iconName] = dynamic(dynamicIconImports[iconName], {
            loading: IconLoading,
            ssr: false
        })
    }

    const Icon = iconCache[iconName]
    return <Icon {...props} />
}

// ----------------------------------------------------------------------
// ICON SELECTOR
// ----------------------------------------------------------------------
const ICON_LIST = [
    'Wallet', 'CreditCard', 'Banknote', 'Coins', 'DollarSign', 'Euro',
    'Home', 'Car', 'Plane', 'ShoppingBag', 'ShoppingCart', 'Gift',
    'Utensils', 'Coffee', 'Beer', 'Wine',
    'Zap', 'Wifi', 'Smartphone', 'Tv', 'Music', 'Film',
    'Heart', 'Activity', 'Stethoscope', 'Pill',
    'Briefcase', 'GraduationCap', 'Book', 'Wrench', 'Hammer',
    'User', 'Users', 'Baby', 'Dog', 'Cat',
    'Sun', 'Moon', 'Umbrella', 'CloudRain',
    'MapPin', 'Flag', 'Trophy', 'Star', 'Gamepad2',
    'Tag', 'Paperclip', 'Folder', 'FileText'
]

export function IconSelector({ selectedIcon, onSelect, color }) {
    return (
        <div className="space-y-3">
            <div className="grid grid-cols-6 sm:grid-cols-8 gap-2 max-h-48 overflow-y-auto custom-scrollbar p-1">
                {ICON_LIST.map(iconName => {
                    const Icon = LucideIcons[iconName] || LucideIcons.HelpCircle
                    const isSelected = selectedIcon === iconName

                    return (
                        <button
                            key={iconName}
                            onClick={() => onSelect(iconName)}
                            className={cn(
                                "flex items-center justify-center p-2 rounded-lg border transition-all aspect-square",
                                isSelected
                                    ? "bg-slate-800 border-slate-600 shadow-md transform scale-105"
                                    : "bg-slate-900/50 border-slate-800 hover:bg-slate-800 hover:border-slate-700"
                            )}
                            title={iconName}
                        >
                            <Icon
                                className="w-5 h-5"
                                style={{ color: isSelected ? color : undefined }}
                            />
                        </button>
                    )
                })}
            </div>
        </div>
    )
}

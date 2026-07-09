import { forwardRef } from "react"
import { cn } from "@/lib/utils"

const Button = forwardRef(({ className, variant = "default", size = "default", ...props }, ref) => {
    const variants = {
        default: "bg-sky-500 text-slate-50 hover:bg-sky-600 shadow-lg shadow-sky-500/25",
        outline: "border border-slate-700 bg-transparent hover:bg-slate-800 text-slate-100",
        ghost: "hover:bg-slate-800 text-slate-300 hover:text-slate-100",
        danger: "bg-rose-500 text-rose-50 hover:bg-rose-600 shadow-lg shadow-rose-500/25",
    }

    const sizes = {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        icon: "h-10 w-10",
    }

    return (
        <button
            className={cn(
                "inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-400 disabled:pointer-events-none disabled:opacity-50",
                variants[variant],
                sizes[size],
                className
            )}
            ref={ref}
            {...props}
        />
    )
})
Button.displayName = "Button"

export { Button }

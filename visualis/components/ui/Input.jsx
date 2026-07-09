import { cn } from '@/lib/utils'

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

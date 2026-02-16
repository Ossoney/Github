'use client'
import { usePrivacy } from '@/lib/privacy'
import { useLanguage } from '@/lib/i18n'
import { cn } from '@/lib/utils'

export function Money({ amount, currency, className, colored = false, coloredInverted = false }) {
    const { isPrivacyMode } = usePrivacy()
    const { formatMoney } = useLanguage()

    // Safety check for amount
    const numericAmount = parseFloat(amount) || 0

    if (isPrivacyMode) {
        return <span className={cn("tracking-widest opacity-75 select-none blur-[2px]", className)}>••••••</span>
    }

    // Color logic
    let colorClass = ''

    if (colored) {
        colorClass = numericAmount >= 0 ? 'text-emerald-400' : 'text-rose-400'
    } else if (coloredInverted) {
        colorClass = numericAmount >= 0 ? 'text-rose-400' : 'text-emerald-400'
    }

    return (
        <span className={cn(colorClass, className)}>
            {formatMoney(numericAmount, currency)}
        </span>
    )
}

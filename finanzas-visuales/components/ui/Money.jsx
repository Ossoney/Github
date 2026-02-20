'use client'
import { usePrivacy } from '@/lib/privacy'
import { useLanguage } from '@/lib/i18n'
import { cn } from '@/lib/utils'

export function Money({ amount, currency, className, colored = false, coloredInverted = false, showDecimals = true, showPlus = false, forceSign = null }) {
    const { isPrivacyMode } = usePrivacy()
    const { formatMoney } = useLanguage()

    // Safety check for amount
    const rawValue = parseFloat(amount) || 0

    if (isPrivacyMode) {
        return <span className={cn("tracking-widest opacity-75 select-none blur-[2px]", className)}>••••••</span>
    }

    const isNegative = rawValue < 0;
    const absValue = Math.abs(rawValue);

    const formatOptions = !showDecimals ? { minimumFractionDigits: 0, maximumFractionDigits: 0 } : {}

    const formattedAmount = formatMoney(absValue, currency, formatOptions);

    let sign = '';
    if (forceSign) {
        sign = forceSign + ' ';
    } else if (isNegative) {
        sign = '- ';
    } else if (showPlus && rawValue > 0) {
        sign = '+ ';
    }

    return (
        <span className={cn(
            className,
            colored && (rawValue > 0 ? 'text-emerald-400' : rawValue < 0 ? 'text-rose-400' : ''),
            coloredInverted && (rawValue > 0 ? 'text-rose-400' : rawValue < 0 ? 'text-emerald-400' : '')
        )}>
            {sign}{formattedAmount}
        </span>
    )
}

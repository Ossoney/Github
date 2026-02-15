'use client'

import { useStore } from '@/hooks/useStore'
import { Button } from '@/components/ui/UI'
import { ChevronLeft, ChevronRight, Calendar } from 'lucide-react'
import { format } from 'date-fns'
import { useLanguage } from '@/lib/i18n'

export function MonthSelector() {
    const { currentDate, nextMonth, prevMonth } = useStore()
    const { locale } = useLanguage()

    const formattedDate = format(currentDate, 'MMMM yyyy', { locale })

    return (
        <div className="flex items-center justify-between bg-slate-900/50 p-2 rounded-2xl border border-slate-800 backdrop-blur-md">
            <Button variant="ghost" size="icon" onClick={prevMonth} className="text-slate-400 hover:text-sky-400">
                <ChevronLeft className="w-6 h-6" />
            </Button>

            <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-slate-500" />
                <span className="text-2xl font-bold text-slate-200 capitalize tracking-wide">
                    {formattedDate}
                </span>
            </div>

            <Button variant="ghost" size="icon" onClick={nextMonth} className="text-slate-400 hover:text-sky-400">
                <ChevronRight className="w-6 h-6" />
            </Button>
        </div>
    )
}

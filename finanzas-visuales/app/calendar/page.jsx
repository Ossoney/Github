'use client'

import { CalendarGrid } from "@/components/calendar/CalendarGrid"
import { Button } from "@/components/ui/UI"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"
import { useLanguage } from "@/lib/i18n"

export default function CalendarPage() {
    const { t } = useLanguage()

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex items-center gap-4">
                <Link href="/">
                    <Button variant="ghost" className="gap-2 pl-2 pr-4 text-slate-400 hover:text-white">
                        <ArrowLeft className="w-5 h-5" />
                        <span className="font-medium">Volver</span>
                    </Button>
                </Link>
                <div>
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-indigo-400 bg-clip-text text-transparent">
                        {t('calendar_view') || "Vista de Calendario"}
                    </h1>
                    <p className="text-sm text-slate-400">
                        {t('calendar_desc') || "Visualiza tus ingresos y gastos mes a mes."}
                    </p>
                </div>
            </div>

            <CalendarGrid />
        </div>
    )
}

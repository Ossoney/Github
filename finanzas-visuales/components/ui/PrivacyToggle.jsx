'use client'
import { usePrivacy } from '@/lib/privacy'
import { Eye, EyeOff } from 'lucide-react'
import { Button } from './UI'
import { cn } from '@/lib/utils'

export function PrivacyToggle({ className }) {
    const { isPrivacyMode, togglePrivacyMode } = usePrivacy()

    return (
        <Button
            variant="ghost"
            size="icon"
            onClick={togglePrivacyMode}
            className={cn("text-slate-400 hover:text-sky-400 hover:bg-slate-800", className)}
            title={isPrivacyMode ? "Mostrar importes" : "Ocultar importes"}
        >
            {isPrivacyMode ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
        </Button>
    )
}

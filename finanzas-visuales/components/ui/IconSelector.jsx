'use client'

import React, { useState } from 'react'
import * as LucideIcons from 'lucide-react'
import { Input } from '@/components/ui/Input'
import { cn } from '@/lib/utils'

// Curated list of relevant icons for finances/categories
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

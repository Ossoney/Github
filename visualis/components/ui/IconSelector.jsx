'use client'

import React from 'react'
import * as LucideIcons from 'lucide-react'
import { cn } from '@/lib/utils'

// Comprehensive curated list of icons for categories & finances
const ICON_LIST = [
    // Finanzas, Cuentas & Bancos
    'Wallet', 'CreditCard', 'Banknote', 'Coins', 'DollarSign', 'Euro', 'Landmark', 'PiggyBank', 'TrendingUp', 'Percent',
    // Hogar, Vivienda & Alquiler
    'Home', 'Building', 'Key', 'Bed', 'Sofa', 'Bath',
    // Energía, Servicios & Electricidad
    'Zap', 'Flame', 'Droplets', 'Wifi', 'Phone', 'Lightbulb', 'Shield', 'FileText',
    // Transporte & Automóvil
    'Car', 'Fuel', 'ParkingSquare', 'Wrench', 'Bike', 'Bus', 'Train', 'Ship', 'Plane', 'Ticket',
    // Alimentación, Comida & Ocio
    'ShoppingCart', 'ShoppingBag', 'Utensils', 'Coffee', 'Beer', 'Wine', 'Cookie', 'Pizza', 'Apple',
    // Ocio, Cultura & Multimedia
    'Film', 'Tv', 'Music', 'Headphones', 'Camera', 'Gamepad2', 'Smile', 'PartyPopper',
    // Deportes & Salud
    'Dumbbell', 'Trophy', 'Activity', 'Heart', 'HeartPulse', 'Stethoscope', 'Pill', 'Scissors', 'Glasses',
    // Viajes, Vacaciones & Aire Libre
    'Compass', 'MapPin', 'Sun', 'Moon', 'Umbrella', 'CloudRain', 'Palmtree', 'Mountain', 'Tent',
    // Educación, Libros & Trabajo
    'GraduationCap', 'Book', 'BookOpen', 'Briefcase', 'PenTool', 'Printer', 'Smartphone', 'Laptop',
    // Familia, Mascotas & Regalos
    'User', 'Users', 'Baby', 'Dog', 'Cat', 'Gift', 'Sparkles', 'Star', 'FlameKindling',
    // Herramientas & Organización
    'Hammer', 'Package', 'Box', 'Tag', 'Paperclip', 'Folder', 'Circle', 'HelpCircle'
]

export function IconSelector({ selectedIcon, onSelect, color }) {
    return (
        <div className="space-y-3">
            <div className="grid grid-cols-6 sm:grid-cols-8 gap-2 max-h-56 overflow-y-auto custom-scrollbar p-1">
                {ICON_LIST.map(iconName => {
                    const Icon = LucideIcons[iconName] || LucideIcons.HelpCircle
                    const isSelected = selectedIcon === iconName

                    return (
                        <button
                            key={iconName}
                            type="button"
                            onClick={() => onSelect(iconName)}
                            className={cn(
                                "flex items-center justify-center p-2 rounded-lg border transition-all aspect-square",
                                isSelected
                                    ? "bg-slate-800 border-slate-500 shadow-md transform scale-105 ring-1 ring-sky-500"
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

import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { db } from './db'
import { format } from 'date-fns'

// ----------------------------------------------------------------------
// UI UTILS
// ----------------------------------------------------------------------
export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

export const formatCurrency = (amount, currency = 'EUR') => {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: currency,
    }).format(amount);
};

export { exportToExcel } from './export'
export { importFromExcel } from './import'

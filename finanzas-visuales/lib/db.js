import Dexie from 'dexie';

// Check if we are in the browser
const isBrowser = typeof window !== 'undefined';

// Mock DB for server-side rendering to prevent crashes
const mockDB = {
    settings: { get: () => Promise.resolve(null) },
    transactions: { toArray: () => Promise.resolve([]) },
    wallets: { toArray: () => Promise.resolve([]) },
    categories: { toArray: () => Promise.resolve([]) },
    recurring: { toArray: () => Promise.resolve([]) },
    tags: { toArray: () => Promise.resolve([]) },
    budgets: { toArray: () => Promise.resolve([]) },
    on: () => { },
    version: () => ({
        stores: () => ({
            upgrade: () => { }
        })
    })
};

export const db = isBrowser ? new Dexie('FinanzasVisualesDB') : mockDB;

if (isBrowser) {

    // Version 1: Initial Schema
    db.version(1).stores({
        wallets: '++id, name, type',
        categories: '++id, name, type',
        transactions: '++id, walletId, categoryId, date, type',
    });

    // Version 2: Nested Categories + Tags + Comments
    // Dexie handles upgrades automatically if we keep keys consistent
    db.version(2).stores({
        wallets: '++id, name, type',
        categories: '++id, name, type, parentId', // Added parentId index
        transactions: '++id, walletId, categoryId, date, type, *tags', // Added multi-entry index for tags
    });

    // Version 3: Profiles, Recurring, Tags, Budgets
    db.version(3).stores({
        wallets: '++id, name, type',
        categories: '++id, name, type, parentId',
        transactions: '++id, walletId, categoryId, date, type, *tags',
        settings: 'id', // Singleton for global settings (id='global')
        recurring: '++id, walletId, categoryId, dayOfMonth, type, active',
        tags: '++id, name',
    }).upgrade(async tx => {
        // Initialize default settings if needed
    });

    // Version 5: Specific Subcategory Icons
    db.version(5).stores({
        wallets: '++id, name, type',
        categories: '++id, name, type, parentId',
        transactions: '++id, walletId, categoryId, date, type, *tags',
        settings: 'id',
        recurring: '++id, walletId, categoryId, dayOfMonth, type, active',
        tags: '++id, name',
        budgets: '++id, categoryId, amount, type',
    }).upgrade(async tx => {
        // Migration: Update existing subcategories with specific icons
        const iconMap = {
            // Income
            'Recuperación': 'RotateCcw',
            'Alquiler Vacacional': 'Sun',
            'Intereses': 'Percent',
            'Negocio VUT': 'Building',
            'Otro Negocio': 'Briefcase',
            'Nómina': 'Banknote',
            'Desempleo': 'Umbrella',
            'Ventas': 'ShoppingBag',

            // Expenses
            'Combustible': 'Fuel',
            'Mantenimiento': 'Wrench',
            'Multas': 'AlertCircle',
            'Parking': 'ParkingSquare',
            'Peajes': 'Ticket',
            'Hipoteca': 'Home',
            'Préstamo': 'Banknote',
            'Comisiones': 'Percent',
            'Electrónica': 'Smartphone',
            'Oficina': 'Printer',
            'Reparaciones': 'Hammer',
            'Supermercado': 'ShoppingCart',
            'Carreras/Tr': 'Trophy',
            'Gimnasio': 'Dumbbell',
            'Libros/Comic': 'Book',
            'Suscripcion': 'CreditCard',
            'Lavandería': 'Droplets',
            'Ropa Deportiva': 'Activity',
            'Bar': 'Beer',
            'Cafés': 'Coffee',
            'Restaurante': 'Utensils',
            'Farmacia': 'Pill',
            'Peluquería': 'Scissors',
            'Médico': 'Stethoscope',
            'Agua': 'Droplets',
            'Luz': 'Zap',
            'Internet': 'Wifi',
            'Bus': 'Bus',
            'Metro': 'Train',
            'Uber-Cabify': 'Car',
            'Entradas': 'Ticket',
            'Hoteles': 'Bed',
            'Veterinario': 'Stethoscope'
        }

        await tx.categories.toCollection().modify(cat => {
            if (iconMap[cat.name]) {
                cat.icon = iconMap[cat.name]
            }
        })
    });

    // Version 6: Import CSV Categories
    db.version(6).stores({
        wallets: '++id, name, type',
        categories: '++id, name, type, parentId',
        transactions: '++id, walletId, categoryId, date, type, *tags',
        settings: 'id',
        recurring: '++id, walletId, categoryId, dayOfMonth, type, active',
        tags: '++id, name',
        budgets: '++id, categoryId, amount, type',
    }).upgrade(async tx => {
        // 1. Define Data Structure
        const incomeData = {
            'Alquiler': { color: '#3b82f6', icon: 'Home', children: ['Alquiler', 'Recuperación Suministros', 'Alquiler Vacacional'] },
            'Otros Ingresos': { color: '#6366f1', icon: 'Wallet', children: ['Devoluciones', 'Ventas Activos', 'Herencias', 'Regalos'] },
            'Dividendos': { color: '#8b5cf6', icon: 'TrendingUp', children: ['Dividendos', 'Intereses', 'Otros Rendimientos'] },
            'Negocio': { color: '#a855f7', icon: 'Briefcase', children: ['Negocio VUT', 'Consultorias', 'Otros Negocios'] },
            'Sueldo': { color: '#10b981', icon: 'Banknote', children: ['Nómina', 'Desempleo', 'Extras'] },
            'Wallapop-Vinted': { color: '#f59e0b', icon: 'ShoppingBag', children: ['Ventas', 'Otros'] }
        };

        const expenseData = {
            'Automóvil': { color: '#EF4444', icon: 'Car', children: ['Combustible', 'Mantenimiento', 'Multas', 'Parking', 'Peajes', 'Otros Gastos Automovil'] },
            'Bancos': { color: '#64748B', icon: 'Landmark', children: ['Hipoteca', 'Préstamo', 'Comisiones', 'Otras Deudas'] },
            'Alimentación': { color: '#10B981', icon: 'Utensils', children: ['Supermercado', 'Restaurante', 'Snacks'] },
            'Compras': { color: '#F97316', icon: 'ShoppingCart', children: ['Electrónica', 'Oficina', 'Otras', 'Regalos', 'Reparaciones'] },
            'Deporte': { color: '#F59E0B', icon: 'Dumbbell', children: ['Carreras/Travesías', 'Club', 'Deporte', 'Gimnasio'] },
            'Formación': { color: '#EAB308', icon: 'BookOpen', children: ['Curso', 'Libros/Comics', 'Suscripcion', 'Material'] },
            'Limpieza': { color: '#06B6D4', icon: 'Sparkles', children: ['Lavandería', 'Limpieza'] },
            'Moda': { color: '#EC4899', icon: 'Shirt', children: ['Calzado', 'Ropa Deporte', 'Ropa Vestir'] },
            'Ocio': { color: '#8B5CF6', icon: 'Beer', children: ['Bar', 'Cafés', 'Cine', 'Netflix-HBO'] },
            'Salud': { color: '#EF4444', icon: 'HeartPulse', children: ['Farmacia', 'Peluquería', 'Médico', 'Salud y Belleza'] },
            'Suministros': { color: '#F59E0B', icon: 'Zap', children: ['Agua', 'Luz', 'Comunidad', 'Electricidad', 'Gas', 'Impuestos', 'Internet', 'Seguros', 'Telefono', 'Otros Suministros'] },
            'Transporte': { color: '#3B82F6', icon: 'Train', children: ['Bus', 'Metro', 'Taxi', 'Tren', 'Uber-Cabify', 'Coche Compartido'] },
            'Viajes': { color: '#0EA5E9', icon: 'Plane', children: ['Entradas', 'Hoteles', 'Viajes'] },
            'Mascotas': { color: '#A855F7', icon: 'Dog', children: ['Veterinario', 'Mascota', 'Juguetes', 'Otros'] }
        };

        // Helper for icons mapping (simple match or defaults)
        const getIconForChild = (name) => {
            const map = {
                'Alquiler': 'Home', 'Recuperación Suministros': 'RotateCcw', 'Alquiler Vacacional': 'Sun',
                'Devoluciones': 'RotateCcw', 'Ventas Activos': 'Banknote', 'Herencias': 'Scroll', 'Regalos': 'Gift',
                'Dividendos': 'TrendingUp', 'Intereses': 'Percent', 'Otros Rendimientos': 'PlusCircle',
                'Negocio VUT': 'Building', 'Consultorias': 'Briefcase', 'Otros Negocios': 'Briefcase',
                'Nómina': 'Banknote', 'Desempleo': 'Umbrella', 'Extras': 'Plus',
                'Ventas': 'ShoppingBag', 'Otros': 'MoreHorizontal',
                'Combustible': 'Fuel', 'Mantenimiento': 'Wrench', 'Multas': 'AlertCircle', 'Parking': 'ParkingSquare', 'Peajes': 'Ticket', 'Otros Gastos Automovil': 'Car',
                'Hipoteca': 'Home', 'Préstamo': 'Banknote', 'Comisiones': 'Percent', 'Otras Deudas': 'CreditCard',
                'Supermercado': 'ShoppingCart', 'Restaurante': 'Utensils', 'Snacks': 'Cookie',
                'Electrónica': 'Smartphone', 'Oficina': 'Printer', 'Otras': 'ShoppingBag', 'Reparaciones': 'Hammer',
                'Carreras/Travesías': 'Trophy', 'Club': 'Users', 'Deporte': 'Activity', 'Gimnasio': 'Dumbbell',
                'Curso': 'GraduationCap', 'Libros/Comics': 'Book', 'Suscripcion': 'CreditCard', 'Material': 'PenTool',
                'Lavandería': 'Droplets', 'Limpieza': 'Sparkles',
                'Calzado': 'Footprints', 'Ropa Deporte': 'Activity', 'Ropa Vestir': 'Shirt',
                'Bar': 'Beer', 'Cafés': 'Coffee', 'Cine': 'Film', 'Netflix-HBO': 'Tv',
                'Farmacia': 'Pill', 'Peluquería': 'Scissors', 'Médico': 'Stethoscope', 'Salud y Belleza': 'Heart',
                'Agua': 'Droplets', 'Luz': 'Zap', 'Comunidad': 'Users', 'Electricidad': 'Zap', 'Gas': 'Flame', 'Impuestos': 'FileText', 'Internet': 'Wifi', 'Seguros': 'Shield', 'Telefono': 'Phone', 'Otros Suministros': 'Box',
                'Bus': 'Bus', 'Metro': 'Train', 'Taxi': 'Car', 'Tren': 'Train', 'Uber-Cabify': 'Car', 'Coche Compartido': 'Car',
                'Entradas': 'Ticket', 'Hoteles': 'Bed', 'Viajes': 'Plane',
                'Veterinario': 'Stethoscope', 'Mascota': 'Dog', 'Juguetes': 'Gamepad2'
            };
            return map[name] || 'Circle';
        };

        // Helper to process categories
        const processCategories = async (data, type) => {
            for (const [parentName, info] of Object.entries(data)) {
                // 1. Find or Create Parent
                let parent = await tx.categories.where({ name: parentName, type: type }).first();
                let parentId;

                if (parent) {
                    parentId = parent.id;
                    // Update parent props if needed? For now respect existing.
                } else {
                    parentId = await tx.categories.add({
                        name: parentName,
                        type: type,
                        icon: info.icon,
                        color: info.color,
                        parentId: null
                    });
                }

                // 2. Find or Create Children
                for (const childName of info.children) {
                    const existingChild = await tx.categories.where({ name: childName, parentId: parentId }).first();
                    if (!existingChild) {
                        await tx.categories.add({
                            name: childName,
                            type: type,
                            icon: getIconForChild(childName) || info.icon,
                            color: info.color,
                            parentId: parentId
                        });
                    }
                }
            }
        };

        await processCategories(incomeData, 'income');
        await processCategories(expenseData, 'expense');
    });

    // Version 7: User Requested Refinements
    db.version(7).stores({
        wallets: '++id, name, type',
        categories: '++id, name, type, parentId',
        transactions: '++id, walletId, categoryId, date, type, *tags',
        settings: 'id',
        recurring: '++id, walletId, categoryId, dayOfMonth, type, active',
        tags: '++id, name',
        budgets: '++id, categoryId, amount, type',
    }).upgrade(async tx => {
        // 1. Simple Removals (Unique Names)
        const namesToRemove = [
            'Otros gastos automóvil',
            'Otras deudas',
            'Ropa Deportiva',
            'Recuperación',
            'Otro Negocio'
        ];
        await tx.categories.where('name').anyOf(namesToRemove).delete();

        // 2. Remove "Restaurante" ONLY from "Ocio" (Keep in Alimentación)
        const ocio = await tx.categories.where({ name: 'Ocio' }).first();
        if (ocio) {
            await tx.categories.where({ name: 'Restaurante', parentId: ocio.id }).delete();
            // Rename child "Ocio" -> "Ocio Diverso"
            await tx.categories.where({ name: 'Ocio', parentId: ocio.id }).modify({ name: 'Ocio Diverso' });
        }

        // 3. Rename "Otras" -> "Varias" in "Compras"
        const compras = await tx.categories.where({ name: 'Compras' }).first();
        if (compras) {
            await tx.categories.where({ name: 'Otras', parentId: compras.id }).modify({ name: 'Varias' });
        }

        // 4. Remove Duplicates in "Formación" (Libros/Comic)
        const formacion = await tx.categories.where({ name: 'Formación' }).first();
        if (formacion) {
            const books = await tx.categories.where({ name: 'Libros/Comic', parentId: formacion.id }).toArray();
            if (books.length > 1) {
                // Keep the first one, delete the rest
                const idsToDelete = books.slice(1).map(c => c.id);
                await tx.categories.bulkDelete(idsToDelete);
            }
        }

        // 5. Remove Parents (and their children)
        const parentsToRemove = ['Devoluciones', 'Regalos', 'Wallapop-Vinted'];
        for (const name of parentsToRemove) {
            const parent = await tx.categories.where({ name }).first();
            if (parent) {
                await tx.categories.where({ parentId: parent.id }).delete();
                await tx.categories.delete(parent.id);
            }
        }

        // 6. Add "Ventas Segunda Mano" to "Otros Ingresos"
        // Try to find "Otros Ingresos" (from v6) or "Otros" (from seed?)
        let otrosIngresos = await tx.categories.where({ name: 'Otros Ingresos' }).first();
        if (!otrosIngresos) {
            otrosIngresos = await tx.categories.where({ name: 'Otros', type: 'income', parentId: null }).first();
        }

        if (otrosIngresos) {
            // Check if already exists to avoid dupes in re-runs (though upgrade runs once)
            const exists = await tx.categories.where({ name: 'Ventas Segunda Mano', parentId: otrosIngresos.id }).first();
            if (!exists) {
                await tx.categories.add({
                    name: 'Ventas Segunda Mano',
                    type: 'income',
                    parentId: otrosIngresos.id,
                    icon: 'ShoppingBag',
                    color: otrosIngresos.color
                });
            }
        }
    });

    // Seed data
    db.on('populate', async () => {
        // 1. Wallets
        // 1. Wallets
        await db.wallets.bulkAdd([
            { name: 'Mi día a día', type: 'bank', balance: 0, currency: 'EUR', isDefault: true },
        ]);

        // 2. Income Categories
        const incomeParents = [
            { name: 'Alquiler', icon: 'Home', color: '#3b82f6' }, // Blue
            { name: 'Otros Ingresos', icon: 'Wallet', color: '#6366f1' }, // Indigo
            { name: 'Dividendos', icon: 'TrendingUp', color: '#8b5cf6' }, // Violet
            { name: 'Negocio', icon: 'Briefcase', color: '#a855f7' }, // Purple
            { name: 'Sueldo', icon: 'Banknote', color: '#10b981' }, // Emerald
        ];

        const incomeChildren = {
            'Alquiler': [
                { name: 'Alquiler', icon: 'Home' },
                { name: 'Alquiler Vacacional', icon: 'Sun' }
            ],
            'Otros Ingresos': [
                { name: 'Devoluciones', icon: 'RotateCcw' },
                { name: 'Regalos', icon: 'Gift' },
                { name: 'Ventas Segunda Mano', icon: 'ShoppingBag' }, // Was Wallapop-Vinted
                { name: 'Herencias', icon: 'Scroll' }
            ],
            'Dividendos': [
                { name: 'Dividendos', icon: 'TrendingUp' },
                { name: 'Intereses', icon: 'Percent' }
            ],
            'Negocio': [
                { name: 'Negocio VUT', icon: 'Building' },
                { name: 'Consultorias', icon: 'Briefcase' }
            ],
            'Sueldo': [
                { name: 'Nómina', icon: 'Banknote' },
                { name: 'Desempleo', icon: 'Umbrella' },
                { name: 'Extras', icon: 'Plus' }
            ]
        };

        // Insert Income Categories
        for (const parent of incomeParents) {
            const parentId = await db.categories.add({
                name: parent.name,
                icon: parent.icon,
                color: parent.color,
                type: 'income',
                parentId: null
            });

            const childrenNames = incomeChildren[parent.name] || [];
            const children = childrenNames.map(child => ({
                name: child.name,
                icon: child.icon || parent.icon,
                color: parent.color,
                type: 'income',
                parentId: parentId
            }));

            if (children.length > 0) {
                await db.categories.bulkAdd(children);
            }
        }

        // 3. Expense Categories
        const expenseParents = [
            { name: 'Automóvil', icon: 'Car', color: '#EF4444' }, // Red
            { name: 'Bancos', icon: 'Landmark', color: '#64748B' }, // Slate
            { name: 'Alimentación', icon: 'Utensils', color: '#10B981' }, // Emerald (New Parent)
            { name: 'Compras', icon: 'ShoppingCart', color: '#F97316' }, // Orange
            { name: 'Deporte', icon: 'Dumbbell', color: '#F59E0B' }, // Amber
            { name: 'Formación', icon: 'BookOpen', color: '#EAB308' }, // Yellow
            { name: 'Limpieza', icon: 'Sparkles', color: '#06B6D4' }, // Cyan
            { name: 'Moda', icon: 'Shirt', color: '#EC4899' }, // Pink
            { name: 'Ocio', icon: 'Beer', color: '#8B5CF6' }, // Violet
            { name: 'Salud', icon: 'HeartPulse', color: '#EF4444' }, // Red
            { name: 'Suministros', icon: 'Zap', color: '#F59E0B' }, // Amber
            { name: 'Transporte', icon: 'Train', color: '#3B82F6' }, // Blue
            { name: 'Viajes', icon: 'Plane', color: '#0EA5E9' }, // Sky
            { name: 'Mascotas', icon: 'Dog', color: '#A855F7' }, // Purple
        ];

        const expenseChildren = {
            'Automóvil': [
                { name: 'Combustible', icon: 'Fuel' },
                { name: 'Mantenimiento', icon: 'Wrench' },
                { name: 'Multas', icon: 'AlertCircle' },
                { name: 'Parking', icon: 'ParkingSquare' },
                { name: 'Peajes', icon: 'Ticket' }
            ],
            'Bancos': [
                { name: 'Hipoteca', icon: 'Home' },
                { name: 'Préstamo', icon: 'Banknote' },
                { name: 'Comisiones', icon: 'Percent' }
            ],
            'Alimentación': [
                { name: 'Supermercado', icon: 'ShoppingCart' },
                { name: 'Restaurante', icon: 'Utensils' }, // Moved from Ocio
                { name: 'Snacks', icon: 'Cookie' }
            ],
            'Compras': [
                { name: 'Electrónica', icon: 'Smartphone' },
                { name: 'Oficina', icon: 'Printer' },
                { name: 'Varias', icon: 'ShoppingBag' }, // Renamed from Otras
                { name: 'Regalos', icon: 'Gift' },
                { name: 'Reparaciones', icon: 'Hammer' }
            ],
            'Deporte': [
                { name: 'Carreras/Travesías', icon: 'Trophy' },
                { name: 'Club', icon: 'UserPlus' },
                { name: 'Gimnasio', icon: 'Dumbbell' } // Removed duplicate 'Deporte' child?
            ],
            'Formación': [
                { name: 'Curso', icon: 'GraduationCap' },
                { name: 'Libros/Comics', icon: 'Book' },
                { name: 'Suscripcion', icon: 'CreditCard' },
                { name: 'Material', icon: 'PenTool' }
            ],
            'Limpieza': [
                { name: 'Lavandería', icon: 'Droplets' },
                { name: 'Limpieza', icon: 'Sparkles' }
            ],
            'Moda': [
                { name: 'Calzado', icon: 'Footprints' },
                { name: 'Ropa Vestir', icon: 'Shirt' }
            ],
            'Ocio': [
                { name: 'Bar', icon: 'Beer' },
                { name: 'Cafés', icon: 'Coffee' },
                { name: 'Ocio Diverso', icon: 'Smile' }, // Renamed from Ocio
                { name: 'Cine', icon: 'Film' },
                { name: 'Netflix-HBO', icon: 'Tv' }
            ],
            'Salud': [
                { name: 'Farmacia', icon: 'Pill' },
                { name: 'Peluquería', icon: 'Scissors' },
                { name: 'Médico', icon: 'Stethoscope' },
                { name: 'Salud y Belleza', icon: 'Heart' }
            ],
            'Suministros': [
                { name: 'Agua', icon: 'Droplets' },
                { name: 'Luz', icon: 'Zap' },
                { name: 'Comunidad', icon: 'Users' },
                { name: 'Gas', icon: 'Flame' },
                { name: 'Impuestos', icon: 'FileText' },
                { name: 'Internet', icon: 'Wifi' },
                { name: 'Seguros', icon: 'Shield' },
                { name: 'Telefono', icon: 'Phone' },
                { name: 'Otros Suministros', icon: 'Box' }
            ],
            'Transporte': [
                { name: 'Bus', icon: 'Bus' },
                { name: 'Metro', icon: 'Train' },
                { name: 'Taxi', icon: 'Car' },
                { name: 'Tren', icon: 'Train' },
                { name: 'Uber-Cabify', icon: 'Car' },
                { name: 'Coche Compartido', icon: 'Car' }
            ],
            'Viajes': [
                { name: 'Entradas', icon: 'Ticket' },
                { name: 'Hoteles', icon: 'Bed' },
                { name: 'Viajes', icon: 'Plane' }
            ],
            'Mascotas': [
                { name: 'Veterinario', icon: 'Stethoscope' },
                { name: 'Mascota', icon: 'Dog' },
                { name: 'Juguetes', icon: 'Gamepad2' }
            ]
        };

        // Insert Expense Parents & Children
        for (const parent of expenseParents) {
            const parentId = await db.categories.add({
                name: parent.name,
                icon: parent.icon,
                color: parent.color,
                type: 'expense',
                parentId: null
            });

            const childrenNames = expenseChildren[parent.name] || [];
            const children = childrenNames.map(child => ({
                name: child.name,
                icon: child.icon || parent.icon,
                color: parent.color,
                type: 'expense',
                parentId: parentId
            }));

            if (children.length > 0) {
                await db.categories.bulkAdd(children);
            }
        }
    });
}

/**
 * Export all data from the database to a JSON object
 */
export const exportDB = async () => {
    const data = {
        meta: {
            version: 1,
            date: new Date().toISOString(),
            app: 'Visualis'
        },
        tables: {}
    };

    const tables = ['wallets', 'categories', 'transactions', 'settings', 'recurring', 'tags', 'budgets'];

    for (const tableName of tables) {
        data.tables[tableName] = await db.table(tableName).toArray();
    }

    return data;
};

/**
 * Import data from a JSON object, replacing current data
 */
export const importDB = async (data) => {
    // Basic validation
    if (!data || !data.tables) {
        throw new Error('Invalid backup format');
    }

    const tables = ['wallets', 'categories', 'transactions', 'settings', 'recurring', 'tags', 'budgets'];

    await db.transaction('rw', tables.map(t => db.table(t)), async () => {
        // 1. Clear all existing data
        for (const tableName of tables) {
            await db.table(tableName).clear();
        }

        // 2. Insert new data
        for (const tableName of tables) {
            if (data.tables[tableName] && Array.isArray(data.tables[tableName])) {
                await db.table(tableName).bulkAdd(data.tables[tableName]);
            }
        }
    });

    return true;
};

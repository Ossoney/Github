'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { db } from '@/lib/db'
import { es, enUS, gl, eu, ca } from 'date-fns/locale'

// ----------------------------------------------------------------------
// DICTIONARIES
// ----------------------------------------------------------------------
const dictionaries = {
    es: {
        app_title: 'VISUALIS',
        app_subtitle: 'tus finanzas fáciles',
        dashboard_recent_activity: 'Actividad Reciente',
        dashboard_monthly_budget: 'Presupuesto del Mes',
        total_balance: 'Balance Total',
        income: 'Ingresos',
        expense: 'Gastos',
        result: 'Resultado',
        month: 'Mes',
        settings: 'Configuración',
        profile: 'Perfil',
        accounts: 'Cuentas/Proyectos',
        categories: 'Categorías',
        recurring: 'Recurrentes',
        data: 'Datos',
        theme: 'Tema',
        language: 'Idioma',
        select_language: 'Selecciona tu idioma',
        save: 'Guardar',
        cancel: 'Cancelar',
        delete: 'Eliminar',
        edit: 'Editar',
        new_transaction: 'Nueva Transacción',
        edit_transaction: 'Editar Transacción',
        amount: 'Cantidad',
        date: 'Fecha',
        wallet: 'Cuenta',
        category: 'Categoría',
        description: 'Descripción',
        tags: 'Etiquetas',
        export_excel: 'Descargar Excel',
        import_excel: 'Importar Excel',
        reset_data: 'Borrar Todo',
        danger_zone: 'Zona de Peligro',
        warning_nuclear: '⚠️ ¡ADVERTENCIA NUCLEAR! ⚠️',
        confirm_nuclear: '¿Estás SEGURO de querer borrar TODOS los datos?',
        nuclear_button: 'Botón Nuclear',

        // Wallet Summary
        global_total: 'TOTAL GLOBAL',
        net_worth: 'Patrimonio',
        monthly_variation: 'Variación Mensual',
        total: 'Total',
        this_month: 'Este Mes',

        // Transaction List
        no_recent_transactions: 'No hay movimientos recientes',
        uncategorized: 'Sin categoría',

        // Budget List
        budgets: 'Presupuestos',
        monthly_total: 'Total Mensual',
        no_expenses_this_month: 'No hay gastos este mes.',
        of: 'de',

        // Transaction Form
        select_wallet: 'Selecciona cuenta',
        change: 'Cambiar',
        back_to_categories: 'Volver a Categorías',
        optional_note: 'Nota opcional...',
        update: 'Actualizar',

        // Validation & Errors
        confirm_delete_transaction: '¿Seguro que quieres eliminar esta transacción?',
        validation_amount: 'Por favor, indica la cantidad.',
        validation_wallet: 'Por favor, selecciona una cuenta (Efectivo, Banco, etc).',
        validation_category: 'Por favor, selecciona una categoría.',
        validation_amount_invalid: 'La cantidad no es válida.',
        validation_date_invalid: 'La fecha seleccionada no es válida.',
        error_saving: 'Error al guardar',
        error_deleting: 'Error al eliminar',
        confirm: 'Confirmar',
        confirm_action: 'Confirmación',

        // Settings Managers
        my_accounts: 'Mis Cuentas/Proyectos',
        create_account: 'Crear Cuenta/Proyecto',
        account_name_placeholder: 'Nombre (ej. Revolut, Proyecto X)',
        initial_balance: 'Saldo Inicial',
        no_accounts: 'No tienes cuentas/proyectos. Crea una para empezar.',
        confirm_delete_account: '¿Seguro que quieres borrar esta cuenta? Se mantendrán las transacciones pero quedarán huérfanas.',

        recurring_transactions: 'Recurrentes',
        new_recurring: 'Nueva Recurrente',
        edit_recurring: 'Editar Recurrente',
        select_account: 'Selecciona Cuenta',
        select_category: 'Selecciona Categoría',
        day_of_month: 'Día del mes',
        no_recurring: 'No tienes transacciones recurrentes.',
        confirm_delete_recurring: '¿Eliminar recurrencia?',

        new_category_parent: 'Nueva Categoría Principal',
        new_category_child: 'Nueva Subcategoría',
        add_subcategory: 'Añadir Subcategoría',
        confirm_delete_category: '¿Borrar categoría? Si es padre, se borrarán también sus hijos.',
        // Settings Menu
        settings: 'Configuración',
        profile: 'Perfil',
        appearance: 'Apariencia',
        accounts: 'Cuentas/Proyectos',
        categories: 'Categorías',
        budgets: 'Presupuestos',
        recurring: 'Recurrentes',
        tags: 'Etiquetas',
        data: 'Datos',
        language: 'Idioma',
        language: 'Idioma',
        version_help: 'Versión/Ayuda',
        version_date: 'Febrero 2026',

        // Profile Settings
        user_profile: 'Perfil de Usuario',
        change_photo: 'Pulsa para cambiar la foto',
        name: 'Nombre',
        your_name: 'Tu Nombre',
        save_profile: 'Guardar Perfil',
        saving: 'Guardando...',
        profile_saved: 'Perfil guardado correctamente',
        customize_home: 'Personalizar Inicio',
        customize_home_desc: 'Muestra "Las finanzas de [Nombre]" en lugar del texto por defecto.',
        finances_of: 'las finanzas de {name}',

        // Help Guide
        help_financial_title: 'Gestión Financiera',
        help_dashboard_desc: 'Visión global de tu patrimonio y actividad reciente.',
        help_calendar_title: 'Vista de Calendario',
        help_calendar_help_desc: 'Visualiza tus gastos e ingresos diarios y previsiones en un calendario mensual.',
        help_transactions_desc: 'Registro detallado de ingresos y gastos con buscador avanzado.',

        help_structure_title: 'Estructura',
        help_accounts_desc: 'Gestiona múltiples cuentas (bancos, efectivo, tarjetas).',
        help_categories_desc: 'Organiza tus movimientos en categorías y subcategorías.',
        help_tags_desc: 'Etiqueta transacciones para agrupar conceptos transversales (#Viaje).',

        help_planning_title: 'Planificación',
        help_budgets_desc: 'Establece límites de gasto mensual por categoría.',
        help_recurring_desc: 'Configura movimientos fijos automáticos (alquiler, nómina).',

        help_customization_title: 'Personalización',
        help_themes_desc: 'Elige entre múltiples temas visuales.',
        help_profile_desc: 'Personaliza tu nombre y avatar.',
        help_languages_desc: 'Cambia el idioma de la aplicación.',

        help_data_title: 'Datos y Privacidad',
        help_security_title: 'Seguridad',
        help_privacy_desc: 'Tus datos nunca salen de tu dispositivo (Local First).',
        help_privacy_mode_title: 'Modo Privacidad',
        help_privacy_mode_desc: 'Oculta los saldos sensibles con un clic para mayor discreción.',
        help_backups_desc: 'Exporta e importa tus datos en formato JSON.',
        help_excel_desc: 'Compatible con hojas de cálculo para análisis externos.',
        help_safe_zone_desc: 'Restablecimiento de fábrica disponible.',

        // Donation
        donation_title: 'Invítame a un café',
        donation_desc: 'Si Visualis te es útil, puedes apoyar su desarrollo con una pequeña donación.',
        donate_button: 'Invitar (PayPal)',

        // Theme Settings
        choose_theme: 'Elige el ambiente para tu aplicación:',
        theme_names: {
            sky: 'Noche Estrellada',
            gold: 'Eclipse Dorado',
            forest: 'Bosque Profundo',
            nebula: 'Nebulosa Púrpura',
            cyber: 'Futuro Neón',
            wine: 'Vino Selecto',
            coffee: 'Grano Tostado',
            royal: 'Zafiro Real',
            minimal: 'Minimalismo Puro',
        },

        // Currency Settings
        main_currency: 'Moneda Principal',

        // Tag Settings
        manage_tags: 'Gestionar Etiquetas',
        new_tag_placeholder: 'Nueva etiqueta (ej. #vacaciones)',
        no_tags: 'No hay etiquetas creadas aún.',
        confirm_delete_tag: '¿Eliminar etiqueta?',

        // Data Settings
        backups: 'Copias de Seguridad',
        export_title: 'Exportar',
        export_desc: 'Descarga una copia de seguridad de tus movimientos, cuentas y categorías en formato Excel.',
        download_excel: 'Descargar Excel (.xlsx)',
        import_title: 'Importar',
        import_desc: 'Restaura una copia de seguridad.',
        import_warning: 'Esto borrará los datos actuales',
        select_file: 'Seleccionar Archivo (.xlsx)',
        danger_zone: 'Zona de Peligro',
        danger_desc: 'Si necesitas empezar de cero, puedes borrar toda la base de datos local. Esta acción es irreversible.',
        nuclear_button: 'Botón Nuclear',

        // New Data Settings
        security_title: 'Seguridad',
        backup_create: 'Crear Copia de Seguridad',
        backup_desc: 'Guarda un archivo completo de todos tus datos para poder restaurarlos más tarde si cambias de dispositivo o borras el navegador.',
        restore_title: 'Restaurar Copia',
        restore_desc: 'Recupera tus datos desde un archivo de copia de seguridad.',
        restore_confirm: '⚠️ ¿Restaurar copia de seguridad? ESTO SOBRESCRIBIRÁ TODOS LOS DATOS ACTUALES.',
        excel_data_title: 'Datos Excel',
        excel_data_desc: 'Herramientas para trabajar con tus datos en hojas de cálculo externas.',
        json_backup_title: 'Copia de Seguridad (JSON)',
        json_restore_success: '✅ Copia de seguridad restaurada correctamente.',
        json_restore_error: '❌ Error al restaurar la copia: ',

        // Data Alerts
        nuclear_warning_1: '⚠️ ¡ADVERTENCIA NUCLEAR! ⚠️\n\n¿Estás SEGURO de querer borrar TODOS los datos?\n\nEsta acción eliminará todas tus transacciones, cuentas, presupuestos y configuración.\n\nNO HAY VUELTA ATRÁS.',
        nuclear_warning_2: '¿De verdad? Confirma una última vez que quieres empezar de cero.',
        import_confirm: '⚠️ ¿Estás seguro de IMPORTAR este archivo?\n\n"{fileName}"\n\nSe ELIMINARÁN todos los datos actuales y se reemplazarán por los del archivo.',
        import_success: '✅ Importación completada. Se han restaurado {count} transacciones.',
        import_error: '❌ Error al importar: ',

        // Advanced Search
        transaction_history: 'Historial Completo',
        search_placeholder: 'Buscar por concepto, categoría, nota...',
        filters: 'Filtros',
        clear_filters: 'Limpiar',
        filter_by: 'Filtrar por',
        type: 'Tipo',
        all: 'Todos',
        date: 'Fecha',
        see_all: 'Ver Todo',
        no_transactions_found: 'No se encontraron transacciones.',
        try_adjusting_filters: 'Prueba a cambiar los filtros.',

        // Calendar
        calendar_view: 'Vista de Calendario',
        calendar_desc: 'Visualiza tus ingresos y gastos mes a mes.',
        go_to_today: 'Ir a Hoy',
        projected: 'Proyecciones (Recurrentes)',
        transactions: 'Movimientos Reales',

        // Category Translations (ES defaults - map to themselves or variations)
        category_names: {
            // Keeps original Spanish as fallback, but defined here for consistency if we wanted to rename
            'Wallapop-Vinted': 'Segunda Mano',
            'Uber-Cabify': 'Uber-Cabify',
        }
    },
    en: {
        app_title: 'VISUALIS',
        app_subtitle: 'your finances',
        dashboard_recent_activity: 'Recent Activity',
        dashboard_monthly_budget: 'Monthly Budget',
        total_balance: 'Total Balance',
        income: 'Income',
        expense: 'Expenses',
        result: 'Result',
        month: 'Month',
        settings: 'Settings',
        profile: 'Profile',
        accounts: 'Accounts/Projects',
        categories: 'Categories',
        recurring: 'Recurring',
        data: 'Data',
        theme: 'Theme',
        language: 'Language',
        select_language: 'Select your language',
        save: 'Save',
        cancel: 'Cancel',
        delete: 'Delete',
        edit: 'Edit',
        new_transaction: 'New Transaction',
        edit_transaction: 'Edit Transaction',
        amount: 'Amount',
        date: 'Date',
        wallet: 'Wallet',
        category: 'Category',
        description: 'Description',
        tags: 'Tags',
        export_excel: 'Download Excel',
        import_excel: 'Import Excel',
        reset_data: 'Reset Data',
        danger_zone: 'Danger Zone',
        warning_nuclear: '⚠️ NUCLEAR WARNING! ⚠️',
        confirm_nuclear: 'Are you SURE you want to delete ALL data?',
        nuclear_button: 'Nuclear Button',

        // New Data Settings
        security_title: 'Security',
        backup_create: 'Create Backup',
        backup_desc: 'Save a full backup file of all your data to restore later if you switch devices or clear your browser.',
        restore_title: 'Restore Backup',
        restore_desc: 'Recover your data from a backup file.',
        restore_confirm: '⚠️ Restore backup? THIS WILL OVERWRITE ALL CURRENT DATA.',
        excel_data_title: 'Excel Data',
        excel_data_desc: 'Tools to work with your data in external spreadsheets.',
        json_backup_title: 'Full Backup (JSON)',
        json_restore_success: '✅ Backup restored successfully.',
        json_restore_error: '❌ Error restoring backup: ',

        // Advanced Search
        transaction_history: 'Full History',
        search_placeholder: 'Search by concept, category, note...',
        filters: 'Filters',
        clear_filters: 'Clear',
        filter_by: 'Filter by',
        type: 'Type',
        all: 'All',
        date: 'Date',
        see_all: 'See All',
        no_transactions_found: 'No transactions found.',
        try_adjusting_filters: 'Try adjusting filters.',

        // Calendar
        calendar_view: 'Calendar View',
        calendar_desc: 'Visualize your income and expenses month by month.',
        go_to_today: 'Go to Today',
        projected: 'Projected (Recurring)',
        transactions: 'Actual Transactions',

        // Wallet Summary
        global_total: 'GLOBAL TOTAL',
        net_worth: 'Net Worth',
        monthly_variation: 'Monthly Variation',
        total: 'Total',
        this_month: 'This Month',

        // Transaction List
        no_recent_transactions: 'No recent transactions',
        uncategorized: 'Uncategorized',

        // Budget List
        budgets: 'Budgets',
        monthly_total: 'Monthly Total',
        no_expenses_this_month: 'No expenses this month.',
        of: 'of',

        // Transaction Form
        select_wallet: 'Select Wallet',
        change: 'Change',
        back_to_categories: 'Back to Categories',
        optional_note: 'Optional note...',
        update: 'Update',

        // Validation & Errors
        confirm_delete_transaction: 'Are you sure you want to delete this transaction?',
        validation_amount: 'Please enter an amount.',
        validation_wallet: 'Please select a wallet.',
        validation_category: 'Please select a category.',
        validation_amount_invalid: 'Invalid amount.',
        validation_date_invalid: 'Invalid date selected.',
        error_saving: 'Error saving',
        error_deleting: 'Error deleting',
        confirm: 'Confirm',
        confirm_action: 'Confirmation',

        // Settings Managers
        my_accounts: 'My Accounts/Projects',
        create_account: 'Create Account/Project',
        account_name_placeholder: 'Name (e.g. Revolut, Project X)',
        initial_balance: 'Initial Balance',
        no_accounts: 'No accounts/projects yet. Create one to start.',
        confirm_delete_account: 'Are you sure? Transactions will remain but become orphaned.',

        recurring_transactions: 'Recurring',
        new_recurring: 'New Recurring',
        edit_recurring: 'Edit Recurring',
        select_account: 'Select Wallet',
        select_category: 'Select Category',
        day_of_month: 'Day of month',
        no_recurring: 'No recurring transactions.',
        confirm_delete_recurring: 'Delete recurring transaction?',

        new_category_parent: 'New Main Category',
        new_category_child: 'New Subcategory',
        add_subcategory: 'Add Subcategory',
        confirm_delete_category: 'Delete category? If parent, children will be deleted too.',
        // Settings Menu
        settings: 'Settings',
        profile: 'Profile',
        appearance: 'Appearance',
        accounts: 'Accounts/Projects',
        categories: 'Categories',
        budgets: 'Budgets',
        recurring: 'Recurring',
        tags: 'Tags',
        data: 'Data',
        language: 'Language',
        language: 'Language',
        version_help: 'Version/Help',
        version_date: 'February 2026',

        // Profile Settings
        user_profile: 'User Profile',
        change_photo: 'Click to change photo',
        name: 'Name',
        your_name: 'Your Name',
        save_profile: 'Save Profile',
        saving: 'Saving...',
        profile_saved: 'Profile saved successfully',

        profile_saved: 'Profile saved successfully',
        customize_home: 'Customize Home',
        customize_home_desc: 'Shows "The finances of [Name]" instead of default text.',
        finances_of: 'the finances of {name}',

        // Help Guide
        help_financial_title: '1. Main Financial Management',
        help_dashboard_desc: 'Global wealth summary, time selector and recent activity.',
        help_transactions_desc: 'Detailed record of income and expenses with advanced search and filters.',

        help_structure_title: '2. Organizational Structure',
        help_accounts_desc: 'Multi-account management (Bank, Cash, Savings) and specific projects.',
        help_categories_desc: 'Hierarchical system with customizable icons and colors.',
        help_tags_desc: 'Transversal classification (tags) to group expenses from different categories.',

        help_planning_title: '3. Planning and Automation',
        help_budgets_desc: 'Monthly spending limits with visual progress bars.',
        help_recurring_desc: 'Automation of fixed income and expenses (Salary, Subscriptions).',

        help_customization_title: '4. Customization and Experience',
        help_themes_desc: '9 unique atmospheres (Starry Night, Cyberpunk, Minimalist...).',
        help_profile_desc: 'Customization of name, avatar and home title.',
        help_languages_desc: 'Full support for Spanish, English, Galician and Basque.',

        help_data_title: '5. Data and Privacy',
        help_privacy_desc: 'All data lives in your browser. Zero external servers.',
        help_backups_desc: 'Full export/import in JSON format.',
        help_excel_desc: 'Compatible with spreadsheets for external analysis.',
        help_safe_zone_desc: 'Factory reset available.',

        // Donation
        donation_title: 'Buy me a coffee',
        donation_desc: 'If Visualis is useful to you, you can support its development with a small donation.',
        donate_button: 'Donate (PayPal)',

        // Theme Settings
        choose_theme: 'Choose the ambiance for your app:',
        theme_names: {
            sky: 'Starry Night',
            gold: 'Golden Eclipse',
            forest: 'Deep Forest',
            nebula: 'Purple Nebula',
            cyber: 'Neon Future',
            wine: 'Select Wine',
            coffee: 'Roasted Bean',
            royal: 'Royal Sapphire',
            minimal: 'Pure Minimalism',
        },

        // Currency Settings
        main_currency: 'Main Currency',

        // Tag Settings
        manage_tags: 'Manage Tags',
        new_tag_placeholder: 'New tag (e.g. #vacation)',
        no_tags: 'No tags created yet.',
        confirm_delete_tag: 'Delete tag?',

        // Data Settings
        backups: 'Backups',
        export_title: 'Export',
        export_desc: 'Download a backup of your transactions, accounts, and categories in Excel format.',
        download_excel: 'Download Excel (.xlsx)',
        import_title: 'Import',
        import_desc: 'Restore a backup.',
        import_warning: 'This will delete current data',
        select_file: 'Select File (.xlsx)',
        danger_zone: 'Danger Zone',
        danger_desc: 'If you need to start over, you can wipe the entire local database. This action is irreversible.',
        nuclear_button: 'Nuclear Button',

        // Data Alerts
        nuclear_warning_1: '⚠️ NUCLEAR WARNING! ⚠️\n\nAre you SURE you want to delete ALL data?\n\nThis will remove all transactions, accounts, budgets, and settings.\n\nTHERE IS NO GOING BACK.',
        nuclear_warning_2: 'Really? Confirm one last time that you want to start from scratch.',
        import_confirm: '⚠️ Are you sure you want to IMPORT this file?\n\n"{fileName}"\n\nAll current data will be DELETED and replaced.',
        import_success: '✅ Import completed. Restored {count} transactions.',
        import_error: '❌ Import error: ',

        // Category Translations
        category_names: {
            // Income
            'Alquiler': 'Rent',
            'Devoluciones': 'Refunds',
            'Dividendos': 'Dividends',
            'Negocio': 'Business',
            'Regalos': 'Gifts',
            'Sueldo': 'Salary',
            'Wallapop-Vinted': 'Second Hand',
            'Recuperación': 'Recovery',
            'Alquiler Vacacional': 'Vacation Rental',
            'Intereses': 'Interests',
            'Negocio VUT': 'Side Hustle',
            'Otro Negocio': 'Other Business',
            'Nómina': 'Paycheck',
            'Desempleo': 'Unemployment',
            'Ventas': 'Sales',
            'Otros': 'Others',

            // Expenses
            'Automóvil': 'Car',
            'Bancos': 'Banks',
            'Compras': 'Shopping',
            'Deporte': 'Sports',
            'Formación': 'Education',
            'Limpieza': 'Cleaning',
            'Moda': 'Fashion',
            'Ocio': 'Leisure',
            'Salud': 'Health',
            'Suministros': 'Utilities',
            'Transporte': 'Transport',
            'Viajes': 'Travel',
            'Mascotas': 'Pets',

            'Combustible': 'Fuel',
            'Mantenimiento': 'Maintenance',
            'Multas': 'Fines',
            'Parking': 'Parking',
            'Peajes': 'Tolls',
            'Otros gastos automóvil': 'Other car expenses',
            'Hipoteca': 'Mortgage',
            'Préstamo': 'Loan',
            'Comisiones': 'Commissions',
            'Otras deudas': 'Other debts',
            'Electrónica': 'Electronics',
            'Oficina': 'Office',
            'Otras': 'Others',
            'Reparaciones': 'Repairs',
            'Supermercado': 'Groceries',
            'Carreras/Tr': 'Races',
            'Club': 'Club',
            'Gimnasio': 'Gym',
            'Curso': 'Course',
            'Libros/Comic': 'Books/Comics',
            'Suscripcion': 'Subscription',
            'Lavandería': 'Laundry',
            'Calzado': 'Footwear',
            'Ropa Deportiva': 'Sportswear',
            'Ropa Vestir': 'Clothing',
            'Bar': 'Bar',
            'Cafés': 'Coffee',
            'Restaurante': 'Restaurant',
            'Farmacia': 'Pharmacy',
            'Peluquería': 'Hairdresser',
            'Médico': 'Doctor',
            'Salud y Belleza': 'Health & Beauty',
            'Agua': 'Water',
            'Luz': 'Electricity',
            'Comunidad': 'HOA Fees',
            'Electricidad': 'Electricity',
            'Gas': 'Gas',
            'Impuestos': 'Taxes',
            'Internet': 'Internet',
            'Seguros': 'Insurance',
            'Telefono': 'Phone',
            'Otros Suministros': 'Other Utilities',
            'Bus': 'Bus',
            'Metro': 'Subway',
            'Taxi': 'Taxi',
            'Tren': 'Train',
            'Uber-Cabify': 'Rideshare',
            'Entradas': 'Tickets',
            'Hoteles': 'Hotels',
            'Veterinario': 'Vet',
            'Mascota': 'Pet Care',
            'Varias': 'Various',
            'Ocio Diverso': 'Diverse Leisure',
            'Ventas Segunda Mano': 'Second Hand Sales'
        }
    },
    gl: {
        app_title: 'VISUALIS',
        app_subtitle: 'as túas finanzas',
        dashboard_recent_activity: 'Actividade Recente',
        dashboard_monthly_budget: 'Orzamento do Mes',
        total_balance: 'Balance Total',
        income: 'Ingresos',
        expense: 'Gastos',
        result: 'Resultado',
        month: 'Mes',
        settings: 'Configuración',
        profile: 'Perfil',
        accounts: 'Contas/Proxectos',
        categories: 'Categorías',
        recurring: 'Recorrentes',
        data: 'Datos',
        theme: 'Tema',
        language: 'Idioma',
        select_language: 'Selecciona o teu idioma',
        save: 'Gardar',
        cancel: 'Cancelar',
        delete: 'Eliminar',
        edit: 'Editar',
        new_transaction: 'Nova Transacción',
        edit_transaction: 'Editar Transacción',
        amount: 'Cantidade',
        date: 'Data',
        wallet: 'Conta',
        category: 'Categoría',
        description: 'Descrición',
        tags: 'Etiquetas',
        export_excel: 'Descargar Excel',
        import_excel: 'Importar Excel',
        reset_data: 'Borrar Todo',
        danger_zone: 'Zona de Perigo',
        warning_nuclear: '⚠️ ADVERTENCIA NUCLEAR! ⚠️',
        confirm_nuclear: 'Estás SEGURO de querer borrar TODOS os datos?',
        nuclear_button: 'Botón Nuclear',

        // New Data Settings
        security_title: 'Seguridade',
        backup_create: 'Crear Copia de Seguridade',
        backup_desc: 'Garda un arquivo completo de todos os teus datos para poder restauralos máis tarde se cambias de dispositivo ou borras o navegador.',
        restore_title: 'Restaurar Copia',
        restore_desc: 'Recupera os teus datos desde un arquivo de copia de seguridade.',
        restore_confirm: '⚠️ Restaurar copia de seguridade? ISTO SOBRESCRIBIRÁ TODOS OS DATOS ACTUAIS.',
        excel_data_title: 'Datos Excel',
        excel_data_desc: 'Ferramentas para traballar cos teus datos en follas de cálculo externas.',
        json_backup_title: 'Copia de Seguridade (JSON)',
        json_restore_success: '✅ Copia de seguridade restaurada correctamente.',
        json_restore_error: '❌ Erro ao restaurar a copia: ',

        // Advanced Search
        transaction_history: 'Historial Completo',
        search_placeholder: 'Buscar por concepto, categoría, nota...',
        filters: 'Filtros',
        clear_filters: 'Limpar',
        filter_by: 'Filtrar por',
        type: 'Tipo',
        all: 'Todos',
        date: 'Data',
        see_all: 'Ver Todo',
        no_transactions_found: 'Non se atoparon transaccións.',
        try_adjusting_filters: 'Proba a cambiar os filtros.',

        // Calendar
        calendar_view: 'Vista de Calendario',
        calendar_desc: 'Visualiza os teus ingresos e gastos mes a mes.',
        go_to_today: 'Ir a Hoxe',
        projected: 'Proxeccións (Recorrentes)',
        transactions: 'Movementos Reais',
        confirm: 'Confirmar',
        confirm_action: 'Confirmación',

        // Settings Managers
        my_accounts: 'As Miñas Contas/Proxectos',
        create_account: 'Crear Conta/Proxecto',
        account_name_placeholder: 'Nome (ex. Revolut, Proxecto X)',
        initial_balance: 'Saldo Inicial',
        no_accounts: 'Non tes contas/proxectos. Crea unha para comezar.',
        confirm_delete_account: 'Seguro? As transaccións manteranse pero quedarán orfas.',

        recurring_transactions: 'Recorrentes',
        new_recurring: 'Nova Recorrente',
        edit_recurring: 'Editar Recorrente',
        select_account: 'Selecciona Conta',
        select_category: 'Selecciona Categoría',
        day_of_month: 'Día do mes',
        no_recurring: 'Non tes transaccións recorrentes.',
        confirm_delete_recurring: 'Eliminar recorrente?',

        new_category_parent: 'Nova Categoría Principal',
        new_category_child: 'Nova Subcategoría',
        add_subcategory: 'Engadir Subcategoría',
        confirm_delete_category: 'Borrar categoría? Se é pai, borraranse tamén os fillos.',
        // Settings Menu
        settings: 'Configuración',
        profile: 'Perfil',
        appearance: 'Aparencia',
        accounts: 'Contas/Proxectos',
        categories: 'Categorías',
        budgets: 'Orzamentos',
        recurring: 'Recorrentes',
        tags: 'Etiquetas',
        data: 'Datos',
        language: 'Idioma',
        language: 'Idioma',
        version_help: 'Versión/Axuda',
        version_date: 'Febreiro 2026',

        // Profile Settings
        user_profile: 'Perfil de Usuario',
        change_photo: 'Preme para cambiar a foto',
        name: 'Nome',
        your_name: 'O teu Nome',
        save_profile: 'Gardar Perfil',
        saving: 'Gardando...',
        profile_saved: 'Perfil gardado correctamente',

        profile_saved: 'Perfil gardado correctamente',
        customize_home: 'Personalizar Inicio',
        customize_home_desc: 'Amosa "As finanzas de [Nome]" no lugar do texto por defecto.',
        finances_of: 'as finanzas de {name}',

        // Help Guide
        help_financial_title: '1. Xestión Financeira Principal',
        help_dashboard_desc: 'Resumo global do patrimonio, selector temporal e actividade recente.',
        help_transactions_desc: 'Rexistro detallado de ingresos e gastos con buscador avanzado e filtros.',

        help_structure_title: '2. Estrutura Organizativa',
        help_accounts_desc: 'Xestión multi-conta (Banco, Efectivo, Aforros) e proxectos específicos.',
        help_categories_desc: 'Sistema xerárquico con iconas e cores personalizables.',
        help_tags_desc: 'Clasificación transversal (tags) para agrupar gastos de distintas categorías.',

        help_planning_title: '3. Planificación e Automatización',
        help_budgets_desc: 'Límites de gasto mensuais con barras de progreso visuais.',
        help_recurring_desc: 'Automatización de ingresos e gastos fixos (Nómina, Subscricións).',

        help_customization_title: '4. Personalización e Experiencia',
        help_themes_desc: '9 atmosferas únicas (Noite Estrelada, Cyberpunk, Minimalista...).',
        help_profile_desc: 'Personalización de nome, avatar e título de inicio.',
        help_languages_desc: 'Soporte completo para Español, Inglés, Galego e Euskera.',

        help_data_title: '5. Datos e Privacidade',
        help_privacy_desc: 'Todos os datos viven no teu navegador. Cero servidores externos.',
        help_backups_desc: 'Exportación/Importación completa en formato JSON.',
        help_excel_desc: 'Compatible con follas de cálculo para análises externos.',
        help_safe_zone_desc: 'Restablecemento de fábrica dispoñible.',

        // Donation
        donation_title: 'Convídame a un café',
        donation_desc: 'Se Visualis che é útil, podes apoiar o seu desenvolvemento cunha pequena doazón.',
        donate_button: 'Convidar (PayPal)',

        // Theme Settings
        choose_theme: 'Elixe o ambiente para a túa aplicación:',
        theme_names: {
            sky: 'Noite Estrelada',
            gold: 'Eclipse Dourado',
            forest: 'Bosque Profundo',
            nebula: 'Nebulosa Púrpura',
            cyber: 'Futuro Neón',
            wine: 'Viño Selecto',
            coffee: 'Gran Torrado',
            royal: 'Zafiro Real',
            minimal: 'Minimalismo Puro',
        },

        // Currency Settings
        main_currency: 'Moeda Principal',

        // Tag Settings
        manage_tags: 'Xestionar Etiquetas',
        new_tag_placeholder: 'Nova etiqueta (ex. #vacacións)',
        no_tags: 'Non hai etiquetas creadas aínda.',
        confirm_delete_tag: 'Eliminar etiqueta?',

        // Data Settings
        backups: 'Copias de Seguridade',
        export_title: 'Exportar',
        export_desc: 'Descarga unha copia de seguridade dos teus movementos e contas en formato Excel.',
        download_excel: 'Descargar Excel (.xlsx)',
        import_title: 'Importar',
        import_desc: 'Restaura unha copia de seguridade.',
        import_warning: 'Isto borrará os datos actuais',
        select_file: 'Seleccionar Ficheiro (.xlsx)',
        danger_zone: 'Zona de Perigo',
        danger_desc: 'Se necesitas comezar de cero, podes borrar toda a base de datos local. Esta acción é irreversible.',
        nuclear_button: 'Botón Nuclear',

        // Data Alerts
        nuclear_warning_1: '⚠️ ADVERTENCIA NUCLEAR! ⚠️\n\nEstás SEGURO de querer borrar TODOS os datos?\n\nEsta acción eliminará todas as túas transaccións, contas e configuración.\n\nNON HAI VOLTA ATRÁS.',
        nuclear_warning_2: 'De verdade? Confirma unha última vez que queres comezar de cero.',
        import_confirm: '⚠️ Estás seguro de IMPORTAR este ficheiro?\n\n"{fileName}"\n\nELIMINARANSE todos os datos actuais e substituiranse polos do ficheiro.',
        import_success: '✅ Importación completada. Restauráronse {count} transaccións.',
        import_error: '❌ Erro ao importar: ',

        // Category Translations
        category_names: {
            // Income
            'Alquiler': 'Aluguer',
            'Devoluciones': 'Devolucións',
            'Dividendos': 'Dividendos',
            'Negocio': 'Negocio',
            'Regalos': 'Agasallos',
            'Sueldo': 'Soldo',
            'Wallapop-Vinted': 'Segunda Man',
            'Recuperación': 'Recuperación',
            'Alquiler Vacacional': 'Aluguer Vacacional',
            'Intereses': 'Intereses',
            'Negocio VUT': 'Negocio VUT',
            'Otro Negocio': 'Outro Negocio',
            'Nómina': 'Nómina',
            'Desempleo': 'Desemprego',
            'Ventas': 'Vendas',
            'Otros': 'Outros',

            // Expenses
            'Automóvil': 'Automóbil',
            'Bancos': 'Bancos',
            'Compras': 'Compras',
            'Deporte': 'Deporte',
            'Formación': 'Formación',
            'Limpieza': 'Limpeza',
            'Moda': 'Moda',
            'Ocio': 'Lecer',
            'Salud': 'Saúde',
            'Suministros': 'Subministracions',
            'Transporte': 'Transporte',
            'Viajes': 'Viaxes',
            'Mascotas': 'Mascotas',

            'Combustible': 'Combustible',
            'Mantenimiento': 'Mantemento',
            'Multas': 'Multas',
            'Parking': 'Párking',
            'Peajes': 'Peaxes',
            'Otros gastos automóvil': 'Outros gastos automóbil',
            'Hipoteca': 'Hipoteca',
            'Préstamo': 'Préstamo',
            'Comisiones': 'Comisións',
            'Otras deudas': 'Outras débedas',
            'Electrónica': 'Electrónica',
            'Oficina': 'Oficina',
            'Otras': 'Outras',
            'Reparaciones': 'Reparacións',
            'Supermercado': 'Supermercado',
            'Carreras/Tr': 'Carreiras/Tr',
            'Club': 'Club',
            'Gimnasio': 'Ximnasio',
            'Curso': 'Curso',
            'Libros/Comic': 'Libros/Cómic',
            'Suscripcion': 'Subscrición',
            'Lavandería': 'Lavandaría',
            'Calzado': 'Calzado',
            'Ropa Deportiva': 'Roupa Deportiva',
            'Ropa Vestir': 'Roupa de Vestir',
            'Bar': 'Bar',
            'Cafés': 'Cafés',
            'Restaurante': 'Restaurante',
            'Farmacia': 'Farmacia',
            'Peluquería': 'Peiteado',
            'Médico': 'Médico',
            'Salud y Belleza': 'Saúde e Beleza',
            'Agua': 'Auga',
            'Luz': 'Luz',
            'Comunidad': 'Comunidade',
            'Electricidad': 'Electricidade',
            'Gas': 'Gas',
            'Impuestos': 'Impostos',
            'Internet': 'Internet',
            'Seguros': 'Seguros',
            'Telefono': 'Teléfono',
            'Otros Suministros': 'Outras Subministracions',
            'Bus': 'Bus',
            'Metro': 'Metro',
            'Taxi': 'Taxi',
            'Tren': 'Tren',
            'Uber-Cabify': 'VTC',
            'Entradas': 'Entradas',
            'Hoteles': 'Hoteis',
            'Veterinario': 'Veterinario',
            'Mascota': 'Mascota'
        }
    },
    eu: {
        app_title: 'VISUALIS',
        app_subtitle: 'zure finantzak',
        dashboard_recent_activity: 'Azken Jarduera',
        dashboard_monthly_budget: 'Hileko Aurrekontua',
        total_balance: 'Balantze Osoa',
        income: 'Diru-sarrerak',
        expense: 'Gastuak',
        result: 'Emaitza',
        month: 'Hilabetea',
        settings: 'Ezarpenak',
        profile: 'Profila',
        accounts: 'Kontuak/Proiektuak',
        categories: 'Kategoriak',
        recurring: 'Errepikakorrak',
        data: 'Datuak',
        theme: 'Gaia',
        language: 'Hizkuntza',
        select_language: 'Hautatu zure hizkuntza',
        save: 'Gorde',
        cancel: 'Utzi',
        delete: 'Ezabatu',
        edit: 'Editatu',
        new_transaction: 'Transakzio Berria',
        edit_transaction: 'Editatu Transakzioa',
        amount: 'Zenbatekoa',
        date: 'Data',
        wallet: 'Kontua',
        category: 'Kategoria',
        description: 'Deskribapena',
        tags: 'Etiketak',
        export_excel: 'Deskargatu Excel',
        import_excel: 'Inportatu Excel',
        reset_data: 'Ezabatu Guztia',
        danger_zone: 'Arrisku Eremua',
        warning_nuclear: '⚠️ OHAR NUKLEARRA! ⚠️',
        confirm_nuclear: 'Ziur zaude datu GUZTIAK ezabatu nahi dituzula?',
        nuclear_button: 'Botoi Nuklearra',

        // New Data Settings
        security_title: 'Segurtasuna',
        backup_create: 'Sortu Segurtasun Kopia',
        backup_desc: 'Gorde zure datu guztien fitxategi oso bat, geroago berreskuratu ahal izateko gailuz aldatzen baduzu edo nabigatzailea garbitzen baduzu.',
        restore_title: 'Berreskuratu Kopia',
        restore_desc: 'Berreskuratu zure datuak segurtasun kopia fitxategi batetik.',
        restore_confirm: '⚠️ Segurtasun kopia berreskuratu? HONEK ORAINGO DATU GUZTIAK ORDEZKATUKO DITU.',
        excel_data_title: 'Excel Datuak',
        excel_data_desc: 'Zure datuekin kanpoko kalkulu-orrietan lan egiteko tresnak.',
        json_backup_title: 'Segurtasun Kopia (JSON)',
        json_restore_success: '✅ Segurtasun kopia ondo berreskuratu da.',
        json_restore_error: '❌ Errorea kopia berreskuratzean: ',

        // Advanced Search
        transaction_history: 'Historia Osoa',
        search_placeholder: 'Bilatu kontzeptu, kategoria, oharrez...',
        filters: 'Iragazkiak',
        clear_filters: 'Garbitu',
        filter_by: 'Iragazi honela',
        type: 'Mota',
        all: 'Guztiak',
        date: 'Data',
        see_all: 'Ikusi Guztia',
        no_transactions_found: 'Ez da transakziorik aurkitu.',
        try_adjusting_filters: 'Saiatu iragazkiak aldatzen.',
        confirm: 'Baieztatu',
        confirm_action: 'Baieztapena',

        // Settings Managers
        my_accounts: 'Nire Kontuak/Proiektuak',
        create_account: 'Sortu Kontua/Proiektua',
        account_name_placeholder: 'Izena (adib. Revolut, Proiektua X)',
        initial_balance: 'Hasierako Saldoa',
        no_accounts: 'Ez daukazu konturik/proiekturik. Sortu bat hasteko.',
        confirm_delete_account: 'Ziur zaude? Transakzioak mantenduko dira baina umezurtz geratuko dira.',

        recurring_transactions: 'Errepikakorrak',
        new_recurring: 'Errepikakor Berria',
        edit_recurring: 'Editatu Errepikakorra',
        select_account: 'Hautatu Kontua',
        select_category: 'Hautatu Kategoria',
        day_of_month: 'Hileko eguna',
        no_recurring: 'Ez daukazu transakzio errepikakorrik.',
        confirm_delete_recurring: 'Ezabatu errepikakorra?',

        new_category_parent: 'Kategoria Nagusi Berria',
        new_category_child: 'Azpikategoria Berria',
        add_subcategory: 'Gehitu Azpikategoria',
        confirm_delete_category: 'Kategoria ezabatu? Nagusia bada, semeak ere ezabatuko dira.',
        // Settings Menu
        settings: 'Ezarpenak',
        profile: 'Profila',
        appearance: 'Itxura',
        accounts: 'Kontuak/Proiektuak',
        categories: 'Kategoriak',
        budgets: 'Aurrekontuak',
        recurring: 'Errepikakorrak',
        tags: 'Etiketak',
        data: 'Datuak',
        language: 'Hizkuntza',
        version_help: 'Bertsioa/Laguntza',
        version_date: '2026ko Otsaila',

        // Profile Settings
        user_profile: 'Erabiltzaile Profila',
        change_photo: 'Sakatu argazkia aldatzeko',
        name: 'Izena',
        your_name: 'Zure Izena',
        save_profile: 'Gorde Profila',
        saving: 'Gordetzen...',
        profile_saved: 'Profila ondo gorde da',

        // Theme Settings
        choose_theme: 'Aukeratu aplikazioaren giroa:',
        theme_names: {
            sky: 'Gau Izartsua',
            gold: 'Eklipse Urreztatua',
            forest: 'Baso Sakona',
            nebula: 'Nebulosa Morea',
            cyber: 'Etorkizun Neona',
            wine: 'Ardo Hautatua',
            coffee: 'Ale Txigortua',
            royal: 'Zafiro Erreala',
            minimal: 'Minimalismo Hutsa',
        },

        // Currency Settings
        main_currency: 'Moneta Nagusia',

        // Tag Settings
        manage_tags: 'Kudeatu Etiketak',
        new_tag_placeholder: 'Etiketa berria (adib. #oporrak)',
        no_tags: 'Ez dago etiketarik oraindik.',
        confirm_delete_tag: 'Etiketa ezabatu?',

        // Data Settings
        backups: 'Segurtasun Kopiak',
        export_title: 'Esportatu',
        export_desc: 'Deskargatu zure mugimendu, kontu eta kategorien segurtasun kopia Excel formatuan.',
        download_excel: 'Deskargatu Excel (.xlsx)',
        import_title: 'Inportatu',
        import_desc: 'Berreskuratu segurtasun kopia.',
        import_warning: 'Honek oraingo datuak ezabatuko ditu',
        select_file: 'Hautatu Fitxategia (.xlsx)',
        danger_zone: 'Arrisku Eremua',
        danger_desc: 'Hutsetik hasi behar baduzu, tokiko datu-base osoa ezabatu dezakezu. Ekintza hau itzulezina da.',
        nuclear_button: 'Botoi Nuklearra',

        // Data Alerts
        nuclear_warning_1: '⚠️ OHAR NUKLEARRA! ⚠️\n\nZiur zaude datu GUZTIAK ezabatu nahi dituzula?\n\nEkintza honek transakzio, kontu, aurrekontu eta ezarpen guztiak ezabatuko ditu.\n\nEZ DAGO ATZERA BUELTARIK.',
        nuclear_warning_2: 'Benetan? Baieztatu azken aldiz hutsetik hasi nahi duzula.',
        import_confirm: '⚠️ Ziur zaude fitxategi hau INPORTATU nahi duzula?\n\n"{fileName}"\n\nOraingo datu guztiak EZABATUKO dira eta fitxategikoekin ordezkatuko dira.',
        import_success: '✅ Inportazioa burututa. {count} transakzio berreskuratu dira.',
        import_error: '❌ Inportazio errorea: ',

        // Category Translations
        category_names: {
            // Income
            'Alquiler': 'Alokairua',
            'Devoluciones': 'Itzultzeak',
            'Dividendos': 'Dibidenduak',
            'Negocio': 'Negozioa',
            'Regalos': 'Opariak',
            'Sueldo': 'Soldata',
            'Wallapop-Vinted': 'Bigarren Eskua',
            'Recuperación': 'Berreskuratzea',
            'Alquiler Vacacional': 'Oporretako Alokairua',
            'Intereses': 'Interesak',
            'Negocio VUT': 'Negozio VUT',
            'Otro Negocio': 'Beste Negozio Bat',
            'Nómina': 'Nomina',
            'Desempleo': 'Langabezia',
            'Ventas': 'Salmentak',
            'Otros': 'Besteak',

            // Expenses
            'Automóvil': 'Automobila',
            'Bancos': 'Bankuak',
            'Compras': 'Erosketak',
            'Deporte': 'Kirola',
            'Formación': 'Prestakuntza',
            'Limpieza': 'Garbiketa',
            'Moda': 'Moda',
            'Ocio': 'Aisia',
            'Salud': 'Osasuna',
            'Suministros': 'Hornidurak',
            'Transporte': 'Garraioa',
            'Viajes': 'Bidaiak',
            'Mascotas': 'Maskotak',

            'Combustible': 'Erregaia',
            'Mantenimiento': 'Mantentzea',
            'Multas': 'Isunak',
            'Parking': 'Aparkalekua',
            'Peajes': 'Bidesariak',
            'Otros gastos automóvil': 'Beste gastu batzuk',
            'Hipoteca': 'Hipoteka',
            'Préstamo': 'Mailegua',
            'Comisiones': 'Komisioak',
            'Otras deudas': 'Beste zor batzuk',
            'Electrónica': 'Elektronika',
            'Oficina': 'Bulegoa',
            'Otras': 'Besteak',
            'Reparaciones': 'Konponketak',
            'Supermercado': 'Supermerkatua',
            'Carreras/Tr': 'Lasterketak',
            'Club': 'Kluba',
            'Gimnasio': 'Gimnasioa',
            'Curso': 'Ikastaroa',
            'Libros/Comic': 'Liburuak',
            'Suscripcion': 'Harpidetza',
            'Lavandería': 'Garbigailua',
            'Calzado': 'Oinetakoak',
            'Ropa Deportiva': 'Kirol Arropa',
            'Ropa Vestir': 'Janzteko Arropa',
            'Bar': 'Taberna',
            'Cafés': 'Kafeak',
            'Restaurante': 'Jatetxea',
            'Farmacia': 'Farmazia',
            'Peluquería': 'Ileapaindegia',
            'Médico': 'Medikua',
            'Salud y Belleza': 'Osasuna eta Edertasuna',
            'Agua': 'Ura',
            'Luz': 'Argia',
            'Comunidad': 'Komunitatea',
            'Electricidad': 'Elektrizitatea',
            'Gas': 'Gasa',
            'Impuestos': 'Zergak',
            'Internet': 'Internet',
            'Seguros': 'Aseguruak',
            'Telefono': 'Telefonoa',
            'Otros Suministros': 'Beste Hornidura Batzuk',
            'Bus': 'Autobusa',
            'Metro': 'Metroa',
            'Taxi': 'Taxia',
            'Tren': 'Trena',
            'Uber-Cabify': 'VTC',
            'Entradas': 'Sarrerak',
            'Hoteles': 'Hotelak',
            'Veterinario': 'Albaitaria',
            'Mascota': 'Maskota'
        }
    },
    ca: {
        app_title: 'VISUALIS',
        app_subtitle: 'les teves finances',
        dashboard_recent_activity: 'Activitat Recent',
        dashboard_monthly_budget: 'Pressupost del Mes',
        total_balance: 'Balanç Total',
        income: 'Ingressos',
        expense: 'Despeses',
        result: 'Resultat',
        month: 'Mes',
        settings: 'Configuració',
        profile: 'Perfil',
        accounts: 'Comptes/Projectes',
        categories: 'Categories',
        recurring: 'Recurrents',
        data: 'Dades',
        theme: 'Tema',
        language: 'Idioma',
        select_language: 'Selecciona el teu idioma',
        save: 'Desar',
        cancel: 'Cancel·lar',
        delete: 'Eliminar',
        edit: 'Editar',
        new_transaction: 'Nova Transacció',
        edit_transaction: 'Editar Transacció',
        amount: 'Quantitat',
        date: 'Data',
        wallet: 'Compte',
        category: 'Categoria',
        description: 'Descripció',
        tags: 'Etiquetes',
        export_excel: 'Descarregar Excel',
        import_excel: 'Importar Excel',
        reset_data: 'Esborrar Tot',
        danger_zone: 'Zona de Perill',
        warning_nuclear: '⚠️ ADVERTÈNCIA NUCLEAR! ⚠️',
        confirm_nuclear: 'Estàs SEGUR de voler esborrar TOTES les dades?',
        nuclear_button: 'Botó Nuclear',
        confirm: 'Confirmar',
        confirm_action: 'Confirmació',

        // Settings Managers
        my_accounts: 'Els Meus Comptes/Projectes',
        create_account: 'Crear Compte/Projecte',
        account_name_placeholder: 'Nom (ex. Revolut, Projecte X)',
        initial_balance: 'Balanç Inicial',
        no_accounts: 'No tens comptes/projectes. Crea\'n un per començar.',
        confirm_delete_account: 'Segur que vols esborrar? Les transaccions es mantindran però quedaran òrfenes.',

        recurring_transactions: 'Recurrents',
        new_recurring: 'Nova Recurrent',
        edit_recurring: 'Editar Recurrent',
        select_account: 'Selecciona Compte',
        select_category: 'Selecciona Categoria',
        day_of_month: 'Dia del mes',
        no_recurring: 'No tens transaccions recurrents.',
        confirm_delete_recurring: 'Eliminar recurrent?',

        new_category_parent: 'Nova Categoria Principal',
        new_category_child: 'Nova Subcategoria',
        add_subcategory: 'Afegir Subcategoria',
        confirm_delete_category: 'Esborrar categoria? Si és pare, s\'esborraran també els fills.',
        // Settings Menu
        settings: 'Configuració',
        profile: 'Perfil',
        appearance: 'Aparença',
        accounts: 'Comptes',
        categories: 'Categories',
        budgets: 'Pressupostos',
        recurring: 'Recurrents',
        tags: 'Etiquetes',
        data: 'Dades',
        language: 'Idioma',
        version_help: 'Versió/Ajuda',
        version_date: 'Febrer 2026',

        // Profile Settings
        user_profile: 'Perfil d\'Usuari',
        change_photo: 'Prem per canviar la foto',
        name: 'Nom',
        your_name: 'El teu Nom',
        save_profile: 'Desar Perfil',
        saving: 'Desant...',
        profile_saved: 'Perfil desat correctament',

        // Theme Settings
        choose_theme: 'Tria l\'ambient per a la teva aplicació:',
        theme_names: {
            sky: 'Nit Estrellada',
            gold: 'Eclipsi Daurat',
            forest: 'Bosc Profund',
            nebula: 'Nebulosa Púrpura',
            cyber: 'Futur Neó',
            wine: 'Vi Selecte',
            coffee: 'Gra Torrat',
            royal: 'Safir Reial',
            minimal: 'Minimalisme Pur',
        },

        // Currency Settings
        main_currency: 'Moneda Principal',

        // Tag Settings
        manage_tags: 'Gestionar Etiquetes',
        new_tag_placeholder: 'Nova etiqueta (ex. #vacances)',
        no_tags: 'No hi ha etiquetes creades encara.',
        confirm_delete_tag: 'Eliminar etiqueta?',

        // Data Settings
        backups: 'Còpies de Seguretat',
        export_title: 'Exportar',
        export_desc: 'Descarrega una còpia de seguretat dels teus moviments i comptes en format Excel.',
        download_excel: 'Descarregar Excel (.xlsx)',
        import_title: 'Importar',
        import_desc: 'Restaura una còpia de seguretat.',
        import_warning: 'Això esborrarà les dades actuals',
        select_file: 'Seleccionar Fitxer (.xlsx)',
        danger_zone: 'Zona de Perill',
        danger_desc: 'Si necessites començar de zero, pots esborrar tota la base de dades local. Aquesta acció és irreversible.',
        nuclear_button: 'Botó Nuclear',

        // Data Alerts
        nuclear_warning_1: '⚠️ ADVERTÈNCIA NUCLEAR! ⚠️\n\nEstàs SEGUR de voler esborrar TOTES les dades?\n\nAquesta acció eliminarà totes les teves transaccions, comptes i configuració.\n\nNO HI HA TORNADA ENRERE.',
        nuclear_warning_2: 'De veritat? Confirma una última vegada que vols començar de zero.',
        import_confirm: '⚠️ Estàs segur d\'IMPORTAR aquest fitxer?\n\n"{fileName}"\n\nS\'ELIMINARAN totes les dades actuals i es reemplaçaran per les del fitxer.',
        import_success: '✅ Importació completada. S\'han restaurat {count} transaccions.',
        import_error: '❌ Error en importar: ',

        // Category Translations
        category_names: {
            // Income
            'Alquiler': 'Lloguer',
            'Devoluciones': 'Devolucions',
            'Dividendos': 'Dividends',
            'Negocio': 'Negoci',
            'Regalos': 'Regals',
            'Sueldo': 'Sou',
            'Wallapop-Vinted': 'Vendes Sg.Mà',
            'Recuperación': 'Recuperació',
            'Alquiler Vacacional': 'Lloguer Vacacional',
            'Intereses': 'Interessos',
            'Negocio VUT': 'Negoci VUT',
            'Otro Negocio': 'Altre Negoci',
            'Nómina': 'Nòmina',
            'Desempleo': 'Atur',
            'Ventas': 'Vendes',
            'Otros': 'Altres',

            // Expenses
            'Automóvil': 'Automòbil',
            'Bancos': 'Bancs',
            'Compras': 'Compres',
            'Deporte': 'Esport',
            'Formación': 'Formació',
            'Limpieza': 'Neteja',
            'Moda': 'Moda',
            'Ocio': 'Oci',
            'Salud': 'Salut',
            'Suministros': 'Subministraments',
            'Transporte': 'Transport',
            'Viajes': 'Viatges',
            'Mascotas': 'Mascotes',

            'Combustible': 'Combustible',
            'Mantenimiento': 'Manteniment',
            'Multas': 'Multes',
            'Parking': 'Pàrquing',
            'Peajes': 'Peatges',
            'Otros gastos automóvil': 'Altres despeses automòbil',
            'Hipoteca': 'Hipoteca',
            'Préstamo': 'Préstec',
            'Comisiones': 'Comissions',
            'Otras deudas': 'Altres deutes',
            'Electrónica': 'Electrònica',
            'Oficina': 'Oficina',
            'Otras': 'Altres',
            'Reparaciones': 'Reparacions',
            'Supermercado': 'Supermercat',
            'Carreras/Tr': 'Curses/Tr',
            'Club': 'Club',
            'Gimnasio': 'Gimnàs',
            'Curso': 'Curs',
            'Libros/Comic': 'Llibres/Còmic',
            'Suscripcion': 'Subscripció',
            'Lavandería': 'Bugaderia',
            'Calzado': 'Calçat',
            'Ropa Deportiva': 'Roba Esportiva',
            'Ropa Vestir': 'Roba de Vestir',
            'Bar': 'Bar',
            'Cafés': 'Cafès',
            'Restaurante': 'Restaurant',
            'Farmacia': 'Farmàcia',
            'Peluquería': 'Perruqueria',
            'Médico': 'Metge',
            'Salud y Belleza': 'Salut i Bellesa',
            'Agua': 'Aigua',
            'Luz': 'Llum',
            'Comunidad': 'Comunitat',
            'Electricidad': 'Electricitat',
            'Gas': 'Gas',
            'Impuestos': 'Impostos',
            'Internet': 'Internet',
            'Seguros': 'Assegurances',
            'Telefono': 'Telèfon',
            'Otros Suministros': 'Altres Subministraments',
            'Bus': 'Bus',
            'Metro': 'Metro',
            'Taxi': 'Taxi',
            'Tren': 'Tren',
            'Uber-Cabify': 'VTC',
            'Entradas': 'Entrades',
            'Hoteles': 'Hotels',
            'Veterinario': 'Veterinari',
            'Mascota': 'Mascota'
        }
    },
}

// ----------------------------------------------------------------------
// CURRENCIES
// ----------------------------------------------------------------------
export const CURRENCIES = [
    { code: 'EUR', name: 'Euro (€)', symbol: '€' },
    { code: 'USD', name: 'US Dollar ($)', symbol: '$' },
    { code: 'GBP', name: 'British Pound (£)', symbol: '£' },
    { code: 'JPY', name: 'Japanese Yen (¥)', symbol: '¥' },
    { code: 'CNY', name: 'Chinese Yuan (¥)', symbol: 'CN¥' },
    { code: 'AUD', name: 'Australian Dollar (A$)', symbol: 'A$' },
    { code: 'CAD', name: 'Canadian Dollar (C$)', symbol: 'C$' },
    { code: 'CHF', name: 'Swiss Franc (CHF)', symbol: 'CHF' },
    { code: 'HKD', name: 'Hong Kong Dollar (HK$)', symbol: 'HK$' },
]

// ----------------------------------------------------------------------
// CONTEXT
// ----------------------------------------------------------------------
const LanguageContext = createContext()

export function LanguageProvider({ children }) {
    const [language, setLanguageState] = useState('es')
    const [currency, setCurrencyState] = useState('EUR')
    const [isLoaded, setIsLoaded] = useState(false)

    useEffect(() => {
        const loadSettings = async () => {
            try {
                const settings = await db.settings.get('global')

                // Language
                if (settings?.language) {
                    setLanguageState(settings.language)
                } else {
                    const browserLang = navigator.language.split('-')[0]
                    if (['es', 'en', 'gl', 'eu', 'ca'].includes(browserLang)) {
                        setLanguageState(browserLang)
                    } else {
                        setLanguageState('es')
                    }
                }

                // Currency
                if (settings?.currency) {
                    setCurrencyState(settings.currency)
                }
            } catch (e) {
                console.error("Failed to load settings:", e)
            } finally {
                setIsLoaded(true)
            }
        }
        loadSettings()
    }, [])

    const setLanguage = async (lang) => {
        setLanguageState(lang)
        try {
            const settings = await db.settings.get('global') || { id: 'global' }
            await db.settings.put({ ...settings, language: lang })
        } catch (e) {
            console.error("Failed to save language:", e)
        }
    }

    const setCurrency = async (curr) => {
        setCurrencyState(curr)
        try {
            const settings = await db.settings.get('global') || { id: 'global' }
            await db.settings.put({ ...settings, currency: curr })
        } catch (e) {
            console.error("Failed to save currency:", e)
        }
    }

    const t = (key) => {
        return dictionaries[language]?.[key] || dictionaries['es'][key] || key
    }

    // Helper for categories
    const tCategory = (name) => {
        if (!name) return ''
        const dict = dictionaries[language]
        return dict?.category_names?.[name] || dictionaries['es']?.category_names?.[name] || name
    }

    // Helper to format currency dynamically
    const formatMoney = (amount, currencyCode = null) => {
        return new Intl.NumberFormat(language === 'en' ? 'en-US' : 'es-ES', {
            style: 'currency',
            currency: currencyCode || currency,
        }).format(amount)
    }

    const symbol = CURRENCIES.find(c => c.code === currency)?.symbol || currency

    const locales = { es, en: enUS, gl, eu, ca }
    const locale = locales[language] || es

    return (
        <LanguageContext.Provider value={{ language, setLanguage, currency, setCurrency, symbol, t, tCategory, formatMoney, isLoaded, locale }}>
            {children}
        </LanguageContext.Provider>
    )
}

export const useLanguage = () => useContext(LanguageContext)

'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { db } from '@/lib/db'
import { es, enUS, gl, eu, ca } from 'date-fns/locale'

const dictionaries = {
    "es": {
        "app_title": "VISUALIS",
        "app_subtitle": "Tus finanzas fáciles",
        "meta_title": "Visualis | tus Finanzas",
        "dashboard_recent_activity": "Actividad Reciente",
        "dashboard_monthly_budget": "Presupuesto del Mes",
        "total_balance": "Balance Total",
        "income": "Ingresos",
        "expense": "Gastos",
        "result": "Resultado",
        "transfer": "Traspaso",
        "month": "mes",
        "week": "semana",
        "settings": "Configuración",
        "profile": "Perfil",
        "accounts": "Cuentas/Proyectos",
        "categories": "Categorías",
        "recurring": "Recurrentes",
        "data": "Datos",
        "theme": "Tema",
        "language": "Idioma",
        "select_language": "Selecciona tu idioma",
        "save": "Guardar",
        "cancel": "Cancelar",
        "delete": "Eliminar",
        "edit": "Editar",
        "new_transaction": "Nueva Transacción",
        "edit_transaction": "Editar Transacción",
        "amount": "Cantidad",
        "date": "Fecha",
        "wallet": "Cuenta",
        "category": "Categoría",
        "category_name": "Nombre de la Categoría",
        "color": "Color",
        "icon": "Icono",
        "description": "Descripción",
        "tags": "Etiquetas",
        "export_excel": "Descargar Excel",
        "import_excel": "Importar Excel",
        "reset_data": "Borrar Todo",
        "danger_zone": "Zona de Peligro",
        "warning_nuclear": "⚠️ ¡ADVERTENCIA NUCLEAR! ⚠️",
        "confirm_nuclear": "¿Estás SEGURO de querer borrar TODOS los datos?",
        "nuclear_button": "Botón Nuclear",
        "global_total": "TOTAL GLOBAL",
        "net_worth": "Patrimonio",
        "monthly_variation": "Variación Mensual",
        "total": "Total",
        "this_month": "Este Mes",
        "no_recent_transactions": "No hay movimientos recientes",
        "uncategorized": "Sin categoría",
        "budgets": "Presupuestos",
        "monthly_total": "Total Mensual",
        "no_expenses_this_month": "No hay gastos este mes.",
        "of": "de",
        "select_wallet": "Selecciona cuenta",
        "select_destination": "Selecciona destino",
        "wallet_source": "Cuenta Origen",
        "wallet_destination": "Cuenta Destino",
        "change": "Cambiar",
        "back_to_categories": "Volver a Categorías",
        "optional_note": "Nota opcional...",
        "update": "Actualizar",
        "confirm_delete_transaction": "¿Seguro que quieres eliminar esta transacción?",
        "validation_amount": "Por favor, indica la cantidad.",
        "validation_wallet": "Por favor, selecciona una cuenta (Efectivo, Banco, etc).",
        "validation_category": "Por favor, selecciona una categoría.",
        "validation_amount_invalid": "La cantidad no es válida.",
        "validation_date_invalid": "La fecha seleccionada no es válida.",
        "error_saving": "Error al guardar",
        "error_deleting": "Error al eliminar",
        "confirm": "Confirmar",
        "confirm_action": "Confirmación",
        "confirm_delete_transaction_desc": "¿Estás seguro de que quieres eliminar esta transacción? Esta acción no se puede deshacer y el saldo de la cuenta se actualizará.",
        "my_accounts": "Mis Cuentas/Proyectos",
        "create_account": "Crear Cuenta/Proyecto",
        "account_name_placeholder": "Nombre (ej. Revolut, Proyecto X)",
        "initial_balance": "Saldo Inicial",
        "no_accounts": "No tienes cuentas/proyectos. Crea una para empezar.",
        "confirm_delete_account": "¿Seguro que quieres borrar esta cuenta? Se mantendrán las transacciones pero quedarán huérfanas.",
        "recurring_transactions": "Recurrentes",
        "notifications_title": "Activar Notificaciones",
        "notifications_desc": "Para que podamos recordarte tus hábitos y transacciones recurrentes, necesitamos tu permiso para mostrar notificaciones en este dispositivo.",
        "notifications_btn": "Permitir Notificaciones",
        "notifications_cancel": "Más tarde",
        "notifications_granted": "¡Listo! Las notificaciones están activas.",
        "notifications_denied": "Las notificaciones están bloqueadas. Puedes cambiarlas en los ajustes de tu navegador.",
        "new_recurring": "Nueva Recurrente",
        "edit_recurring": "Editar Recurrente",
        "select_account": "Selecciona Cuenta",
        "select_category": "Selecciona Categoría",
        "day_of_month": "Día del mes",
        "no_recurring": "No tienes transacciones recurrentes.",
        "confirm_delete_recurring": "¿Eliminar recurrencia?",
        "make_recurring": "Hacer recurrente",
        "make_recurring_desc_expense": "Se creará un gasto fijo mensual.",
        "make_recurring_desc_income": "Se creará un ingreso fijo mensual.",
        "recurring_added": "Recurrencia creada correctamente",
        "new_category_parent": "Nueva Categoría Principal",
        "new_category_child": "Nueva Subcategoría",
        "add_subcategory": "Añadir Subcategoría",
        "confirm_delete_category": "¿Borrar categoría? Si es padre, se borrarán también sus hijos.",
        "move_transactions": "Mover movimientos a…",
        "move_and_delete": "Mover y eliminar",
        "category_to_delete": "A eliminar",
        "subcategory_to_delete": "Subcategoría a eliminar",
        "appearance": "Apariencia",
        "version_help": "Versión/Ayuda",
        "version_date": "Marzo 2026 (v1.4.25)",
        "user_profile": "Perfil de Usuario",
        "change_photo": "Pulsa para cambiar la foto",
        "name": "Nombre",
        "your_name": "Tu Nombre",
        "save_profile": "Guardar Perfil",
        "saving": "Guardando...",
        "profile_saved": "Perfil guardado correctamente",
        "customize_home": "Personalizar Inicio",
        "customize_home_desc": "Muestra \"Las finanzas de [Nombre]\" en lugar del texto por defecto.",
        "finances_of": "las finanzas de {name}",
        "help_financial_title": "Gestión Financiera",
        "help_dashboard_desc": "Visión global de tu patrimonio and actividad reciente.",
        "help_calendar_title": "Vista de Calendario",
        "help_calendar_help_desc": "Visualiza tus gastos e ingresos diarios y previsiones en un calendario mensual.",
        "help_transactions_desc": "Registro detallado de ingresos y gastos con buscador avanzado.",
        "help_split_title": "Transacciones Divididas",
        "help_split_desc": "Divide un ticket único en múltiples categorías (ej. Supermercado -> Alimentación + Limpieza).",
        "help_context_title": "Contexto Inteligente",
        "help_context_desc": "El botón \"+\" detecta si estás en Ingresos o Gastos y se adapta automáticamente.",
        "help_emotional_title": "Gasto Emocional",
        "help_emotional_desc": "Registra cómo te sentiste (😍, 😐, 😠) para entender tus hábitos.",
        "help_structure_title": "Estructura",
        "help_accounts_desc": "Gestiona múltiples cuentas (bancos, efectivo, tarjetas).",
        "help_categories_desc": "Organiza tus movimientos en categorías y subcategorías.",
        "help_tags_desc": "Etiqueta transacciones para agrupar conceptos transversales (#Viaje).",
        "help_planning_title": "Planificación",
        "help_budgets_desc": "Establece límites de gasto mensual por categoría.",
        "help_recurring_desc": "Configura movimientos fijos automáticos (alquiler, nómina).",
        "help_customization_title": "Personalización",
        "help_themes_desc": "Elige entre múltiples temas visuales.",
        "help_profile_desc": "Personaliza tu nombre y avatar.",
        "help_languages_desc": "Cambia el idioma de la aplicación.",
        "help_data_title": "Datos y Privacidad",
        "help_security_title": "Seguridad",
        "help_privacy_desc": "Tus datos nunca salen de tu dispositivo (Local First).",
        "help_privacy_mode_title": "Modo Privacidad",
        "help_privacy_mode_desc": "Oculta los saldos sensibles con un clic para mayor discreción.",
        "help_backups_desc": "Exporta e importa tus datos en formato JSON.",
        "help_excel_desc": "Compatible con hojas de cálculo para análisis externos.",
        "help_safe_zone_desc": "Restablecimiento de fábrica disponible.",
        "donation_title": "Invítame a un café",
        "donation_desc": "Si Visualis te es útil, puedes apoyar su desarrollo con una pequeña donación.",
        "donate_button": "Invitar (PayPal)",
        "suggestions_title": "Sugerencias y Errores",
        "suggestions_desc": "Si tienes sugerencias que hacerme o errores que corregir, escríbeme a:",
        "choose_theme": "Elige el ambiente para tu aplicación:",
        "theme_names": {
            "sky": "Noche Estrellada",
            "forest": "Bosque Profundo",
            "nebula": "Nebulosa Púrpura",
            "mondrian": "Estilo Mondrian",
            "wine": "Vino Selecto",
            "light-sky": "Cielo Ártico",
            "light-mint": "Oasis Esmeralda",
            "light-warm": "Horizonte Ámbar",
            "pop-art": "Pop Art"
        },
        "main_currency": "Moneda Principal",
        "manage_tags": "Gestionar Etiquetas",
        "new_tag_placeholder": "Nueva etiqueta (ej. #vacaciones)",
        "no_tags": "No hay etiquetas creadas aún.",
        "confirm_delete_tag": "¿Eliminar etiqueta?",
        "backups": "Copias de Seguridad",
        "export_title": "Exportar",
        "export_desc": "Descarga una copia de seguridad de tus movimientos, cuentas y categorías en formato Excel.",
        "download_excel": "Descargar Excel (.xlsx)",
        "import_title": "Importar",
        "import_desc": "Restaura una copia de seguridad.",
        "import_warning": "Esto borrará los datos actuales",
        "select_file": "Seleccionar Archivo (.xlsx)",
        "danger_desc": "Si necesitas empezar de cero, puedes borrar toda la base de datos local. Esta acción es irreversible.",
        "security_title": "Security",
        "backup_create": "Crear Copia de Seguridad",
        "backup_desc": "Guarda un archivo completo de todos tus datos para poder restaurarlos más tarde si cambias de dispositivo o borras el navegador.",
        "restore_title": "Restaurar Copia",
        "restore_desc": "Recupera tus datos desde un archivo de copia de seguridad.",
        "restore_confirm": "⚠️ ¿Restaurar copia de seguridad? ESTO SOBRESCRIBIRÁ TODOS LOS DATOS ACTUALES.",
        "excel_data_title": "Datos Excel",
        "excel_data_desc": "Herramientas para trabajar con tus datos en hojas de cálculo externas.",
        "json_backup_title": "Copia de Seguridad (JSON)",
        "json_restore_success": "✅ Copia de seguridad restaurada correctamente.",
        "json_restore_error": "❌ Error al restaurar la copia: ",
        "nuclear_warning_1": "⚠️ ¡ADVERTENCIA NUCLEAR! ⚠️\n\n¿Estás SEGURO de querer borrar TODOS los datos?\n\nEsta acción eliminará todas tus transacciones, cuentas, presupuestos y configuración.\n\nNO HAY VUELTA ATRÁS.",
        "nuclear_warning_2": "¿De verdad? Confirma una última vez que quieres empezar de cero.",
        "import_confirm": "⚠️ ¿Estás seguro de IMPORTAR este archivo?\n\n\"{fileName}\"\n\nSe ELIMINARÁN todos los datos actuales y se reemplazarán por los del archivo.",
        "import_success": "✅ Importación completada. Se han restaurado {count} transacciones.",
        "import_error": "❌ Error al importar: ",
        "advanced_search": "Búsqueda avanzada",
        "transaction_history": "Historial Completo",
        "search_placeholder": "Buscar por concepto, categoría, nota...",
        "filters": "Filtros",
        "clear_filters": "Limpiar",
        "filter_by": "Filtrar por",
        "type": "Tipo",
        "all": "Todos",
        "see_all": "Ver Todo",
        "no_transactions_found": "No se encontraron transacciones.",
        "try_adjusting_filters": "Prueba a cambiar los filtros.",
        "sync_success": "Saldos sincronizados correctamente.",
        "autosave_title": "Autoguardado Diario",
        "autosave_enabled": "Activar Autoguardado",
        "autosave_desc": "Guarda una copia de seguridad local en el navegador cada 24 horas (formato JSON).",
        "current_balance": "Saldo Actual",
        "calendar_view": "Vista de Calendario",
        "calendar_desc": "Visualiza tus ingresos y gastos mes a mes.",
        "go_to_today": "Ir a Hoy",
        "projected": "Proyecciones (Recurrentes)",
        "transactions": "Movimientos Reales",
        "habits": "Hábitos",
        "habit_tracker": "Seguimiento de Hábitos",
        "new_habit": "Nuevo Hábito",
        "edit_habit": "Editar Hábito",
        "habit_name": "Nombre del hábito",
        "habit_goal": "Meta",
        "goal_per_week": "{n} a la semana",
        "habit_frequency": "Frecuencia",
        "no_habits": "Todavía no tienes hábitos.",
        "confirm_delete_habit": "¿Eliminar hábito?",
        "weekly_progress": "Progreso Semanal",
        "current_streak": "Racha Actual",
        "best_streak": "Mejor Racha",
        "consistency_last_30_days": "Consistencia (30 días)",
        "days_streak": "{n} días",
        "day_m": "L",
        "day_t": "M",
        "day_w": "X",
        "day_th": "J",
        "day_f": "V",
        "day_s": "S",
        "day_su": "D",
        "score": "Puntuación",
        "streak": "Racha",
        "best": "Mejor",
        "monthly_consistency": "Consistencia Mensual",
        "close": "Cerrar",
        "reminder": "Recordatorio",
        "activated": "Activado",
        "not_set": "Sin configurar",
        "daily_reminder": "Recordatorio diario",
        "notification_info": "Puedes configurar la hora del recordatorio editando el hábito. Las notificaciones dependen de los permisos de tu navegador.",
        "category_names": {
            "Wallapop-Vinted": "Segunda Mano",
            "Uber-Cabify": "Uber-Cabify"
        }
    },
    "en": {
        "app_title": "VISUALIS",
        "app_subtitle": "your finances",
        "meta_title": "Visualis | Your Finances",
        "dashboard_recent_activity": "Recent Activity",
        "dashboard_monthly_budget": "Monthly Budget",
        "total_balance": "Total Balance",
        "income": "Income",
        "expense": "Expenses",
        "result": "Result",
        "transfer": "Transfer",
        "month": "month",
        "week": "week",
        "settings": "Settings",
        "profile": "Profile",
        "accounts": "Accounts/Projects",
        "categories": "Categories",
        "recurring": "Recurring",
        "data": "Data",
        "theme": "Theme",
        "language": "Language",
        "select_language": "Select your language",
        "save": "Save",
        "cancel": "Cancel",
        "delete": "Delete",
        "edit": "Edit",
        "new_transaction": "New Transaction",
        "edit_transaction": "Edit Transaction",
        "amount": "Amount",
        "date": "Date",
        "wallet": "Wallet",
        "category": "Category",
        "category_name": "Category Name",
        "color": "Color",
        "icon": "Icon",
        "description": "Description",
        "tags": "Tags",
        "export_excel": "Download Excel",
        "import_excel": "Import Excel",
        "reset_data": "Reset Data",
        "danger_zone": "Danger Zone",
        "warning_nuclear": "⚠️ NUCLEAR WARNING! ⚠️",
        "confirm_nuclear": "Are you SURE you want to delete ALL data?",
        "nuclear_button": "Nuclear Button",
        "advanced_search": "Advanced Search",
        "transaction_history": "Full History",
        "search_placeholder": "Search by concept, category, note...",
        "filters": "Filters",
        "clear_filters": "Clear",
        "filter_by": "Filter by",
        "type": "Type",
        "all": "All",
        "see_all": "See All",
        "no_transactions_found": "No transactions found.",
        "try_adjusting_filters": "Try adjusting filters.",
        "habits": "Habits",
        "habit_tracker": "Habit Tracker",
        "new_habit": "New Habit",
        "edit_habit": "Edit Habit",
        "habit_name": "Habit name",
        "habit_goal": "Goal",
        "goal_per_week": "{n} per week",
        "habit_frequency": "Frequency",
        "no_habits": "No habits yet.",
        "confirm_delete_habit": "Delete habit?",
        "weekly_progress": "Weekly Progress",
        "current_streak": "Current Streak",
        "best_streak": "Best Streak",
        "consistency_last_30_days": "Consistency (30 days)",
        "days_streak": "{n} days",
        "score": "Score",
        "close": "Close",
        "reminder": "Reminder",
        "activated": "Enabled",
        "not_set": "Not set",
        "daily_reminder": "Daily reminder",
        "notification_info": "You can set the reminder time by editing the habit. Notifications depend on your browser permissions.",
        "streak": "Streak",
        "best": "Best",
        "monthly_consistency": "Monthly Consistency",
        "day_m": "M",
        "day_t": "T",
        "day_w": "W",
        "day_th": "T",
        "day_f": "F",
        "day_s": "S",
        "day_su": "S",
        "theme_names": {
            "sky": "Starry Night",
            "forest": "Deep Forest",
            "nebula": "Purple Nebula",
            "mondrian": "Mondrian Style",
            "wine": "Select Wine",
            "light-sky": "Arctic Sky",
            "light-mint": "Emerald Oasis",
            "light-warm": "Amber Horizon",
            "pop-art": "Pop Art"
        },
        "category_names": {
            "Uber-Cabify": "Rideshare",
            "Wallapop-Vinted": "Second Hand"
        }
    },
    "gl": {
        "app_title": "VISUALIS",
        "app_subtitle": "as túas finanzas",
        "meta_title": "Visualis | as túas Finanzas",
        "dashboard_recent_activity": "Actividade Recente",
        "dashboard_monthly_budget": "Orzamento do Mes",
        "total_balance": "Balance Total",
        "income": "Ingresos",
        "expense": "Gastos",
        "result": "Resultado",
        "theme_names": {
            "sky": "Noite Estrelada",
            "forest": "Bosque Profundo",
            "nebula": "Nebulosa Púrpura",
            "mondrian": "Estilo Mondrian",
            "wine": "Viño Selecto",
            "light-sky": "Ceo Ártico",
            "light-mint": "Oasis Esmeralda",
            "light-warm": "Horizonte Ámbar",
            "pop-art": "Pop Art"
        },
        "category_names": {
            "Wallapop-Vinted": "Segunda Man",
            "Uber-Cabify": "VTC"
        }
    },
    "eu": {
        "app_title": "VISUALIS",
        "app_subtitle": "zure finantzak",
        "meta_title": "Visualis | zure Finantzak",
        "dashboard_recent_activity": "Azken Jarduera",
        "dashboard_monthly_budget": "Hileko Aurrekontua",
        "total_balance": "Balantze Osoa",
        "income": "Diru-sarrerak",
        "expense": "Gastuak",
        "theme_names": {
            "sky": "Gau Izartsua",
            "forest": "Baso Sakona",
            "nebula": "Nebulosa Morea",
            "mondrian": "Mondrian Estiloa",
            "wine": "Ardo Hautatua",
            "light-sky": "Zeru Artikoa",
            "light-mint": "Esmeralda Oasia",
            "light-warm": "Anbar Ostertza",
            "pop-art": "Pop Art"
        }
    },
    "ca": {
        "app_title": "VISUALIS",
        "app_subtitle": "les teves finances",
        "meta_title": "Visualis | les teves Finances",
        "dashboard_recent_activity": "Activitat Recent",
        "dashboard_monthly_budget": "Pressupost del Mes",
        "total_balance": "Balanç Total",
        "income": "Ingressos",
        "expense": "Despeses",
        "theme_names": {
            "sky": "Nit Estrellada",
            "forest": "Bosc Profund",
            "nebula": "Nebulosa Púrpura",
            "mondrian": "Estilo Mondrian",
            "wine": "Viño Selecte",
            "light-sky": "Cel Àrtic",
            "light-mint": "Oasi Maragda",
            "light-warm": "Horitzó Àmbar",
            "pop-art": "Pop Art"
        }
    }
};

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
];

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
    const [language, setLanguageState] = useState('es');
    const [currency, setCurrencyState] = useState('EUR');
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        const loadSettings = async () => {
            try {
                const settings = await db.settings.get('global');
                if (settings?.language) {
                    setLanguageState(settings.language);
                } else {
                    const browserLang = navigator.language.split('-')[0];
                    if (['es', 'en', 'gl', 'eu', 'ca'].includes(browserLang)) {
                        setLanguageState(browserLang);
                    } else {
                        setLanguageState('es');
                    }
                }
                if (settings?.currency) {
                    setCurrencyState(settings.currency);
                }
            } catch (e) {
                console.error("Failed to load settings:", e);
            } finally {
                setIsLoaded(true);
            }
        };
        loadSettings();
    }, []);

    const setLanguage = async (lang) => {
        setLanguageState(lang);
        try {
            const settings = await db.settings.get('global') || { id: 'global' };
            await db.settings.put({ ...settings, language: lang });
        } catch (e) { console.error(e); }
    };

    const setCurrency = async (curr) => {
        setCurrencyState(curr);
        try {
            const settings = await db.settings.get('global') || { id: 'global' };
            await db.settings.put({ ...settings, currency: curr });
        } catch (e) { console.error(e); }
    };

    const t = (key) => dictionaries[language]?.[key] || dictionaries['es'][key] || key;
    const tCategory = (name) => dictionaries[language]?.category_names?.[name] || dictionaries['es']?.category_names?.[name] || name;

    const formatMoney = (amount, currencyCode = null, options = {}) => {
        return new Intl.NumberFormat(language === 'en' ? 'en-US' : 'es-ES', {
            style: 'currency',
            currency: currencyCode || currency,
            ...options
        }).format(amount);
    };

    const symbol = CURRENCIES.find(c => c.code === currency)?.symbol || currency;
    const locales = { es, en: enUS, gl, eu, ca };
    const locale = locales[language] || es;

    return (
        <LanguageContext.Provider value={{ language, setLanguage, currency, setCurrency, symbol, t, tCategory, formatMoney, isLoaded, locale }}>
            {children}
        </LanguageContext.Provider>
    );
}

export const useLanguage = () => useContext(LanguageContext);

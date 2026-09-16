// Maps common category name keywords to appropriate Lucide icons
export const ICON_MAP = [
    // Utilities & Energy / Electricidad / Suministros (prioridad antes de casa)
    { keywords: ['electricidad', 'electric', 'electrica', 'electrico', 'luz', 'energia', 'energy', 'power', 'kilovatios', 'kwh'], icon: 'Zap' },
    { keywords: ['gas', 'butano', 'calefaccion', 'heating', 'combustion'], icon: 'Flame' },
    { keywords: ['agua', 'water', 'aqualia', 'fontaneria', 'plumbing'], icon: 'Droplets' },
    { keywords: ['internet', 'wifi', 'fibra', 'adsl', 'banda ancha', 'router'], icon: 'Wifi' },
    { keywords: ['telefono', 'phone', 'movil', 'linea', 'vodafone', 'movistar', 'orange', 'pepephone', 'o2', 'digi'], icon: 'Phone' },
    { keywords: ['suministr', 'utilit', 'services', 'servicios'], icon: 'Zap' },

    // Transport & Vehicles / Automóvil
    { keywords: ['automovil', 'automobil', 'coche', 'car', 'auto', 'vehiculo', 'vehicle', 'moto', 'motocicleta', 'scooter'], icon: 'Car' },
    { keywords: ['combustible', 'gasolina', 'diesel', 'gasoil', 'gasolinera', 'fuel', 'repostaje'], icon: 'Fuel' },
    { keywords: ['parking', 'aparcamiento', 'aparcam', 'estacionamiento', 'estacionam', 'garaje', 'garage'], icon: 'ParkingSquare' },
    { keywords: ['peaje', 'toll', 'viñeta', 'autopista'], icon: 'Ticket' },
    { keywords: ['taller', 'mantenimiento', 'mecanico', 'reparacion auto', 'itv', 'neumaticos', 'ruedas', 'revision'], icon: 'Wrench' },
    { keywords: ['multa', 'sancion', 'fine', 'radar'], icon: 'AlertCircle' },
    { keywords: ['metro', 'subway', 'tren', 'train', 'renfe', 'ferrocarril'], icon: 'Train' },
    { keywords: ['bus', 'autobus', 'autocar'], icon: 'Bus' },
    { keywords: ['taxi', 'uber', 'cabify', 'bolt', 'vtc', 'coche compartido', 'blablacar'], icon: 'Car' },
    { keywords: ['transport', 'desplazamiento'], icon: 'Train' },

    // Sport / Deporte & Fitness
    { keywords: ['deporte', 'sport', 'fitness', 'gimnasio', 'gym', 'crossfit', 'carrera', 'maraton', 'travesia', 'atletismo', 'natacion', 'futbol', 'baloncesto', 'padel', 'tenis', 'ciclismo', 'bici', 'entrenamiento', 'workout', 'yoga', 'pilates'], icon: 'Dumbbell' },
    { keywords: ['trofeo', 'carreras/travesias', 'campeonato', 'competicion'], icon: 'Trophy' },

    // Housing / Alquiler / Hipoteca
    { keywords: ['alquiler vacacional', 'vacational rent', 'aluguer vacacional'], icon: 'Sun' },
    { keywords: ['alquiler', 'rent', 'aluguer', 'inquilino', 'arrendamiento'], icon: 'Home' },
    { keywords: ['hipoteca', 'mortgage', 'prestamo vivienda'], icon: 'Home' },
    { keywords: ['hogar', 'casa', 'home', 'housing', 'vivienda', 'piso', 'apartamento', 'comunidad', 'comunita', 'ibi', 'basura'], icon: 'Home' },

    // Travel & Vacations / Viajes
    { keywords: ['viaje', 'viajes', 'travel', 'trip', 'turismo', 'turism', 'vacacion', 'vacaciones', 'vacation', 'vuelo', 'avion', 'flight', 'aeropuerto', 'billete avion'], icon: 'Plane' },
    { keywords: ['hotel', 'hoteles', 'hostal', 'alojamiento', 'aloxa', 'resort', 'booking', 'airbnb'], icon: 'Bed' },
    { keywords: ['maleta', 'equipaje', 'excursion', 'tour'], icon: 'Compass' },

    // Food & Groceries / Alimentación
    { keywords: ['supermercado', 'supermarket', 'hipermercado', 'mercadona', 'carrefour', 'lidl', 'dia', 'alcampo', 'compra comida', 'grocer', 'fruite', 'fruteria', 'carniceria', 'pescaderia', 'panaderia'], icon: 'ShoppingCart' },
    { keywords: ['restaur', 'comida fuera', 'almuerzo', 'cena', 'dinner', 'lunch', 'gastronomia'], icon: 'Utensils' },
    { keywords: ['cafe', 'café', 'coffee', 'desayuno', 'starbucks'], icon: 'Coffee' },
    { keywords: ['bar', 'cerveza', 'beer', 'copas', 'pub'], icon: 'Beer' },
    { keywords: ['vino', 'wine', 'bodega'], icon: 'Wine' },
    { keywords: ['snack', 'aperitivo', 'tapa', 'dulces', 'golosinas'], icon: 'Cookie' },
    { keywords: ['aliment', 'comida', 'food'], icon: 'Utensils' },

    // Health / Salud
    { keywords: ['farmacia', 'medicamento', 'pildora', 'pastilla', 'receta'], icon: 'Pill' },
    { keywords: ['medico', 'doctor', 'hospital', 'consulta', 'clinica', 'urgencias', 'especialista'], icon: 'Stethoscope' },
    { keywords: ['dental', 'dentista', 'odontolog'], icon: 'Smile' },
    { keywords: ['optic', 'optica', 'gafas', 'lentillas'], icon: 'Glasses' },
    { keywords: ['salud', 'health', 'fisio', 'psicolog', 'terapia', 'bienestar'], icon: 'HeartPulse' },

    // Shopping / Compras & Ropa / Moda
    { keywords: ['ropa', 'moda', 'fashion', 'vestir', 'pantalon', 'camisa', 'camiseta', 'abrigo', 'chaqueta', 'zara', 'mango'], icon: 'Shirt' },
    { keywords: ['calzado', 'zapato', 'zapatilla', 'bota', 'sneaker'], icon: 'Footprints' },
    { keywords: ['electronica', 'tecnologia', 'gadget', 'informatica'], icon: 'Smartphone' },
    { keywords: ['oficina', 'papeleria', 'material oficina', 'impresion'], icon: 'Printer' },
    { keywords: ['reparacion', 'bricolaje', 'herramienta', 'ferreteria'], icon: 'Hammer' },
    { keywords: ['compras', 'shopping', 'tienda', 'varias', 'compras varias'], icon: 'ShoppingCart' },
    { keywords: ['segunda mano', 'wallapop', 'vinted', 'ebay'], icon: 'ShoppingBag' },

    // Cleaning / Limpieza
    { keywords: ['lavanderia', 'tintoreria', 'lavado', 'colada'], icon: 'Droplets' },
    { keywords: ['limpieza', 'cleaning', 'detergente', 'aseo'], icon: 'Sparkles' },

    // Work / Salary / Negocio
    { keywords: ['nomina', 'sueldo', 'salario', 'salary', 'payroll'], icon: 'Banknote' },
    { keywords: ['desempleo', 'paro', 'prestacion', 'subsidio'], icon: 'Umbrella' },
    { keywords: ['negocio vut', 'vut', 'apartamento turistico'], icon: 'Building' },
    { keywords: ['consultoria', 'asesoria', 'freelance'], icon: 'Briefcase' },
    { keywords: ['negocio', 'empresa', 'business', 'trabajo', 'work', 'job', 'profesional'], icon: 'Briefcase' },

    // Education / Formación
    { keywords: ['curso', 'course', 'academia', 'master', 'clases', 'taller educativo', 'formacion', 'training'], icon: 'GraduationCap' },
    { keywords: ['libro', 'comic', 'libreria', 'novela', 'lectura', 'editorial', 'ebook'], icon: 'Book' },
    { keywords: ['colegio', 'universidad', 'escuela', 'matricula', 'instituto'], icon: 'School' },
    { keywords: ['educacion', 'education', 'estudio', 'aprender'], icon: 'BookOpen' },

    // Entertainment / Ocio
    { keywords: ['cine', 'pelicula', 'teatro', 'espectaculo', 'cinema', 'movie'], icon: 'Film' },
    { keywords: ['netflix', 'hbo', 'disney', 'prime video', 'streaming', 'television', 'tv'], icon: 'Tv' },
    { keywords: ['musica', 'spotify', 'concierto', 'festival'], icon: 'Music' },
    { keywords: ['juego', 'videojuego', 'gaming', 'playstation', 'xbox', 'nintendo', 'steam'], icon: 'Gamepad2' },
    { keywords: ['entrada', 'ticket', 'evento', 'concierto', 'show'], icon: 'Ticket' },
    { keywords: ['ocio diverso', 'ocio', 'diversion', 'entretenimiento', 'leisure'], icon: 'Smile' },

    // Savings / Investments / Finanzas / Bancos
    { keywords: ['dividendo', 'dividend'], icon: 'TrendingUp' },
    { keywords: ['interes', 'rendimiento', 'deposito', 'yield'], icon: 'Percent' },
    { keywords: ['inversion', 'bolsa', 'acciones', 'fondos', 'etf', 'cripto', 'crypto'], icon: 'TrendingUp' },
    { keywords: ['ahorro', 'hucha', 'savings'], icon: 'PiggyBank' },
    { keywords: ['prestamo', 'credito', 'deuda', 'loan', 'financiamiento'], icon: 'Banknote' },
    { keywords: ['comision', 'comisiones', 'fee', 'cuota bancaria'], icon: 'Percent' },
    { keywords: ['banco', 'bank', 'bancos', 'banca', 'entidad financiera'], icon: 'Landmark' },

    // Personal Care & Beauty
    { keywords: ['peluqueria', 'barberia', 'barbero', 'corte pelo'], icon: 'Scissors' },
    { keywords: ['belleza', 'estetica', 'cosmetica', 'maquillaje', 'spa', 'masaje'], icon: 'Sparkles' },

    // Pets / Mascotas
    { keywords: ['veterinario', 'clinica veterinaria'], icon: 'Stethoscope' },
    { keywords: ['mascota', 'perro', 'gato', 'pet', 'pienso', 'animal'], icon: 'Dog' },

    // Gifts & Donations
    { keywords: ['regalo', 'gift', 'cumpleaños', 'boda', 'aniversario', 'donacion', 'donativo', 'ong', 'charity'], icon: 'Gift' },

    // Insurance & Taxes / Impuestos
    { keywords: ['seguro', 'poliza', 'insurance', 'mapfre', 'axa', 'allianz', 'mutua'], icon: 'Shield' },
    { keywords: ['impuesto', 'tasa', 'hacienda', 'irpf', 'iva', 'tax', 'tributo'], icon: 'FileText' },

    // Kids / Children
    { keywords: ['hijo', 'niño', 'bebe', 'guarderia', 'child', 'kid', 'baby', 'pañales'], icon: 'Baby' },
]

export function guessIcon(name, isParent = true) {
    if (!name) return isParent ? 'Folder' : 'Circle'
    const normalized = name.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    for (const entry of ICON_MAP) {
        if (entry.keywords.some(kw => normalized.includes(kw))) {
            return entry.icon
        }
    }
    return isParent ? 'Folder' : 'Circle'
}

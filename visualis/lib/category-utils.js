
// Maps common category name keywords to appropriate Lucide icons
export const ICON_MAP = [
    // Food & Groceries
    { keywords: ['aliment', 'comida', 'supermercado', 'restaur', 'food', 'grocer', 'cocina', 'cena', 'almuerzo', 'desayuno', 'cafe', 'café', 'bar', 'mercad', 'fruite'], icon: 'ShoppingCart' },
    // Transport
    { keywords: ['transport', 'gasolina', 'combustible', 'coche', 'car', 'auto', 'moto', 'metro', 'bus', 'taxi', 'uber', 'tren', 'vuelo', 'avion', 'viaje', 'parking', 'peaje', 'aparcam', 'estacionam'], icon: 'Car' },
    // Health
    { keywords: ['salud', 'health', 'medic', 'farmacia', 'doctor', 'hospital', 'deporte', 'gym', 'sport', 'fitness', 'dental', 'optic', 'dentista', 'fisio', 'psicolog', 'terapia', 'medica'], icon: 'Heart' },
    // Housing & Services
    { keywords: ['hogar', 'casa', 'alquiler', 'hipoteca', 'luz', 'agua', 'gas', 'internet', 'telefono', 'suministr', 'home', 'rent', 'mortgage', 'electricity', 'housing', 'aluguer', 'comunida', 'comunita', 'electricida', 'mantenim', 'ibi', 'basura'], icon: 'Home' },
    // Shopping / Clothing
    { keywords: ['ropa', 'moda', 'calzado', 'fashion', 'compras', 'shopping', 'tienda', 'zapa', 'vestir'], icon: 'ShoppingBag' },
    // Work / Salary
    { keywords: ['trabajo', 'salario', 'sueldo', 'nomina', 'work', 'salary', 'income', 'ingreso', 'empresa', 'freelance', 'negocio', 'venda', 'venta'], icon: 'Briefcase' },
    // Education
    { keywords: ['educacion', 'cursos', 'libros', 'colegio', 'universidad', 'school', 'education', 'formacion', 'estudi'], icon: 'GraduationCap' },
    // Entertainment / Leisure
    { keywords: ['ocio', 'entretenimiento', 'cine', 'musica', 'netflix', 'spotify', 'juegos', 'games', 'leisure', 'recreation', 'suscripcion', 'subscri', 'entrad'], icon: 'Play' },
    // Savings / Investments
    { keywords: ['ahorro', 'inversion', 'saving', 'invest', 'bolsa', 'fondos', 'pension', 'dividend', 'interes'], icon: 'PiggyBank' },
    // Gifts / Social
    { keywords: ['regalo', 'gift', 'cumpleaños', 'social', 'celebracion', 'fiesta', 'agasallo'], icon: 'Gift' },
    // Technology
    { keywords: ['tecnologia', 'tech', 'ordenador', 'movil', 'phone', 'computer', 'electronico', 'electronic', 'software'], icon: 'Smartphone' },
    // Travel
    { keywords: ['viaje', 'hotel', 'travel', 'vacacion', 'vacation', 'turismo', 'alojamiento', 'aloxa'], icon: 'Plane' },
    // Insurance / Taxes
    { keywords: ['seguro', 'impuest', 'tasa', 'tax', 'insurance', 'contribucion', 'ivm'], icon: 'ShieldCheck' },
    // Pets
    { keywords: ['mascota', 'perro', 'gato', 'pet', 'veterinario', 'vet'], icon: 'PawPrint' },
    // Kids / Children
    { keywords: ['hijo', 'niño', 'bebe', 'guarderia', 'child', 'kid', 'baby'], icon: 'Baby' },
    // Beauty / Personal Care
    { keywords: ['belleza', 'peluqueria', 'beauty', 'estetica', 'cosmetica', 'personal'], icon: 'Sparkles' },
    // Bank / Finances
    { keywords: ['banco', 'bank', 'comision', 'prestamo', 'credito', 'loan', 'finanza', 'finance'], icon: 'Landmark' },
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

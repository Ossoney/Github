// =====================
// ZODIACO OCCIDENTAL
// =====================
const ZODIAC_SIGNS = [
    { name: "Aries", icon: "♈", dates: "21 Mar - 19 Abr" },
    { name: "Tauro", icon: "♉", dates: "20 Abr - 20 May" },
    { name: "Géminis", icon: "♊", dates: "21 May - 20 Jun" },
    { name: "Cáncer", icon: "♋", dates: "21 Jun - 22 Jul" },
    { name: "Leo", icon: "♌", dates: "23 Jul - 22 Ago" },
    { name: "Virgo", icon: "♍", dates: "23 Ago - 22 Sep" },
    { name: "Libra", icon: "♎", dates: "23 Sep - 22 Oct" },
    { name: "Escorpio", icon: "♏", dates: "23 Oct - 21 Nov" },
    { name: "Sagitario", icon: "♐", dates: "22 Nov - 21 Dic" },
    { name: "Capricornio", icon: "♑", dates: "22 Dic - 19 Ene" },
    { name: "Acuario", icon: "♒", dates: "20 Ene - 18 Feb" },
    { name: "Piscis", icon: "♓", dates: "19 Feb - 20 Mar" }
];

// =====================
// ZODIACO CHINO
// =====================
const CHINESE_ZODIAC = [
    { name: "Rata", icon: "🐀", years: "2020, 2008, 1996, 1984, 1972" },
    { name: "Buey", icon: "🐂", years: "2021, 2009, 1997, 1985, 1973" },
    { name: "Tigre", icon: "🐅", years: "2022, 2010, 1998, 1986, 1974" },
    { name: "Conejo", icon: "🐇", years: "2023, 2011, 1999, 1987, 1975" },
    { name: "Dragón", icon: "🐉", years: "2024, 2012, 2000, 1988, 1976" },
    { name: "Serpiente", icon: "🐍", years: "2025, 2013, 2001, 1989, 1977" },
    { name: "Caballo", icon: "🐎", years: "2026, 2014, 2002, 1990, 1978" },
    { name: "Cabra", icon: "🐐", years: "2027, 2015, 2003, 1991, 1979" },
    { name: "Mono", icon: "🐒", years: "2028, 2016, 2004, 1992, 1980" },
    { name: "Gallo", icon: "🐓", years: "2029, 2017, 2005, 1993, 1981" },
    { name: "Perro", icon: "🐕", years: "2030, 2018, 2006, 1994, 1982" },
    { name: "Cerdo", icon: "🐖", years: "2031, 2019, 2007, 1995, 1983" }
];

// =====================
// HUMOR DEL DÍA
// =====================
const MOODS = [
    "Optimista irracional",
    "Caféfobo",
    "Berserker silencioso",
    "Filósofo existencial",
    "Mono con typewriter",
    "Globo a punto de explotar",
    "Gato solariego",
    "Pato en pánico",
    "Paciente zero del drama",
    "Peppa Pig en modo adulto"
];

// =====================
// COLORES DE LA SUERTE
// =====================
const LUCKY_COLORS = [
    { name: "Violeta oscuro", hex: "#4c1d95" },
    { name: "Rosa neon", hex: "#f472b6" },
    { name: "Verde veneno", hex: "#22c55e" },
    { name: "Amarillo核电", hex: "#facc15" },
    { name: "Rojo dramático", hex: "#ef4444" },
    { name: "Azul triste", hex: "#3b82f6" },
    { name: "Naranja warning", hex: "#f97316" },
    { name: "Negro holes", hex: "#171717" }
];

// =====================
// PARTES DEL TEXTO
// =====================
const INTROS = [
    "Los astros se han alineado de forma sospechosa y dicen que...",
    "Venus está en una posición incómoda, lo que significa que...",
    "He consultado a las estrellas y, francamente, están preocupadas porque...",
    "El universo tiene un mensaje para ti, aunque preferiría no dártelo: ",
    "Saturno indica turbulencias emocionales, básicamente...",
    "Tu aura hoy brilla, pero con la intensidad de una bombilla fundida, así que...",
    "Mercurio NO está retrógrado, así que esta vez es culpa tuya que...",
    "La energía cósmica de hoy sugiere que...",
    "Según la posición de la luna (y mi intuición), hoy es obvio que...",
    "Las constelaciones se han reunido para cotillear sobre ti y concluyen que..."
];

const BODIES = [
    "hoy es uno de esos días en los que tu paciencia será más corta que la batería de tu móvil.",
    "deberías evitar tomar decisiones importantes, como cortarte el flequillo o enviar ese WhatsApp.",
    "tu capacidad para procrastinar alcanzará niveles olímpicos.",
    "alguien va a poner a prueba tus nervios masticando muy fuerte cerca de tu oído.",
    "esa 'gran idea' que tuviste anoche te parecerá ridícula antes del mediodía.",
    "sentirás una inexplicable necesidad de gastar dinero en cosas que no necesitas.",
    "tu carisma hoy está en números rojos, mejor no intentes negociar nada.",
    "es probable que te tropieces, física o emocionalmente, en público.",
    "hoy tu mayor logro será simplemente sobrevivir a la jornada laboral sin llorar.",
    "el destino te tiene preparada una sorpresa, y probablemente sea trabajo extra."
];

const ADVICES = [
    "Mi consejo: escóndete bajo una manta hasta mañana.",
    "Lo mejor que puedes hacer es fingir demencia.",
    "Te sugiero fuertemente que pidas pizza y no hables con nadie.",
    "Simplemente asiente y sonríe, nadie notará que no estás escuchando.",
    "Evita los espejos y las redes sociales por tu bien mental.",
    "Si la vida te da limones, asegúrate de que no te den en un ojo.",
    "Recuerda: si nadie te ve cometer el error, nunca pasó.",
    "Hoy es un buen día para decir 'no' a todo. Absolutamente a todo.",
    "Mantén tus expectativas bajas. Más bajas. Ahí, perfecto.",
    "Hazte un favor y no mires tu cuenta bancaria hoy."
];

const COMPATIBILITY_LEVELS = [
    "Fatal 💀",
    "Mal 👎",
    "Regular 😐",
    "Bien 👍",
    "Muy Bien 💖",
    "Extraordinario 🔥",
    "Peligroso ⚠️",
    "Explosivo 🧨"
];

// Generador de semilla según modo
function getModeSeed(mode) {
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = (now.getMonth() + 1).toString().padStart(2, '0');
    const dd = now.getDate().toString().padStart(2, '0');
    const hh = now.getHours().toString().padStart(2, '0');

    switch (mode) {
        case 'hourly':
            return parseInt(`${yyyy}${mm}${dd}${hh}`);
        case 'daily':
            return parseInt(`${yyyy}${mm}${dd}`);
        case 'weekly':
            // Semana del año
            const week = Math.ceil((now - new Date(yyyy, 0, 1)) / (7 * 24 * 60 * 60 * 1000));
            return parseInt(`${yyyy}${week}`);
        default:
            return parseInt(`${yyyy}${mm}${dd}${hh}`);
    }
}

// Alias para compatibilidad
function getHourlySeed() {
    return getModeSeed('hourly');
}

function seededRandom(seed) {
    var x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
}

// =====================
// ZODIACO CHINO - AÑO DE NACIMIENTO
// =====================
function getChineseZodiacIndex(birthYear) {
    // 1924 fue el año de la Rata en el ciclo chino
    const cycleStart = 1924;
    const offset = (birthYear - cycleStart) % 12;
    return offset >= 0 ? offset : 12 + offset;
}

// =====================
// HISTORIAL
// =====================
const HISTORY_KEY = 'horoscopo_history';

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
    } catch {
        return [];
    }
}

function addToHistory(entry) {
    const history = getHistory();
    history.unshift(entry);
    // Mantener solo los últimos 50
    if (history.length > 50) history.pop();
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

function clearHistory() {
    localStorage.removeItem(HISTORY_KEY);
}

// =====================
// GENERADOR PRINCIPAL
// =====================
function getHoroscope(signIndex, mode = 'hourly', zodiacType = 'western') {
    const modeSeed = getModeSeed(mode);
    const zodiacArray = zodiacType === 'western' ? ZODIAC_SIGNS : CHINESE_ZODIAC;
    const sign = zodiacArray[signIndex];
    
    /*
     Combinamos: Semilla del modo + (Índice Signo * Constante)
    */
    let uniqueSeed = modeSeed + (signIndex * 1337);

    // Elegir partes del texto
    const introIndex = Math.floor(seededRandom(uniqueSeed++) * INTROS.length);
    const bodyIndex = Math.floor(seededRandom(uniqueSeed++) * BODIES.length);
    const adviceIndex = Math.floor(seededRandom(uniqueSeed++) * ADVICES.length);

    // Número de la mala suerte (1-99)
    const luckyNum = Math.floor(seededRandom(uniqueSeed++) * 99) + 1;

    // Afinidad
    let compSignIndex = Math.floor(seededRandom(uniqueSeed++) * zodiacArray.length);
    if (compSignIndex === signIndex) compSignIndex = (compSignIndex + 1) % zodiacArray.length;

    const compLevelIndex = Math.floor(seededRandom(uniqueSeed++) * COMPATIBILITY_LEVELS.length);

    // Humor del día
    const moodIndex = Math.floor(seededRandom(uniqueSeed++) * MOODS.length);
    
    // Color de la suerte
    const colorIndex = Math.floor(seededRandom(uniqueSeed++) * LUCKY_COLORS.length);

    // Construir texto
    const fullText = `${INTROS[introIndex]} ${BODIES[bodyIndex]} ${ADVICES[adviceIndex]}`;

    const result = {
        text: fullText,
        number: luckyNum,
        mood: MOODS[moodIndex],
        color: LUCKY_COLORS[colorIndex],
        compatibility: {
            sign: zodiacArray[compSignIndex].name,
            level: COMPATIBILITY_LEVELS[compLevelIndex]
        },
        timestamp: Date.now(),
        mode: mode,
        zodiacType: zodiacType,
        signName: sign.name
    };

    // Guardar en historial
    addToHistory(result);
    
    return result;
}

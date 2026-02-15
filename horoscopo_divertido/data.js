const ZODIAC_SIGNS = [
    { name: "Aries", icon: "♈", dates: "21 Mar - 19 Abr", apiName: "aries" },
    { name: "Tauro", icon: "♉", dates: "20 Abr - 20 May", apiName: "taurus" },
    { name: "Géminis", icon: "♊", dates: "21 May - 20 Jun", apiName: "gemini" },
    { name: "Cáncer", icon: "♋", dates: "21 Jun - 22 Jul", apiName: "cancer" },
    { name: "Leo", icon: "♌", dates: "23 Jul - 22 Ago", apiName: "leo" },
    { name: "Virgo", icon: "♍", dates: "23 Ago - 22 Sep", apiName: "virgo" },
    { name: "Libra", icon: "♎", dates: "23 Sep - 22 Oct", apiName: "libra" },
    { name: "Escorpio", icon: "♏", dates: "23 Oct - 21 Nov", apiName: "scorpio" },
    { name: "Sagitario", icon: "♐", dates: "22 Nov - 21 Dic", apiName: "sagittarius" },
    { name: "Capricornio", icon: "♑", dates: "22 Dic - 19 Ene", apiName: "capricorn" },
    { name: "Acuario", icon: "♒", dates: "20 Ene - 18 Feb", apiName: "aquarius" },
    { name: "Piscis", icon: "♓", dates: "19 Feb - 20 Mar", apiName: "pisces" }
];

// Partes del texto para combinatoria
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

// Generador de semilla horaria: AAAA + MM + DD + HH
function getHourlySeed() {
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = (now.getMonth() + 1).toString().padStart(2, '0');
    const dd = now.getDate().toString().padStart(2, '0');
    const hh = now.getHours().toString().padStart(2, '0');

    return parseInt(`${yyyy}${mm}${dd}${hh}`);
}

function seededRandom(seed) {
    var x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
}

function getHoroscope(signIndex) {
    const hourlySeed = getHourlySeed();
    /*
     Combinamos: Semilla Horaria + (Índice Signo * Constante)
     Esto asegura resultados únicos por signo y por hora.
    */
    let uniqueSeed = hourlySeed + (signIndex * 1337);

    // Elegir partes del texto
    const introIndex = Math.floor(seededRandom(uniqueSeed++) * INTROS.length);
    const bodyIndex = Math.floor(seededRandom(uniqueSeed++) * BODIES.length);
    const adviceIndex = Math.floor(seededRandom(uniqueSeed++) * ADVICES.length);

    // Número de la mala suerte (1-99)
    const luckyNum = Math.floor(seededRandom(uniqueSeed++) * 99) + 1;

    // Afinidad
    let compSignIndex = Math.floor(seededRandom(uniqueSeed++) * 12);
    // Evitar que sea el mismo signo (opcional, pero más divertido si es otro)
    if (compSignIndex === signIndex) compSignIndex = (compSignIndex + 1) % 12;

    const compLevelIndex = Math.floor(seededRandom(uniqueSeed++) * COMPATIBILITY_LEVELS.length);

    // Construir texto
    const fullText = `${INTROS[introIndex]} ${BODIES[bodyIndex]} ${ADVICES[adviceIndex]}`;

    return {
        text: fullText,
        number: luckyNum,
        compatibility: {
            sign: ZODIAC_SIGNS[compSignIndex].name,
            level: COMPATIBILITY_LEVELS[compLevelIndex]
        }
    };
}

async function translateText(text) {
    try {
        const response = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=en|es`);
        const data = await response.json();
        return data.responseData.translatedText;
    } catch (e) {
        console.warn("Translation failed", e);
        return text; // Return original if translation fails
    }
}

async function fetchDailyHoroscope(signApiName) {
    try {
        const response = await fetch(`https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign=${signApiName}&day=today`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        const englishText = data.data.horoscope_data;

        // Translate to Spanish
        return await translateText(englishText);
    } catch (error) {
        console.error("Error fetching/translating horoscope:", error);
        return null; // Return null to trigger fallback
    }
}

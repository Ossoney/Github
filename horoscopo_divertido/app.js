const grid = document.getElementById('grid');
const modal = document.getElementById('modal');
const closeBtn = document.getElementById('close');

const ui = {
    icon: document.getElementById('result-icon'),
    sign: document.getElementById('result-sign'),
    text: document.getElementById('prediction'),
    number: document.getElementById('lucky-num'),
    compLevel: document.getElementById('comp-level'),
    compSign: document.getElementById('comp-sign'),
    loader: document.getElementById('loader'),
    content: document.getElementById('result-text-container')
};

// Generar Grid
ZODIAC_SIGNS.forEach((sign, index) => {
    const card = document.createElement('div');
    card.className = 'sign-card';
    card.innerHTML = `
        <span class="sign-icon">${sign.icon}</span>
        <span class="sign-name">${sign.name}</span>
    `;
    card.onclick = () => openHoroscope(index);
    grid.appendChild(card);
});

async function openHoroscope(index) {
    const sign = ZODIAC_SIGNS[index];

    // Preparar Modal
    ui.icon.textContent = sign.icon;
    ui.sign.textContent = sign.name;

    // Mostrar Loader
    modal.classList.remove('hidden');
    ui.loader.classList.remove('hidden');
    ui.content.classList.add('hidden');

    try {
        // Obtenemos datos locales para los "extras" (número, compatibilidad)
        // y como fallback por si la API falla.
        const localData = getHoroscope(index);

        // Fetch a la API real (con un mínimo delay estético de 500ms)
        // Usamos un timeout para evitar que el fetch se quede colgado eternamente
        const fetchPromise = fetchDailyHoroscope(sign.apiName);
        const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 5000));

        const [apiText] = await Promise.all([
            Promise.race([fetchPromise, timeoutPromise]),
            new Promise(resolve => setTimeout(resolve, 800))
        ]);

        // Si hay texto de la API, lo usamos. Si no, usamos el local.
        if (apiText) {
            ui.text.textContent = `"${apiText}"`;
            // Los extras se mantienen aleatorios
            ui.number.textContent = localData.number;
            ui.compLevel.textContent = localData.compatibility.level;
            ui.compSign.textContent = localData.compatibility.sign;
        } else {
            throw new Error("API returns empty or null");
        }

    } catch (error) {
        console.error("Error UI / Fallback:", error);
        // Fallback de emergencia
        const fallback = getHoroscope(index);
        ui.text.textContent = `"${fallback.text}"`;
        ui.number.textContent = fallback.number;
        ui.compLevel.textContent = fallback.compatibility.level;
        ui.compSign.textContent = fallback.compatibility.sign;
    } finally {
        ui.loader.classList.add('hidden');
        ui.content.classList.remove('hidden');
    }
}

closeBtn.onclick = () => {
    modal.classList.add('hidden');
};

// Cerrar al tocar fuera
modal.onclick = (e) => {
    if (e.target === modal) {
        modal.classList.add('hidden');
    }
};

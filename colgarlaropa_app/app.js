const ui = {
    app: document.getElementById('app'),
    icon: document.getElementById('status-icon'),
    main: document.getElementById('main-status'),
    sub: document.getElementById('sub-status'),
    details: document.getElementById('details'),
    rain: document.getElementById('rain-prob'),
    temp: document.getElementById('temp'),
    loc: document.getElementById('location'),
    btn: document.getElementById('refresh-btn')
};

async function init() {
    ui.btn.addEventListener('click', () => location.reload());

    if (!navigator.geolocation) {
        showError("Tu navegador no soporta geolocalización.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        position => fetchWeather(position.coords),
        error => showError("Necesitamos tu ubicación para ver el cielo.")
    );
}

async function fetchWeather(coords) {
    const { latitude, longitude } = coords;

    try {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m&hourly=precipitation_probability,rain&forecast_days=1&timezone=auto`;

        const response = await fetch(url);
        const data = await response.json();

        analyzeData(data);
    } catch (e) {
        console.error(e);
        showError("Error al conectar con el servicio meteorológico.");
    }
}

function analyzeData(data) {
    // Obtenemos la hora actual
    const currentHourIndex = new Date().getHours();

    // Analizamos las próximas 8 horas (o hasta el final del día)
    let maxRainProb = 0;
    let willRain = false;

    const relevantHours = data.hourly.precipitation_probability.slice(currentHourIndex, currentHourIndex + 8);

    for (let prob of relevantHours) {
        if (prob > 0) {
            willRain = true;
        }
        if (prob > maxRainProb) maxRainProb = prob;
    }

    const currentTemp = data.current.temperature_2m;
    const timezone = data.timezone; // A veces OpenMeteo da timezone como ubicación aprox

    updateUI({
        canHang: !willRain,
        rainProb: maxRainProb,
        temp: currentTemp,
        location: timezone.split('/')[1]?.replace('_', ' ') || 'Ubicación'
    });
}

function updateUI(state) {
    ui.app.classList.remove('loading');
    ui.details.classList.remove('hidden');

    if (state.canHang) {
        ui.app.classList.add('yes');
        ui.app.classList.remove('no');
        ui.icon.textContent = "👕";
        ui.main.textContent = "¡ADELANTE!";
        ui.sub.textContent = "Puedes colgar la ropa.";
    } else {
        ui.app.classList.add('no');
        ui.app.classList.remove('yes');
        ui.icon.textContent = "☔";
        ui.main.textContent = "MEJOR ESPERA";
        ui.sub.textContent = `Riesgo de lluvia (${state.rainProb}%)`;
    }

    ui.rain.textContent = `${state.rainProb}%`;
    ui.temp.textContent = `${state.temp}°C`;
    ui.loc.textContent = state.location;
}

function showError(msg) {
    ui.app.classList.remove('loading');
    ui.main.textContent = "Ups...";
    ui.sub.textContent = msg;
    ui.icon.textContent = "😵";
}

init();

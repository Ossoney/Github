// =====================
// Estado de la app
// =====================
let currentMode = 'hourly';
let currentZodiac = 'western';

// =====================
// Elementos del DOM
// =====================
const grid = document.getElementById('grid');
const modal = document.getElementById('modal');
const closeBtn = document.getElementById('close');
const historyModal = document.getElementById('history-modal');
const closeHistoryBtn = document.getElementById('close-history');
const historyBtn = document.getElementById('history-btn');
const clearHistoryBtn = document.getElementById('clear-history-btn');
const historyList = document.getElementById('history-list');

// =====================
// Elementos UI del Modal
// =====================
const ui = {
    icon: document.getElementById('result-icon'),
    sign: document.getElementById('result-sign'),
    text: document.getElementById('prediction'),
    number: document.getElementById('lucky-num'),
    mood: document.getElementById('mood-text'),
    color: document.getElementById('lucky-color'),
    colorSwatch: document.getElementById('color-swatch'),
    compLevel: document.getElementById('comp-level'),
    compSign: document.getElementById('comp-sign'),
    loader: document.getElementById('loader'),
    content: document.getElementById('result-text-container'),
    badge: document.getElementById('mode-badge'),
    shareBtn: document.getElementById('share-btn')
};

// =====================
// Inicialización
// =====================
function init() {
    renderZodiacGrid();
    setupEventListeners();
}

function getZodiacArray() {
    return currentZodiac === 'western' ? ZODIAC_SIGNS : CHINESE_ZODIAC;
}

// =====================
// Renderizar Grid
// =====================
function renderZodiacGrid() {
    grid.innerHTML = '';
    const signs = getZodiacArray();
    
    signs.forEach((sign, index) => {
        const card = document.createElement('div');
        card.className = 'sign-card';
        
        // Mostrar fechas solo en zodiaco occidental
        const dates = currentZodiac === 'western' && sign.dates ? 
            `<span class="sign-dates">${sign.dates}</span>` : '';
        
        // Para zodiaco chino, mostrar años relacionados
        const years = currentZodiac === 'chinese' && sign.years ?
            `<span class="sign-dates">${sign.years}</span>` : '';
        
        card.innerHTML = `
            <span class="sign-icon">${sign.icon}</span>
            <span class="sign-name">${sign.name}</span>
            ${dates}
            ${years}
        `;
        card.onclick = () => openHoroscope(index);
        grid.appendChild(card);
    });
}

// =====================
// Abrir Horóscopo
// =====================
let currentPrediction = null;

function openHoroscope(index) {
    const sign = getZodiacArray()[index];
    
    // Generar predicción con modo y tipo de zodiaco actuales
    currentPrediction = getHoroscope(index, currentMode, currentZodiac);

    // Preparar Modal
    ui.icon.textContent = sign.icon;
    ui.sign.textContent = sign.name;
    
    // Badge de modo
    const modeLabels = {
        hourly: '📅 Por Horas',
        daily: '📆 Diario',
        weekly: '📆 Semanal'
    };
    ui.badge.textContent = modeLabels[currentMode];

    // Mostrar Loader primero
    modal.classList.remove('hidden');
    ui.loader.classList.remove('hidden');
    ui.content.classList.add('hidden');

    // Simular "Leyendo astros"
    setTimeout(() => {
        ui.loader.classList.add('hidden');
        ui.content.classList.remove('hidden');

        // Mostrar datos
        ui.text.textContent = `"${currentPrediction.text}"`;
        ui.number.textContent = currentPrediction.number;
        ui.mood.textContent = currentPrediction.mood;
        ui.color.textContent = currentPrediction.color.name;
        ui.colorSwatch.style.backgroundColor = currentPrediction.color.hex;
        ui.compLevel.textContent = currentPrediction.compatibility.level;
        ui.compSign.textContent = currentPrediction.compatibility.sign;
    }, 800);
}

// =====================
// Compartir Predicción
// =====================
function sharePrediction() {
    if (!currentPrediction) return;
    
    const shareText = `🔮 ${currentPrediction.signName}\n\n"${currentPrediction.text}"\n\n` +
        `🎭 Humor: ${currentPrediction.mood}\n` +
        `🎨 Color: ${currentPrediction.color.name}\n` +
        `🔢 Número: ${currentPrediction.number}\n\n` +
        `#HoroscopoDivertido`;

    if (navigator.share) {
        navigator.share({
            title: `Horóscopo de ${currentPrediction.signName}`,
            text: shareText
        }).catch(() => {});
    } else {
        // Fallback: copiar al portapapeles
        navigator.clipboard.writeText(shareText).then(() => {
            alert('¡Predicción copiada al portapapeles! 📋');
        }).catch(() => {});
    }
}

// =====================
// Historial
// =====================
function showHistory() {
    const history = getHistory();
    historyList.innerHTML = '';
    
    if (history.length === 0) {
        historyList.innerHTML = '<p class="no-history">No hay predicciones en el historial aún. ¡Consulta tu futuro!</p>';
    } else {
        history.forEach((entry, index) => {
            const item = document.createElement('div');
            item.className = 'history-item';
            
            const date = new Date(entry.timestamp);
            const dateStr = date.toLocaleDateString('es', { 
                day: 'numeric', 
                month: 'short', 
                hour: '2-digit',
                minute: '2-digit'
            });
            
            const zodiacIcon = entry.zodiacType === 'western' ? '♈' : '🐉';
            
            item.innerHTML = `
                <div class="history-header">
                    <span class="history-icon">${zodiacIcon}</span>
                    <strong>${entry.signName}</strong>
                    <span class="history-date">${dateStr}</span>
                </div>
                <p class="history-text">${entry.text}</p>
            `;
            historyList.appendChild(item);
        });
    }
    
    historyModal.classList.remove('hidden');
}

// =====================
// Event Listeners
// =====================
function setupEventListeners() {
    // Cerrar modal principal
    closeBtn.onclick = () => modal.classList.add('hidden');
    
    // Cerrar modal historial
    closeHistoryBtn.onclick = () => historyModal.classList.add('hidden');
    
    // Abrir historial
    historyBtn.onclick = showHistory;
    
    // Limpiar historial
    clearHistoryBtn.onclick = () => {
        if (confirm('¿Seguro que quieres borrar todo el historial?')) {
            clearHistory();
            showHistory();
        }
    };
    
    // Compartir
    ui.shareBtn.onclick = sharePrediction;
    
    // Cerrar al tocar fuera del modal
    modal.onclick = (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    };
    
    historyModal.onclick = (e) => {
        if (e.target === historyModal) historyModal.classList.add('hidden');
    };
    
    // Selector de modo
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentMode = btn.dataset.mode;
            renderZodiacGrid();
        };
    });
    
    // Toggle zodiaco
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentZodiac = btn.dataset.zodiac;
            renderZodiacGrid();
        };
    });
}

// Iniciar app
init();


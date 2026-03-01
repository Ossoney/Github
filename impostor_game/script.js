/* --- DATA --- */
const CATEGORIES = {
    lugares: [
        "Playa", "Escuela", "Hospital", "Avión", "Cine", "Restaurante", "Cementerio", "Circo",
        "Banco", "Spa", "Zoológico", "Supermercado", "Estación Espacial", "Submarino", "Pirámide",
        "Polo Norte", "Casino", "Biblioteca", "Gimnasio", "Crucero"
    ],
    comida: [
        "Pizza", "Sushi", "Hamburguesa", "Tacos", "Paella", "Helado", "Chocolate", "Ensalada",
        "Sopa", "Pasta", "Curry", "Tortilla", "Ceviche", "Parrillada", "Donut"
    ],
    animales: [
        "Perro", "Gato", "Elefante", "León", "Tiburón", "Águila", "Serpiente", "Delfín",
        "Pingüino", "Mono", "Jirafa", "Canguro", "Oso Panda", "Murciélago", "Camaleón"
    ],
    profesiones: [
        "Médico", "Bombero", "Policía", "Profesor", "Astronauta", "Chef", "Programador",
        "Abogado", "Músico", "Actor", "Futbolista", "Piloto", "Detective", "Carpintero"
    ]
};

/* --- STATE --- */
const state = {
    players: 4,
    impostors: 1,
    category: 'all',
    roles: [], // Array of strings: "Impostor" or the secret word
    currentPlayerIndex: 0,
    secretWord: "",
    timer: 300, // 5 minutes in seconds
    timerInterval: null
};

/* --- DOM ELEMENTS --- */
const screens = {
    setup: document.getElementById('screen-setup'),
    pass: document.getElementById('screen-pass'),
    reveal: document.getElementById('screen-reveal'),
    game: document.getElementById('screen-game')
};

const els = {
    playerCount: document.getElementById('player-count'),
    impostorCount: document.getElementById('impostor-count'),
    categorySelect: document.getElementById('category-select'),
    currentPlayerNum: document.getElementById('current-player-num'),
    roleContent: document.getElementById('role-content'),
    roleInstruction: document.getElementById('role-instruction'),
    gameCategoryDisplay: document.getElementById('game-category-display'),
    timerDisplay: document.getElementById('timer-display'),
    timerProgress: document.getElementById('timer-progress')
};

/* --- NAVIGATION --- */
function showScreen(screenKey) {
    const target = screens[screenKey];

    // Hide others
    Object.values(screens).forEach(s => {
        if (s !== target) {
            s.classList.remove('active');
            setTimeout(() => {
                if (!s.classList.contains('active')) {
                    s.classList.add('hidden');
                }
            }, 400);
        }
    });

    // Show target
    target.classList.remove('hidden');
    // Force reflow for transition
    void target.offsetWidth;
    target.classList.add('active');
}

/* --- SETUP LOGIC --- */
function updateCounts() {
    els.playerCount.innerText = state.players;
    els.impostorCount.innerText = state.impostors;
}

document.getElementById('btn-dec-players').addEventListener('click', () => {
    if (state.players > 3) {
        state.players--;
        if (state.impostors >= state.players) state.impostors = state.players - 1;
        updateCounts();
    }
});

document.getElementById('btn-inc-players').addEventListener('click', () => {
    if (state.players < 20) {
        state.players++;
        updateCounts();
    }
});

document.getElementById('btn-dec-impostors').addEventListener('click', () => {
    if (state.impostors > 1) {
        state.impostors--;
        updateCounts();
    }
});

document.getElementById('btn-inc-impostors').addEventListener('click', () => {
    // Max impostors is roughly half the players usually, but let's be flexible
    if (state.impostors < state.players - 1) {
        state.impostors++;
        updateCounts();
    }
});

/* --- GAME LOGIC --- */
function startGame() {
    // 1. Select Category & Word
    let words = [];
    state.category = els.categorySelect.value;

    if (state.category === 'all') {
        const cats = Object.values(CATEGORIES);
        words = cats[Math.floor(Math.random() * cats.length)];
    } else {
        words = CATEGORIES[state.category];
    }

    state.secretWord = words[Math.floor(Math.random() * words.length)];

    // 2. Assign Roles
    state.roles = Array(state.players).fill(state.secretWord);

    // Distribute impostors randomly using Fisher-Yates shuffle concept
    let impostorIndices = new Set();
    while (impostorIndices.size < state.impostors) {
        const r = Math.floor(Math.random() * state.players);
        impostorIndices.add(r);
    }

    impostorIndices.forEach(idx => state.roles[idx] = "IMPOSTOR");

    // 3. Reset Game State
    state.currentPlayerIndex = 0;

    // 4. Start Pass Loop
    showNextPlayerPassScreen();
}

function showNextPlayerPassScreen() {
    if (state.currentPlayerIndex >= state.players) {
        startTimer();
        return;
    }

    els.currentPlayerNum.innerText = state.currentPlayerIndex + 1;
    showScreen('pass');
}

function revealRole() {
    const role = state.roles[state.currentPlayerIndex];
    const isImpostor = role === "IMPOSTOR";

    els.roleContent.innerHTML = isImpostor
        ? `<div class="role-impostor">🤫 IMPOSTOR</div>`
        : `<div class="role-word">${role}</div>`;

    els.roleInstruction.innerText = isImpostor
        ? "Miente y descubre la palabra."
        : "Descubre quién es el impostor.";

    showScreen('reveal');
}

function hideRoleAndNext() {
    state.currentPlayerIndex++;
    showNextPlayerPassScreen();
}

/* --- TIMER LOGIC --- */
function startTimer() {
    showScreen('game');
    els.gameCategoryDisplay.innerText = "Categoría: " +
        (state.category === 'all' ? "Aleatoria" : state.category.charAt(0).toUpperCase() + state.category.slice(1));

    let timeLeft = state.timer;
    const totalTime = state.timer;
    const circle = els.timerProgress;
    const radius = 45;
    const circumference = 2 * Math.PI * radius;

    clearInterval(state.timerInterval);

    updateTimerDisplay(timeLeft);

    state.timerInterval = setInterval(() => {
        timeLeft--;
        updateTimerDisplay(timeLeft);

        // Update SVG Progress
        const dashoffset = circumference - (timeLeft / totalTime) * circumference;
        circle.style.strokeDashoffset = dashoffset;

        if (timeLeft <= 0) {
            clearInterval(state.timerInterval);
            els.timerDisplay.innerText = "TIEMPO";
            circle.style.stroke = "red";
        }
    }, 1000);
}

function updateTimerDisplay(seconds) {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    els.timerDisplay.innerText = `${m}:${s}`;
}

/* --- EVENT LISTENERS --- */
document.getElementById('btn-start-game').addEventListener('click', startGame);
document.getElementById('btn-reveal-role').addEventListener('click', revealRole);
document.getElementById('btn-hide-role').addEventListener('click', hideRoleAndNext);

document.getElementById('btn-end-game').addEventListener('click', () => {
    clearInterval(state.timerInterval);
    // Reveal everything
    const winnerText = state.roles.includes("IMPOSTOR") ? `La palabra era: ${state.secretWord}` : "Juego terminado";
    alert(winnerText); // Simple alert for now, could be a modal
    showScreen('setup');
});

document.getElementById('btn-new-game').addEventListener('click', () => {
    clearInterval(state.timerInterval);
    showScreen('setup');
});

// Initialize
updateCounts();

/* --- DATA --- */
const CATEGORIES = {
    peliculas: [
        "MATRIX", "TERMINATOR", "ALIEN", "TITANIC", "AVATAR", "GLADIADOR", "ORIGEN",
        "INTERSTELLAR", "JOKER", "PSICOSIS", "RESPLANDOR", "ROCKY", "SHREK", "FROZEN"
    ],
    tecnologia: [
        "JAVASCRIPT", "PYTHON", "ALGORITMO", "SERVIDOR", "ENCRIPTADO", "FIREWALL",
        "DATABASE", "PROCESADOR", "QUANTUM", "INTERFACE", "ANDROID", "CIBERNETICA", "SOFTWARE"
    ],
    paises: [
        "ESPAÑA", "JAPON", "ALEMANIA", "ARGENTINA", "CANADA", "NORUEGA", "BRASIL",
        "EGIPTO", "ISLANDIA", "VIETNAM", "SUECIA", "COREA", "FRANCIA", "ITALIA", "MEXICO"
    ]
};

/* --- STATE --- */
const state = {
    word: "",
    category: "",
    guessed: new Set(),
    wrongGuesses: 0,
    maxLives: 6,
    score: 0,
    isPlaying: false
};

/* --- DOM ELEMENTS --- */
const els = {
    wordDisplay: document.getElementById('word-display'),
    keyboard: document.getElementById('keyboard'),
    scoreVal: document.getElementById('score-val'),
    categoryVal: document.getElementById('category-val'),
    modalScreen: document.getElementById('modal-screen'),
    modalTitle: document.getElementById('modal-title'),
    modalMsg: document.getElementById('modal-msg'),
    targetWord: document.getElementById('target-word'),
    btnRestart: document.getElementById('btn-restart'),
    startScreen: document.getElementById('start-screen'),
    bodyParts: document.querySelectorAll('.draw-part')
};

/* --- INIT --- */
function init() {
    createKeyboard();
    attachEvents();
}

function createKeyboard() {
    els.keyboard.innerHTML = '';
    const letters = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"; // Added Ñ
    for (let char of letters) {
        const btn = document.createElement('button');
        btn.classList.add('key-btn');
        btn.textContent = char;
        btn.dataset.key = char;
        btn.addEventListener('click', () => handleGuess(char));
        els.keyboard.appendChild(btn);
    }
}

function attachEvents() {
    // Physical Keyboard support
    document.addEventListener('keydown', (e) => {
        if (!state.isPlaying) return;
        let char = e.key.toUpperCase();
        if (char === 'N' && e.key === 'ñ') char = 'Ñ'; // Basic handling, usually key is already correct or code needed
        // Fix for standard layouts
        if (e.key === 'ñ' || e.key === 'Ñ') char = 'Ñ';

        if (state.guessed.has(char)) return;
        if (/^[A-ZÑ]$/.test(char)) {
            handleGuess(char);
        }
    });

    // Category Selection
    document.querySelectorAll('.cat-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const catKey = btn.dataset.cat;
            startGame(catKey);
        });
    });

    // Restart
    els.btnRestart.addEventListener('click', () => {
        els.modalScreen.classList.add('hidden');
        els.startScreen.classList.remove('hidden'); // Go back to category select
    });
}

/* --- GAME LOGIC --- */
function startGame(catKey) {
    state.category = catKey;
    state.guessed.clear();
    state.wrongGuesses = 0;
    state.isPlaying = true;

    // Select Word
    let pool = [];
    if (catKey === 'aleatorio') {
        Object.values(CATEGORIES).forEach(arr => pool.push(...arr));
        els.categoryVal.textContent = "DB_ALEATORIA";
    } else {
        pool = CATEGORIES[catKey];
        els.categoryVal.textContent = catKey.toUpperCase();
    }
    state.word = pool[Math.floor(Math.random() * pool.length)];

    // UI Reset
    els.startScreen.classList.add('hidden');
    els.bodyParts.forEach(part => part.classList.remove('visible'));

    // Reset Keyboard
    document.querySelectorAll('.key-btn').forEach(btn => {
        btn.disabled = false;
        btn.className = 'key-btn';
    });

    renderWord();
}

function handleGuess(char) {
    if (!state.isPlaying || state.guessed.has(char)) return;

    state.guessed.add(char);

    // Update Keyboard UI
    const btn = document.querySelector(`.key-btn[data-key="${char}"]`);
    if (btn) btn.disabled = true;

    if (state.word.includes(char)) {
        // Correct
        if (btn) btn.classList.add('correct');
        renderWord();
        checkWin();
    } else {
        // Wrong
        if (btn) btn.classList.add('wrong');
        state.wrongGuesses++;
        drawHangman(state.wrongGuesses);
        checkLoss();
    }
}

function renderWord() {
    els.wordDisplay.innerHTML = '';
    const wordArray = state.word.split('');
    let allGuessed = true;

    wordArray.forEach(char => {
        const slot = document.createElement('div');
        slot.classList.add('letter-slot');
        if (state.guessed.has(char)) {
            slot.textContent = char;
            slot.classList.add('filled');
        } else {
            slot.textContent = "";
            allGuessed = false;
        }
        els.wordDisplay.appendChild(slot);
    });

    return allGuessed;
}

function drawHangman(errors) {
    // errors is 1-indexed, so part index is errors - 1
    // We have 6 parts (0 to 5)
    // 0: Head, 1: Body, 2: L-Arm, 3: R-Arm, 4: L-Leg, 5: R-Leg
    const partIndex = errors - 1;
    if (partIndex >= 0 && partIndex < els.bodyParts.length) {
        els.bodyParts[partIndex].classList.add('visible');
    }
}

function checkWin() {
    const isWon = state.word.split('').every(c => state.guessed.has(c));
    if (isWon) {
        endGame(true);
    }
}

function checkLoss() {
    if (state.wrongGuesses >= state.maxLives) {
        endGame(false);
    }
}

function endGame(isVictory) {
    state.isPlaying = false;
    setTimeout(() => {
        els.modalScreen.classList.remove('hidden');
        els.targetWord.textContent = state.word;

        if (isVictory) {
            els.modalTitle.textContent = "SISTEMA HACKEADO";
            els.modalTitle.className = "neon-green";
            els.modalMsg.textContent = "ACCESO CONCEDIDO";
            state.score += 100;
            els.scoreVal.textContent = state.score.toString().padStart(4, '0');
        } else {
            els.modalTitle.textContent = "FALLO DEL SISTEMA";
            els.modalTitle.className = "neon-red";
            els.modalMsg.textContent = "TERMINAL BLOQUEADO";
            state.score = Math.max(0, state.score - 50); // Penalty
            els.scoreVal.textContent = state.score.toString().padStart(4, '0');
        }
    }, 500);
}

// Start
init();

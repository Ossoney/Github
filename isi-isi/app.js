/* ============================================
   isi-isi — App de Gastos Compartidos
   Lógica completa: estado, i18n, multi-grupo,
   renderizado, algoritmos, persistencia, onboarding
   ============================================ */

// ---- Constants & Keys ----
const STORAGE_KEY = 'isi-isi-multidata'; // New key for multi-group support

const CATEGORIES = [
  { id: 'food',      icon: '🍔' },
  { id: 'home',      icon: '🏠' },
  { id: 'transport', icon: '🚗' },
  { id: 'fun',       icon: '🎉' },
  { id: 'shopping',  icon: '🛒' },
  { id: 'services',  icon: '💡' },
  { id: 'travel',    icon: '✈️' },
  { id: 'other',     icon: '📌' },
];

// ---- i18n Dictionaries ----
const DICS = {
  es: {
    months: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
    categories: {
      food: 'Comida', home: 'Casa', transport: 'Transporte', fun: 'Ocio', shopping: 'Compras', services: 'Servicios', travel: 'Viaje', other: 'Otro'
    },
    onboard_subtitle: 'Gastos compartidos, sin líos.<br>Configura tu grupo para empezar.',
    onboard_step0_title: '¿Cómo se llama el grupo?',
    onboard_step0_placeholder: 'Ej: Viaje Asturias, Piso centro...',
    onboard_step0_hint: 'Dale un nombre para identificarlo fácilmente.',
    onboard_step1_title: '¿Cómo te llamas?',
    onboard_step1_placeholder: 'Tu nombre...',
    onboard_step1_hint: 'Para saber quién eres dentro del grupo.',
    onboard_step2_title: 'Añade a los demás miembros',
    onboard_step2_placeholder: 'Nombre del miembro...',
    onboard_counter_empty: 'Añade al menos 1 miembro más aparte de ti.',
    onboard_counter_filled: 'miembro(s) añadido(s) (mínimo 1)',
    next: 'Siguiente →',
    back: '← Atrás',
    start: '¡Empezar!',
    groups_title: 'Mis Grupos',
    members_title: 'Miembros del Grupo',
    switch_group: 'Cambiar grupo',
    share: 'Compartir',
    reset: 'Resetear datos',
    add_expense: 'Añadir gasto',
    nav_inicio: 'Inicio',
    nav_gastos: 'Gastos',
    nav_saldos: 'Saldos',
    nav_balance: 'Balance',
    nav_stats: 'Stats',
    new_expense: 'Nuevo gasto',
    edit_expense: 'Editar gasto',
    expense_title_label: '¿En qué se gastó?',
    expense_title_placeholder: 'Ej: Cena, Supermercado...',
    amount: 'Importe',
    who_paid: '¿Quién pagó?',
    category: 'Categoría',
    split_among: 'Dividir entre',
    split_equal: 'Equitativo',
    split_shares: 'Partes',
    split_exact: 'Exacto',
    date: 'Fecha',
    cancel: 'Cancelar',
    save: 'Guardar',
    group: 'Grupo',
    group_name_label: 'Nombre del grupo',
    group_name_placeholder: 'Nombre del grupo',
    members: 'Miembros',
    add_member_placeholder: 'Añadir miembro...',
    you_are: 'Tú eres...',
    my_groups: 'Mis Grupos',
    new_group_placeholder: 'Nombre del nuevo grupo...',
    create: 'Crear',
    detail: 'Detalle',
    delete: 'Eliminar',
    paid_by: 'Pagado por',
    divided_among: 'Dividir entre ({{count}} personas)',
    edit: 'Editar',
    state_settled: 'Todo liquidado',
    state_settled_subtitle: 'No hay deudas pendientes entre los miembros.',
    transfers_needed: 'Transferencias necesarias',
    transfers_subtitle: 'movimientos para liquidar todas las deudas',
    who_pays_whom: 'Quién paga a quién',
    settle: 'Liquidar',
    total_group_spend: 'Gasto total del grupo',
    by_category: 'Por categoría',
    summary: 'Resumen',
    average_per_person: 'Media / persona',
    all: 'Todos',
    spent_total: 'total',
    spent_total_paid: 'Total pagado por persona',
    spent_net_balance: 'Saldo neto de cada miembro',
    active_you: 'Tú',
    paid_past: 'pagó',
    toast_quota: 'Espacio lleno',
    toast_exists: 'Ya existe',
    toast_fill_all: 'Completa todos los campos',
    toast_select_participant: 'Selecciona al menos un participante',
    toast_pct_sum: 'Los porcentajes deben sumar 100%',
    toast_shares_sum: 'Asigna al menos una parte',
    toast_exact_sum: 'Las cantidades deben sumar el total',
    toast_saved: 'Gasto añadido',
    toast_updated: 'Gasto actualizado',
    toast_deleted: 'Gasto eliminado',
    toast_settled: 'Deuda liquidada',
    toast_removed_member: 'Miembro eliminado',
    toast_cannot_remove: 'No se puede eliminar: tiene gastos asociados',
    toast_group_created: '¡Grupo "{{name}}" creado!',
    toast_import_ok: 'Grupo importado con éxito',
    toast_import_err: 'Error al importar el enlace',
    toast_confirm_settle: '¿Confirmar que {{from}} pagó {{amount}} a {{to}}?',
    toast_confirm_reset: '¿Borrar TODOS los datos de todos los grupos y empezar de cero?',
    toast_confirm_delete_group: '¿Eliminar el grupo "{{name}}"? Todos sus gastos se perderán.',
    toast_confirm_delete_expense: '¿Eliminar este gasto? Esta acción no se puede deshacer.',
    empty_no_expenses: 'No hay gastos aún.<br>Pulsa <strong>+</strong> para añadir uno.',
    empty_no_members: 'Añade miembros al grupo primero.',
    empty_no_stats: 'Las estadísticas aparecerán cuando añadas gastos.',
    estas_en_paz: 'Estás en paz ✌️',
    te_deben: 'Te deben',
    debes: 'Debes',
    total_grupo: 'Total del grupo',
    deudas_simplificadas: 'Deudas simplificadas',
    actividad_reciente: 'Actividad reciente',
    first_expense_prompt: '¡Añade tu primer gasto!<br>Pulsa el botón <strong>+</strong> para empezar.',
    share_interactive_link: 'Ver grupo interactivo:',
    sent_from_app: 'Enviado desde isi-isi',
  },
  en: {
    months: ['January','February','March','April','May','June','July','August','September','October','November','December'],
    categories: {
      food: 'Food', home: 'Home', transport: 'Transport', fun: 'Leisure', shopping: 'Shopping', services: 'Utilities', travel: 'Travel', other: 'Other'
    },
    onboard_subtitle: 'Shared expenses, simplified.<br>Configure your group to start.',
    onboard_step0_title: 'What is the group name?',
    onboard_step0_placeholder: 'e.g. Trip to London, Shared flat...',
    onboard_step0_hint: 'Give it a name to identify it easily.',
    onboard_step1_title: 'What is your name?',
    onboard_step1_placeholder: 'Your name...',
    onboard_step1_hint: 'So we know who you are in the group.',
    onboard_step2_title: 'Add the other members',
    onboard_step2_placeholder: 'Member name...',
    onboard_counter_empty: 'Add at least 1 more member besides yourself.',
    onboard_counter_filled: 'member(s) added (minimum 1)',
    next: 'Next →',
    back: '← Back',
    start: 'Start!',
    groups_title: 'My Groups',
    members_title: 'Group Members',
    switch_group: 'Switch group',
    share: 'Share',
    reset: 'Reset data',
    add_expense: 'Add expense',
    nav_inicio: 'Home',
    nav_gastos: 'Expenses',
    nav_saldos: 'Balances',
    nav_balance: 'Settle up',
    nav_stats: 'Stats',
    new_expense: 'New expense',
    edit_expense: 'Edit expense',
    expense_title_label: 'What was it spent on?',
    expense_title_placeholder: 'e.g. Dinner, Supermarket...',
    amount: 'Amount',
    who_paid: 'Who paid?',
    category: 'Category',
    split_among: 'Split among',
    split_equal: 'Equally',
    split_shares: 'Shares',
    split_exact: 'Exact',
    date: 'Date',
    cancel: 'Cancel',
    save: 'Save',
    group: 'Group',
    group_name_label: 'Group name',
    group_name_placeholder: 'Group name',
    members: 'Members',
    add_member_placeholder: 'Add member...',
    you_are: 'You are...',
    my_groups: 'My Groups',
    new_group_placeholder: 'New group name...',
    create: 'Create',
    detail: 'Detail',
    delete: 'Delete',
    paid_by: 'Paid by',
    divided_among: 'Split among ({{count}} people)',
    edit: 'Edit',
    state_settled: 'Settle Up',
    state_settled_subtitle: 'No pending debts between members.',
    transfers_needed: 'Suggested transfers',
    transfers_subtitle: 'payments to settle all debts',
    who_pays_whom: 'Who pays whom',
    settle: 'Settle',
    total_group_spend: 'Total group spend',
    by_category: 'By category',
    summary: 'Summary',
    average_per_person: 'Average per person',
    all: 'All',
    spent_total: 'total',
    spent_total_paid: 'Total paid per person',
    spent_net_balance: 'Net balance per member',
    active_you: 'You',
    paid_past: 'paid',
    toast_quota: 'Storage full',
    toast_exists: 'Already exists',
    toast_fill_all: 'Please fill in all fields',
    toast_select_participant: 'Select at least one participant',
    toast_pct_sum: 'Percentages must sum to 100%',
    toast_shares_sum: 'Assign at least one share',
    toast_exact_sum: 'Amounts must sum to total',
    toast_saved: 'Expense added',
    toast_updated: 'Expense updated',
    toast_deleted: 'Expense deleted',
    toast_settled: 'Debt settled',
    toast_removed_member: 'Member removed',
    toast_cannot_remove: 'Cannot remove: associated expenses exist',
    toast_group_created: 'Group "{{name}}" created!',
    toast_import_ok: 'Group imported successfully',
    toast_import_err: 'Error importing link',
    toast_confirm_settle: 'Confirm that {{from}} paid {{amount}} to {{to}}?',
    toast_confirm_reset: 'Erase ALL data of all groups and start fresh?',
    toast_confirm_delete_group: 'Delete group "{{name}}"? All its expenses will be lost.',
    toast_confirm_delete_expense: 'Delete this expense? This cannot be undone.',
    empty_no_expenses: 'No expenses yet.<br>Tap <strong>+</strong> to add one.',
    empty_no_members: 'Add group members first.',
    empty_no_stats: 'Stats will appear when you add expenses.',
    estas_en_paz: 'You are all settled up ✌️',
    te_deben: 'You are owed',
    debes: 'You owe',
    total_grupo: 'Group total',
    deudas_simplificadas: 'Simplified debts',
    actividad_reciente: 'Recent activity',
    first_expense_prompt: 'Add your first expense!<br>Press the <strong>+</strong> button to start.',
    share_interactive_link: 'View interactive group:',
    sent_from_app: 'Sent from isi-isi',
  }
};

// Select Language
let lang = 'es';
const userLang = navigator.language || navigator.userLanguage;
if (userLang && !userLang.toLowerCase().startsWith('es')) {
  lang = 'en';
}

function t(key, vars = {}) {
  const dictionary = DICS[lang] || DICS.es;
  let raw = dictionary[key] || DICS.es[key] || key;
  Object.keys(vars).forEach(k => {
    raw = raw.replace(`{{${k}}}`, vars[k]);
  });
  return raw;
}

// Localize DOM Elements
function localizeDOM() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.innerHTML = t(key);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    el.setAttribute('placeholder', t(key));
  });
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    el.setAttribute('title', t(key));
  });
  // Localize category labels
  CATEGORIES.forEach(c => {
    c.label = t('categories')[c.id] || c.id;
  });
}

// ---- Global State ----
// Multi-group schema: { activeGroupId: String, groups: { [id]: { group: {...}, expenses: [], payments: [] } } }
let db = {
  activeGroupId: '',
  groups: {}
};

let state = {
  group: { name: 'isi-isi', currency: '€', members: [], currentUser: null },
  expenses: [],
  payments: [],
  currentView: 'dashboard',
  filterCategory: 'all',
};

// ---- Modal/Form State ----
let splitMode = 'equal';
let selectedPayer = null;
let selectedCategory = 'other';
let splitChecked = {};
let splitShares = {};
let splitPercentages = {};
let splitExact = {};
let editingExpenseId = null;
let confirmCallback = null;

// ---- Onboarding State ----
let onboardStep = 0;
let onboardMembers = [];

// ---- Persistence ----
function save() {
  try {
    if (db.activeGroupId) {
      db.groups[db.activeGroupId] = {
        group: state.group,
        expenses: state.expenses,
        payments: state.payments
      };
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
  } catch (e) { /* quota exceeded */ }
}

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      db = JSON.parse(raw);
      if (!db.groups) db.groups = {};
      
      // Fallback for legacy format
      const legacyRaw = localStorage.getItem('isi-isi-data');
      if (legacyRaw && Object.keys(db.groups).length === 0) {
        const legacyData = JSON.parse(legacyRaw);
        const legacyId = uid();
        db.groups[legacyId] = {
          group: legacyData.group || { name: 'isi-isi', currency: '€', members: [], currentUser: null },
          expenses: legacyData.expenses || [],
          payments: legacyData.payments || []
        };
        db.activeGroupId = legacyId;
        localStorage.removeItem('isi-isi-data');
      }

      if (db.activeGroupId && db.groups[db.activeGroupId]) {
        const active = db.groups[db.activeGroupId];
        state.group = active.group;
        state.expenses = active.expenses || [];
        state.payments = active.payments || [];
        return true;
      }
    }
  } catch (e) { /* corrupted */ }
  return false;
}

// ---- Utilities ----
function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
}

function hashColor(name) {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = ((hash % 360) + 360) % 360;
  return `hsl(${hue}, 55%, 50%)`;
}

function getInitials(name) {
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
  }
  return parts[0].charAt(0).toUpperCase();
}

function avatarHTML(member, sizeClass = '') {
  const initials = getInitials(member.name);
  const cls = sizeClass ? `avatar ${sizeClass}` : 'avatar';
  return `<div class="${cls}" style="background:${hashColor(member.name)}">${initials}</div>`;
}

function fmt(amount) {
  return amount.toFixed(2).replace('.', ',') + ' ' + state.group.currency;
}

function fmtDate(isoStr) {
  const d = new Date(isoStr);
  const months = t('months');
  return d.getDate() + ' ' + months[d.getMonth()].toLowerCase().slice(0, 3) + ' ' + d.getFullYear();
}

function fmtDateTime(isoStr) {
  const d = new Date(isoStr);
  const day = d.getDate();
  const months = t('months');
  const mon = months[d.getMonth()].toLowerCase().slice(0, 3);
  const h = String(d.getHours()).padStart(2, '0');
  const m = String(d.getMinutes()).padStart(2, '0');
  return `${day} ${mon} ${h}:${m}`;
}

function getMember(id) {
  return state.group.members.find(m => m.id === id);
}

function getCategoryInfo(catId) {
  return CATEGORIES.find(c => c.id === catId) || CATEGORIES[CATEGORIES.length - 1];
}

function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ---- Core Algorithms ----
function calcBalances() {
  const balances = {};
  state.group.members.forEach(m => { balances[m.id] = 0; });

  state.expenses.forEach(exp => {
    if (balances[exp.paidBy] !== undefined) {
      balances[exp.paidBy] += exp.amount;
    }
    Object.keys(exp.splits).forEach(mid => {
      if (balances[mid] !== undefined) {
        balances[mid] -= exp.splits[mid];
      }
    });
  });

  state.payments.forEach(p => {
    if (balances[p.from] !== undefined) balances[p.from] += p.amount;
    if (balances[p.to] !== undefined) balances[p.to] -= p.amount;
  });

  return balances;
}

function simplifyDebts() {
  const balances = calcBalances();
  const debtors = [];
  const creditors = [];

  Object.keys(balances).forEach(id => {
    const bal = Math.round(balances[id] * 100) / 100;
    if (bal < -0.01) debtors.push({ id, amount: -bal });
    else if (bal > 0.01) creditors.push({ id, amount: bal });
  });

  debtors.sort((a, b) => b.amount - a.amount);
  creditors.sort((a, b) => b.amount - a.amount);

  const transfers = [];
  let di = 0, ci = 0;

  while (di < debtors.length && ci < creditors.length) {
    const transfer = Math.min(debtors[di].amount, creditors[ci].amount);
    if (transfer > 0.01) {
      transfers.push({
        from: debtors[di].id,
        to: creditors[ci].id,
        amount: Math.round(transfer * 100) / 100,
      });
    }
    debtors[di].amount -= transfer;
    creditors[ci].amount -= transfer;
    if (debtors[di].amount < 0.01) di++;
    if (creditors[ci].amount < 0.01) ci++;
  }

  return transfers;
}

function totalSpent() {
  return state.expenses.reduce((sum, e) => sum + e.amount, 0);
}

function totalPaidBy(memberId) {
  return state.expenses
    .filter(e => e.paidBy === memberId)
    .reduce((sum, e) => sum + e.amount, 0);
}

function spendingByCategory() {
  const cats = {};
  state.expenses.forEach(e => {
    cats[e.category] = (cats[e.category] || 0) + e.amount;
  });
  return cats;
}

// ---- Navigation ----
function nav(viewId) {
  state.currentView = viewId;
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const target = document.getElementById('view-' + viewId);
  if (target) target.classList.add('active');
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.view === viewId);
  });
  renderView(viewId);
}

// ---- Rendering ----
function render() {
  renderHeader();
  renderView(state.currentView);
}

function renderHeader() {
  document.getElementById('header-title').textContent = state.group.name;
  document.getElementById('header-subtitle').textContent = `Total: ${fmt(totalSpent())}`;
}

function renderView(viewId) {
  switch (viewId) {
    case 'dashboard': renderDashboard(); break;
    case 'expenses':  renderExpenses(); break;
    case 'saldos':    renderSaldos(); break;
    case 'balance':   renderBalance(); break;
    case 'stats':     renderStats(); break;
  }
}

// ---- Dashboard ----
function renderDashboard() {
  const container = document.getElementById('dashboard-content');
  const balances = calcBalances();
  const transfers = simplifyDebts();
  const currentUser = state.group.currentUser;

  let summaryHTML = '';
  if (currentUser && balances[currentUser] !== undefined) {
    const myBal = Math.round(balances[currentUser] * 100) / 100;
    let amountClass = 'zero', label = t('estas_en_paz');
    if (myBal > 0.01) { amountClass = 'positive'; label = t('te_deben'); }
    else if (myBal < -0.01) { amountClass = 'negative'; label = t('debes'); }
    summaryHTML = `
      <div class="summary-card">
        <div class="label">${label}</div>
        <div class="amount ${amountClass}">${fmt(Math.abs(myBal))}</div>
        <div class="sub-label">${state.expenses.length} ${t('nav_gastos').toLowerCase()} · ${fmt(totalSpent())} ${t('spent_total')}</div>
      </div>`;
  } else {
    summaryHTML = `
      <div class="summary-card">
        <div class="label">${t('total_grupo')}</div>
        <div class="amount zero">${fmt(totalSpent())}</div>
        <div class="sub-label">${state.expenses.length} ${t('nav_gastos').toLowerCase()} · ${state.group.members.length} ${t('members').toLowerCase()}</div>
      </div>`;
  }

  let debtsHTML = '';
  if (transfers.length > 0) {
    debtsHTML = `<div class="section-title">${t('deudas_simplificadas')}</div><div class="glass-card" style="padding:var(--space-sm)">`;
    transfers.forEach(tCode => {
      const from = getMember(tCode.from), to = getMember(tCode.to);
      if (!from || !to) return;
      debtsHTML += `
        <div class="debt-item">
          ${avatarHTML(from, 'sm')}
          <div class="debt-info"><div class="debt-names">${escapeHTML(from.name)}<span class="arrow">→</span>${escapeHTML(to.name)}</div></div>
          <div class="debt-amount">${fmt(tCode.amount)}</div>
          <button class="btn-settle" onclick="settleDebt('${tCode.from}','${tCode.to}',${tCode.amount})">${t('settle')}</button>
        </div>`;
    });
    debtsHTML += '</div>';
  } else if (state.expenses.length > 0) {
    debtsHTML = `<div class="section-title">${t('nav_balance')}</div>
      <div class="empty-state"><div class="empty-icon">🎉</div><div class="empty-text">${t('state_settled_subtitle')}</div></div>`;
  }

  let recentHTML = '';
  const recent = [...state.expenses].sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)).slice(0, 5);
  if (recent.length > 0) {
    recentHTML = `<div class="section-title">${t('actividad_reciente')}</div>`;
    recent.forEach(exp => {
      const payer = getMember(exp.paidBy);
      if (!payer) return;
      recentHTML += `
        <div class="activity-item">
          <div class="activity-dot"></div>
          <div class="activity-text"><strong>${escapeHTML(payer.name)}</strong> ${t('paid_past')} ${fmt(exp.amount)} — ${escapeHTML(exp.title)}</div>
          <div class="activity-time">${fmtDateTime(exp.date)}</div>
        </div>`;
    });
  }

  if (state.expenses.length === 0) {
    container.innerHTML = summaryHTML + `
      <div class="empty-state"><div class="empty-icon">💸</div><div class="empty-text">${t('first_expense_prompt')}</div></div>`;
    return;
  }

  container.innerHTML = summaryHTML + debtsHTML + recentHTML;
}

// ---- Expenses ----
function renderExpenses() {
  const container = document.getElementById('expenses-content');

  if (state.expenses.length === 0) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">📋</div><div class="empty-text">${t('empty_no_expenses')}</div></div>`;
    return;
  }

  let pillsHTML = `<div class="filter-pills"><button class="pill ${state.filterCategory === 'all' ? 'active' : ''}" onclick="setFilter('all')">${t('all')}</button>`;
  CATEGORIES.forEach(c => {
    if (state.expenses.some(e => e.category === c.id)) {
      pillsHTML += `<button class="pill ${state.filterCategory === c.id ? 'active' : ''}" onclick="setFilter('${c.id}')">${c.icon} ${t('categories')[c.id]}</button>`;
    }
  });
  pillsHTML += '</div>';

  let filtered = state.expenses;
  if (state.filterCategory !== 'all') filtered = filtered.filter(e => e.category === state.filterCategory);
  filtered = [...filtered].sort((a, b) => new Date(b.date) - new Date(a.date));

  const groups = {};
  filtered.forEach(exp => {
    const d = new Date(exp.date);
    const key = `${d.getFullYear()}-${d.getMonth()}`;
    const months = t('months');
    if (!groups[key]) groups[key] = { label: months[d.getMonth()] + ' ' + d.getFullYear(), items: [] };
    groups[key].items.push(exp);
  });

  let listHTML = '';
  Object.values(groups).forEach(grp => {
    listHTML += `<div class="month-group"><div class="month-header">${grp.label}</div>`;
    grp.items.forEach(exp => {
      const cat = getCategoryInfo(exp.category);
      const payer = getMember(exp.paidBy);
      const pIds = Object.keys(exp.splits);
      const avatars = pIds.slice(0, 3).map(mid => { const m = getMember(mid); return m ? avatarHTML(m, 'sm') : ''; }).join('');
      const more = pIds.length - 3;
      listHTML += `
        <div class="expense-item" onclick="showExpenseDetail('${exp.id}')">
          <div class="expense-icon">${cat.icon}</div>
          <div class="expense-info">
            <div class="title">${escapeHTML(exp.title)}</div>
            <div class="meta"><span>${payer ? escapeHTML(payer.name) + ' ' + t('paid_past') : ''}</span><span>·</span><span>${fmtDate(exp.date)}</span></div>
          </div>
          <div class="expense-right">
            <div class="amount">${fmt(exp.amount)}</div>
            <div class="participants"><div class="avatar-stack">${avatars}${more > 0 ? `<div class="avatar-more">+${more}</div>` : ''}</div></div>
          </div>
        </div>`;
    });
    listHTML += '</div>';
  });

  container.innerHTML = pillsHTML + listHTML;
}

// ---- Saldos ----
function renderSaldos() {
  const container = document.getElementById('saldos-content');
  const balances = calcBalances();

  if (state.group.members.length === 0) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">👥</div><div class="empty-text">${t('empty_no_members')}</div></div>`;
    return;
  }

  const maxBal = Math.max(...Object.values(balances).map(Math.abs), 1);

  let html = `<div class="section-title">${t('spent_net_balance')}</div><div class="glass-card" style="padding:var(--space-sm)">`;
  state.group.members
    .map(m => ({ m, bal: Math.round((balances[m.id] || 0) * 100) / 100 }))
    .sort((a, b) => b.bal - a.bal)
    .forEach(({ m, bal }) => {
      const pct = Math.abs(bal) / maxBal * 100;
      const cls = bal > 0.01 ? 'positive' : bal < -0.01 ? 'negative' : 'zero';
      const barCls = bal >= 0 ? 'positive' : 'negative';
      html += `
        <div class="balance-item">
          ${avatarHTML(m)}
          <div class="balance-info">
            <div class="name">${escapeHTML(m.name)}</div>
            <div class="bar-track"><div class="bar-fill ${barCls}" style="width:${pct}%"></div></div>
          </div>
          <div class="balance-amount ${cls}">${bal > 0 ? '+' : ''}${fmt(bal)}</div>
        </div>`;
    });
  html += '</div>';

  // Per-person paid totals
  const maxPaid = Math.max(...state.group.members.map(m => totalPaidBy(m.id)), 1);
  html += `<div class="section-title">${t('spent_total_paid')}</div><div class="glass-card" style="padding:var(--space-sm)">`;
  state.group.members
    .map(m => ({ m, paid: totalPaidBy(m.id) }))
    .sort((a, b) => b.paid - a.paid)
    .forEach(({ m, paid }) => {
      const pct = (paid / maxPaid) * 100;
      html += `
        <div class="balance-item">
          ${avatarHTML(m)}
          <div class="balance-info">
            <div class="name">${escapeHTML(m.name)}</div>
            <div class="bar-track"><div class="bar-fill positive" style="width:${pct}%"></div></div>
          </div>
          <div class="balance-amount" style="color:var(--text-primary)">${fmt(paid)}</div>
        </div>`;
    });
  html += '</div>';

  container.innerHTML = html;
}

// ---- Balance (simplified transfers) ----
function renderBalance() {
  const container = document.getElementById('balance-content');
  const transfers = simplifyDebts();

  if (state.group.members.length === 0) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">👥</div><div class="empty-text">${t('empty_no_members')}</div></div>`;
    return;
  }

  if (transfers.length === 0) {
    container.innerHTML = `
      <div class="summary-card" style="margin-bottom:var(--space-lg)">
        <div class="label">${t('group')}</div>
        <div class="amount positive" style="font-size:1.5rem">✅ ${t('state_settled')}</div>
        <div class="sub-label">${t('state_settled_subtitle')}</div>
      </div>`;
    return;
  }

  let html = `
    <div class="summary-card" style="margin-bottom:var(--space-lg)">
      <div class="label">${t('transfers_needed')}</div>
      <div class="amount zero" style="font-size:1.8rem">${transfers.length}</div>
      <div class="sub-label">${t('transfers_subtitle')}</div>
    </div>
    <div class="section-title">${t('who_pays_whom')}</div>
    <div class="glass-card" style="padding:var(--space-sm)">`;

  transfers.forEach(tCode => {
    const from = getMember(tCode.from), to = getMember(tCode.to);
    if (!from || !to) return;
    html += `
      <div class="debt-item">
        ${avatarHTML(from, 'sm')}
        <div class="debt-info"><div class="debt-names">${escapeHTML(from.name)}<span class="arrow">→</span>${escapeHTML(to.name)}</div></div>
        <div class="debt-amount">${fmt(tCode.amount)}</div>
        <button class="btn-settle" onclick="settleDebt('${tCode.from}','${tCode.to}',${tCode.amount})">${t('settle')}</button>
      </div>`;
  });

  html += '</div>';
  container.innerHTML = html;
}

// ---- Stats ----
function renderStats() {
  const container = document.getElementById('stats-content');

  if (state.expenses.length === 0) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-text">${t('empty_no_stats')}</div></div>`;
    return;
  }

  const total = totalSpent();

  let html = `<div class="stat-card"><div class="stat-title">${t('total_group_spend')}</div><div class="stat-value">${fmt(total)}</div></div>`;

  // By category
  const catSpend = spendingByCategory();
  const catEntries = Object.entries(catSpend).sort((a, b) => b[1] - a[1]);
  const maxCat = catEntries.length > 0 ? catEntries[0][1] : 1;
  html += `<div class="stat-card"><div class="stat-title">${t('by_category')}</div>`;
  catEntries.forEach(([catId, amount]) => {
    const cat = getCategoryInfo(catId);
    const catLabel = t('categories')[catId] || catId;
    html += `
      <div class="stat-bar-row">
        <div class="stat-bar-label">${cat.icon} ${catLabel}</div>
        <div class="stat-bar-track"><div class="stat-bar-fill cat-${catId}" style="width:${(amount / maxCat) * 100}%"></div></div>
        <div class="stat-bar-value">${fmt(amount)}</div>
      </div>`;
  });
  html += '</div>';

  // Summary numbers
  html += `
    <div class="stat-card">
      <div class="stat-title">${t('summary')}</div>
      <div style="display:flex;gap:var(--space-lg);flex-wrap:wrap">
        <div><div style="font-size:1.8rem;font-weight:700">${state.expenses.length}</div><div style="font-size:0.75rem;color:var(--text-secondary)">${t('nav_gastos')}</div></div>
        <div><div style="font-size:1.8rem;font-weight:700">${state.group.members.length}</div><div style="font-size:0.75rem;color:var(--text-secondary)">${t('members')}</div></div>
        <div><div style="font-size:1.8rem;font-weight:700">${fmt(total / Math.max(state.group.members.length, 1))}</div><div style="font-size:0.75rem;color:var(--text-secondary)">${t('average_per_person')}</div></div>
      </div>
    </div>`;

  container.innerHTML = html;
}

// ---- Filter ----
function setFilter(cat) {
  state.filterCategory = cat;
  renderExpenses();
}

// ---- Modals ----
function openModal(id) {
  const el = document.getElementById(id);
  if (el) { el.classList.add('open'); document.body.style.overflow = 'hidden'; }
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) { el.classList.remove('open'); document.body.style.overflow = ''; }
}

// ---- Expense Modal ----
function openExpenseModal(expense) {
  editingExpenseId = expense ? expense.id : null;
  document.getElementById('modal-expense-title').textContent = expense ? t('edit_expense') : t('new_expense');

  document.getElementById('expense-id').value = expense ? expense.id : '';
  document.getElementById('expense-title-input').value = expense ? expense.title : '';
  document.getElementById('expense-amount-input').value = expense ? expense.amount : '';
  document.getElementById('expense-date-input').value = expense
    ? new Date(expense.date).toISOString().slice(0, 10)
    : new Date().toISOString().slice(0, 10);

  selectedPayer = expense ? expense.paidBy : (state.group.currentUser || (state.group.members[0]?.id || null));
  selectedCategory = expense ? expense.category : 'other';
  splitMode = expense ? (expense.splitMode || 'equal') : 'equal';

  splitChecked = {}; splitShares = {}; splitPercentages = {}; splitExact = {};
  state.group.members.forEach(m => {
    if (expense && expense.splits) {
      splitChecked[m.id] = m.id in expense.splits;
      splitShares[m.id] = splitChecked[m.id] ? 1 : 0;
      splitPercentages[m.id] = splitChecked[m.id] ? ((expense.splits[m.id] / expense.amount) * 100).toFixed(1) : '0';
      splitExact[m.id] = splitChecked[m.id] ? expense.splits[m.id].toFixed(2) : '0';
    } else {
      splitChecked[m.id] = true;
      splitShares[m.id] = 1;
      splitPercentages[m.id] = (100 / state.group.members.length).toFixed(1);
      splitExact[m.id] = '';
    }
  });

  renderPayerSelector();
  renderCategorySelector();
  renderSplitTabs();
  renderSplitConfig();
  openModal('modal-expense');
}

function renderPayerSelector() {
  document.getElementById('payer-selector').innerHTML = state.group.members.map(m => `
    <div class="chip ${selectedPayer === m.id ? 'active' : ''}" onclick="selectPayer('${m.id}')">
      ${avatarHTML(m)}<span>${escapeHTML(m.name)}</span>
    </div>`).join('');
}
function selectPayer(id) { selectedPayer = id; renderPayerSelector(); }

function renderCategorySelector() {
  document.getElementById('category-selector').innerHTML = CATEGORIES.map(c => `
    <button type="button" class="cat-btn ${selectedCategory === c.id ? 'active' : ''}" onclick="selectCategory('${c.id}')">
      <span class="cat-icon">${c.icon}</span><span>${t('categories')[c.id]}</span>
    </button>`).join('');
}
function selectCategory(id) { selectedCategory = id; renderCategorySelector(); }

function renderSplitTabs() {
  document.querySelectorAll('.split-tab').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.mode === splitMode);
  });
}
function setSplitMode(mode) { splitMode = mode; renderSplitTabs(); renderSplitConfig(); }

function renderSplitConfig() {
  const container = document.getElementById('split-config');
  const amount = parseFloat(document.getElementById('expense-amount-input').value) || 0;
  const members = state.group.members;
  let html = '';

  if (splitMode === 'equal') {
    const checkedCount = members.filter(m => splitChecked[m.id]).length;
    const perPerson = checkedCount > 0 ? amount / checkedCount : 0;
    members.forEach(m => {
      const checked = splitChecked[m.id];
      html += `<div class="split-row">
        <div class="split-check ${checked ? 'checked' : ''}" onclick="toggleSplitCheck('${m.id}')"></div>
        ${avatarHTML(m)}<div class="name">${escapeHTML(m.name)}</div>
        <div class="split-value">${checked ? fmt(perPerson) : '—'}</div>
      </div>`;
    });
  } else if (splitMode === 'percentage') {
    let totalPct = 0;
    members.forEach(m => { totalPct += parseFloat(splitPercentages[m.id]) || 0; });
    members.forEach(m => {
      const pct = splitPercentages[m.id] || '0';
      html += `<div class="split-row">${avatarHTML(m)}<div class="name">${escapeHTML(m.name)}</div>
        <input type="number" class="split-input" value="${pct}" step="0.1" min="0" max="100" onchange="setSplitPct('${m.id}',this.value)" onfocus="this.select()">
        <span class="split-suffix">%</span><div class="split-value">${fmt((parseFloat(pct)/100)*amount)}</div></div>`;
    });
    const totalCls = Math.abs(totalPct - 100) < 0.1 ? 'valid' : 'invalid';
    html += `<div class="split-total-row"><span>Total</span><span class="total-value ${totalCls}">${totalPct.toFixed(1)}%</span></div>`;
  } else if (splitMode === 'shares') {
    let totalSh = 0;
    members.forEach(m => { totalSh += splitShares[m.id] || 0; });
    const perShare = totalSh > 0 ? amount / totalSh : 0;
    members.forEach(m => {
      const s = splitShares[m.id] || 0;
      html += `<div class="split-row">${avatarHTML(m)}<div class="name">${escapeHTML(m.name)}</div>
        <div class="shares-control"><button type="button" class="shares-btn" onclick="adjShare('${m.id}',-1)">−</button>
        <div class="shares-count">${s}</div><button type="button" class="shares-btn" onclick="adjShare('${m.id}',1)">+</button></div>
        <div class="split-value">${fmt(s * perShare)}</div></div>`;
    });
  } else if (splitMode === 'exact') {
    let totalEx = 0;
    members.forEach(m => { totalEx += parseFloat(splitExact[m.id]) || 0; });
    members.forEach(m => {
      html += `<div class="split-row">${avatarHTML(m)}<div class="name">${escapeHTML(m.name)}</div>
        <input type="number" class="split-input" value="${splitExact[m.id] || ''}" step="0.01" min="0" placeholder="0,00"
        onchange="setSplitExact('${m.id}',this.value)" onfocus="this.select()"><span class="split-suffix">${state.group.currency}</span></div>`;
    });
    const diff = Math.round((amount - totalEx) * 100) / 100;
    const totalCls = Math.abs(diff) < 0.01 ? 'valid' : 'invalid';
    html += `<div class="split-total-row"><span>Total asignado</span><span class="total-value ${totalCls}">${fmt(totalEx)}${Math.abs(diff)>=0.01 ? ` (faltan ${fmt(diff)})` : ''}</span></div>`;
  }

  container.innerHTML = html;
}

function toggleSplitCheck(id) { splitChecked[id] = !splitChecked[id]; renderSplitConfig(); }
function setSplitPct(id, val) { splitPercentages[id] = val; renderSplitConfig(); }
function adjShare(id, delta) { splitShares[id] = Math.max(0, (splitShares[id] || 0) + delta); renderSplitConfig(); }
function setSplitExact(id, val) { splitExact[id] = val; renderSplitConfig(); }

// ---- Save Expense ----
function handleSaveExpense(e) {
  e.preventDefault();
  const title = document.getElementById('expense-title-input').value.trim();
  const amount = parseFloat(document.getElementById('expense-amount-input').value);
  const date = document.getElementById('expense-date-input').value;

  if (!title || !amount || amount <= 0 || !selectedPayer) { toast(t('toast_fill_all')); return; }

  const splits = {};
  const members = state.group.members;

  if (splitMode === 'equal') {
    const included = members.filter(m => splitChecked[m.id]);
    if (included.length === 0) { toast(t('toast_select_participant')); return; }
    const pp = amount / included.length;
    included.forEach(m => { splits[m.id] = Math.round(pp * 100) / 100; });
  } else if (splitMode === 'percentage') {
    let tp = 0;
    members.forEach(m => { const p = parseFloat(splitPercentages[m.id]) || 0; tp += p; if (p > 0) splits[m.id] = Math.round((p/100)*amount*100)/100; });
    if (Math.abs(tp - 100) > 0.5) { toast(t('toast_pct_sum')); return; }
  } else if (splitMode === 'shares') {
    let ts = 0;
    members.forEach(m => { ts += splitShares[m.id] || 0; });
    if (ts === 0) { toast(t('toast_shares_sum')); return; }
    const ps = amount / ts;
    members.forEach(m => { const s = splitShares[m.id] || 0; if (s > 0) splits[m.id] = Math.round(s*ps*100)/100; });
  } else if (splitMode === 'exact') {
    let te = 0;
    members.forEach(m => { const v = parseFloat(splitExact[m.id]) || 0; te += v; if (v > 0) splits[m.id] = Math.round(v*100)/100; });
    if (Math.abs(te - amount) > 0.05) { toast(t('toast_exact_sum')); return; }
  }

  if (Object.keys(splits).length === 0) { toast(t('toast_select_participant')); return; }

  if (editingExpenseId) {
    const idx = state.expenses.findIndex(ex => ex.id === editingExpenseId);
    if (idx !== -1) {
      state.expenses[idx] = { ...state.expenses[idx], title, amount, paidBy: selectedPayer, category: selectedCategory, date, splitMode, splits };
    }
    toast(t('toast_updated'));
  } else {
    state.expenses.push({ id: uid(), title, amount, paidBy: selectedPayer, category: selectedCategory, date, splitMode, splits, createdAt: new Date().toISOString() });
    toast(t('toast_saved'));
  }

  save(); closeModal('modal-expense'); render();
}

// ---- Expense Detail ----
function showExpenseDetail(expId) {
  const exp = state.expenses.find(e => e.id === expId);
  if (!exp) return;
  const cat = getCategoryInfo(exp.category);
  const payer = getMember(exp.paidBy);

  let html = `
    <div class="detail-header">
      <div class="detail-icon">${cat.icon}</div>
      <div class="detail-amount">${fmt(exp.amount)}</div>
      <div class="detail-title">${escapeHTML(exp.title)}</div>
      <div class="detail-date">${fmtDate(exp.date)} · ${t('categories')[exp.category]}</div>
    </div>
    <div class="detail-section"><div class="detail-label">${t('paid_by')}</div>
      <div style="display:flex;align-items:center;gap:var(--space-sm)">
        ${payer ? avatarHTML(payer) : ''}<span style="font-weight:500">${payer ? escapeHTML(payer.name) : 'Desconocido'}</span>
      </div></div>
    <div class="detail-section"><div class="detail-label">${t('divided_among', {count: Object.keys(exp.splits).length})}</div>`;
  Object.entries(exp.splits).forEach(([mid, amount]) => {
    const m = getMember(mid);
    if (!m) return;
    html += `<div class="detail-split-row">${avatarHTML(m, 'sm')}<div class="name">${escapeHTML(m.name)}</div><div class="amount">${fmt(amount)}</div></div>`;
  });
  html += `</div>
    <div class="detail-actions">
      <button class="btn-secondary" onclick="editExpense('${exp.id}')">✏️ ${t('edit')}</button>
      <button class="btn-danger" onclick="confirmDeleteExpense('${exp.id}')">🗑️ ${t('delete')}</button>
    </div>`;

  document.getElementById('detail-content').innerHTML = html;
  openModal('modal-detail');
}

function editExpense(id) {
  closeModal('modal-detail');
  const exp = state.expenses.find(e => e.id === id);
  if (exp) setTimeout(() => openExpenseModal(exp), 200);
}

function confirmDeleteExpense(id) {
  closeModal('modal-detail');
  showConfirm(t('toast_confirm_delete_expense'), () => {
    state.expenses = state.expenses.filter(e => e.id !== id);
    save(); render(); toast(t('toast_deleted'));
  });
}

// ---- Settle Debt ----
function settleDebt(fromId, toId, amount) {
  const from = getMember(fromId), to = getMember(toId);
  if (!from || !to) return;
  showConfirm(t('toast_confirm_settle', {from: from.name, amount: fmt(amount), to: to.name}), () => {
    state.payments.push({ id: uid(), from: fromId, to: toId, amount, date: new Date().toISOString() });
    save(); render(); toast(t('toast_settled'));
  }, t('settle'));
}

// ---- Group Modal ----
function openGroupModal() { renderGroupModal(); openModal('modal-group'); }

function renderGroupModal() {
  document.getElementById('group-name-input').value = state.group.name;
  document.getElementById('members-list').innerHTML = state.group.members.map(m => {
    const isYou = m.id === state.group.currentUser;
    return `<div class="member-item">${avatarHTML(m)}<div class="name">${escapeHTML(m.name)}</div>
      ${isYou ? `<span class="you-badge">${t('active_you')}</span>` : ''}
      <button class="btn-remove" onclick="removeMember('${m.id}')" title="${t('delete')}">×</button></div>`;
  }).join('');
  document.getElementById('current-user-selector').innerHTML = state.group.members.map(m => `
    <div class="chip ${state.group.currentUser === m.id ? 'active' : ''}" onclick="setCurrentUser('${m.id}')">
      ${avatarHTML(m)}<span>${escapeHTML(m.name)}</span></div>`).join('');
}

function addMember() {
  const input = document.getElementById('new-member-input');
  const name = input.value.trim();
  if (!name) return;
  if (state.group.members.some(m => m.name.toLowerCase() === name.toLowerCase())) { toast(t('toast_exists')); return; }
  const nm = { id: uid(), name };
  state.group.members.push(nm);
  if (state.group.members.length === 1 && !state.group.currentUser) state.group.currentUser = nm.id;
  input.value = '';
  save(); renderGroupModal(); render();
}

function removeMember(id) {
  if (state.expenses.some(e => e.paidBy === id || (e.splits && id in e.splits))) { toast(t('toast_cannot_remove')); return; }
  state.group.members = state.group.members.filter(m => m.id !== id);
  if (state.group.currentUser === id) state.group.currentUser = null;
  save(); renderGroupModal(); render(); toast(t('toast_removed_member'));
}

function setCurrentUser(id) { state.group.currentUser = id; save(); renderGroupModal(); render(); }

function updateGroupName() {
  const name = document.getElementById('group-name-input').value.trim();
  if (name) { state.group.name = name; save(); renderHeader(); }
}

// ---- Groups List Modal ----
function openGroupsListModal() { renderGroupsList(); openModal('modal-groups-list'); }

function renderGroupsList() {
  const container = document.getElementById('groups-list-container');
  const groupIds = Object.keys(db.groups);
  
  if (groupIds.length === 0) {
    container.innerHTML = `<div class="empty-state"><div class="empty-text">No hay grupos creados.</div></div>`;
    return;
  }

  container.innerHTML = groupIds.map(id => {
    const data = db.groups[id];
    const isActive = id === db.activeGroupId;
    const expenseCount = data.expenses ? data.expenses.length : 0;
    const memberCount = data.group?.members ? data.group.members.length : 0;

    return `
      <div class="group-list-item ${isActive ? 'active' : ''}" onclick="switchActiveGroup('${id}')">
        <div class="group-info">
          <div class="group-name">${escapeHTML(data.group?.name || 'Grupo')}</div>
          <div class="group-meta">${memberCount} ${t('members').toLowerCase()} · ${expenseCount} ${t('nav_gastos').toLowerCase()}</div>
        </div>
        <button class="btn-delete-group" onclick="event.stopPropagation(); deleteGroup('${id}')" title="${t('delete')}">×</button>
      </div>`;
  }).join('');
}

function switchActiveGroup(id) {
  if (db.groups[id]) {
    db.activeGroupId = id;
    state.group = db.groups[id].group;
    state.expenses = db.groups[id].expenses || [];
    state.payments = db.groups[id].payments || [];
    save();
    closeModal('modal-groups-list');
    render();
  }
}

function createNewGroup() {
  const input = document.getElementById('new-group-name-input');
  const name = input.value.trim();
  if (!name) return;
  
  // Close group list modal and show onboarding steps configured for this new group
  closeModal('modal-groups-list');
  input.value = '';
  
  // Set up onboarding fields for a fresh group
  document.getElementById('onboard-group-name').value = name;
  document.getElementById('onboard-your-name').value = '';
  onboardMembers = [];
  showOnboarding();
  onboardStep = 1; // skip group name step since we just typed it
  renderOnboardStep();
}

function deleteGroup(id) {
  const groupName = db.groups[id]?.group?.name || 'Grupo';
  showConfirm(t('toast_confirm_delete_group', {name: groupName}), () => {
    delete db.groups[id];
    
    const remainingIds = Object.keys(db.groups);
    if (remainingIds.length > 0) {
      if (db.activeGroupId === id) {
        db.activeGroupId = remainingIds[0];
        state.group = db.groups[db.activeGroupId].group;
        state.expenses = db.groups[db.activeGroupId].expenses || [];
        state.payments = db.groups[db.activeGroupId].payments || [];
      }
      save();
      renderGroupsList();
      render();
    } else {
      // No groups left
      db.activeGroupId = '';
      state.group = { name: 'isi-isi', currency: '€', members: [], currentUser: null };
      state.expenses = [];
      state.payments = [];
      save();
      closeModal('modal-groups-list');
      showOnboarding();
    }
  });
}

// ---- Share ----
function shareGroup() {
  const transfers = simplifyDebts();
  const total = totalSpent();

  // Create a shareable URL containing the entire state serialized and encoded
  let shareUrl = window.location.href.split('?')[0];
  try {
    const dataStr = JSON.stringify({
      group: state.group,
      expenses: state.expenses,
      payments: state.payments
    });
    const encoded = btoa(unescape(encodeURIComponent(dataStr)));
    shareUrl += `?data=${encoded}`;
  } catch (e) {
    console.error('Error generating share URL:', e);
  }

  let text = `💸 *${state.group.name}*\n`;
  text += `${t('total_group_spend')}: ${fmt(total)}\n`;
  text += `${state.group.members.length} ${t('members').toLowerCase()} · ${state.expenses.length} ${t('nav_gastos').toLowerCase()}\n\n`;

  if (transfers.length > 0) {
    text += `📋 *${t('deudas_simplificadas')}:*\n`;
    transfers.forEach(tCode => {
      const from = getMember(tCode.from), to = getMember(tCode.to);
      if (from && to) text += `• ${from.name} → ${to.name}: ${fmt(tCode.amount)}\n`;
    });
  } else {
    text += `✅ ${t('state_settled_subtitle')}\n`;
  }

  text += `\n🔗 *${t('share_interactive_link')}*\n${shareUrl}\n\n`;
  text += `_${t('sent_from_app')}_`;

  if (navigator.share) {
    navigator.share({
      title: state.group.name + ' — Gastos',
      text: text
    }).catch(() => {
      const url = `https://wa.me/?text=${encodeURIComponent(text)}`;
      window.open(url, '_blank');
    });
  } else {
    const url = `https://wa.me/?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank');
  }
}

// ---- Confirm Dialog ----
function showConfirm(text, callback, okLabel) {
  document.getElementById('confirm-text').textContent = text;
  const okBtn = document.getElementById('confirm-ok');
  okBtn.textContent = okLabel || t('delete');
  okBtn.className = (okLabel && okLabel !== t('delete') && okLabel !== 'Eliminar') ? 'btn-primary' : 'btn-danger';
  confirmCallback = callback;
  document.getElementById('confirm-dialog').classList.add('open');
}
function closeConfirm() { document.getElementById('confirm-dialog').classList.remove('open'); confirmCallback = null; }

// ---- Toast ----
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2500);
}

// ---- Reset ----
function resetData() {
  showConfirm(t('toast_confirm_reset'), () => {
    localStorage.removeItem(STORAGE_KEY);
    db = { activeGroupId: '', groups: {} };
    state.group = { name: 'isi-isi', currency: '€', members: [], currentUser: null };
    state.expenses = [];
    state.payments = [];
    save();
    render();
    showOnboarding();
    toast(t('reset'));
  });
}

// ============================================
//   ONBOARDING
// ============================================

function showOnboarding() {
  onboardStep = 0;
  onboardMembers = [];
  document.getElementById('onboarding').classList.remove('hidden');
  document.getElementById('app-header').style.display = 'none';
  document.getElementById('app-main').style.display = 'none';
  document.getElementById('fab').style.display = 'none';
  document.getElementById('navbar').style.display = 'none';
  renderOnboardStep();
  setTimeout(() => document.getElementById('onboard-group-name').focus(), 300);
}

function hideOnboarding() {
  document.getElementById('onboarding').classList.add('hidden');
  document.getElementById('app-header').style.display = '';
  document.getElementById('app-main').style.display = '';
  document.getElementById('fab').style.display = '';
  document.getElementById('navbar').style.display = '';
}

function renderOnboardStep() {
  for (let i = 0; i < 3; i++) {
    const step = document.getElementById('onboard-step-' + i);
    const dot = document.getElementById('dot-' + i);
    if (step) step.classList.toggle('active', i === onboardStep);
    if (dot) {
      dot.classList.toggle('active', i === onboardStep);
      dot.classList.toggle('done', i < onboardStep);
    }
  }

  if (onboardStep === 2) {
    renderOnboardMembers();
  }
}

function renderOnboardMembers() {
  const list = document.getElementById('onboard-members-list');
  list.innerHTML = onboardMembers.map((name, i) => `
    <div class="onboard-member-chip">
      <div class="avatar" style="background:${hashColor(name)};width:24px;height:24px;font-size:0.6rem;border-radius:9999px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:600">${getInitials(name)}</div>
      <span>${escapeHTML(name)}</span>
      <div class="remove-chip" onclick="removeOnboardMember(${i})">×</div>
    </div>`).join('');

  const count = onboardMembers.length;
  document.getElementById('onboard-counter').innerHTML = count > 0
    ? `<strong>${count}</strong> ${t('onboard_counter_filled')}`
    : t('onboard_counter_empty');

  document.getElementById('onboard-finish').disabled = count < 1;
}

function addOnboardMember() {
  const input = document.getElementById('onboard-member-input');
  const name = input.value.trim();
  if (!name) return;
  if (onboardMembers.some(n => n.toLowerCase() === name.toLowerCase())) { toast(t('toast_exists')); return; }
  const yourName = document.getElementById('onboard-your-name').value.trim();
  if (yourName && name.toLowerCase() === yourName.toLowerCase()) { toast(t('toast_exists')); return; }
  onboardMembers.push(name);
  input.value = '';
  renderOnboardMembers();
  input.focus();
}

function removeOnboardMember(index) {
  onboardMembers.splice(index, 1);
  renderOnboardMembers();
}

function finishOnboarding() {
  const groupName = document.getElementById('onboard-group-name').value.trim() || 'Group';
  const yourName = document.getElementById('onboard-your-name').value.trim();

  if (!yourName) { toast(t('onboard_step1_placeholder')); onboardStep = 1; renderOnboardStep(); return; }

  const youMember = { id: uid(), name: yourName };
  const otherMembers = onboardMembers.map(name => ({ id: uid(), name }));

  const newGroupId = uid();
  db.groups[newGroupId] = {
    group: {
      name: groupName,
      currency: '€',
      members: [youMember, ...otherMembers],
      currentUser: youMember.id,
    },
    expenses: [],
    payments: []
  };
  db.activeGroupId = newGroupId;
  
  state.group = db.groups[newGroupId].group;
  state.expenses = [];
  state.payments = [];

  save();
  hideOnboarding();
  render();
  toast(t('toast_group_created', {name: groupName}));
}

function initOnboardingEvents() {
  document.getElementById('onboard-next-0').addEventListener('click', () => {
    const name = document.getElementById('onboard-group-name').value.trim();
    if (!name) { toast(t('onboard_step0_placeholder')); return; }
    onboardStep = 1;
    renderOnboardStep();
    setTimeout(() => document.getElementById('onboard-your-name').focus(), 100);
  });

  document.getElementById('onboard-next-1').addEventListener('click', () => {
    const name = document.getElementById('onboard-your-name').value.trim();
    if (!name) { toast(t('onboard_step1_placeholder')); return; }
    onboardStep = 2;
    renderOnboardStep();
    setTimeout(() => document.getElementById('onboard-member-input').focus(), 100);
  });

  document.getElementById('onboard-back-1').addEventListener('click', () => { onboardStep = 0; renderOnboardStep(); });
  document.getElementById('onboard-back-2').addEventListener('click', () => { onboardStep = 1; renderOnboardStep(); });

  document.getElementById('onboard-add-member').addEventListener('click', addOnboardMember);
  document.getElementById('onboard-member-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); addOnboardMember(); }
  });

  document.getElementById('onboard-finish').addEventListener('click', finishOnboarding);

  document.getElementById('onboard-group-name').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); document.getElementById('onboard-next-0').click(); }
  });
  document.getElementById('onboard-your-name').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); document.getElementById('onboard-next-1').click(); }
  });
}

// ============================================
//   EVENT LISTENERS
// ============================================

function initEvents() {
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => nav(btn.dataset.view));
  });

  document.getElementById('fab').addEventListener('click', () => {
    if (state.group.members.length < 2) { toast(t('empty_no_members')); openGroupModal(); return; }
    openExpenseModal(null);
  });

  document.getElementById('btn-group').addEventListener('click', openGroupModal);
  document.getElementById('btn-groups-list').addEventListener('click', openGroupsListModal);
  document.getElementById('header-title').addEventListener('click', openGroupsListModal);
  document.getElementById('btn-create-new-group').addEventListener('click', createNewGroup);
  document.getElementById('new-group-name-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); createNewGroup(); }
  });
  
  document.getElementById('btn-reset').addEventListener('click', resetData);
  document.getElementById('btn-share').addEventListener('click', shareGroup);

  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      closeModal(btn.dataset.close);
      if (btn.dataset.close === 'modal-group') updateGroupName();
    });
  });
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) { closeModal(overlay.id); if (overlay.id === 'modal-group') updateGroupName(); }
    });
  });

  document.getElementById('expense-form').addEventListener('submit', handleSaveExpense);
  document.querySelectorAll('.split-tab').forEach(tab => {
    tab.addEventListener('click', () => setSplitMode(tab.dataset.mode));
  });
  document.getElementById('expense-amount-input').addEventListener('input', renderSplitConfig);

  document.getElementById('btn-add-member').addEventListener('click', addMember);
  document.getElementById('new-member-input').addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); addMember(); } });
  document.getElementById('group-name-input').addEventListener('change', updateGroupName);

  document.getElementById('confirm-ok').addEventListener('click', () => { if (confirmCallback) confirmCallback(); closeConfirm(); });
  document.getElementById('confirm-cancel').addEventListener('click', closeConfirm);
  document.getElementById('confirm-dialog').addEventListener('click', (e) => { if (e.target.id === 'confirm-dialog') closeConfirm(); });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (document.getElementById('confirm-dialog').classList.contains('open')) closeConfirm();
      else document.querySelectorAll('.modal-overlay.open').forEach(m => { closeModal(m.id); if (m.id === 'modal-group') updateGroupName(); });
    }
  });
}

// ============================================
//   INITIALIZATION
// ============================================

function init() {
  localizeDOM();

  // Check for shared URL data first
  let loaded = false;
  const urlParams = new URLSearchParams(window.location.search);
  const sharedData = urlParams.get('data');

  if (sharedData) {
    try {
      const decodedData = decodeURIComponent(escape(atob(sharedData)));
      const parsed = JSON.parse(decodedData);
      if (parsed && parsed.group) {
        const importId = uid();
        db.groups[importId] = {
          group: parsed.group,
          expenses: parsed.expenses || [],
          payments: parsed.payments || []
        };
        db.activeGroupId = importId;
        
        state.group = parsed.group;
        state.expenses = parsed.expenses || [];
        state.payments = parsed.payments || [];
        
        save();
        loaded = true;
        toast(t('toast_import_ok'));
        
        const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
        window.history.replaceState({ path: cleanUrl }, '', cleanUrl);
      }
    } catch (e) {
      console.error('Error importing shared group:', e);
      toast(t('toast_import_err'));
    }
  }

  if (!loaded) {
    loaded = load();
  }

  initEvents();
  initOnboardingEvents();

  if (!loaded) {
    showOnboarding();
  } else {
    hideOnboarding();
    render();
  }
}

document.addEventListener('DOMContentLoaded', init);

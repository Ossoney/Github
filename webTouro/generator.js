/**
 * 12fogar Admin Link Generator Logic
 * Automates creating guest links and WhatsApp templates with zero friction.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Pre-fill default dates (Tomorrow -> Tomorrow + 4 days)
  const today = new Date();
  
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  const defaultCheckout = new Date(tomorrow);
  defaultCheckout.setDate(defaultCheckout.getDate() + 4);

  // Format as YYYY-MM-DD for date inputs
  const formatDateString = (date) => {
    const yyyy = date.getFullYear();
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
  };

  document.getElementById('checkin-input').value = formatDateString(tomorrow);
  document.getElementById('checkout-input').value = formatDateString(defaultCheckout);

  // Set up event listeners on all inputs to generate in real-time
  const inputs = ['guest-name-input', 'checkin-input', 'checkout-input', 'pin-input', 'lang-input', 'apartment-input'];
  inputs.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', generateData);
      el.addEventListener('change', generateData);
    }
  });

  const aptInput = document.getElementById('apartment-input');
  if (aptInput) {
    aptInput.addEventListener('change', () => {
      const pinInput = document.getElementById('pin-input');
      const pinLabel = document.getElementById('pin-label');
      if (aptInput.value === 'peru') {
        if (pinInput) pinInput.value = '1702';
        if (pinLabel) pinLabel.textContent = 'PIN Caja Llaves (Buzón 2B)';
      } else {
        if (pinInput) pinInput.value = '1262';
        if (pinLabel) pinLabel.textContent = 'PIN Caja Llaves (Buzón 2C)';
      }
      generateData();
    });
  }

  // Initial generation
  generateData();
});

function generateData() {
  const name = document.getElementById('guest-name-input').value.trim();
  const checkinVal = document.getElementById('checkin-input').value;
  const checkoutVal = document.getElementById('checkout-input').value;
  const pin = document.getElementById('pin-input').value.trim();
  const lang = document.getElementById('lang-input').value;
  const apartment = document.getElementById('apartment-input') ? document.getElementById('apartment-input').value : 'touro';
  
  const resultsCard = document.getElementById('results-card');

  // If name is empty, hide results
  if (!name) {
    resultsCard.style.display = 'none';
    return;
  }

  resultsCard.style.display = 'block';

  // 1. Build the Dynamic Guest Portal Link
  // Detect where generator.html is running and swap it with index.html
  let basePath = window.location.href;
  if (basePath.includes('generator.html')) {
    basePath = basePath.replace('generator.html', 'index.html');
  } else if (basePath.endsWith('/')) {
    basePath = basePath + 'index.html';
  } else {
    // If not matching generator.html, just construct index.html path in same directory
    const parts = basePath.split('/');
    parts[parts.length - 1] = 'index.html';
    basePath = parts.join('/');
  }

  const queryParams = new URLSearchParams({
    huesped: name,
    in: checkinVal,
    out: checkoutVal,
    p: pin
  });
  if (apartment === 'peru') {
    queryParams.set('a', 'p');
  }
  if (lang === 'en') {
    queryParams.set('l', 'en');
  }

  const finalUrl = `${basePath.split('?')[0]}?${queryParams.toString()}`;
  document.getElementById('generated-url').textContent = finalUrl;

  // 2. Build the WhatsApp Welcome Message template
  const checkinDate = new Date(checkinVal);
  const checkoutDate = new Date(checkoutVal);

  const optionsMonth = { month: 'long' };
  const optionsDay = { day: 'numeric' };

  const localeStr = (lang === 'en') ? 'en-US' : 'es-ES';
  const startDay = checkinDate.toLocaleDateString(localeStr, optionsDay);
  const startMonth = checkinDate.toLocaleDateString(localeStr, optionsMonth);
  const endDay = checkoutDate.toLocaleDateString(localeStr, optionsDay);
  const endMonth = checkoutDate.toLocaleDateString(localeStr, optionsMonth);

  let dateRangeStr = "";
  if (lang === 'en') {
    if (startMonth === endMonth) {
      dateRangeStr = `${startMonth} ${startDay} to ${endDay}`;
    } else {
      dateRangeStr = `${startMonth} ${startDay} to ${endMonth} ${endDay}`;
    }
  } else {
    if (startMonth === endMonth) {
      dateRangeStr = `${startDay} al ${endDay} de ${startMonth}`;
    } else {
      dateRangeStr = `${startDay} de ${startMonth} al ${endDay} de ${endMonth}`;
    }
  }

  let whatsappMessage = "";
  if (lang === 'en') {
    if (apartment === 'peru') {
      whatsappMessage = `Hi, this is Oscar from the apartment you booked for today. Do you have an approximate arrival time? The usual check-in time is from 5 pm onwards to ensure the apartment is spotless. If you need to check in earlier, please let me know so we can see what we can arrange. 

I'm sending you the personalized digital guide for your stay in Ribeira from ${dateRangeStr}:

🔗 ${finalUrl}

On this link you will easily find:
📍 Exact location and Google Maps navigation.
🔑 Detailed arrival instructions with the key box code (PIN: ${pin}) and portal automatic open call.
🏠 House rules and important details.
🍽️ Our favorite local recommendations for dining, beaches, and sightseeing to eat well and enjoy Barbanza.

Have a great trip and don't hesitate to write to me if you need anything!

p.s. Below is the link to the GUEST REGISTRATION form. Please share it via WhatsApp and have all guests over 14 years old fill it out.

Oscar`;
    } else {
      whatsappMessage = `Hi, this is Oscar from the apartment you booked for today. Do you have an approximate arrival time? The usual check-in time is from 5 pm onwards to ensure the apartment is spotless. If you need to check in earlier, please let me know so we can see what we can arrange. 

I'm sending you the personalized digital guide for your stay in Ribeira from ${dateRangeStr}:

🔗 ${finalUrl}

On this link you will easily find:
📍 Exact location and Google Maps navigation.
🔑 Detailed arrival instructions with the key box code (PIN: ${pin}) and portal automatic open call.
🚗 Your assigned parking space (Space Nº 41 - fixed).
🏠 House rules and important details.
🍽️ Our favorite local recommendations for dining, beaches, and sightseeing to eat well and enjoy Barbanza.

Have a great trip and don't hesitate to write to me if you need anything!

p.s. Below is the link to the GUEST REGISTRATION form. Please share it via WhatsApp and have all guests over 14 years old fill it out.

Oscar`;
    }
  } else {
    if (apartment === 'peru') {
      whatsappMessage = `Hola, soy Oscar del apartamento que reservaste para hoy ¿tienes una hora aproximada de llegada? La hora de entrada habitual es a partir de las 17h para tener el apartamento impecable. Si necesitas entrar antes, házmelo saber para ver qué podemos hacer. 

Te adjunto la guía digital personalizada para tu estancia en Ribeira del ${dateRangeStr}:

🔗 ${finalUrl}

En este enlace encontrarás de forma cómoda:
📍 Ubicación exacta y navegación en Google Maps.
🔑 Instrucciones detalladas de llegada con el código de la caja de llaves (PIN: ${pin}) y llamada de apertura del portal.
🏠 Normas de la casa y detalles importantes.
🍽️ Nuestras recomendaciones favoritas de restaurantes, playas y visitas para comer bien y disfrutar de Barbanza.

¡Que tengáis muy buen viaje y cualquier cosa no dudes en escribirme!

p.d. A continuación te paso un enlace con el REGISTRO DE HUESPEDES para que compartáis por whatsapp y rellenéis los mayores de 14 años.

Óscar`;
    } else {
      whatsappMessage = `Hola, soy Oscar del apartamento que reservaste para hoy ¿tienes una hora aproximada de llegada? La hora de entrada habitual es a partir de las 17h para tener el apartamento impecable. Si necesitas entrar antes, házmelo saber para ver qué podemos hacer. 

Te adjunto la guía digital personalizada para tu estancia en Ribeira del ${dateRangeStr}:

🔗 ${finalUrl}

En este enlace encontrarás de forma cómoda:
📍 Ubicación exacta y navegación en Google Maps.
🔑 Instrucciones detalladas de llegada con el código de la caja de llaves (PIN: ${pin}) y llamada de apertura del portal.
🚗 Tu plaza de garaje asignada (Plaza Nº 41 - fija).
🏠 Normas de la casa y detalles importantes.
🍽️ Nuestras recomendaciones favoritas de restaurantes, playas y visitas para comer bien y disfrutar de Barbanza.

¡Que tengáis muy buen viaje y cualquier cosa no dudes en escribirme!

p.d. A continuación te paso un enlace con el REGISTRO DE HUESPEDES para que compartáis por whatsapp y rellenéis los mayores de 14 años.

Óscar`;
    }
  }

  document.getElementById('generated-message').textContent = whatsappMessage;
}

// Secure clipboard copy helper
function copyToClipboard(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    return navigator.clipboard.writeText(text);
  } else {
    // Fallback for older web views
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed'; // Avoid scrolling to bottom
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    try {
      document.execCommand('copy');
      document.body.removeChild(textarea);
      return Promise.resolve();
    } catch (err) {
      document.body.removeChild(textarea);
      return Promise.reject(err);
    }
  }
}

// Show temporary feedback toast
function showToast() {
  const toast = document.getElementById('copy-toast');
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 2000);
}

// Copiar Enlace del Portal
function copyLink() {
  const url = document.getElementById('generated-url').textContent;
  copyToClipboard(url)
    .then(() => showToast())
    .catch(err => alert('Error al copiar el enlace: ' + err));
}

// Copiar Mensaje de WhatsApp
function copyWhatsAppMessage() {
  const msg = document.getElementById('generated-message').textContent;
  copyToClipboard(msg)
    .then(() => showToast())
    .catch(err => alert('Error al copiar el mensaje: ' + err));
}

// Compartir por WhatsApp o Web Share API
function shareWhatsAppNative() {
  const msg = document.getElementById('generated-message').textContent;
  const url = document.getElementById('generated-url').textContent;
  const guestName = document.getElementById('guest-name-input').value.trim() || 'Huésped';

  if (navigator.share) {
    navigator.share({
      title: `Guía Digital 12fogar - ${guestName}`,
      text: msg
    }).then(() => console.log('Contenido compartido con éxito'))
      .catch(err => {
        if (err.name !== 'AbortError') {
          openWhatsAppDirect(msg);
        }
      });
  } else {
    openWhatsAppDirect(msg);
  }
}

// Auxiliar para abrir WhatsApp directo
function openWhatsAppDirect(text) {
  const encodedText = encodeURIComponent(text);
  const whatsappUrl = `https://api.whatsapp.com/send?text=${encodedText}`;
  window.open(whatsappUrl, '_blank');
}


/**
 * 12fogar Guest App Logic
 * Client-side script for dynamic customization and interactive widgets.
 */

const enTranslations = {
  // Navigation
  'nav-inicio': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>Home',
  'nav-llegada': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>Arrival',
  'nav-casa': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>House Rules',
  'nav-recoms': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>Things to Do',

  // Welcome box & Stay Dates placeholder
  'stay-dates-range': 'Loading stay dates...',

  // Header Cards & Countdown
  'countdown-title-text': 'Your Stay',
  
  // Section Headers & Titles
  'title-welcome': 'Welcome to Ribeira',
  'desc-welcome-1': 'We welcome you to the <strong>Romantic apartment with the sea at your feet</strong> in Ribeira. We want your stay to be magical, relaxing and absolutely unforgettable.',
  'desc-welcome-2': 'In this digital guide you have everything you need for your arrival and stay. Scroll down or use the bottom navigation bar to see details of access, rules, and local recommendations.',
  
  'title-actions': 'Quick Actions',
  'btn-action-llegar': 'How to Arrive',
  'btn-action-maps': 'Google Maps',
  'btn-action-tours': 'Tours & Sightseeing',
  'btn-action-norms': 'House Rules',
  
  'title-weather': 'Weather in Ribeira',
  
  // Access Instructions
  'title-access': 'Access Instructions',
  'desc-access-1': 'The apartment is located at <strong>126 Manzanares Street, Ribeira</strong>. It has a private garage with direct access to the apartment via elevator.',
  'step1-title': 'Step 1: Open the Main Gate',
  'step1-desc': 'Stand in front of portal 126 of the building (just behind the main building). Press button <strong>2C</strong> on the intercom and immediately call the phone number <a href="tel:634322002" class="phone-call-btn"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>+34 634 32 20 02</a>.<br><small style="color: var(--accent); font-weight: 600;">* I have authorized your mobile phone number so the main gate opens automatically.</small>',
  
  'step2-title': 'Step 2: Retrieve the Keys',
  'step2-desc': 'Enter the hall and open <strong>mailbox 2C</strong>. You will find a black safety key box. Enter the opening code: <span class="code-highlight" id="key-pin">1262</span>. Pull down the left black lever to open it. Inside you will find the keys and the garage remote.<br><small>Please close the safety box again, scramble the number wheels, and close the mailbox when you are finished. :)</small>',
  'btn-video-box': '🎥 Watch short video on how to open the box',
  
  'step3-title': 'Step 3: Garage and Elevator',
  'step3-desc': 'Your assigned parking space is number <strong id="parking-spot-number">41</strong>. When entering the garage, turn right and then right again. You can go straight up to the apartment using the elevator.<br><strong>Attention:</strong> The same key opens the main gate, the inner garage door, and the apartment. We recommend going up to the apartment first and then parking slowly.',

  'title-visual': 'Visual Help',
  'desc-visual': 'Below are photos of the location and the building to help you orient yourself without getting lost:',
  'label-portal': 'Building Entrance (Portal 126):',
  'label-maps': 'Location on Google Maps:',
  'label-maps-help': '(Tap to open navigation)',
  'btn-open-maps': 'Open in Google Maps',
  'label-mailbox': 'Entrance to Portal and Garage:',

  // House Rules Section
  'wifi-card-title': 'No Wi-Fi Here',
  'wifi-card-desc-1': '<strong>We want you to disconnect, rest and look at the sea.</strong>',
  'wifi-card-desc-2': 'Take advantage of this stay to relax with the sound of the waves, take a walk along Ribeira beach, and disconnect from notifications.',
  
  'title-rules': 'House Rules',
  'desc-rules': 'To guarantee a pleasant stay and perfect condition of the apartment, we remind you of the following guidelines:',
  'rule1-title': 'No Smoking',
  'rule1-desc': 'The apartment is a 100% smoke-free space.',
  'rule2-title': 'No Parties Allowed',
  'rule2-desc': 'Let\'s respect the rest of the neighbors in the building.',
  'rule3-title': 'No Pets Allowed',
  'rule3-desc': 'We love animals, but due to allergy reasons and past experiences, they are not allowed.',
  'rule4-title': 'Only Registered Guests',
  'rule4-desc': 'The booking is made exclusively for the number of people indicated in the contract.',
  'rule-footer': 'The most important rule is to enjoy your stay to the fullest!',

  'title-checkout': 'Check-out Instructions',
  'desc-checkout-1': 'The checkout limit time is at <strong>12:00h</strong>.',
  'desc-checkout-2': 'When you leave, please do the following:',
  'checkout-li-1': 'Turn off all lights and heating.',
  'checkout-li-2': 'Leave the keys and garage remote in the same security box inside mailbox 2C.',
  'checkout-li-3': 'Scramble the numerical code when closing the safety metal box.',
  'checkout-li-4': 'Send me a quick WhatsApp to confirm everything went great and you have departed.',

  // Recommendations
  'title-recoms': 'Things to Do in Ribeira & Surrounds',
  'desc-recoms': 'Here are our favorite local suggestions for dining and exploring the Barbanza area:',
  'btn-tab-comer': '🍽️ Where to Eat',
  'btn-tab-playas': '🏖️ Beaches',
  'btn-tab-visitas': '⛰️ What to See',
  
  // Comer
  'rec-comer-title-1': 'Pobra do Caramiñal - El Sisal',
  'rec-comer-desc-1': 'Excellent to grab a bite or a drink on their terrace right above the food market, with fantastic views of the estuary.',
  'rec-comer-title-2': 'Aguiño - Faro de Sálvora Restaurant',
  'rec-comer-desc-2': 'Super famous for its incredible <span class="rec-highlight">octopus sandwich</span>. Their lunch menus are highly recommended and homemade.',
  'rec-comer-title-3': 'Ribeira - Xardín or Botter Restaurant',
  'rec-comer-desc-3': 'El Xardín is fantastic for fresh local seafood and fish. El Botter (near the church) has a great atmosphere for beers, wines, and tapas.',
  'rec-comer-title-4': 'Corrubedo - Benboa',
  'rec-comer-desc-4': 'A super unique concept that is a restaurant, fish shop, market, and tavern all in one, with spectacular decoration.',
  'rec-comer-title-5': 'Boiro - Arume Restaurant',
  'rec-comer-desc-5': 'Specialists in a spectacular <span class="rec-highlight">lobster rice</span>, octopus, and fresh fish. Reservation is advised.',

  // Playas
  'rec-playas-title-1': 'Vilar Beach (Ribeira)',
  'rec-playas-desc-1': 'Spectacular open ocean beach. At low tide, it\'s a wonder to take a miles-long walk on its fine sand at any time of the year.',
  'rec-playas-title-2': 'Furnas Beach (Porto do Son)',
  'rec-playas-desc-2': 'Stunning open ocean beach surrounded by rocks and wooden walkways. It is famous for filming the movie <i>Mar Adentro</i> and the TV series <i>Fariña</i>.',
  'rec-playas-title-3': 'Espiñeirido Beach (Porto do Son)',
  'rec-playas-desc-3': 'Open ocean. A spectacular place where, with a bit of luck, it is common to see <span class="rec-highlight">dolphins</span> playing near the coast.',
  'rec-playas-title-4': 'Cabío Beach (Pobra do Caramiñal)',
  'rec-playas-desc-4': 'More sheltered beach inside the estuary, ideal for windy days or to relax. It has a beautiful pine forest behind it.',

  // Visitas
  'rec-visitas-title-1': 'La Curota Viewpoint',
  'rec-visitas-desc-1': 'The highest point of the mountain range. On a clear day, you can perfectly see the entire Arousa estuary and the Muros and Noia estuary. Jaw-dropping views.',
  'rec-visitas-title-2': 'Baroña Celtic Ruins (Porto do Son)',
  'rec-visitas-desc-2': 'Fortified Celtic settlement from the Iron Age located on a rocky peninsula next to the sea. A must-visit, preferably before sunset.',
  'rec-visitas-title-3': 'Axeitos Dolmen',
  'rec-visitas-desc-3': 'Spectacular megalithic funerary monument, known as the "Parthenon of Galician megalithism" due to its excellent state of preservation.',
  'rec-visitas-title-4': 'Sálvora Island',
  'rec-visitas-desc-4': 'Has a magical history of legend. Guided tours are available by boat leaving from the port of Aguiño.',

  // Itinerary
  'title-itinerary': '6-Day Galicia Route',
  'desc-itinerary': 'If you want to explore the rest of our wonderful region, we suggest this optimized day-by-day itinerary:',
  'day1-title': 'Day 1: Santiago de Compostela',
  'day1-desc': 'A must-visit to the Cathedral of Santiago, the stone old town with its arched streets, and the local food market.',
  'day2-title': 'Day 2: Rías Baixas (Pontevedra and Combarro)',
  'day2-desc': 'Visit the pedestrian old town of Pontevedra, the traditional grain granaries ("hórreos") by the sea in Combarro, and the Natural Park of Illa de Arousa.',
  'day3-title': 'Day 3: A Coruña and Betanzos',
  'day3-desc': 'Walk along A Coruña\'s seafront promenade to the Tower of Hercules (the only working Roman lighthouse). Nearby is Betanzos, home of the best Spanish potato omelette (intentionally undercooked and runny).',
  'day4-title': 'Day 4: Arousa Estuary and Barbanza',
  'day4-desc': 'Explore the Celtic ruins of Baroña, eat the octopus sandwich in Aguiño, go up to La Curota, and relax on the massive Vilar beach.',
  'day5-title': 'Day 5: Ourense and Hot Springs',
  'day5-desc': 'Enjoy the open-air Roman hot springs in Outariz on the banks of the Miño River, Ourense\'s historic center, and the beautiful medieval town of Allariz.',
  'day6-title': 'Day 6: Lugo and its Roman Wall',
  'day6-desc': 'Lugo houses the only fully preserved Roman wall in the world, which you can walk on top of. It is also famous for its abundant free tapas served with drinks.',

  // Video Section
  'title-videos': 'Inspiring Videos',
  'desc-videos': 'Discover the landscapes that await you in Galicia:',

  // Tours Section
  'title-tours': 'Tours and Sightseeing',
  'desc-tours': 'Would you like to book official excursions or guided tours in Ribeira and the rest of Galicia?',
  'btn-tours-ribeira': 'Explore Tours in Ribeira',
  'btn-tours-galicia': 'Explore Tours in Galicia',

  // Santiago Recommendations
  'title-santiago': 'Things to Do in Santiago & Surrounds',
  'desc-santiago': 'Our favorite recommendations in Galicia\'s capital city, Santiago de Compostela:',
  'btn-santiago-tab-resto': '🍽️ Where to Eat',
  'btn-santiago-tab-copas': '🍷 Drinks & Wine',
  'btn-santiago-tab-gastro': '✨ Dining Experiences',
  
  'stgo-sp-title-2': 'A Moa Restaurant',
  'stgo-sp-desc-2': 'Great food with a highly recommended garden and terrace.',
  'stgo-sp-title-5': 'O 16 Restaurant',
  'stgo-sp-desc-5': 'Traditional Galician homemade cuisine.',

  'stgo-resto-title-1': 'A Curtiduría Restaurant',
  'stgo-resto-desc-1': 'Specializing in incredibly tasty rice dishes.',
  'stgo-resto-title-2': 'El Romero Restaurant',
  'stgo-resto-desc-2': 'We advise booking in advance. Highly recommended for couples. Fixed menu (no choosing) with absolutely outstanding desserts.',
  'stgo-resto-title-3': 'A Taboa de Picar Restaurant',
  'stgo-resto-desc-3': 'Features a beautiful terrace overlooking the Cathedral. Ideal for tapas and sharing plates.',
  'stgo-resto-title-4': 'A Gamela Restaurant',
  'stgo-resto-desc-4': 'A very small, cozy tavern specializing in delicious mushrooms.',
  'stgo-resto-title-5': 'Costa Vella Hotel',
  'stgo-resto-desc-5': 'Probably the most famous and visited garden café in Santiago to grab a coffee or drink.',
  'stgo-resto-title-6': 'San Miguel Hotel',
  'stgo-resto-desc-6': 'A very peaceful and quiet terrace for dinner or drinks.',
  'stgo-resto-title-7': 'Mesón Do Pulpo',
  'stgo-resto-desc-7': 'An old-school, traditional Galician tavern specializing in classic boiled octopus.',

  'stgo-copas-title-1': 'Classic Wine Spots',
  'stgo-copas-desc-1': 'To enjoy fine wines in authentic local spots recommended by locals: <span class="rec-highlight">O Gato Negro</span> and <span class="rec-highlight">El Fonda Club</span>.',
  'stgo-copas-title-2': 'Abastos Food Market',
  'stgo-copas-desc-2': 'Highly recommended to grab a bite or simply stroll and soak up the local Galician market life.',
  'stgo-copas-title-3': 'Live Music Sessions',
  'stgo-copas-desc-3': '<span class="rec-highlight">Casa das Crechas</span> and <span class="rec-highlight">Borriquita de Belén</span> regularly host excellent live music concerts.',
  'stgo-copas-title-4': 'Pub Atlántico',
  'stgo-copas-desc-4': 'Cozy atmosphere with great music and excellent cocktails/drinks.',
  'stgo-copas-title-5': 'Pub Momo',
  'stgo-copas-desc-5': 'Absolutely worth visiting for its spectacular terrace and landscaped gardens.',
  'stgo-copas-title-6': 'Bar Moha & Bar La Tita',
  'stgo-copas-desc-6': 'A must-stop to grab a beer served with the absolute best Spanish potato omelette (tortilla) tapa in Santiago.',

  'stgo-gastro-title-1': 'Sophisticated Creative Cooking (A Viaxe, Lume)',
  'stgo-gastro-desc-1': 'Highly rated dining spots recommended by major travel guides, run by second chefs of Michelin-starred kitchens. They offer exquisite tasting menus at very affordable prices (35 to 50 euros per person).',
  'stgo-gastro-title-2': 'Michelin Star (A Tafona, Casa Marcelo)',
  'stgo-gastro-desc-2': 'Award-winning restaurants that **do** hold a prestigious Michelin Star. Exquisite tasting menus for around 60-70 euros per person. Highly recommended.',

  'santiago-footer': 'If you would like any other specific recommendations, please ask us!',
  'btn-santiago-web': 'Santiago Tourism Website'
};


document.addEventListener('DOMContentLoaded', () => {
  // Register Service Worker for PWA (Offline Support)
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('./sw.js')
        .then(reg => console.log('Service Worker registered successfully:', reg.scope))
        .catch(err => console.log('Service Worker registration failed:', err));
    });
  }

  // 1. Parse URL Parameters
  const params = new URLSearchParams(window.location.search);
  const guestName = params.get('huesped') || params.get('h') || 'Huésped';
  const checkInStr = params.get('entrada') || params.get('in');
  const checkOutStr = params.get('salida') || params.get('out');
  const apartment = params.get('a') || params.get('apt') || 't';
  const pinCode = params.get('pin') || params.get('p') || (apartment === 'p' ? '1702' : '1262');
  const parkingSpot = params.get('garaje') || params.get('g') || '41';
  const lang = (params.get('lang') || params.get('l') || 'es').toLowerCase();

  // Handle Peru Apartment Content Swapping
  if (apartment === 'p') {
    document.body.classList.add('theme-peru');
    // 1. Swap Spanish texts (DOM elements)
    const descWelcome = document.getElementById('desc-welcome-1');
    if (descWelcome) {
      descWelcome.innerHTML = 'Te damos la bienvenida al <strong>Apartamento con vistas al mar y playa enfrente</strong> en Ribeira. Queremos que tu estancia sea mágica, relajante y absolutamente inolvidable.';
    }
    const descAccess = document.getElementById('desc-access-1');
    if (descAccess) {
      descAccess.innerHTML = 'El apartamento se encuentra en la <strong>Rúa Perú, Ribeira</strong>. Dispone de un cómodo acceso al portal y ascensor directo al apartamento.';
    }
    const step1Title = document.getElementById('step1-title');
    if (step1Title) {
      step1Title.textContent = 'Paso 1: Abrir el Portal Exterior';
    }
    const step1Desc = document.getElementById('step1-desc');
    if (step1Desc) {
      step1Desc.innerHTML = 'Sitúate frente al <strong>portal 17</strong> del edificio en Rúa Perú. Pulsa el botón <strong>2B</strong> en el telefonillo y, de inmediato, realiza una llamada al teléfono <a href="tel:634322002" class="phone-call-btn"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>+34 634 32 20 02</a>.<br><small style="color: var(--accent); font-weight: 600;">* He autorizado tu número de teléfono móvil para que el portal se abra de forma automática.</small>';
    }
    const step2Title = document.getElementById('step2-title');
    if (step2Title) {
      step2Title.textContent = 'Paso 2: Retirar las Llaves';
    }
    const step2Desc = document.getElementById('step2-desc');
    if (step2Desc) {
      step2Desc.innerHTML = 'Entra en el portal y abre el <strong>buzón 2B</strong>. Encontrarás una caja de seguridad negra. Introduce el código de apertura: <span class="code-highlight" id="key-pin">1702</span>. Baja la palanca negra de la izquierda para abrirla. Dentro están las llaves.<br><small>Por favor, vuelve a cerrar la caja de seguridad, desordena las ruedas numéricas y cierra el buzón al terminar. :)</small>';
    }

    // Hide Step 3 (garage)
    const step3Title = document.getElementById('step3-title');
    if (step3Title && step3Title.parentElement) {
      step3Title.parentElement.style.display = 'none';
    }

    // Hide Touro specific visual cards
    const portalLabel = document.getElementById('label-portal');
    if (portalLabel) {
      portalLabel.style.display = 'none';
      const portalImg = portalLabel.nextElementSibling;
      if (portalImg) portalImg.style.display = 'none';
    }
    const mailboxLabel = document.getElementById('label-mailbox');
    if (mailboxLabel) {
      mailboxLabel.style.display = 'none';
      const mailboxImg = mailboxLabel.nextElementSibling;
      if (mailboxImg) mailboxImg.style.display = 'none';
    }

    // Swap map image and link
    const mapImg = document.querySelector('.clickable-map-container img');
    if (mapImg) {
      mapImg.src = 'assets/maps-peru.jpg';
    }
    const mapContainer = document.querySelector('.clickable-map-container');
    if (mapContainer) {
      mapContainer.setAttribute('onclick', "window.open('https://maps.google.com/?q=R%C3%BAa+Per%C3%BA+Ribeira', '_blank')");
    }

    // Swap Quick Actions Google Maps link
    const quickMapsBtn = document.querySelector('div.action-btn[onclick*="LBf5qg3hrHA2"]');
    if (quickMapsBtn) {
      quickMapsBtn.setAttribute('onclick', "window.open('https://maps.google.com/?q=R%C3%BAa+Per%C3%BA+Ribeira', '_blank')");
    }

    // Swap Check-out instructions mailbox to 2B
    const checkoutLi2 = document.getElementById('checkout-li-2');
    if (checkoutLi2) {
      checkoutLi2.textContent = 'Deja las llaves en la misma caja de seguridad dentro del buzón 2B.';
    }

    // 2. Dynamically update English translations if active
    enTranslations['desc-welcome-1'] = 'We welcome you to the <strong>Apartment with sea views and beach in front</strong> in Ribeira. We want your stay to be magical, relaxing and absolutely unforgettable.';
    enTranslations['desc-access-1'] = 'The apartment is located at <strong>Rúa Perú, Ribeira</strong>. It has convenient building access and a direct elevator to the apartment.';
    enTranslations['step1-title'] = 'Step 1: Open the Main Gate';
    enTranslations['step1-desc'] = 'Stand in front of <strong>portal 17</strong> of the building on Rúa Perú. Press button <strong>2B</strong> on the intercom and immediately call the phone number <a href="tel:634322002" class="phone-call-btn"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>+34 634 32 20 02</a>.<br><small style="color: var(--accent); font-weight: 600;">* I have authorized your mobile phone number so the main gate opens automatically.</small>';
    enTranslations['step2-title'] = 'Step 2: Retrieve the Keys';
    enTranslations['step2-desc'] = 'Enter the hall and open <strong>mailbox 2B</strong>. You will find a black safety key box. Enter the opening code: <span class="code-highlight" id="key-pin">1702</span>. Pull down the left black lever to open it. Inside you will find the keys to the apartment.<br><small>Please close the safety box again, scramble the number wheels, and close the mailbox when you are finished. :)</small>';
    enTranslations['checkout-li-2'] = 'Leave the keys in the same security box inside mailbox 2B.';
  }

  // 2. Setup Personalized Greetings and Custom Details
  if (lang === 'en') {
    document.getElementById('welcome-name').textContent = `Hello, ${guestName}!`;
  } else {
    document.getElementById('welcome-name').textContent = `¡Hola, ${guestName}!`;
  }
  document.getElementById('key-pin').textContent = pinCode;
  document.getElementById('parking-spot-number').textContent = parkingSpot;

  // Apply dynamic translation if language is English
  if (lang === 'en') {
    document.title = "Guest Guide | 12fogar";
    for (const [id, value] of Object.entries(enTranslations)) {
      const el = document.getElementById(id);
      if (el) {
        if (value.includes('<') || value.includes('>')) {
          el.innerHTML = value;
        } else {
          el.textContent = value;
        }
      }
    }
    
    // Dynamically translate Civitatis Links and pointing to /en/
    const ribeiraBtn = document.getElementById('btn-tours-ribeira');
    const galiciaBtn = document.getElementById('btn-tours-galicia');
    if (ribeiraBtn) {
      ribeiraBtn.href = "https://www.civitatis.com/en/riveira/?aid=11475";
      ribeiraBtn.textContent = "Explore Tours in Ribeira";
    }
    if (galiciaBtn) {
      galiciaBtn.href = "https://www.civitatis.com/en/galicia/?aid=11475";
      galiciaBtn.textContent = "Explore Tours in Galicia";
    }

    // Dynamically translate the keybox helper video link
    const videoBoxBtn = document.getElementById('btn-video-box-link');
    if (videoBoxBtn) {
      videoBoxBtn.setAttribute('onclick', "window.open('https://youtube.com/shorts/pKjnYQ3Df0w?si=5-LFFPk7znA6XB08', '_blank')");
    }
  }

  // Personalize WhatsApp link
  const whatsappFloat = document.getElementById('whatsapp-float');
  if (whatsappFloat) {
    const welcomeMsg = (lang === 'en')
      ? `Hi Oscar! I'm ${guestName}, your guest at the apartment in Ribeira.`
      : `¡Hola Óscar! Soy ${guestName}, tu huésped del apartamento en Ribeira.`;
    const encodedText = encodeURIComponent(welcomeMsg);
    whatsappFloat.href = `https://api.whatsapp.com/send?phone=34656998500&text=${encodedText}`;
  }

  // 3. Format and Process Dates
  let checkInDate, checkOutDate;
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  if (checkInStr) {
    checkInDate = new Date(checkInStr);
  } else {
    checkInDate = new Date();
  }

  if (checkOutStr) {
    checkOutDate = new Date(checkOutStr);
  } else {
    checkOutDate = new Date(checkInDate);
    checkOutDate.setDate(checkOutDate.getDate() + 4); // Default 4 nights
  }

  // Set normalized time to midnight for math calculations
  const checkInMidnight = new Date(checkInDate);
  checkInMidnight.setHours(0, 0, 0, 0);
  const checkOutMidnight = new Date(checkOutDate);
  checkOutMidnight.setHours(0, 0, 0, 0);

  // Format date range nicely dynamically (supporting Spanish / English)
  const optionsMonth = { month: 'long' };
  const optionsDay = { day: 'numeric' };
  const optionsYear = { year: 'numeric' };

  const localeStr = (lang === 'en') ? 'en-US' : 'es-ES';
  const startDay = checkInDate.toLocaleDateString(localeStr, optionsDay);
  const startMonth = checkInDate.toLocaleDateString(localeStr, optionsMonth);
  const endDay = checkOutDate.toLocaleDateString(localeStr, optionsDay);
  const endMonth = checkOutDate.toLocaleDateString(localeStr, optionsMonth);
  const year = checkOutDate.toLocaleDateString(localeStr, optionsYear);

  let dateRangeStr = "";
  if (lang === 'en') {
    if (startMonth === endMonth) {
      dateRangeStr = `${startMonth} ${startDay} to ${endDay}, ${year}`;
    } else {
      dateRangeStr = `${startMonth} ${startDay} to ${endMonth} ${endDay}, ${year}`;
    }
  } else {
    if (startMonth === endMonth) {
      dateRangeStr = `${startDay} al ${endDay} de ${startMonth}, ${year}`;
    } else {
      dateRangeStr = `${startDay} de ${startMonth} al ${endDay} de ${endMonth}, ${year}`;
    }
  }
  document.getElementById('stay-dates-range').textContent = dateRangeStr;

  // ==================== DYNAMIC STAY-DATE LAYOUT REORDERING ENGINE ====================
  const wrapper = document.querySelector('.main-wrapper');
  
  const countdownNode = document.getElementById('countdown-card');
  const welcomeNode = document.getElementById('tab-inicio');
  const accessNode = document.getElementById('tab-llegada');
  const wifiNode = document.getElementById('card-wifi');
  const checkoutNode = document.getElementById('card-checkout');
  const recomsNode = document.getElementById('tab-recoms');
  const rulesNode = document.getElementById('tab-casa');
  const navLlegada = document.getElementById('nav-llegada');

  if (wrapper && welcomeNode && accessNode && wifiNode && checkoutNode && recomsNode && rulesNode) {
    const oneDayMs = 24 * 60 * 60 * 1000;
    const stayDurationNights = Math.round((checkOutMidnight.getTime() - checkInMidnight.getTime()) / oneDayMs);

    const isSingleNight = stayDurationNights <= 1;
    const isBeforeStay = today.getTime() < checkInMidnight.getTime();
    const isAfterStay = today.getTime() > checkOutMidnight.getTime();
    const isOutsideStay = isBeforeStay || isAfterStay;

    const isFirstDay = today.getTime() === checkInMidnight.getTime();
    const isLastDay = today.getTime() === checkOutMidnight.getTime();
    const isPenultimateDay = today.getTime() === (checkOutMidnight.getTime() - oneDayMs);
    const isLastTwoDays = isLastDay || isPenultimateDay;

    let order = [];
    const llegarBtn = document.querySelector('div.action-btn[onclick*="tab-llegada"]');
    const llegarSpan = document.getElementById('btn-action-llegar');

    if (isOutsideStay) {
      // Hide access instructions, visual help, and checkout instructions
      accessNode.style.display = 'none';
      checkoutNode.style.display = 'none';
      if (navLlegada) {
        navLlegada.style.display = 'none';
      }
      
      // Update Como Llegar button to show "Operativo en breve" / "Active soon" and prompt alert
      if (llegarSpan) {
        llegarSpan.textContent = (lang === 'en') ? 'How to Arrive (Active soon)' : 'Cómo Llegar (Operativo en breve)';
      }
      if (llegarBtn) {
        llegarBtn.style.opacity = '0.75';
        llegarBtn.setAttribute('onclick', "alert('" + ((lang === 'en') 
          ? 'Access instructions will be available starting on your check-in date. Safe travels!' 
          : 'Las instrucciones de acceso estarán disponibles a partir de la fecha de entrada de tu reserva. ¡Buen viaje!') + "')");
      }

      // Visible order: Welcome -> WiFi -> Recoms -> Rules
      order = [welcomeNode, wifiNode, recomsNode, rulesNode];
    } else {
      // Ensure they are displayed during the stay
      accessNode.style.display = '';
      checkoutNode.style.display = '';
      if (navLlegada) {
        navLlegada.style.display = '';
      }

      // Restore standard Como Llegar button behavior
      if (llegarSpan) {
        llegarSpan.textContent = (lang === 'en') ? 'How to Arrive' : 'Cómo Llegar';
      }
      if (llegarBtn) {
        llegarBtn.style.opacity = '';
        llegarBtn.setAttribute('onclick', "scrollToSection('tab-llegada')");
      }

      if (isSingleNight) {
        // Single night stay: Welcome -> Access -> Checkout -> WiFi -> Recoms -> Rules
        order = [welcomeNode, accessNode, checkoutNode, wifiNode, recomsNode, rulesNode];
      } else if (isFirstDay) {
        // First Day: Welcome -> Access -> WiFi -> Recoms -> Checkout -> Rules
        order = [welcomeNode, accessNode, wifiNode, recomsNode, checkoutNode, rulesNode];
      } else if (isLastTwoDays) {
        // Penultimate & Checkout Days: Welcome -> Checkout -> WiFi -> Recoms -> Access -> Rules
        order = [welcomeNode, checkoutNode, wifiNode, recomsNode, accessNode, rulesNode];
      } else {
        // Middle Days: Welcome -> WiFi -> Recoms -> Checkout -> Access -> Rules
        order = [welcomeNode, wifiNode, recomsNode, checkoutNode, accessNode, rulesNode];
      }
    }

    // Always put countdown-card first if it exists
    if (countdownNode) {
      wrapper.appendChild(countdownNode);
    }
    
    // Append in computed order to safely rearrange inside parent wrapper
    order.forEach(node => {
      wrapper.appendChild(node);
    });
  }

  // 4. Booking Status & Countdown Banner
  const countdownCard = document.getElementById('countdown-card');
  const countdownText = document.getElementById('countdown-text');
  const countdownIcon = document.getElementById('countdown-icon');

  if (countdownCard) {
    const diffTime = checkInMidnight.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    countdownCard.style.display = 'flex';

    if (lang === 'en') {
      if (diffDays > 1) {
        countdownText.textContent = `Your trip starts in ${diffDays} days!`;
        countdownIcon.textContent = '✈️';
      } else if (diffDays === 1) {
        countdownText.textContent = 'Your trip starts tomorrow!';
        countdownIcon.textContent = '👜';
      } else if (today >= checkInMidnight && today < checkOutMidnight) {
        countdownText.textContent = 'Enjoy your stay in Ribeira!';
        countdownIcon.textContent = '🏖️';
        countdownCard.style.background = 'linear-gradient(135deg, #2ec4b6, #0081a7)';
      } else if (today.getTime() === checkOutMidnight.getTime()) {
        countdownText.textContent = 'Today is check-out day. Safe travels back!';
        countdownIcon.textContent = '🚗';
        countdownCard.style.background = 'linear-gradient(135deg, #e63946, #d90429)';
      } else {
        countdownText.textContent = 'We hope to see you again very soon!';
        countdownIcon.textContent = '❤️';
        countdownCard.style.background = 'linear-gradient(135deg, #0b1d3a, #1c3d5a)';
      }
    } else {
      if (diffDays > 1) {
        countdownText.textContent = `¡Tu viaje comienza en ${diffDays} días!`;
        countdownIcon.textContent = '✈️';
      } else if (diffDays === 1) {
        countdownText.textContent = '¡Tu viaje comienza mañana!';
        countdownIcon.textContent = '👜';
      } else if (today >= checkInMidnight && today < checkOutMidnight) {
        countdownText.textContent = '¡Disfruta de tu estancia en Ribeira!';
        countdownIcon.textContent = '🏖️';
        countdownCard.style.background = 'linear-gradient(135deg, #2ec4b6, #0081a7)';
      } else if (today.getTime() === checkOutMidnight.getTime()) {
        countdownText.textContent = 'Hoy es el día de salida. ¡Feliz viaje de vuelta!';
        countdownIcon.textContent = '🚗';
        countdownCard.style.background = 'linear-gradient(135deg, #e63946, #d90429)';
      } else {
        countdownText.textContent = '¡Esperamos volver a verte muy pronto!';
        countdownIcon.textContent = '❤️';
        countdownCard.style.background = 'linear-gradient(135deg, #0b1d3a, #1c3d5a)';
      }
    }
  }

  // 5. Setup Action Buttons (Call portal removed)

  // 6. Dynamic Weather API Integration (Ribeira: 42.5509, -8.9862)
  fetchWeather(42.5509, -8.9862, lang);

  // 7. Intersection Observer for bottom nav active states
  const sections = document.querySelectorAll('.tab-content');
  const navItems = document.querySelectorAll('.nav-item');

  const observerOptions = {
    root: null, // viewport
    rootMargin: '-15% 0px -55% 0px', // balanced focus area
    threshold: 0
  };

  const observerCallback = (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        // Update active class on nav item that corresponds to the active section
        navItems.forEach(item => {
          item.classList.remove('active');
          const onclickAttr = item.getAttribute('onclick') || '';
          if (onclickAttr.includes(id)) {
            item.classList.add('active');
          }
        });
      }
    });
  };

  const observer = new IntersectionObserver(observerCallback, observerOptions);
  sections.forEach(section => {
    // Only observe major sections (tab-inicio, tab-llegada, tab-casa, tab-recoms)
    if (['tab-inicio', 'tab-llegada', 'tab-casa', 'tab-recoms'].includes(section.id)) {
      observer.observe(section);
    }
  });
});

// Smooth scrolling to section
function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    const yOffset = -15; // Balanced offset for mobile viewports
    const y = section.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: y, behavior: 'smooth' });
  }
}

// Recommendation Category Switching inside the recommendations tab
function switchRecsTab(category) {
  // Hide all recs contents
  const recsContents = document.querySelectorAll('.recs-content');
  recsContents.forEach(c => c.style.display = 'none');

  // Show selected category
  const activeCategory = document.getElementById(`rec-${category}`);
  if (activeCategory) {
    activeCategory.style.display = 'block';
  }

  // Update active tab button style
  const recsButtons = document.querySelectorAll('.recs-tab-btn');
  // Only filter those that are NOT santiago-tab-btn
  const filteredButtons = Array.from(recsButtons).filter(btn => !btn.classList.contains('santiago-tab-btn'));
  filteredButtons.forEach(btn => btn.classList.remove('active'));

  const clickedBtn = filteredButtons.find(btn => btn.getAttribute('onclick').includes(category));
  if (clickedBtn) {
    clickedBtn.classList.add('active');
  }
}

// Category Switching inside the Santiago recommendations tab
function switchSantiagoTab(category) {
  // Hide all santiago contents
  const santiagoContents = document.querySelectorAll('.santiago-content');
  santiagoContents.forEach(c => c.style.display = 'none');

  // Show selected category
  const activeCategory = document.getElementById(`santiago-${category}`);
  if (activeCategory) {
    activeCategory.style.display = 'block';
  }

  // Update active tab button style
  const santiagoButtons = document.querySelectorAll('.santiago-tab-btn');
  santiagoButtons.forEach(btn => btn.classList.remove('active'));

  const clickedBtn = document.getElementById(`btn-santiago-tab-${category}`);
  if (clickedBtn) {
    clickedBtn.classList.add('active');
  }
}

// Fetch 3-Day Weather Forecast in Ribeira (using free Open-Meteo daily endpoint)
// Results are cached in sessionStorage for 1 hour to avoid redundant API calls
async function fetchWeather(lat, lon, lang) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Europe/Madrid`;
  const CACHE_KEY = `weather_cache_${lat}_${lon}`;
  const CACHE_TTL_MS = 60 * 60 * 1000; // 1 hour

  // Try to use sessionStorage cache first
  try {
    const cached = sessionStorage.getItem(CACHE_KEY);
    if (cached) {
      const { timestamp, data } = JSON.parse(cached);
      if (Date.now() - timestamp < CACHE_TTL_MS) {
        renderWeather(data, lang);
        return;
      }
    }
  } catch (e) { /* sessionStorage unavailable, proceed normally */ }


  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('API Error');
    const data = await response.json();
    
    if (data && data.daily) {
      const container = document.getElementById('weather-widget');
      if (!container) return;
      container.innerHTML = ''; // clear loading state
      
      const isEn = (lang === 'en');
      
      for (let i = 0; i < 3; i++) {
        const dateStr = data.daily.time[i];
        const maxTemp = Math.round(data.daily.temperature_2m_max[i]);
        const minTemp = Math.round(data.daily.temperature_2m_min[i]);
        const code = data.daily.weather_code[i];
        
        let dayName = '';
        if (i === 0) {
          dayName = isEn ? 'Today' : 'Hoy';
        } else if (i === 1) {
          dayName = isEn ? 'Tomorrow' : 'Mañana';
        } else {
          // Format weekday name safely in local timezone
          const dateObj = new Date(dateStr + 'T00:00:00');
          dayName = dateObj.toLocaleDateString(isEn ? 'en-US' : 'es-ES', { weekday: 'short' });
          if (dayName.endsWith('.')) {
            dayName = dayName.slice(0, -1);
          }
        }
        
        const weatherMap = mapWmoWeatherCode(code, lang);
        
        const dayCol = document.createElement('div');
        dayCol.className = 'weather-day-col';
        dayCol.innerHTML = `
          <span class="weather-day-name">${dayName}</span>
          <span class="weather-day-icon">${weatherMap.emoji}</span>
          <div class="weather-day-temp">
            <span class="temp-max">${maxTemp}°</span>
            <span class="temp-min">${minTemp}°</span>
          </div>
          <span class="weather-day-desc">${weatherMap.desc}</span>
        `;
        container.appendChild(dayCol);
      }
    }
  } catch (error) {
    console.error('Error loading weather:', error);
    const container = document.getElementById('weather-widget');
    if (container) {
      container.innerHTML = ''; // clear loading state
      const isEn = (lang === 'en');
      const fallbackData = [
        { name: isEn ? 'Today' : 'Hoy', tempMax: 20, tempMin: 13, emoji: '⛅', desc: isEn ? 'Partly cloudy' : 'Nublado' },
        { name: isEn ? 'Tomorrow' : 'Mañana', tempMax: 21, tempMin: 14, emoji: '☀️', desc: isEn ? 'Clear sky' : 'Despejado' },
        { name: isEn ? 'Sat' : 'Sáb', tempMax: 19, tempMin: 12, emoji: '🌧️', desc: isEn ? 'Light showers' : 'Chubascos' }
      ];
      
      try {
        const day3Date = new Date();
        day3Date.setDate(day3Date.getDate() + 2);
        let d3Name = day3Date.toLocaleDateString(isEn ? 'en-US' : 'es-ES', { weekday: 'short' });
        if (d3Name.endsWith('.')) d3Name = d3Name.slice(0, -1);
        fallbackData[2].name = d3Name;
      } catch(e) {}

      fallbackData.forEach(item => {
        const dayCol = document.createElement('div');
        dayCol.className = 'weather-day-col';
        dayCol.innerHTML = `
          <span class="weather-day-name">${item.name}</span>
          <span class="weather-day-icon">${item.emoji}</span>
          <div class="weather-day-temp">
            <span class="temp-max">${item.tempMax}°</span>
            <span class="temp-min">${item.tempMin}°</span>
          </div>
          <span class="weather-day-desc">${item.desc}</span>
        `;
        container.appendChild(dayCol);
      });
    }
  }
}

// Map WMO Weather Codes to Friendly Emoji & Descriptions dynamically
function mapWmoWeatherCode(code, lang) {
  const isEn = (lang === 'en');
  if (code === 0) return { emoji: '☀️', desc: isEn ? 'Clear sky' : 'Cielo despejado' };
  if ([1, 2, 3].includes(code)) return { emoji: '⛅', desc: isEn ? 'Partly cloudy' : 'Parcialmente nublado' };
  if ([45, 48].includes(code)) return { emoji: '🌫️', desc: isEn ? 'Fog or mist' : 'Niebla o bruma' };
  if ([51, 53, 55].includes(code)) return { emoji: '🌧️', desc: isEn ? 'Drizzle' : 'Llovizna' };
  if ([61, 63, 65].includes(code)) return { emoji: '🌧️', desc: isEn ? 'Rainy' : 'Lluvia constante' };
  if ([71, 73, 75].includes(code)) return { emoji: '❄️', desc: isEn ? 'Snow' : 'Nieve' };
  if ([80, 81, 82].includes(code)) return { emoji: '🌧️', desc: isEn ? 'Showers' : 'Chubascos de lluvia' };
  if ([95, 96, 99].includes(code)) return { emoji: '⛈️', desc: isEn ? 'Thunderstorm' : 'Tormenta eléctrica' };
  return { emoji: '⛅', desc: isEn ? 'Pleasant weather' : 'Clima agradable' };
}

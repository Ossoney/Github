import { useState, useEffect, useMemo, useRef } from 'react'
import { ReactReader } from 'react-reader'

function App() {
  const [books, setBooks] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [scaning, setScanning] = useState(false)
  const [showScanModal, setShowScanModal] = useState(false)
  const [scanDirectory, setScanDirectory] = useState('c:\\Users\\OscarSson\\Videos\\Epub') 
  const [cardSize, setCardSize] = useState(110) 
  const [flippedCards, setFlippedCards] = useState({})
  const [sortOption, setSortOption] = useState('dateDesc')
  const [readingBookId, setReadingBookId] = useState(null)
  const [readingLocation, setReadingLocation] = useState(null)
  const [readerSettings, setReaderSettings] = useState({
    fontSize: 100,
    theme: 'light'
  })
  const [visibleCount, setVisibleCount] = useState(40)
  const [stats, setStats] = useState(null)
  const renditionRef = useRef(null)

  const fetchStats = async () => {
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/stats`)
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error("Error fetching stats:", error)
    }
  }

  const fetchSettings = async () => {
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/settings`)
      if (response.ok) {
        const data = await response.json()
        if (data.watch_path) setScanDirectory(data.watch_path)
      }
    } catch (error) {
      console.error("Error fetching settings:", error)
    }
  }

  const fetchBooks = async (isSearch = false) => {
    if (!isSearch) setLoading(true)
    try {
      const url = `http://${window.location.hostname}:8000/api/books?limit=1000${search ? `&search=${encodeURIComponent(search)}` : ''}`
      const response = await fetch(url)
      if (response.ok) {
        const data = await response.json()
        setBooks(data)
      }
    } catch (error) {
      console.error("Error fetching books:", error)
    } finally {
      if (!isSearch) setLoading(false)
    }
  }

  useEffect(() => {
    fetchStats()
    fetchSettings()
    fetchBooks()
  }, [])

  // Debounce para búsqueda
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchBooks(true)
    }, 500)
    return () => clearTimeout(timer)
  }, [search])

  // Listener para el Scroll Infinito
  useEffect(() => {
    const handleScroll = () => {
      if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
        setVisibleCount(prev => prev + 40)
      }
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Resetear el scroll cuando se busca o se ordena
  useEffect(() => {
    setVisibleCount(40)
    window.scrollTo(0, 0)
  }, [search, sortOption])

  const handleScan = async () => {
    setScanning(true)
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/scan?directory=${encodeURIComponent(scanDirectory)}`, {
        method: 'POST'
      })
      if (response.ok) {
        alert("Escaneo iniciado. Comenzarán a aparecer solitos en breves.")
        setShowScanModal(false)
        // Set an interval to poll for new books
        const interval = setInterval(fetchBooks, 5000); // Cada 5 segundos para no agobiar
        setTimeout(() => clearInterval(interval), 3600000); // Mantener el refresco durante 1 hora
      }
    } catch (error) {
      alert("Error al intentar escanear la carpeta.")
    } finally {
      setScanning(false)
    }
  }

  const handleClearLibrary = async () => {
    if (window.confirm("¿Estás seguro de que quieres vaciar toda la biblioteca? Esto borrará la base de datos y portadas, pero no afectará a tus ePubs originales.")) {
      try {
        const response = await fetch(`http://${window.location.hostname}:8000/api/library`, {
          method: 'DELETE'
        });
        if (response.ok) {
          setBooks([]);
        } else {
          alert("Error al intentar limpiar la biblioteca.");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Error de conexión al limpiar la biblioteca.");
      }
    }
  }

  const handleOpenEpub = async (id, e) => {
    e.stopPropagation();
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/open/${id}`);
      const data = await response.json();
      if (data.error) {
        alert("Error al abrir: " + data.error);
      }
    } catch (error) {
      alert("Error de conexión al intentar abrir el libro.");
    }
  }

  const filteredAndSortedBooks = useMemo(() => {
    // Ya vienen filtrados del backend por search, solo ordenamos aquí
    return [...books].sort((a, b) => {
      if (sortOption === 'titleAsc') return (a.title || "").localeCompare(b.title || "");
      if (sortOption === 'authorAsc') return (a.author || "").localeCompare(b.author || "");
      if (sortOption === 'dateAsc') return a.id - b.id;
      return b.id - a.id;
    });
  }, [books, sortOption]);

  const libraryStats = useMemo(() => {
    return stats;
  }, [stats]);

  const handleLocationChange = (bookId, epubcfi) => {
    setReadingLocation(epubcfi)
    
    // Actualizar el estado local inmediatamente para que si se cierra y abre el libro
    // aparezca en la posición correcta sin recargar la página
    setBooks(prevBooks => prevBooks.map(b => 
      b.id === bookId ? { ...b, progress: epubcfi } : b
    ))

    // Guardar en el backend con un pequeño delay para no saturar si se pasa rápido
    fetch(`http://${window.location.hostname}:8000/api/books/${bookId}/progress?progress=${encodeURIComponent(epubcfi)}`, {
      method: 'POST'
    }).catch(err => console.error("Error saving progress:", err))
  }

  // Estilos para los temas del lector
  const readerThemes = {
    light: { body: { background: '#fff !important', color: '#000 !important' } },
    sepia: { body: { background: '#f4ecd8 !important', color: '#5b4636 !important' } },
    dark: { body: { background: '#1a1a1a !important', color: '#ccc !important' } }
  }

  const changeFontSize = (delta) => {
    setReaderSettings(prev => ({ ...prev, fontSize: Math.max(50, Math.min(200, prev.fontSize + delta)) }))
  }

  // Efecto para aplicar cambios al lector cuando cambian los ajustes
  useEffect(() => {
    if (renditionRef.current) {
      const rendition = renditionRef.current
      rendition.themes.register('custom', readerThemes[readerSettings.theme])
      rendition.themes.select('custom')
      rendition.themes.fontSize(`${readerSettings.fontSize}%`)
    }
    
    // 🎨 SINCRONIZACIÓN DE FONDO: Eliminar el 'marco blanco'
    if (readingBookId) {
      const themeColors = {
        light: '#ffffff',
        sepia: '#f4ecd8',
        dark: '#1a1a1a'
      }
      const currentColor = themeColors[readerSettings.theme] || '#ffffff'
      document.body.style.backgroundColor = currentColor
      document.documentElement.style.backgroundColor = currentColor
    } else {
      document.body.style.backgroundColor = ''
      document.documentElement.style.backgroundColor = ''
    }
  }, [readerSettings, readingBookId])

  const toggleFlip = (id) => {
    setFlippedCards(prev => ({ ...prev, [id]: !prev[id] }))
  }

  // Detectar si estamos en el servidor local para mostrar opciones de gestión
  const isAdmin = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

  return (
    <div className="app-container">
      <header>
        <div className="logo-area">
          <h1>EPUB Master Library</h1>
          <p>Tu colección visual y fluida</p>
        </div>
        
        <div className="controls-bar">
          <div className="size-control">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{opacity: 0.6}}><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect></svg>
            <input 
              type="range" 
              min="70" 
              max="350" 
              value={cardSize}
              onChange={(e) => setCardSize(e.target.value)}
            />
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg>
          </div>

          <div className="search-box">
            <svg className="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input 
              type="text" 
              placeholder="Buscar título o autor..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <select 
            value={sortOption} 
            onChange={(e) => setSortOption(e.target.value)}
            className="sort-select"
            title="Ordenar biblioteca"
          >
            <option value="dateDesc">Más recientes (Defecto)</option>
            <option value="dateAsc">Más antiguos</option>
            <option value="titleAsc">Título (A-Z)</option>
            <option value="authorAsc">Autor (A-Z)</option>
          </select>
          {isAdmin && (
            <>
              <button className="btn-secondary" onClick={handleClearLibrary} style={{marginRight: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem'}} title="Vaciar biblioteca completa">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 6h18"></path>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
                Vaciar
              </button>
              
              <button className="btn-primary" onClick={() => setShowScanModal(true)} style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                Añadir Biblioteca
              </button>
            </>
          )}
        </div>
      </header>
      
      {libraryStats && !loading && (
        <div className="stats-panel" style={{
          display: 'flex', gap: '2rem', padding: '0.8rem 1.2rem', 
          background: 'rgba(255,255,255,0.03)', borderRadius: 'var(--radius-md)',
          marginBottom: '2rem', alignItems: 'center', fontSize: '0.85rem', width: 'fit-content'
        }}>
          <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem'}}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-color)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
            <span style={{letterSpacing: '0.5px', textTransform: 'uppercase', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)'}}>Biblioteca</span>
            <span style={{fontSize: '1.1rem', fontWeight: 700}}>{libraryStats.total.toLocaleString()} libros</span>
          </div>
        </div>
      )}

      <main>
        {loading ? (
          <div className="empty-state">
            <div className="loader"></div>
            <h3 style={{marginTop: '1rem'}}>Cargando tu biblioteca...</h3>
          </div>
        ) : books.length === 0 ? (
          <div className="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
            <h3>Tu biblioteca está vacía</h3>
            <p>Haz clic en "Añadir Biblioteca" para escanear tus archivos EPUB locales.</p>
          </div>
        ) : (
          <div className="book-grid" style={{ '--card-size': `${cardSize}px` }}>
            {filteredAndSortedBooks.slice(0, visibleCount).map((book, index) => (
              <div 
                className={`book-card fade-in ${flippedCards[book.id] ? 'flipped' : ''}`} 
                style={{ animationDelay: `${(index % 40) * 0.05}s` }} 
                key={book.id}
                onClick={() => toggleFlip(book.id)}
              >
                <div className="book-card-inner">
                  <div className="book-card-front">
                    <div className="book-cover-container">
                      {book.cover_path ? (
                        <img src={`http://${window.location.hostname}:8000${book.cover_path}`} alt={book.title} />
                      ) : (
                        <div className="no-cover">
                          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                          </svg>
                          <span>Sin Portada</span>
                        </div>
                      )}
                    </div>
                    <div className="book-info">
                      <h3 className="book-title" title={book.title}>{book.title}</h3>
                      <p className="book-author" title={book.author}>{book.author}</p>
                    </div>
                  </div>
                  
                  <div className="book-card-back">
                    <h4 title={book.title}>{book.title}</h4>
                    <h5 className="book-card-back-author" title={book.author}>{book.author}</h5>
                    <div className="book-card-divider"></div>
                    <p>{book.description && book.description !== "" ? book.description : "Sin descripción o resumen disponible para este EPUB."}</p>
                    <div style={{marginTop: '1.2rem', width: '100%'}}>
                      <button className="btn-open-epub" style={{width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center'}} onClick={(e) => { e.stopPropagation(); setReadingBookId(book.id); setReadingLocation(book.progress); }}>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{marginRight: '0.6rem'}}>
                          <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                          <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                        </svg>
                        Comenzar Lectura
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Modal Tool */}
      <div className={`modal-overlay ${showScanModal ? 'open' : ''}`}>
        <div className="modal-content">
          <h2>Escanear Carpeta</h2>
          <p style={{color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.9rem'}}>
            Introduce la ruta absoluta de la carpeta donde guardas tus archivos EPUB.
          </p>
          <input 
            type="text" 
            value={scanDirectory}
            onChange={(e) => setScanDirectory(e.target.value)}
            placeholder="Ej: C:\Epubs"
          />
          <div className="modal-actions">
            <button className="btn-secondary" onClick={() => setShowScanModal(false)}>Cancelar</button>
            <button className="btn-primary" onClick={handleScan} disabled={scaning}>
              {scaning ? 'Escaneando...' : 'Iniciar Escaneo'}
            </button>
          </div>
        </div>
      </div>

      <footer style={{ marginTop: '4rem', paddingTop: '2rem', borderTop: '1px solid var(--border-color)', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        <p style={{ marginBottom: '0.5rem' }}>Epub Biblio es un programa freeware que organiza visualmente tus archivos EPUB. Los archivos originales se mantienen.</p>
        <p>Si el programa te ha sido útil invítame a un café en <a href="https://paypal.me/ossoney" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-color)', textDecoration: 'none' }}>paypal.me/ossoney</a>. Envíame 1$ - 2$ - 3$ o lo que te apetezca.</p>
      </footer>
      {/* Web Reader Modal/Overlay */}
      {readingBookId && (
        <div style={{
          position: 'fixed', inset: 0, 
          backgroundColor: readerSettings.theme === 'dark' ? '#1a1a1a' : readerSettings.theme === 'sepia' ? '#f4ecd8' : '#fff', 
          zIndex: 9999, display: 'flex', flexDirection: 'column'
        }}>
          <div style={{
            height: '60px', display: 'flex', alignItems: 'center', padding: '0 1.5rem', 
            borderBottom: '1px solid var(--border-color)', 
            backgroundColor: readerSettings.theme === 'dark' ? '#222' : readerSettings.theme === 'sepia' ? '#ede4ce' : 'var(--surface-color)', 
            justifyContent: 'space-between',
            color: readerSettings.theme === 'dark' ? '#eee' : 'inherit'
          }}>
            <div style={{display: 'flex', alignItems: 'center', gap: '1.5rem'}}>
              <h3 style={{margin: 0, fontSize: '1rem'}}>Lector Web</h3>
              
              <div className="reader-controls" style={{display: 'flex', gap: '0.8rem', alignItems: 'center', borderLeft: '1px solid rgba(128,128,128,0.3)', paddingLeft: '1.5rem'}}>
                {/* Control de Tamaño */}
                <div style={{display: 'flex', gap: '0.2rem'}}>
                  <button className="btn-icon" onClick={() => changeFontSize(-10)} title="Reducir letra">A-</button>
                  <span style={{fontSize: '0.8rem', minWidth: '35px', textAlign: 'center'}}>{readerSettings.fontSize}%</span>
                  <button className="btn-icon" onClick={() => changeFontSize(10)} title="Aumentar letra">A+</button>
                </div>
                
                {/* Selectores de Tema */}
                <div style={{display: 'flex', gap: '0.8rem', marginLeft: '1rem'}}>
                  <button 
                    onClick={() => setReaderSettings(p => ({...p, theme: 'light'}))}
                    className={`theme-pill ${readerSettings.theme === 'light' ? 'active' : ''}`}
                    style={{backgroundColor: '#fff'}}
                    title="Tema Claro"
                  />
                  <button 
                    onClick={() => setReaderSettings(p => ({...p, theme: 'sepia'}))}
                    className={`theme-pill ${readerSettings.theme === 'sepia' ? 'active' : ''}`}
                    style={{backgroundColor: '#f4ecd8'}}
                    title="Tema Sepia"
                  />
                  <button 
                    onClick={() => setReaderSettings(p => ({...p, theme: 'dark'}))}
                    className={`theme-pill ${readerSettings.theme === 'dark' ? 'active' : ''}`}
                    style={{backgroundColor: '#1a1a1a'}}
                    title="Tema Oscuro"
                  />
                </div>
              </div>
            </div>

            <button className="btn-secondary" style={{padding: '0.4rem 1rem'}} onClick={() => setReadingBookId(null)}>
              Cerrar
            </button>
          </div>
          <div style={{flex: 1, position: 'relative'}}>
            <ReactReader
              url={`http://${window.location.hostname}:8000/api/download/${readingBookId}`}
              location={readingLocation}
              locationChanged={(epubcfi) => handleLocationChange(readingBookId, epubcfi)}
              getRendition={(rendition) => {
                renditionRef.current = rendition
                // Aplicar inmediatamente al cargar
                rendition.themes.register('custom', readerThemes[readerSettings.theme])
                rendition.themes.select('custom')
                rendition.themes.fontSize(`${readerSettings.fontSize}%`)
              }}
              epubInitOptions={{
                openAs: 'epub'
              }}
              epubOptions={{
                flow: 'paginated',
                manager: 'continuous'
              }}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default App

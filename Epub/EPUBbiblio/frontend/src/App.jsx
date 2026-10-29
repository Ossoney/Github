import { useState, useEffect, useMemo, useRef, useCallback, Fragment } from 'react'
import { ReactReader } from 'react-reader'

const getBookGradient = (title) => {
  const gradients = [
    'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
    'linear-gradient(135deg, #2b5876 0%, #4e4376 100%)',
    'linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)',
    'linear-gradient(135deg, #373b44 0%, #4286f4 100%)',
    'linear-gradient(135deg, #134e5e 0%, #71b280 100%)',
    'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)',
    'linear-gradient(135deg, #4b1248 0%, #f0c27b 100%)',
    'linear-gradient(135deg, #3a1c71 0%, #d76d77 50%, #ffaf7b 100%)',
    'linear-gradient(135deg, #232526 0%, #414345 100%)',
  ];
  let hash = 0;
  for (let i = 0; i < (title || "").length; i++) {
    hash = (hash << 5) - hash + title.charCodeAt(i);
    hash |= 0;
  }
  return gradients[Math.abs(hash) % gradients.length];
};

const CARD_SIZE_SCALES = [110, 135, 160, 190, 220];

const isAdultTheme = (name = '') => {
  const n = String(name).toLowerCase();
  return n.includes('erót') || n.includes('erot') || n.includes('adult') || n.includes('bdsm');
};

const isAdultTag = (tags = '') => {
  const t = String(tags).toLowerCase();
  return t.includes('erót') || t.includes('erot') || t.includes('adult') || t.includes('bdsm') || t.includes('sumis');
};

function App() {
  // Estado de autenticación
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('epub_biblio_token') || '')
  const [authStatus, setAuthStatus] = useState({ authenticated: false, has_master: false, user: null })
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authTab, setAuthTab] = useState('login') // 'login' | 'register' | 'forgot'
  const [authForm, setAuthForm] = useState({ username: '', password: '', confirmPassword: '' })
  const [authMessage, setAuthMessage] = useState({ text: '', type: '' }) // type: 'info' | 'success' | 'error'
  const [forgotForm, setForgotForm] = useState({ username: '', recoveryKey: '', newPassword: '', confirmPassword: '' })
  const [showChangePassModal, setShowChangePassModal] = useState(false)
  const [changePassForm, setChangePassForm] = useState({ currentPassword: '', newPassword: '', confirmPassword: '' })
  const [changePassMessage, setChangePassMessage] = useState({ text: '', type: '' })
  const [showMasterWizard, setShowMasterWizard] = useState(false)

  // Estado de Bibliotecas (Multi-Library) con persistencia
  const [libraries, setLibraries] = useState([])
  const [selectedLibraryId, setSelectedLibraryIdState] = useState(() => {
    const saved = localStorage.getItem('epub_biblio_library')
    return saved ? Number(saved) : null
  })

  const setSelectedLibraryId = useCallback((val) => {
    setSelectedLibraryIdState(val)
    if (val) {
      localStorage.setItem('epub_biblio_library', String(val))
    } else {
      localStorage.removeItem('epub_biblio_library')
    }
  }, [])
  const [showCreateLibModal, setShowCreateLibModal] = useState(false)
  const [newLibForm, setNewLibForm] = useState({ name: '', path: '', library_type: 'all' })
  const [userLibModal, setUserLibModal] = useState({ open: false, user: null, selectedIds: [] })

  // Estado del Panel de Administración (Master)
  const [showAdminModal, setShowAdminModal] = useState(false)
  const [adminTab, setAdminTab] = useState('users') // 'users' | 'libraries' | 'maintenance'
  const [adminUsers, setAdminUsers] = useState([])
  const [adminLoading, setAdminLoading] = useState(false)
  const [ratingsSyncStatus, setRatingsSyncStatus] = useState({ running: false, total: 0, processed: 0, found: 0, current_book: '' })
  const [scanStatus, setScanStatus] = useState({ running: false, total_files: 0, processed: 0, new_books: 0, current_file: '', library_name: '', last_result: null })

  // Filtro de formatos de archivo (EPUB y/o PDF)
  const [formatFilters, setFormatFilters] = useState(() => {
    try {
      const saved = localStorage.getItem('epub_biblio_formats')
      if (saved) return JSON.parse(saved)
    } catch {}
    return { epub: true, pdf: true }
  })

  const toggleFormat = (fmt) => {
    setFormatFilters(prev => {
      const next = { ...prev, [fmt]: !prev[fmt] }
      // Evitar que ambos queden desactivados (si desactiva el único activo, no hacer nada)
      if (!next.epub && !next.pdf) return prev
      try {
        localStorage.setItem('epub_biblio_formats', JSON.stringify(next))
      } catch {}
      return next
    })
  }
  const [books, setBooks] = useState([])
  const [myReadings, setMyReadings] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [scanning, setScanning] = useState(false)
  const [scanDirectory, setScanDirectory] = useState('c:\\Users\\OscarSson\\Videos\\Epub')
  const [flippedCards, setFlippedCards] = useState({})
  // 5 Escalas exactas para ordenador: 110px, 135px, 160px, 190px y 220px
  const [scaleLevel, setScaleLevel] = useState(() => {
    const saved = localStorage.getItem('epub_biblio_scale')
    return saved ? Math.min(CARD_SIZE_SCALES.length, Math.max(1, parseInt(saved, 10))) : 3
  })
  const cardSize = CARD_SIZE_SCALES[scaleLevel - 1] || 160

  const handleScaleChange = (val) => {
    const lvl = Math.min(CARD_SIZE_SCALES.length, Math.max(1, parseInt(val, 10)))
    setScaleLevel(lvl)
    localStorage.setItem('epub_biblio_scale', String(lvl))
  }
  const [sortOption, setSortOption] = useState('dateDesc')
  const [visibleCount, setVisibleCount] = useState(40)
  const [stats, setStats] = useState(null)

  // Detección de dispositivo móvil
  const checkIsMobileDevice = () => {
    if (typeof window === 'undefined') return false
    const ua = navigator.userAgent || ''
    const isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua)
    const isSmallScreen = window.innerWidth <= 768
    return isMobileUA || isSmallScreen
  }

  const [isMobile, setIsMobile] = useState(checkIsMobileDevice)
  const [mobileCols, setMobileCols] = useState(() => {
    try {
      const saved = localStorage.getItem('epub_mobile_cols')
      return saved ? Number(saved) : 3 // 3 columnas por defecto para carátulas proporcionadas en móvil
    } catch {
      return 3
    }
  })

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(checkIsMobileDevice())
    }
    window.addEventListener('resize', handleResize)
    window.addEventListener('orientationchange', handleResize)
    return () => {
      window.removeEventListener('resize', handleResize)
      window.removeEventListener('orientationchange', handleResize)
    }
  }, [])

  const handleSetMobileCols = (cols) => {
    setMobileCols(cols)
    try {
      localStorage.setItem('epub_mobile_cols', String(cols))
    } catch {
      // ignore
    }
  }

  // Lector Web
  const [readingBookId, setReadingBookId] = useState(null)
  const [readingBookObj, setReadingBookObj] = useState(null)
  const [readingLocation, setReadingLocation] = useState(null)
  const [readerSettings, setReaderSettings] = useState({
    fontSize: 100,
    theme: 'light'
  })
  const [showPreviewNotice, setShowPreviewNotice] = useState(false)
  const renditionRef = useRef(null)

  // Opiniones / Reseñas
  const [selectedBookForReviews, setSelectedBookForReviews] = useState(null)
  const [reviewsData, setReviewsData] = useState({ average_rating: 0, total_reviews: 0, reviews: [] })
  const [reviewInput, setReviewInput] = useState({ rating: 0, comment: '' })
  const [hoverRating, setHoverRating] = useState(0)
  const [savingReview, setSavingReview] = useState(false)
  const [syncingBookRating, setSyncingBookRating] = useState(false)
  const [syncFeedback, setSyncFeedback] = useState(null)

  // Reportes de incidencias (desde el modal de Valorar → Admin)
  const [showReportForm, setShowReportForm] = useState(false)
  const [reportInput, setReportInput] = useState({ report_type: 'other', message: '' })
  const [sendingReport, setSendingReport] = useState(false)
  const [reportFeedback, setReportFeedback] = useState(null)

  // Admin: reportes pendientes
  const [adminReports, setAdminReports] = useState([])
  const [loadingReports, setLoadingReports] = useState(false)

  // Notificación de descarga directa
  const [downloadToast, setDownloadToast] = useState(null)

  // Helper para peticiones autenticadas
  const apiFetch = useCallback(async (url, options = {}) => {
    const headers = {
      ...(options.headers || {})
    }
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`
    }
    return fetch(url, { ...options, headers })
  }, [authToken])

  // Comprobar estado de autenticación
  const checkAuth = useCallback(async (explicitToken = null) => {
    try {
      const tokenToUse = explicitToken || authToken || localStorage.getItem('epub_biblio_token') || ''
      const headers = {}
      if (tokenToUse) {
        headers['Authorization'] = `Bearer ${tokenToUse}`
      }
      const response = await fetch(`http://${window.location.hostname}:8000/api/auth/status`, { headers })
      if (response.ok) {
        const data = await response.json()
        setAuthStatus(data)
        if (!data.has_master) {
          setShowMasterWizard(true)
        } else {
          setShowMasterWizard(false)
        }
        if (!data.authenticated && tokenToUse) {
          localStorage.removeItem('epub_biblio_token')
          setAuthToken('')
        }
      }
    } catch (error) {
      console.error("Error comprobando autenticación:", error)
    }
  }, [authToken])

  // Cargar Bibliotecas
  const fetchLibraries = useCallback(async () => {
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/libraries`)
      if (response.ok) {
        const data = await response.json()
        setLibraries(data)
      }
    } catch (error) {
      console.error("Error al cargar bibliotecas:", error)
    }
  }, [apiFetch])

  const fetchStats = useCallback(async (targetLibId = undefined, overrideFormats = undefined) => {
    try {
      const activeLib = targetLibId !== undefined ? targetLibId : selectedLibraryId
      const currentFmts = overrideFormats !== undefined ? overrideFormats : formatFilters
      let url = `http://${window.location.hostname}:8000/api/stats`
      const params = []
      if (activeLib) params.push(`library_id=${activeLib}`)
      const fmtList = []
      if (currentFmts.epub) fmtList.push('epub')
      if (currentFmts.pdf) fmtList.push('pdf')
      if (fmtList.length > 0) params.push(`formats=${fmtList.join(',')}`)
      if (params.length > 0) url += `?${params.join('&')}`

      const response = await apiFetch(url)
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error("Error fetching stats:", error)
    }
  }, [selectedLibraryId, formatFilters, apiFetch])

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

  const fetchBooks = useCallback(async (isSearch = false, targetLibId = undefined, overrideSearch = undefined, overrideSort = undefined, overrideFormats = undefined) => {
    if (!isSearch) setLoading(true)
    try {
      const activeLib = targetLibId !== undefined ? targetLibId : selectedLibraryId
      const term = overrideSearch !== undefined ? overrideSearch : search
      const currentSort = overrideSort !== undefined ? overrideSort : sortOption
      const currentFmts = overrideFormats !== undefined ? overrideFormats : formatFilters

      const fmtList = []
      if (currentFmts.epub) fmtList.push('epub')
      if (currentFmts.pdf) fmtList.push('pdf')

      let url = `http://${window.location.hostname}:8000/api/books?limit=1000&sort_by=${encodeURIComponent(currentSort)}`
      if (fmtList.length > 0) url += `&formats=${encodeURIComponent(fmtList.join(','))}`
      if (term && term.trim()) url += `&search=${encodeURIComponent(term.trim())}`
      if (activeLib) url += `&library_id=${activeLib}`

      const response = await apiFetch(url)
      if (response.ok) {
        const data = await response.json()
        setBooks(data)
      } else if (response.status === 403) {
        setBooks([])
      }
    } catch (error) {
      console.error("Error fetching books:", error)
    } finally {
      if (!isSearch) setLoading(false)
    }
  }, [selectedLibraryId, search, sortOption, formatFilters, apiFetch])

  const fetchMyReadings = useCallback(async () => {
    if (!authStatus.authenticated) return
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/my-readings`)
      if (response.ok) {
        const data = await response.json()
        setMyReadings(data)
      }
    } catch (error) {
      console.error("Error fetching my readings:", error)
    }
  }, [apiFetch, authStatus.authenticated])

  // Carga inicial solo al montar el componente
  useEffect(() => {
    checkAuth()
    fetchLibraries()
    fetchStats()
    fetchSettings()
    fetchBooks()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleLibraryChange = (newLibId) => {
    const libIdNum = newLibId ? Number(newLibId) : null
    setSelectedLibraryId(libIdNum)
    fetchBooks(false, libIdNum, search)
    fetchStats(libIdNum)
  }

  // Cambio de biblioteca activa, ordenación o filtros de formato (EPUB / PDF)
  useEffect(() => {
    fetchBooks(false, selectedLibraryId, search, sortOption, formatFilters)
    fetchStats(selectedLibraryId, formatFilters)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedLibraryId, sortOption, formatFilters])

  useEffect(() => {
    if (activeView === 'myReadings') {
      fetchMyReadings()
    }
  }, [activeView, fetchMyReadings])

  // Debounce optimizado para búsqueda en tiempo real (300ms)
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchBooks(true, selectedLibraryId, search)
    }, 300)
    return () => clearTimeout(timer)
  }, [search, selectedLibraryId, fetchBooks])

  // Scroll Infinito
  useEffect(() => {
    const handleScroll = () => {
      if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
        setVisibleCount(prev => prev + 40)
      }
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    setVisibleCount(40)
    window.scrollTo(0, 0)
  }, [search, sortOption, activeView, selectedLibraryId, formatFilters])

  // Salida inmediata con tecla ESC para cualquier modal, panel o lector web
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        if (readingBookId) {
          setReadingBookId(null)
          if (activeView === 'myReadings') fetchMyReadings()
        }
        setShowAdminModal(false)
        setShowAuthModal(false)
        setShowCreateLibModal(false)
        setUserLibModal({ open: false, user: null, selectedIds: [] })
        setSelectedBookForReviews(null)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [readingBookId, activeView, fetchMyReadings])

  // GESTIÓN DE AUTENTICACIÓN
  const handleLogin = async (e) => {
    e?.preventDefault()
    setAuthMessage({ text: '', type: '' })
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: authForm.username,
          password: authForm.password
        })
      })
      const data = await response.json()
      if (response.ok) {
        localStorage.setItem('epub_biblio_token', data.token)
        setAuthToken(data.token)
        setShowAuthModal(false)
        setAuthForm({ username: '', password: '', confirmPassword: '' })
        checkAuth(data.token)
        fetchLibraries()
      } else {
        setAuthMessage({ text: data.detail || "Error al iniciar sesión.", type: 'error' })
      }
    } catch {
      setAuthMessage({ text: "Error de conexión con el servidor.", type: 'error' })
    }
  }

  const handleRegister = async (e) => {
    e?.preventDefault()
    setAuthMessage({ text: '', type: '' })

    if (authForm.password !== authForm.confirmPassword) {
      setAuthMessage({ text: "Las contraseñas no coinciden.", type: 'error' })
      return
    }

    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: authForm.username,
          password: authForm.password
        })
      })
      const data = await response.json()
      if (response.ok) {
        setAuthMessage({
          text: "¡Registro completado! Tu cuenta está pendiente de aprobación por el Administrador Master.",
          type: 'success'
        })
        setAuthForm({ username: '', password: '', confirmPassword: '' })
      } else {
        setAuthMessage({ text: data.detail || "Error al registrarse.", type: 'error' })
      }
    } catch {
      setAuthMessage({ text: "Error de conexión al registrar cuenta.", type: 'error' })
    }
  }

  const handleRegisterMaster = async (e) => {
    e?.preventDefault()
    setAuthMessage({ text: '', type: '' })
    if (authForm.password !== authForm.confirmPassword) {
      setAuthMessage({ text: "Las contraseñas no coinciden.", type: 'error' })
      return
    }
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/auth/register-master`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: authForm.username,
          password: authForm.password
        })
      })
      const data = await response.json()
      if (response.ok) {
        localStorage.setItem('epub_biblio_token', data.token)
        setAuthToken(data.token)
        setShowMasterWizard(false)
        setAuthForm({ username: '', password: '', confirmPassword: '' })
        checkAuth()
        fetchLibraries()
      } else {
        setAuthMessage({ text: data.detail || "Error al configurar el Master.", type: 'error' })
      }
    } catch {
      setAuthMessage({ text: "Error de conexión al crear cuenta Master.", type: 'error' })
    }
  }

  const handleLogout = async () => {
    try {
      await apiFetch(`http://${window.location.hostname}:8000/api/auth/logout`, { method: 'POST' })
    } catch {}
    localStorage.removeItem('epub_biblio_token')
    setAuthToken('')
    setAuthStatus({ authenticated: false, has_master: true, user: null })
    setActiveView('all')
    setSelectedLibraryId(null)
    fetchLibraries()
  }

  const handleResetWithKey = async (e) => {
    e?.preventDefault()
    setAuthMessage({ text: '', type: '' })
    if (forgotForm.newPassword !== forgotForm.confirmPassword) {
      setAuthMessage({ text: "Las contraseñas no coinciden.", type: 'error' })
      return
    }
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/auth/reset-with-recovery-key`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: forgotForm.username,
          recovery_key: forgotForm.recoveryKey,
          new_password: forgotForm.newPassword
        })
      })
      const data = await response.json()
      if (response.ok) {
        setAuthTab('login')
        setAuthForm(prev => ({ ...prev, username: forgotForm.username, password: '' }))
        setAuthMessage({ text: "¡Contraseña restablecida con éxito! Ya puedes iniciar sesión.", type: 'success' })
        setForgotForm({ username: '', recoveryKey: '', newPassword: '', confirmPassword: '' })
      } else {
        setAuthMessage({ text: data.detail || "Error al restablecer contraseña.", type: 'error' })
      }
    } catch {
      setAuthMessage({ text: "Error de conexión con el servidor.", type: 'error' })
    }
  }

  const handleChangeMyPassword = async (e) => {
    e?.preventDefault()
    setChangePassMessage({ text: '', type: '' })
    if (changePassForm.newPassword !== changePassForm.confirmPassword) {
      setChangePassMessage({ text: "Las nuevas contraseñas no coinciden.", type: 'error' })
      return
    }
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/auth/change-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_password: changePassForm.currentPassword,
          new_password: changePassForm.newPassword
        })
      })
      const data = await response.json()
      if (response.ok) {
        setChangePassMessage({ text: "Contraseña cambiada correctamente.", type: 'success' })
        setTimeout(() => {
          setShowChangePassModal(false)
          setChangePassForm({ currentPassword: '', newPassword: '', confirmPassword: '' })
          setChangePassMessage({ text: '', type: '' })
        }, 1200)
      } else {
        setChangePassMessage({ text: data.detail || "Error al cambiar la contraseña.", type: 'error' })
      }
    } catch {
      setChangePassMessage({ text: "Error de conexión con el servidor.", type: 'error' })
    }
  }

  const handleAdminResetPassword = async (user) => {
    const newPass = window.prompt(`Introduce la nueva contraseña para '${user.username}' (mínimo 4 caracteres):`)
    if (!newPass) return
    if (newPass.length < 4) {
      alert("La contraseña debe tener al menos 4 caracteres.")
      return
    }
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users/${user.id}/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password: newPass })
      })
      if (response.ok) {
        alert(`Contraseña actualizada con éxito para '${user.username}'.`)
      } else {
        const data = await response.json()
        alert(data.detail || "Error al restablecer contraseña.")
      }
    } catch {
      alert("Error de conexión al restablecer contraseña.")
    }
  }

  // PANEL DE ADMINISTRACIÓN MASTER
  const loadAdminUsers = async () => {
    setAdminLoading(true)
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users`)
      if (response.ok) {
        const data = await response.json()
        setAdminUsers(data)
      }
    } catch (err) {
      console.error("Error al cargar usuarios de administración:", err)
    } finally {
      setAdminLoading(false)
    }
  }

  const handleApproveUser = async (userId) => {
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users/${userId}/approve`, {
        method: 'POST'
      })
      if (response.ok) {
        loadAdminUsers()
      } else {
        alert("Error al aprobar usuario.")
      }
    } catch {
      alert("Error de conexión al aprobar.")
    }
  }

  const handleRejectUser = async (userId) => {
    if (!window.confirm("¿Seguro que deseas rechazar este usuario?")) return
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users/${userId}/reject`, {
        method: 'POST'
      })
      if (response.ok) {
        loadAdminUsers()
      }
    } catch {
      alert("Error al rechazar usuario.")
    }
  }

  const handleForceLogoutUser = async (u) => {
    if (!window.confirm(`¿Cerrar todas las sesiones activas de "${u.username}"?`)) return
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users/${u.id}/logout`, {
        method: 'POST'
      })
      if (response.ok) {
        alert(`Sesión de "${u.username}" cerrada correctamente.`)
        loadAdminUsers()
      } else {
        alert("Error al cerrar la sesión del usuario.")
      }
    } catch {
      alert("Error de conexión al cerrar la sesión.")
    }
  }

  const handleDeleteUser = async (userId) => {
    if (!window.confirm("¿Estás seguro de eliminar este usuario permanentemente?")) return
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users/${userId}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        loadAdminUsers()
      }
    } catch {
      alert("Error al eliminar usuario.")
    }
  }

  const handleToggleRole = async (userId, currentRole) => {
    const newRole = currentRole === 'master' ? 'reader' : 'master'
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users/${userId}/role`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: newRole })
      })
      if (response.ok) {
        loadAdminUsers()
      }
    } catch {
      alert("Error al cambiar rol.")
    }
  }

  const handleEditDownloadLimit = async (u) => {
    const limitVal = u.daily_download_limit !== undefined ? u.daily_download_limit : u.weekly_download_limit
    const currentVal = limitVal !== null && limitVal !== undefined ? limitVal : 'ilimitado'
    const input = window.prompt(
      `Configurar límite de descargas diarias para "${u.username}":\n\n- Escribe un número (ej. 1, 2, 5)\n- O escribe "ilimitado" / "-1" para no poner ningún límite\n\nValor actual: ${currentVal}`,
      limitVal !== null && limitVal !== undefined ? limitVal : ''
    )
    if (input === null) return // Cancelado

    let newLimit = null
    const cleaned = input.trim().toLowerCase()
    if (cleaned !== '' && cleaned !== 'ilimitado' && cleaned !== 'sin limite' && cleaned !== '-1') {
      const parsed = parseInt(cleaned, 10)
      if (isNaN(parsed) || parsed < 0) {
        alert("Por favor, introduce un número válido mayor o igual a 0, o 'ilimitado'.")
        return
      }
      newLimit = parsed
    }

    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users/${u.id}/download-limit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ daily_limit: newLimit, weekly_limit: newLimit })
      })
      if (response.ok) {
        loadAdminUsers()
      } else {
        const err = await response.json().catch(() => ({}))
        alert(err.detail || "Error al actualizar el límite de descarga.")
      }
    } catch {
      alert("Error de conexión al actualizar el límite.")
    }
  }

  // GESTIÓN DE BIBLIOTECAS (MULTI-LIBRARY)
  const handleCreateLibrary = async (e) => {
    e?.preventDefault()
    if (!newLibForm.name.trim()) return
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/libraries`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newLibForm)
      })
      if (response.ok) {
        const createdLib = await response.json()
        setShowCreateLibModal(false)
        setNewLibForm({ name: '', path: '', library_type: 'all' })
        await fetchLibraries()
        setSelectedLibraryId(createdLib.id)
        setShowAdminModal(false)
        fetchBooks(false, createdLib.id)
        fetchStats(createdLib.id)
      } else {
        const data = await response.json()
        alert(data.detail || "Error al crear la biblioteca.")
      }
    } catch {
      alert("Error de conexión al crear biblioteca.")
    }
  }

  const handleDeleteLibrary = async (libId, libName) => {
    if (!window.confirm(`¿Estás seguro de eliminar la biblioteca '${libName}'? Se borrarán sus libros asignados del catálogo.`)) return
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/libraries/${libId}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        if (selectedLibraryId === libId) setSelectedLibraryId(null)
        fetchLibraries()
        fetchBooks(false, null)
        fetchStats(null)
      } else {
        const data = await response.json()
        alert(data.detail || "Error al eliminar biblioteca.")
      }
    } catch {
      alert("Error de conexión al eliminar biblioteca.")
    }
  }

  const handleScanLibrary = async (libId, libName, libPath) => {
    const pathInput = window.prompt(`Directorio de EPUBs para escanear en '${libName}':`, libPath || '')
    if (pathInput === null) return
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/libraries/${libId}/scan?directory=${encodeURIComponent(pathInput)}`, {
        method: 'POST'
      })
      if (response.ok) {
        alert(`Escaneo de '${libName}' iniciado en segundo plano. Cambiando la vista a esta biblioteca.`)
        setSelectedLibraryId(libId)
        setShowAdminModal(false)
        fetchLibraries()
        fetchBooks(false, libId)
        fetchStats(libId)
        const interval = setInterval(() => { 
          fetchBooks(false, libId)
          fetchLibraries()
          fetchStats(libId)
        }, 4000)
        setTimeout(() => clearInterval(interval), 180000)
      } else {
        const data = await response.json()
        alert(data.detail || "Error al iniciar escaneo.")
      }
    } catch {
      alert("Error de conexión al iniciar escaneo.")
    }
  }

  // ASIGNACIÓN DE BIBLIOTECAS A USUARIOS
  const openUserLibrariesModal = (user) => {
    setUserLibModal({
      open: true,
      user: user,
      selectedIds: user.assigned_libraries || []
    })
  }

  const toggleUserLibraryCheckbox = (libId) => {
    setUserLibModal(prev => {
      const exists = prev.selectedIds.includes(libId)
      const nextIds = exists 
        ? prev.selectedIds.filter(id => id !== libId)
        : [...prev.selectedIds, libId]
      return { ...prev, selectedIds: nextIds }
    })
  }

  const handleSaveUserLibraries = async () => {
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/admin/users/${userLibModal.user.id}/libraries`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ library_ids: userLibModal.selectedIds })
      })
      if (response.ok) {
        setUserLibModal({ open: false, user: null, selectedIds: [] })
        loadAdminUsers()
        alert("Bibliotecas asignadas correctamente.")
      } else {
        alert("Error al guardar asignación de bibliotecas.")
      }
    } catch {
      alert("Error de conexión al guardar asignación.")
    }
  }

  // ESCANEO Y VACIADO GLOBAL
  const handleScanGlobal = async () => {
    setScanning(true)
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/scan?directory=${encodeURIComponent(scanDirectory)}&library_id=1`, {
        method: 'POST'
      })
      if (response.ok) {
        alert("Escaneo iniciado en segundo plano por el Administrador Master.")
        setShowAdminModal(false)
        const interval = setInterval(() => { fetchBooks(); fetchLibraries(); }, 5000)
        setTimeout(() => clearInterval(interval), 3600000)
      } else {
        alert("Error al iniciar el escaneo.")
      }
    } catch {
      alert("Error al intentar escanear la carpeta.")
    } finally {
      setScanning(false)
    }
  }

  const handleClearLibrary = async () => {
    if (window.confirm("¿Estás seguro de que quieres vaciar toda la biblioteca? Esto borrará la base de datos y portadas, pero no afectará a tus ePubs originales.")) {
      try {
        const response = await apiFetch(`http://${window.location.hostname}:8000/api/library`, {
          method: 'DELETE'
        })
        if (response.ok) {
          setBooks([])
          setShowAdminModal(false)
          fetchStats()
          fetchLibraries()
          alert("Biblioteca limpiada correctamente.")
        } else {
          alert("Error al intentar limpiar la biblioteca.")
        }
      } catch {
        alert("Error de conexión al limpiar la biblioteca.")
      }
    }
  }

  // SINCRONIZACIÓN EN SEGUNDO PLANO DE VALORACIONES (OPEN LIBRARY)
  const handleStartRatingsSync = async () => {
    try {
      const res = await apiFetch(`http://${window.location.hostname}:8000/api/admin/sync-ratings/start`, { method: 'POST' })
      if (res.ok) {
        setRatingsSyncStatus(prev => ({ ...prev, running: true, stop_requested: false }))
      } else {
        alert("Error al iniciar sincronización.")
      }
    } catch {
      alert("Error de conexión al iniciar la sincronización.")
    }
  }

  const handleStopRatingsSync = async () => {
    try {
      const res = await apiFetch(`http://${window.location.hostname}:8000/api/admin/sync-ratings/stop`, { method: 'POST' })
      if (res.ok) {
        setRatingsSyncStatus(prev => ({ ...prev, stop_requested: true }))
      }
    } catch {
      alert("Error al solicitar detención de la sincronización.")
    }
  }

  const handleStopScan = async () => {
    try {
      const res = await apiFetch(`http://${window.location.hostname}:8000/api/admin/scan/stop`, { method: 'POST' })
      if (res.ok) {
        setScanStatus(prev => ({ ...prev, stop_requested: true }))
      }
    } catch {
      alert("Error al solicitar detención del escaneo.")
    }
  }

  useEffect(() => {
    let timer
    const pollStatuses = async () => {
      if (authStatus.authenticated && authStatus.user?.role === 'master') {
        try {
          // Consultar estado de escaneo
          const scanRes = await apiFetch(`http://${window.location.hostname}:8000/api/admin/scan/status`)
          if (scanRes.ok) {
            const data = await scanRes.json()
            setScanStatus(prev => {
              // Si estaba corriendo y acaba de terminar, refrescar catálogo y bibliotecas
              if (prev.running && !data.running) {
                fetchBooks()
                fetchLibraries()
                fetchStats()
              }
              return data
            })
          }
        } catch {}

        // Consultar estado de Open Library si está en Mantenimiento
        if (showAdminModal && adminTab === 'maintenance') {
          try {
            const res = await apiFetch(`http://${window.location.hostname}:8000/api/admin/sync-ratings/status`)
            if (res.ok) {
              const data = await res.json()
              setRatingsSyncStatus(data)
            }
          } catch {}
        }
      }
    }

    if (authStatus.authenticated && authStatus.user?.role === 'master') {
      pollStatuses()
      timer = setInterval(pollStatuses, 2000)
    }
    return () => {
      if (timer) clearInterval(timer)
    }
  }, [showAdminModal, adminTab, authStatus, apiFetch, fetchBooks, fetchLibraries, fetchStats])

  // LECTOR WEB & HISTORIAL INDIVIDUAL
  const initialCfiRef = useRef(null)

  const startReading = async (book) => {
    setReadingBookId(book.id)
    setReadingBookObj(book)
    setShowPreviewNotice(!authStatus.authenticated)
    initialCfiRef.current = null
    try {
      if (authStatus.authenticated) {
        const response = await apiFetch(`http://${window.location.hostname}:8000/api/books/${book.id}/my-progress`)
        if (response.ok) {
          const data = await response.json()
          setReadingLocation(data.progress || book.progress || null)
        } else {
          setReadingLocation(book.progress || null)
        }
      } else {
        // Modo anónimo: empezar siempre desde el inicio
        setReadingLocation(null)
      }
    } catch {
      setReadingLocation(book.progress || null)
    }
  }

  const handleLocationChange = (bookId, epubcfi) => {
    // Si no está autenticado, solo puede ver la primera página
    if (!authStatus.authenticated) {
      if (!initialCfiRef.current) {
        initialCfiRef.current = epubcfi
        setReadingLocation(epubcfi)
      } else if (epubcfi !== initialCfiRef.current) {
        // Intentó avanzar de página sin estar logueado
        setShowPreviewNotice(true)
        if (renditionRef.current && initialCfiRef.current) {
          try {
            renditionRef.current.display(initialCfiRef.current)
          } catch {
            // ignore
          }
        }
        return
      }
      return
    }

    setReadingLocation(epubcfi)
    setBooks(prev => prev.map(b => b.id === bookId ? { ...b, progress: epubcfi } : b))
    apiFetch(`http://${window.location.hostname}:8000/api/books/${bookId}/progress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ progress: epubcfi })
    }).catch(err => console.error("Error guardando progreso:", err))
  }

  // RESEÑAS Y OPINIONES
  const openReviewsModal = async (book, e) => {
    e?.stopPropagation()
    setSelectedBookForReviews(book)
    setReviewInput({ rating: 0, comment: '' })
    setHoverRating(0)
    setSyncFeedback(null)
    setShowReportForm(false)
    setReportInput({ report_type: 'other', message: '' })
    setReportFeedback(null)
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/api/books/${book.id}/reviews`)
      if (response.ok) {
        const data = await response.json()
        setReviewsData(data)
        if (data.average_rating > 0 || data.cover_path) {
          setBooks(prev => prev.map(b => b.id === book.id ? { 
            ...b, 
            ...(data.average_rating > 0 ? { rating: data.average_rating, reviews_count: data.total_reviews } : {}),
            ...(data.cover_path ? { cover_path: data.cover_path } : {})
          } : b))
          setMyReadings(prev => prev.map(b => b.id === book.id ? { 
            ...b, 
            ...(data.average_rating > 0 ? { rating: data.average_rating, reviews_count: data.total_reviews } : {}),
            ...(data.cover_path ? { cover_path: data.cover_path } : {})
          } : b))
        }
        if (authStatus.authenticated) {
          const myRev = data.reviews.find(r => r.user_id === authStatus.user?.id)
          if (myRev) {
            setReviewInput({ rating: myRev.rating, comment: myRev.comment || '' })
          }
        }
      }
    } catch (err) {
      console.error("Error al obtener opiniones:", err)
    }
  }

  const handleSyncSingleBookRating = async () => {
    if (!selectedBookForReviews) return
    setSyncingBookRating(true)
    setSyncFeedback(null)
    try {
      const res = await fetch(`http://${window.location.hostname}:8000/api/books/${selectedBookForReviews.id}/sync-external-rating`, { method: 'POST' })
      if (res.ok) {
        const data = await res.json()
        setReviewsData(prev => ({
          ...prev,
          average_rating: data.average_rating,
          total_reviews: data.total_reviews,
          source: data.source
        }))
        setSyncFeedback({
          status: data.status,
          message: data.message
        })
        if (data.average_rating > 0 || data.cover_path) {
          setBooks(prev => prev.map(b => b.id === selectedBookForReviews.id ? { 
            ...b, 
            ...(data.average_rating > 0 ? { rating: data.average_rating, reviews_count: data.total_reviews } : {}),
            ...(data.cover_path ? { cover_path: data.cover_path } : {})
          } : b))
          setMyReadings(prev => prev.map(b => b.id === selectedBookForReviews.id ? { 
            ...b, 
            ...(data.average_rating > 0 ? { rating: data.average_rating, reviews_count: data.total_reviews } : {}),
            ...(data.cover_path ? { cover_path: data.cover_path } : {})
          } : b))
        }
      } else {
        setSyncFeedback({ status: 'error', message: 'Error en la respuesta del servidor al consultar Open Library.' })
      }
    } catch (e) {
      console.error("Error al sincronizar libro con Open Library:", e)
      setSyncFeedback({ status: 'error', message: 'No se pudo conectar con el servidor o Open Library. Comprueba tu conexión a Internet.' })
    } finally {
      setSyncingBookRating(false)
    }
  }

  const handleSaveReview = async (e) => {
    e?.preventDefault()
    if (!authStatus.authenticated) {
      setShowAuthModal(true)
      return
    }
    if (!reviewInput.rating || reviewInput.rating < 1) {
      alert("Por favor, selecciona una puntuación de 1 a 5 estrellas para valorar este libro.")
      return
    }
    setSavingReview(true)
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/books/${selectedBookForReviews.id}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rating: reviewInput.rating,
          comment: reviewInput.comment
        })
      })
      if (response.ok) {
        const updated = await fetch(`http://${window.location.hostname}:8000/api/books/${selectedBookForReviews.id}/reviews`)
        if (updated.ok) {
          const newRevData = await updated.json()
          setReviewsData(newRevData)
          const newAvg = newRevData.average_rating || 0.0
          const newCnt = newRevData.total_reviews || 0
          setBooks(prev => prev.map(b => b.id === selectedBookForReviews.id ? { ...b, rating: newAvg, reviews_count: newCnt } : b))
          setMyReadings(prev => prev.map(b => b.id === selectedBookForReviews.id ? { ...b, rating: newAvg, reviews_count: newCnt } : b))
        }
      } else {
        alert("Error al guardar opinión.")
      }
    } catch {
      alert("Error de conexión al publicar reseña.")
    } finally {
      setSavingReview(false)
    }
  }

  const handleDeleteReview = async () => {
    if (!window.confirm("¿Seguro que deseas eliminar tu opinión?")) return
    try {
      const response = await apiFetch(`http://${window.location.hostname}:8000/api/books/${selectedBookForReviews.id}/reviews`, {
        method: 'DELETE'
      })
      if (response.ok) {
        setReviewInput({ rating: 0, comment: '' })
        setHoverRating(0)
        const updated = await fetch(`http://${window.location.hostname}:8000/api/books/${selectedBookForReviews.id}/reviews`)
        if (updated.ok) {
          const newRevData = await updated.json()
          setReviewsData(newRevData)
          const newAvg = newRevData.average_rating || 0.0
          const newCnt = newRevData.total_reviews || 0
          setBooks(prev => prev.map(b => b.id === selectedBookForReviews.id ? { ...b, rating: newAvg, reviews_count: newCnt } : b))
          setMyReadings(prev => prev.map(b => b.id === selectedBookForReviews.id ? { ...b, rating: newAvg, reviews_count: newCnt } : b))
        }
      }
    } catch {
      alert("Error al eliminar opinión.")
    }
  }

  const handleSendReport = async (e) => {
    e?.preventDefault()
    if (!reportInput.message.trim()) return
    setSendingReport(true)
    setReportFeedback(null)
    try {
      const res = await apiFetch(
        `http://${window.location.hostname}:8000/api/books/${selectedBookForReviews.id}/report`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ report_type: reportInput.report_type, message: reportInput.message.trim() })
        }
      )
      const data = await res.json()
      if (res.ok) {
        setReportFeedback({ ok: true, message: data.message })
        setReportInput({ report_type: 'other', message: '' })
        setShowReportForm(false)
      } else {
        setReportFeedback({ ok: false, message: data.detail || 'Error al enviar el reporte.' })
      }
    } catch {
      setReportFeedback({ ok: false, message: 'Error de conexión al enviar el reporte.' })
    } finally {
      setSendingReport(false)
    }
  }

  const loadAdminReports = async () => {
    setLoadingReports(true)
    try {
      const res = await apiFetch(`http://${window.location.hostname}:8000/api/admin/reports`)
      if (res.ok) setAdminReports(await res.json())
    } catch { /* silencioso */ }
    finally { setLoadingReports(false) }
  }

  const handleMarkReportReviewed = async (reportId) => {
    try {
      const res = await apiFetch(
        `http://${window.location.hostname}:8000/api/admin/reports/${reportId}/mark-reviewed`,
        { method: 'POST' }
      )
      if (res.ok) setAdminReports(prev => prev.filter(r => r.id !== reportId))
    } catch { /* silencioso */ }
  }

  // Filtrado y ordenación
  const currentBooksList = activeView === 'myReadings' ? myReadings : books
  const filteredAndSortedBooks = useMemo(() => {
    return [...currentBooksList].sort((a, b) => {
      if (sortOption === 'ratingDesc') {
        const diff = (b.rating || 0) - (a.rating || 0)
        if (diff !== 0) return diff
        return b.id - a.id
      }
      if (sortOption === 'titleAsc') return (a.title || "").localeCompare(b.title || "")
      if (sortOption === 'authorAsc') return (a.author || "").localeCompare(b.author || "")
      if (sortOption === 'dateAsc') return a.id - b.id
      return b.id - a.id
    })
  }, [currentBooksList, sortOption])

  const selectedLibObj = libraries.find(l => l.id === selectedLibraryId)
  const isSelectedLibAdult = selectedLibObj && isAdultTheme(selectedLibObj.name)

  // Ajustes de lectura
  const readerThemes = {
    light: { body: { background: '#fff !important', color: '#000 !important' } },
    sepia: { body: { background: '#f4ecd8 !important', color: '#5b4636 !important' } },
    dark: { body: { background: '#1a1a1a !important', color: '#ccc !important' } }
  }

  const changeFontSize = (delta) => {
    setReaderSettings(prev => ({ ...prev, fontSize: Math.max(50, Math.min(200, prev.fontSize + delta)) }))
  }

  useEffect(() => {
    if (renditionRef.current) {
      const rendition = renditionRef.current
      rendition.themes.register('custom', readerThemes[readerSettings.theme])
      rendition.themes.select('custom')
      rendition.themes.fontSize(`${readerSettings.fontSize}%`)
    }
    if (readingBookId) {
      const themeColors = { light: '#ffffff', sepia: '#f4ecd8', dark: '#1a1a1a' }
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

  const isMaster = authStatus.authenticated && authStatus.user?.role === 'master'
  const pendingUsersCount = adminUsers.filter(u => u.status === 'pending').length

  return (
    <div className="app-container">
      <header className="app-header">
        {/* Línea 1: Identidad y Usuario */}
        <div className="header-top">
          <div className="logo-area">
            <h1>EPUB Biblio</h1>
            <p>Tu colección visual y fluida</p>
          </div>

          {/* Zona de Usuario / Autenticación */}
          <div className="user-area">
            {authStatus.authenticated ? (
              <>
                <div className="user-profile-badge">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                  <span className="user-name-text" title={authStatus.user?.username}>{authStatus.user?.username}</span>
                  <span className={`role-badge ${authStatus.user?.role}`}>
                    {authStatus.user?.role === 'master' ? '👑 Master' : 'Lector'}
                  </span>
                </div>

                {isMaster && (
                  <>
                    {scanStatus.running && (
                      <button
                        className="btn-secondary btn-sm-mobile"
                        onClick={() => { setShowAdminModal(true); setAdminTab('maintenance'); }}
                        style={{
                          background: 'rgba(16, 185, 129, 0.15)',
                          borderColor: '#10b981',
                          color: '#34d399',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.4rem',
                          fontSize: '0.8rem',
                          cursor: 'pointer'
                        }}
                        title="Escaneo en curso. Haz clic para ver progreso en Mantenimiento."
                      >
                        <span style={{ animation: 'spin 1.5s linear infinite', display: 'inline-block' }}>⚡</span>
                        <span>{scanStatus.total_files > 0 ? `${Math.round((scanStatus.processed / scanStatus.total_files) * 100)}%` : 'Escaneando...'}</span>
                      </button>
                    )}

                    <button 
                      className="btn-primary btn-sm-mobile" 
                      onClick={() => { setShowAdminModal(true); loadAdminUsers(); fetchLibraries(); }} 
                      style={{ position: 'relative' }}
                      title="Panel de Administración Master"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="12" cy="12" r="3"></circle>
                        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                      </svg>
                      <span>Admin</span>
                      {pendingUsersCount > 0 && (
                        <span className="badge-notification">
                          {pendingUsersCount}
                        </span>
                      )}
                    </button>
                  </>
                )}

                <button 
                  className="btn-secondary btn-sm-mobile" 
                  onClick={handleLogout} 
                  title="Cerrar sesión"
                  style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                    <polyline points="16 17 21 12 16 7"></polyline>
                    <line x1="21" y1="12" x2="9" y2="12"></line>
                  </svg>
                  <span>Salir</span>
                </button>
              </>
            ) : (
              <button 
                className="btn-primary" 
                onClick={() => { setShowAuthModal(true); setAuthMessage({ text: '', type: '' }); }}
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                  <polyline points="10 17 15 12 10 7"></polyline>
                  <line x1="15" y1="12" x2="3" y2="12"></line>
                </svg>
                <span>Iniciar Sesión</span>
              </button>
            )}
          </div>
        </div>

        {/* Línea 2: Barra de Búsqueda y Filtros */}
        <div className="header-controls">
          {/* Búsqueda */}
          <div className="search-box">
            <svg className="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input 
              type="text" 
              placeholder="Buscar título o autor..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault()
                  fetchBooks(true, selectedLibraryId, search)
                }
              }}
            />
            {search && (
              <button 
                type="button" 
                onClick={() => {
                  setSearch('')
                  fetchBooks(true, selectedLibraryId, '')
                }} 
                className="search-clear-btn"
                title="Limpiar búsqueda"
              >
                ✕
              </button>
            )}
          </div>

          {/* Filtros: Biblioteca, Ordenación y Zoom */}
          <div className="filter-controls">
            {/* Selector de Biblioteca Activa (Multi-Library) */}
            {libraries.length > 0 && (
              <select
                value={selectedLibraryId || ''}
                onChange={(e) => handleLibraryChange(e.target.value)}
                className={`sort-select lib-filter-select ${isSelectedLibAdult ? 'adult-active' : ''}`}
                title="Biblioteca activa"
              >
                <option value="" style={{ color: 'var(--text-main)', background: 'var(--surface-color)' }}>
                  📚 Todas las bibliotecas
                </option>
                {libraries.map((lib, idx) => {
                  const adult = isAdultTheme(lib.name)
                  const prevLib = libraries[idx - 1]
                  const showDivider = prevLib && prevLib.group !== lib.group
                  return (
                    <Fragment key={lib.id}>
                      {showDivider && (
                        <option disabled style={{ color: '#94a3b8', background: 'var(--surface-color)', textAlign: 'center', letterSpacing: '2px' }}>
                          ──────────────
                        </option>
                      )}
                      <option 
                        value={lib.id}
                        style={{ 
                          color: adult ? '#f472b6' : 'var(--text-main)', 
                          fontWeight: adult ? 700 : 'normal',
                          background: 'var(--surface-color)'
                        }}
                      >
                        {adult ? '🔞 ' : (lib.name.includes('⭐') ? '' : '🏛️ ')}{lib.name} ({lib.book_count.toLocaleString()})
                      </option>
                    </Fragment>
                  )
                })}
              </select>
            )}

            {/* Conmutadores de formato EPUB / PDF (Solo visible para el Administrador Master) */}
            {authStatus.authenticated && authStatus.user?.role === 'master' && (
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem', background: 'var(--surface-color)', padding: '0.2rem 0.35rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                <button
                  type="button"
                  onClick={() => toggleFormat('epub')}
                  style={{
                    padding: '0.35rem 0.65rem',
                    fontSize: '0.78rem',
                    fontWeight: 600,
                    borderRadius: '4px',
                    border: 'none',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.3rem',
                    transition: 'all 0.15s ease',
                    background: formatFilters.epub ? 'rgba(99, 102, 241, 0.2)' : 'transparent',
                    color: formatFilters.epub ? 'var(--accent-hover)' : 'var(--text-muted)',
                    boxShadow: formatFilters.epub ? 'inset 0 0 0 1px var(--accent-color)' : 'none',
                    opacity: formatFilters.epub ? 1 : 0.55
                  }}
                  title={formatFilters.epub ? "EPUB activo (haz clic para desactivar)" : "EPUB inactivo (haz clic para activar)"}
                >
                  <span>{formatFilters.epub ? '✓' : '○'}</span>
                  <span>EPUB</span>
                </button>
                <button
                  type="button"
                  onClick={() => toggleFormat('pdf')}
                  style={{
                    padding: '0.35rem 0.65rem',
                    fontSize: '0.78rem',
                    fontWeight: 600,
                    borderRadius: '4px',
                    border: 'none',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.3rem',
                    transition: 'all 0.15s ease',
                    background: formatFilters.pdf ? 'rgba(239, 68, 68, 0.2)' : 'transparent',
                    color: formatFilters.pdf ? '#f87171' : 'var(--text-muted)',
                    boxShadow: formatFilters.pdf ? 'inset 0 0 0 1px #ef4444' : 'none',
                    opacity: formatFilters.pdf ? 1 : 0.55
                  }}
                  title={formatFilters.pdf ? "PDF activo (haz clic para desactivar)" : "PDF inactivo (haz clic para activar)"}
                >
                  <span>{formatFilters.pdf ? '✓' : '○'}</span>
                  <span>PDF</span>
                </button>
              </div>
            )}

            {/* Ordenar */}
            <select 
              value={sortOption} 
              onChange={(e) => setSortOption(e.target.value)}
              className="sort-select order-filter-select"
              title="Ordenar biblioteca"
            >
              <option value="dateDesc">Más recientes (Defecto)</option>
              <option value="ratingDesc">Mejor valorados ⭐</option>
              <option value="dateAsc">Más antiguos</option>
              <option value="titleAsc">Título (A-Z)</option>
              <option value="authorAsc">Autor (A-Z)</option>
            </select>

            {/* Tamaño de tarjetas: 5 escalas en ordenador (proporcionales, desde 150px hasta 300px) */}
            <div className="size-control" title={`Tamaño de portadas: Nivel ${scaleLevel} de ${CARD_SIZE_SCALES.length}`}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{opacity: 0.6}}><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect></svg>
              <input 
                type="range" 
                min="1" 
                max={CARD_SIZE_SCALES.length} 
                step="1"
                list="size-scales"
                value={scaleLevel}
                onChange={(e) => handleScaleChange(e.target.value)}
                title={`Tamaño de portadas: Nivel ${scaleLevel} de ${CARD_SIZE_SCALES.length}`}
              />
              <datalist id="size-scales">
                <option value="1"></option>
                <option value="2"></option>
                <option value="3"></option>
                <option value="4"></option>
                <option value="5"></option>
              </datalist>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg>
              <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)', minWidth: '1.8rem', textAlign: 'center' }}>
                {scaleLevel}/{CARD_SIZE_SCALES.length}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Pestañas de Vista y Estadísticas */}
      <div className="sub-header-bar">
        <div className="nav-tabs">
          <button 
            className={`nav-tab-btn ${activeView === 'all' ? 'active' : ''}`}
            onClick={() => setActiveView('all')}
          >
            📚 Todos los libros
          </button>
          {authStatus.authenticated && (
            <button 
              className={`nav-tab-btn ${activeView === 'myReadings' ? 'active' : ''}`}
              onClick={() => setActiveView('myReadings')}
            >
              📖 Mis lecturas
            </button>
          )}
        </div>

        {/* Selector de Tamaño de Portadas para Móvil (Detección automática) */}
        {isMobile && (
          <div className="mobile-view-control">
            <span className="mobile-view-label">Portadas:</span>
            <div className="mobile-view-buttons">
              <button 
                type="button" 
                className={`mobile-view-btn ${mobileCols === 3 ? 'active' : ''}`}
                onClick={() => handleSetMobileCols(3)}
                title="3 libros por fila (Compacto)"
              >
                3 por fila
              </button>
              <button 
                type="button" 
                className={`mobile-view-btn ${mobileCols === 2 ? 'active' : ''}`}
                onClick={() => handleSetMobileCols(2)}
                title="2 libros por fila (Grande)"
              >
                2 por fila
              </button>
            </div>
          </div>
        )}

        {stats && !loading && (
          <div className="stats-panel">
            <div style={{display: 'flex', alignItems: 'center', gap: '0.6rem'}}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-color)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
              <span className="stats-label">
                {selectedLibraryId ? (libraries.find(l => l.id === selectedLibraryId)?.name || 'Biblioteca') : 'Total'}
              </span>
              <span className="stats-count">{stats.total.toLocaleString()} libros</span>
            </div>
          </div>
        )}
      </div>

      {/* Indicador de Filtro de Biblioteca Activa */}
      {selectedLibraryId && (
        <div className={`library-active-banner ${isSelectedLibAdult ? 'adult-theme-banner' : ''}`}>
          <div>
            <span style={{ color: 'var(--text-muted)' }}>Viendo: </span>
            <strong style={{ color: isSelectedLibAdult ? '#f472b6' : 'var(--accent-hover)' }}>
              {isSelectedLibAdult ? '🔞 ' : '🏛️ '}{libraries.find(l => l.id === selectedLibraryId)?.name || 'Biblioteca'}
            </strong>
          </div>
          <button 
            className="btn-secondary btn-sm-mobile" 
            onClick={() => handleLibraryChange('')}
          >
            Ver todas las bibliotecas ✕
          </button>
        </div>
      )}

      {/* Catálogo de Libros */}
      <main>
        {loading ? (
          <div className="empty-state">
            <div className="loader"></div>
            <h3 style={{marginTop: '1rem'}}>Cargando biblioteca...</h3>
          </div>
        ) : filteredAndSortedBooks.length === 0 ? (
          <div className="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
            {activeView === 'myReadings' ? (
              <>
                <h3>Aún no has comenzado a leer libros</h3>
                <p>Explora el catálogo general y haz clic en "Leer" para guardar tu progreso personal.</p>
              </>
            ) : (
              <>
                <h3>No se encontraron libros</h3>
                <p>{search ? "Prueba con otro término de búsqueda." : "No hay libros en esta biblioteca o no tienes permisos asignados."}</p>
              </>
            )}
          </div>
        ) : (
          <div 
            className={`book-grid ${isMobile ? `mobile-grid-${mobileCols}` : ''}`} 
            style={{ 
              '--card-size': isMobile 
                ? (mobileCols === 3 ? '108px' : '165px') 
                : `${cardSize}px` 
            }}
          >
            {filteredAndSortedBooks.slice(0, visibleCount).map((book, index) => (
              <div 
                className={`book-card fade-in ${flippedCards[book.id] ? 'flipped' : ''}`} 
                style={{ animationDelay: `${(index % 40) * 0.05}s` }} 
                key={book.id}
                onClick={() => toggleFlip(book.id)}
              >
                <div className="book-card-inner">
                  {/* Cara Frontal */}
                  <div className="book-card-front">
                    <div className="book-cover-container">
                      {book.cover_path ? (
                        <img 
                          src={`http://${window.location.hostname}:8000${book.cover_path}`} 
                          alt={book.title} 
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                            const fallback = e.currentTarget.nextElementSibling;
                            if (fallback) fallback.style.display = 'flex';
                          }}
                        />
                      ) : null}
                      <div 
                        className="no-cover-art" 
                        style={{ 
                          background: getBookGradient(book.title),
                          display: book.cover_path ? 'none' : 'flex' 
                        }}
                      >
                        <div className="book-spine-line"></div>
                        <div className="no-cover-content">
                          <span className="no-cover-title">{book.title}</span>
                          <span className="no-cover-author">{book.author}</span>
                        </div>
                        <div className="no-cover-decor">📖</div>
                      </div>
                    </div>
                    <div className="book-info">
                      <h3 className="book-title" title={book.title}>{book.title}</h3>
                      <div className="book-author-row" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '0.35rem', minWidth: 0, marginTop: 'auto' }}>
                        <p className="book-author" title={book.author} style={{ margin: 0, flex: 1, minWidth: 0 }}>
                          {book.format === 'pdf' && (
                            <span style={{ display: 'inline-block', marginRight: '0.35rem', padding: '0.05rem 0.3rem', fontSize: '0.65rem', fontWeight: 800, background: '#ef4444', color: '#fff', borderRadius: '3px', verticalAlign: 'middle' }}>PDF</span>
                          )}
                          {book.author}
                        </p>
                        {book.rating > 0 && (
                          <div 
                            className="book-rating-badge"
                            title={`Valoración: ${book.rating} (${book.reviews_count || 1} ${book.reviews_count === 1 ? 'opinión' : 'opiniones'})`}
                            style={{ 
                              display: 'inline-flex', 
                              alignItems: 'center', 
                              gap: '0.15rem', 
                              fontSize: 'clamp(0.68rem, calc(var(--card-size) * 0.002 + 0.35rem), 0.82rem)', 
                              fontWeight: 700, 
                              color: '#f59e0b',
                              flexShrink: 0,
                              whiteSpace: 'nowrap'
                            }}
                          >
                            ⭐ {book.rating.toFixed(1)}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  {/* Cara Trasera (Ficha, Lectura y Reseñas) */}
                  <div className="book-card-back">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.3rem', width: '100%' }}>
                      <h4 title={book.title} style={{ flex: 1, minWidth: 0 }}>{book.title}</h4>
                      {book.rating > 0 && (
                        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f59e0b', whiteSpace: 'nowrap', flexShrink: 0 }} title={`Valoración: ${book.rating} (${book.reviews_count || 1})`}>
                          ⭐ {book.rating.toFixed(1)}
                        </span>
                      )}
                    </div>
                    <h5 className="book-card-back-author" title={book.author}>{book.author}</h5>
                    <div className="book-card-divider"></div>
                    {book.tags && (
                      <div 
                        style={{ 
                          fontSize: '0.72rem', 
                          color: isAdultTag(book.tags) ? '#f472b6' : '#60a5fa', 
                          fontWeight: isAdultTag(book.tags) ? 600 : 'normal',
                          marginBottom: '0.35rem', 
                          whiteSpace: 'nowrap', 
                          overflow: 'hidden', 
                          textOverflow: 'ellipsis' 
                        }} 
                        title={book.tags}
                      >
                        {isAdultTag(book.tags) ? '🔞 ' : '🏷️ '}{book.tags}
                      </div>
                    )}
                    <p style={{ flex: 1, minHeight: 0, overflowY: 'auto', margin: '0.1rem 0', wordBreak: 'break-word', hyphens: 'auto' }}>
                      {book.description && book.description !== "" ? book.description : "Sin descripción o resumen disponible para este EPUB."}
                    </p>
                    
                    {/* Botones de acción: Fila 1 (Leer/Ojo ancho completo) y Fila 2 (Valorar y Descargar) */}
                    <div style={{ marginTop: 'auto', width: '100%', display: 'flex', flexDirection: 'column', gap: '0.3rem', paddingTop: '0.3rem', flexShrink: 0 }}>
                      {/* Fila 1: Ojo que ocupa todo el ancho */}
                      <button 
                        className="btn-open-epub" 
                        style={{ width: '100%', margin: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.35rem', padding: '0.42rem 0.4rem', borderRadius: 'var(--radius-sm)' }} 
                        onClick={(e) => { e.stopPropagation(); startReading(book); }}
                        title="Leer libro"
                      >
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                          <circle cx="12" cy="12" r="3" />
                        </svg>
                        <span style={{ fontSize: '0.78rem', fontWeight: 600 }}>Leer</span>
                      </button>

                      {/* Fila 2: Valorar y Descargar en dos columnas */}
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.3rem', width: '100%' }}>
                        <button 
                          className="btn-secondary" 
                          style={{ width: '100%', margin: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '0.4rem 0.2rem', borderRadius: 'var(--radius-sm)', color: '#f59e0b', borderColor: 'rgba(245, 158, 11, 0.4)' }} 
                          onClick={(e) => {
                            e.stopPropagation();
                            if (!authStatus.authenticated) {
                              setAuthModalMessage('Debes iniciar sesión para valorar libros y compartir tu opinión.');
                              setShowAuthModal(true);
                              return;
                            }
                            openReviewsModal(book, e);
                          }}
                          title="Valorar libro"
                        >
                          <svg width="17" height="17" viewBox="0 0 24 24" fill="#f59e0b" stroke="#f59e0b" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                          </svg>
                        </button>

                        <button 
                          className="btn-secondary" 
                          style={{ width: '100%', margin: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '0.4rem 0.2rem', borderRadius: 'var(--radius-sm)', color: 'var(--accent-hover)', backgroundColor: 'rgba(99, 102, 241, 0.12)', borderColor: 'var(--accent-color)' }} 
                          onClick={async (e) => { 
                            e.stopPropagation(); 
                            if (!authStatus.authenticated) {
                              setAuthModalMessage('Debes iniciar sesión para poder descargar libros.');
                              setShowAuthModal(true);
                              return;
                            }

                            const safeTitle = (book.title || 'libro').replace(/[\\/*?:"<>|]/g, '').trim();
                            const safeAuthor = (book.author || '').replace(/[\\/*?:"<>|]/g, '').trim();
                            const isPdf = book.format === 'pdf' || (book.file_path && book.file_path.toLowerCase().endsWith('.pdf'));
                            const fileExt = isPdf ? '.pdf' : '.epub';
                            const filename = safeAuthor ? `${safeAuthor} - ${safeTitle}${fileExt}` : `${safeTitle}${fileExt}`;
                            const downloadUrl = `http://${window.location.hostname}:8000/api/download/${book.id}?is_download=1${authToken ? `&token=${authToken}` : ''}`;

                            try {
                              const res = await fetch(downloadUrl, {
                                headers: authToken ? { 'Authorization': `Bearer ${authToken}` } : {}
                              });

                              if (!res.ok) {
                                const errData = await res.json().catch(() => ({}));
                                const errMsg = errData.detail || "No se ha podido descargar el archivo.";
                                setDownloadToast({
                                  text: errMsg,
                                  type: 'error'
                                });
                                setTimeout(() => setDownloadToast(null), 5000);
                                return;
                              }

                              const blob = await res.blob();
                              const blobUrl = window.URL.createObjectURL(blob);
                              const a = document.createElement('a');
                              a.href = blobUrl;
                              a.download = filename;
                              document.body.appendChild(a);
                              a.click();
                              document.body.removeChild(a);
                              window.URL.revokeObjectURL(blobUrl);

                              // Mensaje de éxito informando de la descarga
                              setDownloadToast({
                                text: `📥 Libro descargado en tu equipo: "${book.title}"`,
                                type: 'success'
                              });
                              setTimeout(() => setDownloadToast(null), 3500);
                            } catch {
                              setDownloadToast({
                                text: "Error de red al intentar descargar el libro.",
                                type: 'error'
                              });
                              setTimeout(() => setDownloadToast(null), 4000);
                            }
                          }}
                          title={`Descargar archivo ${book.format === 'pdf' ? '.PDF' : '.EPUB'}`}
                        >
                          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                            <polyline points="7 10 12 15 17 10" />
                            <line x1="12" y1="15" x2="12" y2="3" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* MODAL: AUTENTICACIÓN (LOGIN Y AUTO-REGISTRO) */}
      <div 
        className={`modal-overlay ${showAuthModal ? 'open' : ''}`}
        onClick={(e) => { if (e.target === e.currentTarget) setShowAuthModal(false); }}
      >
        <div className="modal-content">
          <div className="auth-tabs">
            <button 
              className={`auth-tab ${authTab === 'login' ? 'active' : ''}`}
              onClick={() => { setAuthTab('login'); setAuthMessage({ text: '', type: '' }); }}
            >
              Iniciar Sesión
            </button>
            <button 
              className={`auth-tab ${authTab === 'register' ? 'active' : ''}`}
              onClick={() => { setAuthTab('register'); setAuthMessage({ text: '', type: '' }); }}
            >
              Auto-registrarse
            </button>
            <button 
              className={`auth-tab ${authTab === 'forgot' ? 'active' : ''}`}
              onClick={() => { setAuthTab('forgot'); setAuthMessage({ text: '', type: '' }); }}
            >
              Recuperar Clave
            </button>
          </div>

          {authMessage.text && (
            <div className={`auth-alert ${authMessage.type}`}>
              {authMessage.text}
            </div>
          )}

          {authTab === 'login' ? (
            <form onSubmit={handleLogin}>
              <div className="form-group">
                <label>Usuario</label>
                <input 
                  type="text" 
                  required
                  placeholder="Tu nombre de usuario o email"
                  value={authForm.username}
                  onChange={(e) => setAuthForm({ ...authForm, username: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Contraseña</label>
                <input 
                  type="password" 
                  required
                  placeholder="Tu contraseña"
                  value={authForm.password}
                  onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
                />
              </div>
              <div style={{ textAlign: 'right', marginTop: '-0.25rem', marginBottom: '0.75rem' }}>
                <button 
                  type="button" 
                  style={{ background: 'none', border: 'none', color: 'var(--accent-hover)', fontSize: '0.82rem', cursor: 'pointer', textDecoration: 'underline' }}
                  onClick={() => { setAuthTab('forgot'); setAuthMessage({ text: '', type: '' }); }}
                >
                  ¿Has olvidado tu contraseña?
                </button>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowAuthModal(false)}>Cancelar</button>
                <button type="submit" className="btn-primary">Entrar</button>
              </div>
            </form>
          ) : authTab === 'forgot' ? (
            <form onSubmit={handleResetWithKey}>
              <div className="auth-alert info" style={{ fontSize: '0.82rem', lineHeight: '1.4' }}>
                <p style={{ margin: '0 0 0.5rem 0' }}>
                  🛡️ <strong>Administrador Master:</strong> Puedes restablecer tu clave introduciendo la <em>Clave de Recuperación del Servidor</em> que encontrarás en tu equipo en el archivo <code>Documents\Epubbiblio\recovery_key.txt</code>.
                </p>
                <p style={{ margin: 0 }}>
                  👤 <strong>Lectores:</strong> Si no tienes acceso a la máquina, solicita a tu Administrador Master que te asigne una nueva clave desde el panel de control.
                </p>
              </div>
              <div className="form-group">
                <label>Usuario / Email a restablecer</label>
                <input 
                  type="text" 
                  required
                  placeholder="Ej: ossoney@yahoo.es"
                  value={forgotForm.username}
                  onChange={(e) => setForgotForm({ ...forgotForm, username: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Clave de Recuperación del Servidor</label>
                <input 
                  type="text" 
                  required
                  placeholder="Ej: EPUB-XXXX-XXXX-XXXX"
                  value={forgotForm.recoveryKey}
                  onChange={(e) => setForgotForm({ ...forgotForm, recoveryKey: e.target.value.toUpperCase() })}
                />
                <small style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                  Ubicación: <code>%USERPROFILE%\Documents\Epubbiblio\recovery_key.txt</code>
                </small>
              </div>
              <div className="form-group">
                <label>Nueva Contraseña</label>
                <input 
                  type="password" 
                  required
                  placeholder="Mínimo 4 caracteres"
                  value={forgotForm.newPassword}
                  onChange={(e) => setForgotForm({ ...forgotForm, newPassword: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Confirmar Nueva Contraseña</label>
                <input 
                  type="password" 
                  required
                  placeholder="Repite la nueva contraseña"
                  value={forgotForm.confirmPassword}
                  onChange={(e) => setForgotForm({ ...forgotForm, confirmPassword: e.target.value })}
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => { setAuthTab('login'); setAuthMessage({ text: '', type: '' }); }}>
                  Volver al Login
                </button>
                <button type="submit" className="btn-primary">Restablecer Clave</button>
              </div>
            </form>
          ) : (
            <form onSubmit={handleRegister}>
              <div className="auth-alert info">
                📝 Las nuevas cuentas se crean en modo <strong>pendiente de aprobación</strong>. Podrás acceder tan pronto el Administrador Master active tu usuario.
              </div>
              <div className="form-group">
                <label>Usuario deseado</label>
                <input 
                  type="text" 
                  required
                  placeholder="Mínimo 3 caracteres"
                  value={authForm.username}
                  onChange={(e) => setAuthForm({ ...authForm, username: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Contraseña</label>
                <input 
                  type="password" 
                  required
                  placeholder="Mínimo 4 caracteres"
                  value={authForm.password}
                  onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Confirmar contraseña</label>
                <input 
                  type="password" 
                  required
                  placeholder="Repite la contraseña"
                  value={authForm.confirmPassword}
                  onChange={(e) => setAuthForm({ ...authForm, confirmPassword: e.target.value })}
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowAuthModal(false)}>Cancelar</button>
                <button type="submit" className="btn-primary">Solicitar Registro</button>
              </div>
            </form>
          )}
        </div>
      </div>

      {/* MODAL: ASISTENTE DE PRIMER ARRANQUE (CREACIÓN DEL MASTER) */}
      <div className={`modal-overlay ${showMasterWizard ? 'open' : ''}`}>
        <div className="modal-content">
          <h2>👑 Configuración Inicial: Administrador Master</h2>
          <p style={{ color: 'var(--text-muted)', marginBottom: '1.25rem', fontSize: '0.9rem', lineHeight: '1.4' }}>
            No se ha detectado ningún Administrador Master. Crea tu cuenta principal para gestionar la biblioteca, asignar bibliotecas y aprobar a los futuros lectores.
          </p>
          {authMessage.text && (
            <div className={`auth-alert ${authMessage.type}`}>
              {authMessage.text}
            </div>
          )}
          <form onSubmit={handleRegisterMaster}>
            <div className="form-group">
              <label>Usuario Master</label>
              <input 
                type="text" 
                required
                placeholder="Ej: admin"
                value={authForm.username}
                onChange={(e) => setAuthForm({ ...authForm, username: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Contraseña</label>
              <input 
                type="password" 
                required
                placeholder="Contraseña segura"
                value={authForm.password}
                onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Confirmar Contraseña</label>
              <input 
                type="password" 
                required
                placeholder="Repite la contraseña"
                value={authForm.confirmPassword}
                onChange={(e) => setAuthForm({ ...authForm, confirmPassword: e.target.value })}
              />
            </div>
            <div className="modal-actions">
              <button type="submit" className="btn-primary" style={{ width: '100%' }}>
                Crear Administrador Master e Iniciar
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* MODAL: PANEL DE ADMINISTRACIÓN MASTER */}
      <div 
        className={`modal-overlay ${showAdminModal ? 'open' : ''}`}
        onClick={(e) => { if (e.target === e.currentTarget) setShowAdminModal(false); }}
      >
        <div className="modal-content admin-modal-content">
          <div className="admin-modal-header">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h2 style={{ margin: 0 }}>👑 Panel de Control Master</h2>
              <button 
                className="btn-secondary" 
                style={{ padding: '0.35rem 0.85rem', fontSize: '1.1rem', lineHeight: 1 }} 
                onClick={() => setShowAdminModal(false)}
                title="Cerrar ventana (ESC)"
              >
                ✕
              </button>
            </div>

            <div className="auth-tabs" style={{ marginBottom: '0.25rem' }}>
              <button 
                className={`auth-tab ${adminTab === 'users' ? 'active' : ''}`}
                onClick={() => setAdminTab('users')}
              >
                👥 Usuarios {pendingUsersCount > 0 && `(${pendingUsersCount} pendientes)`}
              </button>
              <button 
                className={`auth-tab ${adminTab === 'libraries' ? 'active' : ''}`}
                onClick={() => setAdminTab('libraries')}
              >
                🏛️ Bibliotecas ({libraries.length})
              </button>
              <button 
                className={`auth-tab ${adminTab === 'maintenance' ? 'active' : ''}`}
                onClick={() => setAdminTab('maintenance')}
              >
                ⚙️ Mantenimiento Global
              </button>
              <button 
                className={`auth-tab ${adminTab === 'reports' ? 'active' : ''}`}
                onClick={() => { setAdminTab('reports'); loadAdminReports(); }}
                style={{ position: 'relative' }}
              >
                🚨 Incidencias {adminReports.length > 0 && `(${adminReports.length})`}
              </button>
            </div>
          </div>

          <div className="admin-modal-body">
            {/* Pestaña 1: Usuarios */}
            {adminTab === 'users' && (
              <div>
                {adminLoading ? (
                  <div style={{ textAlign: 'center', padding: '2rem' }}><div className="loader"></div></div>
                ) : adminUsers.length === 0 ? (
                  <p style={{ color: 'var(--text-muted)' }}>No hay usuarios registrados en el sistema.</p>
                ) : (
                  <div style={{ overflowX: 'auto', maxHeight: '400px' }}>
                    <table className="admin-table">
                      <thead>
                        <tr>
                          <th>Usuario</th>
                          <th>Rol</th>
                          <th>Estado</th>
                          <th>Bibliotecas</th>
                          <th>Descargas</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>
                      <tbody>
                        {adminUsers.map(u => (
                          <tr key={u.id}>
                            <td style={{ fontWeight: 600 }}>{u.username}</td>
                            <td>
                              <button 
                                className={`role-badge ${u.role}`}
                                style={{ cursor: u.id === authStatus.user?.id ? 'default' : 'pointer', border: 'none' }}
                                onClick={() => u.id !== authStatus.user?.id && handleToggleRole(u.id, u.role)}
                                title={u.id === authStatus.user?.id ? "No puedes cambiar tu propio rol" : "Clic para alternar Master/Lector"}
                              >
                                {u.role === 'master' ? '👑 Master' : 'Lector'}
                              </button>
                            </td>
                            <td>
                              <span className={`role-badge ${u.status}`}>
                                {u.status === 'active' ? 'Activo' : u.status === 'pending' ? '⏳ Pendiente' : 'Rechazado'}
                              </span>
                            </td>
                            <td>
                              {u.role === 'master' ? (
                                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Acceso total</span>
                              ) : (
                                <button 
                                  className="btn-action-sm btn-lib"
                                  onClick={() => openUserLibrariesModal(u)}
                                  title="Asignar qué bibliotecas puede ver este lector"
                                >
                                  🏛️ {(u.assigned_libraries || []).length} asignadas
                                </button>
                              )}
                            </td>
                            <td>
                              {u.role === 'master' ? (
                                <span style={{ fontSize: '0.8rem', color: '#10b981', fontWeight: 600 }}>
                                  ♾️ Ilimitado
                                </span>
                              ) : (
                                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}>
                                  <span style={{ 
                                    fontSize: '0.8rem', 
                                    color: ((u.daily_download_limit !== null && u.daily_download_limit !== undefined ? (u.downloads_today || 0) >= u.daily_download_limit : false)) ? '#f87171' : 'var(--text-muted)' 
                                  }}>
                                    📥 <strong>{u.downloads_today ?? u.downloads_this_week ?? 0}</strong>/{u.daily_download_limit !== null && u.daily_download_limit !== undefined ? `${u.daily_download_limit}/día` : (u.weekly_download_limit !== null && u.weekly_download_limit !== undefined ? `${u.weekly_download_limit}/día` : '∞')}
                                  </span>
                                  <button 
                                    className="btn-action-sm" 
                                    style={{ padding: '0.2rem 0.4rem', fontSize: '0.72rem', background: 'rgba(255,255,255,0.06)', border: '1px solid var(--border-color)', color: 'var(--text-main)' }}
                                    onClick={() => handleEditDownloadLimit(u)}
                                    title="Modificar límite diario de descargas para este usuario"
                                  >
                                    ✏️
                                  </button>
                                </div>
                              )}
                            </td>
                            <td>
                              <button 
                                className="btn-action-sm" 
                                style={{ background: '#3b82f6', color: '#fff', border: 'none' }}
                                onClick={() => handleAdminResetPassword(u)} 
                                title="Restablecer o cambiar la contraseña de este usuario"
                              >
                                🔑 Clave
                              </button>
                              {u.status === 'pending' && (
                                <button className="btn-action-sm btn-approve" onClick={() => handleApproveUser(u.id)}>
                                  Aprobar
                                </button>
                              )}
                              {u.status === 'active' && u.id !== authStatus.user?.id && (
                                <button 
                                  className="btn-action-sm" 
                                  style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24', border: '1px solid rgba(245, 158, 11, 0.3)' }}
                                  onClick={() => handleForceLogoutUser(u)}
                                  title="Cerrar las sesiones activas de este usuario"
                                >
                                  🚪 Cerrar sesión
                                </button>
                              )}
                              {u.status === 'active' && u.id !== authStatus.user?.id && (
                                <button className="btn-action-sm btn-reject" onClick={() => handleRejectUser(u.id)}>
                                  Suspender
                                </button>
                              )}
                              {u.status === 'rejected' && (
                                <button className="btn-action-sm btn-approve" onClick={() => handleApproveUser(u.id)}>
                                  Reactivar
                                </button>
                              )}
                              {u.id !== authStatus.user?.id && (
                                <button className="btn-action-sm btn-delete" onClick={() => handleDeleteUser(u.id)}>
                                  Borrar
                                </button>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
                <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                  <button className="btn-secondary" onClick={() => setShowAdminModal(false)}>
                    Cerrar Panel
                  </button>
                </div>
              </div>
            )}

            {/* Pestaña 2: Bibliotecas (Multi-Library) */}
            {adminTab === 'libraries' && (
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                  <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    Crea y gestiona colecciones separadas para tus lectores.
                  </p>
                  <button 
                    className="btn-primary" 
                    style={{ fontSize: '0.85rem', padding: '0.5rem 1rem' }}
                    onClick={() => setShowCreateLibModal(true)}
                  >
                    + Nueva Biblioteca
                  </button>
                </div>

                <div className="library-grid-admin">
                  {libraries.map(lib => {
                    const adult = isAdultTheme(lib.name)
                    return (
                      <div key={lib.id} className={`library-card-admin ${adult ? 'adult-theme-card' : ''}`}>
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                            <h4 style={{ color: adult ? '#f472b6' : undefined }}>
                              {adult ? '🔞' : '🏛️'} {lib.name}
                            </h4>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                              {adult && <span className="adult-pill">🔞 +18</span>}
                              {lib.library_type === 'pdf' && (
                                <span style={{ fontSize: '0.72rem', background: 'rgba(239, 68, 68, 0.2)', color: '#f87171', border: '1px solid rgba(239, 68, 68, 0.4)', borderRadius: '4px', padding: '0.1rem 0.35rem', fontWeight: 600 }}>PDF</span>
                              )}
                              <span style={{ fontSize: '0.85rem', fontWeight: 700, color: adult ? '#f472b6' : 'var(--accent-hover)' }}>
                                {lib.book_count.toLocaleString()} libros
                              </span>
                            </div>
                          </div>
                          {lib.path ? (
                            <div className="library-path-admin">
                              📁 {lib.path}
                            </div>
                          ) : null}
                        </div>

                      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', alignItems: 'center' }}>
                        {(lib.path || lib.id === 1) ? (
                          <button 
                            className="btn-secondary" 
                            style={{ flex: 1, padding: '0.4rem', fontSize: '0.8rem' }}
                            onClick={() => handleScanLibrary(lib.id, lib.name, lib.path || (lib.id === 1 ? scanDirectory : ''))}
                            title="Escanear carpeta física en busca de nuevos libros"
                          >
                            ⚡ Escanear
                          </button>
                        ) : (
                          <div style={{ flex: 1, fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', opacity: 0.8 }}>
                            🏷️ Colección temática
                          </div>
                        )}
                        {lib.id !== 1 && lib.id !== 2 && (
                          <button 
                            className="btn-action-sm btn-delete" 
                            style={{ padding: '0.4rem 0.8rem' }}
                            onClick={() => handleDeleteLibrary(lib.id, lib.name)}
                            title="Eliminar biblioteca y sus libros"
                          >
                            Eliminar
                          </button>
                        )}
                      </div>
                    </div>
                  )
                })}
                </div>

                <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                  <button className="btn-secondary" onClick={() => setShowAdminModal(false)}>
                    Cerrar Panel
                  </button>
                </div>
              </div>
            )}

            {/* Pestaña 3: Mantenimiento Global */}
            {adminTab === 'maintenance' && (
              <div>
                <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1.25rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', marginBottom: '1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <h3 style={{ fontSize: '1.1rem', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span>⚡</span> Escanear Directorio de EPUBs
                    </h3>
                    {scanStatus.running && (
                      <span className="badge" style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#34d399', border: '1px solid #10b981', fontSize: '0.75rem', padding: '0.2rem 0.5rem', borderRadius: '1rem' }}>
                        Escaneando...
                      </span>
                    )}
                  </div>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1rem' }}>
                    Introduce la ruta física del servidor para incorporar nuevos libros a la <strong>Biblioteca Principal</strong> en segundo plano sin interrumpir tu navegación.
                  </p>

                  {scanStatus.running ? (
                    <div style={{ background: 'rgba(0,0,0,0.25)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.5rem' }}>
                        <span>
                          {scanStatus.total_files > 0 
                            ? `Analizados: ${scanStatus.processed.toLocaleString()} de ${scanStatus.total_files.toLocaleString()} archivos`
                            : `Analizados: ${scanStatus.processed.toLocaleString()} archivos`}
                        </span>
                        <span style={{ color: '#34d399', fontWeight: 600 }}>
                          📚 +{scanStatus.new_books.toLocaleString()} nuevos incorporados
                        </span>
                      </div>
                      <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden', marginBottom: '0.6rem' }}>
                        <div 
                          style={{ 
                            width: `${scanStatus.total_files > 0 ? Math.min(100, Math.round((scanStatus.processed / scanStatus.total_files) * 100)) : 100}%`, 
                            height: '100%', 
                            background: 'linear-gradient(90deg, #10b981, #06b6d4)',
                            transition: 'width 0.3s ease'
                          }} 
                        />
                      </div>
                      {scanStatus.current_file && (
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', marginBottom: '0.75rem' }}>
                          Procesando: <em>{scanStatus.current_file}</em>
                        </div>
                      )}
                      <button 
                        className="btn-secondary" 
                        onClick={handleStopScan}
                        style={{ borderColor: '#ef4444', color: '#fca5a5', padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
                      >
                        {scanStatus.stop_requested ? 'Deteniendo...' : 'Detener Escaneo'}
                      </button>
                    </div>
                  ) : (
                    <div>
                      {scanStatus.last_result && (
                        <div style={{ marginBottom: '1rem', fontSize: '0.82rem', color: '#10b981', display: 'flex', alignItems: 'center', gap: '0.4rem', background: 'rgba(16,185,129,0.1)', padding: '0.5rem 0.75rem', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(16,185,129,0.2)' }}>
                          ✓ {scanStatus.last_result.stopped ? 'Escaneo detenido por el usuario:' : 'Último escaneo completado:'} {scanStatus.last_result.processed.toLocaleString()} archivos analizados ({scanStatus.last_result.new_books.toLocaleString()} libros nuevos añadidos).
                        </div>
                      )}
                      <input 
                        type="text" 
                        value={scanDirectory}
                        onChange={(e) => setScanDirectory(e.target.value)}
                        placeholder="Ej: C:\Epubs"
                        style={{ width: '100%', marginBottom: '1rem', padding: '0.75rem', borderRadius: 'var(--radius-sm)', background: 'var(--bg-color)', border: '1px solid var(--border-color)', color: 'white' }}
                      />
                      <button className="btn-primary" onClick={handleScanGlobal} style={{ width: '100%' }}>
                        Iniciar Escaneo en Biblioteca Principal
                      </button>
                    </div>
                  )}
                </div>

                {/* Sincronizar valoraciones desde Open Library */}
                <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1.25rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', marginBottom: '1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <h3 style={{ fontSize: '1.1rem', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span>🌐</span> Sincronizar valoraciones desde Open Library
                    </h3>
                    {ratingsSyncStatus.running && (
                      <span className="badge" style={{ background: 'rgba(59, 130, 246, 0.2)', color: '#60a5fa', border: '1px solid #3b82f6', fontSize: '0.75rem', padding: '0.2rem 0.5rem', borderRadius: '1rem' }}>
                        En ejecución...
                      </span>
                    )}
                  </div>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1rem', lineHeight: '1.4' }}>
                    Consulta automáticamente en segundo plano la base de datos libre de <strong>Open Library (Internet Archive)</strong> para rellenar las estrellas ⭐ de tu catálogo sin interferir mientras usas la biblioteca.
                  </p>

                  {ratingsSyncStatus.running ? (
                    <div style={{ background: 'rgba(0,0,0,0.25)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.5rem' }}>
                        <span>Analizados: <strong>{ratingsSyncStatus.processed}</strong> de {ratingsSyncStatus.total} libros</span>
                        <span style={{ color: '#f59e0b', fontWeight: 600 }}>⭐ {ratingsSyncStatus.found} notas asignadas</span>
                      </div>
                      <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden', marginBottom: '0.6rem' }}>
                        <div 
                          style={{ 
                            width: `${ratingsSyncStatus.total > 0 ? Math.min(100, Math.round((ratingsSyncStatus.processed / ratingsSyncStatus.total) * 100)) : 0}%`, 
                            height: '100%', 
                            background: 'linear-gradient(90deg, #3b82f6, #f59e0b)',
                            transition: 'width 0.3s ease'
                          }} 
                        />
                      </div>
                      {ratingsSyncStatus.current_book && (
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', marginBottom: '0.75rem' }}>
                          Buscando: <em>{ratingsSyncStatus.current_book}</em>
                        </div>
                      )}
                      <button 
                        className="btn-secondary" 
                        onClick={handleStopRatingsSync}
                        style={{ borderColor: '#ef4444', color: '#fca5a5', padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
                      >
                        {ratingsSyncStatus.stop_requested ? 'Deteniendo...' : 'Detener Sincronización'}
                      </button>
                    </div>
                  ) : (
                    <div>
                      {ratingsSyncStatus.processed > 0 && (
                        <div style={{ marginBottom: '1rem', fontSize: '0.82rem', color: '#10b981', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                          ✓ Sincronización finalizada: {ratingsSyncStatus.processed} libros analizados ({ratingsSyncStatus.found} con valoración encontrada).
                        </div>
                      )}
                      <button 
                        className="btn-primary" 
                        onClick={handleStartRatingsSync}
                        style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}
                      >
                        <span>⭐</span> Iniciar Sincronización en Segundo Plano
                      </button>
                    </div>
                  )}
                </div>

                <div style={{ background: 'rgba(239, 68, 68, 0.08)', padding: '1.25rem', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                  <h3 style={{ color: '#fca5a5', fontSize: '1.1rem', marginBottom: '0.5rem' }}>Zona de Peligro: Vaciar Catálogo</h3>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1rem' }}>
                    Esta acción borra el catálogo de la base de datos y las imágenes de portada generadas. Los archivos EPUB originales no se tocan.
                  </p>
                  <button className="btn-secondary" onClick={handleClearLibrary} style={{ borderColor: '#ef4444', color: '#fca5a5' }}>
                    Vaciar todo el Catálogo
                  </button>
                </div>

                <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                  <button className="btn-secondary" onClick={() => setShowAdminModal(false)}>
                    Cerrar Panel
                  </button>
                </div>
              </div>
            )}

            {/* Pestaña 4: Incidencias y Reportes */}
            {adminTab === 'reports' && (
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <div>
                    <h3 style={{ fontSize: '1.1rem', margin: 0 }}>🚨 Incidencias Reportadas por Lectores</h3>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', margin: '0.25rem 0 0' }}>
                      Revisa los avisos de géneros incorrectos o problemas comunicados por los usuarios.
                    </p>
                  </div>
                  <button 
                    className="btn-secondary" 
                    onClick={loadAdminReports} 
                    style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem' }}
                    disabled={loadingReports}
                  >
                    {loadingReports ? 'Actualizando...' : '🔄 Actualizar'}
                  </button>
                </div>

                {loadingReports ? (
                  <div style={{ textAlign: 'center', padding: '2rem 0' }}>
                    <div className="loader" style={{ margin: '0 auto 0.5rem' }}></div>
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Cargando incidencias...</span>
                  </div>
                ) : adminReports.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '3rem 1rem', background: 'rgba(255,255,255,0.02)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                    <span style={{ fontSize: '2rem', display: 'block', marginBottom: '0.5rem' }}>✨</span>
                    <h4 style={{ margin: '0 0 0.35rem', color: '#4ade80' }}>¡No hay incidencias pendientes!</h4>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', margin: 0 }}>
                      Tu biblioteca está en orden y sin avisos de fallos pendientes de revisar.
                    </p>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', maxHeight: '420px', overflowY: 'auto' }}>
                    {adminReports.map(rep => (
                      <div 
                        key={rep.id} 
                        style={{ 
                          background: 'rgba(255,255,255,0.03)', 
                          border: '1px solid rgba(239,68,68,0.3)', 
                          borderRadius: 'var(--radius-sm)', 
                          padding: '1rem',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '0.5rem'
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem' }}>
                          <div>
                            <span 
                              style={{ 
                                display: 'inline-block',
                                padding: '0.15rem 0.5rem', 
                                borderRadius: '1rem', 
                                fontSize: '0.72rem', 
                                fontWeight: 600,
                                background: rep.report_type === 'wrong_genre' ? 'rgba(239,68,68,0.15)' : 'rgba(245,158,11,0.15)',
                                color: rep.report_type === 'wrong_genre' ? '#f87171' : '#fbbf24',
                                border: `1px solid ${rep.report_type === 'wrong_genre' ? '#ef4444' : '#f59e0b'}`,
                                marginBottom: '0.35rem'
                              }}
                            >
                              {rep.report_type === 'wrong_genre' ? '🏷️ Género equivocado' : '⚠️ Otra incidencia'}
                            </span>
                            <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>
                              📖 {rep.book_title} <span style={{ color: 'var(--text-muted)', fontWeight: 400, fontSize: '0.82rem' }}>de {rep.book_author}</span>
                            </div>
                          </div>
                          <button 
                            className="btn-primary" 
                            onClick={() => handleMarkReportReviewed(rep.id)}
                            style={{ 
                              fontSize: '0.78rem', 
                              padding: '0.35rem 0.75rem', 
                              background: '#10b981', 
                              borderColor: '#10b981',
                              whiteSpace: 'nowrap'
                            }}
                            title="Marcar incidencia como revisada y resuelta"
                          >
                            ✓ Resolver
                          </button>
                        </div>

                        <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.65rem 0.8rem', borderRadius: 'var(--radius-sm)', fontSize: '0.85rem', color: '#f1f5f9', whiteSpace: 'pre-wrap' }}>
                          "{rep.message}"
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          <span>Reportado por: <strong>{rep.reported_by}</strong></span>
                          <span>{rep.created_at}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                  <button className="btn-secondary" onClick={() => setShowAdminModal(false)}>
                    Cerrar Panel
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* MINI-MODAL: CREAR BIBLIOTECA */}
      <div 
        className={`modal-overlay ${showCreateLibModal ? 'open' : ''}`}
        onClick={(e) => { if (e.target === e.currentTarget) setShowCreateLibModal(false); }}
      >
        <div className="modal-content" style={{ maxWidth: '450px' }}>
          <h3>🏛️ Crear Nueva Biblioteca</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
            Crea una biblioteca temática independiente para asignar a grupos específicos de usuarios.
          </p>
          <form onSubmit={handleCreateLibrary}>
            <div className="form-group">
              <label>Nombre de la Biblioteca</label>
              <input 
                type="text" 
                required
                placeholder="Ej: Ciencia Ficción, Cómics, Infantil..."
                value={newLibForm.name}
                onChange={(e) => setNewLibForm({ ...newLibForm, name: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Formato admitido</label>
              <select
                value={newLibForm.library_type || 'all'}
                onChange={(e) => setNewLibForm({ ...newLibForm, library_type: e.target.value })}
                style={{ width: '100%', padding: '0.6rem 0.8rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-main)' }}
              >
                <option value="all">Todos los formatos (EPUB y PDF)</option>
                <option value="pdf">Solo documentos PDF</option>
                <option value="epub">Solo libros EPUB</option>
              </select>
            </div>
            <div className="form-group">
              <label>Ruta de Carpeta en Disco (Opcional)</label>
              <input 
                type="text" 
                placeholder="Ej: C:\Users\OscarSson\Videos\Epub\SciFi"
                value={newLibForm.path}
                onChange={(e) => setNewLibForm({ ...newLibForm, path: e.target.value })}
              />
            </div>
            <div className="modal-actions">
              <button type="button" className="btn-secondary" onClick={() => setShowCreateLibModal(false)}>Cancelar</button>
              <button type="submit" className="btn-primary">Crear Biblioteca</button>
            </div>
          </form>
        </div>
      </div>

      {/* MINI-MODAL: ASIGNAR BIBLIOTECAS A USUARIO */}
      <div 
        className={`modal-overlay ${userLibModal.open ? 'open' : ''}`}
        onClick={(e) => { if (e.target === e.currentTarget) setUserLibModal({ open: false, user: null, selectedIds: [] }); }}
      >
        <div className="modal-content" style={{ maxWidth: '450px' }}>
          <h3>🏛️ Asignar Bibliotecas</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
            Selecciona qué bibliotecas tiene permitido consultar el lector <strong>{userLibModal.user?.username}</strong>:
          </p>

          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.8rem' }}>
            <button 
              type="button" 
              className="btn-secondary" 
              style={{ fontSize: '0.78rem', padding: '0.3rem 0.6rem' }}
              onClick={() => setUserLibModal(prev => ({ ...prev, selectedIds: libraries.map(l => l.id) }))}
            >
              ✓ Marcar todas
            </button>
            <button 
              type="button" 
              className="btn-secondary" 
              style={{ fontSize: '0.78rem', padding: '0.3rem 0.6rem' }}
              onClick={() => setUserLibModal(prev => ({ ...prev, selectedIds: [] }))}
            >
              ✕ Desmarcar todas
            </button>
          </div>

          <div style={{ maxHeight: '340px', overflowY: 'auto', marginBottom: '1.5rem', paddingRight: '0.25rem' }}>
            {libraries.map(lib => {
              const adult = isAdultTheme(lib.name)
              return (
                <label 
                  key={lib.id} 
                  className="checkbox-row" 
                  style={{
                    borderColor: adult ? 'rgba(236, 72, 153, 0.45)' : undefined,
                    background: adult ? 'rgba(236, 72, 153, 0.08)' : undefined
                  }}
                >
                  <input 
                    type="checkbox" 
                    checked={userLibModal.selectedIds.includes(lib.id)}
                    onChange={() => toggleUserLibraryCheckbox(lib.id)}
                    style={{ accentColor: adult ? '#ec4899' : undefined }}
                  />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem', color: adult ? '#f472b6' : 'inherit', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <span>{adult ? '🔞' : '🏛️'} {lib.name}</span>
                      {adult && <span className="adult-pill" style={{ fontSize: '0.65rem', padding: '0.1rem 0.35rem' }}>+18</span>}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: adult ? '#fbcfe8' : 'var(--text-muted)' }}>
                      {lib.book_count.toLocaleString()} libros
                    </div>
                  </div>
                </label>
              )
            })}
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={() => setUserLibModal({ open: false, user: null, selectedIds: [] })}>
              Cancelar
            </button>
            <button type="button" className="btn-primary" onClick={handleSaveUserLibraries}>
              Guardar Asignaciones
            </button>
          </div>
        </div>
      </div>

      {/* MODAL: OPINIONES Y RESEÑAS */}
      <div 
        className={`modal-overlay ${selectedBookForReviews ? 'open' : ''}`}
        onClick={(e) => { if (e.target === e.currentTarget) setSelectedBookForReviews(null); }}
      >
        <div className="modal-content" style={{ maxWidth: '600px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div>
              <h2 style={{ fontSize: '1.25rem', margin: 0 }}>{selectedBookForReviews?.title}</h2>
              <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '0.85rem' }}>{selectedBookForReviews?.author}</p>
            </div>
            <button className="btn-secondary" style={{ padding: '0.3rem 0.8rem' }} onClick={() => setSelectedBookForReviews(null)}>✕</button>
          </div>

          {/* Resumen de valoración */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginBottom: '1.25rem', background: 'rgba(255,255,255,0.03)', padding: '0.75rem 1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ fontSize: '1.5rem', fontWeight: 700, color: '#f59e0b' }}>
                  ⭐ {reviewsData.average_rating > 0 ? reviewsData.average_rating : '-'}
                </span>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                  ({reviewsData.total_reviews} {reviewsData.total_reviews === 1 ? 'opinión' : 'opiniones'})
                </span>
                {reviewsData.source && reviewsData.source !== "Sin valorar" && (
                  <span style={{ 
                    fontSize: '0.75rem', 
                    padding: '0.2rem 0.5rem', 
                    borderRadius: '12px', 
                    background: reviewsData.source === 'Comunidad' ? 'rgba(56, 189, 248, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                    color: reviewsData.source === 'Comunidad' ? '#38bdf8' : '#fbbf24',
                    fontWeight: 600
                  }}>
                    {reviewsData.source}
                  </span>
                )}
              </div>
              <button
                type="button"
                className="btn-secondary"
                style={{ fontSize: '0.75rem', padding: '0.35rem 0.7rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}
                title="Consultar o actualizar valoración en Open Library"
                disabled={syncingBookRating}
                onClick={handleSyncSingleBookRating}
              >
                {syncingBookRating ? 'Buscando...' : '🔄 Consultar Open Library'}
              </button>
            </div>

            {syncFeedback && (
              <div style={{
                padding: '0.45rem 0.75rem',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.8rem',
                background: syncFeedback.status === 'found' ? 'rgba(34, 197, 94, 0.15)' : (syncFeedback.status === 'error' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(148, 163, 184, 0.12)'),
                color: syncFeedback.status === 'found' ? '#4ade80' : (syncFeedback.status === 'error' ? '#f87171' : '#cbd5e1'),
                border: `1px solid ${syncFeedback.status === 'found' ? '#22c55e' : (syncFeedback.status === 'error' ? '#ef4444' : 'var(--border-color)')}`
              }}>
                {syncFeedback.message}
              </div>
            )}
          </div>

          {/* Formulario para añadir/editar opinión */}
          {authStatus.authenticated ? (
            <form onSubmit={handleSaveReview} style={{ marginBottom: '1.5rem', background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Tu Valoración:</label>
                <div className="star-rating" style={{ display: 'flex', gap: '6px', alignItems: 'center', cursor: 'pointer' }}>
                  {[1, 2, 3, 4, 5].map(star => {
                    const activeRating = hoverRating || reviewInput.rating;
                    const isSelected = star <= activeRating;
                    return (
                      <span 
                        key={star} 
                        className="star-interactive"
                        style={{ 
                          fontSize: '1.5rem', 
                          color: isSelected ? '#f59e0b' : 'rgba(255,255,255,0.25)', 
                          cursor: 'pointer',
                          transition: 'transform 0.1s ease, color 0.15s ease',
                          transform: hoverRating === star ? 'scale(1.2)' : 'scale(1)',
                          userSelect: 'none'
                        }}
                        onMouseEnter={() => setHoverRating(star)}
                        onMouseLeave={() => setHoverRating(0)}
                        onClick={() => setReviewInput(prev => ({ ...prev, rating: star }))}
                        title={`${star} estrella${star > 1 ? 's' : ''}`}
                      >
                        {isSelected ? '★' : '☆'}
                      </span>
                    );
                  })}
                  {reviewInput.rating > 0 && (
                    <span style={{ fontSize: '0.8rem', color: '#f59e0b', fontWeight: 600, marginLeft: '0.4rem' }}>
                      {reviewInput.rating}/5
                    </span>
                  )}
                </div>
              </div>
              <textarea 
                rows="3" 
                placeholder="Escribe tu opinión personal o reseña sobre este libro..."
                value={reviewInput.comment}
                onChange={(e) => setReviewInput({ ...reviewInput, comment: e.target.value })}
                style={{ width: '100%', padding: '0.75rem', borderRadius: 'var(--radius-sm)', background: 'var(--bg-color)', border: '1px solid var(--border-color)', color: 'white', fontFamily: 'inherit', resize: 'vertical' }}
              />
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', marginTop: '0.5rem' }}>
                {reviewsData.reviews.some(r => r.user_id === authStatus.user?.id) && (
                  <button type="button" className="btn-secondary" onClick={handleDeleteReview} style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem' }}>
                    Borrar mi reseña
                  </button>
                )}
                <button type="submit" className="btn-primary" disabled={savingReview} style={{ fontSize: '0.8rem', padding: '0.4rem 1rem' }}>
                  {savingReview ? 'Guardando...' : 'Publicar Reseña'}
                </button>
              </div>
            </form>
          ) : (
            <div className="auth-alert info" style={{ marginBottom: '1.5rem', cursor: 'pointer' }} onClick={() => setShowAuthModal(true)}>
              🔒 <strong>Inicia sesión</strong> para valorar este libro y compartir tu opinión con la comunidad.
            </div>
          )}

          {/* Lista de Reseñas */}
          <div style={{ maxHeight: '250px', overflowY: 'auto' }}>
            {reviewsData.reviews.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', textAlign: 'center', margin: '1rem 0' }}>
                Aún no hay opiniones para este libro. ¡Sé el primero en opinar!
              </p>
            ) : (
              reviewsData.reviews.map(rev => (
                <div key={rev.id} className="review-item">
                  <div className="review-header">
                    <span className="review-author">{rev.username}</span>
                    <div>
                      <span style={{ color: '#f59e0b', marginRight: '0.5rem' }}>
                        {'★'.repeat(rev.rating)}{'☆'.repeat(5 - rev.rating)}
                      </span>
                      <span className="review-date">{rev.updated_at}</span>
                    </div>
                  </div>
                  {rev.comment && <p className="review-comment">{rev.comment}</p>}
                </div>
              ))
            )}
          </div>

          {/* Sección: Reportar incidencia */}
          <div style={{ marginTop: '1.25rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
            {reportFeedback && (
              <div style={{
                marginBottom: '0.75rem', padding: '0.5rem 0.8rem',
                borderRadius: 'var(--radius-sm)', fontSize: '0.82rem',
                background: reportFeedback.ok ? 'rgba(34,197,94,0.12)' : 'rgba(239,68,68,0.12)',
                color: reportFeedback.ok ? '#4ade80' : '#f87171',
                border: `1px solid ${reportFeedback.ok ? '#22c55e' : '#ef4444'}`
              }}>
                {reportFeedback.message}
              </div>
            )}
            {!showReportForm ? (
              <button 
                type="button"
                onClick={() => { setShowReportForm(true); setReportFeedback(null); }}
                style={{ 
                  background: 'none', 
                  border: '1px dashed rgba(239,68,68,0.4)', 
                  color: '#fca5a5',
                  borderRadius: 'var(--radius-sm)', 
                  padding: '0.5rem 0.9rem', 
                  fontSize: '0.8rem',
                  cursor: 'pointer', 
                  width: '100%', 
                  textAlign: 'left',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}
              >
                <span>🚨</span>
                <span>Si detectas que el libro no pertenece al género o cualquier otra incidencia, explícamelo e intentaré subsanarlo cuanto antes</span>
              </button>
            ) : (
              <form onSubmit={handleSendReport} style={{ background: 'rgba(239,68,68,0.05)', border: '1px solid rgba(239,68,68,0.25)', borderRadius: 'var(--radius-sm)', padding: '0.9rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.6rem' }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#fca5a5' }}>🚨 Reportar incidencia de este libro</span>
                  <button type="button" onClick={() => setShowReportForm(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '1rem', lineHeight: 1 }}>✕</button>
                </div>
                <select 
                  value={reportInput.report_type} 
                  onChange={e => setReportInput(p => ({ ...p, report_type: e.target.value }))}
                  style={{ width: '100%', marginBottom: '0.6rem', padding: '0.5rem 0.6rem', borderRadius: 'var(--radius-sm)', background: 'var(--bg-color)', border: '1px solid var(--border-color)', color: 'white', fontSize: '0.82rem' }}
                >
                  <option value="wrong_genre">Libro en el género equivocado</option>
                  <option value="other">Cualquier otra incidencia (datos erróneos, portada, etc.)</option>
                </select>
                <textarea 
                  rows={3} 
                  required 
                  placeholder="Explícame la incidencia e intentaré subsanarla cuanto antes…"
                  value={reportInput.message} 
                  onChange={e => setReportInput(p => ({ ...p, message: e.target.value }))}
                  style={{ width: '100%', padding: '0.6rem 0.75rem', borderRadius: 'var(--radius-sm)', background: 'var(--bg-color)', border: '1px solid var(--border-color)', color: 'white', fontFamily: 'inherit', resize: 'vertical', fontSize: '0.82rem' }}
                />
                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', marginTop: '0.6rem' }}>
                  <button type="button" className="btn-secondary" style={{ fontSize: '0.78rem', padding: '0.35rem 0.75rem' }} onClick={() => setShowReportForm(false)}>
                    Cancelar
                  </button>
                  <button type="submit" className="btn-primary" disabled={sendingReport || !reportInput.message.trim()} style={{ fontSize: '0.78rem', padding: '0.35rem 0.9rem', background: '#dc2626', borderColor: '#dc2626' }}>
                    {sendingReport ? 'Enviando...' : 'Enviar incidencia'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer style={{ marginTop: '4rem', paddingTop: '2rem', borderTop: '1px solid var(--border-color)', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        <p style={{ marginBottom: '0.5rem' }}>Epub Biblio es un programa freeware que organiza visualmente tus archivos EPUB. Los archivos originales se mantienen.</p>
        <p>Si el programa te ha sido útil invítame a un café en <a href="https://paypal.me/ossoney" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-color)', textDecoration: 'none' }}>paypal.me/ossoney</a>. Envíame 1$ - 2$ - 3$ o lo que te apetezca.</p>
      </footer>

      {/* MODAL: CAMBIAR MI CONTRASEÑA */}
      <div className={`modal-overlay ${showChangePassModal ? 'open' : ''}`}>
        <div className="modal-content" style={{ maxWidth: '400px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <h2 style={{ fontSize: '1.2rem', margin: 0 }}>🔑 Cambiar Mi Contraseña</h2>
            <button className="btn-secondary" style={{ padding: '0.2rem 0.6rem' }} onClick={() => setShowChangePassModal(false)}>✕</button>
          </div>

          {changePassMessage.text && (
            <div className={`auth-alert ${changePassMessage.type}`}>
              {changePassMessage.text}
            </div>
          )}

          <form onSubmit={handleChangeMyPassword}>
            <div className="form-group">
              <label>Contraseña Actual</label>
              <input 
                type="password" 
                required
                placeholder="Tu contraseña actual"
                value={changePassForm.currentPassword}
                onChange={(e) => setChangePassForm({ ...changePassForm, currentPassword: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Nueva Contraseña</label>
              <input 
                type="password" 
                required
                placeholder="Mínimo 4 caracteres"
                value={changePassForm.newPassword}
                onChange={(e) => setChangePassForm({ ...changePassForm, newPassword: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Confirmar Nueva Contraseña</label>
              <input 
                type="password" 
                required
                placeholder="Repite la nueva contraseña"
                value={changePassForm.confirmPassword}
                onChange={(e) => setChangePassForm({ ...changePassForm, confirmPassword: e.target.value })}
              />
            </div>
            <div className="modal-actions">
              <button type="button" className="btn-secondary" onClick={() => setShowChangePassModal(false)}>Cancelar</button>
              <button type="submit" className="btn-primary">Guardar Nueva Clave</button>
            </div>
          </form>
        </div>
      </div>

      {/* NOTIFICACIÓN FLOTANTE DE DESCARGA Y LÍMITE */}
      {downloadToast && (
        <div style={{
          position: 'fixed',
          bottom: '2rem',
          left: '50%',
          transform: 'translateX(-50%)',
          backgroundColor: (typeof downloadToast === 'object' && downloadToast.type === 'error') ? '#dc2626' : '#10b981',
          color: '#ffffff',
          padding: '0.85rem 1.75rem',
          borderRadius: (typeof downloadToast === 'object' && downloadToast.type === 'error') ? '16px' : '50px',
          boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.6rem',
          fontWeight: 600,
          fontSize: '0.92rem',
          maxWidth: '92%',
          textAlign: 'center',
          lineHeight: '1.4',
          zIndex: 99999,
          pointerEvents: 'none',
          animation: 'fadeIn 0.25s ease-out',
          border: (typeof downloadToast === 'object' && downloadToast.type === 'error') ? '1px solid rgba(255, 255, 255, 0.25)' : 'none'
        }}>
          {typeof downloadToast === 'object' ? downloadToast.text : downloadToast}
        </div>
      )}

      {/* Web Reader Modal */}
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
                <div style={{display: 'flex', gap: '0.2rem'}}>
                  <button className="btn-icon" onClick={() => changeFontSize(-10)} title="Reducir letra">A-</button>
                  <span style={{fontSize: '0.8rem', minWidth: '35px', textAlign: 'center'}}>{readerSettings.fontSize}%</span>
                  <button className="btn-icon" onClick={() => changeFontSize(10)} title="Aumentar letra">A+</button>
                </div>
                
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

            <button className="btn-secondary" style={{padding: '0.4rem 1rem'}} onClick={() => { setReadingBookId(null); setReadingBookObj(null); if (activeView === 'myReadings') fetchMyReadings(); }}>
              Cerrar
            </button>
          </div>

          {/* Banner de previsualización limitada para usuarios sin iniciar sesión */}
          {!authStatus.authenticated && showPreviewNotice && (
            <div style={{
              backgroundColor: 'rgba(234, 88, 12, 0.95)',
              color: '#fff',
              padding: '0.55rem 1.2rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              fontSize: '0.85rem',
              fontWeight: 500,
              zIndex: 10
            }}>
              <span>
                📖 <strong>Modo Vista Previa:</strong> Estás viendo la primera página. <em>Inicia sesión</em> para leer el libro completo y guardar tu progreso.
              </span>
              <div style={{ display: 'flex', gap: '0.6rem' }}>
                <button 
                  className="btn-primary" 
                  style={{ backgroundColor: '#fff', color: '#ea580c', border: 'none', padding: '0.25rem 0.75rem', fontSize: '0.8rem', fontWeight: 600 }}
                  onClick={() => { setReadingBookId(null); setShowAuthModal(true); }}
                >
                  Iniciar Sesión
                </button>
                <button 
                  style={{ background: 'none', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '1rem', lineHeight: 1 }}
                  onClick={() => setShowPreviewNotice(false)}
                >
                  ✕
                </button>
              </div>
            </div>
          )}

          <div style={{flex: 1, position: 'relative'}}>
            {readingBookObj?.format === 'pdf' ? (
              <iframe 
                src={`http://${window.location.hostname}:8000/api/download/${readingBookId}${authToken ? `?token=${authToken}` : ''}`}
                style={{ width: '100%', height: '100%', border: 'none' }}
                title={readingBookObj.title || "Visor PDF"}
              />
            ) : (
              <ReactReader
                url={`http://${window.location.hostname}:8000/api/download/${readingBookId}${authToken ? `?token=${authToken}` : ''}`}
                location={readingLocation}
                locationChanged={(epubcfi) => handleLocationChange(readingBookId, epubcfi)}
                getRendition={(rendition) => {
                  renditionRef.current = rendition
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
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App

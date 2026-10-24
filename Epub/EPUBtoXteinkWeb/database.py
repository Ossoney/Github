import sqlite3
import hashlib
import secrets
import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "users.db"

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        # Tabla de usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL,
            credits_purchased INTEGER DEFAULT 0,
            daily_used INTEGER DEFAULT 0,
            last_used_date TEXT DEFAULT ''
        )
        """)
        # Tabla de sesiones
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        # Tabla para usuarios anónimos (IP/Fingerprint)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS anon_usage (
            identifier TEXT PRIMARY KEY,
            daily_used INTEGER DEFAULT 0,
            last_used_date TEXT DEFAULT ''
        )
        """)
        # Tabla de pagos (Stripe sessions)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount_cents INTEGER NOT NULL,
            credits_added INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        conn.commit()

init_db()

def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def create_user(email: str, password: str):
    email = email.strip().lower()
    salt = secrets.token_hex(16)
    pwd_hash = _hash_password(password, salt)
    now = datetime.datetime.now().isoformat()
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, password_hash, salt, created_at) VALUES (?, ?, ?, ?)",
                (email, pwd_hash, salt, now)
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None

def verify_user(email: str, password: str):
    email = email.strip().lower()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            return None
        pwd_hash = _hash_password(password, row['salt'])
        if pwd_hash == row['password_hash']:
            return row
    return None

def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    now = datetime.datetime.now().isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)", (token, user_id, now))
        conn.commit()
    return token

def get_user_by_email(email: str):
    email = email.strip().lower()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()

def add_credits_by_email(email: str, credits_to_add: int) -> bool:
    email = email.strip().lower()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            return False
        user_id = row['id']
        cursor.execute(
            "UPDATE users SET credits_purchased = credits_purchased + ? WHERE id = ?",
            (credits_to_add, user_id)
        )
        conn.commit()
        return True
def get_user_by_session(token: str):
    if not token:
        return None
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.* FROM users u
            JOIN sessions s ON u.id = s.user_id
            WHERE s.token = ?
        """, (token,))
        return cursor.fetchone()

def delete_session(token: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()

MASTER_EMAILS = {"ossoney@yahoo.es", "ossoney@gmail.com"}

def is_master_user(email: str) -> bool:
    if not email:
        return False
    return email.strip().lower() in MASTER_EMAILS

def get_today_str() -> str:
    return datetime.date.today().isoformat()

def get_user_allowance(user_id: int):
    """
    Devuelve la información de cupos del usuario.
    Si es usuario master, tiene cupo ilimitado.
    """
    today = get_today_str()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        u = cursor.fetchone()
        if not u:
            return None

        email = u['email'].lower()
        if is_master_user(email):
            return {
                "daily_limit": "∞",
                "daily_used": u['daily_used'],
                "daily_remaining": "∞",
                "purchased_credits": u['credits_purchased'],
                "total_available": 999999,
                "email": u['email'],
                "is_master": True
            }

        daily_used = u['daily_used']
        if u['last_used_date'] != today:
            daily_used = 0
            cursor.execute("UPDATE users SET daily_used = 0, last_used_date = ? WHERE id = ?", (today, user_id))
            conn.commit()

        daily_limit = 2
        daily_rem = max(0, daily_limit - daily_used)
        purchased = u['credits_purchased']

        return {
            "daily_limit": daily_limit,
            "daily_used": daily_used,
            "daily_remaining": daily_rem,
            "purchased_credits": purchased,
            "total_available": daily_rem + purchased,
            "email": u['email'],
            "is_master": False
        }

def deduct_user_credit(user_id: int) -> bool:
    """Consume 1 crédito. Si es master, no descuenta nada y siempre autoriza."""
    today = get_today_str()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        u = cursor.fetchone()
        if not u:
            return False

        email = u['email'].lower()
        if is_master_user(email):
            # Usuario master: acceso ilimitado
            cursor.execute(
                "UPDATE users SET daily_used = daily_used + 1, last_used_date = ? WHERE id = ?",
                (today, user_id)
            )
            conn.commit()
            return True

        daily_used = u['daily_used']
        if u['last_used_date'] != today:
            daily_used = 0

        if daily_used < 2:
            cursor.execute(
                "UPDATE users SET daily_used = ?, last_used_date = ? WHERE id = ?",
                (daily_used + 1, today, user_id)
            )
            conn.commit()
            return True
        elif u['credits_purchased'] > 0:
            cursor.execute(
                "UPDATE users SET credits_purchased = credits_purchased - 1 WHERE id = ?",
                (user_id,)
            )
            conn.commit()
            return True
        else:
            return False

def get_anon_allowance(ip_or_id: str):
    """Usuario sin loguear: 1 conversión al día."""
    today = get_today_str()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM anon_usage WHERE identifier = ?", (ip_or_id,))
        row = cursor.fetchone()
        daily_used = 0
        if row:
            if row['last_used_date'] == today:
                daily_used = row['daily_used']

        daily_limit = 1
        daily_rem = max(0, daily_limit - daily_used)
        return {
            "daily_limit": daily_limit,
            "daily_used": daily_used,
            "daily_remaining": daily_rem,
            "purchased_credits": 0,
            "total_available": daily_rem
        }

def deduct_anon_credit(ip_or_id: str) -> bool:
    today = get_today_str()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM anon_usage WHERE identifier = ?", (ip_or_id,))
        row = cursor.fetchone()
        daily_used = 0
        if row and row['last_used_date'] == today:
            daily_used = row['daily_used']

        if daily_used >= 1:
            return False

        if row:
            cursor.execute(
                "UPDATE anon_usage SET daily_used = ?, last_used_date = ? WHERE identifier = ?",
                (daily_used + 1, today, ip_or_id)
            )
        else:
            cursor.execute(
                "INSERT INTO anon_usage (identifier, daily_used, last_used_date) VALUES (?, ?, ?)",
                (ip_or_id, 1, today)
            )
        conn.commit()
        return True

def add_user_purchased_credits(user_id: int, credits_to_add: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET credits_purchased = credits_purchased + ? WHERE id = ?",
            (credits_to_add, user_id)
        )
        conn.commit()

def record_payment(session_id: str, user_id: int, amount_cents: int, credits_added: int, status="completed"):
    now = datetime.datetime.now().isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO payments (session_id, user_id, amount_cents, credits_added, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, user_id, amount_cents, credits_added, status, now)
        )
        conn.commit()

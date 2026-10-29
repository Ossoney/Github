import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from database import SessionLocal, User, UserSession

# Duración de la sesión: 30 días
SESSION_DURATION_DAYS = 30

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${key}"

def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    try:
        salt, key = stored_password_hash.split('$')
        computed_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(key, computed_key)
    except Exception:
        return False

def create_user_session(db: Session, user_id: int) -> UserSession:
    token = secrets.token_urlsafe(48)
    expires_at = datetime.utcnow() + timedelta(days=SESSION_DURATION_DAYS)
    session = UserSession(
        user_id=user_id,
        token=token,
        created_at=datetime.utcnow(),
        expires_at=expires_at
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_token_from_request(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Query(None)
) -> Optional[str]:
    if authorization and authorization.startswith("Bearer "):
        return authorization.split("Bearer ")[1].strip()
    if token:
        return token.strip()
    return None

def get_optional_user(
    db: Session = Depends(get_db),
    auth_token: Optional[str] = Depends(get_token_from_request)
) -> Optional[User]:
    if not auth_token:
        return None
    
    session = db.query(UserSession).filter(
        UserSession.token == auth_token,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    
    if not session:
        return None
        
    user = db.query(User).filter(User.id == session.user_id).first()
    return user

def get_current_user(
    user: Optional[User] = Depends(get_optional_user)
) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado o sesión expirada."
        )
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está pendiente de aprobación o inactiva."
        )
    return user

def require_master(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "master":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: se requieren permisos de Administrador Master."
        )
    return current_user

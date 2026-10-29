#!/usr/bin/env python3
"""
Herramienta de consola para restablecer la contraseña de cualquier usuario en EPUB Biblio.
Uso:
    python reset_password.py
    python reset_password.py <nombre_usuario> <nueva_contraseña>
"""

import sys
import os
import getpass

# Asegurar importación de módulos locales
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from database import SessionLocal, User, UserSession
from auth import hash_password
from paths import get_or_create_recovery_key, RECOVERY_KEY_PATH

def main():
    print("=" * 60)
    print("  EPUB Biblio - Restablecimiento de Contraseña")
    print("=" * 60)

    # Mostrar clave de recuperación del servidor
    rec_key = get_or_create_recovery_key()
    print(f"Clave de Recuperación del Servidor: {rec_key}")
    print(f"(Guardada en: {RECOVERY_KEY_PATH})\n")

    if len(sys.argv) >= 3:
        username = sys.argv[1].strip()
        new_password = sys.argv[2]
    else:
        username = input("Introduce el nombre de usuario (o email): ").strip()
        if not username:
            print("Operación cancelada: el nombre de usuario no puede estar vacío.")
            return
        new_password = getpass.getpass("Introduce la nueva contraseña: ")
        confirm = getpass.getpass("Confirma la nueva contraseña: ")
        if new_password != confirm:
            print("Error: Las contraseñas no coinciden.")
            return

    if len(new_password) < 4:
        print("Error: La contraseña debe tener al menos 4 caracteres.")
        return

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"Error: No se encontró ningún usuario con el nombre '{username}'.")
            print("\nUsuarios registrados:")
            for u in db.query(User).all():
                print(f" - ID: {u.id} | Usuario: {u.username} | Rol: {u.role} | Estado: {u.status}")
            return

        user.password_hash = hash_password(new_password)
        db.query(UserSession).filter(UserSession.user_id == user.id).delete()
        db.commit()
        print(f"\n[OK] Contraseña restablecida con éxito para '{user.username}' (Rol: {user.role}).")
        print("Todas las sesiones activas han sido cerradas para mayor seguridad.")
    finally:
        db.close()

if __name__ == "__main__":
    main()

import os
import sys
import uuid
import shutil
import zipfile
import json
import datetime
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from starlette.routing import Route
import uvicorn
import stripe

from converter import EPUBConverterCore, DEVICE_PROFILES
import database

BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML = BASE_DIR / "index.html"
FAVICON_ICO = BASE_DIR / "favicon.ico"
FAVICON_PNG = BASE_DIR / "favicon.png"
PROCESSED_STORAGE = BASE_DIR / "temp_downloads"
PROCESSED_STORAGE.mkdir(exist_ok=True)

# Configuración de Stripe y Ko-fi
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_placeholder_key")
stripe.api_key = STRIPE_SECRET_KEY
KOFI_VERIFICATION_TOKEN = os.environ.get("KOFI_VERIFICATION_TOKEN", "31acdb13-7457-4cca-83ca-47609905621e")

def get_client_ip(request):
    """Extrae la IP o identificador del cliente."""
    client = request.client
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return client.host if client else "127.0.0.1"

def get_current_user(request):
    token = request.cookies.get("session_token")
    if token:
        return database.get_user_by_session(token)
    return None

async def serve_index(request):
    """Entrega la interfaz web de usuario."""
    if not INDEX_HTML.exists():
        return HTMLResponse("<h1>index.html no encontrado</h1>", status_code=404)
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content)

async def serve_favicon_ico(request):
    if FAVICON_ICO.exists():
        return FileResponse(FAVICON_ICO, media_type="image/x-icon")
    return JSONResponse({"detail": "Not found"}, status_code=404)

async def serve_favicon_png(request):
    if FAVICON_PNG.exists():
        return FileResponse(FAVICON_PNG, media_type="image/png")
    return JSONResponse({"detail": "Not found"}, status_code=404)

async def api_devices(request):
    return JSONResponse(DEVICE_PROFILES)

async def api_auth_status(request):
    """Devuelve el estado de sesión y los créditos/cupos disponibles."""
    user = get_current_user(request)
    if user:
        info = database.get_user_allowance(user['id'])
        return JSONResponse({
            "logged_in": True,
            "email": user['email'],
            "is_master": info.get('is_master', False),
            "daily_limit": info['daily_limit'],
            "daily_used": info['daily_used'],
            "daily_remaining": info['daily_remaining'],
            "purchased_credits": info['purchased_credits'],
            "total_available": info['total_available'],
        })
    else:
        ip = get_client_ip(request)
        info = database.get_anon_allowance(ip)
        return JSONResponse({
            "logged_in": False,
            "email": None,
            "is_master": False,
            "daily_limit": info['daily_limit'],
            "daily_used": info['daily_used'],
            "daily_remaining": info['daily_remaining'],
            "purchased_credits": 0,
            "total_available": info['total_available'],
        })

async def api_register(request):
    try:
        body = await request.json()
        email = body.get("email", "").strip()
        password = body.get("password", "").strip()
        if not email or len(password) < 6:
            return JSONResponse({"detail": "Email válido y contraseña de mín. 6 caracteres requeridos"}, status_code=400)

        user_id = database.create_user(email, password)
        if not user_id:
            return JSONResponse({"detail": "El correo ya está registrado"}, status_code=409)

        token = database.create_session(user_id)
        resp = JSONResponse({"success": True, "email": email})
        resp.set_cookie("session_token", token, max_age=86400 * 30, httponly=True, samesite="lax")
        return resp
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)

async def api_login(request):
    try:
        body = await request.json()
        email = body.get("email", "").strip()
        password = body.get("password", "").strip()
        user = database.verify_user(email, password)
        if not user:
            return JSONResponse({"detail": "Credenciales incorrectas"}, status_code=401)

        token = database.create_session(user['id'])
        resp = JSONResponse({"success": True, "email": user['email']})
        resp.set_cookie("session_token", token, max_age=86400 * 30, httponly=True, samesite="lax")
        return resp
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)

async def api_forgot_password(request):
    try:
        body = await request.json()
        email = body.get("email", "").strip().lower()
        if not email:
            return JSONResponse({"detail": "Indica un correo electrónico"}, status_code=400)

        token = database.create_password_reset_token(email)
        if not token:
            # Por privacidad no revelamos si existe o no, pero informamos positivamente
            return JSONResponse({
                "success": True, 
                "message": "Si el correo está registrado, se ha generado el enlace de restablecimiento."
            })

        host_url = str(request.base_url).rstrip("/")
        reset_link = f"{host_url}/?reset_token={token}"
        print(f"🔑 [PASSWORD RESET] Enlace generado para {email}: {reset_link}")

        return JSONResponse({
            "success": True,
            "message": "Enlace de restablecimiento generado con éxito.",
            "reset_link": reset_link,
            "token": token
        })
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)

async def api_reset_password(request):
    try:
        body = await request.json()
        token = body.get("token", "").strip()
        new_password = body.get("password", "").strip()

        if not token or len(new_password) < 6:
            return JSONResponse({"detail": "Token requerido y contraseña de mín. 6 caracteres"}, status_code=400)

        success = database.complete_password_reset(token, new_password)
        if not success:
            return JSONResponse({"detail": "El enlace ha caducado o no es válido"}, status_code=400)

        return JSONResponse({"success": True, "message": "Contraseña actualizada correctamente"})
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)

async def api_logout(request):
    token = request.cookies.get("session_token")
    if token:
        database.delete_session(token)
    resp = JSONResponse({"success": True})
    resp.delete_cookie("session_token")
    return resp

# ----------------- PANEL DE CONTROL MASTER -----------------
async def api_admin_stats(request):
    user = get_current_user(request)
    if not user or not database.is_master_user(user['email']):
        return JSONResponse({"detail": "Acceso restringido a usuarios Master"}, status_code=403)

    stats = database.get_admin_dashboard_stats()
    return JSONResponse(stats)

async def api_admin_update_credits(request):
    user = get_current_user(request)
    if not user or not database.is_master_user(user['email']):
        return JSONResponse({"detail": "Acceso restringido a usuarios Master"}, status_code=403)

    try:
        body = await request.json()
        target_user_id = int(body.get("user_id"))
        new_credits = int(body.get("credits"))

        success = database.set_user_credits(target_user_id, new_credits)
        if not success:
            return JSONResponse({"detail": "Usuario no encontrado"}, status_code=404)

        return JSONResponse({"success": True, "user_id": target_user_id, "new_credits": new_credits})
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)

# ----------------- STRIPE CHECKOUT & CREDITS -----------------
async def api_create_checkout(request):
    user = get_current_user(request)
    if not user:
        return JSONResponse({"detail": "Debes iniciar sesión para comprar créditos"}, status_code=401)

    try:
        body = await request.json()
        plan = body.get("plan") # "100" o "300"
        
        if plan == "100":
            amount_cents = 500 # 5,00 €
            credits_to_add = 100
            plan_name = "100 Conversiones EPUBtoXteink"
        elif plan == "300":
            amount_cents = 1000 # 10,00 €
            credits_to_add = 300
            plan_name = "300 Conversiones EPUBtoXteink"
        else:
            return JSONResponse({"detail": "Plan no válido"}, status_code=400)

        host_url = str(request.base_url).rstrip("/")
        success_url = f"{host_url}/api/payment/success?session_id={{CHECKOUT_SESSION_ID}}&user_id={user['id']}&credits={credits_to_add}"
        cancel_url = f"{host_url}/?payment=cancelled"

        # Si no hay clave real de Stripe configurada, simular checkout directo
        if STRIPE_SECRET_KEY.startswith("sk_test_placeholder"):
            mock_session_id = f"mock_{uuid.uuid4()}"
            database.add_user_purchased_credits(user['id'], credits_to_add)
            database.record_payment(mock_session_id, user['id'], amount_cents, credits_to_add, "completed_mock")
            return JSONResponse({
                "checkout_url": f"/?payment=success&added={credits_to_add}&mock=1"
            })

        # Sesión Stripe oficial
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'unit_amount': amount_cents,
                    'product_data': {
                        'name': plan_name,
                        'description': f'Recarga de {credits_to_add} conversiones para lectores e-ink Xteink',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_email=user['email'],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'user_id': str(user['id']),
                'credits_to_add': str(credits_to_add)
            }
        )

        return JSONResponse({"checkout_url": checkout_session.url})

    except Exception as e:
        return JSONResponse({"detail": f"Error de pago: {str(e)}"}, status_code=500)

async def api_payment_success(request):
    """Callback tras completar el pago en Stripe."""
    session_id = request.query_params.get("session_id")
    user_id = int(request.query_params.get("user_id", "0"))
    credits = int(request.query_params.get("credits", "0"))

    if user_id > 0 and credits > 0:
        database.add_user_purchased_credits(user_id, credits)
        database.record_payment(session_id or "direct", user_id, 0, credits, "completed")

    return RedirectResponse(f"/?payment=success&added={credits}")

async def api_kofi_webhook(request):
    """
    Webhook oficial de Ko-fi.
    Recibe alertas instantáneas de pagos/donaciones y suma créditos automáticamente.
    """
    try:
        # Ko-fi envía los datos como form-data (application/x-www-form-urlencoded) con un campo 'data' en JSON
        form = await request.form()
        data_raw = form.get("data")
        if not data_raw:
            return JSONResponse({"detail": "Missing data payload"}, status_code=400)

        data = json.loads(data_raw)
        token = data.get("verification_token")
        if token != KOFI_VERIFICATION_TOKEN:
            return JSONResponse({"detail": "Unauthorized token"}, status_code=403)

        email = data.get("email", "").strip().lower()
        message = data.get("message", "")
        amount = float(data.get("amount", 0.0))
        kofi_tx_id = data.get("kofi_transaction_id") or str(uuid.uuid4())

        # Intentar extraer email del mensaje si se indicó explícitamente
        target_email = email
        if message and "@" in message:
            import re
            emails_in_msg = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", message)
            if emails_in_msg:
                # Comprobar si ese email existe en la BD
                cand_user = database.get_user_by_email(emails_in_msg[0])
                if cand_user:
                    target_email = cand_user['email']

        # Determinar créditos según importe donado:
        # 5 € o más -> 100 créditos (o múltiplo)
        # 10 € o más -> 300 créditos
        if amount >= 9.90:
            credits = 300
        elif amount >= 4.90:
            credits = 100
        else:
            # Cálculo proporcional si donan otra cantidad (20 créditos por cada euro)
            credits = int(amount * 20)

        if credits > 0 and target_email:
            user = database.get_user_by_email(target_email)
            if user:
                database.add_user_purchased_credits(user['id'], credits)
                database.record_payment(kofi_tx_id, user['id'], int(amount * 100), credits, "completed_kofi")
                print(f"🎉 Ko-fi Webhook: Asignados {credits} créditos al usuario {target_email} por {amount}€")
                return JSONResponse({"success": True, "credits_added": credits, "user": target_email})
            else:
                print(f"⚠️ Ko-fi Webhook: Pago de {amount}€ recibido de {target_email}, pero el usuario aún no está registrado en la web.")
                # Si el usuario no existe aún, se puede crear o registrar el pago
                return JSONResponse({"success": True, "message": "Email not found yet, payment logged"})

        return JSONResponse({"success": True, "message": "Processed without credits"})
    except Exception as e:
        print(f"❌ Error en webhook de Ko-fi: {e}")
        return JSONResponse({"detail": str(e)}, status_code=500)

# ----------------- CONVERSIÓN CON CONTROL DE CUPO -----------------
async def api_convert(request):
    filename = request.query_params.get("filename", "document.epub")
    device = request.query_params.get("device", "X4p")
    mode = request.query_params.get("mode", "epub")
    batch_id = request.query_params.get("batch_id", "")

    if device not in DEVICE_PROFILES:
        device = "X4p"

    # Verificar cupos / créditos
    user = get_current_user(request)
    if user:
        allowed = database.deduct_user_credit(user['id'])
        if not allowed:
            return JSONResponse({
                "detail": "Has alcanzado tu límite de conversiones (2/día). Compra un pack de 100 o 300 conversiones para continuar."
            }, status_code=429)
    else:
        ip = get_client_ip(request)
        allowed = database.deduct_anon_credit(ip)
        if not allowed:
            return JSONResponse({
                "detail": "Has alcanzado tu límite gratuito (1/día). Inicia sesión para tener 2 al día o adquirir créditos."
            }, status_code=429)

    body_bytes = await request.body()
    if not body_bytes:
        return JSONResponse({"detail": "No se recibieron datos"}, status_code=400)

    task_id = str(uuid.uuid4())
    work_dir = PROCESSED_STORAGE / (batch_id if batch_id else task_id)
    work_dir.mkdir(parents=True, exist_ok=True)

    input_file = work_dir / f"in_{task_id}_{filename}"
    with open(input_file, "wb") as f:
        f.write(body_bytes)

    converter = EPUBConverterCore(device_name=device)

    try:
        stem = Path(filename).stem
        if mode == "wallpaper":
            out_name = f"{stem}_{device}.bmp"
            out_file = work_dir / out_name
            converter.optimize_wallpaper_file(input_file, out_file)
        else:
            out_name = f"{stem}_{device}.epub"
            out_file = work_dir / out_name
            converter.process_epub_file(input_file, out_file)

        try:
            if input_file.exists():
                os.remove(input_file)
        except Exception:
            pass

        final_size = out_file.stat().st_size

        return JSONResponse({
            "task_id": task_id,
            "batch_id": batch_id,
            "output_name": out_name,
            "file_size": final_size,
            "device": device,
            "mode": mode
        })
    except Exception as e:
        if not batch_id:
            shutil.rmtree(work_dir, ignore_errors=True)
        return JSONResponse({"detail": f"Error en {filename}: {str(e)}"}, status_code=500)

async def api_download_zip(request):
    batch_id = request.path_params["batch_id"]
    batch_dir = PROCESSED_STORAGE / batch_id
    if not batch_dir.is_dir():
        return JSONResponse({"detail": "Lote no encontrado o expirado"}, status_code=404)

    files_to_zip = [f for f in batch_dir.iterdir() if f.is_file() and not f.name.startswith("in_") and not f.name.endswith(".zip")]
    if not files_to_zip:
        return JSONResponse({"detail": "No hay archivos listos"}, status_code=404)

    zip_path = batch_dir / "Lote_Optimizado_Xteink.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_zip:
            zf.write(f, f.name)

    return FileResponse(path=zip_path, filename="Lote_Optimizado_Xteink.zip", media_type="application/zip")

async def api_download(request):
    task_id = request.path_params["task_id"]
    task_dir = PROCESSED_STORAGE / task_id

    if not task_dir.is_dir():
        return JSONResponse({"detail": "Archivo no encontrado"}, status_code=404)

    files = [f for f in task_dir.iterdir() if f.is_file() and not f.name.startswith("in_") and not f.name.endswith(".zip")]
    if not files:
        return JSONResponse({"detail": "Archivo no disponible"}, status_code=404)

    target_file = files[0]
    media_type = "application/epub+zip" if target_file.suffix.lower() == ".epub" else "image/bmp"
    return FileResponse(path=target_file, filename=target_file.name, media_type=media_type)

routes = [
    Route("/", serve_index, methods=["GET"]),
    Route("/favicon.ico", serve_favicon_ico, methods=["GET"]),
    Route("/favicon.png", serve_favicon_png, methods=["GET"]),
    Route("/api/devices", api_devices, methods=["GET"]),
    Route("/api/auth/status", api_auth_status, methods=["GET"]),
    Route("/api/auth/register", api_register, methods=["POST"]),
    Route("/api/auth/login", api_login, methods=["POST"]),
    Route("/api/auth/logout", api_logout, methods=["POST"]),
    Route("/api/auth/forgot-password", api_forgot_password, methods=["POST"]),
    Route("/api/auth/reset-password", api_reset_password, methods=["POST"]),
    Route("/api/admin/stats", api_admin_stats, methods=["GET"]),
    Route("/api/admin/update-credits", api_admin_update_credits, methods=["POST"]),
    Route("/api/payment/create-checkout", api_create_checkout, methods=["POST"]),
    Route("/api/payment/success", api_payment_success, methods=["GET"]),
    Route("/api/kofi/webhook", api_kofi_webhook, methods=["POST"]),
    Route("/api/convert", api_convert, methods=["POST"]),
    Route("/api/download/{task_id}", api_download, methods=["GET"]),
    Route("/api/download_batch/{batch_id}", api_download_zip, methods=["GET"]),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"🚀 Iniciando servidor EPUBtoXteink Web en http://{host}:{port}")
    uvicorn.run("app:app", host=host, port=port, reload=False)

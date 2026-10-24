# Iniciar servidor web EPUBtoXteink Web
@echo off
title EPUBtoXteink Web Server
cd /d "%~dp0"
echo ===================================================
echo     Iniciando EPUBtoXteink Web (Servidor Local)
echo ===================================================
echo.
echo Abriendo navegador en http://localhost:8080 ...
start http://localhost:8080
echo.
python app.py
pause

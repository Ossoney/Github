@echo off
setlocal
chcp 65001 >nul

set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=python"

:: Si se hace doble clic sin arrastrar nada, abrir la interfaz gráfica
if "%~1"=="" (
    echo Iniciando ComicReducer GUI...
    start "" "%PYTHON_EXE%" "%SCRIPT_DIR%ComicReducer.py" --gui
    exit /b
)

:: Si se arrastran archivos o carpetas sobre el .bat
echo ===================================================
echo   ComicReducer - Procesamiento Drag and Drop
echo ===================================================

:loop
if "%~1"=="" goto end
echo Procesando: "%~1"
"%PYTHON_EXE%" "%SCRIPT_DIR%ComicReducer.py" "%~1"
shift
goto loop

:end
echo ===================================================
echo   Proceso finalizado.
echo ===================================================
pause

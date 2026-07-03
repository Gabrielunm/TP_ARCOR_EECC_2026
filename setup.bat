@echo off
title ARCOR Dashboard Setup

echo === ARCOR Dashboard - Configuracion Inicial ===
echo.

IF NOT EXIST "venv\" (
    echo [1/3] Creando entorno virtual...
    python -m venv venv
    IF ERRORLEVEL 1 (
        echo ERROR: No se pudo crear el venv. Verifica que Python este instalado.
        pause
        exit /b 1
    )
    echo   OK - Entorno creado
) ELSE (
    echo [1/3] El entorno virtual ya existe.
)

echo [2/3] Instalando dependencias...
call venv\Scripts\pip install -q -r requirements.txt
IF ERRORLEVEL 1 (
    echo ERROR: Fallo la instalacion de dependencias.
    pause
    exit /b 1
)
echo   OK - Dependencias instaladas

echo [3/3] Listo!
echo.
echo Para iniciar el dashboard, ejecuta:  run.bat
echo.
pause

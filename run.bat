@echo off
title ARCOR Dashboard

IF NOT EXIST "venv\" (
    echo ERROR: No existe el entorno virtual.
    echo Ejecuta primero  setup.bat
    pause
    exit /b 1
)

echo Iniciando ARCOR Dashboard...
call venv\Scripts\streamlit run app.py
IF ERRORLEVEL 1 (
    echo ERROR: Fallo al iniciar la app.
    pause
    exit /b 1
)

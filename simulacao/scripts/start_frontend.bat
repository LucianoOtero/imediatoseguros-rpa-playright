@echo off
echo Iniciando Frontend (Simulação Webflow)...
cd /d "%~dp0..\frontend"
python -m http.server 3000
pause




























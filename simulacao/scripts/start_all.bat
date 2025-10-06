@echo off
echo Iniciando Simulação Completa...
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo.
start "Frontend" cmd /k "cd /d "%~dp0..\frontend" && python -m http.server 3000"
timeout /t 2
start "Backend" cmd /k "cd /d "%~dp0..\backend" && php -S localhost:8000"
echo.
echo Ambientes iniciados!
echo Pressione qualquer tecla para fechar...
pause > nul

















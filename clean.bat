@echo off
echo 🧹 LIMPANDO ARQUIVOS TEMPORÁRIOS...
echo.

echo 📁 Removendo screenshots...
if exist "*.png" del /q "*.png"

echo 📄 Removendo estados HTML...
if exist "*.html" del /q "*.html"

echo 📊 Removendo relatórios antigos...
if exist "relatorios\*.json" del /q "relatorios\*.json"
if exist "relatorios\*.txt" del /q "relatorios\*.txt"

echo ✅ Limpeza concluída!
pause

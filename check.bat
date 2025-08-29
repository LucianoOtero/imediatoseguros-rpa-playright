@echo off
echo �� VERIFICANDO ARQUIVOS DO PROJETO...
echo.

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 📋 Executando verificação...
python verificar_arquivos.py

echo.
echo ✅ Verificação concluída!
pause

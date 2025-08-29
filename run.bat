@echo off
echo �� EXECUTANDO COTAÇÃO DE SEGURO...
echo.

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 📱 Executando todas as telas...
python executar_todas_telas.py

echo.
echo ✅ Execução concluída!
pause

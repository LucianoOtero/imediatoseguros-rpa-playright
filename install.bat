@echo off
echo �� INSTALANDO DEPENDÊNCIAS DO PROJETO...
echo.

echo 📦 Criando ambiente virtual...
python -m venv venv

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 📥 Instalando dependências...
pip install -r requirements.txt

echo ✅ Instalação concluída!
echo.
echo Para ativar o ambiente virtual:
echo   venv\Scripts\activate.bat
echo.
echo Para executar o projeto:
echo   python executar_todas_telas.py
echo.
pause

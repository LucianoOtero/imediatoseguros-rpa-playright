@echo off
echo �� TESTANDO TELAS INDIVIDUAIS...
echo.

if "%1"=="" (
    echo Uso: test.bat <numero_tela>
    echo Exemplo: test.bat 6
    echo.
    echo Telas disponíveis: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    pause
    exit /b
)

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 📱 Testando Tela %1...
python testar_telas_individual.py %1

echo.
echo ✅ Teste concluído!
pause

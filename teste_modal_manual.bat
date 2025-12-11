@echo off
echo ========================================
echo TESTE MANUAL DO MODAL - WINDOWS
echo ========================================
echo.

echo 1. Iniciando servidor frontend...
cd simulacao\frontend
start /B python -m http.server 3000
echo    Servidor iniciado em http://localhost:3000
echo.

echo 2. Aguardando 3 segundos...
timeout /t 3 /nobreak > nul
echo.

echo 3. Abrindo navegador...
start http://localhost:3000
echo    Navegador aberto
echo.

echo ========================================
echo INSTRUCOES PARA TESTE MANUAL:
echo ========================================
echo.
echo 1. Preencha o formulario com os dados do veiculo
echo 2. Clique em "Calcular Seguro"
echo 3. Observe o modal abrir
echo 4. Verifique se o progresso avanca de 0%% a 100%%
echo 5. Verifique se as estimativas aparecem no final
echo.
echo Pressione qualquer tecla para encerrar o servidor...
pause > nul
echo.

echo 4. Encerrando servidor...
taskkill /f /im python.exe > nul 2>&1
echo    Servidor encerrado
echo.

echo ========================================
echo TESTE CONCLUIDO
echo ========================================
pause




























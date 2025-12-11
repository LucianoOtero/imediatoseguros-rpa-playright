#!/bin/bash

# DEBUG PHP EXECUTION - RPA IMEDIATO SEGUROS
# Script para debugar execução via PHP

echo "🔍 INICIANDO DEBUG PHP EXECUTION"
echo "=================================="

# Configurações
RPA_DIR="/opt/imediatoseguros-rpa"
LOG_FILE="/tmp/debug_php_$(date +%Y%m%d_%H%M%S).log"

# Função para log
log_debug() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_debug "=== INICIANDO DEBUG PHP EXECUTION ==="

# 1. Verificar ambiente atual
log_debug "1. VERIFICANDO AMBIENTE ATUAL"
log_debug "   Usuário atual: $(whoami)"
log_debug "   Diretório atual: $(pwd)"
log_debug "   PATH: $PATH"
log_debug "   Python: $(which python)"
log_debug "   Python3: $(which python3)"

# 2. Verificar se estamos no diretório correto
log_debug "2. VERIFICANDO DIRETÓRIO RPA"
if [ -d "$RPA_DIR" ]; then
    log_debug "   Diretório RPA existe: $RPA_DIR"
    cd "$RPA_DIR"
    log_debug "   Mudou para: $(pwd)"
else
    log_debug "   ERRO: Diretório RPA não existe: $RPA_DIR"
    exit 1
fi

# 3. Verificar ambiente virtual
log_debug "3. VERIFICANDO AMBIENTE VIRTUAL"
if [ -f "venv/bin/activate" ]; then
    log_debug "   Script de ativação existe"
    source venv/bin/activate
    log_debug "   Ambiente virtual ativado"
    log_debug "   Python após ativação: $(which python)"
    log_debug "   VIRTUAL_ENV: $VIRTUAL_ENV"
else
    log_debug "   ERRO: Script de ativação não encontrado"
    exit 1
fi

# 4. Verificar arquivo de teste
log_debug "4. VERIFICANDO ARQUIVO DE TESTE"
if [ -f "teste_api_simples.py" ]; then
    log_debug "   Arquivo teste_api_simples.py existe"
    log_debug "   Permissões: $(ls -la teste_api_simples.py)"
else
    log_debug "   ERRO: Arquivo teste_api_simples.py não encontrado"
    exit 1
fi

# 5. Testar execução direta
log_debug "5. TESTANDO EXECUÇÃO DIRETA"
log_debug "   Comando: python teste_api_simples.py --session debug_php_direto"
python teste_api_simples.py --session debug_php_direto
EXIT_CODE=$?
log_debug "   Código de saída: $EXIT_CODE"

# 6. Verificar se dados foram salvos no Redis
log_debug "6. VERIFICANDO REDIS"
sleep 2
REDIS_KEYS=$(redis-cli keys '*debug_php_direto*')
log_debug "   Chaves Redis encontradas: $REDIS_KEYS"

if [ -n "$REDIS_KEYS" ]; then
    log_debug "   ✅ Dados salvos no Redis com sucesso"
    for key in $REDIS_KEYS; do
        log_debug "   Chave: $key"
        redis-cli get "$key" | head -c 200 >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"
    done
else
    log_debug "   ❌ Nenhum dado encontrado no Redis"
fi

# 7. Simular comando exato do PHP
log_debug "7. SIMULANDO COMANDO EXATO DO PHP"
COMANDO_PHP="cd /opt/imediatoseguros-rpa && source venv/bin/activate && python teste_api_simples.py --session debug_php_simulado --modo-silencioso"
log_debug "   Comando: $COMANDO_PHP"

# Executar comando
bash -c "$COMANDO_PHP"
EXIT_CODE_PHP=$?
log_debug "   Código de saída: $EXIT_CODE_PHP"

# 8. Verificar Redis após simulação PHP
log_debug "8. VERIFICANDO REDIS APÓS SIMULAÇÃO PHP"
sleep 2
REDIS_KEYS_PHP=$(redis-cli keys '*debug_php_simulado*')
log_debug "   Chaves Redis encontradas: $REDIS_KEYS_PHP"

if [ -n "$REDIS_KEYS_PHP" ]; then
    log_debug "   ✅ Dados salvos no Redis com sucesso (simulação PHP)"
else
    log_debug "   ❌ Nenhum dado encontrado no Redis (simulação PHP)"
fi

# 9. Verificar logs do sistema
log_debug "9. VERIFICANDO LOGS DO SISTEMA"
if [ -f "/var/log/nginx/error.log" ]; then
    log_debug "   Últimas linhas do nginx error.log:"
    tail -5 /var/log/nginx/error.log | while read line; do
        log_debug "     $line"
    done
fi

if [ -f "/var/log/php8.3-fpm.log" ]; then
    log_debug "   Últimas linhas do php-fpm.log:"
    tail -5 /var/log/php8.3-fpm.log | while read line; do
        log_debug "     $line"
    done
fi

# 10. Verificar processos Python
log_debug "10. VERIFICANDO PROCESSOS PYTHON"
PROCESSOS_PYTHON=$(ps aux | grep python | grep -v grep)
log_debug "   Processos Python ativos:"
echo "$PROCESSOS_PYTHON" | while read line; do
    log_debug "     $line"
done

# 11. Testar com nohup (como o PHP faz)
log_debug "11. TESTANDO COM NOHUP (COMO PHP)"
COMANDO_NOHUP="nohup bash -c 'cd /opt/imediatoseguros-rpa && source venv/bin/activate && python teste_api_simples.py --session debug_php_nohup --modo-silencioso' > /dev/null 2>&1 & echo \$!"
log_debug "   Comando nohup: $COMANDO_NOHUP"

PID=$(bash -c "$COMANDO_NOHUP")
log_debug "   PID retornado: $PID"

# Aguardar um pouco
sleep 3

# Verificar se processo ainda está rodando
if ps -p "$PID" > /dev/null 2>&1; then
    log_debug "   Processo $PID ainda está rodando"
else
    log_debug "   Processo $PID já terminou"
fi

# Verificar Redis após nohup
sleep 2
REDIS_KEYS_NOHUP=$(redis-cli keys '*debug_php_nohup*')
log_debug "   Chaves Redis após nohup: $REDIS_KEYS_NOHUP"

if [ -n "$REDIS_KEYS_NOHUP" ]; then
    log_debug "   ✅ Dados salvos no Redis com sucesso (nohup)"
else
    log_debug "   ❌ Nenhum dado encontrado no Redis (nohup)"
fi

# 12. Verificar arquivo de parâmetros
log_debug "12. VERIFICANDO ARQUIVO DE PARÂMETROS"
if [ -d "temp" ]; then
    log_debug "   Diretório temp existe"
    ls -la temp/ | while read line; do
        log_debug "     $line"
    done
else
    log_debug "   Diretório temp não existe"
fi

# 13. Verificar permissões
log_debug "13. VERIFICANDO PERMISSÕES"
log_debug "   Permissões do diretório RPA:"
ls -la /opt/imediatoseguros-rpa/ | head -10 | while read line; do
    log_debug "     $line"
done

log_debug "   Permissões do arquivo de teste:"
ls -la /opt/imediatoseguros-rpa/teste_api_simples.py

# 14. Verificar variáveis de ambiente
log_debug "14. VERIFICANDO VARIÁVEIS DE AMBIENTE"
log_debug "   HOME: $HOME"
log_debug "   USER: $USER"
log_debug "   SHELL: $SHELL"
log_debug "   LANG: $LANG"
log_debug "   DISPLAY: $DISPLAY"

# 15. Testar comando mínimo
log_debug "15. TESTANDO COMANDO MÍNIMO"
echo "print('Teste mínimo funcionando')" > /tmp/teste_minimo.py
python /tmp/teste_minimo.py
EXIT_CODE_MINIMO=$?
log_debug "   Código de saída (mínimo): $EXIT_CODE_MINIMO"
rm -f /tmp/teste_minimo.py

log_debug "=== DEBUG PHP EXECUTION FINALIZADO ==="
log_debug "Log completo salvo em: $LOG_FILE"

echo ""
echo "📊 RESUMO DO DEBUG:"
echo "==================="
echo "📁 Log detalhado: $LOG_FILE"
echo "🔍 Verifique o log para identificar problemas"
echo "✅ Se execução direta funcionou mas nohup não, problema é de ambiente"
echo "❌ Se execução direta não funcionou, problema é do código"




























#!/bin/bash
# Script principal para executar todos os testes corrigidos

echo "=== Executando Plano de Testes Fase 2 (Corrigido) ==="

# Configurações
LOG_DIR="/tmp/test_logs_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOG_DIR"

# Função para log
log() {
    echo "$(date): $1" | tee -a "$LOG_DIR/test_execution.log"
}

# Função para executar teste
run_test() {
    local test_name="$1"
    local script_path="$2"
    local log_file="$LOG_DIR/${test_name}.log"
    
    log "Iniciando teste: $test_name"
    
    if [ -f "$script_path" ]; then
        bash "$script_path" 2>&1 | tee "$log_file"
        local exit_code=${PIPESTATUS[0]}
        
        if [ $exit_code -eq 0 ]; then
            log "✅ Teste $test_name concluído com sucesso"
        else
            log "❌ Teste $test_name falhou (código: $exit_code)"
        fi
        
        return $exit_code
    else
        log "❌ Script não encontrado: $script_path"
        return 1
    fi
}

# Iniciar execução
log "Iniciando execução do plano de testes corrigido"
log "Logs salvos em: $LOG_DIR"

# Dia 1: Correção do Progress Tracker
log "=== DIA 1: Correção do Progress Tracker ==="
run_test "progress_tracker_fix" "test_progress_tracker_fix.sh"
PROGRESS_TRACKER_RESULT=$?

# Dia 2: Testes Concorrentes
log "=== DIA 2: Testes Concorrentes ==="
run_test "concurrent_tests" "test_concurrent_fixed.sh"
CONCURRENT_RESULT=$?

# Dia 3: Validação de Arquivos
log "=== DIA 3: Validação de Arquivos ==="
run_test "file_validation" "test_validate_files.sh"
VALIDATION_RESULT=$?

# Dia 4: Testes de Carga e Performance
log "=== DIA 4: Testes de Carga e Performance ==="
run_test "load_performance" "test_load_performance.sh"
LOAD_RESULT=$?

# Dia 5: Relatório Final
log "=== DIA 5: Relatório Final ==="
run_test "final_report" "test_final_report.sh"
REPORT_RESULT=$?

# Resumo final
log "=== RESUMO FINAL ==="
log "Progress Tracker: $([ $PROGRESS_TRACKER_RESULT -eq 0 ] && echo "✅ Sucesso" || echo "❌ Falhou")"
log "Testes Concorrentes: $([ $CONCURRENT_RESULT -eq 0 ] && echo "✅ Sucesso" || echo "❌ Falhou")"
log "Validação de Arquivos: $([ $VALIDATION_RESULT -eq 0 ] && echo "✅ Sucesso" || echo "❌ Falhou")"
log "Testes de Carga: $([ $LOAD_RESULT -eq 0 ] && echo "✅ Sucesso" || echo "❌ Falhou")"
log "Relatório Final: $([ $REPORT_RESULT -eq 0 ] && echo "✅ Sucesso" || echo "❌ Falhou")"

# Calcular sucesso geral
TOTAL_TESTS=5
SUCCESSFUL_TESTS=0

[ $PROGRESS_TRACKER_RESULT -eq 0 ] && SUCCESSFUL_TESTS=$((SUCCESSFUL_TESTS + 1))
[ $CONCURRENT_RESULT -eq 0 ] && SUCCESSFUL_TESTS=$((SUCCESSFUL_TESTS + 1))
[ $VALIDATION_RESULT -eq 0 ] && SUCCESSFUL_TESTS=$((SUCCESSFUL_TESTS + 1))
[ $LOAD_RESULT -eq 0 ] && SUCCESSFUL_TESTS=$((SUCCESSFUL_TESTS + 1))
[ $REPORT_RESULT -eq 0 ] && SUCCESSFUL_TESTS=$((SUCCESSFUL_TESTS + 1))

SUCCESS_RATE=$((SUCCESSFUL_TESTS * 100 / TOTAL_TESTS))

log "Taxa de sucesso: $SUCCESSFUL_TESTS/$TOTAL_TESTS ($SUCCESS_RATE%)"

if [ $SUCCESS_RATE -ge 80 ]; then
    log "🎉 Plano de testes executado com sucesso!"
    exit 0
else
    log "⚠️ Plano de testes executado com problemas"
    exit 1
fi

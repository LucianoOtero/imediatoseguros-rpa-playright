#!/bin/bash
# Script de monitoramento em tempo real de sessões RPA

# Carregar configurações
source "$(dirname "$0")/../config/test_config.sh"

set -e

log_info "=== Monitor de Sessões RPA ==="

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Opções:"
    echo "  -s, --session SESSION_ID    Monitorar sessão específica"
    echo "  -a, --all                   Monitorar todas as sessões ativas"
    echo "  -i, --interval SECONDS      Intervalo de atualização (padrão: 2)"
    echo "  -h, --help                  Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 -s rpa_v4_20250930_201530_abc123"
    echo "  $0 -a -i 5"
    echo "  $0 --session rpa_v4_20250930_201530_abc123 --interval 1"
}

# Função para monitorar uma sessão específica
monitor_session() {
    local session_id="$1"
    local interval="$2"
    
    log_info "Monitorando sessão: $session_id"
    log_info "Intervalo: ${interval}s (Ctrl+C para parar)"
    echo ""
    
    while true; do
        PROGRESS=$(curl -s --connect-timeout $CONNECTION_TIMEOUT "$API_URL$PROGRESS_ENDPOINT/$session_id")
        
        if [ $? -ne 0 ]; then
            log_error "Falha ao consultar progresso da sessão $session_id"
            sleep $interval
            continue
        fi
        
        if ! validate_json "$PROGRESS"; then
            log_error "Resposta de progresso inválida para sessão $session_id"
            sleep $interval
            continue
        fi
        
        # Extrair dados
        STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
        ETAPA=$(echo "$PROGRESS" | jq -r '.progress.etapa_atual')
        TOTAL=$(echo "$PROGRESS" | jq -r '.progress.total_etapas')
        PERCENTUAL=$(echo "$PROGRESS" | jq -r '.progress.percentual')
        MENSAGEM=$(echo "$PROGRESS" | jq -r '.progress.mensagem')
        TIMESTAMP=$(echo "$PROGRESS" | jq -r '.timestamp')
        
        # Limpar tela e mostrar status
        clear
        echo "=== Monitor RPA - Sessão: $session_id ==="
        echo "Timestamp: $TIMESTAMP"
        echo ""
        echo "Status: $STATUS"
        echo "Etapa: $ETAPA/$TOTAL ($PERCENTUAL%)"
        echo "Mensagem: $MENSAGEM"
        echo ""
        
        # Mostrar estimativas se disponíveis
        ESTIMATIVAS=$(echo "$PROGRESS" | jq -r '.progress.estimativas.capturadas')
        if [ "$ESTIMATIVAS" = "true" ]; then
            echo "=== Estimativas Capturadas ==="
            echo "$PROGRESS" | jq '.progress.estimativas.dados'
            echo ""
        fi
        
        # Mostrar resultados finais se disponíveis
        RESULTADOS=$(echo "$PROGRESS" | jq -r '.progress.resultados_finais.rpa_finalizado')
        if [ "$RESULTADOS" = "true" ]; then
            echo "=== Resultados Finais ==="
            echo "$PROGRESS" | jq '.progress.resultados_finais.dados'
            echo ""
        fi
        
        # Mostrar timeline se disponível
        TIMELINE=$(echo "$PROGRESS" | jq -r '.progress.timeline')
        if [ "$TIMELINE" != "null" ] && [ "$TIMELINE" != "[]" ]; then
            echo "=== Timeline ==="
            echo "$PROGRESS" | jq -r '.progress.timeline[] | "\(.timestamp) - \(.mensagem)"'
            echo ""
        fi
        
        echo "Pressione Ctrl+C para parar o monitoramento"
        echo "Próxima atualização em ${interval}s..."
        
        # Verificar se concluído
        if [ "$STATUS" = "success" ] || [ "$STATUS" = "completed" ]; then
            log_success "Sessão $session_id concluída com sucesso!"
            break
        elif [ "$STATUS" = "failed" ] || [ "$STATUS" = "error" ]; then
            log_error "Sessão $session_id falhou: $MENSAGEM"
            break
        fi
        
        sleep $interval
    done
}

# Função para monitorar todas as sessões ativas
monitor_all_sessions() {
    local interval="$1"
    
    log_info "Monitorando todas as sessões ativas"
    log_info "Intervalo: ${interval}s (Ctrl+C para parar)"
    echo ""
    
    while true; do
        # Buscar sessões ativas (assumindo que temos um endpoint para listar sessões)
        # Por enquanto, vamos monitorar arquivos de progresso
        PROGRESS_FILES=$(find "$RPA_DATA_DIR" -name "progress_*.json" -mtime -1 2>/dev/null | head -10)
        
        if [ -z "$PROGRESS_FILES" ]; then
            clear
            echo "=== Monitor RPA - Todas as Sessões ==="
            echo "Nenhuma sessão ativa encontrada"
            echo ""
            echo "Pressione Ctrl+C para parar o monitoramento"
            echo "Próxima atualização em ${interval}s..."
            sleep $interval
            continue
        fi
        
        # Limpar tela e mostrar status de todas as sessões
        clear
        echo "=== Monitor RPA - Todas as Sessões ==="
        echo "Timestamp: $(date)"
        echo ""
        
        for file in $PROGRESS_FILES; do
            SESSION_ID=$(basename "$file" .json | sed 's/progress_//')
            
            if ! validate_json_file "$file"; then
                continue
            fi
            
            STATUS=$(jq -r '.status' "$file")
            ETAPA=$(jq -r '.etapa_atual' "$file")
            TOTAL=$(jq -r '.total_etapas' "$file")
            PERCENTUAL=$(jq -r '.percentual' "$file")
            MENSAGEM=$(jq -r '.mensagem' "$file")
            TIMESTAMP=$(jq -r '.timestamp_atualizacao' "$file")
            
            echo "Sessão: $SESSION_ID"
            echo "  Status: $STATUS"
            echo "  Etapa: $ETAPA/$TOTAL ($PERCENTUAL%)"
            echo "  Mensagem: $MENSAGEM"
            echo "  Última atualização: $TIMESTAMP"
            echo ""
        done
        
        echo "Pressione Ctrl+C para parar o monitoramento"
        echo "Próxima atualização em ${interval}s..."
        
        sleep $interval
    done
}

# Função para validar arquivo JSON
validate_json_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        return 1
    fi
    
    if command_exists jq; then
        jq . "$file" >/dev/null 2>&1
    else
        python3 -m json.tool "$file" >/dev/null 2>&1
    fi
}

# Processar argumentos
SESSION_ID=""
MONITOR_ALL=false
INTERVAL=2

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--session)
            SESSION_ID="$2"
            shift 2
            ;;
        -a|--all)
            MONITOR_ALL=true
            shift
            ;;
        -i|--interval)
            INTERVAL="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Verificar se estamos no servidor correto
if [ "$(hostname)" != "ubuntu-2gb-hel1-1" ]; then
    log_error "Execute este script no servidor Hetzner"
    exit 1
fi

# Executar monitoramento
if [ "$MONITOR_ALL" = true ]; then
    monitor_all_sessions "$INTERVAL"
elif [ ! -z "$SESSION_ID" ]; then
    monitor_session "$SESSION_ID" "$INTERVAL"
else
    log_error "Especifique uma sessão (-s) ou use --all para monitorar todas"
    show_help
    exit 1
fi

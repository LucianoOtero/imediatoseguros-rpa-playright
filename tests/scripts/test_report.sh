#!/bin/bash
# Script para gerar relatório de testes

# Carregar configurações
source "$(dirname "$0")/../config/test_config.sh"

set -e

log_info "=== Relatório de Testes API V4 ==="

# Função para gerar relatório
generate_report() {
    local output_file="$1"
    
    log_info "Gerando relatório em: $output_file"
    
    {
        echo "# Relatório de Testes API V4"
        echo "Data: $(date)"
        echo "Servidor: $(hostname)"
        echo ""
        
        echo "## Resumo Executivo"
        echo ""
        
        # Contar arquivos de progresso
        PROGRESS_COUNT=$(find "$RPA_DATA_DIR" -name "progress_*.json" -mtime -1 2>/dev/null | wc -l)
        echo "- Arquivos de progresso gerados: $PROGRESS_COUNT"
        
        # Contar arquivos de resultados
        RESULT_COUNT=$(find /opt/imediatoseguros-rpa/ -name "dados_planos_seguro_*.json" -mtime -1 2>/dev/null | wc -l)
        echo "- Arquivos de resultados gerados: $RESULT_COUNT"
        
        # Verificar status da API
        if curl -s --connect-timeout $CONNECTION_TIMEOUT "$API_URL$HEALTH_ENDPOINT" | jq -e '.success' >/dev/null 2>&1; then
            echo "- Status da API: ✅ Funcionando"
        else
            echo "- Status da API: ❌ Com problemas"
        fi
        
        echo ""
        echo "## Detalhes dos Testes"
        echo ""
        
        # Analisar arquivos de progresso
        if [ $PROGRESS_COUNT -gt 0 ]; then
            echo "### Arquivos de Progresso"
            echo ""
            
            PROGRESS_FILES=$(find "$RPA_DATA_DIR" -name "progress_*.json" -mtime -1 2>/dev/null | head -10)
            for file in $PROGRESS_FILES; do
                SESSION_ID=$(basename "$file" .json | sed 's/progress_//')
                
                if ! validate_json_file "$file"; then
                    echo "❌ **$SESSION_ID**: JSON inválido"
                    continue
                fi
                
                STATUS=$(jq -r '.status' "$file")
                ETAPA=$(jq -r '.etapa_atual' "$file")
                TOTAL=$(jq -r '.total_etapas' "$file")
                PERCENTUAL=$(jq -r '.percentual' "$file")
                MENSAGEM=$(jq -r '.mensagem' "$file")
                TIMESTAMP=$(jq -r '.timestamp_atualizacao' "$file")
                
                echo "#### Sessão: $SESSION_ID"
                echo "- **Status**: $STATUS"
                echo "- **Etapa**: $ETAPA/$TOTAL ($PERCENTUAL%)"
                echo "- **Mensagem**: $MENSAGEM"
                echo "- **Timestamp**: $TIMESTAMP"
                
                # Verificar estimativas
                ESTIMATIVAS=$(jq -r '.dados_extra.estimativas_tela_5' "$file")
                if [ "$ESTIMATIVAS" != "null" ] && [ "$ESTIMATIVAS" != "false" ]; then
                    COBERTURAS=$(jq -r '.dados_extra.estimativas_tela_5.coberturas_detalhadas | length' "$file")
                    echo "- **Estimativas**: ✅ Capturadas ($COBERTURAS coberturas)"
                else
                    echo "- **Estimativas**: ❌ Não capturadas"
                fi
                
                # Verificar resultados finais
                PLANO_REC=$(jq -r '.dados_extra.plano_recomendado' "$file")
                if [ "$PLANO_REC" != "null" ]; then
                    VALOR_REC=$(jq -r '.dados_extra.plano_recomendado.valor' "$file")
                    echo "- **Resultados Finais**: ✅ Capturados (Recomendado: $VALOR_REC)"
                else
                    echo "- **Resultados Finais**: ❌ Não capturados"
                fi
                
                echo ""
            done
        else
            echo "### Arquivos de Progresso"
            echo "❌ Nenhum arquivo de progresso encontrado"
            echo ""
        fi
        
        # Analisar arquivos de resultados
        if [ $RESULT_COUNT -gt 0 ]; then
            echo "### Arquivos de Resultados"
            echo ""
            
            RESULT_FILES=$(find /opt/imediatoseguros-rpa/ -name "dados_planos_seguro_*.json" -mtime -1 2>/dev/null | head -5)
            for file in $RESULT_FILES; do
                FILENAME=$(basename "$file")
                
                if ! validate_json_file "$file"; then
                    echo "❌ **$FILENAME**: JSON inválido"
                    continue
                fi
                
                PLANO_REC=$(jq -r '.plano_recomendado.valor' "$file")
                PLANO_ALT=$(jq -r '.plano_alternativo.valor' "$file")
                
                echo "#### $FILENAME"
                echo "- **Plano Recomendado**: $PLANO_REC"
                echo "- **Plano Alternativo**: $PLANO_ALT"
                
                # Validar valores
                if [[ "$PLANO_REC" =~ ^R\$[0-9.,]+$ ]] && [[ "$PLANO_ALT" =~ ^R\$[0-9.,]+$ ]]; then
                    echo "- **Status**: ✅ Valores válidos"
                else
                    echo "- **Status**: ❌ Valores podem estar inválidos"
                fi
                
                echo ""
            done
        else
            echo "### Arquivos de Resultados"
            echo "❌ Nenhum arquivo de resultados encontrado"
            echo ""
        fi
        
        echo "## Conclusões"
        echo ""
        
        if [ $PROGRESS_COUNT -gt 0 ] && [ $RESULT_COUNT -gt 0 ]; then
            echo "✅ **Testes bem-sucedidos**: $PROGRESS_COUNT sessões processadas, $RESULT_COUNT resultados gerados"
        elif [ $PROGRESS_COUNT -gt 0 ]; then
            echo "⚠️ **Testes parciais**: $PROGRESS_COUNT sessões processadas, mas nenhum resultado final"
        else
            echo "❌ **Testes falharam**: Nenhuma sessão processada com sucesso"
        fi
        
        echo ""
        echo "## Próximos Passos"
        echo ""
        echo "1. Verificar logs de erro se houver falhas"
        echo "2. Validar implementação --data nos scripts Python"
        echo "3. Testar com dados diferentes se necessário"
        echo "4. Implementar melhorias baseadas nos resultados"
        
    } > "$output_file"
    
    log_success "Relatório gerado: $output_file"
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

# Verificar se estamos no servidor correto
if [ "$(hostname)" != "ubuntu-2gb-hel1-1" ]; then
    log_error "Execute este script no servidor Hetzner"
    exit 1
fi

# Gerar relatório
REPORT_FILE="relatorio_testes_$(date +%Y%m%d_%H%M%S).md"
generate_report "$REPORT_FILE"

# Mostrar resumo
log_info "=== Resumo do Relatório ==="
echo "Arquivo: $REPORT_FILE"
echo "Localização: $(pwd)/$REPORT_FILE"
echo ""

# Mostrar estatísticas rápidas
PROGRESS_COUNT=$(find "$RPA_DATA_DIR" -name "progress_*.json" -mtime -1 2>/dev/null | wc -l)
RESULT_COUNT=$(find /opt/imediatoseguros-rpa/ -name "dados_planos_seguro_*.json" -mtime -1 2>/dev/null | wc -l)

echo "Estatísticas:"
echo "- Arquivos de progresso: $PROGRESS_COUNT"
echo "- Arquivos de resultados: $RESULT_COUNT"

if [ $PROGRESS_COUNT -gt 0 ] && [ $RESULT_COUNT -gt 0 ]; then
    log_success "Testes bem-sucedidos!"
elif [ $PROGRESS_COUNT -gt 0 ]; then
    log_warning "Testes parciais - verificar relatório"
else
    log_error "Testes falharam - verificar relatório"
fi

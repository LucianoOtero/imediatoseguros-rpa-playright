#!/bin/bash
# Script para validação de arquivos

echo "=== Validação de Arquivos ==="

# Validar arquivos de progresso
echo "1. Validando arquivos de progresso..."
PROGRESS_COUNT=0
PROGRESS_VALID=0

find /opt/imediatoseguros-rpa/rpa_data/ -name "progress_*.json" -mtime -1 | while read -r file; do
    PROGRESS_COUNT=$((PROGRESS_COUNT + 1))
    echo "Validando: $(basename "$file")"
    
    # Verificar se é JSON válido
    if jq . "$file" >/dev/null 2>&1; then
        echo "  ✅ JSON válido"
        PROGRESS_VALID=$((PROGRESS_VALID + 1))
        
        # Verificar campos obrigatórios
        ETAPA=$(jq -r '.etapa_atual' "$file")
        STATUS=$(jq -r '.status' "$file")
        SESSION_ID=$(jq -r '.session_id' "$file")
        TIMESTAMP=$(jq -r '.timestamp_atualizacao' "$file")
        
        if [ "$ETAPA" != "null" ] && [ "$STATUS" != "null" ] && [ "$SESSION_ID" != "null" ] && [ "$TIMESTAMP" != "null" ]; then
            echo "  ✅ Campos obrigatórios presentes"
            echo "    - Etapa: $ETAPA"
            echo "    - Status: $STATUS"
            echo "    - Session ID: $SESSION_ID"
            echo "    - Timestamp: $TIMESTAMP"
        else
            echo "  ❌ Campos obrigatórios ausentes"
        fi
        
        # Verificar estimativas se disponíveis
        ESTIMATIVAS=$(jq -r '.dados_extra.estimativas_tela_5' "$file")
        if [ "$ESTIMATIVAS" != "null" ] && [ "$ESTIMATIVAS" != "false" ]; then
            COBERTURAS=$(jq -r '.dados_extra.estimativas_tela_5.coberturas_detalhadas | length' "$file")
            echo "  ✅ Estimativas capturadas ($COBERTURAS coberturas)"
        fi
        
        # Verificar resultados finais se disponíveis
        PLANO_REC=$(jq -r '.dados_extra.plano_recomendado' "$file")
        if [ "$PLANO_REC" != "null" ]; then
            VALOR_REC=$(jq -r '.dados_extra.plano_recomendado.valor' "$file")
            echo "  ✅ Resultados finais capturados (Recomendado: $VALOR_REC)"
        fi
    else
        echo "  ❌ JSON inválido"
    fi
    
    echo ""
done

# Validar arquivos de resultados
echo "2. Validando arquivos de resultados..."
RESULT_COUNT=0
RESULT_VALID=0

find /opt/imediatoseguros-rpa/ -name "dados_planos_seguro_*.json" -mtime -1 | while read -r file; do
    RESULT_COUNT=$((RESULT_COUNT + 1))
    echo "Validando: $(basename "$file")"
    
    # Verificar se é JSON válido
    if jq . "$file" >/dev/null 2>&1; then
        echo "  ✅ JSON válido"
        RESULT_VALID=$((RESULT_VALID + 1))
        
        # Verificar estrutura
        PLANO_REC=$(jq -r '.plano_recomendado.valor' "$file")
        PLANO_ALT=$(jq -r '.plano_alternativo.valor' "$file")
        
        if [ "$PLANO_REC" != "null" ] && [ "$PLANO_ALT" != "null" ]; then
            echo "  ✅ Estrutura correta"
            echo "  📊 Plano Recomendado: $PLANO_REC"
            echo "  📊 Plano Alternativo: $PLANO_ALT"
            
            # Validar valores monetários
            if [[ "$PLANO_REC" =~ ^R\$[0-9.,]+$ ]] && [[ "$PLANO_ALT" =~ ^R\$[0-9.,]+$ ]]; then
                echo "  ✅ Valores monetários válidos"
            else
                echo "  ⚠️ Valores monetários podem estar inválidos"
            fi
        else
            echo "  ❌ Estrutura incorreta"
        fi
        
        # Verificar campos obrigatórios
        FRANQUIA_REC=$(jq -r '.plano_recomendado.valor_franquia' "$file")
        FRANQUIA_ALT=$(jq -r '.plano_alternativo.valor_franquia' "$file")
        
        if [ "$FRANQUIA_REC" != "null" ] && [ "$FRANQUIA_ALT" != "null" ]; then
            echo "  ✅ Campos de franquia presentes"
        else
            echo "  ⚠️ Campos de franquia ausentes"
        fi
    else
        echo "  ❌ JSON inválido"
    fi
    
    echo ""
done

# Resumo da validação
echo "=== Resumo da Validação ==="
echo "Arquivos de progresso: $PROGRESS_COUNT total, $PROGRESS_VALID válidos"
echo "Arquivos de resultados: $RESULT_COUNT total, $RESULT_VALID válidos"

if [ $PROGRESS_VALID -eq $PROGRESS_COUNT ] && [ $RESULT_VALID -eq $RESULT_COUNT ]; then
    echo "✅ Validação bem-sucedida!"
else
    echo "⚠️ Validação com problemas identificados"
fi

echo "=== Validação de Arquivos concluída ==="

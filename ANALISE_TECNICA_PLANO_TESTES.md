# Análise Técnica - Plano de Testes API V4

## Resumo Executivo

**Analista**: Engenheiro de Software  
**Data**: 01/10/2025  
**Documento Analisado**: `PLANO_TESTES_API_V4_PROGRESS_TRACKER.md`  
**Status**: Aprovado com Melhorias Necessárias  

## Avaliação Geral

### Pontos Fortes ✅
- **Cobertura funcional adequada**: Abrange todos os cenários críticos
- **Scripts automatizados**: Reduz intervenção manual
- **Cronograma definido**: 3 dias bem estruturados
- **Critérios de sucesso claros**: Objetivos mensuráveis

### Pontos Críticos ⚠️
- **Falta de validação de pré-condições**
- **Dados de teste hardcoded**
- **Ausência de timeouts**
- **Falta de cleanup automático**

## Análise Detalhada

### 1. Problemas Identificados

#### 1.1 Falta de Validação de Pré-condições
```bash
# PROBLEMA: Não verifica se o RPA está configurado para usar a API V4
# RISCO: Testes podem falhar silenciosamente
# IMPACTO: Alto - Pode gerar falsos positivos
```

#### 1.2 Dados de Teste Hardcoded
```bash
# PROBLEMA: CPF, placa, CEP fixos em todos os testes
# RISCO: Dados podem estar inválidos ou expirados
# IMPACTO: Médio - Pode causar falhas intermitentes
```

#### 1.3 Ausência de Timeouts
```bash
# PROBLEMA: Loops infinitos sem timeout
# RISCO: Testes podem travar indefinidamente
# IMPACTO: Alto - Pode bloquear execução
```

#### 1.4 Falta de Cleanup
```bash
# PROBLEMA: Não limpa sessões ativas após testes
# RISCO: Acúmulo de processos e recursos
# IMPACTO: Médio - Pode degradar performance
```

### 2. Melhorias Técnicas Propostas

#### 2.1 Script de Preparação Aprimorado
```bash
#!/bin/bash
# test_prepare_enhanced.sh

set -e  # Exit on any error

echo "=== Preparação do Ambiente de Teste ==="

# Verificar se estamos no servidor correto
if [ "$(hostname)" != "ubuntu-2gb-hel1-1" ]; then
    echo "❌ ERRO: Execute este script no servidor Hetzner"
    exit 1
fi

# Verificar serviços críticos
echo "Verificando serviços..."
services=("nginx" "php8.3-fpm" "redis-server")
for service in "${services[@]}"; do
    if ! systemctl is-active --quiet "$service"; then
        echo "❌ ERRO: Serviço $service não está ativo"
        exit 1
    fi
    echo "✅ $service está ativo"
done

# Verificar se a API V4 está respondendo
echo "Verificando API V4..."
if ! curl -s http://localhost/api/rpa/health | jq -e '.success' > /dev/null; then
    echo "❌ ERRO: API V4 não está respondendo"
    exit 1
fi
echo "✅ API V4 está respondendo"

# Limpar dados de teste anteriores
echo "Limpando dados de teste anteriores..."
rm -f /opt/imediatoseguros-rpa/rpa_data/progress_test_*
rm -f /opt/imediatoseguros-rpa/rpa_data/history_test_*
rm -f /opt/imediatoseguros-rpa/dados_planos_seguro_test_*
rm -f /opt/imediatoseguros-rpa/sessions/test_*

# Verificar permissões
echo "Verificando permissões..."
directories=("/opt/imediatoseguros-rpa/rpa_data" "/opt/imediatoseguros-rpa/sessions" "/opt/imediatoseguros-rpa/scripts")
for dir in "${directories[@]}"; do
    if [ ! -w "$dir" ]; then
        echo "❌ ERRO: Diretório $dir não é gravável"
        exit 1
    fi
    echo "✅ $dir é gravável"
done

# Verificar se os arquivos Python têm --data implementado
echo "Verificando implementação --data..."
if ! grep -q "add_argument.*--data" /opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py; then
    echo "❌ ERRO: RPA Modular não tem --data implementado"
    exit 1
fi
echo "✅ RPA Modular tem --data implementado"

if ! grep -q "add_argument.*--data" /opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py; then
    echo "❌ ERRO: RPA Principal não tem --data implementado"
    exit 1
fi
echo "✅ RPA Principal tem --data implementado"

echo "✅ Preparação concluída com sucesso"
```

#### 2.2 Script de Teste com Timeout e Validação
```bash
#!/bin/bash
# test_modular_enhanced.sh

set -e

# Configurações
API_URL="http://37.27.92.160"
TIMEOUT=900  # 15 minutos
POLL_INTERVAL=2
TEST_DATA='{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'

echo "=== Teste RPA Modular ==="

# Função de cleanup
cleanup() {
    if [ ! -z "$SESSION_ID" ]; then
        echo "Limpando sessão $SESSION_ID..."
        # Aqui poderia implementar um endpoint para cancelar sessão
    fi
}
trap cleanup EXIT

# Iniciar sessão
echo "Iniciando sessão RPA Modular..."
RESPONSE=$(curl -s -X POST "$API_URL/api/rpa/start" \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

SESSION_ID=$(echo "$RESPONSE" | jq -r '.session_id')
if [ "$SESSION_ID" = "null" ] || [ -z "$SESSION_ID" ]; then
    echo "❌ ERRO: Falha ao criar sessão"
    echo "Resposta: $RESPONSE"
    exit 1
fi

echo "✅ Sessão criada: $SESSION_ID"

# Monitorar progresso com timeout
echo "Monitorando progresso (timeout: ${TIMEOUT}s)..."
START_TIME=$(date +%s)
LAST_ETAPA=0

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "❌ ERRO: Timeout atingido (${TIMEOUT}s)"
        exit 1
    fi
    
    PROGRESS=$(curl -s "$API_URL/api/rpa/progress/$SESSION_ID")
    if [ $? -ne 0 ]; then
        echo "❌ ERRO: Falha ao consultar progresso"
        exit 1
    fi
    
    STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
    ETAPA=$(echo "$PROGRESS" | jq -r '.progress.etapa_atual')
    TOTAL=$(echo "$PROGRESS" | jq -r '.progress.total_etapas')
    PERCENTUAL=$(echo "$PROGRESS" | jq -r '.progress.percentual')
    MENSAGEM=$(echo "$PROGRESS" | jq -r '.progress.mensagem')
    
    # Só imprimir quando a etapa mudar
    if [ "$ETAPA" != "$LAST_ETAPA" ]; then
        echo "[$(date)] Etapa $ETAPA/$TOTAL ($PERCENTUAL%) - $STATUS: $MENSAGEM"
        LAST_ETAPA=$ETAPA
    fi
    
    # Verificar sucesso
    if [ "$STATUS" = "success" ] && [ "$ETAPA" = "5" ]; then
        ESTIMATIVAS=$(echo "$PROGRESS" | jq -r '.progress.estimativas.capturadas')
        if [ "$ESTIMATIVAS" = "true" ]; then
            echo "✅ Estimativas capturadas com sucesso!"
            echo "$PROGRESS" | jq '.progress.estimativas.dados'
            
            # Validar arquivo de progresso
            PROGRESS_FILE="/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json"
            if [ -f "$PROGRESS_FILE" ]; then
                echo "✅ Arquivo de progresso gerado: $PROGRESS_FILE"
            else
                echo "❌ ERRO: Arquivo de progresso não encontrado"
                exit 1
            fi
            break
        fi
    fi
    
    # Verificar erro
    if [ "$STATUS" = "failed" ] || [ "$STATUS" = "error" ]; then
        echo "❌ ERRO na execução: $MENSAGEM"
        echo "Progresso completo: $PROGRESS"
        exit 1
    fi
    
    sleep $POLL_INTERVAL
done

echo "✅ Teste RPA Modular concluído com sucesso"
```

#### 2.3 Script de Validação Aprimorado
```bash
#!/bin/bash
# test_validation_enhanced.sh

set -e

echo "=== Validação Completa de Arquivos ==="

# Função para validar JSON
validate_json() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "❌ Arquivo não encontrado: $file"
        return 1
    fi
    
    if ! jq . "$file" > /dev/null 2>&1; then
        echo "❌ JSON inválido: $file"
        return 1
    fi
    
    echo "✅ JSON válido: $file"
    return 0
}

# Validar arquivos de progresso
echo "=== Validando arquivos de progresso ==="
PROGRESS_FILES=$(find /opt/imediatoseguros-rpa/rpa_data/ -name "progress_test_*.json" -o -name "progress_rpa_v4_*.json" | head -10)

if [ -z "$PROGRESS_FILES" ]; then
    echo "❌ Nenhum arquivo de progresso encontrado"
    exit 1
fi

for file in $PROGRESS_FILES; do
    echo "Validando: $(basename "$file")"
    
    if ! validate_json "$file"; then
        continue
    fi
    
    # Verificar campos obrigatórios
    ETAPA=$(jq -r '.etapa_atual' "$file")
    STATUS=$(jq -r '.status' "$file")
    SESSION_ID=$(jq -r '.session_id' "$file")
    TIMESTAMP=$(jq -r '.timestamp_atualizacao' "$file")
    
    echo "  - Etapa: $ETAPA"
    echo "  - Status: $STATUS"
    echo "  - Session ID: $SESSION_ID"
    echo "  - Timestamp: $TIMESTAMP"
    
    # Validar estimativas
    if [ "$ETAPA" = "5" ] || [ "$ETAPA" = "15" ]; then
        ESTIMATIVAS=$(jq -r '.dados_extra.estimativas_tela_5' "$file")
        if [ "$ESTIMATIVAS" != "null" ] && [ "$ESTIMATIVAS" != "false" ]; then
            COBERTURAS=$(jq -r '.dados_extra.estimativas_tela_5.coberturas_detalhadas | length' "$file")
            echo "  - ✅ Estimativas capturadas ($COBERTURAS coberturas)"
        else
            echo "  - ❌ Estimativas não capturadas"
        fi
    fi
    
    # Validar resultados finais
    if [ "$ETAPA" = "15" ]; then
        PLANO_REC=$(jq -r '.dados_extra.plano_recomendado' "$file")
        if [ "$PLANO_REC" != "null" ]; then
            VALOR_REC=$(jq -r '.dados_extra.plano_recomendado.valor' "$file")
            echo "  - ✅ Resultados finais capturados (Recomendado: $VALOR_REC)"
        else
            echo "  - ❌ Resultados finais não capturados"
        fi
    fi
    
    echo ""
done

# Validar arquivos de resultados
echo "=== Validando arquivos de resultados ==="
RESULT_FILES=$(find /opt/imediatoseguros-rpa/ -name "dados_planos_seguro_*.json" | head -5)

for file in $RESULT_FILES; do
    echo "Validando: $(basename "$file")"
    
    if ! validate_json "$file"; then
        continue
    fi
    
    PLANO_REC=$(jq -r '.plano_recomendado.valor' "$file")
    PLANO_ALT=$(jq -r '.plano_alternativo.valor' "$file")
    
    echo "  - Plano Recomendado: $PLANO_REC"
    echo "  - Plano Alternativo: $PLANO_ALT"
    
    # Validar se os valores são válidos
    if [[ "$PLANO_REC" =~ ^R\$[0-9.,]+$ ]] && [[ "$PLANO_ALT" =~ ^R\$[0-9.,]+$ ]]; then
        echo "  - ✅ Valores válidos"
    else
        echo "  - ❌ Valores inválidos"
    fi
    
    echo ""
done

echo "✅ Validação concluída"
```

## Recomendações de Implementação

### 1. Estrutura de Diretórios Proposta
```
tests/
├── scripts/
│   ├── test_prepare_enhanced.sh
│   ├── test_modular_enhanced.sh
│   ├── test_principal_enhanced.sh
│   ├── test_concurrent_enhanced.sh
│   └── test_validation_enhanced.sh
├── data/
│   ├── test_data_valid.json
│   └── test_data_invalid.json
├── reports/
│   └── test_report_template.md
└── README.md
```

### 2. Configuração Centralizada
```bash
# test_config.sh
export API_URL="http://37.27.92.160"
export TIMEOUT=900
export POLL_INTERVAL=2
export TEST_DATA_DIR="./tests/data"
export REPORTS_DIR="./tests/reports"
```

### 3. Relatório Automatizado
```bash
#!/bin/bash
# generate_report.sh

REPORT_FILE="$REPORTS_DIR/test_report_$(date +%Y%m%d_%H%M%S).md"

cat > "$REPORT_FILE" << EOF
# Relatório de Testes - API V4 Progress Tracker

## Data: $(date)
## Executor: $(whoami)
## Servidor: $(hostname)

### Resumo Executivo
- Total de testes: [AUTO-GERADO]
- Sucessos: [AUTO-GERADO]
- Falhas: [AUTO-GERADO]
- Taxa de sucesso: [AUTO-GERADO]%

### Detalhes dos Testes
[AUTO-GERADO baseado nos logs]

### Problemas Identificados
[AUTO-GERADO baseado nos logs de erro]

### Recomendações
[AUTO-GERADO baseado nos resultados]
EOF

echo "Relatório gerado: $REPORT_FILE"
```

## Cronograma Revisado

### Dia 1: Preparação e Validação
- **09:00** - Preparação do ambiente
- **09:30** - Validação de pré-condições
- **10:00** - Teste RPA Modular
- **11:00** - Validação de arquivos
- **11:30** - Análise de resultados

### Dia 2: Teste Principal e Concorrência
- **09:00** - Teste RPA Principal
- **11:00** - Teste de execuções concorrentes
- **12:00** - Validação de arquivos
- **12:30** - Análise de resultados

### Dia 3: Erros e Relatório
- **09:00** - Teste de tratamento de erros
- **10:00** - Teste de recuperação
- **10:30** - Validação final
- **11:00** - Geração de relatório
- **11:30** - Análise final

## Critérios de Aprovação

### Obrigatórios ✅
- [ ] Validação de pré-condições implementada
- [ ] Timeouts configurados (15 minutos)
- [ ] Cleanup automático funcionando
- [ ] Tratamento de erros robusto
- [ ] Validação de JSON implementada

### Recomendados 📋
- [ ] Dados de teste dinâmicos
- [ ] Relatórios automatizados
- [ ] Configuração centralizada
- [ ] Logs estruturados
- [ ] Métricas de performance

## Conclusão

O plano original é um **bom ponto de partida**, mas precisa de **melhorias técnicas significativas** para ser adequado para produção. As melhorias propostas aumentam a **robustez**, **confiabilidade** e **manutenibilidade** dos testes.

### Recomendação Final
**APROVAR** com implementação das melhorias antes da execução.

### Próximos Passos
1. **Implementar** as melhorias técnicas
2. **Testar** os scripts aprimorados
3. **Validar** em ambiente de desenvolvimento
4. **Executar** em produção
5. **Monitorar** resultados

---

**Analista**: Engenheiro de Software  
**Data**: 01/10/2025  
**Status**: Aprovado com Melhorias  
**Próxima Revisão**: Após implementação das melhorias

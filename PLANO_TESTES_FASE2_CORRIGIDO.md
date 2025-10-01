# Plano de Testes - Fase 2 - API V4 RPA (Corrigido)

## Resumo Executivo

### Situação Atual
- **RPA Principal**: ✅ Executado com sucesso
- **RPA Modular**: ⚠️ Em execução (inconclusivo) - **NÃO CRÍTICO**
- **API V4**: ✅ Funcional
- **Progress Tracker**: ❌ **PROBLEMA IDENTIFICADO E CORRIGIDO**
- **Dados Capturados**: ✅ Planos de seguro obtidos

### Problema Identificado e Corrigido
- **Causa**: RPA usando Redis automaticamente, mas PHP MonitorService lendo apenas arquivos JSON
- **Solução**: Forçar RPA a usar `--progress-tracker json` em vez de `auto`
- **Resultado**: Progress tracker funcionará em tempo real via arquivos JSON

### Objetivo da Fase 2
Concluir os testes pendentes, validar a correção do progress tracker e preparar o sistema para produção.

## Análise dos Problemas Identificados

### 1. Progress Tracker Corrigido ✅
- **Status**: Problema identificado e solução implementada
- **Impacto**: **ALTO** (crítico para produção)
- **Causa**: RPA usando Redis, PHP lendo apenas JSON
- **Solução**: Forçar RPA a usar `--progress-tracker json`

### 2. Testes Concorrentes Não Executados
- **Status**: Não executados
- **Impacto**: **ALTO** (crítico para produção)
- **Causa**: Priorização do progress tracker
- **Ação**: Executar testes concorrentes

### 3. Validação de Arquivos Não Executada
- **Status**: Não executada
- **Impacto**: **MÉDIO** (importante para produção)
- **Causa**: Dependência dos testes anteriores
- **Ação**: Executar validação de arquivos

### 4. RPA Modular Inconclusivo
- **Status**: Em execução
- **Impacto**: **BAIXO** (não crítico para produção)
- **Causa**: Execução em background sem monitoramento adequado
- **Ação**: Investigar e concluir (baixa prioridade)

## Plano de Testes - Fase 2 (Corrigido)

### Semana 1: Correções Críticas para Produção

#### Dia 1: Correção do Progress Tracker ✅
- **09:00** - Identificar problema (RPA usando Redis, PHP lendo JSON)
- **09:30** - Implementar correção (forçar `--progress-tracker json`)
- **10:00** - Testar progress tracker em tempo real
- **10:30** - Validar arquivos JSON sendo criados
- **11:00** - Confirmar funcionamento

#### Dia 2: Testes Concorrentes do RPA Principal
- **09:00** - Preparar ambiente para testes concorrentes
- **09:30** - Executar teste de 2 sessões simultâneas
- **10:00** - Executar teste de 3 sessões simultâneas
- **10:30** - Executar teste de 5 sessões simultâneas
- **11:00** - Analisar resultados e performance

#### Dia 3: Validação de Arquivos
- **09:00** - Executar validação de arquivos de progresso
- **09:30** - Executar validação de arquivos de resultados
- **10:00** - Validar estrutura JSON
- **10:30** - Validar campos obrigatórios
- **11:00** - Gerar relatório de validação

#### Dia 4: Testes de Carga e Performance
- **09:00** - Executar testes de carga (10 sessões)
- **09:30** - Monitorar performance do sistema
- **10:00** - Testar limites de recursos
- **10:30** - Otimizar configurações
- **11:00** - Validar melhorias

#### Dia 5: Relatório e Análise
- **09:00** - Compilar resultados dos testes
- **09:30** - Analisar performance e confiabilidade
- **10:00** - Identificar melhorias necessárias
- **10:30** - Gerar relatório final
- **11:00** - Apresentar conclusões

### Semana 2: Melhorias e Otimizações

#### Dia 1: Métricas de Performance
- **09:00** - Implementar coleta de métricas
- **09:30** - Configurar monitoramento de CPU e memória
- **10:00** - Implementar logs de performance
- **10:30** - Testar coleta de métricas
- **11:00** - Validar funcionamento

#### Dia 2: Alertas de Falha
- **09:00** - Implementar sistema de alertas
- **09:30** - Configurar notificações por email
- **10:00** - Implementar alertas por Slack
- **10:30** - Testar sistema de alertas
- **11:00** - Validar funcionamento

#### Dia 3: Cache e Otimizações
- **09:00** - Implementar cache Redis
- **09:30** - Otimizar consultas ao banco de dados
- **10:00** - Implementar compressão de dados
- **10:30** - Testar otimizações
- **11:00** - Validar melhorias de performance

#### Dia 4: Suporte a Múltiplas Sessões
- **09:00** - Implementar gerenciamento de sessões
- **09:30** - Configurar limites de sessões simultâneas
- **10:00** - Implementar fila de processamento
- **10:30** - Testar múltiplas sessões
- **11:00** - Validar funcionamento

#### Dia 5: Sistema de Notificações
- **09:00** - Implementar notificações em tempo real
- **09:30** - Configurar WebSocket
- **10:00** - Implementar notificações push
- **10:30** - Testar sistema de notificações
- **11:00** - Validar funcionamento

## Scripts de Teste Detalhados

### 1. Script de Correção do Progress Tracker

```bash
#!/bin/bash
# Script para corrigir e testar progress tracker

echo "=== Correção do Progress Tracker ==="

# 1. Verificar problema atual
echo "1. Verificando problema atual..."
SESSION_ID=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')

echo "Sessão criada: $SESSION_ID"

# 2. Verificar se arquivo JSON foi criado
echo "2. Verificando arquivo JSON..."
sleep 5
if [ -f "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" ]; then
    echo "✅ Arquivo JSON criado"
    cat "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" | jq .
else
    echo "❌ Arquivo JSON não criado"
fi

# 3. Verificar progresso via API
echo "3. Verificando progresso via API..."
PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
echo "$PROGRESS" | jq .

# 4. Monitorar em tempo real
echo "4. Monitorando em tempo real..."
START_TIME=$(date +%s)
TIMEOUT=300  # 5 minutos

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "Timeout atingido (${TIMEOUT}s)"
        break
    fi
    
    PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
    STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
    ETAPA=$(echo "$PROGRESS" | jq -r '.progress.etapa_atual')
    PERCENTUAL=$(echo "$PROGRESS" | jq -r '.progress.percentual')
    MENSAGEM=$(echo "$PROGRESS" | jq -r '.progress.mensagem')
    
    echo "$(date): Status: $STATUS, Etapa: $ETAPA, Percentual: $PERCENTUAL, Mensagem: $MENSAGEM"
    
    if [ "$STATUS" = "success" ] || [ "$STATUS" = "failed" ]; then
        echo "Execução concluída com status: $STATUS"
        break
    fi
    
    sleep 2
done

echo "=== Correção do Progress Tracker concluída ==="
```

### 2. Script de Testes Concorrentes

```bash
#!/bin/bash
# Script para testes concorrentes

echo "=== Testes Concorrentes ==="

# Função para iniciar sessão
start_session() {
    local session_num=$1
    curl -s -X POST http://37.27.92.160/api/rpa/start \
      -H "Content-Type: application/json" \
      -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id'
}

# Iniciar múltiplas sessões
echo "1. Iniciando 5 sessões simultâneas..."
for i in {1..5}; do
    SESSION_ID=$(start_session $i)
    echo "Sessão $i: $SESSION_ID"
    echo "$SESSION_ID" >> /tmp/sessions.txt
done

# Monitorar todas as sessões
echo "2. Monitorando todas as sessões..."
START_TIME=$(date +%s)
TIMEOUT=1800  # 30 minutos

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "Timeout atingido (${TIMEOUT}s)"
        break
    fi
    
    echo "=== Status das Sessões ($(date)) ==="
    ALL_COMPLETED=true
    
    while read -r SESSION_ID; do
        PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
        STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
        ETAPA=$(echo "$PROGRESS" | jq -r '.progress.etapa_atual')
        PERCENTUAL=$(echo "$PROGRESS" | jq -r '.progress.percentual')
        
        echo "Sessão $SESSION_ID: $STATUS (Etapa $ETAPA, $PERCENTUAL%)"
        
        if [ "$STATUS" != "success" ] && [ "$STATUS" != "failed" ]; then
            ALL_COMPLETED=false
        fi
    done < /tmp/sessions.txt
    
    if [ "$ALL_COMPLETED" = true ]; then
        echo "Todas as sessões concluídas!"
        break
    fi
    
    sleep 10
done

# Limpar arquivo temporário
rm -f /tmp/sessions.txt

echo "=== Testes Concorrentes concluídos ==="
```

### 3. Script de Teste de Carga

```bash
#!/bin/bash
# Script de teste de carga

echo "=== Teste de Carga ==="

# Configurações
CONCURRENT_SESSIONS=10
TEST_DURATION=300  # 5 minutos
LOG_FILE="/tmp/load_test_$(date +%Y%m%d_%H%M%S).log"

# Função para iniciar sessão
start_session() {
    local session_num=$1
    local start_time=$(date +%s)
    
    SESSION_ID=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
      -H "Content-Type: application/json" \
      -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')
    
    local end_time=$(date +%s)
    local response_time=$((end_time - start_time))
    
    echo "$(date): Sessão $session_num criada: $SESSION_ID (${response_time}s)" >> "$LOG_FILE"
    echo "$SESSION_ID" >> /tmp/sessions_load.txt
}

# Função para monitorar sessão
monitor_session() {
    local session_id=$1
    local start_time=$(date +%s)
    
    while true; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        if [ $elapsed -gt $TEST_DURATION ]; then
            echo "$(date): Timeout para sessão $session_id" >> "$LOG_FILE"
            break
        fi
        
        PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$session_id)
        STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
        
        if [ "$STATUS" = "success" ] || [ "$STATUS" = "failed" ]; then
            local end_time=$(date +%s)
            local total_time=$((end_time - start_time))
            echo "$(date): Sessão $session_id concluída: $STATUS (${total_time}s)" >> "$LOG_FILE"
            break
        fi
        
        sleep 5
    done
}

# Executar teste de carga
echo "Iniciando teste de carga com $CONCURRENT_SESSIONS sessões..."
echo "Duração: $TEST_DURATION segundos"
echo "Log: $LOG_FILE"

# Iniciar sessões
for i in $(seq 1 $CONCURRENT_SESSIONS); do
    start_session $i &
done

# Aguardar todas as sessões iniciarem
sleep 10

# Monitorar todas as sessões
while read -r SESSION_ID; do
    monitor_session "$SESSION_ID" &
done < /tmp/sessions_load.txt

# Aguardar conclusão
wait

# Limpar arquivo temporário
rm -f /tmp/sessions_load.txt

echo "=== Teste de carga concluído ==="
echo "Log salvo em: $LOG_FILE"
```

### 4. Script de Validação de Arquivos

```bash
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
```

### 5. Script de Investigação do RPA Modular (Baixa Prioridade)

```bash
#!/bin/bash
# Script para investigar RPA modular (baixa prioridade)

echo "=== Investigação do RPA Modular (Baixa Prioridade) ==="

# Verificar processos em execução
echo "1. Verificando processos Python em execução..."
ps aux | grep python | grep modular

# Verificar logs
echo "2. Verificando logs recentes..."
tail -50 /opt/imediatoseguros-rpa/logs/rpa_v4_*.log

# Verificar arquivos de progresso
echo "3. Verificando arquivos de progresso..."
ls -la /opt/imediatoseguros-rpa/rpa_data/ | grep modular

# Verificar status do Redis
echo "4. Verificando status do Redis..."
redis-cli ping

# Executar teste manual (opcional)
echo "5. Executando teste manual (opcional)..."
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --config /opt/imediatoseguros-rpa/parametros.json --session test_modular_investigation

echo "=== Investigação do RPA Modular concluída ==="
echo "NOTA: RPA Modular não será utilizado em produção"
```

## Cronograma Detalhado

### Semana 1: Correções Críticas para Produção

| Dia | Atividade | Prioridade | Dependências | Status |
|-----|-----------|------------|--------------|--------|
| 1 | Correção do Progress Tracker | **CRÍTICA** | Nenhuma | ✅ Concluída |
| 2 | Testes Concorrentes do RPA Principal | **CRÍTICA** | Progress Tracker | ⏳ Pendente |
| 3 | Validação de Arquivos | **IMPORTANTE** | Nenhuma | ⏳ Pendente |
| 4 | Testes de Carga e Performance | **IMPORTANTE** | Testes Concorrentes | ⏳ Pendente |
| 5 | Relatório e Análise | **IMPORTANTE** | Todos os testes | ⏳ Pendente |

### Semana 2: Melhorias e Otimizações

| Dia | Atividade | Prioridade | Dependências | Status |
|-----|-----------|------------|--------------|--------|
| 1 | Métricas de Performance | Desejável | Semana 1 | ⏳ Pendente |
| 2 | Alertas de Falha | Desejável | Métricas | ⏳ Pendente |
| 3 | Cache e Otimizações | Desejável | Alertas | ⏳ Pendente |
| 4 | Suporte a Múltiplas Sessões | Desejável | Cache | ⏳ Pendente |
| 5 | Sistema de Notificações | Desejável | Múltiplas Sessões | ⏳ Pendente |

## Critérios de Sucesso

### Semana 1 (Crítico para Produção)
- [x] Progress tracker corrigido e funcionando
- [ ] Testes concorrentes executados com sucesso
- [ ] Validação de arquivos concluída
- [ ] Testes de carga e performance validados
- [ ] Relatório final gerado

### Semana 2 (Melhorias)
- [ ] Métricas de performance implementadas
- [ ] Sistema de alertas funcionando
- [ ] Cache e otimizações implementadas
- [ ] Suporte a múltiplas sessões
- [ ] Sistema de notificações funcionando

## Riscos e Mitigações

### Riscos Identificados

#### 1. Progress Tracker Complexo ✅ RESOLVIDO
- **Probabilidade**: N/A
- **Impacto**: N/A
- **Mitigação**: Problema identificado e corrigido

#### 2. Performance em Testes Concorrentes
- **Probabilidade**: Média
- **Impacto**: Alto
- **Mitigação**: Monitoramento contínuo e ajustes

#### 3. Validação de Arquivos Demorada
- **Probabilidade**: Baixa
- **Impacto**: Médio
- **Mitigação**: Automação e otimização

#### 4. RPA Modular Não Concluir
- **Probabilidade**: Média
- **Impacto**: Baixo (não crítico para produção)
- **Mitigação**: Investigar causa raiz e implementar correções

### Plano de Contingência

#### Se Testes Concorrentes Falharem
1. Reduzir número de sessões
2. Implementar fila de processamento
3. Otimizar recursos
4. Monitorar performance

#### Se Validação de Arquivos Falhar
1. Verificar estrutura de dados
2. Corrigir scripts de validação
3. Implementar validação incremental
4. Adicionar logs detalhados

#### Se RPA Modular Falhar
1. Investigar logs detalhados
2. Verificar configurações do Redis
3. Testar execução manual
4. Implementar correções (baixa prioridade)

## Métricas de Acompanhamento

### Métricas Técnicas
- **Tempo de execução**: < 3 minutos por sessão (RPA Principal)
- **Taxa de sucesso**: > 95% (RPA Principal)
- **Uso de memória**: < 3GB
- **Uso de CPU**: < 80%

### Métricas de Qualidade
- **Cobertura de testes**: 100%
- **Validação de dados**: 100%
- **Sincronização**: < 5 segundos
- **Disponibilidade**: > 99%

## Próximos Passos

### Imediatos (Próximos 3 dias)
1. **Executar testes concorrentes do RPA Principal**
2. **Executar validação de arquivos**
3. **Executar testes de carga e performance**
4. **Gerar relatório de progresso**

### Médio Prazo (Próximas 2 semanas)
1. **Implementar métricas de performance**
2. **Implementar sistema de alertas**
3. **Otimizar configurações**
4. **Implementar melhorias**

### Longo Prazo (Próximos 2 meses)
1. **Implementar cache e otimizações**
2. **Implementar suporte a múltiplas sessões**
3. **Implementar sistema de notificações**
4. **Otimizar performance geral**

## Conclusão

O Plano de Testes da Fase 2 (Corrigido) foi desenvolvido para concluir os testes pendentes, validar a correção do progress tracker e preparar o sistema para produção, **focando no RPA Principal que será utilizado em produção**.

### Benefícios Esperados
- **Sistema 100% funcional para produção**
- **Progress tracker funcionando em tempo real**
- **Performance otimizada**
- **Monitoramento completo**
- **Alta disponibilidade**
- **Escalabilidade garantida**

### Entregáveis
- **Relatório de conclusão dos testes**
- **Sistema otimizado e validado para produção**
- **Progress tracker funcionando via JSON**
- **Documentação atualizada**
- **Scripts de monitoramento**
- **Plano de manutenção**

### Nota Importante
O RPA Modular não será utilizado em produção e tem prioridade baixa nos testes. O foco principal é garantir que o RPA Principal esteja 100% funcional e otimizado para produção.

### Correção Implementada
- **Problema**: RPA usando Redis, PHP lendo apenas JSON
- **Solução**: Forçar RPA a usar `--progress-tracker json`
- **Resultado**: Progress tracker funcionando em tempo real

---

**Documento gerado em:** 01/10/2025 16:30  
**Responsável:** Equipe de Desenvolvimento  
**Status:** Pronto para implementação com correção aplicada  
**Próxima revisão:** 02/10/2025

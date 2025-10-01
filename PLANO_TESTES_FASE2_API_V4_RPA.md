# Plano de Testes - Fase 2 - API V4 RPA

## Resumo Executivo

### Situação Atual
- **RPA Principal**: ✅ Executado com sucesso
- **RPA Modular**: ⚠️ Em execução (inconclusivo)
- **API V4**: ✅ Funcional
- **Progress Tracker**: ⚠️ Operacional, mas com limitações
- **Dados Capturados**: ✅ Planos de seguro obtidos

### Objetivo da Fase 2
Concluir os testes pendentes, corrigir problemas identificados e validar o sistema para produção.

## Análise dos Problemas Identificados

### 1. RPA Modular Inconclusivo
- **Status**: Em execução
- **Impacto**: Alto
- **Causa Provável**: Execução em background sem monitoramento adequado
- **Ação**: Investigar e concluir

### 2. Progress Tracker Não Atualizado em Tempo Real
- **Status**: Operacional, mas com limitações
- **Impacto**: Médio
- **Causa Provável**: Falta de sincronização entre Redis e JSON
- **Ação**: Implementar atualização em tempo real

### 3. Testes Concorrentes Não Executados
- **Status**: Não executados
- **Impacto**: Médio
- **Causa Provável**: Priorização do RPA principal
- **Ação**: Executar testes concorrentes

### 4. Validação de Arquivos Não Executada
- **Status**: Não executada
- **Impacto**: Baixo
- **Causa Provável**: Dependência dos testes anteriores
- **Ação**: Executar validação de arquivos

## Plano de Testes - Fase 2

### Semana 1: Conclusão dos Testes Pendentes

#### Dia 1: Investigação e Correção do RPA Modular
- **09:00** - Verificar status do RPA modular
- **09:30** - Investigar causa da execução inconclusiva
- **10:00** - Implementar correções necessárias
- **10:30** - Executar teste do RPA modular
- **11:00** - Validar resultados

#### Dia 2: Implementação do Progress Tracker em Tempo Real
- **09:00** - Analisar implementação atual do progress tracker
- **09:30** - Identificar pontos de falha na sincronização
- **10:00** - Implementar atualização em tempo real
- **10:30** - Testar sincronização Redis + JSON
- **11:00** - Validar funcionamento

#### Dia 3: Testes Concorrentes
- **09:00** - Preparar ambiente para testes concorrentes
- **09:30** - Executar teste de 2 sessões simultâneas
- **10:00** - Executar teste de 3 sessões simultâneas
- **10:30** - Executar teste de 5 sessões simultâneas
- **11:00** - Analisar resultados e performance

#### Dia 4: Validação de Arquivos
- **09:00** - Executar validação de arquivos de progresso
- **09:30** - Executar validação de arquivos de resultados
- **10:00** - Validar estrutura JSON
- **10:30** - Validar campos obrigatórios
- **11:00** - Gerar relatório de validação

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

### 1. Script de Investigação do RPA Modular

```bash
#!/bin/bash
# Script para investigar e corrigir RPA modular

echo "=== Investigação do RPA Modular ==="

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

# Executar teste manual
echo "5. Executando teste manual..."
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --config /opt/imediatoseguros-rpa/parametros.json --session test_modular_investigation

echo "=== Investigação concluída ==="
```

### 2. Script de Teste do Progress Tracker

```bash
#!/bin/bash
# Script para testar progress tracker em tempo real

echo "=== Teste do Progress Tracker em Tempo Real ==="

# Iniciar sessão
echo "1. Iniciando nova sessão..."
SESSION_ID=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')

echo "Sessão criada: $SESSION_ID"

# Monitorar progresso em tempo real
echo "2. Monitorando progresso em tempo real..."
START_TIME=$(date +%s)
TIMEOUT=900  # 15 minutos

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

echo "=== Teste do Progress Tracker concluído ==="
```

### 3. Script de Testes Concorrentes

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

## Cronograma Detalhado

### Semana 1: Conclusão dos Testes Pendentes

| Dia | Atividade | Horário | Responsável | Status |
|-----|-----------|---------|-------------|--------|
| 1 | Investigação e Correção do RPA Modular | 09:00-11:00 | Dev Team | ⏳ Pendente |
| 2 | Implementação do Progress Tracker em Tempo Real | 09:00-11:00 | Dev Team | ⏳ Pendente |
| 3 | Testes Concorrentes | 09:00-11:00 | Dev Team | ⏳ Pendente |
| 4 | Validação de Arquivos | 09:00-11:00 | Dev Team | ⏳ Pendente |
| 5 | Relatório e Análise | 09:00-11:00 | Dev Team | ⏳ Pendente |

### Semana 2: Melhorias e Otimizações

| Dia | Atividade | Horário | Responsável | Status |
|-----|-----------|---------|-------------|--------|
| 1 | Métricas de Performance | 09:00-11:00 | Dev Team | ⏳ Pendente |
| 2 | Alertas de Falha | 09:00-11:00 | Dev Team | ⏳ Pendente |
| 3 | Cache e Otimizações | 09:00-11:00 | Dev Team | ⏳ Pendente |
| 4 | Suporte a Múltiplas Sessões | 09:00-11:00 | Dev Team | ⏳ Pendente |
| 5 | Sistema de Notificações | 09:00-11:00 | Dev Team | ⏳ Pendente |

## Critérios de Sucesso

### Semana 1
- [ ] RPA modular executado com sucesso
- [ ] Progress tracker atualizado em tempo real
- [ ] Testes concorrentes executados
- [ ] Validação de arquivos concluída
- [ ] Relatório final gerado

### Semana 2
- [ ] Métricas de performance implementadas
- [ ] Sistema de alertas funcionando
- [ ] Cache e otimizações implementadas
- [ ] Suporte a múltiplas sessões
- [ ] Sistema de notificações funcionando

## Riscos e Mitigações

### Riscos Identificados

#### 1. RPA Modular Não Concluir
- **Probabilidade**: Média
- **Impacto**: Alto
- **Mitigação**: Investigar causa raiz e implementar correções

#### 2. Progress Tracker Complexo
- **Probabilidade**: Alta
- **Impacto**: Médio
- **Mitigação**: Implementação incremental com testes

#### 3. Performance em Testes Concorrentes
- **Probabilidade**: Média
- **Impacto**: Médio
- **Mitigação**: Monitoramento contínuo e ajustes

#### 4. Validação de Arquivos Demorada
- **Probabilidade**: Baixa
- **Impacto**: Baixo
- **Mitigação**: Automação e otimização

### Plano de Contingência

#### Se RPA Modular Falhar
1. Investigar logs detalhados
2. Verificar configurações do Redis
3. Testar execução manual
4. Implementar correções

#### Se Progress Tracker Falhar
1. Implementar fallback para JSON
2. Otimizar sincronização
3. Adicionar logs de debug
4. Testar incrementalmente

#### Se Testes Concorrentes Falharem
1. Reduzir número de sessões
2. Implementar fila de processamento
3. Otimizar recursos
4. Monitorar performance

## Métricas de Acompanhamento

### Métricas Técnicas
- **Tempo de execução**: < 3 minutos por sessão
- **Taxa de sucesso**: > 95%
- **Uso de memória**: < 3GB
- **Uso de CPU**: < 80%

### Métricas de Qualidade
- **Cobertura de testes**: 100%
- **Validação de dados**: 100%
- **Sincronização**: < 5 segundos
- **Disponibilidade**: > 99%

## Próximos Passos

### Imediatos (Próximos 3 dias)
1. **Executar script de investigação do RPA modular**
2. **Implementar correções identificadas**
3. **Executar testes de validação**
4. **Gerar relatório de progresso**

### Médio Prazo (Próximas 2 semanas)
1. **Implementar progress tracker em tempo real**
2. **Executar testes concorrentes**
3. **Implementar métricas de performance**
4. **Implementar sistema de alertas**

### Longo Prazo (Próximos 2 meses)
1. **Implementar cache e otimizações**
2. **Implementar suporte a múltiplas sessões**
3. **Implementar sistema de notificações**
4. **Otimizar performance geral**

## Conclusão

O Plano de Testes da Fase 2 foi desenvolvido para concluir os testes pendentes, corrigir problemas identificados e preparar o sistema para produção. Com a execução deste plano, o sistema estará pronto para uso em produção com todas as funcionalidades validadas e otimizadas.

### Benefícios Esperados
- **Sistema 100% funcional**
- **Performance otimizada**
- **Monitoramento completo**
- **Alta disponibilidade**
- **Escalabilidade garantida**

### Entregáveis
- **Relatório de conclusão dos testes**
- **Sistema otimizado e validado**
- **Documentação atualizada**
- **Scripts de monitoramento**
- **Plano de manutenção**

---

**Documento gerado em:** 01/10/2025 14:00  
**Responsável:** Equipe de Desenvolvimento  
**Status:** Aguardando aprovação do engenheiro de software  
**Próxima revisão:** 02/10/2025

# Plano de Testes - API V4 com Progress Tracker

## Objetivo
Validar a execução do RPA via API V4, capturando progresso em tempo real, estimativas iniciais e cálculo final.

## Estrutura dos Testes

### Fase 1: Preparação do Ambiente
- Limpar dados de testes anteriores
- Verificar serviços (Nginx, PHP-FPM, Redis)
- Confirmar arquivos Python atualizados
- Validar permissões de escrita

### Fase 2: Teste RPA Modular (5 telas)
- Iniciar sessão via API
- Monitorar progresso a cada 2s
- Validar estimativas na Tela 5
- Verificar arquivos de progresso
- Confirmar status final

### Fase 3: Teste RPA Principal (15 telas)
- Iniciar sessão via API
- Monitorar progresso a cada 2s
- Validar estimativas na Tela 5
- Validar cálculo final na Tela 15
- Verificar arquivos de progresso
- Confirmar status final

### Fase 4: Teste de Execuções Concorrentes
- Executar 2 sessões simultâneas
- Monitorar ambas em tempo real
- Validar isolamento de dados
- Verificar performance

### Fase 5: Teste de Tratamento de Erros
- Simular falhas
- Validar captura de erros
- Verificar recuperação
- Confirmar logs

## Scripts de Teste

### 1. Script de Preparação (`test_prepare.sh`)
```bash
#!/bin/bash
# Limpar dados de teste anteriores
rm -f /opt/imediatoseguros-rpa/rpa_data/progress_test_*
rm -f /opt/imediatoseguros-rpa/rpa_data/history_test_*
rm -f /opt/imediatoseguros-rpa/dados_planos_seguro_test_*

# Verificar serviços
systemctl is-active nginx php8.3-fpm redis-server

# Verificar permissões
ls -la /opt/imediatoseguros-rpa/rpa_data/
ls -la /opt/imediatoseguros-rpa/sessions/
```

### 2. Script de Teste RPA Modular (`test_modular.sh`)
```bash
#!/bin/bash
# Iniciar sessão RPA Modular
SESSION_ID=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')

echo "Sessão iniciada: $SESSION_ID"

# Monitorar progresso
while true; do
  PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
  STATUS=$(echo $PROGRESS | jq -r '.progress.status')
  ETAPA=$(echo $PROGRESS | jq -r '.progress.etapa_atual')
  TOTAL=$(echo $PROGRESS | jq -r '.progress.total_etapas')
  PERCENTUAL=$(echo $PROGRESS | jq -r '.progress.percentual')
  MENSAGEM=$(echo $PROGRESS | jq -r '.progress.mensagem')
  
  echo "[$(date)] Etapa $ETAPA/$TOTAL ($PERCENTUAL%) - $STATUS: $MENSAGEM"
  
  # Verificar estimativas
  if [ "$STATUS" = "success" ] && [ "$ETAPA" = "5" ]; then
    ESTIMATIVAS=$(echo $PROGRESS | jq -r '.progress.estimativas.capturadas')
    if [ "$ESTIMATIVAS" = "true" ]; then
      echo "✅ Estimativas capturadas com sucesso!"
      echo $PROGRESS | jq '.progress.estimativas.dados'
      break
    fi
  fi
  
  # Verificar erro
  if [ "$STATUS" = "failed" ] || [ "$STATUS" = "error" ]; then
    echo "❌ Erro na execução: $MENSAGEM"
    break
  fi
  
  sleep 2
done
```

### 3. Script de Teste RPA Principal (`test_principal.sh`)
```bash
#!/bin/bash
# Iniciar sessão RPA Principal
SESSION_ID=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')

echo "Sessão iniciada: $SESSION_ID"

# Monitorar progresso
while true; do
  PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
  STATUS=$(echo $PROGRESS | jq -r '.progress.status')
  ETAPA=$(echo $PROGRESS | jq -r '.progress.etapa_atual')
  TOTAL=$(echo $PROGRESS | jq -r '.progress.total_etapas')
  PERCENTUAL=$(echo $PROGRESS | jq -r '.progress.percentual')
  MENSAGEM=$(echo $PROGRESS | jq -r '.progress.mensagem')
  
  echo "[$(date)] Etapa $ETAPA/$TOTAL ($PERCENTUAL%) - $STATUS: $MENSAGEM"
  
  # Verificar estimativas (Tela 5)
  if [ "$ETAPA" = "5" ] && [ "$STATUS" = "success" ]; then
    ESTIMATIVAS=$(echo $PROGRESS | jq -r '.progress.estimativas.capturadas')
    if [ "$ESTIMATIVAS" = "true" ]; then
      echo "✅ Estimativas iniciais capturadas!"
      echo $PROGRESS | jq '.progress.estimativas.dados'
    fi
  fi
  
  # Verificar cálculo final (Tela 15)
  if [ "$STATUS" = "success" ] && [ "$ETAPA" = "15" ]; then
    RESULTADOS=$(echo $PROGRESS | jq -r '.progress.resultados_finais.rpa_finalizado')
    if [ "$RESULTADOS" = "true" ]; then
      echo "✅ Cálculo final capturado!"
      echo $PROGRESS | jq '.progress.resultados_finais.dados'
      break
    fi
  fi
  
  # Verificar erro
  if [ "$STATUS" = "failed" ] || [ "$STATUS" = "error" ]; then
    echo "❌ Erro na execução: $MENSAGEM"
    break
  fi
  
  sleep 2
done
```

### 4. Script de Teste Concorrente (`test_concurrent.sh`)
```bash
#!/bin/bash
# Iniciar 2 sessões simultâneas
SESSION1=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')

SESSION2=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')

echo "Sessões iniciadas: $SESSION1 e $SESSION2"

# Monitorar ambas as sessões
while true; do
  PROGRESS1=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION1)
  PROGRESS2=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION2)
  
  STATUS1=$(echo $PROGRESS1 | jq -r '.progress.status')
  STATUS2=$(echo $PROGRESS2 | jq -r '.progress.status')
  
  ETAPA1=$(echo $PROGRESS1 | jq -r '.progress.etapa_atual')
  ETAPA2=$(echo $PROGRESS2 | jq -r '.progress.etapa_atual')
  
  echo "[$(date)] Sessão 1: Etapa $ETAPA1 - $STATUS1 | Sessão 2: Etapa $ETAPA2 - $STATUS2"
  
  # Verificar se ambas concluíram
  if [ "$STATUS1" = "success" ] && [ "$STATUS2" = "success" ]; then
    echo "✅ Ambas as sessões concluídas com sucesso!"
    break
  fi
  
  # Verificar se alguma falhou
  if [ "$STATUS1" = "failed" ] || [ "$STATUS2" = "failed" ]; then
    echo "❌ Uma das sessões falhou!"
    break
  fi
  
  sleep 2
done
```

### 5. Script de Validação de Arquivos (`test_validation.sh`)
```bash
#!/bin/bash
# Validar arquivos de progresso
echo "=== Validando arquivos de progresso ==="

# Listar arquivos de progresso
ls -la /opt/imediatoseguros-rpa/rpa_data/progress_test_*

# Validar estrutura JSON
for file in /opt/imediatoseguros-rpa/rpa_data/progress_test_*.json; do
  if [ -f "$file" ]; then
    echo "Validando: $file"
    jq . "$file" > /dev/null
    if [ $? -eq 0 ]; then
      echo "✅ JSON válido"
      
      # Verificar campos obrigatórios
      ETAPA=$(jq -r '.etapa_atual' "$file")
      STATUS=$(jq -r '.status' "$file")
      SESSION_ID=$(jq -r '.session_id' "$file")
      
      echo "  - Etapa: $ETAPA"
      echo "  - Status: $STATUS"
      echo "  - Session ID: $SESSION_ID"
      
      # Verificar estimativas
      if [ "$ETAPA" = "5" ] || [ "$ETAPA" = "15" ]; then
        ESTIMATIVAS=$(jq -r '.dados_extra.estimativas_tela_5' "$file")
        if [ "$ESTIMATIVAS" != "null" ]; then
          echo "  - ✅ Estimativas capturadas"
        fi
      fi
      
      # Verificar resultados finais
      if [ "$ETAPA" = "15" ]; then
        RESULTADOS=$(jq -r '.dados_extra.plano_recomendado' "$file")
        if [ "$RESULTADOS" != "null" ]; then
          echo "  - ✅ Resultados finais capturados"
        fi
      fi
    else
      echo "❌ JSON inválido"
    fi
  fi
done

# Validar arquivos de resultados
echo "=== Validando arquivos de resultados ==="
ls -la /opt/imediatoseguros-rpa/dados_planos_seguro_test_*

for file in /opt/imediatoseguros-rpa/dados_planos_seguro_test_*.json; do
  if [ -f "$file" ]; then
    echo "Validando: $file"
    jq . "$file" > /dev/null
    if [ $? -eq 0 ]; then
      echo "✅ JSON válido"
      
      PLANO_REC=$(jq -r '.plano_recomendado.valor' "$file")
      PLANO_ALT=$(jq -r '.plano_alternativo.valor' "$file")
      
      echo "  - Plano Recomendado: $PLANO_REC"
      echo "  - Plano Alternativo: $PLANO_ALT"
    else
      echo "❌ JSON inválido"
    fi
  fi
done
```

## Cronograma de Execução

### Dia 1: Preparação e Teste RPA Modular
- 09:00 - Executar `test_prepare.sh`
- 09:30 - Executar `test_modular.sh`
- 10:30 - Executar `test_validation.sh`
- 11:00 - Análise de resultados

### Dia 2: Teste RPA Principal
- 09:00 - Executar `test_principal.sh`
- 11:00 - Executar `test_validation.sh`
- 11:30 - Análise de resultados

### Dia 3: Teste Concorrente e Erros
- 09:00 - Executar `test_concurrent.sh`
- 10:30 - Teste de tratamento de erros
- 11:00 - Executar `test_validation.sh`
- 11:30 - Análise final

## Critérios de Sucesso

### RPA Modular
- [ ] Sessão criada via API
- [ ] Progresso monitorado em tempo real
- [ ] Estimativas capturadas na Tela 5
- [ ] Arquivo de progresso gerado
- [ ] Status final: "success"

### RPA Principal
- [ ] Sessão criada via API
- [ ] Progresso monitorado em tempo real
- [ ] Estimativas capturadas na Tela 5
- [ ] Cálculo final capturado na Tela 15
- [ ] Arquivo de progresso gerado
- [ ] Arquivo de resultados gerado
- [ ] Status final: "success"

### Execuções Concorrentes
- [ ] 2 sessões simultâneas
- [ ] Isolamento de dados
- [ ] Performance aceitável
- [ ] Ambas concluídas com sucesso

### Tratamento de Erros
- [ ] Erros capturados corretamente
- [ ] Logs gerados
- [ ] Recuperação funcional
- [ ] Status de erro reportado

## Relatório de Testes

### Template de Relatório
```markdown
# Relatório de Testes - API V4 Progress Tracker

## Data: [DATA]
## Executor: [NOME]

### Resumo Executivo
- Total de testes: [NÚMERO]
- Sucessos: [NÚMERO]
- Falhas: [NÚMERO]
- Taxa de sucesso: [PERCENTUAL]%

### Detalhes dos Testes

#### RPA Modular
- Status: [SUCESSO/FALHA]
- Tempo de execução: [TEMPO]
- Estimativas capturadas: [SIM/NÃO]
- Arquivos gerados: [LISTA]

#### RPA Principal
- Status: [SUCESSO/FALHA]
- Tempo de execução: [TEMPO]
- Estimativas capturadas: [SIM/NÃO]
- Cálculo final capturado: [SIM/NÃO]
- Arquivos gerados: [LISTA]

#### Execuções Concorrentes
- Status: [SUCESSO/FALHA]
- Sessões simultâneas: [NÚMERO]
- Performance: [ACEITÁVEL/LENTA]
- Isolamento: [OK/PROBLEMA]

### Problemas Identificados
- [LISTA DE PROBLEMAS]

### Recomendações
- [LISTA DE RECOMENDAÇÕES]

### Próximos Passos
- [LISTA DE AÇÕES]
```

## Conclusão

Este plano de testes garante:
1. Execução real via API V4
2. Monitoramento em tempo real
3. Captura de estimativas e resultados
4. Execuções concorrentes
5. Tratamento de erros
6. Validação de arquivos
7. Relatórios detalhados

**Objetivo**: Garantir que a API V4 execute o RPA e capture os dados no progress tracker.

---

**Data de Criação**: 01/10/2025  
**Versão**: 1.0  
**Status**: Aguardando Aprovação do Engenheiro de Software

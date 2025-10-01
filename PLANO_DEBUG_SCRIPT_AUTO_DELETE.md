# PLANO DE DEBUG E TESTES - SCRIPT AUTO-DELETE
## PROBLEMA: SCRIPT RPA SE AUTO-DELETA APÓS FALHA

**Data:** 01/10/2025  
**Engenheiro de Testes:** Responsável pela análise e plano  
**Baseado em:** Relatório de Correção do Desenvolvedor  
**Status:** NOVO PROBLEMA IDENTIFICADO  
**Prioridade:** CRÍTICA  

---

## 📋 RESUMO EXECUTIVO

### Problema Identificado
O script RPA está sendo criado e executado com sucesso (conforme logs), mas está se auto-deletando imediatamente após falha na execução, impedindo que o RPA inicie.

### Descoberta Principal
O log indica "RPA background process started successfully" com detalhes de criação do script, mas o arquivo não existe no filesystem, indicando que o script está se auto-deletando após falha.

### Objetivo do Plano
Identificar com precisão por que o script está falhando e se auto-deletando, implementar correções baseadas em evidências concretas.

---

## 🎯 ESTRATÉGIA DE DEBUG

### Abordagem
1. **Testes de Preservação** - Manter script para análise
2. **Testes de Execução** - Identificar ponto de falha
3. **Testes de Ambiente** - Verificar dependências e permissões
4. **Testes de Logs** - Rastrear fluxo de execução
5. **Testes de Correção** - Implementar e validar soluções

### Metodologia
- **Bottom-up:** Testar componentes individuais primeiro
- **Black-box:** Testar execução do script sem conhecimento interno
- **White-box:** Analisar código e logs para identificar falhas
- **Grey-box:** Combinar abordagens para análise completa

---

## 🧪 FASE 1: TESTES DE PRESERVAÇÃO

### 1.1 Desabilitar Auto-Delete
**Objetivo:** Preservar script para análise detalhada

#### Teste 1.1.1: Backup do SessionService
```bash
# Backup do arquivo atual
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.$(date +%Y%m%d_%H%M%S)"

# Verificar backup
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.*"
```

**Critério de Sucesso:** Backup criado com timestamp

#### Teste 1.1.2: Remover Auto-Delete Temporariamente
```bash
# Localizar linha com rm -f "$0"
ssh root@37.27.92.160 "grep -n 'rm -f.*\$0' /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"

# Comentar linha de auto-delete
ssh root@37.27.92.160 "sed -i 's/rm -f \"\$0\"/# rm -f \"\$0\" # TEMPORARIAMENTE DESABILITADO/' /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"

# Verificar alteração
ssh root@37.27.92.160 "grep -A 2 -B 2 'rm -f.*\$0' /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"
```

**Critério de Sucesso:** Linha comentada, script não se auto-deleta

#### Teste 1.1.3: Validar Sintaxe PHP
```bash
# Validar sintaxe
ssh root@37.27.92.160 "php -l /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"

# Reiniciar PHP-FPM
ssh root@37.27.92.160 "systemctl restart php8.3-fpm"
```

**Critério de Sucesso:** Sintaxe válida, serviço reiniciado

### 1.2 Teste de Preservação do Script
**Objetivo:** Verificar se script persiste após desabilitar auto-delete

#### Teste 1.2.1: Criar Nova Sessão
```bash
# Criar nova sessão RPA
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' \
  -s | jq -r '.session_id'
```

**Critério de Sucesso:** Session ID retornado

#### Teste 1.2.2: Verificar Persistência do Script
```bash
# Obter session_id da resposta anterior
SESSION_ID="rpa_v4_$(date +%Y%m%d_%H%M%S)_*"

# Verificar se script existe
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"

# Verificar timestamp
ssh root@37.27.92.160 "ls -lat /opt/imediatoseguros-rpa/scripts/ | head -5"
```

**Critério de Sucesso:** Script existe e não foi deletado

---

## 🔍 FASE 2: TESTES DE EXECUÇÃO

### 2.1 Análise do Script Gerado
**Objetivo:** Examinar conteúdo do script para identificar problemas

#### Teste 2.1.1: Examinar Conteúdo do Script
```bash
# Obter session_id mais recente
SESSION_ID=$(ssh root@37.27.92.160 "ls -t /opt/imediatoseguros-rpa/scripts/start_rpa_v4_*.sh | head -1 | sed 's/.*start_rpa_v4_//; s/\.sh$//'")

# Examinar conteúdo do script
ssh root@37.27.92.160 "cat /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"
```

**Critério de Sucesso:** Script legível, sem erros de sintaxe

#### Teste 2.1.2: Verificar Shebang e Permissões
```bash
# Verificar shebang
ssh root@37.27.92.160 "head -1 /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"

# Verificar permissões
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"

# Verificar se é executável
ssh root@37.27.92.160 "test -x /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh && echo 'Executável' || echo 'Não executável'"
```

**Critério de Sucesso:** Shebang correto, permissões adequadas, executável

#### Teste 2.1.3: Verificar Encoding
```bash
# Verificar encoding do arquivo
ssh root@37.27.92.160 "file /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"

# Verificar line endings
ssh root@37.27.92.160 "hexdump -C /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh | head -5"
```

**Critério de Sucesso:** Encoding correto, line endings LF

### 2.2 Teste de Execução Manual
**Objetivo:** Executar script manualmente para identificar falhas

#### Teste 2.2.1: Execução com Debug
```bash
# Executar script com debug
ssh root@37.27.92.160 "bash -x /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"
```

**Critério de Sucesso:** Script executa sem erros críticos

#### Teste 2.2.2: Capturar Output e Erros
```bash
# Executar e capturar output
ssh root@37.27.92.160 "bash /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh 2>&1 | tee /tmp/script_output.log"

# Examinar output
ssh root@37.27.92.160 "cat /tmp/script_output.log"
```

**Critério de Sucesso:** Output capturado, erros identificados

#### Teste 2.2.3: Verificar Logs do RPA
```bash
# Verificar logs específicos da sessão
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/logs/rpa_v4_${SESSION_ID}.log"

# Examinar logs
ssh root@37.27.92.160 "cat /opt/imediatoseguros-rpa/logs/rpa_v4_${SESSION_ID}.log"
```

**Critério de Sucesso:** Logs existem, conteúdo analisável

---

## 🔧 FASE 3: TESTES DE AMBIENTE

### 3.1 Verificação de Permissões
**Objetivo:** Verificar se www-data tem permissões adequadas

#### Teste 3.1.1: Permissões do Diretório
```bash
# Verificar permissões do diretório scripts
ssh root@37.27.92.160 "ls -ld /opt/imediatoseguros-rpa/scripts/"

# Verificar permissões do diretório sessions
ssh root@37.27.92.160 "ls -ld /opt/imediatoseguros-rpa/sessions/"

# Verificar permissões do diretório logs
ssh root@37.27.92.160 "ls -ld /opt/imediatoseguros-rpa/logs/"
```

**Critério de Sucesso:** Permissões adequadas para www-data

#### Teste 3.1.2: Teste de Escrita
```bash
# Testar escrita como www-data
ssh root@37.27.92.160 "sudo -u www-data touch /opt/imediatoseguros-rpa/scripts/test_write.txt"

# Verificar se arquivo foi criado
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/scripts/test_write.txt"

# Limpar arquivo de teste
ssh root@37.27.92.160 "rm -f /opt/imediatoseguros-rpa/scripts/test_write.txt"
```

**Critério de Sucesso:** www-data pode escrever no diretório

#### Teste 3.1.3: Teste de Execução
```bash
# Criar script de teste simples
ssh root@37.27.92.160 "sudo -u www-data bash -c 'echo \"#!/bin/bash\necho \"Teste de execução\"\" > /opt/imediatoseguros-rpa/scripts/test_exec.sh'"

# Tornar executável
ssh root@37.27.92.160 "chmod +x /opt/imediatoseguros-rpa/scripts/test_exec.sh"

# Executar como www-data
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/scripts/test_exec.sh"

# Limpar arquivo de teste
ssh root@37.27.92.160 "rm -f /opt/imediatoseguros-rpa/scripts/test_exec.sh"
```

**Critério de Sucesso:** www-data pode executar scripts

### 3.2 Verificação do Ambiente Python
**Objetivo:** Verificar se ambiente Python está funcionando

#### Teste 3.2.1: Verificar Python e Venv
```bash
# Verificar se Python existe
ssh root@37.27.92.160 "which python3"

# Verificar se venv existe
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/venv/"

# Verificar se executável Python existe
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/venv/bin/python"
```

**Critério de Sucesso:** Python e venv existem e são acessíveis

#### Teste 3.2.2: Teste de Execução Python
```bash
# Testar execução Python como www-data
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/venv/bin/python -c 'print(\"Python funcionando\")'"

# Testar importação de módulos
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/venv/bin/python -c 'import sys; print(sys.version)'"
```

**Critério de Sucesso:** Python executa corretamente

#### Teste 3.2.3: Verificar RPA Principal
```bash
# Verificar se arquivo RPA existe
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py"

# Testar execução do RPA (dry-run)
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/venv/bin/python /opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py --help"
```

**Critério de Sucesso:** RPA existe e responde a --help

---

## 📊 FASE 4: TESTES DE LOGS

### 4.1 Análise de Logs de Execução
**Objetivo:** Rastrear fluxo de execução do script

#### Teste 4.1.1: Logs do Sistema
```bash
# Verificar logs do sistema
ssh root@37.27.92.160 "tail -20 /var/log/syslog | grep -i rpa"

# Verificar logs do PHP-FPM
ssh root@37.27.92.160 "tail -20 /var/log/php8.3-fpm.log"

# Verificar logs do Nginx
ssh root@37.27.92.160 "tail -20 /var/log/nginx/error.log"
```

**Critério de Sucesso:** Logs analisados, erros identificados

#### Teste 4.1.2: Logs da Aplicação
```bash
# Verificar logs da aplicação
ssh root@37.27.92.160 "tail -20 /opt/imediatoseguros-rpa-v4/logs/rpa/app.log"

# Filtrar logs da sessão específica
ssh root@37.27.92.160 "grep '${SESSION_ID}' /opt/imediatoseguros-rpa-v4/logs/rpa/app.log"
```

**Critério de Sucesso:** Logs da sessão encontrados

#### Teste 4.1.3: Logs do RPA
```bash
# Verificar logs específicos do RPA
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/logs/rpa_v4_${SESSION_ID}.log"

# Examinar logs do RPA
ssh root@37.27.92.160 "cat /opt/imediatoseguros-rpa/logs/rpa_v4_${SESSION_ID}.log"
```

**Critério de Sucesso:** Logs do RPA analisados

### 4.2 Monitoramento em Tempo Real
**Objetivo:** Monitorar execução em tempo real

#### Teste 4.2.1: Monitoramento de Logs
```bash
# Monitorar logs em tempo real
ssh root@37.27.92.160 "tail -f /opt/imediatoseguros-rpa-v4/logs/rpa/app.log /opt/imediatoseguros-rpa/logs/rpa_v4_${SESSION_ID}.log" &
```

**Critério de Sucesso:** Monitoramento ativo

#### Teste 4.2.2: Execução com Monitoramento
```bash
# Executar script com monitoramento
ssh root@37.27.92.160 "bash /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh &"

# Aguardar e verificar processo
ssh root@37.27.92.160 "sleep 5 && ps aux | grep rpa_v4_${SESSION_ID}"
```

**Critério de Sucesso:** Processo monitorado

---

## 🎯 FASE 5: TESTES DE CORREÇÃO

### 5.1 Implementação de Logs de Debug
**Objetivo:** Adicionar logs detalhados para debug

#### Teste 5.1.1: Modificar Script para Debug
```bash
# Backup do script original
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh.backup"

# Adicionar logs de debug
ssh root@37.27.92.160 "sed -i '2i echo \"$(date): Script iniciado\" >> /tmp/debug_${SESSION_ID}.log' /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"

# Adicionar log antes da execução do RPA
ssh root@37.27.92.160 "sed -i '/cd \/opt\/imediatoseguros-rpa/i echo \"$(date): Iniciando RPA\" >> /tmp/debug_${SESSION_ID}.log' /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"
```

**Critério de Sucesso:** Logs de debug adicionados

#### Teste 5.1.2: Executar Script com Debug
```bash
# Executar script modificado
ssh root@37.27.92.160 "bash /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"

# Examinar logs de debug
ssh root@37.27.92.160 "cat /tmp/debug_${SESSION_ID}.log"
```

**Critério de Sucesso:** Logs de debug capturados

### 5.2 Teste de Correções Incrementais
**Objetivo:** Implementar e testar correções baseadas nos achados

#### Teste 5.2.1: Correção de Permissões
```bash
# Verificar e corrigir permissões se necessário
ssh root@37.27.92.160 "chown -R www-data:www-data /opt/imediatoseguros-rpa/"

# Verificar permissões
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/ | head -10"
```

**Critério de Sucesso:** Permissões corretas

#### Teste 5.2.2: Correção de Ambiente
```bash
# Verificar e corrigir ambiente Python se necessário
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/venv/bin/python -m pip list | grep playwright"

# Instalar dependências se necessário
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/venv/bin/python -m pip install --upgrade playwright"
```

**Critério de Sucesso:** Ambiente Python funcional

---

## 📋 CRITÉRIOS DE ACEITAÇÃO

### Funcionalidade
- [ ] Script persiste no filesystem
- [ ] Script executa sem erros críticos
- [ ] RPA inicia corretamente
- [ ] Progress tracker atualiza
- [ ] Logs de debug funcionam

### Performance
- [ ] Tempo de execução < 30 segundos
- [ ] Sem erros nos logs
- [ ] Processo RPA ativo
- [ ] Sistema responsivo

### Qualidade
- [ ] Logs detalhados para debug
- [ ] Tratamento de erros robusto
- [ ] Permissões adequadas
- [ ] Ambiente Python funcional

---

## 🚨 PLANO DE CONTINGÊNCIA

### Se Testes Falharem
1. **Documentar falha** - Logs e evidências
2. **Analisar causa** - Identificar componente com problema
3. **Implementar correção** - Baseada em evidências
4. **Retestar** - Validar correção
5. **Regressão** - Verificar que não quebrou outras funcionalidades

### Se Correções Quebrarem Funcionalidade
1. **Rollback imediato** - Restaurar estado anterior
2. **Análise de impacto** - Identificar o que foi afetado
3. **Correção incremental** - Implementar mudanças menores
4. **Teste gradual** - Validar cada mudança
5. **Documentação** - Registrar lições aprendidas

---

## 📊 MÉTRICAS DE SUCESSO

### Métricas Técnicas
- **Taxa de sucesso:** > 95% das execuções de script
- **Tempo de execução:** < 30 segundos
- **Erros de execução:** < 1% das execuções
- **Persistência de script:** 100% das sessões

### Métricas de Qualidade
- **Cobertura de debug:** > 90% do fluxo de execução
- **Logs de erro:** < 5 por execução
- **Tempo de debug:** < 15 minutos para identificar problema
- **Tempo de correção:** < 1 hora para implementar solução

---

## ⏰ CRONOGRAMA DE EXECUÇÃO

### Dia 1 (Hoje)
- **09:00-10:00:** Fase 1 - Testes de Preservação
- **10:00-11:00:** Fase 2 - Testes de Execução
- **11:00-12:00:** Fase 3 - Testes de Ambiente

### Dia 2 (Amanhã)
- **09:00-10:00:** Fase 4 - Testes de Logs
- **10:00-11:00:** Fase 5 - Testes de Correção
- **11:00-12:00:** Análise de resultados e implementação

---

## 📝 RELATÓRIO DE TESTES

### Template de Relatório
```markdown
# RELATÓRIO DE TESTES - SCRIPT AUTO-DELETE

## Resumo Executivo
- Total de testes: [X]
- Sucessos: [X]
- Falhas: [X]
- Taxa de sucesso: [X]%

## Testes por Fase
### Fase 1: Preservação
- [ ] Teste 1.1.1: Backup do SessionService
- [ ] Teste 1.1.2: Remover Auto-Delete
- [ ] Teste 1.1.3: Validar Sintaxe PHP
- [ ] Teste 1.2.1: Criar Nova Sessão
- [ ] Teste 1.2.2: Verificar Persistência

### Fase 2: Execução
- [ ] Teste 2.1.1: Examinar Conteúdo
- [ ] Teste 2.1.2: Verificar Shebang
- [ ] Teste 2.1.3: Verificar Encoding
- [ ] Teste 2.2.1: Execução com Debug
- [ ] Teste 2.2.2: Capturar Output
- [ ] Teste 2.2.3: Verificar Logs RPA

### Fase 3: Ambiente
- [ ] Teste 3.1.1: Permissões Diretório
- [ ] Teste 3.1.2: Teste de Escrita
- [ ] Teste 3.1.3: Teste de Execução
- [ ] Teste 3.2.1: Verificar Python
- [ ] Teste 3.2.2: Teste Execução Python
- [ ] Teste 3.2.3: Verificar RPA Principal

### Fase 4: Logs
- [ ] Teste 4.1.1: Logs do Sistema
- [ ] Teste 4.1.2: Logs da Aplicação
- ] Teste 4.1.3: Logs do RPA
- [ ] Teste 4.2.1: Monitoramento
- [ ] Teste 4.2.2: Execução Monitorada

### Fase 5: Correção
- [ ] Teste 5.1.1: Modificar Script
- [ ] Teste 5.1.2: Executar com Debug
- [ ] Teste 5.2.1: Correção Permissões
- [ ] Teste 5.2.2: Correção Ambiente

## Problemas Identificados
1. [Problema 1]
2. [Problema 2]
3. [Problema 3]

## Correções Implementadas
1. [Correção 1]
2. [Correção 2]
3. [Correção 3]

## Próximos Passos
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]
```

---

## 👥 EQUIPE ENVOLVIDA

**Engenheiro de Testes:** Responsável pelo plano e execução  
**Desenvolvedor:** Implementação de correções  
**Engenheiro de Software:** Análise e validação  
**DevOps:** Configuração de servidor  

---

## 📞 CONTATOS DE EMERGÊNCIA

**Engenheiro de Testes:** Disponível para suporte técnico  
**Desenvolvedor:** Disponível para implementação  
**Engenheiro de Software:** Disponível para análise  
**DevOps:** Disponível para configuração  

---

## 🔄 PRÓXIMOS PASSOS

### Imediato (Hoje)
1. **Executar Fase 1** - Testes de Preservação
2. **Identificar causa da falha** - Baseado nos resultados
3. **Implementar correção específica** - Para o problema identificado

### Curto Prazo (Esta Semana)
1. **Executar todas as fases** - Validação completa
2. **Implementar correções** - Baseadas em evidências
3. **Validar funcionamento** - Testes de regressão

### Médio Prazo (Próxima Semana)
1. **Documentar solução** - Para futuras referências
2. **Implementar monitoramento** - Alertas automáticos
3. **Preparar para produção** - Validação final

---

**Plano preparado para execução imediata dos testes e debug.**

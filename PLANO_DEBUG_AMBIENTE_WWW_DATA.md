# PLANO DE DEBUG - AMBIENTE WWW-DATA
## INVESTIGAÇÃO DO PROBLEMA SECUNDÁRIO

**Data:** 01/10/2025  
**Engenheiro:** Responsável por testes e debug  
**Status:** 🔍 PLANO DE DEBUG DEFINITIVO  
**Prioridade:** CRÍTICA  

---

## 📋 ANÁLISE DO PROBLEMA

### Contexto
O RPA executa perfeitamente quando chamado manualmente como `root`, mas falha quando chamado pela API como `www-data`. O progress tracker não é criado e o RPA falha imediatamente.

### Evidências Coletadas

#### Execução Manual (root) - ✅ FUNCIONA
```bash
# Comando
bash /opt/imediatoseguros-rpa/scripts/start_rpa_v4_*.sh

# Resultado
[21:33:16] [INFO] Usando parametros.json
Wed Oct  1 09:33:16 PM UTC 2025: RPA concluído com sucesso

# Arquivos gerados
/opt/imediatoseguros-rpa/dados_planos_seguro_20251001_212608.json
```

#### Execução via API (www-data) - ❌ FALHA
```bash
# Comando
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"97137189768",...}'

# Resultado
Wed Oct  1 21:35:08 UTC 2025: RPA falhou para sessão rpa_v4_20251001_213507_ab0669e2

# Arquivos NÃO gerados
# Progress tracker não criado
# RPA falha em 1 segundo
```

### Hipótese Principal
O problema está relacionado às **diferenças de ambiente** entre `root` e `www-data`:
1. **Permissões de arquivo/diretório**
2. **Variáveis de ambiente** (DISPLAY, PATH, etc.)
3. **Dependências do Python** não acessíveis
4. **Configuração do display** para browser automation
5. **Recursos do sistema** (memória, CPU, etc.)

---

## 🎯 ESTRATÉGIA DE DEBUG

### Fase 1: Análise de Ambiente (15 minutos)
Comparar ambiente `root` vs `www-data` para identificar diferenças.

### Fase 2: Testes de Permissões (10 minutos)
Verificar permissões de arquivos, diretórios e execução.

### Fase 3: Testes de Dependências (10 minutos)
Verificar se todas as dependências estão acessíveis para `www-data`.

### Fase 4: Testes de Execução (15 minutos)
Executar RPA como `www-data` com debug detalhado.

### Fase 5: Correção e Validação (20 minutos)
Implementar correções e validar funcionamento.

---

## 🔍 FASE 1: ANÁLISE DE AMBIENTE

### Teste 1.1: Comparar Variáveis de Ambiente
**Objetivo:** Identificar diferenças nas variáveis de ambiente.

**Comandos:**
```bash
# Como root
ssh root@37.27.92.160 "env | sort > /tmp/env_root.txt"

# Como www-data
ssh root@37.27.92.160 "sudo -u www-data env | sort > /tmp/env_wwwdata.txt"

# Comparar
ssh root@37.27.92.160 "diff /tmp/env_root.txt /tmp/env_wwwdata.txt"
```

**Critério de Sucesso:** Identificar variáveis críticas diferentes.

### Teste 1.2: Verificar PATH e Comandos
**Objetivo:** Verificar se comandos essenciais estão no PATH.

**Comandos:**
```bash
# Como root
ssh root@37.27.92.160 "which python3 && which pip && which node && which npm"

# Como www-data
ssh root@37.27.92.160 "sudo -u www-data which python3 && sudo -u www-data which pip && sudo -u www-data which node && sudo -u www-data which npm"
```

**Critério de Sucesso:** Todos os comandos acessíveis para ambos os usuários.

### Teste 1.3: Verificar DISPLAY e X11
**Objetivo:** Verificar configuração de display para browser automation.

**Comandos:**
```bash
# Como root
ssh root@37.27.92.160 "echo \$DISPLAY && xset q 2>/dev/null || echo 'X11 não disponível'"

# Como www-data
ssh root@37.27.92.160 "sudo -u www-data bash -c 'echo \$DISPLAY && xset q 2>/dev/null || echo \"X11 não disponível\"'"
```

**Critério de Sucesso:** DISPLAY configurado corretamente para ambos.

### Teste 1.4: Verificar Recursos do Sistema
**Objetivo:** Verificar limites de recursos (memória, CPU, etc.).

**Comandos:**
```bash
# Como root
ssh root@37.27.92.160 "ulimit -a"

# Como www-data
ssh root@37.27.92.160 "sudo -u www-data bash -c 'ulimit -a'"
```

**Critério de Sucesso:** Limites adequados para execução do RPA.

---

## 🔐 FASE 2: TESTES DE PERMISSÕES

### Teste 2.1: Verificar Permissões de Diretórios
**Objetivo:** Verificar se `www-data` pode acessar todos os diretórios necessários.

**Comandos:**
```bash
# Verificar diretórios críticos
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/"
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/venv/"
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/rpa_data/"
ssh root@37.92.160 "ls -la /opt/imediatoseguros-rpa/logs/"
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/scripts/"
ssh root@37.27.92.160 "ls -la /tmp/"

# Testar acesso como www-data
ssh root@37.27.92.160 "sudo -u www-data ls -la /opt/imediatoseguros-rpa/"
ssh root@37.27.92.160 "sudo -u www-data ls -la /opt/imediatoseguros-rpa/venv/"
ssh root@37.27.92.160 "sudo -u www-data ls -la /opt/imediatoseguros-rpa/rpa_data/"
ssh root@37.27.92.160 "sudo -u www-data ls -la /opt/imediatoseguros-rpa/logs/"
ssh root@37.27.92.160 "sudo -u www-data ls -la /opt/imediatoseguros-rpa/scripts/"
ssh root@37.27.92.160 "sudo -u www-data ls -la /tmp/"
```

**Critério de Sucesso:** `www-data` pode acessar todos os diretórios.

### Teste 2.2: Verificar Permissões de Arquivos
**Objetivo:** Verificar se `www-data` pode executar arquivos necessários.

**Comandos:**
```bash
# Verificar arquivos críticos
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/venv/bin/python"
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py"
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/parametros.json"

# Testar execução como www-data
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/venv/bin/python --version"
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/venv/bin/python -c 'import sys; print(sys.path)'"
```

**Critério de Sucesso:** `www-data` pode executar Python e acessar arquivos.

### Teste 2.3: Verificar Criação de Arquivos
**Objetivo:** Verificar se `www-data` pode criar arquivos nos diretórios necessários.

**Comandos:**
```bash
# Testar criação de arquivos
ssh root@37.27.92.160 "sudo -u www-data touch /opt/imediatoseguros-rpa/rpa_data/teste_wwwdata.txt"
ssh root@37.27.92.160 "sudo -u www-data touch /opt/imediatoseguros-rpa/logs/teste_wwwdata.log"
ssh root@37.27.92.160 "sudo -u www-data touch /tmp/teste_wwwdata.json"

# Verificar se foram criados
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/rpa_data/teste_wwwdata.txt"
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/logs/teste_wwwdata.log"
ssh root@37.27.92.160 "ls -la /tmp/teste_wwwdata.json"

# Limpar arquivos de teste
ssh root@37.27.92.160 "rm -f /opt/imediatoseguros-rpa/rpa_data/teste_wwwdata.txt /opt/imediatoseguros-rpa/logs/teste_wwwdata.log /tmp/teste_wwwdata.json"
```

**Critério de Sucesso:** `www-data` pode criar arquivos em todos os diretórios.

---

## 🐍 FASE 3: TESTES DE DEPENDÊNCIAS

### Teste 3.1: Verificar Python e Dependências
**Objetivo:** Verificar se Python e dependências estão acessíveis.

**Comandos:**
```bash
# Como root
ssh root@37.27.92.160 "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python -c 'import sys; print(\"Python:\", sys.version); import playwright; print(\"Playwright:\", playwright.__version__)'"

# Como www-data
ssh root@37.27.92.160 "sudo -u www-data bash -c 'cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python -c \"import sys; print(\\\"Python:\\\", sys.version); import playwright; print(\\\"Playwright:\\\", playwright.__version__)\"'"
```

**Critério de Sucesso:** Python e Playwright acessíveis para ambos.

### Teste 3.2: Verificar Módulos do RPA
**Objetivo:** Verificar se módulos específicos do RPA estão acessíveis.

**Comandos:**
```bash
# Como root
ssh root@37.27.92.160 "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python -c 'import json, os, sys, time, argparse; print(\"Módulos básicos: OK\")'"

# Como www-data
ssh root@37.27.92.160 "sudo -u www-data bash -c 'cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python -c \"import json, os, sys, time, argparse; print(\\\"Módulos básicos: OK\\\")\"'"
```

**Critério de Sucesso:** Módulos básicos acessíveis para ambos.

### Teste 3.3: Verificar Arquivo de Configuração
**Objetivo:** Verificar se `parametros.json` está acessível.

**Comandos:**
```bash
# Como root
ssh root@37.27.92.160 "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python -c 'import json; data = json.load(open(\"parametros.json\")); print(\"parametros.json: OK\", len(data), \"campos\")'"

# Como www-data
ssh root@37.27.92.160 "sudo -u www-data bash -c 'cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python -c \"import json; data = json.load(open(\\\"parametros.json\\\")); print(\\\"parametros.json: OK\\\", len(data), \\\"campos\\\")\"'"
```

**Critério de Sucesso:** `parametros.json` acessível para ambos.

---

## 🚀 FASE 4: TESTES DE EXECUÇÃO

### Teste 4.1: Executar RPA com Debug Detalhado
**Objetivo:** Executar RPA como `www-data` com logs detalhados.

**Comandos:**
```bash
# Criar script de debug
ssh root@37.27.92.160 "cat > /opt/imediatoseguros-rpa/debug_rpa_wwwdata.sh << 'EOF'
#!/bin/bash
echo \"=== DEBUG RPA WWW-DATA ===\"
echo \"Usuário: \$(whoami)\"
echo \"UID: \$(id -u)\"
echo \"GID: \$(id -g)\"
echo \"Grupos: \$(groups)\"
echo \"PWD: \$(pwd)\"
echo \"PATH: \$PATH\"
echo \"DISPLAY: \$DISPLAY\"
echo \"HOME: \$HOME\"
echo \"TMPDIR: \$TMPDIR\"
echo \"=== TESTANDO PYTHON ===\"
/opt/imediatoseguros-rpa/venv/bin/python --version
echo \"=== TESTANDO ARQUIVO ===\"
ls -la /opt/imediatoseguros-rpa/parametros.json
echo \"=== EXECUTANDO RPA ===\"
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config parametros.json --session debug_wwwdata --progress-tracker json 2>&1
echo \"=== RESULTADO: \$? ===\"
EOF"

# Tornar executável
ssh root@37.27.92.160 "chmod +x /opt/imediatoseguros-rpa/debug_rpa_wwwdata.sh"

# Executar como www-data
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/debug_rpa_wwwdata.sh"
```

**Critério de Sucesso:** Identificar exatamente onde o RPA falha.

### Teste 4.2: Executar RPA com Timeout
**Objetivo:** Executar RPA com timeout para evitar travamento.

**Comandos:**
```bash
# Executar com timeout de 30 segundos
ssh root@37.27.92.160 "sudo -u www-data timeout 30 /opt/imediatoseguros-rpa/debug_rpa_wwwdata.sh"
```

**Critério de Sucesso:** RPA executa ou falha com erro específico.

### Teste 4.3: Verificar Logs do Sistema
**Objetivo:** Verificar logs do sistema para erros relacionados.

**Comandos:**
```bash
# Verificar logs do sistema
ssh root@37.27.92.160 "tail -20 /var/log/syslog | grep -i www-data"
ssh root@37.27.92.160 "tail -20 /var/log/auth.log | grep -i www-data"
ssh root@37.27.92.160 "journalctl -u php8.3-fpm --since '5 minutes ago' | tail -20"
```

**Critério de Sucesso:** Identificar erros nos logs do sistema.

---

## 🔧 FASE 5: CORREÇÃO E VALIDAÇÃO

### Teste 5.1: Implementar Correções
**Objetivo:** Implementar correções baseadas nos problemas identificados.

**Possíveis Correções:**

#### Correção 1: Ajustar Permissões
```bash
# Se problema de permissões
ssh root@37.27.92.160 "chown -R www-data:www-data /opt/imediatoseguros-rpa/rpa_data/"
ssh root@37.27.92.160 "chown -R www-data:www-data /opt/imediatoseguros-rpa/logs/"
ssh root@37.27.92.160 "chmod -R 755 /opt/imediatoseguros-rpa/rpa_data/"
ssh root@37.27.92.160 "chmod -R 755 /opt/imediatoseguros-rpa/logs/"
```

#### Correção 2: Configurar DISPLAY
```bash
# Se problema de display
ssh root@37.27.92.160 "echo 'export DISPLAY=:99' >> /etc/environment"
ssh root@37.27.92.160 "systemctl restart php8.3-fpm"
```

#### Correção 3: Ajustar Limites de Recursos
```bash
# Se problema de recursos
ssh root@37.27.92.160 "echo 'www-data soft nofile 65536' >> /etc/security/limits.conf"
ssh root@37.27.92.160 "echo 'www-data hard nofile 65536' >> /etc/security/limits.conf"
```

#### Correção 4: Configurar Variáveis de Ambiente
```bash
# Se problema de variáveis
ssh root@37.27.92.160 "echo 'export PATH=/opt/imediatoseguros-rpa/venv/bin:\$PATH' >> /etc/environment"
ssh root@37.27.92.160 "systemctl restart php8.3-fpm"
```

### Teste 5.2: Validar Correções
**Objetivo:** Validar se as correções resolveram o problema.

**Comandos:**
```bash
# Testar execução como www-data
ssh root@37.27.92.160 "sudo -u www-data /opt/imediatoseguros-rpa/debug_rpa_wwwdata.sh"

# Testar via API
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' -s

# Verificar progress tracker
sleep 10
curl -s http://37.27.92.160/api/rpa/progress/[SESSION_ID]
```

**Critério de Sucesso:** RPA executa via API e progress tracker atualiza.

### Teste 5.3: Testes de Regressão
**Objetivo:** Garantir que as correções não quebraram funcionalidades existentes.

**Comandos:**
```bash
# Testar execução manual (root)
ssh root@37.27.92.160 "bash /opt/imediatoseguros-rpa/scripts/start_rpa_v4_*.sh"

# Testar API com diferentes tipos de JSON
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{}' -s
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"123"}' -s
```

**Critério de Sucesso:** Todas as funcionalidades continuam funcionando.

---

## 📊 CRITÉRIOS DE SUCESSO

### Fase 1: Análise de Ambiente
- [ ] Variáveis de ambiente comparadas
- [ ] PATH e comandos verificados
- [ ] DISPLAY e X11 verificados
- [ ] Recursos do sistema verificados

### Fase 2: Testes de Permissões
- [ ] Permissões de diretórios verificadas
- [ ] Permissões de arquivos verificadas
- [ ] Criação de arquivos testada

### Fase 3: Testes de Dependências
- [ ] Python e dependências verificadas
- [ ] Módulos do RPA verificados
- [ ] Arquivo de configuração verificado

### Fase 4: Testes de Execução
- [ ] RPA executado com debug detalhado
- [ ] RPA executado com timeout
- [ ] Logs do sistema verificados

### Fase 5: Correção e Validação
- [ ] Correções implementadas
- [ ] Correções validadas
- [ ] Testes de regressão passaram

---

## 🎯 RESULTADO ESPERADO

### Sucesso Completo
- RPA executa via API como `www-data`
- Progress tracker atualiza em tempo real
- Arquivos de progresso são criados
- Resultados finais são gerados
- Sistema funciona end-to-end

### Sucesso Parcial
- RPA executa via API mas com limitações
- Progress tracker atualiza parcialmente
- Alguns arquivos são criados
- Sistema funciona com restrições

### Falha
- RPA não executa via API
- Progress tracker não atualiza
- Nenhum arquivo é criado
- Sistema não funciona

---

## 📝 OBSERVAÇÕES IMPORTANTES

### Diferenças Esperadas Entre root e www-data
1. **Permissões:** `www-data` pode ter permissões limitadas
2. **Variáveis de ambiente:** Podem estar diferentes
3. **Recursos:** Limites podem ser mais restritivos
4. **Display:** Pode não estar configurado para browser automation

### Estratégia de Correção
1. **Identificar problema específico** através dos testes
2. **Implementar correção mínima** necessária
3. **Validar correção** sem quebrar funcionalidades
4. **Documentar mudanças** para futuras referências

### Monitoramento
- Verificar logs do sistema durante os testes
- Monitorar uso de recursos (CPU, memória)
- Verificar permissões após correções
- Testar funcionalidades existentes

---

**Plano preparado com estratégia sistemática para identificar e resolver o problema do ambiente www-data.**

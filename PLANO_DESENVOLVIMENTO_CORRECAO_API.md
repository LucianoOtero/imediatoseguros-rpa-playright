# PLANO DE DESENVOLVIMENTO E CORREÇÃO - API RPA HETZNER
## Desenvolvedor: Análise e Implementação

**Data:** 28 de Setembro de 2025  
**Projeto:** RPA Imediato Seguros - Correção API PHP  
**Ambiente:** Hetzner Server (Ubuntu) - IP: 37.27.92.160  

---

## 🎯 RESUMO EXECUTIVO

Como desenvolvedor, analisei os relatórios técnicos e identifiquei que o sistema RPA está **funcionalmente completo**, mas possui **3 problemas críticos** na camada de integração web que impedem o funcionamento da API PHP. O plano de correção está estruturado em 4 fases prioritárias com estimativa total de **3-4 horas de desenvolvimento**.

---

## 🔍 ANÁLISE TÉCNICA COMO DESENVOLVEDOR

### **Problemas Identificados:**

1. **CRÍTICO: Parsing JSON Falho**
   - **Arquivo:** `/var/www/rpaimediatoseguros.com.br/executar_rpa.php:5`
   - **Causa:** `json_decode()` retorna `null`, acesso a `$dados['session']` falha
   - **Impacto:** Session ID nulo, RPA não executa

2. **CRÍTICO: Ambiente Virtual Inacessível**
   - **Arquivo:** `diagnostico_completo_hetzner.py`
   - **Causa:** Comandos `source` em shell não-interativo
   - **Impacto:** Diagnóstico falha, mas execução manual funciona

3. **MÉDIO: Configuração Shell Inconsistente**
   - **Causa:** PHP executa em ambiente diferente do shell interativo
   - **Impacto:** Comportamento inconsistente entre testes

### **Status Atual do Sistema:**
- ✅ **RPA Python:** 100% funcional (execução manual)
- ✅ **Redis:** 41 chaves ativas, PONG respondendo
- ✅ **Nginx/PHP:** Serviços rodando corretamente
- ❌ **API PHP:** Falha no parsing JSON
- ❌ **Diagnóstico:** 6/30 testes falhando

---

## 🚀 PLANO DE DESENVOLVIMENTO

### **FASE 1: CORREÇÃO CRÍTICA - API PHP (Prioridade: ALTA)**
**Tempo Estimado:** 1-2 horas  
**Objetivo:** Corrigir parsing JSON e validação de entrada

#### **1.1 Backup e Preparação (15 min)**
```bash
# Backup do arquivo atual
cp /var/www/rpaimediatoseguros.com.br/executar_rpa.php /var/www/rpaimediatoseguros.com.br/executar_rpa.php.backup.$(date +%Y%m%d_%H%M%S)

# Verificar permissões
ls -la /var/www/rpaimediatoseguros.com.br/executar_rpa.php
```

#### **1.2 Implementação da Correção (45 min)**
```php
<?php
header('Content-Type: application/json');

// Log de debug
error_log("=== API RPA DEBUG ===");
error_log("Timestamp: " . date('Y-m-d H:i:s'));

// Capturar input bruto
$raw_input = file_get_contents('php://input');
error_log("Raw input length: " . strlen($raw_input));
error_log("Raw input: " . $raw_input);

// Validar se há dados
if (empty($raw_input)) {
    error_log("ERROR: No input data");
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'error' => 'No input data',
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

// Decodificar JSON
$dados = json_decode($raw_input, true);
$json_error = json_last_error();

// Verificar se JSON é válido
if ($json_error !== JSON_ERROR_NONE) {
    error_log("ERROR: JSON decode failed - " . json_last_error_msg());
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'error' => 'Invalid JSON: ' . json_last_error_msg(),
        'json_error_code' => $json_error,
        'raw_input' => $raw_input,
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

error_log("JSON decoded successfully: " . print_r($dados, true));

// Validar estrutura obrigatória
if (!isset($dados['session'])) {
    error_log("ERROR: Session key missing");
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'error' => 'Session key missing',
        'received_keys' => array_keys($dados),
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

if (empty($dados['session'])) {
    error_log("ERROR: Session ID empty");
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'error' => 'Session ID cannot be empty',
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

$session_id = $dados['session'];
error_log("Session ID validated: " . $session_id);

// Salvar dados do formulário
$dados_formulario = $dados['dados'] ?? [];
$parametros_file = "temp/parametros_{$session_id}.json";
$saved = file_put_contents($parametros_file, json_encode($dados_formulario));

if ($saved === false) {
    error_log("ERROR: Failed to save parameters file");
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'error' => 'Failed to save parameters',
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

error_log("Parameters saved to: " . $parametros_file);

// Executar RPA
$command = "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python teste_api_simples.py --session $session_id --modo-silencioso";
error_log("Executing command: " . $command);

$pid = shell_exec("nohup bash -c '$command' > /dev/null 2>&1 & echo $!");
$pid = trim($pid);

error_log("RPA started with PID: " . $pid);

// Resposta de sucesso
$response = [
    'success' => true,
    'session_id' => $session_id,
    'pid' => $pid,
    'timestamp' => date('Y-m-d H:i:s'),
    'parameters_saved' => true
];

error_log("API response: " . json_encode($response));
echo json_encode($response);
?>
```

#### **1.3 Testes da Correção (30 min)**
```bash
# Teste 1: JSON válido
curl -X POST http://37.27.92.160/executar_rpa.php \
  -H 'Content-Type: application/json' \
  -d '{"session":"teste_correcao_1","dados":{"placa":"ABC1234"}}'

# Teste 2: JSON sem session
curl -X POST http://37.27.92.160/executar_rpa.php \
  -H 'Content-Type: application/json' \
  -d '{"dados":{"placa":"ABC1234"}}'

# Teste 3: JSON malformado
curl -X POST http://37.27.92.160/executar_rpa.php \
  -H 'Content-Type: application/json' \
  -d '{"session":"teste_invalido"'

# Teste 4: JSON vazio
curl -X POST http://37.27.92.160/executar_rpa.php \
  -H 'Content-Type: application/json' \
  -d ''

# Verificar logs
tail -20 /var/log/nginx/error.log
tail -20 /var/log/php8.3-fpm.log

# Verificar Redis
redis-cli keys '*teste_correcao_1*'
```

---

### **FASE 2: CORREÇÃO DO DIAGNÓSTICO (Prioridade: MÉDIA)**
**Tempo Estimado:** 30 minutos  
**Objetivo:** Corrigir comandos `source` no script de diagnóstico

#### **2.1 Identificar Comandos Problemáticos (10 min)**
```bash
# Buscar comandos 'source' no script
grep -n "source" /opt/imediatoseguros-rpa/diagnostico_completo_hetzner.py
```

#### **2.2 Implementar Correções (20 min)**
```python
# ANTES (falha)
comando = "source venv/bin/activate && python --version"

# DEPOIS (funciona)
comando = "/opt/imediatoseguros-rpa/venv/bin/python --version"

# Aplicar em todas as ocorrências:
# - Linha ~120: Versão Python
# - Linha ~130: Ambiente Virtual  
# - Linha ~140: Playwright
# - Linha ~200: Teste Help
# - Linha ~210: Teste Versão
# - Linha ~220: Teste Inicialização
```

---

### **FASE 3: PADRONIZAÇÃO DO AMBIENTE (Prioridade: MÉDIA)**
**Tempo Estimado:** 1 hora  
**Objetivo:** Criar wrapper padronizado para execução

#### **3.1 Criar Script Wrapper (20 min)**
```bash
# Criar wrapper script
cat > /opt/imediatoseguros-rpa/executar_rpa_wrapper.sh << 'EOF'
#!/bin/bash
# Wrapper para execução padronizada do RPA
set -e

# Configurar ambiente
cd /opt/imediatoseguros-rpa
export PATH="/opt/imediatoseguros-rpa/venv/bin:$PATH"
export PYTHONPATH="/opt/imediatoseguros-rpa:$PYTHONPATH"

# Log de execução
echo "$(date): Starting RPA with args: $@" >> /opt/imediatoseguros-rpa/logs/wrapper.log

# Executar Python
exec /opt/imediatoseguros-rpa/venv/bin/python "$@"
EOF

# Tornar executável
chmod +x /opt/imediatoseguros-rpa/executar_rpa_wrapper.sh
```

#### **3.2 Atualizar Comandos PHP (20 min)**
```php
// ANTES
$command = "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python teste_api_simples.py --session $session_id --modo-silencioso";

// DEPOIS
$command = "/opt/imediatoseguros-rpa/executar_rpa_wrapper.sh teste_api_simples.py --session $session_id --modo-silencioso";
```

#### **3.3 Testar Wrapper (20 min)**
```bash
# Teste manual do wrapper
/opt/imediatoseguros-rpa/executar_rpa_wrapper.sh teste_api_simples.py --session teste_wrapper --modo-silencioso

# Verificar logs
tail -10 /opt/imediatoseguros-rpa/logs/wrapper.log

# Verificar Redis
redis-cli keys '*teste_wrapper*'
```

---

### **FASE 4: VALIDAÇÃO E TESTES (Prioridade: ALTA)**
**Tempo Estimado:** 30 minutos  
**Objetivo:** Validar correções e executar testes completos

#### **4.1 Executar Diagnóstico Completo (15 min)**
```bash
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python diagnostico_completo_hetzner.py > diagnostico_pos_correcao_$(date +%Y%m%d_%H%M%S).log 2>&1
```

#### **4.2 Testes de Integração (15 min)**
```bash
# Teste 1: API com dados válidos
curl -X POST http://37.27.92.160/executar_rpa.php \
  -H 'Content-Type: application/json' \
  -d '{"session":"teste_final_1","dados":{"placa":"ABC1234","combustivel":"flex"}}'

# Aguardar 10 segundos
sleep 10

# Verificar progresso
curl "http://37.27.92.160/get_progress.php?session=teste_final_1"

# Verificar Redis
redis-cli keys '*teste_final_1*'
redis-cli get "rpa:progress:teste_final_1"
redis-cli get "rpa:result:teste_final_1"

# Teste 2: API com dados inválidos
curl -X POST http://37.27.92.160/executar_rpa.php \
  -H 'Content-Type: application/json' \
  -d '{"session":"","dados":{"placa":"ABC1234"}}'

# Teste 3: API sem dados
curl -X POST http://37.27.92.160/executar_rpa.php \
  -H 'Content-Type: application/json' \
  -d '{}'
```

---

## 📊 CRITÉRIOS DE SUCESSO

### **Métricas de Qualidade:**
- **Taxa de Sucesso da API:** 95%+ (28/30 testes)
- **Response Time:** < 2 segundos
- **Error Rate:** < 5%
- **Redis Integration:** 100% funcional

### **Funcionalidades Validadas:**
- ✅ Parsing JSON robusto com validação
- ✅ Tratamento de erros adequado
- ✅ Logging detalhado para debug
- ✅ Execução RPA via API
- ✅ Progress tracking em tempo real
- ✅ Diagnóstico completo funcionando

### **Testes de Regressão:**
- ✅ Execução manual do RPA
- ✅ ProgressTracker funcionando
- ✅ Redis conectividade
- ✅ Nginx/PHP serviços
- ✅ Ambiente virtual Python

---

## 🚨 PLANO DE ROLLBACK

### **Se a correção falhar:**
```bash
# Restaurar backup
cp /var/www/rpaimediatoseguros.com.br/executar_rpa.php.backup.* /var/www/rpaimediatoseguros.com.br/executar_rpa.php

# Verificar funcionamento
curl -X POST http://37.27.92.160/executar_rpa.php \
  -H 'Content-Type: application/json' \
  -d '{"session":"teste_rollback","dados":{"placa":"ABC1234"}}'
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### **Pré-Implementação:**
- [ ] Backup do arquivo atual
- [ ] Verificar permissões
- [ ] Confirmar ambiente de teste

### **Implementação:**
- [ ] Fase 1: Correção API PHP
- [ ] Fase 2: Correção Diagnóstico
- [ ] Fase 3: Padronização Ambiente
- [ ] Fase 4: Validação e Testes

### **Pós-Implementação:**
- [ ] Executar diagnóstico completo
- [ ] Testar cenários de erro
- [ ] Validar integração end-to-end
- [ ] Documentar mudanças
- [ ] Atualizar documentação

---

## 🎯 CONCLUSÃO

O plano de desenvolvimento está estruturado para resolver **todos os problemas identificados** de forma sistemática e segura. Com as correções propostas, o sistema deve atingir **95%+ de confiabilidade** e estar pronto para produção.

**Próximos passos:** Implementar as correções na ordem de prioridade, começando pela Fase 1 (correção crítica da API PHP).

















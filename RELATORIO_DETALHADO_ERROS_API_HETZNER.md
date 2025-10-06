# RELATÓRIO DETALHADO - ERROS API HETZNER
## Análise Completa dos Problemas e Soluções Tentadas

**Data:** 28 de Setembro de 2025  
**Ambiente:** Hetzner Server (Ubuntu) - IP: 37.27.92.160  
**Projeto:** RPA Imediato Seguros - Playwright  

---

## 🎯 RESUMO EXECUTIVO

O sistema RPA funciona perfeitamente quando executado manualmente, mas falha quando executado via API PHP. Após extensiva investigação, identificamos que o problema principal está na **parsing do JSON** no arquivo `executar_rpa.php`, resultando em `session_id` nulo e execução falha.

---

## 🔍 PROBLEMAS IDENTIFICADOS

### 1. **ERRO PRINCIPAL: Session ID Nulo**
- **Sintoma:** API retorna `"session_id": null`
- **Causa:** `$dados['session']` está nulo devido a parsing incorreto do JSON
- **Evidência:** Arquivo `parametros_.json` contém `null` (session vazia)

### 2. **Erro de Parsing JSON no PHP**
- **Localização:** `/var/www/rpaimediatoseguros.com.br/executar_rpa.php` linha 5
- **Erro:** `PHP Warning: Trying to access array offset on null`
- **Frequência:** Repetido em todos os logs do Nginx

### 3. **Execução RPA Falha Silenciosamente**
- **Sintoma:** Processo inicia mas não escreve no Redis
- **Causa:** Session ID nulo impede execução correta
- **Evidência:** Nenhuma chave Redis criada para sessões da API

---

## 🛠️ SOLUÇÕES TENTADAS

### **Tentativa 1: Correção do ProgressTracker**
- **Problema:** Método `update_progress()` ausente na classe `ProgressTracker`
- **Solução:** Adicionado método `update_progress()` em `utils/progress_realtime.py`
- **Resultado:** ✅ **SUCESSO** - ProgressTracker funcionando

### **Tentativa 2: Correção do Modo Headless**
- **Problema:** Playwright tentando abrir browser com display (`headless=False`)
- **Solução:** Alterado para `headless=not DISPLAY_ENABLED`
- **Resultado:** ✅ **SUCESSO** - Browser executa em modo headless

### **Tentativa 3: Remoção do xvfb-run**
- **Problema:** `xvfb-run` causando erros de ambiente
- **Solução:** Removido `xvfb-run` do comando PHP
- **Resultado:** ✅ **SUCESSO** - Comando simplificado

### **Tentativa 4: Correção do Ambiente Virtual**
- **Problema:** `source venv/bin/activate` não funcionava no PHP
- **Solução:** Uso de caminho absoluto `/opt/imediatoseguros-rpa/venv/bin/python`
- **Resultado:** ✅ **SUCESSO** - Python executa corretamente

### **Tentativa 5: Correção de Permissões**
- **Problema:** `www-data` sem permissões de execução
- **Solução:** `chmod 755` nos diretórios RPA e venv
- **Resultado:** ✅ **SUCESSO** - Permissões corretas

### **Tentativa 6: Criação de Arquivo de Teste Simples**
- **Problema:** RPA principal muito complexo para debug
- **Solução:** Criado `teste_api_simples.py` com 3 etapas
- **Resultado:** ✅ **SUCESSO** - Teste manual funciona perfeitamente

---

## 🧪 TESTES REALIZADOS

### **Teste 1: Execução Manual (Root)**
```bash
/opt/imediatoseguros-rpa/venv/bin/python teste_api_simples.py --session teste_manual
```
- **Resultado:** ✅ **SUCESSO** - Redis populado corretamente

### **Teste 2: Execução Manual (www-data)**
```bash
su -s /bin/bash www-data -c '/opt/imediatoseguros-rpa/venv/bin/python teste_api_simples.py --session teste_www_data'
```
- **Resultado:** ✅ **SUCESSO** - Redis populado corretamente

### **Teste 3: Execução com nohup (www-data)**
```bash
su -s /bin/bash www-data -c 'nohup /opt/imediatoseguros-rpa/venv/bin/python teste_api_simples.py --session teste_nohup --modo-silencioso > /tmp/teste.log 2>&1 &'
```
- **Resultado:** ✅ **SUCESSO** - Redis populado corretamente

### **Teste 4: Execução via API PHP**
```bash
curl -X POST http://37.27.92.160/executar_rpa.php -H 'Content-Type: application/json' -d '{"session":"teste_api","dados":{"placa":"ABC1234"}}'
```
- **Resultado:** ❌ **FALHA** - Session ID nulo, Redis vazio

---

## 🔧 DIAGNÓSTICO TÉCNICO

### **Arquivo PHP Atual:**
```php
<?php
header('Content-Type: application/json');

$dados = json_decode(file_get_contents('php://input'), true);
$session_id = $dados['session']; // ← AQUI ESTÁ O PROBLEMA

// Salvar dados do formulário
file_put_contents("temp/parametros_{$session_id}.json", json_encode($dados['dados']));

// Executar RPA
$command = "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python teste_api_simples.py --session $session_id --modo-silencioso";
$pid = shell_exec("nohup bash -c '$command' > /dev/null 2>&1 & echo $!");

echo json_encode([
    'success' => true,
    'session_id' => $session_id, // ← Retorna null
    'pid' => trim($pid)
]);
?>
```

### **Problema Identificado:**
1. `json_decode()` retorna `null` ou array malformado
2. `$dados['session']` acessa índice de array nulo
3. `$session_id` fica nulo
4. Comando executa com session vazia
5. RPA falha silenciosamente

---

## 📊 EVIDÊNCIAS

### **Logs do Nginx:**
```
PHP Warning: Trying to access array offset on null in /var/www/rpaimediatoseguros.com.br/executar_rpa.php on line 5
```

### **Arquivo de Parâmetros:**
```json
null
```

### **Resposta da API:**
```json
{"success":true,"session_id":null,"pid":"403307"}
```

### **Redis (Após API):**
```
(empty array)
```

---

## 🎯 SOLUÇÃO FINAL PROPOSTA

### **Correção do Arquivo PHP:**
```php
<?php
header('Content-Type: application/json');

// Debug do JSON recebido
$raw_input = file_get_contents('php://input');
error_log("Raw input: " . $raw_input);

$dados = json_decode($raw_input, true);
error_log("Decoded data: " . print_r($dados, true));

// Validação robusta
if (!$dados || !isset($dados['session'])) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => 'Invalid JSON or missing session',
        'raw_input' => $raw_input
    ]);
    exit;
}

$session_id = $dados['session'];

// Validação adicional
if (empty($session_id)) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => 'Session ID cannot be empty'
    ]);
    exit;
}

// Salvar dados do formulário
file_put_contents("temp/parametros_{$session_id}.json", json_encode($dados['dados']));

// Executar RPA
$command = "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python teste_api_simples.py --session $session_id --modo-silencioso";
$pid = shell_exec("nohup bash -c '$command' > /dev/null 2>&1 & echo $!");

echo json_encode([
    'success' => true,
    'session_id' => $session_id,
    'pid' => trim($pid)
]);
?>
```

---

## 📈 STATUS ATUAL

- ✅ **ProgressTracker:** Funcionando
- ✅ **Modo Headless:** Funcionando  
- ✅ **Ambiente Virtual:** Funcionando
- ✅ **Permissões:** Funcionando
- ✅ **Execução Manual:** Funcionando
- ❌ **API PHP:** Falhando (JSON parsing)

---

## 🚀 PRÓXIMOS PASSOS

1. **Implementar correção do JSON parsing** no `executar_rpa.php`
2. **Testar API corrigida** com dados válidos
3. **Validar integração completa** RPA + Redis + API
4. **Documentar solução final** para produção

---

## 📝 CONCLUSÃO

O problema não está no ambiente ou no código Python, mas sim na **parsing do JSON** no arquivo PHP. Todas as outras correções foram bem-sucedidas e o sistema está funcionalmente completo, necessitando apenas da correção final do parsing JSON para funcionar completamente via API.

















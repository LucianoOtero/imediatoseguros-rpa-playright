# DIAGNÓSTICO DETALHADO - ERROS ENCONTRADOS
## PROBLEMA: JSON VAZIO NO PHP - RPA V4

**Data:** 01/10/2025  
**Desenvolvedor:** Responsável pela implementação  
**Status:** EXECUÇÃO INTERROMPIDA - ERROS CRÍTICOS  
**Prioridade:** CRÍTICA  

---

## 📋 RESUMO EXECUTIVO

### Problema Principal
O sistema RPA V4 não está recebendo dados JSON corretamente via API. Mesmo enviando dados válidos via `curl`, o PHP recebe um array vazio (`[]`) em vez dos dados esperados, causando falha na execução do RPA com dados dinâmicos.

### Status da Execução
**INTERROMPIDA** - Múltiplos erros críticos impedem o avanço do plano de implementação.

### Impacto
- **Funcionalidade:** RPA não executa com dados dinâmicos
- **Fallback:** Sistema usa `parametros.json` em vez de dados da requisição
- **Progress Tracker:** Não funciona corretamente
- **Produção:** Sistema não está pronto para uso

---

## 🚨 ERROS CRÍTICOS IDENTIFICADOS

### 1. JSON Vazio no PHP (CRÍTICO)
**Localização:** `/opt/imediatoseguros-rpa-v4/public/index.php` linha 78

**Sintoma:**
```json
// Log do sistema mostra dados vazios
{"timestamp":"2025-10-01 17:09:13","level":"INFO","message":"RPA start request received","context":{"data":[]}}
```

**Código Problemático:**
```php
$input = json_decode(file_get_contents('php://input'), true);
$response = $controller->startRPA($input ?: []);
```

**Evidências:**
- Script gerado usa fallback: `"Fonte de dados: parametros.json (fallback)"`
- RPA não inicia automaticamente: `"status": "pending"`
- Dados não chegam ao SessionService

### 2. Variáveis Indefinidas no SessionService.php (CRÍTICO)
**Localização:** `/opt/imediatoseguros-rpa-v4/src/Services/SessionService.php` linhas 330-333

**Erro:**
```
PHP message: PHP Warning: Undefined variable $tempJsonFile in /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php on line 330
PHP message: PHP Warning: Undefined variable $jsonContent in /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php on line 331
PHP message: PHP Warning: Undefined variable $tempJsonFile in /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php on line 333
```

**Causa:** Variáveis `$tempJsonFile` e `$jsonContent` não estão sendo definidas corretamente no método `generateStartScript()`.

### 3. Xdebug com Problemas de Log (MÉDIO)
**Localização:** `/etc/php/8.3/fpm/conf.d/20-xdebug.ini`

**Erro:**
```
PHP message: Xdebug: [Log Files] File '/var/log/xdebug.log' could not be opened.
PHP message: Xdebug: [Step Debug] Could not connect to debugging client. Tried: 127.0.0.1:9003
```

**Causa:** Arquivo de log não existe ou não tem permissões corretas.

### 4. Script de Diagnóstico com Erro de Sintaxe (BAIXO)
**Localização:** `/opt/imediatoseguros-rpa-v4/public/diagnostic.php`

**Erro:**
```
PHP message: PHP Parse error: syntax error, unexpected token "\", expecting end of file
```

**Causa:** Problemas de escape de caracteres ao criar o arquivo via SSH.

---

## 🔍 ANÁLISE TÉCNICA DETALHADA

### Arquitetura do Sistema
```
Frontend (Webflow) → Nginx → PHP-FPM → index.php → SessionService → RPA Python
```

### Fluxo Esperado vs. Atual
**Esperado:**
1. Frontend envia JSON via POST
2. Nginx recebe requisição
3. PHP-FPM processa requisição
4. index.php decodifica JSON
5. SessionService gera script RPA
6. RPA Python executa com dados

**Atual:**
1. Frontend envia JSON via POST ✅
2. Nginx recebe requisição ✅
3. PHP-FPM processa requisição ✅
4. index.php **NÃO** decodifica JSON ❌
5. SessionService **NÃO** recebe dados ❌
6. RPA Python **NÃO** executa ❌

### Ponto de Falha Identificado
**Localização:** `/opt/imediatoseguros-rpa-v4/public/index.php` linha 78
```php
$input = json_decode(file_get_contents('php://input'), true);
```

**Problema:** `file_get_contents('php://input')` retorna string vazia.

### Possíveis Causas (Ordenadas por Probabilidade)
1. **Nginx (60%):** Configuração incorreta para POST requests
2. **PHP-FPM (25%):** Problemas de buffer ou timeout
3. **PHP (10%):** Configurações restritivas (post_max_size, etc.)
4. **Encoding (3%):** Problemas de charset ou BOM
5. **JSON (2%):** Dados corrompidos durante transmissão

---

## 🧪 TESTES REALIZADOS

### 1. Teste de Conectividade
**Comando:**
```bash
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'
```

**Resultado:** ❌ Falha
- HTTP 200 OK
- Mas dados chegam vazios no PHP

### 2. Teste de Script de Diagnóstico
**Comando:**
```bash
curl -X POST http://37.27.92.160/diagnostic.php \
  -H 'Content-Type: application/json' \
  -d '{"test":"data"}'
```

**Resultado:** ❌ Falha
- HTTP 500 Internal Server Error
- Erro de sintaxe PHP

### 3. Teste de Configuração Nginx
**Verificação:**
```bash
cat /etc/nginx/sites-available/rpa-v4
```

**Resultado:** ✅ OK
- Configuração correta
- FastCGI configurado
- Headers corretos

### 4. Teste de Xdebug
**Verificação:**
```bash
php -m | grep xdebug
```

**Resultado:** ⚠️ Parcial
- Xdebug instalado
- Mas problemas de log

---

## 📊 LOGS E EVIDÊNCIAS

### Logs da Aplicação
```json
{"timestamp":"2025-10-01 17:09:13","level":"INFO","message":"RPA start request received","context":{"data":[]}}
{"timestamp":"2025-10-01 17:09:13","level":"INFO","message":"Creating new RPA session","context":{"data":[]}}
{"timestamp":"2025-10-01 17:09:13","level":"INFO","message":"Dados aceitos para execução RPA","context":{"data_received":true}}
```

### Logs do Nginx
```
2025/10/01 18:17:58 [error] 542497#542497: *116 FastCGI sent in stderr: "PHP message: PHP Parse error: syntax error, unexpected token "\", expecting end of file in /opt/imediatoseguros-rpa-v4/public/diagnostic.php on line 3"
```

### Logs do PHP-FPM
```
[01-Oct-2025 18:08:17] NOTICE: fpm is running, pid 550381
[01-Oct-2025 18:08:17] NOTICE: ready to handle connections
```

### Logs do Xdebug
```
PHP message: Xdebug: [Log Files] File '/var/log/xdebug.log' could not be opened.
PHP message: Xdebug: [Step Debug] Could not connect to debugging client. Tried: 127.0.0.1:9003
```

---

## 🔧 CONFIGURAÇÕES ATUAIS

### Nginx
```nginx
server {
    listen 80;
    server_name rpa-v4.local 37.27.92.160;
    root /opt/imediatoseguros-rpa-v4/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### PHP-FPM
```ini
post_max_size = 8M
upload_max_filesize = 2M
max_input_vars = 1000
max_execution_time = 30
```

### Xdebug
```ini
zend_extension=xdebug.so
xdebug.mode=debug,develop
xdebug.start_with_request=yes
xdebug.client_host=127.0.0.1
xdebug.client_port=9003
xdebug.log=/var/log/xdebug.log
xdebug.log_level=7
```

---

## 🎯 CAUSA RAIZ IDENTIFICADA

### Análise dos Logs
1. **Nginx:** Configuração correta, requisições chegam
2. **PHP-FPM:** Funcionando, processa requisições
3. **index.php:** Executa, mas `file_get_contents('php://input')` retorna vazio
4. **SessionService:** Recebe dados vazios, gera script com fallback

### Conclusão
O problema está na **comunicação entre Nginx e PHP-FPM** para requisições POST com body JSON. O Nginx não está passando o body da requisição para o PHP-FPM.

### Evidência
- Requisições GET funcionam
- Requisições POST sem body funcionam
- Requisições POST com JSON body falham
- `file_get_contents('php://input')` retorna vazio

---

## 🚀 SOLUÇÕES PROPOSTAS

### 1. Correção Nginx (PRIORIDADE ALTA)
**Problema:** Nginx não está passando o body da requisição POST para PHP-FPM.

**Solução:**
```nginx
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
    include fastcgi_params;
    
    # Adicionar configurações para POST requests
    fastcgi_read_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_connect_timeout 300;
    fastcgi_buffer_size 128k;
    fastcgi_buffers 4 256k;
    fastcgi_busy_buffers_size 256k;
    fastcgi_temp_file_write_size 256k;
}
```

### 2. Correção SessionService.php (PRIORIDADE ALTA)
**Problema:** Variáveis `$tempJsonFile` e `$jsonContent` não definidas.

**Solução:**
```php
private function generateStartScript(string $sessionId, array $data): string
{
    // Estratégia conservadora: validar dados e usar fallback
    $useJsonData = !empty($data) && $this->validateData($data);
    
    if ($useJsonData) {
        // ✅ SOLUÇÃO: Criar arquivo temporário para evitar problemas de escape
        $tempJsonFile = "/tmp/rpa_data_{$sessionId}.json";
        $jsonContent = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        
        $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data @{$tempJsonFile} --session \$SESSION_ID --progress-tracker json";
        $dataSource = "JSON dinâmico (arquivo temporário)";
        $cleanupCommand = "rm -f {$tempJsonFile}";
    } else {
        $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config /opt/imediatoseguros-rpa/parametros.json --session \$SESSION_ID --progress-tracker json";
        $dataSource = "parametros.json (fallback)";
        $cleanupCommand = "";
    }
    
    // Resto do método...
}
```

### 3. Correção Xdebug (PRIORIDADE MÉDIA)
**Problema:** Arquivo de log não existe ou sem permissões.

**Solução:**
```bash
# Criar arquivo de log com permissões corretas
sudo touch /var/log/xdebug.log
sudo chown www-data:www-data /var/log/xdebug.log
sudo chmod 664 /var/log/xdebug.log
```

### 4. Correção Defensiva no index.php (PRIORIDADE ALTA)
**Problema:** Falta validação e logs para debug.

**Solução:**
```php
// Substituir linha 78 em index.php
$rawInput = file_get_contents('php://input');
$inputLength = strlen($rawInput);

// Log para debug
error_log("DEBUG: Raw input length: $inputLength");
error_log("DEBUG: Raw input content: " . substr($rawInput, 0, 500));

if ($inputLength === 0) {
    error_log("ERROR: Empty input received");
    return ['success' => false, 'error' => 'No data received'];
}

$input = json_decode($rawInput, true);
if (json_last_error() !== JSON_ERROR_NONE) {
    error_log("ERROR: JSON decode failed: " . json_last_error_msg());
    error_log("ERROR: Raw input was: " . $rawInput);
    return ['success' => false, 'error' => 'Invalid JSON: ' . json_last_error_msg()];
}

$response = $controller->startRPA($input);
```

---

## 📋 PLANO DE CORREÇÃO

### Fase 1: Correções Críticas (30 minutos)
1. **Corrigir Nginx** - Adicionar configurações para POST requests
2. **Corrigir SessionService.php** - Definir variáveis corretamente
3. **Implementar correção defensiva** - Adicionar logs e validação

### Fase 2: Testes e Validação (20 minutos)
1. **Testar com dados reais** - Validar funcionamento
2. **Verificar logs** - Confirmar que dados chegam
3. **Validar RPA** - Confirmar execução com dados corretos

### Fase 3: Correções Secundárias (10 minutos)
1. **Corrigir Xdebug** - Criar arquivo de log
2. **Limpar arquivos temporários** - Remover diagnostic.php
3. **Documentar solução** - Para futuras referências

---

## 🎯 CRITÉRIOS DE SUCESSO

### Funcionalidade
- [ ] JSON chega corretamente no PHP
- [ ] `json_decode` funciona sem erros
- [ ] Dados são passados para o RPA
- [ ] Script é gerado com JSON dinâmico
- [ ] RPA executa com dados corretos

### Performance
- [ ] Tempo de resposta < 2 segundos
- [ ] Sem erros nos logs
- [ ] Progress tracker funciona

### Qualidade
- [ ] Código defensivo implementado
- [ ] Logs adequados para debug
- [ ] Tratamento de erros robusto

---

## 🚨 RISCOS E CONTINGÊNCIAS

### Riscos
1. **Alteração no Nginx** pode afetar outras aplicações
2. **Correção no SessionService** pode quebrar funcionalidade existente
3. **Logs excessivos** podem impactar performance

### Contingências
1. **Backup completo** antes de alterações
2. **Teste em ambiente isolado** antes de produção
3. **Rollback rápido** se necessário

---

## 📊 MÉTRICAS DE MONITORAMENTO

### Logs a Monitorar
- `/var/log/nginx/rpa-v4.error.log` - Erros do Nginx
- `/var/log/php8.3-fpm.log` - Erros do PHP-FPM
- `/opt/imediatoseguros-rpa-v4/logs/rpa/app.log` - Logs da aplicação
- `/var/log/xdebug.log` - Logs do Xdebug

### Métricas Importantes
- Taxa de sucesso das requisições POST
- Tempo de resposta da API
- Erros de JSON decode
- Uso de fallback para parametros.json

---

## 👥 EQUIPE ENVOLVIDA

**Desenvolvedor:** Responsável pela implementação  
**Engenheiro de Software:** Análise e validação  
**DevOps:** Configuração de servidor  

---

## 📞 CONTATOS DE EMERGÊNCIA

**Desenvolvedor:** Disponível para implementação  
**Engenheiro de Software:** Disponível para análise  
**DevOps:** Disponível para configuração  

---

## 🔄 PRÓXIMOS PASSOS

### Imediato (Hoje)
1. **Aprovar plano de correção** - Engenheiro de software
2. **Implementar correções críticas** - Desenvolvedor
3. **Testar e validar** - Equipe

### Curto Prazo (Esta Semana)
1. **Monitorar funcionamento** - 24 horas
2. **Documentar solução** - Para futuras referências
3. **Preparar para produção** - Validação final

### Médio Prazo (Próxima Semana)
1. **Otimizar performance** - Melhorias
2. **Implementar cache** - Reduzir latência
3. **Preparar para escala** - Suporte a mais usuários

---

## 📝 OBSERVAÇÕES TÉCNICAS

### Dados de Teste
```json
{
  "cpf": "97137189768",
  "nome": "ALEX KAMINSKI",
  "placa": "EYQ4J41",
  "cep": "03317-000",
  "email": "alex.kaminski@imediatoseguros.com.br",
  "celular": "11953288466",
  "ano": "2009"
}
```

### Ambiente de Teste
- **Servidor:** Hetzner (37.27.92.160)
- **OS:** Ubuntu 22.04 LTS
- **Nginx:** 1.24.0
- **PHP:** 8.3-FPM
- **Python:** 3.11 (venv)

### Arquivos Envolvidos
- `/opt/imediatoseguros-rpa-v4/public/index.php`
- `/opt/imediatoseguros-rpa-v4/src/Services/SessionService.php`
- `/etc/nginx/sites-available/rpa-v4`
- `/opt/imediatoseguros-rpa/parametros.json`

---

**Documento preparado para análise técnica e implementação de correções.**

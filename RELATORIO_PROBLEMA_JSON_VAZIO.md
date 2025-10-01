# RELATÓRIO TÉCNICO: PROBLEMA JSON VAZIO NO PHP

## 📋 INFORMAÇÕES GERAIS

**Data:** 01/10/2025  
**Sistema:** RPA V4 - API PHP  
**Ambiente:** Hetzner Server (37.27.92.160)  
**Versão:** RPA V4 com Progress Tracker JSON  
**Prioridade:** CRÍTICA  

---

## 🚨 PROBLEMA IDENTIFICADO

### Descrição
O sistema RPA V4 não está recebendo dados JSON corretamente via API. Mesmo enviando dados válidos via `curl`, o PHP recebe um array vazio (`[]`) em vez dos dados esperados.

### Impacto
- **Funcionalidade:** RPA não executa com dados dinâmicos
- **Fallback:** Sistema usa `parametros.json` em vez de dados da requisição
- **Progress Tracker:** Não funciona corretamente
- **Produção:** Sistema não está pronto para uso

### Evidências
```json
// Log do sistema mostra dados vazios
{"timestamp":"2025-10-01 17:09:13","level":"INFO","message":"RPA start request received","context":{"data":[]}}

// Script gerado usa fallback
"Fonte de dados: parametros.json (fallback)"

// RPA não inicia automaticamente
"status": "pending"
```

---

## 🔍 ANÁLISE TÉCNICA

### Arquitetura do Sistema
```
Frontend (Webflow) → API PHP (index.php) → SessionService → RPA Python
```

### Fluxo Esperado
1. **Frontend** envia JSON via POST
2. **Nginx** recebe requisição
3. **PHP-FPM** processa requisição
4. **index.php** decodifica JSON
5. **SessionService** gera script RPA
6. **RPA Python** executa com dados

### Ponto de Falha Identificado
**Localização:** `/opt/imediatoseguros-rpa-v4/public/index.php` linha 78
```php
$input = json_decode(file_get_contents('php://input'), true);
$response = $controller->startRPA($input ?: []);
```

### Possíveis Causas
1. **Nginx:** Configuração incorreta para POST requests
2. **PHP-FPM:** Problemas de buffer ou timeout
3. **Encoding:** Problemas de charset ou BOM
4. **JSON:** Dados corrompidos durante transmissão
5. **PHP:** Configurações restritivas (post_max_size, etc.)

---

## 🧪 PLANO DE INVESTIGAÇÃO

### Fase 1: Verificação da Requisição HTTP
**Objetivo:** Confirmar que dados são enviados corretamente

#### Teste 1.1: Validação do Curl
```bash
curl -v -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'
```

**Critério de Sucesso:** Content-Length > 0, dados visíveis no verbose

#### Teste 1.2: Verificação de Headers
```bash
curl -I -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"test":"data"}'
```

**Critério de Sucesso:** Content-Type: application/json presente

### Fase 2: Verificação do Nginx
**Objetivo:** Confirmar que Nginx está passando dados corretamente

#### Teste 2.1: Configuração do Site
```bash
ssh root@37.27.92.160 "cat /etc/nginx/sites-available/imediatoseguros-rpa-v4"
```

**Verificar:**
- `client_max_body_size`
- `client_body_buffer_size`
- `proxy_pass` ou `fastcgi_pass`
- Headers de proxy

#### Teste 2.2: Logs do Nginx
```bash
ssh root@37.27.92.160 "tail -20 /var/log/nginx/access.log | grep POST"
ssh root@37.27.92.160 "tail -20 /var/log/nginx/error.log"
```

**Critério de Sucesso:** Requisição aparece nos logs, sem erros

### Fase 3: Verificação do PHP
**Objetivo:** Confirmar que PHP recebe dados

#### Teste 3.1: Script de Teste Direto
```bash
ssh root@37.27.92.160 "cat > /tmp/test_php_input.php << 'EOF'
<?php
echo \"Content-Type: application/json\n\n\";
echo json_encode([
    'raw_input' => file_get_contents('php://input'),
    'raw_length' => strlen(file_get_contents('php://input')),
    'post_data' => \$_POST,
    'get_data' => \$_GET,
    'request_method' => \$_SERVER['REQUEST_METHOD'],
    'content_type' => \$_SERVER['CONTENT_TYPE'] ?? 'not_set',
    'content_length' => \$_SERVER['CONTENT_LENGTH'] ?? 'not_set'
]);
?>
EOF"
```

#### Teste 3.2: Execução do Teste
```bash
curl -X POST http://37.27.92.160/tmp/test_php_input.php \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI"}'
```

**Critério de Sucesso:** `raw_input` contém dados JSON válidos

### Fase 4: Debug do index.php
**Objetivo:** Identificar ponto exato da falha

#### Teste 4.1: Logs Temporários
```bash
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/public/index.php /opt/imediatoseguros-rpa-v4/public/index.php.backup"

ssh root@37.27.92.160 "sed -i '77a\                error_log(\"DEBUG: Raw input length: \" . strlen(file_get_contents(\"php://input\")));' /opt/imediatoseguros-rpa-v4/public/index.php"
```

#### Teste 4.2: Monitoramento de Logs
```bash
# Terminal 1
ssh root@37.27.92.160 "tail -f /var/log/php8.3-fpm.log"

# Terminal 2
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI"}'
```

**Critério de Sucesso:** Log mostra length > 0

### Fase 5: Teste de json_decode
**Objetivo:** Confirmar funcionamento do json_decode

#### Teste 5.1: Teste Isolado
```bash
ssh root@37.27.92.160 "cat > /tmp/test_json_decode.php << 'EOF'
<?php
\$test_json = '{\"cpf\":\"97137189768\",\"nome\":\"ALEX KAMINSKI\"}';
\$decoded = json_decode(\$test_json, true);
echo \"Test JSON: \" . \$test_json . \"\n\";
echo \"Decoded: \" . print_r(\$decoded, true) . \"\n\";
echo \"JSON Error: \" . json_last_error_msg() . \"\n\";
?>
EOF"

ssh root@37.27.92.160 "php /tmp/test_json_decode.php"
```

**Critério de Sucesso:** JSON decodificado corretamente, sem erros

### Fase 6: Verificação de Encoding
**Objetivo:** Confirmar que não há problemas de encoding

#### Teste 6.1: Análise do Arquivo
```bash
ssh root@37.27.92.160 "file /opt/imediatoseguros-rpa-v4/public/index.php"
ssh root@37.27.92.160 "hexdump -C /opt/imediatoseguros-rpa-v4/public/index.php | head -20"
```

#### Teste 6.2: Verificação de BOM
```bash
ssh root@37.27.92.160 "od -c /opt/imediatoseguros-rpa-v4/public/index.php | head -5"
```

**Critério de Sucesso:** Arquivo UTF-8 sem BOM

### Fase 7: Configuração PHP
**Objetivo:** Verificar configurações que podem afetar input

#### Teste 7.1: Configurações Relevantes
```bash
ssh root@37.27.92.160 "php -i | grep -E 'post_max_size|upload_max_filesize|max_input_vars|max_execution_time'"
```

#### Teste 7.2: Teste de POST Simples
```bash
ssh root@37.27.92.160 "cat > /tmp/test_simple_post.php << 'EOF'
<?php
echo \"POST: \" . print_r(\$_POST, true) . \"\n\";
echo \"Raw input: \" . file_get_contents('php://input') . \"\n\";
?>
EOF"

curl -X POST http://37.27.92.160/tmp/test_simple_post.php \
  -d 'cpf=97137189768&nome=ALEX KAMINSKI'
```

**Critério de Sucesso:** POST funciona, raw input funciona

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
- [ ] Código limpo e documentado
- [ ] Logs adequados para debug
- [ ] Tratamento de erros robusto

---

## 🔧 SOLUÇÕES PROPOSTAS

### Solução 1: Correção de Configuração Nginx
**Se problema for no Nginx:**
```nginx
client_max_body_size 10M;
client_body_buffer_size 128k;
client_body_timeout 60s;
```

### Solução 2: Correção de Configuração PHP
**Se problema for no PHP:**
```ini
post_max_size = 10M
upload_max_filesize = 10M
max_input_vars = 3000
```

### Solução 3: Correção de Código PHP
**Se problema for no código:**
```php
$rawInput = file_get_contents('php://input');
if (empty($rawInput)) {
    error_log("Empty input received");
    return ['success' => false, 'error' => 'No data received'];
}
$input = json_decode($rawInput, true);
if (json_last_error() !== JSON_ERROR_NONE) {
    error_log("JSON decode error: " . json_last_error_msg());
    return ['success' => false, 'error' => 'Invalid JSON'];
}
```

### Solução 4: Implementação de Fallback Robusto
**Se problema for intermitente:**
```php
$input = json_decode(file_get_contents('php://input'), true);
if (empty($input) || json_last_error() !== JSON_ERROR_NONE) {
    // Log do problema
    error_log("JSON input failed, using fallback");
    // Usar dados padrão ou retornar erro
    $input = $this->getDefaultData();
}
```

---

## 📊 MÉTRICAS DE MONITORAMENTO

### Logs a Monitorar
- `/var/log/nginx/access.log` - Requisições HTTP
- `/var/log/nginx/error.log` - Erros do Nginx
- `/var/log/php8.3-fpm.log` - Erros do PHP-FPM
- `/opt/imediatoseguros-rpa-v4/logs/rpa/app.log` - Logs da aplicação

### Métricas Importantes
- Taxa de sucesso das requisições POST
- Tempo de resposta da API
- Erros de JSON decode
- Uso de fallback para parametros.json

---

## 🚀 PRÓXIMOS PASSOS

### Imediato (Hoje)
1. Executar Fase 1 e 3 do plano de investigação
2. Identificar causa raiz
3. Implementar correção

### Curto Prazo (Esta Semana)
1. Testar correção com dados reais
2. Validar progress tracker
3. Preparar para produção

### Médio Prazo (Próxima Semana)
1. Implementar monitoramento
2. Documentar solução
3. Treinar equipe

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
- `/etc/nginx/sites-available/imediatoseguros-rpa-v4`
- `/opt/imediatoseguros-rpa/parametros.json`

---

## 👥 EQUIPE ENVOLVIDA

**Desenvolvedor:** Responsável pela implementação  
**Engenheiro de Software:** Análise e validação  
**DevOps:** Configuração de servidor  

---

**Documento preparado para análise técnica e implementação de correção.**

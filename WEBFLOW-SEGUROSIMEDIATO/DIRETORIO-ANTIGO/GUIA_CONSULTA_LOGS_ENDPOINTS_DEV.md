# 📋 GUIA DE CONSULTA DE LOGS - ENDPOINTS DE DESENVOLVIMENTO

## 🔍 Localização dos Logs

### **add_travelangels_dev.php**
**Arquivo de log**: `/var/www/html/dev/logs/travelangels_dev.txt`

**Configuração no código**:
```php
// Arquivo: /var/www/html/dev/config/dev_config.php
$DEV_LOGGING = [
    'travelangels' => __DIR__ . '/../logs/travelangels_dev.txt',
    ...
];
```

**Função de log**:
```php
// Arquivo: /var/www/html/dev/webhooks/add_travelangels_dev.php
function logDevWebhook($event, $data, $success = true)
{
    global $DEBUG_LOG_FILE, $LOG_PREFIX, $is_dev, $GLOBAL_REQUEST_ID;
    
    $log_entry = $LOG_PREFIX . json_encode($log_data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . PHP_EOL;
    file_put_contents($DEBUG_LOG_FILE, $log_entry, FILE_APPEND | LOCK_EX);
}
```

**Prefixo do log**: `[DEV-TRAVELANGELS]`

---

### **add_webflow_octa_dev.php**
**Arquivo de log**: `/var/www/html/dev/logs/webhook_octadesk_dev.txt`

**Nota**: Existe também `/var/www/html/dev/logs/octadesk_dev.txt` que pode conter logs relacionados, mas o arquivo principal usado pelo endpoint é `webhook_octadesk_dev.txt`

**Função de log**:
```php
// Arquivo: /var/www/html/dev/webhooks/add_webflow_octa_dev.php
function logDevWebhook($action, $data = null, $success = true)
{
    $logFile = __DIR__ . '/../logs/webhook_octadesk_dev.txt';
    $timestamp = date('Y-m-d H:i:s');
    $status = $success ? 'SUCCESS' : 'ERROR';
    
    $logEntry = "[{$timestamp}] [{$status}] [OCTADESK-DEV] {$action}";
    if ($data !== null) {
        $logEntry .= " | Data: " . json_encode($data, JSON_UNESCAPED_UNICODE);
    }
    $logEntry .= PHP_EOL;
    
    file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}
```

**Prefixo do log**: `[OCTADESK-DEV]`

---

## 📊 Estrutura dos Logs

### **add_travelangels_dev.php**

**Formato**:
```
[DEV-TRAVELANGELS] {
    "timestamp": "2025-10-29 18:00:00",
    "environment": "development",
    "webhook": "travelangels",
    "event": "nome_do_evento",
    "success": true/false,
    "data": { ... },
    "request_id": "dev_travel_69025...",
    "memory_usage": 2097152,
    "execution_time": 0.001234
}
```

**Eventos principais**:
- `webhook_started` - Início da requisição
- `json_decode_error` - Erro ao decodificar JSON
- `data_received` - Dados recebidos com sucesso
- `signature_validation` - Validação de signature
- `data_extracted` - Dados extraídos do payload
- `lead_data_prepared` - Dados preparados para o CRM
- `crm_response` - Resposta do CRM
- `webhook_completed` - Requisição finalizada

---

### **add_webflow_octa_dev.php**

**Formato**:
```
[2025-10-29 18:00:00] [SUCCESS/ERROR] [OCTADESK-DEV] nome_da_acao | Data: {...}
```

**Eventos principais**:
- `octadesk_request` - Requisição iniciada
- `octadesk_response` - Resposta recebida
- `octadesk_contact_request` - Busca/criação de contato
- `octadesk_conversation_request` - Criação de conversa
- `octadesk_message_request` - Envio de mensagem
- `webhook_received` - Webhook recebido
- `webflow_data_parsed` - Dados do Webflow parseados
- `webhook_success` - Webhook bem-sucedido
- `webhook_error` - Erro no webhook

---

## 🔧 Como Acessar os Logs

### **Via SSH (Recomendado)**

```bash
# Conectar ao servidor
ssh root@46.62.174.150

# Ver últimas 50 linhas do log travelangels
tail -50 /var/www/html/dev/logs/travelangels_dev.txt

# Ver últimas 50 linhas do log octadesk
tail -50 /var/www/html/dev/logs/webhook_octadesk_dev.txt

# Ver últimas 100 linhas em tempo real (watch)
tail -f /var/www/html/dev/logs/travelangels_dev.txt

# Ver tamanho do arquivo
ls -lh /var/www/html/dev/logs/travelangels_dev.txt
ls -lh /var/www/html/dev/logs/webhook_octadesk_dev.txt
```

---

## 🔎 Comandos Úteis para Análise

### **1. Ver últimas requisições**

```bash
# Últimas 20 requisições do travelangels
tail -100 /var/www/html/dev/logs/travelangels_dev.txt | grep -A 5 "webhook_started"

# Últimas 20 requisições do octadesk
tail -100 /var/www/html/dev/logs/webhook_octadesk_dev.txt | grep -A 3 "webhook_received"
```

---

### **2. Procurar por erros**

```bash
# Erros no travelangels
grep -i "error\|erro\|fail" /var/www/html/dev/logs/travelangels_dev.txt | tail -20

# Erros no octadesk
grep -i "error\|erro\|fail" /var/www/html/dev/logs/webhook_octadesk_dev.txt | tail -20

# Erros de JSON decoding no travelangels
grep "json_decode_error" /var/www/html/dev/logs/travelangels_dev.txt | tail -10
```

---

### **3. Filtrar por data/hora**

```bash
# Logs de hoje
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt

# Logs de uma data específica
grep "2025-10-29" /var/www/html/dev/logs/travelangels_dev.txt

# Logs de um horário específico
grep "2025-10-29 18:" /var/www/html/dev/logs/travelangels_dev.txt
```

---

### **4. Buscar por request_id específico**

```bash
# Se você tiver um request_id do erro
grep "dev_travel_69025efb21c345" /var/www/html/dev/logs/travelangels_dev.txt -A 10
```

---

### **5. Ver dados recebidos (payload)**

```bash
# Ver payloads recebidos
grep "data_received\|webflow_data_parsed" /var/www/html/dev/logs/travelangels_dev.txt | tail -5

# Ver dados extraídos
grep "data_extracted" /var/www/html/dev/logs/travelangels_dev.txt | tail -5
```

---

### **6. Analisar JSON malformado**

```bash
# Ver tentativas de correção de JSON
grep "json_fix" /var/www/html/dev/logs/travelangels_dev.txt | tail -20

# Ver raw_input quando há erro
grep -A 3 "json_decode_error" /var/www/html/dev/logs/travelangels_dev.txt | tail -30
```

---

### **7. Contar requisições**

```bash
# Quantas requisições hoje
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "webhook_started" | wc -l

# Quantos erros hoje
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep -i "error\|erro" | wc -l
```

---

### **8. Ver formato JSON formatado**

```bash
# Ver última entrada formatada
tail -1 /var/www/html/dev/logs/travelangels_dev.txt | sed 's/.*\[DEV-TRAVELANGELS\] //' | python3 -m json.tool

# Ver última entrada do octadesk formatada
tail -1 /var/www/html/dev/logs/webhook_octadesk_dev.txt
```

---

## 📝 Exemplos de Consulta

### **Verificar se uma chamada específica funcionou**

```bash
# 1. Identificar a requisição pela hora (ex: 18:30:00)
grep "2025-10-29 18:30:" /var/www/html/dev/logs/travelangels_dev.txt

# 2. Ver todo o fluxo dessa requisição
grep "dev_travel_XXXXX" /var/www/html/dev/logs/travelangels_dev.txt -A 3 | head -50
```

---

### **Debugar erro de JSON**

```bash
# 1. Ver último erro de JSON
grep "json_decode_error" /var/www/html/dev/logs/travelangels_dev.txt | tail -1

# 2. Extrair o raw_input do erro
grep -A 10 "json_decode_error" /var/www/html/dev/logs/travelangels_dev.txt | \
  grep "raw_input" | tail -1 | \
  sed 's/.*"raw_input": "//;s/".*//' | \
  sed 's/\\"/"/g' | \
  python3 -m json.tool
```

---

### **Verificar chamadas do modal WhatsApp**

```bash
# Buscar por "NOVO CLIENTE WHATSAPP" no nome
grep "NOVO CLIENTE WHATSAPP" /var/www/html/dev/logs/travelangels_dev.txt | tail -5

# Ver dados extraídos dessas chamadas
grep -B 2 -A 10 "NOVO CLIENTE WHATSAPP" /var/www/html/dev/logs/travelangels_dev.txt | tail -20
```

---

## 🚨 Troubleshooting

### **Log vazio ou não atualizando**

```bash
# Verificar permissões
ls -la /var/www/html/dev/logs/

# Verificar se o diretório existe
ls -la /var/www/html/dev/logs/

# Testar escrita
echo "teste" >> /var/www/html/dev/logs/travelangels_dev.txt
```

---

### **Log muito grande**

```bash
# Ver tamanho
du -h /var/www/html/dev/logs/travelangels_dev.txt

# Ver últimas linhas apenas
tail -1000 /var/www/html/dev/logs/travelangels_dev.txt > /tmp/ultimas_linhas.txt

# Limpar log (CUIDADO - fazer backup antes!)
cp /var/www/html/dev/logs/travelangels_dev.txt /var/www/html/dev/logs/travelangels_dev.txt.backup
> /var/www/html/dev/logs/travelangels_dev.txt
```

---

## 📂 Resumo dos Arquivos

| Endpoint | Arquivo de Log | Caminho Completo | Tamanho Atual | Prefixo |
|----------|---------------|------------------|---------------|---------|
| `add_travelangels_dev.php` | `travelangels_dev.txt` | `/var/www/html/dev/logs/travelangels_dev.txt` | ~687KB | `[DEV-TRAVELANGELS]` |
| `add_webflow_octa_dev.php` | `webhook_octadesk_dev.txt` | `/var/www/html/dev/logs/webhook_octadesk_dev.txt` | ~52KB | `[OCTADESK-DEV]` |

**Nota**: Existe também `octadesk_dev.txt` (~178KB) que pode conter logs relacionados do simulador OctaDesk.

---

**Última atualização**: 2025-10-29  
**Ambiente**: Desenvolvimento  
**Servidor**: `root@46.62.174.150`


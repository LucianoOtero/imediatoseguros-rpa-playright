# 🔍 PROCESSO DE VERIFICAÇÃO DE LOGS - WEBHOOK FLYINGDONKEYS V2

## SEQUÊNCIA DE VERIFICAÇÃO

### 1. IDENTIFICAR O REQUEST_ID
```bash
# Buscar pelo email ou timestamp do teste
grep -i "EMAIL_DO_TESTE" /var/www/html/logs/flyingdonkeys_prod.txt | tail -1
# OU buscar pelo timestamp
grep "YYYY-MM-DD HH:MM:SS" /var/www/html/logs/flyingdonkeys_prod.txt | tail -1
# Extrair o request_id da primeira linha encontrada
```

### 2. VERIFICAR SEQUÊNCIA COMPLETA DE EVENTOS (com o request_id encontrado)
```bash
# Buscar TODOS os eventos para esse request_id
grep "REQUEST_ID_AQUI" /var/www/html/logs/flyingdonkeys_prod.txt

# Filtrar apenas os eventos principais (sequência esperada):
grep "REQUEST_ID_AQUI" /var/www/html/logs/flyingdonkeys_prod.txt | grep -E '(event|status|success)' | grep -o '"event":"[^"]*"'
```

### 3. VERIFICAR SIGNATURE VALIDATION
```bash
grep "REQUEST_ID_AQUI" /var/www/html/logs/flyingdonkeys_prod.txt | grep "signature_validation"
# Esperado: "status":"valid" OU "status":"failed"
```

### 4. VERIFICAR PROCESSAMENTO DOS DADOS
```bash
grep "REQUEST_ID_AQUI" /var/www/html/logs/flyingdonkeys_prod.txt | grep -E "(data_received|data_processing_complete|lead_data_prepared)"
# Esperado: success: true
```

### 5. VERIFICAR TENTATIVA DE CRIAÇÃO DO LEAD
```bash
grep "REQUEST_ID_AQUI" /var/www/html/logs/flyingdonkeys_prod.txt | grep -E "(flyingdonkeys_lead_creation_started|flyingdonkeys_api_response|curl_request_complete_lead)"
# Esperado: 
# - flyingdonkeys_lead_creation_started (indica que tentou criar)
# - flyingdonkeys_api_response (resposta da API)
```

### 6. VERIFICAR SE LEAD FOI CRIADO
```bash
grep "REQUEST_ID_AQUI" /var/www/html/logs/flyingdonkeys_prod.txt | grep -E "(flyingdonkeys_lead_created|lead_id|opportunity_created)"
# Esperado: flyingdonkeys_lead_created com lead_id
```

### 7. VERIFICAR ERROS/EXCEÇÕES
```bash
grep "REQUEST_ID_AQUI" /var/www/html/logs/flyingdonkeys_prod.txt | grep -E "(exception|error|failed)" | grep -v "signature_validation_failed"
# Se houver: analisar o erro específico
```

### 8. VERIFICAR CONCLUSÃO DO WEBHOOK
```bash
grep "REQUEST_ID_AQUI" /var/www/html/logs/flyingdonkeys_prod.txt | grep "webhook_completed"
# Esperado: webhook_completed com execution_time
```

## SEQUÊNCIA ESPERADA DE EVENTOS (SUCESSO)

1. ✅ `webhook_started`
2. ✅ `signature_validation` → `status: "valid"`
3. ✅ `data_received`
4. ✅ `api_v2_payload_decoded`
5. ✅ `data_processing_complete`
6. ✅ `crm_connection`
7. ✅ `field_mapping`
8. ✅ `lead_data_prepared`
9. ✅ `espocrm_request_details`
10. ✅ `processing_flyingdonkeys`
11. ✅ `curl_request_complete_lead`
12. ✅ `flyingdonkeys_lead_creation_started`
13. ✅ `flyingdonkeys_api_response`
14. ✅ `flyingdonkeys_lead_created` → **COM lead_id**
15. ✅ `opportunity_data_prepared`
16. ✅ `opportunity_created` → **COM opportunity_id**
17. ✅ `webhook_completed`

## PONTOS DE FALHA COMUNS

- ❌ `signature_validation_failed` → Assinatura inválida
- ❌ `flyingdonkeys_exception` → Erro na criação do lead
- ❌ `flyingdonkeys_lead_creation_missing_id` → Lead criado mas sem ID retornado
- ❌ Sem `webhook_completed` → Processo interrompido/prematuro

## COMANDO COMPLETO DE ANÁLISE (SUBSTITUIR EMAIL_DO_TESTE)

```bash
# 1. Encontrar request_id
REQUEST_ID=$(grep -i "EMAIL_DO_TESTE" /var/www/html/logs/flyingdonkeys_prod.txt | tail -1 | grep -o 'prod_fd_[^"]*' | head -1)

# 2. Mostrar todos os eventos desse request
echo "=== EVENTOS DO REQUEST ==="
grep "$REQUEST_ID" /var/www/html/logs/flyingdonkeys_prod.txt | grep -o '"event":"[^"]*"' | sort | uniq

# 3. Verificar signature
echo -e "\n=== SIGNATURE VALIDATION ==="
grep "$REQUEST_ID" /var/www/html/logs/flyingdonkeys_prod.txt | grep "signature_validation"

# 4. Verificar criação do lead
echo -e "\n=== CRIAÇÃO DO LEAD ==="
grep "$REQUEST_ID" /var/www/html/logs/flyingdonkeys_prod.txt | grep -E "(flyingdonkeys_lead_creation|flyingdonkeys_lead_created|lead_id)"

# 5. Verificar erros
echo -e "\n=== ERROS ==="
grep "$REQUEST_ID" /var/www/html/logs/flyingdonkeys_prod.txt | grep -E "(exception|error|failed)" | grep -v "signature_validation"

# 6. Verificar conclusão
echo -e "\n=== CONCLUSÃO ==="
grep "$REQUEST_ID" /var/www/html/logs/flyingdonkeys_prod.txt | grep "webhook_completed"
```




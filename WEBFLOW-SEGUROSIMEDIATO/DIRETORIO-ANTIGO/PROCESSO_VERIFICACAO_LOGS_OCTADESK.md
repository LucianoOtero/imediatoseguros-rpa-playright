# 🔍 PROCESSO DE VERIFICAÇÃO DE LOGS - WEBHOOK OCTADESK V2

## ARQUIVO DE LOG
`/var/www/html/logs/webhook_octadesk_prod.txt`

## SEQUÊNCIA DE VERIFICAÇÃO

### 1. IDENTIFICAR O TESTE
- Buscar pelo número de telefone do usuário
- Buscar pelo email (se fornecido)
- Buscar pelo timestamp aproximado

### 2. VERIFICAR SEQUÊNCIA COMPLETA DE EVENTOS
```bash
# Buscar por telefone ou email
grep "NUMERO_TELEFONE_OU_EMAIL" /var/www/html/logs/webhook_octadesk_prod.txt | tail -20
```

### 3. VERIFICAR SIGNATURE VALIDATION
- Evento: `signature_validation`
- Esperado: `"status":"valid"`
- Se `failed`: requisição rejeitada

### 4. VERIFICAR PROCESSAMENTO DOS DADOS
- `webhook_received` → requisição chegou
- `webflow_data_parsed` → dados parseados com sucesso
- `contact_data_mapped` → dados mapeados
- Verificar se `ddd` e `celular` foram extraídos corretamente

### 5. VERIFICAR VALIDAÇÃO DE TELEFONE
- `validation_error` → se telefone inválido
- Verificar se `ddd` e `celular` estão presentes e não vazios

### 6. VERIFICAR ENVIO AO OCTADESK
- `octadesk_send_template_payload` → payload preparado
- Verificar resposta da API do OctaDesk
- `http_code` → deve ser 200-299 para sucesso
- `conversationId` → ID da conversa criada

### 7. VERIFICAR ERROS/EXCEÇÕES
- Buscar por `error`, `exception`, `failed`
- Analisar mensagens de erro específicas

### 8. VERIFICAR CONCLUSÃO
- Verificar se houve resposta de sucesso
- Verificar se conversa foi criada no OctaDesk

## SEQUÊNCIA ESPERADA DE EVENTOS (SUCESSO)

1. ✅ `webhook_received` → requisição recebida
2. ✅ `signature_validation` → `status: "valid"`
3. ✅ `webflow_data_parsed` → dados parseados
4. ✅ `contact_data_mapped` → dados mapeados (com `ddd` e `celular` preenchidos)
5. ✅ `octadesk_send_template_payload` → payload preparado
6. ✅ Resposta HTTP 200-299 → sucesso na API
7. ✅ `conversationId` retornado → conversa criada
8. ✅ Resposta de sucesso ao cliente

## PONTOS DE FALHA COMUNS

- ❌ `signature_validation_failed` → Assinatura inválida
- ❌ `validation_error` → `"DDD e CELULAR obrigatórios"` → mapeamento incorreto
- ❌ `phone_validation_error` → telefone inválido após formatação
- ❌ HTTP 400/401/500 → erro na API do OctaDesk
- ❌ Sem `conversationId` → conversa não criada

## COMANDOS ÚTEIS

```bash
# 1. Buscar por telefone (formato: 11987654321 ou 1198765-4321)
grep "NUMERO_TELEFONE" /var/www/html/logs/webhook_octadesk_prod.txt | tail -30

# 2. Verificar signature
grep "NUMERO_TELEFONE" /var/www/html/logs/webhook_octadesk_prod.txt | grep "signature_validation"

# 3. Verificar mapeamento de dados
grep "NUMERO_TELEFONE" /var/www/html/logs/webhook_octadesk_prod.txt | grep "contact_data_mapped"

# 4. Verificar envio ao OctaDesk
grep "NUMERO_TELEFONE" /var/www/html/logs/webhook_octadesk_prod.txt | grep "octadesk_send_template\|http_code\|conversationId"

# 5. Verificar erros
grep "NUMERO_TELEFONE" /var/www/html/logs/webhook_octadesk_prod.txt | grep -E "(error|exception|failed|validation_error)"
```




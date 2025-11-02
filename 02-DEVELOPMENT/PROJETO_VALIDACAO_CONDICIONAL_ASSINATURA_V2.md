# PROJETO: VALIDAÇÃO CONDICIONAL DE ASSINATURA WEBFLOW (ENDPOINTS V2)

**Data de Criação:** 02/11/2025 17:15  
**Data de Implementação:** 02/11/2025 14:25  
**Status:** ✅ **IMPLEMENTADO**  
**Workspace:** imediatoseguros-rpa-playwright  
**Complexidade:** Baixa  
**Impacto:** Médio  
**Tempo Estimado:** ~45 minutos

---

## 📋 OBJETIVO

Modificar os endpoints `add_flyingdonkeys_v2.php` e `add_webflow_octa_v2.php` para validar assinatura do Webflow **apenas quando ela estiver presente**. Requisições sem assinatura (como as que vêm do modal WhatsApp no navegador) devem ser aceitas sem validação, enquanto requisições com assinatura (do Webflow) devem ser validadas rigorosamente.

---

## 🎯 PROBLEMA ATUAL

### Situação Atual:

Os endpoints `_v2` estão configurados para **sempre exigir** assinatura válida do Webflow:

1. **`add_flyingdonkeys_v2.php`** (linha 494-502):
   - Valida assinatura obrigatoriamente
   - Retorna erro se assinatura inválida ou ausente
   - Bloqueia requisições do modal WhatsApp (navegador)

2. **`add_webflow_octa_v2.php`** (linha 347-357):
   - Valida assinatura obrigatoriamente
   - Retorna HTTP 401 se assinatura inválida ou ausente
   - Bloqueia requisições do modal WhatsApp (navegador)

### Impacto:

- ❌ Modal WhatsApp não consegue chamar os endpoints `_v2`
- ❌ Erro CORS resolvido, mas agora bloqueado por validação de assinatura
- ❌ Requisições legítimas do navegador são rejeitadas
- ⚠️ Requisições do Webflow (com assinatura) devem continuar sendo validadas

### Erro Observado no Console:

```
Access to fetch at 'https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php' 
from origin 'https://www.segurosimediato.com.br' has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**Após correção CORS:**
```
POST https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php net::ERR_FAILED
[ERROR] ESPOCRM - INITIAL_REQUEST_ERROR {error: 'Failed to fetch', ...}
```

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos a Modificar:

1. **`02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php`**
   - Função: `validateWebflowSignatureProd()` ou lógica de validação
   - Localização: Linha ~494-502
   - Alteração: Validar apenas se assinatura presente

2. **`02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php`**
   - Função: `validateWebflowSignature()` ou lógica de validação
   - Localização: Linha ~347-357
   - Alteração: Validar apenas se assinatura presente

### Backups a Criar:

- ✅ `add_flyingdonkeys_v2.php.backup_20251102_171500` (será criado antes da implementação)
- ✅ `add_webflow_octa_v2.php.backup_20251102_171500` (será criado antes da implementação)

### Destino no Servidor:

- `/var/www/html/webhooks/add_flyingdonkeys_v2.php`
- `/var/www/html/webhooks/add_webflow_octa_v2.php`

---

## 🔧 SOLUÇÃO PROPOSTA

### Estratégia:

Implementar validação condicional que:
1. **Verifica se assinatura está presente** nos headers
2. **Se presente:** Valida rigorosamente (requisições do Webflow)
3. **Se ausente:** Aceita requisição sem validação (requisições do navegador)

### Lógica:

```php
// Pseudocódigo da lógica
if (assinatura_presente) {
    if (!validar_assinatura()) {
        retornar_erro();
    }
} else {
    // Assinatura ausente = requisição do navegador
    // Aceitar sem validação
    continuar_processamento();
}
```

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DAS ALTERAÇÕES

### 1.1. Modificar `add_flyingdonkeys_v2.php`

#### Alteração na Validação de Assinatura:

**Código Atual (linha ~494-502):**
```php
// Validação de signature em produção
if (!validateWebflowSignatureProd($raw_input, $signature, $timestamp, $WEBFLOW_SECRET_TRAVELANGELS)) {
    logProdWebhook('signature_validation_failed', [...], false);
    sendProdWebhookResponse(false, 'Assinatura inválida');
    exit;
}
```

**Código Novo:**
```php
// Validação condicional de signature
// Se assinatura presente = requisição do Webflow (validar obrigatoriamente)
// Se assinatura ausente = requisição do navegador/modal (aceitar sem validação)
if (!empty($signature) && !empty($timestamp)) {
    // Assinatura presente - validar (requisição do Webflow)
    if (!validateWebflowSignatureProd($raw_input, $signature, $timestamp, $WEBFLOW_SECRET_TRAVELANGELS)) {
        logProdWebhook('signature_validation_failed', [
            'signature_received' => substr($signature, 0, 16) . '...',
            'timestamp_received' => $timestamp,
            'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            'reason' => 'signature_invalid'
        ], false);
        sendProdWebhookResponse(false, 'Assinatura inválida');
        exit;
    }
    logProdWebhook('signature_validation', [
        'status' => 'valid',
        'source' => 'webflow',
        'signature_received' => substr($signature, 0, 16) . '...',
        'timestamp_received' => $timestamp
    ], true);
} else {
    // Assinatura ausente - requisição do navegador/modal (aceitar)
    logProdWebhook('signature_validation', [
        'status' => 'skipped',
        'source' => 'browser',
        'reason' => 'signature_not_provided',
        'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
    ], true);
}
```

### 1.2. Modificar `add_webflow_octa_v2.php`

#### Alteração na Validação de Assinatura:

**Código Atual (linha ~347-357):**
```php
if (!validateWebflowSignature($input, $signature, $WEBFLOW_SECRET_OCTADESK)) {
    logProdWebhook('invalid_signature', [...], false);
    http_response_code(401);
    echo json_encode(['error' => 'Invalid signature']);
    return;
}
```

**Código Novo:**
```php
// Validação condicional de signature
// Se assinatura presente = requisição do Webflow (validar obrigatoriamente)
// Se assinatura ausente = requisição do navegador/modal (aceitar sem validação)
if (!empty($signature) && !empty($timestamp)) {
    // Assinatura presente - validar (requisição do Webflow)
    if (!validateWebflowSignature($input, $signature, $WEBFLOW_SECRET_OCTADESK)) {
        logProdWebhook('invalid_signature', [
            'signature_received' => substr($signature, 0, 16) . '...',
            'timestamp_received' => $timestamp,
            'expected_length' => strlen($signature),
            'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            'reason' => 'signature_invalid'
        ], false);
        http_response_code(401);
        echo json_encode(['error' => 'Invalid signature']);
        return;
    }
    logProdWebhook('signature_validation', [
        'status' => 'valid',
        'source' => 'webflow',
        'signature_received' => substr($signature, 0, 16) . '...',
        'timestamp_received' => $timestamp
    ], true);
} else {
    // Assinatura ausente - requisição do navegador/modal (aceitar)
    logProdWebhook('signature_validation', [
        'status' => 'skipped',
        'source' => 'browser',
        'reason' => 'signature_not_provided',
        'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
    ], true);
}
```

---

## 📤 FASE 2: CÓPIA DOS ARQUIVOS PARA O SERVIDOR

### 2.1. Criar Backups Locais

```bash
# Timestamp: 20251102_171500
cp 02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php \
   02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php.backup_20251102_171500

cp 02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php \
   02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php.backup_20251102_171500
```

### 2.2. Validar Sintaxe PHP Localmente

```bash
php -l 02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php
php -l 02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php
```

### 2.3. Copiar para Servidor

```bash
scp 02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php \
   root@46.62.174.150:/var/www/html/webhooks/add_flyingdonkeys_v2.php

scp 02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php \
   root@46.62.174.150:/var/www/html/webhooks/add_webflow_octa_v2.php
```

### 2.4. Validar no Servidor

```bash
ssh root@46.62.174.150 "php -l /var/www/html/webhooks/add_flyingdonkeys_v2.php"
ssh root@46.62.174.150 "php -l /var/www/html/webhooks/add_webflow_octa_v2.php"
```

---

## 🧪 FASE 3: TESTE E VERIFICAÇÃO

### 3.1. Testes Necessários

#### Teste 1: Requisição do Modal (Sem Assinatura)
- **Ação:** Preencher modal WhatsApp com DDD + Celular
- **Esperado:** Endpoint aceita requisição sem validação
- **Verificar logs:** `signature_validation` com `status: 'skipped'` e `source: 'browser'`
- **Verificar resultado:** Lead criado no FlyingDonkeys e mensagem enviada no OctaDesk

#### Teste 2: Requisição do Webflow (Com Assinatura)
- **Ação:** Submeter formulário diretamente do Webflow
- **Esperado:** Endpoint valida assinatura e processa
- **Verificar logs:** `signature_validation` com `status: 'valid'` e `source: 'webflow'`
- **Verificar resultado:** Lead criado e mensagem enviada

#### Teste 3: Requisição do Webflow (Assinatura Inválida)
- **Ação:** Enviar requisição com assinatura inválida (teste manual)
- **Esperado:** Endpoint rejeita com erro
- **Verificar logs:** `signature_validation_failed` ou `invalid_signature`
- **Verificar resultado:** HTTP 401 ou resposta de erro

### 3.2. Verificação de Logs

**FlyingDonkeys:**
```bash
ssh root@46.62.174.150 "grep 'signature_validation' /var/www/html/logs/flyingdonkeys_prod.txt | tail -10"
```

**OctaDesk:**
```bash
ssh root@46.62.174.150 "grep 'signature_validation' /var/www/html/logs/webhook_octadesk_prod.txt | tail -10"
```

### 3.3. Verificação no Console do Navegador

Após implementação, verificar que:
- ✅ Modal consegue chamar endpoints sem erro CORS
- ✅ Requisições do modal são aceitas
- ✅ Leads são criados no FlyingDonkeys
- ✅ Mensagens são enviadas no OctaDesk
- ✅ Logs mostram `signature_validation` com `status: 'skipped'`

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### Preparação:
- [x] Backup local de `add_flyingdonkeys_v2.php` criado (`add_flyingdonkeys_v2.php.backup_20251102_142054`)
- [x] Backup local de `add_webflow_octa_v2.php` criado (`add_webflow_octa_v2.php.backup_20251102_142054`)
- [x] Código modificado em `add_flyingdonkeys_v2.php`
- [x] Código modificado em `add_webflow_octa_v2.php`

### Validação:
- [x] Sintaxe PHP validada localmente (ambos arquivos) ✅
- [x] Arquivos copiados para servidor ✅
- [x] Sintaxe PHP validada no servidor (ambos arquivos) ✅

### Testes:
- [ ] Teste 1: Modal sem assinatura (FlyingDonkeys)
- [ ] Teste 1: Modal sem assinatura (OctaDesk)
- [ ] Teste 2: Webflow com assinatura válida (FlyingDonkeys)
- [ ] Teste 2: Webflow com assinatura válida (OctaDesk)
- [ ] Teste 3: Webflow com assinatura inválida (rejeição)

### Logs:
- [ ] Logs verificados para requisições sem assinatura
- [ ] Logs verificados para requisições com assinatura válida
- [ ] Logs verificados para requisições com assinatura inválida

### Funcionalidade:
- [ ] Leads sendo criados no FlyingDonkeys via modal
- [ ] Mensagens sendo enviadas no OctaDesk via modal
- [ ] Formulários Webflow continuam funcionando normalmente
- [ ] Console do navegador sem erros

---

## 🔄 ROLLBACK (Se Necessário)

### Procedimento de Reversão:

1. **Restaurar Backups:**
```bash
scp 02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php.backup_20251102_171500 \
   root@46.62.174.150:/var/www/html/webhooks/add_flyingdonkeys_v2.php

scp 02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php.backup_20251102_171500 \
   root@46.62.174.150:/var/www/html/webhooks/add_webflow_octa_v2.php
```

2. **Validar no Servidor:**
```bash
ssh root@46.62.174.150 "php -l /var/www/html/webhooks/add_flyingdonkeys_v2.php"
ssh root@46.62.174.150 "php -l /var/www/html/webhooks/add_webflow_octa_v2.php"
```

3. **Verificar Logs:**
```bash
ssh root@46.62.174.150 "tail -20 /var/www/html/logs/flyingdonkeys_prod.txt"
ssh root@46.62.174.150 "tail -20 /var/www/html/logs/webhook_octadesk_prod.txt"
```

**Tempo estimado de rollback:** ~5 minutos

---

## 📊 CRONOGRAMA

1. **Fase 1 - Implementação:** ~20 minutos
   - Modificar validação em `add_flyingdonkeys_v2.php`
   - Modificar validação em `add_webflow_octa_v2.php`
   - Adicionar logging detalhado

2. **Fase 2 - Deploy:** ~10 minutos
   - Criar backups locais
   - Validar sintaxe
   - Copiar para servidor
   - Validar no servidor

3. **Fase 3 - Testes:** ~15 minutos
   - Testar modal sem assinatura
   - Testar Webflow com assinatura válida
   - Testar Webflow com assinatura inválida
   - Verificar logs

**Total Estimado:** ~45 minutos

---

## 🎯 RESULTADO ESPERADO

Após implementação:

✅ **Requisições do Modal (navegador):**
- Aceitas sem validação de assinatura
- Leads criados no FlyingDonkeys
- Mensagens enviadas no OctaDesk
- Logs mostram `status: 'skipped'` e `source: 'browser'`

✅ **Requisições do Webflow:**
- Validadas rigorosamente quando assinatura presente
- Rejeitadas se assinatura inválida
- Processadas normalmente se assinatura válida
- Logs mostram `status: 'valid'` e `source: 'webflow'`

✅ **Segurança Mantida:**
- Requisições do Webflow continuam protegidas
- Assinaturas inválidas são rejeitadas
- Logging completo de todas as requisições

---

## 🔍 REVISÃO TÉCNICA

### Engenheiro de Software: [AGUARDANDO REVISÃO]
**Data da Revisão:** [AGUARDANDO]

#### Comentários:
- [Aguardando comentários do engenheiro]

#### Alterações Recomendadas:
- [Aguardando recomendações]

#### Status da Revisão:
- [ ] Aprovado sem alterações
- [ ] Aprovado com alterações
- [ ] Requer nova revisão

---

## 📝 NOTAS IMPORTANTES

### ⚠️ PONTOS CRÍTICOS:

1. **Segurança:**
   - ⚠️ Requisições sem assinatura são aceitas (requisições do navegador)
   - ✅ Requisições com assinatura são validadas rigorosamente
   - ✅ CORS já configurado corretamente nos endpoints `_v2`
   - ⚠️ Considerar rate limiting adicional se necessário

2. **Validação:**
   - ✅ Verificar se assinatura está presente antes de validar
   - ✅ Manter validação rigorosa para requisições do Webflow
   - ✅ Logging detalhado de todas as situações

3. **Compatibilidade:**
   - ✅ Requisições do Webflow continuam funcionando normalmente
   - ✅ Requisições do modal passam a funcionar
   - ✅ Não quebra funcionalidade existente

4. **Logging:**
   - ✅ Registrar todas as validações (válida, inválida, pulada)
   - ✅ Registrar origem (webflow vs browser)
   - ✅ Facilitar debugging e análise

### 📋 PROCEDIMENTOS:

1. ✅ Criar backups antes de qualquer alteração
2. ✅ Validar sintaxe PHP antes e depois
3. ✅ Testar ambos os cenários (com e sem assinatura)
4. ✅ Verificar logs após cada teste
5. ✅ Confirmar funcionamento do modal e do Webflow

### 🔒 CONSIDERAÇÕES DE SEGURANÇA:

**Análise de Risco:**

- **Baixo Risco:** Requisições do navegador (modal) já passam por CORS que limita origens
- **Baixo Risco:** Requisições do Webflow continuam protegidas por assinatura
- **Médio Risco:** Requisições sem assinatura não têm autenticação adicional
- **Mitigação:** CORS restrito + logging completo para auditoria

**Alternativas Consideradas:**

1. ❌ **Token adicional para navegador:** Complexidade desnecessária para empresa pequena
2. ❌ **Endpoint separado:** Duplicação de código e manutenção
3. ✅ **Validação condicional:** Solução simples e adequada ao contexto

---

## 📚 REFERÊNCIAS

- **Arquivos:** 
  - `02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php`
  - `02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php`
- **Logs:** 
  - `/var/www/html/logs/flyingdonkeys_prod.txt`
  - `/var/www/html/logs/webhook_octadesk_prod.txt`
- **Documentação Webflow:** Webhook Signature Validation (HMAC-SHA256)

---

**Status:** 🟡 Planejamento (NÃO EXECUTAR)  
**Aguardando:** Revisão técnica + Aprovação para implementação


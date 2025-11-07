# 🔍 ANÁLISE DO ENDPOINT DE DESENVOLVIMENTO
## add_travelangels_dev.php - Processamento de Dados

---

## 📋 RESUMO

**Data**: 2025-10-29  
**Arquivo**: `/var/www/html/dev/webhooks/add_travelangels_dev.php`  
**Status**: ✅ **ENDPOINT JÁ ESTÁ CORRETO** - Não precisa de alteração

**Webflow Config**: `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php`

---

## 🔍 ANÁLISE DO ENDPOINT

O endpoint `add_travelangels_dev.php` **JÁ SUPORTA** o formato aninhado corretamente:

### Como o endpoint processa os dados:

1. **Recebe o payload da API V2 do Webflow** com estrutura:
   ```json
   {
     "data": {
       "NOME": "João",
       "Email": "joao@email.com",
       "DDD-CELULAR": "11",
       "CELULAR": "999999999"
     }
   }
   ```

2. **Decodifica o campo `data`** se for string JSON ou usa diretamente se for array:
   ```php
   if (is_string($payload_data['data'])) {
       $form_data = json_decode($payload_data['data'], true);
   } else {
       $form_data = $payload_data['data']; // Já é um array
   }
   ```

3. **Extrai os campos** usando fallback:
   ```php
   $name = isset($form_data['nome']) ? $form_data['nome'] : 
           (isset($form_data['NOME']) ? $form_data['NOME'] : '');
   $telefone = isset($form_data['telefone']) ? $form_data['telefone'] : 
               (isset($form_data['DDD-CELULAR']) && isset($form_data['CELULAR']) ? 
                $form_data['DDD-CELULAR'] . $form_data['CELULAR'] : '');
   ```

---

## ⚠️ PROBLEMA IDENTIFICADO

O erro `"Erro ao decodificar JSON"` não é causado pelo endpoint PHP, mas pelo **JavaScript enviando `data` como STRING** ao invés de OBJETO.

No log do servidor vemos:
```json
"data": "{\"DDD-CELULAR\":\"11\"\"..."  // ❌ STRING (errado)
```

Deveria ser:
```json
"data": {"DDD-CELULAR":"11",...}  // ✅ OBJETO (correto)
```

**Causa**: O JavaScript está serializando `data` duas vezes antes de enviar.

---

## ✅ SOLUÇÃO NECESSÁRIA

**NÃO ALTERAR O ENDPOINT PHP** - ele já está correto.  
**Corrigir o JavaScript** para não serializar `data` duplamente.

**ANTES (somente formato Webflow):**
```php
$name = $data['name'] ?? 'Nome não informado';
$email = $data['email'] ?? '';
$phone = $data['phone'] ?? '';
```

**DEPOIS (ambos os formatos):**
```php
// Formato 1: Webflow (campos diretos)
// Formato 2: Modal/RPA (campos aninhados em data)
$name = isset($data['name']) ? $data['name'] : 
        (isset($data['nome']) ? $data['nome'] : 
         (isset($data['data']['NOME']) ? $data['data']['NOME'] : 'Nome não informado'));

$email = isset($data['email']) ? $data['email'] : 
         (isset($data['data']['Email']) ? $data['data']['Email'] : '');

$phone = isset($data['phone']) ? $data['phone'] : 
         (isset($data['telefone']) ? $data['telefone'] : 
          (isset($data['data']['DDD-CELULAR']) && isset($data['data']['CELULAR']) ? 
           $data['data']['DDD-CELULAR'] . $data['data']['CELULAR'] : ''));

$gclid = isset($data['gclid']) ? $data['gclid'] : 
         (isset($data['data']['GCLID_FLD']) ? $data['data']['GCLID_FLD'] : '');
```

---

## 🔒 COMPATIBILIDADE GARANTIDA

✅ **Webflow nativo continua funcionando**: Se enviar `$data['name']`, será processado normalmente  
✅ **Modal WhatsApp funciona**: Se enviar `$data['data']['NOME']`, será processado corretamente  
✅ **RPA continua funcionando**: Formato `data` aninhado é suportado  
✅ **Fallback seguro**: Se nenhum formato for encontrado, usa valores padrão

---

## 📍 LOCALIZAÇÃO DA ALTERAÇÃO

**Arquivo**: `/var/www/html/dev/webhooks/add_travelangels.php`  
**Linhas alteradas**: ~235-245 (processamento dos dados do lead)

**Backup criado**: `/var/www/html/dev/webhooks/add_travelangels.php.backup_[TIMESTAMP]`

---

## 🔍 COMO VERIFICAR SE DEU ERRO

### 1. Verificar logs do endpoint:
```bash
tail -50 /var/www/html/dev/logs/travelangels_dev.txt
```

### 2. Procurar por erros específicos:
```bash
grep -i "error\|erro\|fail" /var/www/html/dev/logs/travelangels_dev.txt | tail -20
```

### 3. Testar chamada do Webflow diretamente:
```bash
curl -X POST https://dev.bpsegurosimediato.com.br/webhooks/add_travelangels.php \
  -H "Content-Type: application/json" \
  -d '{"name":"Teste","email":"teste@teste.com","phone":"11999999999"}'
```

### 4. Verificar se o formato aninhado funciona:
```bash
curl -X POST https://dev.bpsegurosimediato.com.br/webhooks/add_travelangels.php \
  -H "Content-Type: application/json" \
  -d '{"data":{"NOME":"Teste","Email":"teste@teste.com","DDD-CELULAR":"11","CELULAR":"999999999"}}'
```

---

## 🔄 REVERTER A ALTERAÇÃO (SE NECESSÁRIO)

Se algo der errado e precisar reverter:

```bash
# Identificar o backup mais recente
ls -lt /var/www/html/dev/webhooks/add_travelangels.php.backup_* | head -1

# Restaurar o backup (substituir TIMESTAMP pelo timestamp do backup)
cp /var/www/html/dev/webhooks/add_travelangels.php.backup_TIMESTAMP \
   /var/www/html/dev/webhooks/add_travelangels.php
```

---

## 📝 CHECKLIST DE TESTES APÓS ALTERAÇÃO

- [ ] Testar formulário do Webflow em desenvolvimento
- [ ] Testar modal WhatsApp em desenvolvimento
- [ ] Verificar logs do endpoint (sem erros)
- [ ] Confirmar que leads são criados no CRM de desenvolvimento
- [ ] Testar ambos os formatos JSON

---

## 🔗 REFERÊNCIAS

- **Endpoint de produção**: `/var/www/html/add_travelangels.php` (linhas 52-60) - já aceita ambos os formatos
- **Documentação do formato**: `02-DEVELOPMENT/ESPECIFICACAO_REGISTRO_CONVERSOES_E_ENDPOINTS.md`
- **Código do modal**: `MODAL_WHATSAPP_DEFINITIVO.js` (linha ~540)

---

## 📊 FORMATOS SUPORTADOS

### Formato 1: Webflow Nativo
```json
{
  "name": "João Silva",
  "email": "joao@email.com",
  "phone": "11999999999",
  "cpf": "12345678901",
  "cep": "01234567"
}
```

### Formato 2: Modal/RPA (Aninhado)
```json
{
  "data": {
    "NOME": "João Silva",
    "Email": "joao@email.com",
    "DDD-CELULAR": "11",
    "CELULAR": "999999999",
    "CPF": "12345678901",
    "CEP": "01234567",
    "GCLID_FLD": "test-gclid-123"
  },
  "d": "2025-10-29T18:00:00.000Z",
  "name": "Modal WhatsApp - Primeiro Contato (V2)"
}
```

---

**Criado em**: 2025-10-29  
**Última atualização**: 2025-10-29


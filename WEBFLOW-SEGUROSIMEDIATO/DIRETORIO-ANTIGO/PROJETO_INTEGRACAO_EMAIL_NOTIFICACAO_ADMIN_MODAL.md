# PROJETO: INTEGRAÇÃO DE EMAIL NOTIFICAÇÃO ADMINISTRADORES NO MODAL WHATSAPP

**Data de Criação:** 03/11/2025 18:00  
**Status:** Planejamento (NÃO EXECUTAR)  
**Workspace:** imediatoseguros-rpa-playwright

---

## 📋 OBJETIVO

Integrar o envio de email para administradores via Amazon SES no endpoint `add_flyingdonkeys_v2.php`, executando após cada chamada bem-sucedida ao EspoCRM. O sistema deve identificar claramente os dois momentos distintos de chamada:

1. **MOMENTO 1 (INITIAL):** Após digitação do telefone no modal (apenas DDD + Celular)
2. **MOMENTO 2 (UPDATE):** Após submissão completa do formulário no modal (todos os dados)

Cada momento deve ter identificadores visuais únicos (emojis e cores) nos logs e nos emails enviados.

---

## 🎯 PROBLEMA ATUAL

Atualmente, o sistema de notificação por email para administradores (`send_admin_notification_ses.php`) foi criado e testado, mas **não está integrado** ao fluxo do modal WhatsApp. Os emails não são enviados automaticamente quando:

1. Um cliente digita o telefone corretamente no modal
2. Um cliente submete o formulário completo no modal

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos a Modificar:
1. `02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php`
   - Adicionar chamada à função `enviarNotificacaoAdministradores()` após processamento bem-sucedido do lead
   - Identificar qual momento (INITIAL ou UPDATE) está sendo processado
   - Adicionar logs diferenciados com emojis e cores para cada momento

### Arquivos de Referência (NÃO MODIFICAR):
- `02-DEVELOPMENT/custom-codes/send_admin_notification_ses.php` - Função de envio já criada
- `02-DEVELOPMENT/custom-codes/aws_ses_config.php` - Configuração AWS SES já criada
- `MODAL_WHATSAPP_DEFINITIVO.js` - Modal que chama o endpoint (não modificar nesta fase)

### Destino no Servidor:
- `/var/www/html/webhooks/add_flyingdonkeys_v2.php`

---

## 🔍 ANÁLISE DOS DOIS MOMENTOS

### **MOMENTO 1: INITIAL (Primeiro Contato - Apenas Telefone)**

**Quando ocorre:**
- Após o cliente digitar DDD + Celular no modal WhatsApp
- Função JavaScript: `sendToEspoCrmInitial()` no `MODAL_WHATSAPP_DEFINITIVO.js`

**Dados enviados:**
```javascript
{
  data: {
    'DDD-CELULAR': '11',
    'CELULAR': '999999999',
    'GCLID_FLD': '...',
    'NOME': '11-999999999-NOVO CLIENTE WHATSAPP',
    'CPF': '',
    'CEP': '',
    'PLACA': '',
    'Email': '11999999999@imediatoseguros.com.br'
  },
  name: 'Modal WhatsApp - Primeiro Contato (V2)'
}
```

**Identificador no PHP:**
- Campo `name` contém: `'Modal WhatsApp - Primeiro Contato (V2)'`
- Campo `NOME` contém padrão: `'{DDD}-{CELULAR}-NOVO CLIENTE WHATSAPP'`
- Campos `CPF`, `CEP`, `PLACA` estão vazios

**Emoji identificador:** 📞 (telefone azul)
**Cor no log:** 🔵 (azul)

---

### **MOMENTO 2: UPDATE (Submissão Completa - Todos os Dados)**

**Quando ocorre:**
- Após o cliente clicar no botão de submissão do modal
- Todos os campos estão preenchidos (CPF, CEP, PLACA, etc.)
- Função JavaScript: `sendToEspoCrmUpdate()` no `MODAL_WHATSAPP_DEFINITIVO.js`

**Dados enviados:**
```javascript
{
  data: {
    'DDD-CELULAR': '11',
    'CELULAR': '999999999',
    'GCLID_FLD': '...',
    'NOME': 'Nome Completo do Cliente',
    'CPF': '123.456.789-00',
    'CEP': '01234-567',
    'PLACA': 'ABC1234',
    'Email': 'cliente@email.com'
  },
  name: 'Modal WhatsApp - Dados Completos (V2)'
}
```

**Identificador no PHP:**
- Campo `name` contém: `'Modal WhatsApp - Dados Completos (V2)'`
- Campo `NOME` contém nome real do cliente (não o padrão)
- Campos `CPF`, `CEP`, `PLACA` estão preenchidos

**Emoji identificador:** ✅ (check verde)
**Cor no log:** 🟢 (verde)

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DAS ALTERAÇÕES

### **1.1. Adicionar Require do Arquivo de Notificação**

**Localização:** Início do arquivo `add_flyingdonkeys_v2.php` (após includes existentes)

```php
// Carregar função de notificação de administradores
require_once __DIR__ . '/send_admin_notification_ses.php';
```

### **1.2. Criar Função de Identificação do Momento**

**Localização:** Após as funções de logging, antes do processamento principal

```php
/**
 * Identifica em qual momento o modal está sendo processado
 * 
 * @param array $form_data Dados do formulário recebido
 * @return array ['moment' => 'initial'|'update', 'emoji' => string, 'color' => string, 'description' => string]
 */
function identifyModalMoment($form_data) {
    // Verificar pelo campo 'name' do payload (se disponível)
    $name_field = $form_data['name'] ?? '';
    
    // Verificar pelo padrão do nome (INITIAL tem padrão especial)
    $nome_value = $form_data['nome'] ?? $form_data['NOME'] ?? '';
    $is_initial_pattern = preg_match('/^\d{2}-\d{9}-NOVO CLIENTE WHATSAPP$/', $nome_value);
    
    // Verificar se campos obrigatórios estão vazios (INITIAL tem apenas telefone)
    $cpf_vazio = empty($form_data['cpf']) && empty($form_data['CPF']);
    $cep_vazio = empty($form_data['cep']) && empty($form_data['CEP']);
    $placa_vazia = empty($form_data['placa']) && empty($form_data['PLACA']);
    
    // Lógica de identificação
    if (
        (strpos($name_field, 'Primeiro Contato') !== false) ||
        $is_initial_pattern ||
        ($cpf_vazio && $cep_vazio && $placa_vazia)
    ) {
        // MOMENTO 1: INITIAL
        return [
            'moment' => 'initial',
            'emoji' => '📞',
            'color' => '🔵',
            'color_name' => 'AZUL',
            'description' => 'Primeiro Contato - Apenas Telefone',
            'icon' => '📞'
        ];
    } else {
        // MOMENTO 2: UPDATE
        return [
            'moment' => 'update',
            'emoji' => '✅',
            'color' => '🟢',
            'color_name' => 'VERDE',
            'description' => 'Submissão Completa - Todos os Dados',
            'icon' => '✅'
        ];
    }
}
```

### **1.3. Preparar Dados para Email**

**Localização:** Após mapeamento de campos, antes do envio ao EspoCRM

```php
// Identificar momento do modal
$modalMoment = identifyModalMoment($form_data);

// Preparar dados para email (sempre incluir, mesmo se alguns campos estiverem vazios)
$emailData = [
    'ddd' => $form_data['DDD-CELULAR'] ?? '',
    'celular' => $form_data['CELULAR'] ?? '',
    'cpf' => $cpf,
    'nome' => $name,
    'email' => $email,
    'cep' => $cep,
    'placa' => $placa,
    'gclid' => $gclid,
    'momento' => $modalMoment['moment'],
    'momento_descricao' => $modalMoment['description'],
    'momento_emoji' => $modalMoment['emoji']
];
```

### **1.4. Enviar Email Após Sucesso no EspoCRM**

**Localização:** Após criação/atualização bem-sucedida do lead (linha ~835 e ~876)

**Após criação bem-sucedida do lead (linha ~835):**
```php
// ✅ LOG: Lead criado com sucesso
logDevWebhook('flyingdonkeys_lead_created', ['lead_id' => $leadIdFlyingDonkeys], true);

// 📧 ENVIAR EMAIL PARA ADMINISTRADORES
try {
    $emailResult = enviarNotificacaoAdministradores($emailData);
    
    // Log diferenciado por momento
    if ($modalMoment['moment'] === 'initial') {
        logProdWebhook('email_notification_initial_sent', [
            'moment' => $modalMoment['moment'],
            'emoji' => $modalMoment['emoji'],
            'color' => $modalMoment['color'],
            'description' => $modalMoment['description'],
            'lead_id' => $leadIdFlyingDonkeys,
            'email_result' => $emailResult,
            'recipients' => count(ADMIN_EMAILS)
        ], $emailResult['success']);
        
        error_log(sprintf(
            "%s [EMAIL-%s] %s Notificação INITIAL enviada - Lead: %s - Sucesso: %s",
            $modalMoment['emoji'],
            $modalMoment['color_name'],
            $modalMoment['description'],
            $leadIdFlyingDonkeys,
            $emailResult['success'] ? 'SIM' : 'NÃO'
        ));
    } else {
        logProdWebhook('email_notification_update_sent', [
            'moment' => $modalMoment['moment'],
            'emoji' => $modalMoment['emoji'],
            'color' => $modalMoment['color'],
            'description' => $modalMoment['description'],
            'lead_id' => $leadIdFlyingDonkeys,
            'email_result' => $emailResult,
            'recipients' => count(ADMIN_EMAILS)
        ], $emailResult['success']);
        
        error_log(sprintf(
            "%s [EMAIL-%s] %s Notificação UPDATE enviada - Lead: %s - Sucesso: %s",
            $modalMoment['emoji'],
            $modalMoment['color_name'],
            $modalMoment['description'],
            $leadIdFlyingDonkeys,
            $emailResult['success'] ? 'SIM' : 'NÃO'
        ));
    }
    
    if (!$emailResult['success']) {
        logProdWebhook('email_notification_failed', [
            'error' => $emailResult['error'] ?? 'Erro desconhecido',
            'lead_id' => $leadIdFlyingDonkeys,
            'moment' => $modalMoment['moment']
        ], false);
    }
} catch (Exception $emailException) {
    // Não bloquear o fluxo principal em caso de erro no email
    logProdWebhook('email_notification_exception', [
        'error' => $emailException->getMessage(),
        'lead_id' => $leadIdFlyingDonkeys,
        'moment' => $modalMoment['moment']
    ], false);
    
    error_log(sprintf(
        "⚠️ [EMAIL-ERRO] Falha ao enviar notificação - Lead: %s - Erro: %s",
        $leadIdFlyingDonkeys,
        $emailException->getMessage()
    ));
}
```

**Após atualização bem-sucedida do lead (linha ~876, quando lead existe):**
```php
// Aplicar a mesma lógica acima após atualização do lead existente
```

### **1.5. Atualizar Função de Envio de Email para Incluir Identificadores Visuais**

**Modificar:** `send_admin_notification_ses.php` (apenas o conteúdo do email)

**Adicionar no assunto do email:**
```php
// No início da função enviarNotificacaoAdministradores()
$momento_emoji = $dados['momento_emoji'] ?? '📧';
$momento_descricao = $dados['momento_descricao'] ?? 'Notificação';

// No assunto:
$subject = sprintf(
    '%s %s - Modal WhatsApp - %s',
    $momento_emoji,
    $momento_descricao,
    $telefoneCompleto
);
```

**Adicionar seção visual no corpo do email (HTML):**
```php
// Adicionar banner colorido no topo do email HTML
$bannerColor = ($dados['momento'] ?? 'initial') === 'initial' ? '#2196F3' : '#4CAF50'; // Azul ou Verde
$bannerEmoji = $dados['momento_emoji'] ?? '📧';
$bannerText = $dados['momento_descricao'] ?? 'Notificação';

// No HTML body, após .header:
<div class="banner" style="background-color: ' . $bannerColor . '; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 16px; margin-bottom: 20px;">
    ' . $bannerEmoji . ' ' . $bannerText . '
</div>
```

---

## 📝 LOGS ESPERADOS

### **Momento 1 (INITIAL):**
```
📞 [EMAIL-AZUL] Primeiro Contato - Apenas Telefone Notificação INITIAL enviada - Lead: 69039ffd9055284be - Sucesso: SIM
```

### **Momento 2 (UPDATE):**
```
✅ [EMAIL-VERDE] Submissão Completa - Todos os Dados Notificação UPDATE enviada - Lead: 69039ffd9055284be - Sucesso: SIM
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [ ] 1. Criar backup de `add_flyingdonkeys_v2.php`
- [ ] 2. Adicionar `require_once` para `send_admin_notification_ses.php`
- [ ] 3. Criar função `identifyModalMoment()`
- [ ] 4. Preparar array `$emailData` com dados completos
- [ ] 5. Adicionar chamada de email após criação bem-sucedida do lead
- [ ] 6. Adicionar chamada de email após atualização bem-sucedida do lead
- [ ] 7. Adicionar logs diferenciados com emojis e cores
- [ ] 8. Atualizar função de email para incluir identificadores visuais
- [ ] 9. Testar com dados INITIAL (apenas telefone)
- [ ] 10. Testar com dados UPDATE (todos os dados)
- [ ] 11. Verificar logs no servidor
- [ ] 12. Verificar recebimento de emails pelos 3 administradores

---

## 🔄 ROLLBACK

Em caso de problemas, reverter alterações:

1. Restaurar backup de `add_flyingdonkeys_v2.php`
2. Verificar se emails pararam de ser enviados
3. Verificar logs para garantir que não há erros

---

## ⚠️ OBSERVAÇÕES IMPORTANTES

1. **Não bloquear fluxo principal:** Em caso de erro no envio de email, o processo principal (criação do lead) deve continuar normalmente
2. **Logs diferenciados:** Cada momento deve ter logs claramente identificáveis
3. **Emails visuais:** Cada email deve ter identificação visual clara (cor e emoji) no assunto e corpo
4. **Performance:** O envio de email é assíncrono e não deve impactar o tempo de resposta do webhook
5. **Administradores:** 3 emails configurados:
   - `lrotero@gmail.com`
   - `alex.kaminski@imediatoseguros.com.br`
   - `alexkaminski70@gmail.com`

---

## 📊 TESTES

### **Teste 1: Momento INITIAL**
1. Abrir modal WhatsApp
2. Digitar apenas DDD + Celular
3. Verificar log: `📞 [EMAIL-AZUL]`
4. Verificar email recebido com banner azul e emoji 📞
5. Verificar que campos CPF, CEP, PLACA aparecem como "Não informado"

### **Teste 2: Momento UPDATE**
1. Com lead já criado no passo anterior
2. Preencher todos os campos no modal
3. Clicar em enviar
4. Verificar log: `✅ [EMAIL-VERDE]`
5. Verificar email recebido com banner verde e emoji ✅
6. Verificar que todos os campos aparecem preenchidos

---

## 🔍 REVISÃO TÉCNICA

**Status:** ⏳ Aguardando revisão do Engenheiro de Software

**Comentários do Engenheiro:**
_[Aguardando comentários]_

---

**Próximos Passos:**
1. Aguardar aprovação do projeto
2. Criar backups
3. Implementar alterações conforme checklist
4. Testar em ambiente de desenvolvimento
5. Deploy para produção após validação



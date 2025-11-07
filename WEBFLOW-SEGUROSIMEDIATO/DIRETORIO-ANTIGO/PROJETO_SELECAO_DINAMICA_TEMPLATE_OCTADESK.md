# PROJETO: SELEÇÃO DINÂMICA DE TEMPLATE OCTADESK

**Data de Criação:** 02/11/2025 14:45  
**Status:** Planejamento (NÃO EXECUTAR)  
**Workspace:** imediatoseguros-rpa-playwright

---

## 📋 OBJETIVO

Implementar seleção dinâmica do template de mensagem WhatsApp que será enviado ao cliente através da API do OctaDesk, permitindo escolher diferentes templates baseado em regras de negócio, dados do formulário ou campanhas de marketing.

---

## 🎯 PROBLEMA ATUAL

O código atual no arquivo `add_webflow_octa_v2.php` utiliza um template fixo (`site_cotacao`) hardcoded na linha 207:

```php
'templateMessage' => [
    'code' => 'site_cotacao',  // ⚠️ HARDCODED - Não permite escolha dinâmica
    ...
]
```

**Limitações:**
- Todos os clientes recebem a mesma mensagem
- Não é possível personalizar mensagens por tipo de produto
- Não é possível usar templates promocionais baseados em campanhas
- Impossível A/B testing de mensagens

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos a Modificar:
1. `02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php`
   - Função `sendToOctaDesk()` - implementar lógica de seleção dinâmica
   - Adicionar validação de templates permitidos
   - Adicionar mapeamento de componentes por template

### Backups a Criar:
- ✅ `add_webflow_octa_v2.php.backup_20251102_144500` (será criado antes da implementação)

### Destino no Servidor:
- `/var/www/html/webhooks/add_webflow_octa_v2.php`

### Arquivos de Documentação:
- `02-DEVELOPMENT/ANALISE_OCTADESK_TEMPLATE_SELECAO.md` (análise técnica já realizada)

---

## 🔍 ANÁLISE TÉCNICA REALIZADA

**Conclusão:** ✅ **SIM, É POSSÍVEL ESCOLHER O TEMPLATE DINAMICAMENTE**

O campo `code` no payload `templateMessage` pode receber qualquer string que corresponda a um template aprovado no WhatsApp Business da conta OctaDesk.

**Documentação completa:** Ver `02-DEVELOPMENT/ANALISE_OCTADESK_TEMPLATE_SELECAO.md`

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DAS ALTERAÇÕES

### 1.1. Criar Função de Seleção de Template

Implementar função que escolhe o template baseado em:
- Campo do formulário (se fornecido)
- Tipo de produto
- UTM Campaign
- Origem/landing page

```php
function selectTemplateCode($data) {
    // 1. Verificar se há campo específico no formulário
    $templateFromForm = $data['custom_fields']['template_code'] ?? null;
    
    // 2. Lista de templates permitidos (validação de segurança)
    $allowedTemplates = [
        'site_cotacao',
        'site_cotacao_residencial',
        'site_cotacao_vida',
        'site_cotacao_promocional',
        'site_cotacao_natal',
        'site_cotacao_blackfriday'
    ];
    
    // 3. Validar template do formulário
    if ($templateFromForm && in_array($templateFromForm, $allowedTemplates)) {
        return $templateFromForm;
    }
    
    // 4. Regra de negócio: baseado em produto
    $produto = $data['custom_fields']['produto'] ?? '';
    if ($produto === 'seguro-residencial') {
        return 'site_cotacao_residencial';
    } else if ($produto === 'seguro-vida') {
        return 'site_cotacao_vida';
    }
    
    // 5. Regra de negócio: baseado em campanha
    $utmCampaign = $data['custom_fields']['utm_campaign'] ?? '';
    if ($utmCampaign === 'promocao_natal') {
        return 'site_cotacao_natal';
    } else if ($utmCampaign === 'black_friday') {
        return 'site_cotacao_blackfriday';
    }
    
    // 6. Default
    return 'site_cotacao';
}
```

### 1.2. Criar Função de Mapeamento de Componentes

Cada template pode ter estrutura diferente de componentes:

```php
function getTemplateComponents($templateCode, $data) {
    $nome = $data['name'] ?? 'cliente';
    $produto = $data['custom_fields']['produto'] ?? 'seguro-auto';
    
    switch ($templateCode) {
        case 'site_cotacao':
            // Template padrão - apenas nome
            return [[
                'type' => 'body',
                'parameters' => [[
                    'type' => 'text',
                    'text' => $nome
                ]]
            ]];
            
        case 'site_cotacao_promocional':
            // Template promocional - nome + produto
            return [[
                'type' => 'body',
                'parameters' => [
                    ['type' => 'text', 'text' => $nome],
                    ['type' => 'text', 'text' => $produto]
                ]
            ]];
            
        case 'site_cotacao_residencial':
        case 'site_cotacao_vida':
        case 'site_cotacao_natal':
        case 'site_cotacao_blackfriday':
            // Outros templates - seguir estrutura padrão
            return [[
                'type' => 'body',
                'parameters' => [[
                    'type' => 'text',
                    'text' => $nome
                ]]
            ]];
            
        default:
            // Fallback - sempre retornar estrutura básica
            return [[
                'type' => 'body',
                'parameters' => [[
                    'type' => 'text',
                    'text' => $nome
                ]]
            ]];
    }
}
```

### 1.3. Modificar Função `sendToOctaDesk()`

Atualizar a função para usar seleção dinâmica:

```php
function sendToOctaDesk($data)
{
    // ... código de validação de telefone existente ...
    
    // ✅ NOVO: Seleção dinâmica do template
    $templateCode = selectTemplateCode($data);
    $components = getTemplateComponents($templateCode, $data);
    
    // Log da seleção do template
    logProdWebhook('template_selected', [
        'template_code' => $templateCode,
        'selection_reason' => 'baseado_em_regras',
        'components_count' => count($components)
    ], true);
    
    // Preparar payload do send-template
    $payloadSend = [
        'target' => [
            // ... código existente ...
        ],
        'content' => [
            'templateMessage' => [
                'code' => $templateCode,  // ✅ DINÂMICO
                'language' => 'pt_BR',
                'components' => $components  // ✅ DINÂMICO
            ]
        ],
        // ... resto do payload existente ...
    ];
    
    // ... código de envio existente ...
}
```

---

## 📤 FASE 2: CÓPIA DOS ARQUIVOS PARA O SERVIDOR

### 2.1. Criar Backup Local
```bash
# Copiar arquivo atual como backup
cp 02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php \
   02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php.backup_20251102_144500
```

### 2.2. Validar Sintaxe PHP
```bash
php -l 02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php
```

### 2.3. Copiar para Servidor
```bash
scp 02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php \
   root@46.62.174.150:/var/www/html/webhooks/add_webflow_octa_v2.php
```

### 2.4. Validar no Servidor
```bash
ssh root@46.62.174.150 "php -l /var/www/html/webhooks/add_webflow_octa_v2.php"
```

---

## 🧪 FASE 3: TESTE E VERIFICAÇÃO

### 3.1. Testes Necessários

#### Teste 1: Template Padrão (Fallback)
- Submeter formulário sem campos especiais
- **Esperado:** Usar template `site_cotacao`
- **Verificar logs:** `template_selected` com `template_code: site_cotacao`

#### Teste 2: Template por Produto
- Submeter formulário com `produto: seguro-residencial`
- **Esperado:** Usar template `site_cotacao_residencial`
- **Verificar logs:** `template_selected` com `template_code: site_cotacao_residencial`

#### Teste 3: Template por Campanha
- Submeter formulário com `utm_campaign: promocao_natal`
- **Esperado:** Usar template `site_cotacao_natal`
- **Verificar logs:** `template_selected` com `template_code: site_cotacao_natal`

#### Teste 4: Template Explícito no Formulário
- Submeter formulário com campo `TEMPLATE_CODE: site_cotacao_promocional`
- **Esperado:** Usar template `site_cotacao_promocional`
- **Verificar logs:** `template_selected` com `template_code: site_cotacao_promocional`

#### Teste 5: Template Inválido (Segurança)
- Submeter formulário com `TEMPLATE_CODE: template_malicioso`
- **Esperado:** Fallback para `site_cotacao` (template inválido ignorado)
- **Verificar logs:** Template rejeitado e fallback aplicado

### 3.2. Verificação de Logs

Comando para verificar logs:
```bash
ssh root@46.62.174.150 "grep 'template_selected' /var/www/html/logs/webhook_octadesk_prod.txt | tail -10"
```

### 3.3. Verificação no OctaDesk

- Confirmar que mensagem foi enviada com template correto
- Verificar que componentes foram aplicados corretamente
- Validar que conversa foi criada

---

## ✅ CHECKLIST DE VERIFICAÇÃO

- [ ] Backup criado localmente
- [ ] Função `selectTemplateCode()` implementada
- [ ] Função `getTemplateComponents()` implementada
- [ ] Função `sendToOctaDesk()` modificada
- [ ] Logging de template selecionado adicionado
- [ ] Validação de templates permitidos implementada
- [ ] Sintaxe PHP validada localmente
- [ ] Arquivo copiado para servidor
- [ ] Sintaxe PHP validada no servidor
- [ ] Teste 1: Template padrão (fallback)
- [ ] Teste 2: Template por produto
- [ ] Teste 3: Template por campanha
- [ ] Teste 4: Template explícito
- [ ] Teste 5: Template inválido (segurança)
- [ ] Logs verificados
- [ ] Mensagem verificada no OctaDesk
- [ ] Documentação atualizada

---

## 🔄 ROLLBACK (Se Necessário)

### Procedimento de Reversão:

1. **Restaurar Backup:**
```bash
scp 02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php.backup_20251102_144500 \
   root@46.62.174.150:/var/www/html/webhooks/add_webflow_octa_v2.php
```

2. **Validar no Servidor:**
```bash
ssh root@46.62.174.150 "php -l /var/www/html/webhooks/add_webflow_octa_v2.php"
```

3. **Verificar Logs:**
```bash
ssh root@46.62.174.150 "tail -20 /var/www/html/logs/webhook_octadesk_prod.txt"
```

---

## 📊 CRONOGRAMA

1. **Fase 1 - Implementação:** ~1 hora
   - Criar funções de seleção e mapeamento
   - Modificar função `sendToOctaDesk()`
   - Adicionar logging

2. **Fase 2 - Deploy:** ~15 minutos
   - Criar backup
   - Validar sintaxe
   - Copiar para servidor

3. **Fase 3 - Testes:** ~1 hora
   - Executar todos os testes
   - Verificar logs
   - Validar no OctaDesk

**Total Estimado:** ~2h15min

---

## 🎯 RESULTADO ESPERADO

Após implementação:
- ✅ Sistema pode escolher template dinamicamente
- ✅ Suporte a múltiplos templates baseados em regras de negócio
- ✅ Validação de segurança contra templates inválidos
- ✅ Logging completo de qual template foi usado
- ✅ Fallback automático para template padrão
- ✅ Facilita A/B testing de mensagens
- ✅ Permite personalização por campanha/produto

---

## ⚠️ REQUISITOS PRÉVIOS

### Templates no WhatsApp Business

**ATENÇÃO:** Antes de implementar, garantir que os seguintes templates estão criados e aprovados no WhatsApp Business da conta OctaDesk:

- [ ] `site_cotacao` (já existe e está funcionando)
- [ ] `site_cotacao_residencial` (a criar)
- [ ] `site_cotacao_vida` (a criar)
- [ ] `site_cotacao_promocional` (a criar)
- [ ] `site_cotacao_natal` (a criar - se necessário)
- [ ] `site_cotacao_blackfriday` (a criar - se necessário)

**Cada template deve:**
- Estar aprovado no WhatsApp Business
- Estar disponível em `pt_BR`
- Ter estrutura de componentes documentada
- Ser testado antes de uso em produção

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

1. **Validação de Templates:**
   - SEMPRE validar contra lista de templates permitidos
   - NUNCA confiar em valores vindos do formulário sem validação
   - SEMPRE ter fallback para template padrão

2. **Componentes por Template:**
   - Cada template pode ter estrutura diferente de componentes
   - Necessário mapear todos os templates antes de usar
   - Testar componentes antes de produção

3. **Templates no WhatsApp Business:**
   - Templates devem estar aprovados ANTES de usar
   - Código do template deve corresponder exatamente
   - Idioma deve estar correto (`pt_BR`)

4. **Logging:**
   - Registrar qual template foi usado para cada envio
   - Facilitar debugging e análise
   - Permitir auditoria de uso

### 📋 PROCEDIMENTOS:

1. ✅ Consultar `ANALISE_OCTADESK_TEMPLATE_SELECAO.md` para detalhes técnicos
2. ⚠️ Garantir que templates estão aprovados no WhatsApp Business
3. ⚠️ Mapear estrutura de componentes de cada template
4. ⚠️ Testar cada template antes de produção
5. ⚠️ Implementar validação rigorosa
6. ⚠️ Manter fallback sempre funcional

---

## 📚 REFERÊNCIAS

- **Análise Técnica:** `02-DEVELOPMENT/ANALISE_OCTADESK_TEMPLATE_SELECAO.md`
- **Código Atual:** `02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php`
- **Logs:** `/var/www/html/logs/webhook_octadesk_prod.txt`
- **Documentação OctaDesk:** API REST - endpoint `/chat/conversation/send-template`

---

**Status:** Planejamento (NÃO EXECUTAR)  
**Aguardando:** Revisão técnica + Aprovação para implementação




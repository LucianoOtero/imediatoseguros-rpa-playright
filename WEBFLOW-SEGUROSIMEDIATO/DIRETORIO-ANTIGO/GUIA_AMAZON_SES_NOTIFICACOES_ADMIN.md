# 📧 GUIA COMPLETO - AMAZON SES PARA NOTIFICAÇÕES INTERNAS

**Data de Criação:** 03/11/2025  
**Objetivo:** Enviar notificações para administradores quando cliente preenche telefone no `MODAL_WHATSAPP_DEFINITIVO`  
**Volume Estimado:** < 1000 emails/mês

---

## 🎯 O QUE É AMAZON SES?

**Amazon SES (Simple Email Service)** é um serviço de envio de emails transacionais gerenciado pela AWS que:
- ✅ Envia emails através de servidores da Amazon (alta confiabilidade)
- ✅ Não precisa configurar servidor SMTP próprio
- ✅ Integração via API REST simples
- ✅ **GRÁTIS até 62.000 emails/mês** (se usado de servidor EC2 na região gratuita)
- ✅ Escalável automaticamente
- ✅ Excelente reputação (menor chance de ir para spam)

---

## 💰 CUSTOS

### **Região Gratuita (AWS Free Tier):**
- **62.000 emails/mês GRÁTIS** se enviado de servidor EC2 na mesma região
- **1.000 emails/mês GRÁTIS** se enviado de fora do EC2

### **Após o Limite:**
- **$0.10 por 1.000 emails** (aproximadamente R$ 0,50 por 1.000 emails)
- **Exemplo:** 1.000 emails/mês = R$ 0/mês (dentro do limite gratuito)
- **Exemplo:** 5.000 emails/mês = R$ 0/mês (ainda grátis até 62.000)

### **Para seu caso (< 1000 emails/mês):**
- ✅ **CUSTO: R$ 0/mês** (dentro do limite gratuito)

---

## 🏗️ COMO FUNCIONA (ARQUITETURA)

```
┌─────────────────────────────────────────────────┐
│   MODAL_WHATSAPP_DEFINITIVO                    │
│   (Cliente preenche telefone)                  │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│   Webhook PHP (add_flyingdonkeys_v2.php)        │
│   - Valida telefone                             │
│   - Prepara dados                               │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│   Função PHP de Envio                           │
│   - Usa AWS SDK para PHP                        │
│   - Chama API do Amazon SES                     │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│   Amazon SES (Servidor AWS)                     │
│   - Autentica email                             │
│   - Processa e envia                            │
│   - Gerencia bounces/spam                       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│   Email dos Administradores                     │
│   (Gmail, Outlook, etc.)                        │
└─────────────────────────────────────────────────┘
```

---

## 🔑 CONCEITOS PRINCIPAIS

### **1. Identidade Verificada (Verified Identity)**
Antes de enviar, você precisa **verificar** que possui o domínio ou email:
- **Domínio verificado:** Permite enviar de qualquer email @seu-dominio.com.br
- **Email verificado:** Permite enviar apenas daquele email específico

**Para seu caso:** Verificar domínio `bpsegurosimediato.com.br`

### **2. Configuração DNS (SPF/DKIM)**
Amazon SES **gera automaticamente** os registros DNS necessários:
- SPF record
- DKIM records (chaves públicas)
- Você apenas **copia e cola** no seu DNS

**Vantagem:** Não precisa gerar chaves manualmente

### **3. Sandbox Mode (Modo de Teste)**
Por padrão, SES inicia em **Sandbox Mode**:
- ⚠️ Só pode enviar para emails **verificados** (apenas para teste)
- Para enviar para qualquer email, precisa **solicitar saída do Sandbox**
- Processo simples: Solicitar via console AWS → Aprovação em 24-48h

### **4. APIs de Envio**
Amazon SES oferece 3 formas de envio:
- **API REST:** Chamadas HTTP diretas
- **SMTP:** Servidor SMTP tradicional
- **AWS SDK:** SDKs para PHP, Python, Node.js, etc.

**Recomendação:** Usar **AWS SDK para PHP** (mais simples e seguro)

---

## 📋 PASSO A PASSO - IMPLEMENTAÇÃO

### **FASE 1: Configuração AWS (30 minutos)**

#### **1.1. Criar Conta AWS**
1. Acessar: https://aws.amazon.com
2. Criar conta (requer cartão de crédito, mas **não cobra** se usar apenas SES dentro do limite gratuito)
3. Completar verificação de conta

#### **1.2. Acessar Console SES**
1. Ir para: https://console.aws.amazon.com/ses
2. Selecionar região: **us-east-1** (N. Virginia) ou **sa-east-1** (São Paulo)
   - ⚠️ **Importante:** Usar sempre a mesma região depois

#### **1.3. Verificar Domínio**
1. No console SES → **Verified identities** → **Create identity**
2. Selecionar **Domain**
3. Digitar: `bpsegurosimediato.com.br`
4. Clicar **Create identity**

#### **1.4. Configurar DNS**
SES vai gerar registros DNS automaticamente:

**Registros a adicionar no DNS:**
```
Tipo: TXT
Nome: _amazonses.bpsegurosimediato.com.br
Valor: [Valor gerado pelo SES - copiar do console]

Tipo: CNAME
Nome: [DKIM Selector 1]._domainkey.bpsegurosimediato.com.br
Valor: [Valor gerado pelo SES - copiar do console]

Tipo: CNAME
Nome: [DKIM Selector 2]._domainkey.bpsegurosimediato.com.br
Valor: [Valor gerado pelo SES - copiar do console]
```

**Como adicionar:**
1. Acessar painel DNS do seu domínio (onde está hospedado)
2. Adicionar cada registro TXT/CNAME
3. Aguardar propagação (5 minutos a 48 horas)

#### **1.5. Verificar Status**
1. Voltar ao console SES
2. Aguardar status mudar para **Verified** (pode levar até 72h, geralmente < 1h)

#### **1.6. Solicitar Saída do Sandbox (Opcional)**
Se quiser enviar para qualquer email (não apenas verificados):

1. No console SES → **Account dashboard**
2. Clicar **Request production access**
3. Preencher formulário:
   - **Mail Type:** Transactional
   - **Website URL:** https://bpsegurosimediato.com.br
   - **Use case:** Notificações internas para administradores quando cliente preenche formulário
   - **Expected sending rate:** < 100 emails/dia
4. Submeter
5. Aguardar aprovação (geralmente 24-48h)

**Alternativa:** Enquanto aguarda aprovação, pode verificar emails dos administradores temporariamente.

---

### **FASE 2: Criar Credenciais AWS (10 minutos)**

#### **2.1. Criar Usuário IAM**
1. Acessar: https://console.aws.amazon.com/iam
2. **Users** → **Create user**
3. Nome: `ses-email-sender`
4. **Não marcar** "Provide user access to the AWS Management Console"
5. Clicar **Next**

#### **2.2. Atribuir Permissões**
1. Selecionar **Attach policies directly**
2. Pesquisar e selecionar: **AmazonSESFullAccess** (ou criar política customizada mais restritiva)
3. Clicar **Next** → **Create user**

#### **2.3. Obter Credenciais**
1. Clicar no usuário criado
2. Ir na aba **Security credentials**
3. **Create access key**
4. Tipo: **Application running outside AWS**
5. Copiar:
   - **Access Key ID** (exemplo: `AKIAIOSFODNN7EXAMPLE`)
   - **Secret Access Key** (exemplo: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)
   - ⚠️ **IMPORTANTE:** Salvar Secret Access Key agora (não será mostrada novamente)

**Armazenar em local seguro:**
- ⚠️ **NÃO** commitar no GitHub
- Usar variáveis de ambiente ou arquivo de configuração seguro
- Restringir acesso ao arquivo (chmod 600)

---

### **FASE 3: Instalar AWS SDK para PHP (15 minutos)**

#### **3.1. No Servidor (via SSH)**

```bash
# Navegar para diretório do projeto
cd /var/www/html/dev/webhooks

# Instalar AWS SDK via Composer
composer require aws/aws-sdk-php
```

**Se não tiver Composer:**
```bash
# Instalar Composer
curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer
```

#### **3.2. Verificar Instalação**
```bash
php -r "require 'vendor/autoload.php'; echo 'AWS SDK instalado!';"
```

---

### **FASE 4: Criar Função PHP de Envio (30 minutos)**

#### **4.1. Criar Arquivo: `send_admin_notification.php`**

```php
<?php
/**
 * PROJETO: NOTIFICAÇÃO EMAIL ADMINISTRADORES VIA AMAZON SES
 * INÍCIO: 03/11/2025
 * 
 * VERSÃO: 1.0 - Implementação inicial
 * 
 * Função para enviar notificações para administradores
 * quando cliente preenche telefone no MODAL_WHATSAPP_DEFINITIVO
 */

require 'vendor/autoload.php';

use Aws\Ses\SesClient;
use Aws\Exception\AwsException;

// ======================
// CONFIGURAÇÃO
// ======================

// Credenciais AWS (obter do IAM)
define('AWS_ACCESS_KEY_ID', 'SUA_ACCESS_KEY_ID_AQUI');
define('AWS_SECRET_ACCESS_KEY', 'SUA_SECRET_ACCESS_KEY_AQUI');
define('AWS_REGION', 'sa-east-1'); // ou 'us-east-1'

// Email remetente (deve ser do domínio verificado)
define('EMAIL_FROM', 'noreply@bpsegurosimediato.com.br');
define('EMAIL_FROM_NAME', 'BP Seguros Imediato');

// Emails dos administradores (destinatários)
define('ADMIN_EMAILS', [
    'admin1@bpsegurosimediato.com.br',
    'admin2@bpsegurosimediato.com.br',
    // Adicionar mais emails conforme necessário
]);

// ======================
// FUNÇÃO PRINCIPAL
// ======================

/**
 * Envia notificação para administradores
 * 
 * @param array $dados Dados do cliente (DDD, celular, CPF, nome, etc.)
 * @return array Resultado do envio ['success' => bool, 'message_id' => string|null, 'error' => string|null]
 */
function enviarNotificacaoAdministradores($dados) {
    try {
        // Criar cliente SES
        $sesClient = new SesClient([
            'version' => 'latest',
            'region'  => AWS_REGION,
            'credentials' => [
                'key'    => AWS_ACCESS_KEY_ID,
                'secret' => AWS_SECRET_ACCESS_KEY,
            ],
        ]);

        // Preparar dados para email
        $ddd = $dados['ddd'] ?? '';
        $celular = $dados['celular'] ?? '';
        $telefoneCompleto = '(' . $ddd . ') ' . $celular;
        
        $cpf = $dados['cpf'] ?? 'Não informado';
        $nome = $dados['nome'] ?? 'Não informado';
        $emailCliente = $dados['email'] ?? 'Não informado';
        $cep = $dados['cep'] ?? 'Não informado';
        $placa = $dados['placa'] ?? 'Não informado';
        $gclid = $dados['gclid'] ?? 'Não informado';

        // Assunto do email
        $subject = '🔔 Novo contato via Modal WhatsApp - ' . $telefoneCompleto;

        // Corpo do email (HTML)
        $htmlBody = '
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #4CAF50; color: white; padding: 15px; text-align: center; border-radius: 5px 5px 0 0; }
                .content { background-color: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; }
                .field { margin: 10px 0; padding: 10px; background-color: white; border-left: 3px solid #4CAF50; }
                .label { font-weight: bold; color: #666; }
                .value { color: #333; }
                .footer { margin-top: 20px; padding: 15px; text-align: center; color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>📱 Novo Contato - Modal WhatsApp</h2>
                </div>
                <div class="content">
                    <p>Um cliente preencheu o telefone corretamente no modal WhatsApp.</p>
                    
                    <div class="field">
                        <span class="label">📞 Telefone:</span>
                        <span class="value">' . htmlspecialchars($telefoneCompleto) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">👤 Nome:</span>
                        <span class="value">' . htmlspecialchars($nome) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">🆔 CPF:</span>
                        <span class="value">' . htmlspecialchars($cpf) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">📧 Email:</span>
                        <span class="value">' . htmlspecialchars($emailCliente) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">📍 CEP:</span>
                        <span class="value">' . htmlspecialchars($cep) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">🚗 Placa:</span>
                        <span class="value">' . htmlspecialchars($placa) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">🔗 GCLID:</span>
                        <span class="value">' . htmlspecialchars($gclid) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">🕐 Data/Hora:</span>
                        <span class="value">' . date('d/m/Y H:i:s') . '</span>
                    </div>
                </div>
                <div class="footer">
                    <p>Esta é uma notificação automática do sistema BP Seguros Imediato.</p>
                    <p>Não responda este email.</p>
                </div>
            </div>
        </body>
        </html>
        ';

        // Corpo do email (texto simples - fallback)
        $textBody = "
Novo Contato - Modal WhatsApp
============================

Um cliente preencheu o telefone corretamente no modal WhatsApp.

Telefone: {$telefoneCompleto}
Nome: {$nome}
CPF: {$cpf}
Email: {$emailCliente}
CEP: {$cep}
Placa: {$placa}
GCLID: {$gclid}
Data/Hora: " . date('d/m/Y H:i:s') . "
        ";

        // Enviar para cada administrador
        $results = [];
        
        foreach (ADMIN_EMAILS as $adminEmail) {
            try {
                $result = $sesClient->sendEmail([
                    'Source' => EMAIL_FROM_NAME . ' <' . EMAIL_FROM . '>',
                    'Destination' => [
                        'ToAddresses' => [$adminEmail],
                    ],
                    'Message' => [
                        'Subject' => [
                            'Data' => $subject,
                            'Charset' => 'UTF-8',
                        ],
                        'Body' => [
                            'Html' => [
                                'Data' => $htmlBody,
                                'Charset' => 'UTF-8',
                            ],
                            'Text' => [
                                'Data' => $textBody,
                                'Charset' => 'UTF-8',
                            ],
                        ],
                    ],
                    // Tags para identificação (opcional, útil para métricas)
                    'Tags' => [
                        [
                            'Name' => 'source',
                            'Value' => 'modal-whatsapp',
                        ],
                        [
                            'Name' => 'type',
                            'Value' => 'admin-notification',
                        ],
                    ],
                ]);

                $results[] = [
                    'email' => $adminEmail,
                    'success' => true,
                    'message_id' => $result['MessageId'],
                ];
                
            } catch (AwsException $e) {
                $results[] = [
                    'email' => $adminEmail,
                    'success' => false,
                    'error' => $e->getAwsErrorMessage(),
                ];
            }
        }

        // Verificar se pelo menos um email foi enviado
        $successCount = count(array_filter($results, fn($r) => $r['success']));
        
        return [
            'success' => $successCount > 0,
            'total_sent' => $successCount,
            'total_failed' => count($results) - $successCount,
            'results' => $results,
        ];

    } catch (AwsException $e) {
        return [
            'success' => false,
            'error' => $e->getAwsErrorMessage(),
            'code' => $e->getAwsErrorCode(),
        ];
    } catch (Exception $e) {
        return [
            'success' => false,
            'error' => $e->getMessage(),
        ];
    }
}

// ======================
// EXEMPLO DE USO
// ======================

/*
// Exemplo de uso no webhook
$dados = [
    'ddd' => '11',
    'celular' => '987654321',
    'cpf' => '123.456.789-00',
    'nome' => 'João Silva',
    'email' => 'joao@email.com',
    'cep' => '01234-567',
    'placa' => 'ABC1234',
    'gclid' => 'gclid123456',
];

$resultado = enviarNotificacaoAdministradores($dados);

if ($resultado['success']) {
    echo "Email enviado com sucesso!";
} else {
    echo "Erro ao enviar email: " . $resultado['error'];
}
*/
```

#### **4.2. Integrar no Webhook Existente**

Adicionar no arquivo `add_flyingdonkeys_v2.php` ou criar função separada:

```php
// No início do arquivo, após validação do telefone
require_once 'send_admin_notification.php';

// Após processamento bem-sucedido
if ($telefone_validado && $lead_criado) {
    // Enviar notificação para administradores (assíncrono, não bloqueia)
    try {
        $dados_notificacao = [
            'ddd' => $ddd,
            'celular' => $celular,
            'cpf' => $cpf ?? null,
            'nome' => $nome ?? null,
            'email' => $email ?? null,
            'cep' => $cep ?? null,
            'placa' => $placa ?? null,
            'gclid' => $gclid ?? null,
        ];
        
        // Enviar em background (não bloquear resposta)
        enviarNotificacaoAdministradores($dados_notificacao);
        
    } catch (Exception $e) {
        // Log erro, mas não falhar o processo principal
        error_log("Erro ao enviar notificação admin: " . $e->getMessage());
    }
}
```

---

### **FASE 5: Testes (15 minutos)**

#### **5.1. Teste Local**
```php
<?php
require 'send_admin_notification.php';

$dados_teste = [
    'ddd' => '11',
    'celular' => '987654321',
    'cpf' => '123.456.789-00',
    'nome' => 'Teste Sistema',
    'email' => 'teste@email.com',
    'cep' => '01234-567',
    'placa' => 'TEST1234',
    'gclid' => 'test-gclid-123',
];

$resultado = enviarNotificacaoAdministradores($dados_teste);
print_r($resultado);
```

#### **5.2. Verificar Email**
- Verificar caixa de entrada dos administradores
- Verificar spam (se necessário)
- Validar que HTML renderiza corretamente

---

## 🔧 CONFIGURAÇÕES AVANÇADAS

### **1. Configuração DNS Completa**

Após verificar domínio no SES, você terá:

**SPF (Já incluído no registro TXT):**
```
TXT _amazonses.bpsegurosimediato.com.br
"v=spf1 include:amazonses.com ~all"
```

**DKIM (CNAMEs gerados automaticamente):**
```
CNAME [selector1]._domainkey.bpsegurosimediato.com.br
CNAME [selector2]._domainkey.bpsegurosimediato.com.br
```

**DMARC (Opcional, mas recomendado):**
```
TXT _dmarc.bpsegurosimediato.com.br
"v=DMARC1; p=none; rua=mailto:admin@bpsegurosimediato.com.br"
```

### **2. Rate Limiting e Quotas**

**Limites padrão:**
- **Sandbox:** 200 emails/dia, 1 email/segundo
- **Production:** Após sair do sandbox, pode aumentar limites

**Para seu caso (< 1000/mês):**
- ✅ Limites padrão são mais que suficientes

### **3. Tracking e Métricas**

SES oferece métricas automáticas:
- Taxa de entrega
- Taxa de bounce
- Taxa de spam complaints
- Taxa de abertura (se configurado)

**Acessar:**
- Console SES → **Configuration sets** → **Sending statistics**

### **4. Bounce e Complaint Handling**

**Configurar feedback loops:**
1. No console SES → **Configuration sets** → **Create configuration set**
2. Configurar **Event destinations** (SNS, CloudWatch, etc.)
3. Criar webhook para processar bounces automaticamente

**Para seu caso:** Não crítico (volume baixo, lista fixa), mas recomendado.

---

## 📊 VANTAGENS DO AMAZON SES

### **Para seu caso específico:**
- ✅ **GRÁTIS:** < 1000 emails/mês = R$ 0/mês
- ✅ **Simples:** API REST, sem configuração de servidor SMTP
- ✅ **Confiável:** Servidores da Amazon (alta disponibilidade)
- ✅ **Reputação:** Menor chance de ir para spam
- ✅ **Escalável:** Se crescer, não precisa mudar
- ✅ **Métricas:** Dashboard automático
- ✅ **Seguro:** Autenticação via IAM

### **Comparado com outras opções:**

| Aspecto | Amazon SES | Servidor Próprio | SendGrid | Mailgun |
|---------|------------|-----------------|----------|---------|
| **Custo (1000/mês)** | R$ 0 | R$ 0 | R$ 0 | R$ 0-35 |
| **Configuração DNS** | Automática | Manual | Automática | Automática |
| **Complexidade** | Baixa | Alta | Muito Baixa | Baixa |
| **Limite Gratuito** | 62.000/mês | - | 3.000/mês | 5.000/mês |
| **Reputação** | Excelente | Variável | Boa | Boa |

---

## ⚠️ LIMITAÇÕES E CUIDADOS

### **1. Sandbox Mode**
- ⚠️ Por padrão, só pode enviar para emails verificados
- ✅ Solução: Solicitar saída do sandbox (processo simples)

### **2. Região AWS**
- ⚠️ Escolher região e **manter consistente**
- ✅ Recomendação: **sa-east-1** (São Paulo) para menor latência

### **3. Credenciais AWS**
- ⚠️ **NUNCA** commitar no GitHub
- ✅ Usar variáveis de ambiente ou arquivo `.env` não versionado

### **4. Verificação de Domínio**
- ⚠️ Pode levar até 72h (geralmente < 1h)
- ✅ Aguardar verificação antes de enviar

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### **Configuração AWS:**
- [ ] Conta AWS criada
- [ ] Região escolhida (sa-east-1 recomendado)
- [ ] Domínio verificado no SES
- [ ] Registros DNS configurados
- [ ] Status "Verified" confirmado
- [ ] Solicitação de saída do sandbox (se necessário)
- [ ] Usuário IAM criado
- [ ] Credenciais (Access Key/Secret) obtidas

### **Desenvolvimento:**
- [ ] AWS SDK instalado (composer require aws/aws-sdk-php)
- [ ] Arquivo `send_admin_notification.php` criado
- [ ] Credenciais configuradas (não versionadas)
- [ ] Lista de emails de administradores definida
- [ ] Integração no webhook implementada
- [ ] Tratamento de erros implementado

### **Testes:**
- [ ] Teste local executado
- [ ] Email recebido na caixa de entrada
- [ ] HTML renderiza corretamente
- [ ] Todos os campos aparecem
- [ ] Teste com dados reais do modal

### **Produção:**
- [ ] Deploy em produção
- [ ] Teste end-to-end (preencher modal → receber email)
- [ ] Monitorar logs por 24-48h
- [ ] Verificar métricas no console SES

---

## 🔗 RECURSOS ÚTEIS

- **Documentação Oficial:** https://docs.aws.amazon.com/ses/
- **SDK PHP:** https://docs.aws.amazon.com/sdk-for-php/
- **Console SES:** https://console.aws.amazon.com/ses
- **Verificação DNS:** https://mxtoolbox.com/spf.aspx

---

## 💡 PRÓXIMOS PASSOS

1. **Criar conta AWS** (se ainda não tiver)
2. **Seguir FASE 1** (Configuração AWS - 30 minutos)
3. **Seguir FASE 2** (Credenciais - 10 minutos)
4. **Seguir FASE 3** (Instalar SDK - 15 minutos)
5. **Seguir FASE 4** (Criar função PHP - 30 minutos)
6. **Seguir FASE 5** (Testes - 15 minutos)

**Tempo Total:** ~2 horas

---

**Status:** 📋 **Guia Completo**  
**Recomendação:** Amazon SES é a melhor opção para este caso (gratuito, simples, confiável)



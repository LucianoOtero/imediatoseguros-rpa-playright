# 🚀 GUIA PASSO A PASSO - CONFIGURAÇÃO AMAZON SES (NO CONSOLE AWS)

**Data:** 03/11/2025  
**Contexto:** Configuração para notificações de administradores quando telefone é validado no modal

---

## 📍 PASSO 1: ACESSAR CONSOLE SES

1. **No console AWS**, na barra de busca superior, digite: **"SES"**
2. Clique em **"Simple Email Service"**
3. Ou acesse diretamente: https://console.aws.amazon.com/ses

**Você verá:** Tela inicial do SES (pode estar em modo Sandbox)

---

## 🌍 PASSO 2: ESCOLHER REGIÃO

⚠️ **IMPORTANTE:** Escolha a região ANTES de começar e mantenha consistente!

1. **No canto superior direito**, clique no dropdown de região
2. **Recomendações:**
   - ✅ **sa-east-1** (São Paulo) - Menor latência para Brasil
   - ✅ **us-east-1** (N. Virginia) - Mais estável, maior comunidade
3. **Selecione uma região** (recomendo **sa-east-1** para você)
4. **Anote qual região escolheu** (precisará depois)

**Você verá:** Interface do SES na região selecionada

---

## ✅ PASSO 3: VERIFICAR DOMÍNIO

### **3.1. Iniciar Verificação**

1. No menu lateral esquerdo, clique em **"Verified identities"**
2. Você verá uma tela com lista de identidades verificadas (provavelmente vazia)
3. Clique no botão **"Create identity"** (canto superior direito)

### **3.2. Tipo de Identidade**

1. Escolha: **"Domain"** (domínio completo)
2. ⚠️ **NÃO escolha "Email address"** (permite apenas um email)

### **3.3. Informar Domínio**

1. No campo **"Domain"**, digite: `bpsegurosimediato.com.br`
2. ⚠️ **Sem "www"** e **sem "http://"** - apenas o domínio
3. Deixe as opções padrão marcadas:
   - ✅ **"Use a DKIM signing key pair"** (já vem marcado)
   - ✅ **"Easy DKIM"** (já selecionado)

### **3.4. Criar Identidade**

1. Role a página até o final
2. Clique em **"Create identity"**

**Você verá:** Mensagem de sucesso e uma tela com **registros DNS a configurar**

---

## 📝 PASSO 4: COPIAR REGISTROS DNS

⚠️ **MOMENTO CRÍTICO:** Copie TODOS os registros antes de fechar esta tela!

### **4.1. Registros a Copiar**

Você verá uma seção chamada **"DNS records"** com 3 registros:

**REGISTRO 1 - TXT (SPF):**
```
Tipo: TXT
Nome: _amazonses.bpsegurosimediato.com.br
Valor: [Uma string longa gerada automaticamente]
```
- Copie o **Nome** completo
- Copie o **Valor** completo (é longo, copie tudo)

**REGISTRO 2 - CNAME (DKIM 1):**
```
Tipo: CNAME
Nome: [Algo como] xxxxxx._domainkey.bpsegurosimediato.com.br
Valor: [Algo como] xxxxxx.dkim.amazonses.com
```
- Copie o **Nome** completo
- Copie o **Valor** completo

**REGISTRO 3 - CNAME (DKIM 2):**
```
Tipo: CNAME
Nome: [Algo como] yyyyyy._domainkey.bpsegurosimediato.com.br
Valor: [Algo como] yyyyyy.dkim.amazonses.com
```
- Copie o **Nome** completo
- Copie o **Valor** completo

### **4.2. Salvar Registros**

⚠️ **IMPORTANTE:** 
- Salve em um arquivo temporário
- Ou tire print da tela
- Ou mantenha a aba aberta

**Você precisará desses registros para configurar no DNS do domínio!**

---

## 🌐 PASSO 5: CONFIGURAR DNS NO PAINEL DO DOMÍNIO

Agora você precisa adicionar esses 3 registros no DNS do seu domínio.

### **5.1. Acessar Painel DNS**

1. Acesse o painel onde o DNS de `bpsegurosimediato.com.br` está gerenciado
   - Pode ser: Cloudflare, GoDaddy, Registro.br, AWS Route 53, etc.
2. Localize a seção de **"DNS Records"** ou **"Zona DNS"**

### **5.2. Adicionar Registro 1 (TXT - SPF)**

1. Clicar em **"Add record"** ou **"Adicionar registro"**
2. Preencher:
   - **Tipo:** `TXT`
   - **Nome/Host:** Cole o nome completo que copiou (ex: `_amazonses.bpsegurosimediato.com.br`)
     - ⚠️ Alguns painéis pedem apenas `_amazonses` (sem o domínio)
     - Teste ambos se necessário
   - **Valor:** Cole o valor completo que copiou do SES
   - **TTL:** Deixar padrão (3600 ou auto)
3. Salvar

### **5.3. Adicionar Registro 2 (CNAME - DKIM 1)**

1. Clicar em **"Add record"** ou **"Adicionar registro"**
2. Preencher:
   - **Tipo:** `CNAME`
   - **Nome/Host:** Cole o nome completo que copiou (ex: `xxxxxx._domainkey.bpsegurosimediato.com.br`)
   - **Valor/Destino:** Cole o valor completo que copiou do SES (ex: `xxxxxx.dkim.amazonses.com`)
   - **TTL:** Deixar padrão
3. Salvar

### **5.4. Adicionar Registro 3 (CNAME - DKIM 2)**

1. Clicar em **"Add record"** ou **"Adicionar registro"**
2. Preencher:
   - **Tipo:** `CNAME`
   - **Nome/Host:** Cole o nome completo do registro 2 (CNAME DKIM 2)
   - **Valor/Destino:** Cole o valor completo do registro 2
   - **TTL:** Deixar padrão
3. Salvar

### **5.5. Verificar Propagação**

1. Aguarde 5-10 minutos
2. Teste se os registros foram propagados:
   - Acesse: https://mxtoolbox.com/TXTLookup.aspx
   - Digite: `_amazonses.bpsegurosimediato.com.br`
   - Verifique se aparece o registro TXT que você configurou

---

## ⏳ PASSO 6: AGUARDAR VERIFICAÇÃO

### **6.1. Voltar ao Console SES**

1. No console AWS, volte para SES
2. Vá em **"Verified identities"**
3. Clique no domínio `bpsegurosimediato.com.br`

### **6.2. Status da Verificação**

Você verá o status:
- **🟡 "Pending verification"** = Aguardando verificação (normal)
- **🟢 "Verified"** = Verificado e pronto para uso!

### **6.3. Tempo de Verificação**

- **Normal:** 15 minutos a 2 horas
- **Máximo:** Até 72 horas (raro)
- **Solução se demorar:** Verifique se os registros DNS estão corretos

**⏸️ AGUARDE o status mudar para "Verified" antes de continuar!**

---

## 🚪 PASSO 7: SOLICITAR SAÍDA DO SANDBOX (OPCIONAL)

⚠️ **Por padrão, SES está em "Sandbox Mode":**
- Só pode enviar para emails **verificados**
- Para enviar para qualquer email, precisa sair do sandbox

### **7.1. Opção A: Verificar Emails dos Administradores (Temporário)**

**Enquanto aguarda aprovação do sandbox:**

1. No console SES → **"Verified identities"**
2. **"Create identity"** → Escolher **"Email address"**
3. Digitar cada email de administrador
4. Confirmar clicando no link que chega no email
5. Repetir para cada administrador

### **7.2. Opção B: Solicitar Saída do Sandbox (Recomendado)**

**Para enviar para qualquer email:**

1. No console SES → **"Account dashboard"** (menu lateral)
2. Você verá uma seção **"Account status"**
3. Clique em **"Request production access"** ou **"Move out of the Amazon SES sandbox"**

### **7.3. Preencher Formulário**

**Campos importantes:**

1. **Mail Type:** 
   - ✅ Selecionar **"Transactional"** (não marketing)

2. **Website URL:** 
   - ✅ Digitar: `https://bpsegurosimediato.com.br`

3. **Use case description:** 
   - ✅ Digitar algo como:
   ```
   Sistema de notificações internas para administradores quando clientes 
   preenchem formulário no website. Apenas emails transacionais, não marketing. 
   Volume estimado: menos de 1000 emails por mês.
   ```

4. **Expected sending rate:**
   - ✅ Digitar: `50` (emails por dia)

5. **Additional contact email addresses:**
   - ✅ Adicionar email de contato alternativo (opcional)

6. **Do you plan to send marketing emails?**
   - ✅ Selecionar **"No"**

7. **I agree to the AWS Service Terms:**
   - ✅ Marcar checkbox

8. **Submit request**

### **7.4. Aguardar Aprovação**

- **Tempo:** Geralmente 24-48 horas
- **Pode ser aprovado instantaneamente** em alguns casos
- **Notificação:** Você receberá email quando aprovado

**Status será atualizado automaticamente no console.**

---

## 🔑 PASSO 8: CRIAR CREDENCIAIS (IAM USER)

Para o código PHP enviar emails, precisa de credenciais AWS.

### **8.1. Acessar IAM**

1. No console AWS, buscar **"IAM"** na barra de busca
2. Ou acessar: https://console.aws.amazon.com/iam
3. Clicar em **"IAM"**

### **8.2. Criar Usuário**

1. No menu lateral, clique em **"Users"**
2. Clique em **"Create user"**

### **8.3. Configurar Usuário**

**Passo 1 - User name:**
- Digite: `ses-email-sender`
- Clique em **"Next"**

**Passo 2 - Permissions:**
1. Selecionar: **"Attach policies directly"**
2. Na busca, digite: **"SES"**
3. Selecionar: **"AmazonSESFullAccess"**
   - ⚠️ Esta política dá acesso total ao SES (ok para este caso)
   - Se quiser mais seguro, pode criar política customizada depois
4. Clique em **"Next"**

**Passo 3 - Review:**
- Revisar informações
- Clique em **"Create user"**

### **8.4. Obter Credenciais**

⚠️ **MOMENTO CRÍTICO:** Copie as credenciais AGORA - não será mostrado novamente!

1. Você verá mensagem: **"User created successfully"**
2. **IMPORTANTE:** Clique em **"Create access key"** (mesmo se não aparecer automaticamente)
3. Se não aparecer, clique no usuário criado → Aba **"Security credentials"** → **"Create access key"**

**Opção de uso:**
- Selecionar: **"Application running outside AWS"** ou **"Other"**
- Marcar checkbox de confirmação
- Clicar em **"Next"**
- Clicar em **"Create access key"**

### **8.5. Copiar Access Key e Secret**

**Você verá duas informações:**

1. **Access key ID:**
   - Exemplo: `AKIAIOSFODNN7EXAMPLE`
   - ✅ **Copie e salve em local seguro**

2. **Secret access key:**
   - Exemplo: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
   - ✅ **Copie e salve em local seguro**
   - ⚠️ **Esta é a ÚNICA vez que será mostrada!**

### **8.6. Salvar Credenciais**

⚠️ **NUNCA commitar no GitHub!**

**Salvar em arquivo seguro:**
```bash
# Criar arquivo .env ou config_local.php
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=sa-east-1
```

---

## ✅ PASSO 9: VERIFICAÇÃO FINAL

### **9.1. Checklist Completo**

Verifique se tudo está ok:

- [ ] **Domínio verificado** (status = "Verified" no SES)
- [ ] **Registros DNS configurados** (3 registros adicionados)
- [ ] **Região escolhida e anotada** (sa-east-1 ou us-east-1)
- [ ] **Sandbox:** 
  - [ ] Opção A: Emails de administradores verificados
  - [ ] OU Opção B: Saída do sandbox solicitada/aprovada
- [ ] **Usuário IAM criado** (`ses-email-sender`)
- [ ] **Access Key ID** copiado e salvo
- [ ] **Secret Access Key** copiado e salvo
- [ ] **Região AWS** anotada

### **9.2. Informações para o Código PHP**

Você precisará dessas informações no código:

```php
// Substituir no código que criaremos depois:
define('AWS_ACCESS_KEY_ID', 'SUA_ACCESS_KEY_ID_AQUI');
define('AWS_SECRET_ACCESS_KEY', 'SUA_SECRET_ACCESS_KEY_AQUI');
define('AWS_REGION', 'sa-east-1'); // ou a região que você escolheu
define('EMAIL_FROM', 'noreply@bpsegurosimediato.com.br');
```

---

## 🧪 PASSO 10: TESTE RÁPIDO (OPCIONAL)

### **10.1. Teste via Console SES**

1. No console SES → **"Verified identities"**
2. Clique no domínio `bpsegurosimediato.com.br`
3. Vá na aba **"Send test email"**
4. Preencher:
   - **From:** Escolher `noreply@bpsegurosimediato.com.br`
   - **To:** Email de administrador (precisa estar verificado se ainda no sandbox)
   - **Subject:** `Teste SES`
   - **Body:** `Este é um teste`
5. Clicar em **"Send test email"**
6. Verificar se email chegou

**Se funcionar, configuração está correta!**

---

## 📋 RESUMO DO QUE VOCÊ TEM AGORA

Após completar os passos, você terá:

✅ **Domínio verificado no SES**
✅ **DNS configurado** (SPF e DKIM)
✅ **Credenciais AWS** (Access Key e Secret)
✅ **Região escolhida**
✅ **Pronto para integrar no código PHP**

---

## 🔄 PRÓXIMOS PASSOS (Depois desta configuração)

1. **Instalar AWS SDK no servidor:**
   ```bash
   composer require aws/aws-sdk-php
   ```

2. **Criar função PHP** (usar o código do guia anterior)

3. **Integrar no webhook** quando telefone for validado

---

## ❓ TROUBLESHOOTING COMUM

### **Problema: Domínio não verifica após 24h**

**Soluções:**
1. Verificar se os 3 registros DNS estão corretos
2. Verificar se os valores foram copiados completamente (sem cortes)
3. Usar ferramenta: https://mxtoolbox.com/TXTLookup.aspx
4. Aguardar mais 24h (pode levar até 72h)

### **Problema: "Email address not verified" ao enviar**

**Soluções:**
1. Verificar se saiu do sandbox (Account dashboard → Status)
2. OU verificar emails de administradores individualmente
3. Aguardar aprovação do sandbox se solicitado

### **Problema: "Access Denied" ao usar credenciais**

**Soluções:**
1. Verificar se Access Key ID está correto
2. Verificar se Secret Access Key está correto
3. Verificar se usuário IAM tem política `AmazonSESFullAccess`
4. Verificar se região está correta no código

### **Problema: "Domain not verified"**

**Soluções:**
1. Verificar se registros DNS foram propagados
2. Aguardar mais tempo (pode levar até 72h)
3. Verificar se domínio está correto (sem www, sem http://)

---

## 📞 ONDE ESTÁ VOCÊ AGORA?

**Responda:**
- [ ] Está no Passo 1 (Acessar Console SES)?
- [ ] Está no Passo 3 (Verificar Domínio)?
- [ ] Está no Passo 4 (Copiar Registros DNS)?
- [ ] Está no Passo 5 (Configurar DNS)?
- [ ] Está no Passo 8 (Criar Credenciais)?
- [ ] Outro passo? Descreva onde está travado

---

**Status:** 📋 **Guia Passo a Passo Completo**  
**Dica:** Mantenha este guia aberto enquanto configura - cada passo é importante!



# ✅ PRÓXIMOS PASSOS - APÓS DKIM CONFIGURADO

**Status Atual:** DKIM configurado com sucesso ✅  
**Data:** 03/11/2025

---

## ✅ O QUE JÁ ESTÁ FEITO

- ✅ Domínio verificado no SES
- ✅ DKIM configurado e funcionando
- ✅ Registros DNS configurados no Cloudflare
- ✅ Status: "Bem-sucedido"

---

## 🔍 VERIFICAÇÃO 1: STATUS DO DOMÍNIO

### **Verificar se domínio está "Verified":**

1. No console SES, vá em **"Verified identities"** (menu lateral)
2. Clique no domínio **`bpsegurosimediato.com.br`**
3. Verifique o status no topo da página:
   - **🟢 "Verified"** = ✅ Pronto para usar!
   - **🟡 "Pending verification"** = Aguardando (normal, pode levar até 72h)

### **Se ainda estiver "Pending":**
- ✅ Normal se acabou de configurar (< 1 hora)
- ✅ Aguarde mais tempo (geralmente verifica em 1-2 horas)
- ✅ Você já configurou tudo corretamente, é só questão de tempo

---

## 🔍 VERIFICAÇÃO 2: TODOS OS REGISTROS DNS

Verifique se todos os registros estão corretos no Cloudflare:

### **Devem existir 3 registros:**

1. **TXT (SPF):**
   - Nome: `_amazonses`
   - Conteúdo: string longa com `v=spf1 include:amazonses.com`

2. **CNAME (DKIM 1):**
   - Nome: `xxxxxx._domainkey` (onde xxxxxx é um seletor)
   - Alvo: `xxxxxx.dkim.amazonses.com`
   - Proxy: **CINZA** (DNS only)

3. **CNAME (DKIM 2):**
   - Nome: `yyyyyy._domainkey` (outro seletor)
   - Alvo: `yyyyyy.dkim.amazonses.com`
   - Proxy: **CINZA** (DNS only)

### **Se algum registro estiver faltando:**
- Volte ao console SES
- Vá em **"Verified identities"** → Clique no domínio
- Role até ver **"DNS records"**
- Copie os registros faltantes e adicione no Cloudflare

---

## 📋 PRÓXIMO PASSO: CRIAR CREDENCIAIS IAM

Agora que o DNS está configurado, você precisa criar credenciais para o código PHP enviar emails.

### **O que fazer:**

1. **Acessar IAM:**
   - No console AWS, buscar **"IAM"** na barra de busca
   - Ou acessar: https://console.aws.amazon.com/iam

2. **Criar Usuário:**
   - Menu lateral → **"Users"** → **"Create user"**
   - Nome: `ses-email-sender`
   - Clique em **"Next"**

3. **Permissões:**
   - Selecionar **"Attach policies directly"**
   - Buscar: **"SES"**
   - Selecionar: **"AmazonSESFullAccess"**
   - Clique em **"Next"** → **"Create user"**

4. **Obter Credenciais:**
   - Clicar no usuário criado
   - Aba **"Security credentials"**
   - **"Create access key"**
   - Selecionar: **"Application running outside AWS"**
   - Copiar:
     - **Access Key ID**
     - **Secret Access Key** (⚠️ Esta é a ÚNICA vez que aparece!)

5. **Salvar Credenciais:**
   - Salvar em local seguro (arquivo `.env` ou config)
   - ⚠️ **NUNCA** commitar no GitHub!

---

## 🧪 TESTE RÁPIDO (OPCIONAL)

Se quiser testar se está tudo funcionando:

### **No Console SES:**

1. **"Verified identities"** → Clique no domínio
2. Aba **"Send test email"**
3. Preencher:
   - **From:** `noreply@bpsegurosimediato.com.br`
   - **To:** Seu email (precisa estar verificado se ainda no sandbox)
   - **Subject:** `Teste SES`
   - **Body:** `Teste de configuração`
4. Clicar em **"Send test email"**
5. Verificar se email chegou

**Se o email chegar:** ✅ Tudo funcionando perfeitamente!

---

## ⚠️ LEMBRETE: SANDBOX MODE

**Se ainda estiver em Sandbox:**
- ⚠️ Só pode enviar para emails **verificados**
- Para enviar para qualquer email, precisa sair do sandbox

### **Como sair do sandbox:**

1. Console SES → **"Account dashboard"**
2. Clicar em **"Request production access"**
3. Preencher formulário:
   - **Mail Type:** Transactional
   - **Website URL:** `https://bpsegurosimediato.com.br`
   - **Use case:** Notificações internas para administradores quando cliente preenche formulário
   - **Expected sending rate:** 50 emails/dia
   - **Marketing emails?** No
4. Submeter
5. Aguardar aprovação (24-48h geralmente)

**OU** verificar emails dos administradores individualmente enquanto aguarda.

---

## 📊 RESUMO DO STATUS

### **✅ Concluído:**
- [x] Conta AWS criada
- [x] Domínio verificado no SES
- [x] DKIM configurado (RSA_2048_BIT)
- [x] Registros DNS configurados no Cloudflare
- [x] Proxy desligado nos CNAMEs

### **🔄 Em Andamento:**
- [ ] Status do domínio mudando para "Verified" (aguardando)

### **⏭️ Próximos Passos:**
- [ ] Criar usuário IAM
- [ ] Obter Access Key e Secret Key
- [ ] Salvar credenciais em local seguro
- [ ] Solicitar saída do sandbox (opcional)
- [ ] Instalar AWS SDK no servidor
- [ ] Criar função PHP de envio
- [ ] Integrar no webhook

---

## 💡 O QUE FAZER AGORA?

### **Opção 1: Aguardar Verificação Completa**
- Aguardar 1-2 horas para domínio mudar para "Verified"
- Enquanto isso, pode criar as credenciais IAM (Passo acima)

### **Opção 2: Continuar Configuração**
- Criar credenciais IAM agora
- Preparar código PHP
- Quando domínio estiver "Verified", testar

**Recomendação:** Criar credenciais IAM agora (não precisa esperar verificação completa).

---

## 📞 PRÓXIMO PASSO CONCRETO

**Você está pronto para:**

1. **Ir para IAM** → Criar usuário → Obter credenciais
2. **OU** Aguardar verificação do domínio primeiro

**O que você prefere fazer agora?**

---

**Status:** ✅ **DKIM Configurado - Pronto para próximos passos**  
**Tempo estimado para próxima etapa:** 10-15 minutos (criar credenciais IAM)



# 🌐 GUIA: CONFIGURAR DNS NO CLOUDFLARE PARA AMAZON SES

**Data:** 03/11/2025  
**Domínio:** bpsegurosimediato.com.br  
**Serviço:** Amazon SES

---

## 🎯 VISÃO GERAL

Este guia mostra como adicionar os registros DNS (TXT e CNAME) do Amazon SES no painel do Cloudflare.

**Você precisa de:**
- ✅ Conta no Cloudflare
- ✅ Domínio `bpsegurosimediato.com.br` já no Cloudflare
- ✅ Os registros DNS que o Amazon SES gerou (do console AWS)

---

## 📋 PASSO A PASSO

### **PASSO 1: ACESSAR PAINEL CLOUDFLARE**

1. Acesse: https://dash.cloudflare.com
2. Faça login na sua conta
3. Clique no domínio **`bpsegurosimediato.com.br`**
4. No menu lateral, clique em **"DNS"** ou **"DNS Records"**

**Você verá:** Lista de registros DNS existentes

---

### **PASSO 2: ADICIONAR REGISTRO TXT (SPF)**

Este é o primeiro registro que você copiou do console Amazon SES.

#### **2.1. Clicar em "Add record"**

No canto superior direito, clique no botão **"+ Add record"**

#### **2.2. Preencher Campos**

**Tipo:**
- Selecione: **"TXT"**

**Nome (Name):**
- No Cloudflare, você pode adicionar de duas formas:
  - **Opção 1 (Recomendada):** Digite apenas `_amazonses`
    - Cloudflare automaticamente completa com o domínio
    - Fica como: `_amazonses.bpsegurosimediato.com.br`
  - **Opção 2:** Digite o nome completo: `_amazonses.bpsegurosimediato.com.br`

**Conteúdo (Content):**
- Cole o **valor completo** que você copiou do console Amazon SES
- É uma string longa, algo como:
  ```
  v=spf1 include:amazonses.com ~all
  ```
- ⚠️ **Cole TUDO**, mesmo que seja longo

**Proxy status:**
- ⚠️ **IMPORTANTE:** Clique na nuvem laranja até ela ficar **CINZA** (DNS only)
  - ✅ **DNS only** (cinza) = Registro DNS puro
  - ❌ **Proxied** (laranja) = Cloudflare proxy (não funciona para SES)
- O TXT deve estar com proxy **DESLIGADO** (cinza)

**TTL:**
- Deixe **"Auto"** ou selecione **"3600"** (1 hora)

#### **2.3. Salvar**

Clique em **"Save"**

**Você verá:** Novo registro TXT na lista

---

### **PASSO 3: ADICIONAR CNAME 1 (DKIM)**

Este é o segundo registro do Amazon SES (primeiro CNAME).

#### **3.1. Clicar em "Add record"**

Novamente, clique em **"+ Add record"**

#### **3.2. Preencher Campos**

**Tipo:**
- Selecione: **"CNAME"**

**Nome (Name):**
- **No Cloudflare, adicione apenas a parte ANTES do domínio:**
  - Se o SES mostrou: `xxxxxx._domainkey.bpsegurosimediato.com.br`
  - No Cloudflare, digite apenas: `xxxxxx._domainkey`
  - Cloudflare automaticamente adiciona `.bpsegurosimediato.com.br`
  
  **OU se preferir:**
  - Digite o nome completo: `xxxxxx._domainkey.bpsegurosimediato.com.br`
  - Cloudflare pode aceitar também

**Alvo (Target):**
- Cole o **valor completo** que você copiou do SES
- Algo como: `xxxxxx.dkim.amazonses.com`
- ⚠️ **Adicione ponto final no final:** `xxxxxx.dkim.amazonses.com.`
  - Alguns DNS requerem ponto final, outros não
  - Se Cloudflare não aceitar com ponto, tente sem

**Proxy status:**
- ⚠️ **IMPORTANTE:** Deixe **CINZA** (DNS only)
  - ✅ **DNS only** (cinza)
  - ❌ **NÃO** use proxy (laranja)

**TTL:**
- Deixe **"Auto"** ou **"3600"**

#### **3.3. Salvar**

Clique em **"Save"**

**Você verá:** Novo registro CNAME na lista

---

### **PASSO 4: ADICIONAR CNAME 2 (DKIM)**

Este é o terceiro registro do Amazon SES (segundo CNAME).

#### **4.1. Clicar em "Add record"**

Clique em **"+ Add record"** novamente

#### **4.2. Preencher Campos**

**Tipo:**
- Selecione: **"CNAME"**

**Nome (Name):**
- Adicione apenas a parte antes do domínio:
  - Se o SES mostrou: `yyyyyy._domainkey.bpsegurosimediato.com.br`
  - No Cloudflare, digite: `yyyyyy._domainkey`

**Alvo (Target):**
- Cole o valor do segundo CNAME do SES
- Algo como: `yyyyyy.dkim.amazonses.com`
- ⚠️ Pode tentar com ou sem ponto final no final

**Proxy status:**
- ⚠️ **IMPORTANTE:** Deixe **CINZA** (DNS only)

**TTL:**
- Deixe **"Auto"**

#### **4.3. Salvar**

Clique em **"Save"**

---

## ✅ VERIFICAÇÃO DOS REGISTROS

### **Verificar no Cloudflare:**

1. Na lista de registros DNS, você deve ver:
   - ✅ 1 registro **TXT** com nome `_amazonses`
   - ✅ 1 registro **CNAME** com nome contendo `_domainkey` (primeiro)
   - ✅ 1 registro **CNAME** com nome contendo `_domainkey` (segundo)

2. Todos devem estar com proxy **CINZA** (DNS only)

### **Verificar Propagação:**

Após salvar, aguarde **5-10 minutos** e verifique:

#### **Teste 1 - TXT Record:**
1. Acesse: https://mxtoolbox.com/TXTLookup.aspx
2. Digite: `_amazonses.bpsegurosimediato.com.br`
3. Clique em **"TXT Lookup"**
4. Você deve ver o registro TXT que adicionou

#### **Teste 2 - CNAME Records:**
1. Acesse: https://mxtoolbox.com/CNAMELookup.aspx
2. Digite: `xxxxxx._domainkey.bpsegurosimediato.com.br` (substitua xxxxxx pelo valor real)
3. Clique em **"CNAME Lookup"**
4. Você deve ver o registro CNAME apontando para `xxxxxx.dkim.amazonses.com`

#### **Teste 3 - Verificação Automática:**
1. Volte ao console Amazon SES
2. Vá em **"Verified identities"**
3. Clique no domínio `bpsegurosimediato.com.br`
4. Verifique o status:
   - **"Pending verification"** = Ainda verificando (normal, aguarde)
   - **"Verified"** = ✅ Verificado e pronto!

---

## 📸 EXEMPLO VISUAL DOS CAMPOS

### **Registro TXT (SPF):**

```
┌─────────────────────────────────────────┐
│ Tipo: TXT                               │
│ Nome: _amazonses                        │
│ Conteúdo: v=spf1 include:amazonses...   │
│ Proxy: [CINZA] DNS only                 │
│ TTL: Auto                               │
└─────────────────────────────────────────┘
```

### **Registro CNAME (DKIM 1):**

```
┌─────────────────────────────────────────┐
│ Tipo: CNAME                             │
│ Nome: xxxxxx._domainkey                 │
│ Alvo: xxxxxx.dkim.amazonses.com         │
│ Proxy: [CINZA] DNS only                 │
│ TTL: Auto                               │
└─────────────────────────────────────────┘
```

### **Registro CNAME (DKIM 2):**

```
┌─────────────────────────────────────────┐
│ Tipo: CNAME                             │
│ Nome: yyyyyy._domainkey                 │
│ Alvo: yyyyyy.dkim.amazonses.com         │
│ Proxy: [CINZA] DNS only                 │
│ TTL: Auto                               │
└─────────────────────────────────────────┘
```

---

## ⚠️ PROBLEMAS COMUNS NO CLOUDFLARE

### **Problema 1: "Proxy enabled" (Nuvem Laranja) - ERRO COMUM!**

**Sintoma:** 
- Erro: `"Target ... is not allowed for a proxied record"`
- OU Registros não verificam no SES

**Solução:**
1. Ao criar o registro, **ANTES de salvar**, verifique:
   - O campo "Proxy status" deve estar **CINZA** (DNS only)
   - Se estiver **LARANJA** (Proxied), clique na nuvem para desligar

2. **Se já salvou com proxy ligado:**
   - Clique no registro DNS na lista
   - Clique na **nuvem laranja** até ficar **CINZA**
   - Clique em **"Save"**
   - Aguardar propagação (pode levar alguns minutos)

**Importante:** 
- DNS records para serviços externos (como SES) **SEMPRE** devem estar com proxy desligado
- Cloudflare **NÃO permite** CNAMEs com proxy apontando para domínios externos

---

### **Problema 2: "Invalid name" ao adicionar CNAME**

**Sintoma:** Cloudflare não aceita o nome do CNAME

**Soluções:**
1. Tente apenas a parte antes do domínio:
   - Use: `xxxxxx._domainkey`
   - Não use: `xxxxxx._domainkey.bpsegurosimediato.com.br`

2. Se ainda não funcionar, verifique:
   - Não há espaços extras
   - Não há caracteres inválidos
   - O nome está correto (copiado do SES)

---

### **Problema 3: "Invalid target" no CNAME**

**Sintoma:** Cloudflare não aceita o valor do CNAME

**Soluções:**
1. Verifique se copiou o valor completo do SES
2. Tente **com** ponto final no final do valor:
   - `xxxxxx.dkim.amazonses.com.`
3. Tente **sem** ponto final:
   - `xxxxxx.dkim.amazonses.com`
4. Cloudflare geralmente aceita sem ponto final

---

### **Problema 4: Registros não propagam após 1 hora**

**Soluções:**
1. Verificar se os registros estão corretos no Cloudflare
2. Limpar cache do Cloudflare:
   - Ir em **"Caching"** → **"Purge Everything"**
3. Verificar no MXToolbox se os registros estão visíveis
4. Aguardar mais tempo (pode levar até 48h, geralmente < 1h)

---

### **Problema 5: Cloudflare mostra "Already exists"**

**Sintoma:** Tentou adicionar registro que já existe

**Solução:**
1. Verifique se o registro já está na lista
2. Se estiver, edite o existente (não crie duplicado)
3. Se não estiver na lista, pode ser cache - aguarde alguns minutos

---

## 🔍 CHECKLIST FINAL

Após adicionar todos os registros, verifique:

- [ ] **3 registros adicionados** (1 TXT + 2 CNAME)
- [ ] **Todos com proxy CINZA** (DNS only)
- [ ] **Valores copiados corretamente** do console SES
- [ ] **Aguardado 5-10 minutos** para propagação
- [ ] **Testado no MXToolbox** (registros visíveis)
- [ ] **Status no SES** mudou para "Verified" (ou ainda "Pending")

---

## 📱 REGISTROS CRIADOS - RESUMO

Após completar, você terá:

```
Tipo: TXT
Nome: _amazonses
Conteúdo: [valor do SES]
Proxy: OFF (cinza)

Tipo: CNAME
Nome: [selector1]._domainkey
Alvo: [selector1].dkim.amazonses.com
Proxy: OFF (cinza)

Tipo: CNAME
Nome: [selector2]._domainkey
Alvo: [selector2].dkim.amazonses.com
Proxy: OFF (cinza)
```

---

## ⏭️ PRÓXIMO PASSO

Após configurar os registros DNS no Cloudflare:

1. ✅ Aguardar propagação (5-10 minutos)
2. ✅ Verificar no console SES se status mudou para "Verified"
3. ✅ Continuar com criação de credenciais IAM (Passo 8 do guia anterior)
4. ✅ Instalar AWS SDK no servidor
5. ✅ Criar função PHP de envio

---

## 📞 PRECISA DE AJUDA?

**Se estiver travado em algum passo:**
1. Me diga **qual registro** está tentando adicionar (TXT ou CNAME)
2. Me diga **qual erro** aparece (se houver)
3. Tire um print da tela (se possível) ou descreva o que vê

**Status:** 📋 **Guia Completo para Cloudflare**  
**Tempo estimado:** 10-15 minutos para configurar os 3 registros


# ⚠️ SOLUÇÃO: ERRO "Target is not allowed for a proxied record"

**Erro:** `Target z2uoveht4sojaiillgwqqsktmub5wdjb.dkim.amazonses.com. is not allowed for a proxied record.`

---

## 🎯 CAUSA DO ERRO

O Cloudflare está mostrando esse erro porque você tentou criar um registro **CNAME com proxy ATIVO** (nuvem laranja), e o Cloudflare **não permite** CNAMEs proxied apontando para domínios externos.

---

## ✅ SOLUÇÃO RÁPIDA

### **Opção 1: Ao Criar o Registro (Recomendada)**

**ANTES de clicar em "Save":**

1. Olhe para o campo **"Proxy status"** ou a **nuvem** ao lado do registro
2. Se estiver **LARANJA** 🟠 (Proxied):
   - **Clique na nuvem** para desligar
   - Deve ficar **CINZA** ⚪ (DNS only)
3. **AGORA** clique em **"Save"**

**Pronto!** O registro será criado corretamente.

---

### **Opção 2: Se Já Salvou Com Erro**

1. **Localize o registro CNAME** na lista de DNS
2. **Clique no registro** para editar
3. Você verá a **nuvem LARANJA** 🟠
4. **Clique na nuvem** para desligar o proxy
5. Deve ficar **CINZA** ⚪
6. Clique em **"Save"**

**Aguarde alguns minutos** e tente criar o registro novamente.

---

## 📸 VISUAL - O QUE FAZER

### **❌ ERRADO (Vai dar erro):**

```
┌──────────────────────────────────────────┐
│ Tipo: CNAME                              │
│ Nome: xxxxxx._domainkey                  │
│ Alvo: xxxxxx.dkim.amazonses.com          │
│ Proxy: [🟠 LARANJA] Proxied  ← ERRADO!  │
└──────────────────────────────────────────┘
```

### **✅ CORRETO (Funciona):**

```
┌──────────────────────────────────────────┐
│ Tipo: CNAME                              │
│ Nome: xxxxxx._domainkey                  │
│ Alvo: xxxxxx.dkim.amazonses.com          │
│ Proxy: [⚪ CINZA] DNS only  ← CORRETO!   │
└──────────────────────────────────────────┘
```

---

## 🔍 COMO IDENTIFICAR O PROXY STATUS

### **No Cloudflare:**

**Ao criar/editar registro:**
- Você verá um campo chamado **"Proxy status"** ou uma **nuvem ao lado**
- **Laranja 🟠** = Proxy ATIVO (não funciona para SES)
- **Cinza ⚪** = Proxy DESLIGADO (funciona para SES)

**Na lista de registros:**
- Registros com proxy aparecem com nuvem **laranja** 🟠
- Registros sem proxy aparecem com nuvem **cinza** ⚪ ou sem nuvem

---

## 📋 CHECKLIST PARA EVITAR O ERRO

Antes de salvar o registro CNAME, verifique:

- [ ] Tipo selecionado: **CNAME**
- [ ] Nome preenchido: `xxxxxx._domainkey` (ou nome completo)
- [ ] Alvo preenchido: `xxxxxx.dkim.amazonses.com`
- [ ] **Proxy: CINZA ⚪ (DNS only)** ← **IMPORTANTE!**
- [ ] TTL: Auto ou 3600
- [ ] Agora pode clicar em **"Save"**

---

## 🎯 PASSO A PASSO COMPLETO (RECRIAR)

Se o registro já foi criado com erro, siga estes passos:

### **1. Deletar Registro Errado (Se Existir)**

1. Na lista de DNS, encontre o CNAME que deu erro
2. Clique nos **3 pontinhos** ao lado
3. Clique em **"Delete"**
4. Confirme

### **2. Criar Novamente Corretamente**

1. Clique em **"+ Add record"**
2. **Tipo:** CNAME
3. **Nome:** `z2uoveht4sojaiillgwqqsktmub5wdjb._domainkey`
   - (Use o valor que você tem do SES)
4. **Alvo:** `z2uoveht4sojaiillgwqqsktmub5wdjb.dkim.amazonses.com`
   - (Sem ponto final no final)
5. **⚠️ ANTES DE SALVAR:** Verifique se proxy está **CINZA ⚪**
   - Se estiver laranja, clique na nuvem para desligar
6. **Save**

### **3. Repetir Para o Segundo CNAME**

1. Adicionar outro CNAME com o segundo seletor do SES
2. Mesma configuração (proxy CINZA)

---

## ❓ POR QUE ISSO ACONTECE?

**Cloudflare Proxy (nuvem laranja):**
- É usado para proteger e acelerar o site
- Funciona bem para sites web (HTTP/HTTPS)
- **NÃO funciona** para registros DNS que apontam para serviços externos

**DNS Records para serviços externos (como SES):**
- Devem estar com proxy **DESLIGADO** (cinza)
- Permite que o DNS seja resolvido diretamente
- Necessário para serviços como SES, Google Workspace, etc.

---

## ✅ VERIFICAÇÃO FINAL

Após corrigir, verifique:

1. **Na lista de DNS:**
   - Ambos os CNAMEs aparecem com nuvem **CINZA** ⚪
   - OU sem nuvem visível (também ok)

2. **Teste de propagação (após 5-10 min):**
   - Acesse: https://mxtoolbox.com/CNAMELookup.aspx
   - Digite: `z2uoveht4sojaiillgwqqsktmub5wdjb._domainkey.bpsegurosimediato.com.br`
   - Deve retornar: `z2uoveht4sojaiillgwqqsktmub5wdjb.dkim.amazonses.com`

3. **No console SES:**
   - Status deve mudar para "Verified" (pode levar alguns minutos a horas)

---

## 🚀 PRÓXIMO PASSO

Depois que ambos os CNAMEs estiverem configurados corretamente:

1. ✅ Aguardar 5-10 minutos para propagação
2. ✅ Verificar status no console SES
3. ✅ Continuar com criação de credenciais IAM
4. ✅ Configurar código PHP

---

**Status:** ✅ **Solução para o erro específico**  
**Tempo para corrigir:** 2-5 minutos



# 🔧 Guia: Configurar Cloudflare para Não Fazer Cache dos Arquivos JavaScript

## 📋 Objetivo
Configurar o Cloudflare para **NÃO fazer cache** dos arquivos JavaScript em `/webhooks/*.js`, garantindo que mudanças sejam imediatamente refletidas sem precisar limpar cache manualmente.

---

## 🎯 Domínio Afetado
- **Desenvolvimento**: `dev.bpsegurosimediato.com.br`
- **Produção**: `bpsegurosimediato.com.br` (opcional, configurar depois)

---

## 📝 Método 1: Cache Rules (Recomendado - Cloudflare Dashboard Atual)

### **Passo 1: Acessar o Dashboard do Cloudflare**

1. Acesse: https://dash.cloudflare.com
2. Faça login na sua conta
3. Selecione o domínio: `bpsegurosimediato.com.br` (ou `dev.bpsegurosimediato.com.br`)

### **Passo 2: Criar Cache Rule**

1. No menu lateral esquerdo, clique em **Rules** → **Cache Rules**
2. Clique no botão **Create rule**
3. Preencha os campos:

   **Rule name:**
   ```
   Bypass Cache - Webhooks JS Files
   ```

   **When incoming requests match:**
   - Campo 1: `Hostname` → `is` → `dev.bpsegurosimediato.com.br`
   - Campo 2: `URI Path` → `starts with` → `/webhooks/`
   - Campo 3: `URI Extension` → `is` → `js`
   
   (Clique em **Add condition** para adicionar mais condições)

4. **Then the settings are:**
   - Selecione `Bypass Cache`
   - Opcionalmente, marque `Clear cache on save` para limpar cache existente

5. Clique em **Save and Deploy**

### **Passo 3: Verificar a Regra**

1. Após salvar, a regra aparecerá na lista
2. Verifique se está **Enabled** (ativa)
3. Teste acessando:
   ```
   https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js
   ```

---

## 📝 Método 2: Page Rules (Método Antigo - Se não tiver Cache Rules)

### **Passo 1: Acessar Page Rules**

1. Acesse: https://dash.cloudflare.com
2. Selecione o domínio
3. No menu lateral, clique em **Rules** → **Page Rules**

### **Passo 2: Criar Page Rule**

1. Clique em **Create Page Rule**

2. **URL pattern:**
   ```
   *dev.bpsegurosimediato.com.br/webhooks/*.js
   ```
   (Para produção: `*bpsegurosimediato.com.br/webhooks/*.js`)

3. **Settings:**
   - Clique em **+ Add a Setting**
   - Selecione **Cache Level**
   - Escolha: **Bypass**
   - Clique em **Save and Deploy**

### **Passo 3: Verificar**

1. A regra aparecerá na lista (ordem importa - regras no topo têm prioridade)
2. Teste acessando o arquivo via navegador

---

## 🔍 Método 3: Verificar/Testar se Está Funcionando

### **Opção A: Via Navegador**

1. Abra o Chrome/Edge em modo anônimo (sem cache)
2. Acesse:
   ```
   https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js
   ```
3. Abra o **DevTools** (F12)
4. Vá na aba **Network**
5. Recarregue a página (Ctrl+R)
6. Clique no arquivo `MODAL_WHATSAPP_DEFINITIVO.js`
7. Verifique os **Headers**:
   - **Response Headers** deve ter: `cf-cache-status: DYNAMIC` ou `BYPASS`
   - Se aparecer `HIT`, o cache ainda está ativo (aguarde alguns minutos)

### **Opção B: Via Terminal (PowerShell)**

```powershell
# Verificar headers de resposta
$response = Invoke-WebRequest -Uri "https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js" -Method Head
$response.Headers["cf-cache-status"]
```

**Resultados esperados:**
- ✅ `DYNAMIC` ou `BYPASS` → Cache desabilitado corretamente
- ❌ `HIT` ou `MISS` → Cache ainda está ativo (aguarde ou verifique a regra)

---

## 📝 Método 4: Configurar para Produção também (Opcional)

Para aplicar a mesma regra em produção:

1. Crie uma **nova Cache Rule** ou **Page Rule**
2. URL pattern:
   ```
   *bpsegurosimediato.com.br/webhooks/*.js
   ```
3. Mesmas configurações: **Bypass Cache**

---

## ⚙️ Configuração Avançada: Cache Control via Headers HTTP (Alternativa)

Se você tiver acesso ao servidor, pode configurar headers HTTP diretamente:

### **No Apache (.htaccess ou VirtualHost)**

```apache
<FilesMatch "MODAL_WHATSAPP_DEFINITIVO\.js|FooterCodeSiteDefinitivoUtils\.js">
    Header set Cache-Control "no-cache, no-store, must-revalidate, max-age=0"
    Header set Pragma "no-cache"
    Header set Expires "0"
</FilesMatch>
```

### **No Nginx (server block)**

```nginx
location ~ ^/webhooks/.*\.js$ {
    add_header Cache-Control "no-cache, no-store, must-revalidate, max-age=0";
    add_header Pragma "no-cache";
    add_header Expires "0";
}
```

---

## ⏱️ Tempo de Propagação

- **Cache Rules**: Aplicação imediata (pode levar 1-2 minutos)
- **Page Rules**: Aplicação imediata (pode levar alguns minutos)
- **Purge Manual**: Necessário após criar a regra para limpar cache existente

### **Como Fazer Purge Manual no Cloudflare:**

1. No dashboard do Cloudflare, vá em **Caching** → **Configuration**
2. Clique em **Purge Everything** (limpa tudo) ou
3. Use **Custom Purge** e insira:
   ```
   https://dev.bpsegurosimediato.com.br/webhooks/*.js
   ```
4. Clique em **Purge**

---

## ✅ Checklist de Verificação

- [ ] Regra criada no Cloudflare (Cache Rule ou Page Rule)
- [ ] Regra está **Enabled** (ativa)
- [ ] URL pattern está correto
- [ ] Cache Level configurado como **Bypass**
- [ ] Purge manual realizado (opcional, mas recomendado)
- [ ] Testado via navegador - `cf-cache-status` mostra `DYNAMIC` ou `BYPASS`
- [ ] Aguardado 2-3 minutos após criar a regra

---

## 🐛 Troubleshooting

### **Problema: Cache ainda está ativo após criar a regra**

**Soluções:**
1. Aguarde 2-5 minutos (propagação do Cloudflare)
2. Faça purge manual do cache
3. Verifique a ordem das regras (Page Rules)
4. Teste em modo anônimo do navegador
5. Verifique se a URL pattern está correta (case-sensitive)

### **Problema: Regra não aparece no dashboard**

**Soluções:**
1. Verifique se está logado no Cloudflare correto
2. Verifique se o domínio está no Cloudflare
3. Atualize a página do dashboard

---

## 📚 Referências

- **Cloudflare Cache Rules**: https://developers.cloudflare.com/cache/how-to/cache-rules/
- **Cloudflare Page Rules**: https://developers.cloudflare.com/fundamentals/get-started/concepts/how-cloudflare-works/
- **Cache Headers**: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control

---

## 🎯 Resultado Esperado

Após configurar, os arquivos em `/webhooks/*.js` **não serão mais cacheados** pelo Cloudflare, garantindo que mudanças no código sejam imediatamente refletidas sem necessidade de limpar cache manualmente.

---

**Última atualização:** 2025-10-29
**Versão do Guia:** 1.0












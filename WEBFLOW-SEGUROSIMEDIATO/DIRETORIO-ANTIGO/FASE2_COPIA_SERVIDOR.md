# FASE 2: CÓPIA DO ARQUIVO PARA O SERVIDOR

## ✅ Arquivo Local Criado
- **Caminho:** `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js`
- **Destino Servidor:** `/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js`
- **URL Pública:** `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js`

## 📤 Comandos para Copiar Arquivo

### Opção 1: Via SCP (PowerShell/SSH)

```powershell
# Comando completo (ajustar caminho se necessário)
scp "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js" root@46.62.174.150:/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js
```

**Ou caminho completo:**
```powershell
scp "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright\02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js" root@46.62.174.150:/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js
```

### Opção 2: Via SFTP (FTP Client)
- **Host:** `46.62.174.150` ou `dev.bpsegurosimediato.com.br`
- **Usuário:** `root`
- **Caminho remoto:** `/var/www/html/dev/webhooks/`
- **Arquivo:** `FooterCodeSiteDefinitivoCompleto.js`

## ✅ Verificações Após Cópia

### 1. Verificar Arquivo no Servidor
```bash
ssh root@46.62.174.150 "ls -lh /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js"
```

### 2. Verificar Tamanho
```bash
ssh root@46.62.174.150 "wc -c /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js"
```
**Esperado:** ~71.000 bytes

### 3. Testar URL Pública
Abrir no navegador:
```
https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js
```

**Verificações:**
- [ ] Status HTTP: 200 OK
- [ ] Content-Type: `text/javascript` ou `application/javascript`
- [ ] Conteúdo JavaScript visível (não erro 404/500)
- [ ] Cache-Control: `public, max-age=3600` (recomendado)

### 4. Verificar Headers HTTP

**Via PowerShell:**
```powershell
Invoke-WebRequest -Uri "https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js" -Method Head | Select-Object StatusCode, Headers
```

**Via cURL:**
```bash
curl -I https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js
```

**Headers Esperados:**
- `Content-Type: text/javascript` ou `application/javascript`
- `Cache-Control: public, max-age=3600` (recomendado)

### 5. Configurar Headers (se necessário)

**Se Content-Type ou Cache-Control estiverem incorretos:**

```bash
# Conectar ao servidor
ssh root@46.62.174.150

# Verificar configuração do Nginx/Apache
# Nginx: /etc/nginx/sites-available/dev.bpsegurosimediato.com.br
# Apache: /etc/apache2/sites-available/dev.bpsegurosimediato.com.br.conf

# Adicionar configuração para arquivos .js (se necessário)
```

## 📝 Checklist Fase 2

- [ ] Arquivo copiado para servidor
- [ ] Arquivo existe no caminho correto
- [ ] URL pública acessível (200 OK)
- [ ] Content-Type correto (`text/javascript`)
- [ ] Cache-Control configurado (opcional mas recomendado)
- [ ] Tamanho do arquivo confere (~71KB)
- [ ] Backup criado no servidor (opcional)

## 🔄 Backup no Servidor (Recomendado)

```bash
# Criar backup antes de atualizar
ssh root@46.62.174.150 "cp /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js.backup_$(date +%Y%m%d_%H%M%S)"
```

## ⚠️ Próximos Passos

Após completar esta fase:
1. **Fase 3:** Fazer backup do Footer Code no Webflow
2. **Fase 4:** Atualizar Webflow para referenciar arquivo unificado
3. **Fase 5:** Testar funcionalidades no site








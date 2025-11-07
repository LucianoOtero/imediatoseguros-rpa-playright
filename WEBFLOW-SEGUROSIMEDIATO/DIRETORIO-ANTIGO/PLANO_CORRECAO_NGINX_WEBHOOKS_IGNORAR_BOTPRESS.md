# PLANO DE CORREÇÃO: NGINX - SERVIR ARQUIVOS WEBHOOKS IGNORANDO BOTPRESS

**Data:** 02/11/2025  
**Domínio:** bpsegurosimediato.com.br  
**Objetivo:** Corrigir 404 em arquivos JavaScript mantendo Botpress operacional (mas ignorado)  
**Status:** 📋 PLANEJADO - NÃO EXECUTADO

---

## 📊 ANÁLISE DA SITUAÇÃO ATUAL

### **Contexto**
- Botpress foi instalado mas **não é mais necessário** para operação
- Botpress **não será desinstalado** (pode estar sendo usado por outras partes)
- Botpress continua rodando na porta `3000`
- Requisições para `/webhooks/*.js` estão retornando **404** porque são enviadas ao Botpress

### **Problema Identificado**
1. Configuração em `sites-available` está **CORRETA** (inclui location block para webhooks)
2. Configuração em `sites-enabled` está **DESATUALIZADA** (não é symlink, falta location block)
3. Todas as requisições caem no `location /` (catch-all) que faz proxy para Botpress
4. Botpress não tem os arquivos → **404**

### **Comportamento Atual do Nginx**

```
GET /webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
  ↓
Ordem de avaliação dos location blocks:
  1. location ~ \.php$ → ❌ Não match
  2. location /logging_system/ → ❌ Não match
  3. location ~ ^/(logs|...) → ❌ Não match
  4. location ~ ^/webhooks/.*\.(js|css)$ → ❌ NÃO EXISTE na config ativa!
  5. location / → ✅ MATCH (catch-all) → proxy_pass Botpress → 404
```

### **Comportamento Esperado Após Correção**

```
GET /webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
  ↓
Ordem de avaliação dos location blocks:
  1. location ~ \.php$ → ❌ Não match
  2. location /logging_system/ → ❌ Não match
  3. location ~ ^/(logs|...) → ❌ Não match
  4. location ~ ^/webhooks/.*\.(js|css)$ → ✅ MATCH → Serve arquivo → 200 OK
  5. location / → Não avaliado (já matchou no 4)
```

---

## 🎯 OBJETIVO DA CORREÇÃO

Adicionar o location block para `/webhooks/.*\.(js|css)$` na configuração **ativa** do Nginx, garantindo que:

1. ✅ Arquivos JS/CSS em `/webhooks/` sejam servidos diretamente pelo Nginx
2. ✅ Botpress continue operacional (não será removido ou parado)
3. ✅ Botpress seja **ignorado** para requisições de webhooks (não recebe essas requisições)
4. ✅ Outras requisições continuem sendo enviadas ao Botpress via `location /` (se necessário)

---

## 🔧 ESTRATÉGIA DE CORREÇÃO

### **Opção 1: Converter para Symlink (RECOMENDADO)**

**Vantagens:**
- ✅ Futuras alterações em `sites-available` serão automaticamente refletidas
- ✅ Boa prática de gerenciamento do Nginx
- ✅ Evita dessincronização futura
- ✅ Mais fácil de manter

**Passos:**
1. Backup da configuração atual
2. Remover arquivo físico em `sites-enabled`
3. Criar symlink apontando para `sites-available`
4. Testar sintaxe
5. Recarregar Nginx

### **Opção 2: Atualizar Arquivo Físico**

**Vantagens:**
- ✅ Mais direto (copiar conteúdo)
- ✅ Mantém estrutura atual

**Desvantagens:**
- ❌ Risco de dessincronização futura
- ❌ Não segue melhor prática

---

## 📋 PLANO DE EXECUÇÃO DETALHADO

### **FASE 1: PREPARAÇÃO E BACKUP**

#### 1.1. Verificar estado atual
```bash
# Verificar configuração atual
cat /etc/nginx/sites-enabled/bpsegurosimediato.com.br

# Verificar se sites-available tem a configuração correta
cat /etc/nginx/sites-available/bpsegurosimediato.com.br | grep -A 10 "location.*webhooks"

# Verificar se é symlink ou arquivo físico
ls -la /etc/nginx/sites-enabled/bpsegurosimediato.com.br
```

**Resultado esperado:**
- ❌ Não é symlink (é arquivo físico)
- ❌ Não contém location block para webhooks

#### 1.2. Criar backup completo
```bash
# Criar diretório de backup
mkdir -p /root/nginx_backups/$(date +%Y%m%d_%H%M%S)

# Backup da configuração atual (sites-enabled)
cp /etc/nginx/sites-enabled/bpsegurosimediato.com.br /root/nginx_backups/$(date +%Y%m%d_%H%M%S)/bpsegurosimediato.com.br.enabled.backup

# Backup da configuração disponível (sites-available)
cp /etc/nginx/sites-available/bpsegurosimediato.com.br /root/nginx_backups/$(date +%Y%m%d_%H%M%S)/bpsegurosimediato.com.br.available.backup

# Verificar backup
ls -lh /root/nginx_backups/$(date +%Y%m%d_%H%M%S)/
```

**Resultado esperado:**
- ✅ Arquivos de backup criados com sucesso

---

### **FASE 2: IMPLEMENTAÇÃO (OPÇÃO 1 - SYMLINK - RECOMENDADA)**

#### 2.1. Remover arquivo físico atual
```bash
# Remover arquivo físico (não é symlink, é seguro remover)
rm /etc/nginx/sites-enabled/bpsegurosimediato.com.br

# Verificar remoção
ls -la /etc/nginx/sites-enabled/bpsegurosimediato.com.br
```

**Resultado esperado:**
- ✅ Arquivo removido (ou erro se já não existir)

#### 2.2. Criar symlink
```bash
# Criar symlink apontando para sites-available
ln -s /etc/nginx/sites-available/bpsegurosimediato.com.br /etc/nginx/sites-enabled/bpsegurosimediato.com.br

# Verificar symlink criado
ls -la /etc/nginx/sites-enabled/bpsegurosimediato.com.br
```

**Resultado esperado:**
```
lrwxrwxrwx 1 root root 55 Nov  2 17:30 /etc/nginx/sites-enabled/bpsegurosimediato.com.br -> /etc/nginx/sites-available/bpsegurosimediato.com.br
```

#### 2.3. Verificar conteúdo do symlink
```bash
# Ler conteúdo através do symlink
cat /etc/nginx/sites-enabled/bpsegurosimediato.com.br | grep -A 10 "location.*webhooks"
```

**Resultado esperado:**
```nginx
location ~ ^/webhooks/.*\.(js|css)$ {
    root /var/www/html;
    try_files $uri =404;
    expires 1h;
    add_header Cache-Control "public, max-age=3600";
    add_header Content-Type application/javascript;
}
```

---

### **FASE 3: VALIDAÇÃO**

#### 3.1. Testar sintaxe do Nginx
```bash
# Testar sintaxe
nginx -t
```

**Resultado esperado:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

**Se houver erro:**
- ❌ Parar execução
- 🔄 Reverter para backup
- 📝 Analisar erro

#### 3.2. Verificar ordem dos location blocks
```bash
# Extrair e verificar ordem dos location blocks
cat /etc/nginx/sites-enabled/bpsegurosimediato.com.br | grep -n "location" | head -10
```

**Ordem esperada (correta):**
```
1. location ~ \.php$           # Regex - alta prioridade
2. location /logging_system/   # Prefixo
3. location ~ ^/(logs|...)     # Regex - alta prioridade
4. location ~ ^/webhooks/.*\.(js|css)$  # Regex - alta prioridade (ANTES do catch-all)
5. location /dev/webhooks/      # Prefixo
6. location /                   # Prefixo simples - BAIXA prioridade (catch-all para Botpress)
```

**✅ Ordem correta garante:**
- Requisições `/webhooks/*.js` fazem match no location block específico (regex) ANTES do `location /` (catch-all)
- Botpress só recebe requisições que não fizeram match nos outros location blocks

---

### **FASE 4: APLICAÇÃO**

#### 4.1. Recarregar Nginx (sem downtime)
```bash
# Recarregar configuração sem parar o serviço
nginx -s reload

# OU usando systemctl
systemctl reload nginx
```

**Resultado esperado:**
- ✅ Nginx recarregado com sucesso
- ✅ Serviço continua rodando
- ✅ Sem downtime

#### 4.2. Verificar status do Nginx
```bash
# Verificar status
systemctl status nginx --no-pager | head -10

# Verificar processos
ps aux | grep nginx | grep -v grep
```

**Resultado esperado:**
- ✅ Nginx está rodando
- ✅ Processos ativos

---

### **FASE 5: TESTE E VALIDAÇÃO**

#### 5.1. Testar acesso HTTP local (do servidor)
```bash
# Testar via curl local
curl -I http://localhost/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js

# OU via HTTPS local
curl -I -k https://localhost/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
```

**Resultado esperado:**
```
HTTP/1.1 200 OK
Content-Type: application/javascript
Cache-Control: public, max-age=3600
Content-Length: 75864
```

#### 5.2. Testar acesso HTTP público
```bash
# Testar via curl externo
curl -I https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
```

**Resultado esperado:**
```
HTTP/2 200
content-type: application/javascript
cache-control: public, max-age=3600
content-length: 75864
server: nginx  ← NÃO deve ter "x-powered-by: Botpress"
```

#### 5.3. Verificar logs do Nginx
```bash
# Verificar log de acesso (últimas 5 linhas)
tail -5 /var/log/nginx/access.log

# Verificar log de erros (últimas 5 linhas)
tail -5 /var/log/nginx/error.log
```

**Resultado esperado:**
- ✅ Log de acesso mostra 200 OK para a requisição
- ✅ Sem erros no log de erros

#### 5.4. Verificar que Botpress continua operacional (se necessário)
```bash
# Testar se Botpress ainda está acessível (para outras rotas)
curl -I http://127.0.0.1:3000/

# Verificar processo do Botpress
ps aux | grep -i botpress | grep -v grep
```

**Resultado esperado:**
- ✅ Botpress continua rodando (se ainda for necessário)
- ✅ Botpress não recebe requisições de `/webhooks/*.js` (que é o esperado)

---

## 🔄 PLANO DE REVERSÃO (ROLLBACK)

Se algo der errado, seguir estes passos:

### **Reversão Rápida**

```bash
# 1. Remover symlink (se foi criado)
rm /etc/nginx/sites-enabled/bpsegurosimediato.com.br

# 2. Restaurar backup
cp /root/nginx_backups/YYYYMMDD_HHMMSS/bpsegurosimediato.com.br.enabled.backup \
   /etc/nginx/sites-enabled/bpsegurosimediato.com.br

# 3. Testar sintaxe
nginx -t

# 4. Recarregar Nginx
nginx -s reload
```

### **Verificação pós-reversão**

```bash
# Verificar que voltou ao estado anterior
curl -I https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
# Deve voltar a dar 404 (estado anterior)
```

---

## 📊 ORDEM DE PRECEDÊNCIA DOS LOCATION BLOCKS (NGINX)

Após a correção, a ordem de avaliação será:

| Prioridade | Tipo | Location Block | Match para `/webhooks/file.js` |
|------------|------|----------------|-------------------------------|
| **1ª** | Regex (`~`) | `location ~ \.php$` | ❌ Não |
| **2ª** | Prefixo | `location /logging_system/` | ❌ Não |
| **3ª** | Regex (`~`) | `location ~ ^/(logs\|...)` | ❌ Não |
| **4ª** | Regex (`~`) | `location ~ ^/webhooks/.*\.(js\|css)$` | ✅ **SIM** |
| **5ª** | Prefixo | `location /dev/webhooks/` | ❌ Não |
| **6ª** | Prefixo (`/`) | `location /` | ❌ Não avaliado (já matchou no 4) |

**✅ Garantia:** Como regex tem prioridade sobre prefixo simples, o location block específico será avaliado ANTES do catch-all.

---

## 🎯 RESULTADO ESPERADO

### **Antes da correção:**
```
GET /webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
  → 404 (Botpress)
```

### **Após a correção:**
```
GET /webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
  → 200 OK (Nginx serve diretamente)
  → Content-Type: application/javascript
  → Cache-Control: public, max-age=3600
```

---

## ⚠️ RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Sintaxe incorreta quebrar Nginx | Baixa | Alto | ✅ Testar com `nginx -t` antes de reload |
| Arquivo não acessível após correção | Baixa | Médio | ✅ Verificar permissões e caminho |
| Botpress parar de funcionar | Muito Baixa | Baixo | ✅ Botpress não será modificado, apenas ignorado para webhooks |
| Downtime durante correção | Muito Baixa | Médio | ✅ Usar `nginx -s reload` (sem parar serviço) |

---

## ✅ CHECKLIST DE EXECUÇÃO

### **Pré-Execução**
- [ ] Backup criado (`/root/nginx_backups/`)
- [ ] Estado atual documentado
- [ ] Plano revisado

### **Execução**
- [ ] Arquivo físico removido (ou symlink criado)
- [ ] Symlink criado corretamente
- [ ] Sintaxe testada (`nginx -t`)
- [ ] Ordem dos location blocks verificada
- [ ] Nginx recarregado (`nginx -s reload`)

### **Pós-Execução**
- [ ] Teste local (curl localhost) → 200 OK
- [ ] Teste público (curl domínio) → 200 OK
- [ ] Logs verificados (sem erros)
- [ ] Botpress ainda operacional (se necessário)
- [ ] Arquivo JavaScript acessível no navegador

---

## 📝 NOTAS IMPORTANTES

### **Sobre o Botpress**
- Botpress **não será removido** nem modificado
- Botpress **não receberá** requisições para `/webhooks/*.js` (será ignorado para essas rotas)
- Botpress **continuará recebendo** outras requisições via `location /` (catch-all)
- Se Botpress não for mais necessário no futuro, pode ser removido sem impacto nesta correção

### **Sobre a Correção**
- ✅ Correção é **reversível** (backup criado)
- ✅ Correção é **sem downtime** (nginx -s reload)
- ✅ Correção segue **boas práticas** (symlink em sites-enabled)
- ✅ Correção **não afeta** outros serviços

---

## 🚀 PRÓXIMOS PASSOS APÓS CORREÇÃO

1. ✅ Monitorar logs por 24h
2. ✅ Verificar acesso aos arquivos JavaScript em produção
3. ✅ Confirmar que não há regressões
4. ✅ Documentar alteração no changelog do projeto

---

**Plano criado em:** 02/11/2025  
**Status:** 📋 PLANEJADO - Aguardando aprovação para execução  
**Tempo estimado de execução:** 5-10 minutos  
**Risco:** Baixo (com backup e validação prévia)



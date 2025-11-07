# CORREÇÃO NGINX WEBHOOKS - AGENDADA PARA EXECUÇÃO

**Status:** 📅 AGENDADA  
**Data de Planejamento:** 02/11/2025  
**Data Prevista de Execução:** Durante a semana (semana de 03-09/11/2025)

---

## 📋 RESUMO EXECUTIVO

### **Problema**
Arquivos JavaScript em `/webhooks/` retornam 404 porque a configuração ativa do Nginx não possui o location block necessário. Requisições estão sendo enviadas ao Botpress (que não tem os arquivos).

### **Solução**
Converter configuração em `sites-enabled` para symlink apontando para `sites-available` (que já possui a configuração correta com location block para webhooks).

### **Resultado Esperado**
Arquivos `/webhooks/*.js` passarão a retornar 200 OK, servidos diretamente pelo Nginx, ignorando o Botpress para essas rotas.

---

## 📄 DOCUMENTAÇÃO COMPLETA

**Plano Detalhado:**
- `02-DEVELOPMENT/PLANO_CORRECAO_NGINX_WEBHOOKS_IGNORAR_BOTPRESS.md`

**Análise do Problema:**
- `02-DEVELOPMENT/ANALISE_PROBLEMA_NGINX_JAVASCRIPT_404.md`

**Relatório da Análise:**
- `02-DEVELOPMENT/RELATORIO_ANALISE_NGINX_COMPLETO.txt`

**Script de Análise:**
- `02-DEVELOPMENT/ANALISE_NGINX_PRODUCAO.sh`

---

## 🚀 QUICK REFERENCE - COMANDOS PARA EXECUÇÃO

### **Passos Rápidos (Opção 1 - Symlink - Recomendado)**

```bash
# 1. Backup
mkdir -p /root/nginx_backups/$(date +%Y%m%d_%H%M%S)
cp /etc/nginx/sites-enabled/bpsegurosimediato.com.br /root/nginx_backups/$(date +%Y%m%d_%H%M%S)/backup.enabled
cp /etc/nginx/sites-available/bpsegurosimediato.com.br /root/nginx_backups/$(date +%Y%m%d_%H%M%S)/backup.available

# 2. Remover arquivo físico
rm /etc/nginx/sites-enabled/bpsegurosimediato.com.br

# 3. Criar symlink
ln -s /etc/nginx/sites-available/bpsegurosimediato.com.br /etc/nginx/sites-enabled/bpsegurosimediato.com.br

# 4. Validar sintaxe
nginx -t

# 5. Recarregar (sem downtime)
nginx -s reload

# 6. Testar
curl -I https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
```

### **Verificação Rápida**

```bash
# Verificar symlink
ls -la /etc/nginx/sites-enabled/bpsegurosimediato.com.br

# Verificar location block
cat /etc/nginx/sites-enabled/bpsegurosimediato.com.br | grep -A 10 "location.*webhooks"

# Verificar logs
tail -5 /var/log/nginx/access.log
tail -5 /var/log/nginx/error.log
```

### **Rollback Rápido (se necessário)**

```bash
# Restaurar backup mais recente
LATEST_BACKUP=$(ls -t /root/nginx_backups/ | head -1)
rm /etc/nginx/sites-enabled/bpsegurosimediato.com.br
cp /root/nginx_backups/$LATEST_BACKUP/backup.enabled /etc/nginx/sites-enabled/bpsegurosimediato.com.br
nginx -t && nginx -s reload
```

---

## ✅ CHECKLIST DE EXECUÇÃO

- [ ] Backup criado
- [ ] Arquivo físico removido
- [ ] Symlink criado
- [ ] Sintaxe validada (`nginx -t`)
- [ ] Nginx recarregado (`nginx -s reload`)
- [ ] Teste local (curl localhost) → 200 OK
- [ ] Teste público (curl domínio) → 200 OK
- [ ] Logs verificados
- [ ] Arquivo acessível no navegador

---

## 📊 CONTEXTO TÉCNICO

### **Situação Atual**
- Arquivo em `sites-enabled`: arquivo físico (não symlink)
- Arquivo em `sites-available`: possui location block correto
- Location block para webhooks: ❌ Ausente na configuração ativa
- Resultado: 404 (Botpress)

### **Após Correção**
- Arquivo em `sites-enabled`: symlink → `sites-available`
- Location block para webhooks: ✅ Presente
- Ordem de precedência: regex `~ ^/webhooks/` avaliado ANTES de `location /`
- Resultado: 200 OK (Nginx serve diretamente)

### **Botpress**
- Continua rodando (não será removido)
- Não recebe requisições de `/webhooks/*.js` (ignorado)
- Continua recebendo outras requisições via `location /`

---

## ⚠️ NOTAS IMPORTANTES

1. **Sem Downtime:** Usar `nginx -s reload` (não `restart`)
2. **Backup Automático:** Criar antes de qualquer alteração
3. **Validação Obrigatória:** Sempre executar `nginx -t` antes de reload
4. **Reversível:** Rollback documentado e testado

---

## 📞 REFERÊNCIAS

- **Servidor:** bpsegurosimediato.com.br (46.62.174.150)
- **Arquivo afetado:** `/var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js`
- **Configuração:** `/etc/nginx/sites-available/bpsegurosimediato.com.br`
- **Configuração ativa:** `/etc/nginx/sites-enabled/bpsegurosimediato.com.br`

---

**Última atualização:** 02/11/2025  
**Próxima ação:** Executar durante a semana conforme disponibilidade



# 📋 PLANO DE MIGRAÇÃO DOMÍNIO - RPA V4.0.1

## 🎯 **OBJETIVO DO PROJETO**

Migrar o ambiente RPA V4.0.1 que funcionava **100% até 30/09/2025** de endereço IP (`37.27.92.160`) para domínio (`rpaimediatoseguros.com.br`), mantendo toda a funcionalidade da versão 4.0.1 documentada como funcional.

---

## 📊 **ESTADO DO AMBIENTE - V4.0.1 (30/09/2025)**

### ✅ **SISTEMA FUNCIONANDO PERFEITAMENTE**
**Data**: 30 de Setembro de 2025 às 20:16:59  
**Status**: ✅ **100% IMPLEMENTADA E TESTADA**

### **🏗️ Arquitetura Funcionando:**

#### **1. Frontend**
- ✅ API REST completa funcionando
- ✅ Dashboard web responsivo operacional
- ✅ Monitoramento tempo real via polling
- ✅ Interface moderna com atualização automática

#### **2. Backend PHP**
- ✅ **Arquitetura Modular**: `Controllers/`, `Services/`, `Repositories/`
- ✅ **Endpoints REST**:
  - `/api/rpa/start` - Criar sessões
  - `/api/rpa/progress/{session_id}` - Monitoramento
  - `/api/rpa/health` - Health checks
  - `/api/rpa/status` - Status sistema
- ✅ **Execução concorrente**: Múltiplas sessões simultâneas
- ✅ **Progress tracking**: Em tempo real via JSON

#### **3. RPA Python**
- ✅ **15 telas executando** (100% de sucesso)
- ✅ **Playwright + Chromium headless**
- ✅ **Progress tracker**: `DatabaseProgressTracker`
- ✅ **Captura de estimativas**: Tela 4
- ✅ **Cálculo final**: Tela 15

#### **4. Infraestrutura**
- ✅ **Nginx**: Configuração correta para `/opt/imediatoseguros-rpa-v4/public`
- ✅ **PHP 8.3-FPM**: Funcionando via `fastcgi_pass`
- ✅ **Permissões**: `www-data:www-data` configuradas
- ✅ **Dependências**: `composer.lock` instalado

---

## 🔍 **ALTERAÇÕES REALIZADAS DEPOIS DE 30/09**

### ❌ **PROBLEMAS INTRODUZIDOS:**

#### **1. Implementação do Modal (modal_rpa_real.html)**
- **Data**: Após 30/09/2025
- **Motivo**: Testar integração via modal + JavaScript
- **Problema**: Assumiu necessidade de domínio para funcionar

#### **2. Alteração Nginx INCORRETA**
```nginx
# ❌ Configuração ANTIGA (funcionava 30/09)
server {
    root /opt/imediatoseguros-rpa-v4/public;
    location /api/ {
        try_files $uri $uri/ /index.php?$query_string;
    }
}

# ❌ Configuração NOVA (quebrou 30/09)
server {
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;  # ❌ PORTA INEXISTENTE!
    }
    location /ws/ {
        proxy_pass http://127.0.0.1:8080/;  # ❌ WEBSOCKET DESNECESSÁRIO!
    }
}
```

#### **3. Motivos da Alteração (INCORRETOS)**
- ❌ **HTTPS**: Assumiu necessidade de SSL para modal
- ❌ **WebSocket**: Assumiu necessidade de WebSocket para progress
- ❌ **Porta 8000**: Assumiu existência de microserviço

#### **4. Problemas Resultantes**
- ❌ **502 Bad Gateway**: Proxy para porta 8000 inexistente
- ❌ **Sistema quebrado**: RPA V4 não funciona mais
- ❌ **Modal falhando**: JavaScript não consegue fazer chamadas API

---

## 🎯 **ESTADO ATUAL DO SISTEMA**

### ❌ **SISTEMA ATUALMENTE QUEBRADO**

#### **1. Problemas de Conectividade**
```bash
# ❌ Teste atual falha
curl https://rpaimediatoseguros.com.br/api/rpa/health
# Resultado: 502 Bad Gateway
```

#### **2. Configuração Incorreta**
- ❌ **Nginx**: Proxy para `127.0.0.1:8000` (serviço inexistente)
- ❌ **Arquivos V4**: Presentes em `/opt/imediatoseguros-rpa-v4/` mas não utilizados
- ❌ **Diretório vazio**: `/var/www/rpaimediatoseguros.com.br/api/` sem conteúdo

#### **3. Serviços**
- ✅ **PHP 8.3-FPM**: Funcionando
- ✅ **Nginx**: Funcionando mas mal configurado
- ✅ **DNS**: `rpaimediatoseguros.com.br` válido (`37.27.92.160`)
- ❌ **Serviço porta 8000**: Inexistente

---

## 🎯 **OBJETIVOS DO PROJETO**

### **OBJETIVO PRIMÁRIO**
Restaurar funcionalidade V4.0.1 mas utilizando **domínio** ao invés de **IP**

### **OBJETIVOS ESPECÍFICOS**

#### **1. Restaurar Funcionalidade V4.0.1**
- ✅ Reverter configuração Nginx para estado de 30/09
- ✅ Manter arquitetura modular funcionando
- ✅ Preservar todos os endpoints REST

#### **2. Implementar Domínio**
- ✅ Configurar SSL/HTTPS para `rpaimediatoseguros.com.br`
- ✅ Migrar testes de `37.27.92.160` para domínio
- ✅ Manter compatibilidade total com V4.0.1

#### **3. Validar Funcionamento**
- ✅ Reproduzir testes que funcionavam em 30/09
- ✅ Confirmar execução das 15 telas
- ✅ Confirmar progress tracking
- ✅ Confirmar captura de estimativas

---

## 📋 **PLANO DE EXECUÇÃO**

### **FASE 1: DIAGNÓSTICO E BACKUP** ⏱️ 5 minutos
```bash
# 1. Backup configuração atual (para rollback)
# 2. Verificar estado atual vs estado esperado
# 3. Confirmar arquivos V4 presentes
```

### **FASE 2: CORREÇÃO NGINX** ⏱️ 10 minutos
```bash
# 1. Restaurar configuração V4 funcionando
# 2. Remover proxy_pass para porta 8000
# 3. Configurar root para /opt/imediatoseguros-rpa-v4/public
# 4. Configurar fastcgi_pass para PHP-FPM
```

### **FASE 3: SSL/HTTPS** ⏱️ 15 minutos
```bash
# 1. Instalar certificado SSL (Let's Encrypt)
# 2. Configurar redirecionamento HTTP→HTTPS
# 3. Testar HTTPS funcionando
```

### **FASE 4: VALIDAÇÃO E TESTES** ⏱️ 20 minutos
```bash
# 1. Health check via domínio
# 2. Teste criação de sessão
# 3. Teste progress tracking
# 4. Reproduzir testes completos V4.0.1
```

---

## 📊 **RESULTADO FINAL ESPERADO**

### ✅ **FUNCIONALIDADES VALIDADAS**

#### **1. API REST funcionando via HTTPS**
```bash
# ✅ Health check
curl https://rpaimediatoseguros.com.br/api/rpa/health
# Resposta esperada: {"status": "healthy", "timestamp": "...", ...}

# ✅ Criação de sessão
curl -X POST https://rpaimediatoseguros.com.br/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"teste": "dados"}'
# Resposta esperada: {"success": true, "session_id": "rpa_v4_...", ...}

# ✅ Progress tracking
curl https://rpaimediatoseguros.com.br/api/rpa/progress/{session_id}
# Resposta esperada: {"etapa_atual": 7, "percentual": 46.7, ...}
```

#### **2. RPA V4 Executando 15 Telas**
- ✅ **Tela 1**: Seleção de Carro
- ✅ **Tela 2**: Inserção de Placa
- ✅ **Tela 3**: Confirmação de Veículo
- ✅ **Tela 4**: Status de Seguro **(Captura estimativas)**
- ✅ **Tela 5**: Carregamento de Estimativa
- ✅ **Tela 6**: Configuração de Combustível
- ✅ **Tela 7**: Preenchimento de CEP
- ✅ **Tela 8**: Seleção de Uso
- ✅ **Tela 9**: Dados Pessoais
- ✅ **Tela 10**: Condutor Principal
- ✅ **Tela 11**: Atividade do Veículo
- ✅ **Tela 12**: Garagem na Residência
- ✅ **Tela 13**: Residência com Menores
- ✅ **Tela 14**: Corretor Anterior
- ✅ **Tela 15**: Resultado Final **(Cálculo final)**

#### **3. Progress Tracking Funcionando**
- ✅ **execução_concorrente**: Múltiplas sessões simultâneas
- ✅ **monitoramento_tempo_real**: Polling a cada 2 segundos
- ✅ **captura_estimativas**: Tela 4 com valores dos planos
- ✅ **calculo_final**: Tela 15 com resultado completo

#### **4. Compatibilidade Total**
- ✅ **Parametros.json**: Funcionando como antes
- ✅ **Progress tracker**: JSON incremental funcionando
- ✅ **Logs estruturados**: Sistema completo funcionando
- ✅ **Permissões**: www-data configuradas corretamente

---

## ⚠️ **RISCOS E MITIGAÇÕES**

### **ALTO RISCO**
- **QUEBRA DO SISTEMA**: Rollback para backup se configuração estiver incorreta

### **MÉDIO RISCO**
- **SSL EXPIRA**: Certificado Let's Encrypt precisa renovação automática
- **DNS**: Manter domínio apontando para IP correto

### **BAIXO RISCO**
- **PERMISSÕES**: Já configuradas corretamente no V4
- **COMPATIBILIDADE**: Arquivos V4 mantidos intactos

---

## 🔄 **ROLLBACK PLAN**

### **Se algo der errado:**
```bash
# 1. Restaurar backup
cp /etc/nginx/sites-available/rpaimediatoseguros.com.br.backup /etc/nginx/sites-available/rpaimediatoseguros.com.br

# 2. Recarregar Nginx
systemctl reload nginx

# 3. Retomar uso de IP
curl http://37.27.92.160/api/rpa/health
```

---

## 📈 **CRITÉRIOS DE SUCESSO**

### **✅ VALIDAÇÃO PRIMÁRIA**
1. **Health check** retornando HTTP 200 OK
2. **Criação de sessão** retornando session_id válido
3. **Progress tracking** atualizando incrementalmente

### **✅ VALIDAÇÃO SECUNDÁRIA**
1. **Execução RPA** das 15 telas completas
2. **Captura estimativas** na Tela 4
3. **Cálculo final** na Tela 15
4. **Tempo execução** < 5 minutos

### **✅ VALIDAÇÃO FINAL**
1. **Reproduzir testes** que funcionavam em 30/09
2. **Sistema estável** por 24h
3. **Logs limpos** sem erros críticos

---

## 📝 **DOCUMENTAÇÃO PÓS-IMPLEMENTAÇÃO**

### **Arquivos a atualizar:**
- ✅ `ARQUITETURA_SOLUCAO_RPA_V4.md`
- ✅ `nginx_rpa_v4_config.conf`
- ✅ URLs hardcoded para domínio
- ✅ Certificados SSL configurados

### **Monitoramento:**
- ✅ Logs Nginx (/var/log/nginx/)
- ✅ Logs PHP (sistema logs/)
- ✅ Logs RPA (/opt/imediatoseguros-rpa/logs/)

---

## 🎯 **ESTADO FINAL ESPERADO**

**ANTES (Problema atual):**
- ❌ `37.27.92.160/api/rpa/health` → IP hardcoded
- ❌ Proxy para porta 8000 inexistente → 502 Bad Gateway
- ❌ Sistema V4 quebrado → Modal falhando

**DEPOIS (Solução):**
- ✅ `https://rpaimediatoseguros.com.br/api/rpa/health` → Domínio SSL
- ✅ Configuração V4 restaurada → Funcionalidade 30/09
- ✅ Sistema funcionando → Testes completos via domínio

---

**Status**: 📋 **PLANO PRONTO PARA ANÁLISE DO ENGENHEIRO**  
**Tempo total estimado**: ~50 minutos  
**Prioridade**: 🔥 **ALTA** - Sistema V4 quebrado aguardando correção  
**Dependências**: Acesso SSH ao Hetzner, certificado SSL, DNS funcionando  
**Resultado**: Sistema V4.0.1 funcionando via domínio ao invés de IP

---

## 🛠️ **COMANDOS PRONTOS PARA EXECUÇÃO**

### **Comandos críticos:**
```bash
# Backup
cp /etc/nginx/sites-available/rpaimediatoseguros.com.br /etc/nginx/sites-available/rpaimediatoseguros.com.br.backup

# Verificar DNS
nslookup rpaimediatoseguros.com.br

# Instalar SSL
certbot --nginx -d rpaimediatoseguros.com.br -d www.rpaimediatoseguros.com.br

# Testes
curl https://rpaimediatoseguros.com.br/api/rpa/health
```

**Arquivo**: `PLANO_MIGRACAO_DOMINIO_V4_RPA.md`  
**Versão**: 1.0  
**Data**: 03/10/2025  
**Autor**: Análise Engenharia de Software

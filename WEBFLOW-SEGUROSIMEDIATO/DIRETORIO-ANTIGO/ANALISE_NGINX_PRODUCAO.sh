#!/bin/bash

###############################################################################
# SCRIPT DE ANÁLISE PROFUNDA - NGINX E AMBIENTE WEB
# Objetivo: Investigar por que arquivos JavaScript não são acessíveis em produção
# Ambiente: bpsegurosimediato.com.br
# Data: 02/11/2025
###############################################################################

set -euo pipefail

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Arquivo de relatório
REPORT_FILE="/tmp/nginx_analysis_report_$(date +%Y%m%d_%H%M%S).txt"
DOMAIN="bpsegurosimediato.com.br"
WEBHOOKS_DIR="/var/www/html/webhooks"
DEV_WEBHOOKS_DIR="/var/www/html/dev/webhooks"
TARGET_JS_FILE="FooterCodeSiteDefinitivoCompleto_prod.js"

echo "================================================================================"
echo "ANÁLISE PROFUNDA - NGINX E AMBIENTE WEB - PRODUÇÃO"
echo "Domínio: $DOMAIN"
echo "Data: $(date)"
echo "================================================================================"
echo ""

###############################################################################
# FUNÇÃO: LOG DE SEÇÃO
###############################################################################
log_section() {
    echo ""
    echo "================================================================================"
    echo -e "${BLUE}$1${NC}"
    echo "================================================================================"
    echo ""
}

###############################################################################
# FUNÇÃO: LOG DE INFORMAÇÃO
###############################################################################
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1" | tee -a "$REPORT_FILE"
}

###############################################################################
# FUNÇÃO: LOG DE AVISO
###############################################################################
log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$REPORT_FILE"
}

###############################################################################
# FUNÇÃO: LOG DE ERRO
###############################################################################
log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$REPORT_FILE"
}

###############################################################################
# SEÇÃO 1: INFORMAÇÕES DO SISTEMA
###############################################################################
log_section "1. INFORMAÇÕES DO SISTEMA"

log_info "Sistema Operacional: $(lsb_release -d 2>/dev/null | cut -f2 || uname -a)"
log_info "Kernel: $(uname -r)"
log_info "Arquitetura: $(uname -m)"
log_info "Usuário atual: $(whoami)"
log_info "UID: $(id -u)"
log_info "Grupos: $(groups)"

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 2: VERIFICAÇÃO DO NGINX
###############################################################################
log_section "2. STATUS E VERSÃO DO NGINX"

if command -v nginx &> /dev/null; then
    NGINX_VERSION=$(nginx -v 2>&1)
    log_info "Nginx instalado: $NGINX_VERSION"
    
    if systemctl is-active --quiet nginx; then
        log_info "Status: Nginx está RODANDO"
        NGINX_STATUS=$(systemctl status nginx --no-pager -l | head -5)
        echo "$NGINX_STATUS" | tee -a "$REPORT_FILE"
    else
        log_error "Nginx NÃO está rodando!"
    fi
    
    log_info "PID do processo principal: $(pgrep -f 'nginx: master process' || echo 'NÃO ENCONTRADO')"
    log_info "Processos Nginx ativos: $(pgrep -f nginx | wc -l)"
else
    log_error "Nginx NÃO está instalado!"
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 3: CONFIGURAÇÃO DO NGINX
###############################################################################
log_section "3. ANÁLISE DE CONFIGURAÇÃO DO NGINX"

NGINX_CONFIG_DIR="/etc/nginx"
SITES_AVAILABLE="$NGINX_CONFIG_DIR/sites-available"
SITES_ENABLED="$NGINX_CONFIG_DIR/sites-enabled"

log_info "Diretório de configuração: $NGINX_CONFIG_DIR"
log_info "Configurações disponíveis: $SITES_AVAILABLE"
log_info "Configurações habilitadas: $SITES_ENABLED"

# Verificar arquivo de configuração do domínio
DOMAIN_CONFIG="$SITES_AVAILABLE/$DOMAIN"
log_info "Procurando configuração em: $DOMAIN_CONFIG"

if [ -f "$DOMAIN_CONFIG" ]; then
    log_info "✅ Arquivo de configuração encontrado: $DOMAIN_CONFIG"
    
    # Verificar se está habilitado (symlink)
    if [ -L "$SITES_ENABLED/$DOMAIN" ]; then
        log_info "✅ Configuração HABILITADA (symlink existe)"
    else
        log_warn "⚠️  Configuração NÃO está habilitada (sem symlink em sites-enabled)"
    fi
    
    # Analisar configuração
    log_info "Análise da configuração do servidor:"
    echo "---" | tee -a "$REPORT_FILE"
    
    # Extrair configurações relevantes
    log_info "Server blocks encontrados:"
    grep -n "server {" "$DOMAIN_CONFIG" | tee -a "$REPORT_FILE" || log_warn "Nenhum server block encontrado"
    
    log_info "Server names configurados:"
    grep -n "server_name" "$DOMAIN_CONFIG" | tee -a "$REPORT_FILE" || log_warn "Nenhum server_name encontrado"
    
    log_info "Location blocks para /webhooks/:"
    grep -A 10 "location.*webhooks" "$DOMAIN_CONFIG" | tee -a "$REPORT_FILE" || log_warn "Nenhum location block para webhooks encontrado"
    
    log_info "Location blocks para arquivos estáticos (.js, .css):"
    grep -A 10 "location.*\.(js\|css)" "$DOMAIN_CONFIG" | tee -a "$REPORT_FILE" || log_warn "Nenhum location block para .js/.css encontrado"
    
    log_info "Root directives:"
    grep -n "root\|alias" "$DOMAIN_CONFIG" | tee -a "$REPORT_FILE" || log_warn "Nenhum root/alias encontrado"
    
    log_info "Try files directives:"
    grep -n "try_files" "$DOMAIN_CONFIG" | tee -a "$REPORT_FILE" || log_warn "Nenhum try_files encontrado"
    
    log_info "Proxy pass directives:"
    grep -n "proxy_pass" "$DOMAIN_CONFIG" | tee -a "$REPORT_FILE" || log_warn "Nenhum proxy_pass encontrado"
    
else
    log_error "❌ Arquivo de configuração NÃO encontrado: $DOMAIN_CONFIG"
    log_info "Listando arquivos em sites-available:"
    ls -la "$SITES_AVAILABLE" | tee -a "$REPORT_FILE"
fi

echo "" | tee -a "$REPORT_FILE"

# Verificar sintaxe do Nginx
log_info "Testando sintaxe da configuração do Nginx:"
if nginx -t 2>&1 | tee -a "$REPORT_FILE"; then
    log_info "✅ Sintaxe do Nginx está CORRETA"
else
    log_error "❌ ERRO na sintaxe do Nginx!"
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 4: VERIFICAÇÃO DE ARQUIVOS E DIRETÓRIOS
###############################################################################
log_section "4. VERIFICAÇÃO DE ARQUIVOS E DIRETÓRIOS"

log_info "Verificando diretório de produção: $WEBHOOKS_DIR"
if [ -d "$WEBHOOKS_DIR" ]; then
    log_info "✅ Diretório existe"
    log_info "Permissões: $(stat -c '%a %U:%G' "$WEBHOOKS_DIR")"
    log_info "Proprietário: $(stat -c '%U:%G' "$WEBHOOKS_DIR")"
    
    log_info "Conteúdo do diretório:"
    ls -lah "$WEBHOOKS_DIR" | tee -a "$REPORT_FILE"
    
    # Verificar arquivo específico
    TARGET_FILE="$WEBHOOKS_DIR/$TARGET_JS_FILE"
    log_info "Verificando arquivo específico: $TARGET_FILE"
    if [ -f "$TARGET_FILE" ]; then
        log_info "✅ Arquivo EXISTE"
        log_info "Tamanho: $(stat -c '%s' "$TARGET_FILE") bytes"
        log_info "Permissões: $(stat -c '%a %U:%G' "$TARGET_FILE")"
        log_info "Proprietário: $(stat -c '%U:%G' "$TARGET_FILE")"
        log_info "Tipo MIME: $(file -b --mime-type "$TARGET_FILE")"
        
        # Testar leitura
        if [ -r "$TARGET_FILE" ]; then
            log_info "✅ Arquivo é LEGÍVEL"
        else
            log_error "❌ Arquivo NÃO é legível!"
        fi
    else
        log_error "❌ Arquivo NÃO encontrado: $TARGET_FILE"
    fi
else
    log_error "❌ Diretório NÃO existe: $WEBHOOKS_DIR"
fi

echo "" | tee -a "$REPORT_FILE"

log_info "Verificando diretório DEV (funcional): $DEV_WEBHOOKS_DIR"
if [ -d "$DEV_WEBHOOKS_DIR" ]; then
    log_info "✅ Diretório DEV existe"
    log_info "Permissões: $(stat -c '%a %U:%G' "$DEV_WEBHOOKS_DIR")"
    
    DEV_TARGET_FILE="$DEV_WEBHOOKS_DIR/$TARGET_JS_FILE"
    if [ -f "$DEV_TARGET_FILE" ]; then
        log_info "✅ Arquivo existe em DEV: $DEV_TARGET_FILE"
        log_info "Permissões: $(stat -c '%a %U:%G' "$DEV_TARGET_FILE")"
    fi
fi

echo "" | tee -a "$REPORT_FILE"

# Verificar diretório raiz do webroot
NGINX_ROOT=$(grep -E "^\s*root\s+" "$DOMAIN_CONFIG" 2>/dev/null | head -1 | awk '{print $2}' | tr -d ';' || echo "/var/www/html")
log_info "Webroot configurado no Nginx: $NGINX_ROOT"

if [ -d "$NGINX_ROOT" ]; then
    log_info "✅ Diretório raiz existe"
    log_info "Permissões: $(stat -c '%a %U:%G' "$NGINX_ROOT")"
    log_info "Estrutura de diretórios:"
    find "$NGINX_ROOT" -maxdepth 3 -type d | head -20 | tee -a "$REPORT_FILE"
else
    log_error "❌ Diretório raiz NÃO existe: $NGINX_ROOT"
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 5: PERMISSÕES E PROPRIETÁRIO
###############################################################################
log_section "5. ANÁLISE DE PERMISSÕES E PROPRIETÁRIO"

# Verificar usuário/grupo do Nginx
NGINX_USER=$(ps aux | grep 'nginx: worker process' | head -1 | awk '{print $1}' || grep -E "^user\s+" "$NGINX_CONFIG_DIR/nginx.conf" | awk '{print $2}' | tr -d ';' || echo "www-data")
log_info "Usuário do Nginx (worker): $NGINX_USER"

NGINX_GROUP=$(id -gn "$NGINX_USER" 2>/dev/null || echo "www-data")
log_info "Grupo do Nginx: $NGINX_GROUP"

# Verificar se o Nginx pode ler os arquivos
if [ -d "$WEBHOOKS_DIR" ]; then
    log_info "Testando acesso do Nginx ao diretório:"
    
    # Verificar permissões do diretório
    DIR_PERMS=$(stat -c '%a' "$WEBHOOKS_DIR")
    DIR_OWNER=$(stat -c '%U' "$WEBHOOKS_DIR")
    DIR_GROUP=$(stat -c '%G' "$WEBHOOKS_DIR")
    
    log_info "Diretório: perms=$DIR_PERMS, owner=$DIR_OWNER, group=$DIR_GROUP"
    
    if [ "$DIR_OWNER" = "$NGINX_USER" ] || [ "$DIR_GROUP" = "$NGINX_GROUP" ]; then
        log_info "✅ Proprietário/grupo compatível com Nginx"
    else
        log_warn "⚠️  Proprietário/grupo pode estar incompatível com Nginx"
    fi
    
    # Verificar se Nginx pode acessar (teste com sudo se possível)
    if sudo -u "$NGINX_USER" test -r "$WEBHOOKS_DIR" 2>/dev/null; then
        log_info "✅ Nginx pode LER o diretório"
    else
        log_error "❌ Nginx NÃO pode ler o diretório!"
    fi
    
    if sudo -u "$NGINX_USER" test -x "$WEBHOOKS_DIR" 2>/dev/null; then
        log_info "✅ Nginx pode ENTRAR no diretório (executar)"
    else
        log_error "❌ Nginx NÃO pode entrar no diretório!"
    fi
fi

# Verificar arquivo específico
if [ -f "$WEBHOOKS_DIR/$TARGET_JS_FILE" ]; then
    FILE_PERMS=$(stat -c '%a' "$WEBHOOKS_DIR/$TARGET_JS_FILE")
    FILE_OWNER=$(stat -c '%U' "$WEBHOOKS_DIR/$TARGET_JS_FILE")
    
    log_info "Arquivo: perms=$FILE_PERMS, owner=$FILE_OWNER"
    
    if sudo -u "$NGINX_USER" test -r "$WEBHOOKS_DIR/$TARGET_JS_FILE" 2>/dev/null; then
        log_info "✅ Nginx pode LER o arquivo"
    else
        log_error "❌ Nginx NÃO pode ler o arquivo!"
    fi
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 6: TESTE DE ACESSO HTTP
###############################################################################
log_section "6. TESTE DE ACESSO HTTP"

JS_URL="https://$DOMAIN/webhooks/$TARGET_JS_FILE"
log_info "Testando acesso HTTP a: $JS_URL"

# Teste com curl
if command -v curl &> /dev/null; then
    log_info "Fazendo requisição HTTP com curl:"
    HTTP_RESPONSE=$(curl -I -s -w "\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}\n" "$JS_URL" 2>&1 || echo "ERROR")
    
    if echo "$HTTP_RESPONSE" | grep -q "HTTP_CODE:200"; then
        log_info "✅ Arquivo ACESSÍVEL via HTTP (200 OK)"
    elif echo "$HTTP_RESPONSE" | grep -q "HTTP_CODE:404"; then
        log_error "❌ Arquivo retorna 404 (NOT FOUND)"
    elif echo "$HTTP_RESPONSE" | grep -q "HTTP_CODE:403"; then
        log_error "❌ Arquivo retorna 403 (FORBIDDEN)"
    else
        log_warn "⚠️  Resposta HTTP inesperada"
    fi
    
    echo "$HTTP_RESPONSE" | tee -a "$REPORT_FILE"
else
    log_warn "curl não está instalado, pulando teste HTTP"
fi

echo "" | tee -a "$REPORT_FILE"

# Comparar com diretório DEV que funciona
DEV_JS_URL="https://dev.$DOMAIN/webhooks/$TARGET_JS_FILE"
log_info "Comparando com DEV (que funciona): $DEV_JS_URL"

if command -v curl &> /dev/null; then
    DEV_HTTP_CODE=$(curl -I -s -o /dev/null -w "%{http_code}" "$DEV_JS_URL" 2>&1 || echo "ERROR")
    log_info "DEV HTTP Code: $DEV_HTTP_CODE"
    
    if [ "$DEV_HTTP_CODE" = "200" ]; then
        log_info "✅ DEV está funcionando (200 OK)"
    fi
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 7: LOGS DO NGINX
###############################################################################
log_section "7. ANÁLISE DE LOGS DO NGINX"

NGINX_ERROR_LOG="/var/log/nginx/error.log"
NGINX_ACCESS_LOG="/var/log/nginx/access.log"

log_info "Verificando logs do Nginx:"

if [ -f "$NGINX_ERROR_LOG" ]; then
    log_info "✅ Log de erros encontrado: $NGINX_ERROR_LOG"
    log_info "Últimas 20 linhas do log de erros relacionadas a webhooks:"
    grep -i "webhooks\|$TARGET_JS_FILE\|404\|403\|permission" "$NGINX_ERROR_LOG" 2>/dev/null | tail -20 | tee -a "$REPORT_FILE" || log_info "Nenhuma entrada relevante encontrada"
else
    log_warn "⚠️  Log de erros não encontrado: $NGINX_ERROR_LOG"
fi

if [ -f "$NGINX_ACCESS_LOG" ]; then
    log_info "✅ Log de acesso encontrado: $NGINX_ACCESS_LOG"
    log_info "Últimas 10 requisições para /webhooks/:"
    grep "/webhooks/" "$NGINX_ACCESS_LOG" 2>/dev/null | tail -10 | tee -a "$REPORT_FILE" || log_info "Nenhuma requisição encontrada"
    
    log_info "Requisições 404 para webhooks:"
    grep "404.*webhooks" "$NGINX_ACCESS_LOG" 2>/dev/null | tail -10 | tee -a "$REPORT_FILE" || log_info "Nenhum 404 encontrado"
else
    log_warn "⚠️  Log de acesso não encontrado: $NGINX_ACCESS_LOG"
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 8: SELINUX / APPARMOR
###############################################################################
log_section "8. VERIFICAÇÃO DE SELINUX/APPARMOR"

# SELinux
if command -v getenforce &> /dev/null; then
    SELINUX_STATUS=$(getenforce 2>/dev/null || echo "N/A")
    log_info "Status SELinux: $SELINUX_STATUS"
    
    if [ "$SELINUX_STATUS" != "Disabled" ]; then
        log_warn "⚠️  SELinux está ATIVO - pode estar bloqueando acesso"
        
        # Verificar contexto dos arquivos
        if command -v ls -Z &> /dev/null && [ -d "$WEBHOOKS_DIR" ]; then
            log_info "Contexto SELinux do diretório:"
            ls -Zd "$WEBHOOKS_DIR" 2>/dev/null | tee -a "$REPORT_FILE" || log_warn "Não foi possível verificar contexto"
        fi
    else
        log_info "✅ SELinux está desabilitado"
    fi
else
    log_info "SELinux não está instalado/configurado"
fi

# AppArmor
if command -v aa-status &> /dev/null; then
    log_info "AppArmor está instalado"
    APPARMOR_STATUS=$(aa-status 2>/dev/null | head -1 || echo "N/A")
    log_info "Status AppArmor: $APPARMOR_STATUS"
else
    log_info "AppArmor não está instalado/configurado"
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 9: FIREWALL E REDE
###############################################################################
log_section "9. VERIFICAÇÃO DE FIREWALL E REDE"

# UFW
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(ufw status | head -1 || echo "N/A")
    log_info "Status UFW: $UFW_STATUS"
    
    if echo "$UFW_STATUS" | grep -q "active"; then
        log_info "Regras UFW:"
        ufw status numbered | tee -a "$REPORT_FILE" || log_warn "Não foi possível listar regras"
    fi
else
    log_info "UFW não está instalado"
fi

# iptables
if command -v iptables &> /dev/null; then
    log_info "Verificando regras iptables relevantes (porta 80/443):"
    iptables -L -n -v | grep -E "80|443|ACCEPT|REJECT|DROP" | head -10 | tee -a "$REPORT_FILE" || log_info "Nenhuma regra relevante encontrada"
fi

# Verificar se porta está escutando
log_info "Portas em escuta relacionadas ao Nginx:"
netstat -tlnp 2>/dev/null | grep -E ":80|:443" | grep nginx | tee -a "$REPORT_FILE" || \
ss -tlnp 2>/dev/null | grep -E ":80|:443" | grep nginx | tee -a "$REPORT_FILE" || \
log_info "Nenhuma porta encontrada (ou comando não disponível)"

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 10: COMPARAÇÃO COM CONFIGURAÇÃO QUE FUNCIONA (DEV)
###############################################################################
log_section "10. COMPARAÇÃO COM CONFIGURAÇÃO DEV (QUE FUNCIONA)"

DEV_CONFIG="$SITES_AVAILABLE/dev.$DOMAIN"
if [ -f "$DEV_CONFIG" ]; then
    log_info "✅ Configuração DEV encontrada: $DEV_CONFIG"
    
    log_info "Location blocks para /dev/webhooks/ na configuração DEV:"
    grep -A 15 "location.*dev/webhooks" "$DEV_CONFIG" | tee -a "$REPORT_FILE" || log_warn "Nenhum location block encontrado"
    
    log_info "Diferenças relevantes entre PROD e DEV:"
    echo "--- PRODUÇÃO ---" | tee -a "$REPORT_FILE"
    grep -A 10 "location.*webhooks" "$DOMAIN_CONFIG" 2>/dev/null | tee -a "$REPORT_FILE" || echo "Nenhum location block para webhooks" | tee -a "$REPORT_FILE"
    
    echo "--- DEV ---" | tee -a "$REPORT_FILE"
    grep -A 10 "location.*dev/webhooks" "$DEV_CONFIG" | tee -a "$REPORT_FILE" || echo "Nenhum location block para dev/webhooks" | tee -a "$REPORT_FILE"
else
    log_warn "⚠️  Configuração DEV não encontrada para comparação"
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# SEÇÃO 11: ANÁLISE DE PATH E RESOLUÇÃO
###############################################################################
log_section "11. ANÁLISE DE PATH E RESOLUÇÃO"

log_info "Analisando como o Nginx resolve o caminho /webhooks/$TARGET_JS_FILE:"

# Extrair root do server block relevante
if [ -f "$DOMAIN_CONFIG" ]; then
    # Procurar server block que corresponde ao domínio
    log_info "Server block que corresponde a $DOMAIN:"
    
    # Tentar encontrar root directive dentro do server block correto
    SERVER_ROOT=$(grep -A 50 "server_name.*$DOMAIN" "$DOMAIN_CONFIG" | grep -E "^\s*root\s+" | head -1 | awk '{print $2}' | tr -d ';' || echo "")
    
    if [ -n "$SERVER_ROOT" ]; then
        log_info "Root do server block: $SERVER_ROOT"
        
        EXPECTED_PATH="$SERVER_ROOT/webhooks/$TARGET_JS_FILE"
        log_info "Caminho esperado (sem location blocks): $EXPECTED_PATH"
        
        if [ -f "$EXPECTED_PATH" ]; then
            log_info "✅ Arquivo EXISTE no caminho esperado"
        else
            log_error "❌ Arquivo NÃO existe no caminho esperado: $EXPECTED_PATH"
        fi
        
        # Verificar se há alias que sobrescreve
        ALIAS_PATH=$(grep -A 50 "server_name.*$DOMAIN" "$DOMAIN_CONFIG" | grep -E "location.*webhooks" -A 10 | grep -E "^\s*alias\s+" | head -1 | awk '{print $2}' | tr -d ';' || echo "")
        
        if [ -n "$ALIAS_PATH" ]; then
            log_info "Alias encontrado no location block: $ALIAS_PATH"
            ALIAS_FULL_PATH="$ALIAS_PATH/$TARGET_JS_FILE"
            log_info "Caminho com alias: $ALIAS_FULL_PATH"
            
            if [ -f "$ALIAS_FULL_PATH" ]; then
                log_info "✅ Arquivo EXISTE no caminho do alias"
            else
                log_error "❌ Arquivo NÃO existe no caminho do alias: $ALIAS_FULL_PATH"
            fi
        fi
    fi
fi

echo "" | tee -a "$REPORT_FILE"

###############################################################################
# RESUMO E CONCLUSÕES
###############################################################################
log_section "RESUMO E CONCLUSÕES"

echo "Análise concluída em: $(date)" | tee -a "$REPORT_FILE"
echo "Relatório completo salvo em: $REPORT_FILE" | tee -a "$REPORT_FILE"
echo ""
log_info "PRINCIPAIS PONTOS VERIFICADOS:"
echo "  ✅ Status do Nginx"
echo "  ✅ Configuração do Nginx (server blocks, location blocks)"
echo "  ✅ Existência e permissões de arquivos e diretórios"
echo "  ✅ Acesso HTTP (curl)"
echo "  ✅ Logs do Nginx (erros e acessos)"
echo "  ✅ SELinux/AppArmor"
echo "  ✅ Firewall (UFW/iptables)"
echo "  ✅ Comparação com configuração DEV (funcional)"
echo "  ✅ Resolução de caminhos (root/alias)"
echo ""
log_info "Relatório completo: $REPORT_FILE"
echo "================================================================================"



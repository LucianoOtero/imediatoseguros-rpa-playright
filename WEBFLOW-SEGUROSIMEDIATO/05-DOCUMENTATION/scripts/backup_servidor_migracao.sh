#!/bin/bash
# Script de Backup e Configuração para Migração Produção
# Data: 06/11/2025

echo "🚀 INICIANDO BACKUP E CONFIGURAÇÃO NO SERVIDOR"
echo "================================================"
echo ""

# Criar diretório de backup com timestamp
BACKUP_DIR="/root/backup_migracao_producao_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR
echo "✅ Diretório de backup criado: $BACKUP_DIR"
echo ""

# Backup arquivos JavaScript PROD (se existirem)
echo "📋 Criando backups dos arquivos PROD..."
if [ -f "/var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js" ]; then
  cp /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js $BACKUP_DIR/FooterCodeSiteDefinitivoCompleto_prod.js.backup
  echo "✅ Backup FooterCode PROD criado"
fi

if [ -f "/var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js" ]; then
  cp /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js $BACKUP_DIR/MODAL_WHATSAPP_DEFINITIVO_prod.js.backup
  echo "✅ Backup Modal PROD criado"
fi

# Backup arquivos PHP PROD (se existirem)
if [ -f "/var/www/html/webhooks/send_email_notification_endpoint_prod.php" ]; then
  cp /var/www/html/webhooks/send_email_notification_endpoint_prod.php $BACKUP_DIR/send_email_notification_endpoint_prod.php.backup
  echo "✅ Backup Email Endpoint PROD criado"
fi

if [ -f "/var/www/html/webhooks/add_flyingdonkeys_prod.php" ]; then
  cp /var/www/html/webhooks/add_flyingdonkeys_prod.php $BACKUP_DIR/add_flyingdonkeys_prod.php.backup
  echo "✅ Backup FlyingDonkeys PROD criado"
fi

if [ -f "/var/www/html/webhooks/add_webflow_octa_prod.php" ]; then
  cp /var/www/html/webhooks/add_webflow_octa_prod.php $BACKUP_DIR/add_webflow_octa_prod.php.backup
  echo "✅ Backup Octadesk PROD criado"
fi

# Backup também dos arquivos _v2.php (caso precisemos reverter)
if [ -f "/var/www/html/webhooks/add_flyingdonkeys_v2.php" ]; then
  cp /var/www/html/webhooks/add_flyingdonkeys_v2.php $BACKUP_DIR/add_flyingdonkeys_v2.php.backup
  echo "✅ Backup FlyingDonkeys V2 criado"
fi

if [ -f "/var/www/html/webhooks/add_webflow_octa_v2.php" ]; then
  cp /var/www/html/webhooks/add_webflow_octa_v2.php $BACKUP_DIR/add_webflow_octa_v2.php.backup
  echo "✅ Backup Octadesk V2 criado"
fi

echo ""
echo "📊 Verificando backups criados:"
ls -lh $BACKUP_DIR/
echo ""

# Verificar se diretório PROD existe e está acessível
echo "📋 Verificando estrutura do diretório PROD..."
if [ ! -d "/var/www/html/webhooks/" ]; then
  echo "⚠️ Diretório /var/www/html/webhooks/ não existe. Criando..."
  mkdir -p /var/www/html/webhooks/
  chmod 755 /var/www/html/webhooks/
  echo "✅ Diretório criado"
else
  echo "✅ Diretório /var/www/html/webhooks/ existe"
fi

echo ""
echo "✅ BACKUP CONCLUÍDO!"
echo "📁 Backups salvos em: $BACKUP_DIR"
echo ""


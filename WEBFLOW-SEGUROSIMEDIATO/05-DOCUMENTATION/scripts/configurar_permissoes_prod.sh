#!/bin/bash
# Script de Configuração de Permissões após Migração
# Data: 06/11/2025

echo "🔧 CONFIGURANDO PERMISSÕES DOS ARQUIVOS PROD"
echo "============================================="
echo ""

# Configurar permissões dos arquivos PROD
echo "📋 Configurando permissões..."
chmod 644 /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
chmod 644 /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js
chmod 644 /var/www/html/webhooks/send_email_notification_endpoint_prod.php
chmod 644 /var/www/html/webhooks/add_flyingdonkeys_prod.php
chmod 644 /var/www/html/webhooks/add_webflow_octa_prod.php

echo "✅ Permissões configuradas (644)"

# Verificar propriedade
echo ""
echo "📋 Configurando propriedade..."
chown www-data:www-data /var/www/html/webhooks/*.js 2>/dev/null
chown www-data:www-data /var/www/html/webhooks/*.php 2>/dev/null

echo "✅ Propriedade configurada (www-data:www-data)"

# Verificar arquivos copiados
echo ""
echo "📊 Arquivos no diretório PROD:"
ls -lh /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js 2>/dev/null || echo "⚠️ FooterCode PROD não encontrado"
ls -lh /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js 2>/dev/null || echo "⚠️ Modal PROD não encontrado"
ls -lh /var/www/html/webhooks/send_email_notification_endpoint_prod.php 2>/dev/null || echo "⚠️ Email Endpoint PROD não encontrado"
ls -lh /var/www/html/webhooks/add_flyingdonkeys_prod.php 2>/dev/null || echo "⚠️ FlyingDonkeys PROD não encontrado"
ls -lh /var/www/html/webhooks/add_webflow_octa_prod.php 2>/dev/null || echo "⚠️ Octadesk PROD não encontrado"

echo ""
echo "✅ CONFIGURAÇÃO DE PERMISSÕES CONCLUÍDA!"


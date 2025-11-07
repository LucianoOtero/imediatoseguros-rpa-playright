#!/bin/bash
# Script para copiar FooterCodeSiteDefinitivoCompleto.js para servidor
# Uso: Executar a partir do diretório raiz do projeto

SERVER="root@46.62.174.150"
REMOTE_PATH="/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js"
LOCAL_FILE="02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js"

echo "📤 Copiando arquivo unificado para servidor..."
echo "Origem: $LOCAL_FILE"
echo "Destino: $SERVER:$REMOTE_PATH"
echo ""

# Verificar se arquivo local existe
if [ ! -f "$LOCAL_FILE" ]; then
    echo "❌ ERRO: Arquivo local não encontrado: $LOCAL_FILE"
    exit 1
fi

# Criar backup no servidor (se arquivo já existir)
echo "📋 Criando backup no servidor (se existir)..."
ssh "$SERVER" "if [ -f $REMOTE_PATH ]; then cp $REMOTE_PATH ${REMOTE_PATH}.backup_$(date +%Y%m%d_%H%M%S); echo '✅ Backup criado'; fi"

# Copiar arquivo
echo "📤 Copiando arquivo..."
scp "$LOCAL_FILE" "$SERVER:$REMOTE_PATH"

if [ $? -eq 0 ]; then
    echo "✅ Arquivo copiado com sucesso!"
    echo ""
    echo "🔍 Verificações:"
    echo "1. Verificando arquivo no servidor..."
    ssh "$SERVER" "ls -lh $REMOTE_PATH"
    echo ""
    echo "2. Verificando tamanho..."
    ssh "$SERVER" "wc -c $REMOTE_PATH"
    echo ""
    echo "3. Testar URL:"
    echo "   https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js"
    echo ""
    echo "✅ Pronto para Fase 3 (Backup Webflow)!"
else
    echo "❌ ERRO ao copiar arquivo"
    exit 1
fi








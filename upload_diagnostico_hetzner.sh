#!/bin/bash

# SCRIPT PARA UPLOAD DOS ARQUIVOS DE DIAGNÓSTICO PARA O HETZNER
# AUTOR: Assistente IA
# DATA: 2025-09-28
# VERSÃO: 1.0.0

echo "🚀 UPLOAD DOS ARQUIVOS DE DIAGNÓSTICO PARA HETZNER"
echo "=================================================="

# Configurações do servidor
SERVER="37.27.92.160"
USER="root"
DEST_DIR="/opt/imediatoseguros-rpa"

# Verificar se os arquivos existem
echo "📋 Verificando arquivos locais..."
if [ ! -f "diagnostico_completo_hetzner.py" ]; then
    echo "❌ ERRO: diagnostico_completo_hetzner.py não encontrado"
    exit 1
fi

if [ ! -f "executar_diagnostico_hetzner.sh" ]; then
    echo "❌ ERRO: executar_diagnostico_hetzner.sh não encontrado"
    exit 1
fi

if [ ! -f "teste_progress_tracker.py" ]; then
    echo "❌ ERRO: teste_progress_tracker.py não encontrado"
    exit 1
fi

echo "✅ Todos os arquivos encontrados"

# Fazer upload dos arquivos
echo ""
echo "📤 Fazendo upload dos arquivos..."

echo "   Uploading diagnostico_completo_hetzner.py..."
scp diagnostico_completo_hetzner.py ${USER}@${SERVER}:${DEST_DIR}/

echo "   Uploading executar_diagnostico_hetzner.sh..."
scp executar_diagnostico_hetzner.sh ${USER}@${SERVER}:${DEST_DIR}/

echo "   Uploading teste_progress_tracker.py..."
scp teste_progress_tracker.py ${USER}@${SERVER}:${DEST_DIR}/

# Dar permissão de execução
echo ""
echo "🔧 Configurando permissões..."
ssh ${USER}@${SERVER} "chmod +x ${DEST_DIR}/executar_diagnostico_hetzner.sh"

# Verificar se os arquivos foram enviados
echo ""
echo "✅ Verificando upload..."
ssh ${USER}@${SERVER} "ls -la ${DEST_DIR}/diagnostico_completo_hetzner.py ${DEST_DIR}/executar_diagnostico_hetzner.sh ${DEST_DIR}/teste_progress_tracker.py"

echo ""
echo "🎯 PRÓXIMOS PASSOS:"
echo "==================="
echo "1. Conectar ao servidor:"
echo "   ssh ${USER}@${SERVER}"
echo ""
echo "2. Navegar para o diretório:"
echo "   cd ${DEST_DIR}"
echo ""
echo "3. Executar diagnóstico completo:"
echo "   ./executar_diagnostico_hetzner.sh"
echo ""
echo "4. Ou executar teste específico do ProgressTracker:"
echo "   python3 teste_progress_tracker.py"
echo ""
echo "5. Ou executar diagnóstico Python:"
echo "   python3 diagnostico_completo_hetzner.py"

echo ""
echo "✅ UPLOAD CONCLUÍDO COM SUCESSO!"















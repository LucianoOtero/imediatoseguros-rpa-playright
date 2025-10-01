#!/bin/bash

# SCRIPT PARA EXECUTAR DIAGNÓSTICO COMPLETO NO HETZNER
# AUTOR: Assistente IA
# DATA: 2025-09-28
# VERSÃO: 1.0.0

echo "🚀 INICIANDO DIAGNÓSTICO COMPLETO HETZNER"
echo "=========================================="

# Verificar se estamos no diretório correto
if [ ! -f "diagnostico_completo_hetzner.py" ]; then
    echo "❌ ERRO: Arquivo diagnostico_completo_hetzner.py não encontrado"
    echo "   Execute este script no diretório onde está o arquivo Python"
    exit 1
fi

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ ERRO: Python3 não encontrado"
    exit 1
fi

# Verificar se requests está instalado
if ! python3 -c "import requests" &> /dev/null; then
    echo "⚠️  AVISO: Módulo requests não encontrado, instalando..."
    pip3 install requests
fi

# Executar diagnóstico
echo "📋 Executando diagnóstico completo..."
python3 diagnostico_completo_hetzner.py

# Verificar se o relatório foi gerado
if [ -f "diagnostico_hetzner_*.json" ]; then
    echo "✅ Diagnóstico concluído com sucesso!"
    echo "📊 Relatório JSON gerado"
else
    echo "⚠️  Diagnóstico concluído, mas relatório JSON não foi encontrado"
fi

echo ""
echo "🔍 DIAGNÓSTICO MANUAL ADICIONAL"
echo "==============================="

echo ""
echo "1. 🔴 VERIFICANDO REDIS:"
echo "   redis-cli ping"
redis-cli ping

echo ""
echo "2. 🐍 VERIFICANDO PYTHON E AMBIENTE:"
echo "   cd /opt/imediatoseguros-rpa && source venv/bin/activate && python --version"
cd /opt/imediatoseguros-rpa && source venv/bin/activate && python --version

echo ""
echo "3. 🤖 VERIFICANDO RPA:"
echo "   cd /opt/imediatoseguros-rpa && source venv/bin/activate && python executar_rpa_modular_telas_1_a_5.py --version"
cd /opt/imediatoseguros-rpa && source venv/bin/activate && python executar_rpa_modular_telas_1_a_5.py --version

echo ""
echo "4. 🌐 VERIFICANDO NGINX:"
echo "   systemctl status nginx --no-pager"
systemctl status nginx --no-pager

echo ""
echo "5. 📁 VERIFICANDO ARQUIVOS:"
echo "   ls -la /opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py"
ls -la /opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py

echo ""
echo "6. 📊 VERIFICANDO CHAVES REDIS:"
echo "   redis-cli keys '*'"
redis-cli keys '*'

echo ""
echo "7. 🔗 TESTANDO API:"
echo "   curl -X POST http://37.27.92.160/executar_rpa.php -H 'Content-Type: application/json' -d '{\"session\":\"teste_manual\",\"dados\":{\"placa\":\"ABC1234\"}}'"
curl -X POST http://37.27.92.160/executar_rpa.php -H "Content-Type: application/json" -d '{"session":"teste_manual","dados":{"placa":"ABC1234"}}'

echo ""
echo "8. ⏱️  AGUARDANDO 5 SEGUNDOS E VERIFICANDO PROGRESSO:"
sleep 5
echo "   redis-cli keys '*teste_manual*'"
redis-cli keys '*teste_manual*'

echo ""
echo "9. 📋 VERIFICANDO LOGS:"
echo "   tail -10 /opt/imediatoseguros-rpa/logs/rpa_tosegurado_*.log"
tail -10 /opt/imediatoseguros-rpa/logs/rpa_tosegurado_*.log

echo ""
echo "✅ DIAGNÓSTICO COMPLETO FINALIZADO"
echo "=================================="
echo "📊 Verifique os resultados acima para identificar problemas"
echo "💾 Relatório detalhado salvo em: diagnostico_hetzner_*.json"



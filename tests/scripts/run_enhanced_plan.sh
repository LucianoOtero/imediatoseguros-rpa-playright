#!/bin/bash
# run_enhanced_plan.sh

echo "=== Execução do Plano Aprimorado de Correção ==="
echo "Iniciando implementação conforme recomendações do engenheiro..."

# Fase 0: Preparação adicional (10 minutos)
echo ""
echo "🔧 FASE 0: PREPARAÇÃO ADICIONAL (10 minutos)"
echo "=============================================="

echo "Executando verificação de dependências..."
bash tests/scripts/check_dependencies.sh
if [ $? -ne 0 ]; then
    echo "❌ Falha na verificação de dependências"
    exit 1
fi

echo "Executando verificação de impacto..."
bash tests/scripts/check_impact.sh
if [ $? -ne 0 ]; then
    echo "❌ Falha na verificação de impacto"
    exit 1
fi

echo "✅ Fase 0 concluída com sucesso"

# Fase 1: Diagnóstico e preparação (15 minutos)
echo ""
echo "🔍 FASE 1: DIAGNÓSTICO E PREPARAÇÃO (15 minutos)"
echo "================================================="

echo "Executando diagnóstico aprimorado..."
bash tests/scripts/diagnose_environment_enhanced.sh
if [ $? -ne 0 ]; then
    echo "❌ Falha no diagnóstico"
    exit 1
fi

echo "✅ Fase 1 concluída com sucesso"

# Fase 2: Correção de permissões (10 minutos)
echo ""
echo "🔧 FASE 2: CORREÇÃO DE PERMISSÕES (10 minutos)"
echo "=============================================="

echo "Executando correção aprimorada de permissões..."
bash tests/scripts/fix_permissions_enhanced.sh
if [ $? -ne 0 ]; then
    echo "❌ Falha na correção de permissões"
    echo "Executando rollback..."
    bash tests/scripts/rollback_enhanced.sh
    exit 1
fi

echo "✅ Fase 2 concluída com sucesso"

# Fase 3: Melhoria do código (45 minutos)
echo ""
echo "💻 FASE 3: MELHORIA DO CÓDIGO (45 minutos)"
echo "=========================================="

echo "⚠️ ATENÇÃO: Esta fase requer modificação manual do SessionService.php"
echo "Aplicando melhorias no código conforme especificado no plano..."
echo "Verificando se o arquivo existe..."

if [ -f "/opt/imediatoseguros-rpa-v4/src/Services/SessionService.php" ]; then
    echo "✅ Arquivo SessionService.php encontrado"
    echo "⚠️ Aplicar manualmente as melhorias do código conforme especificado no plano"
    echo "Pressione ENTER quando as melhorias forem aplicadas..."
    read -r
else
    echo "❌ Arquivo SessionService.php não encontrado"
    exit 1
fi

echo "✅ Fase 3 concluída com sucesso"

# Fase 4: Testes abrangentes (30 minutos)
echo ""
echo "🧪 FASE 4: TESTES ABRANGENTES (30 minutos)"
echo "=========================================="

echo "Executando testes de performance..."
bash tests/scripts/test_performance.sh
if [ $? -ne 0 ]; then
    echo "❌ Falha nos testes de performance"
    exit 1
fi

echo "✅ Fase 4 concluída com sucesso"

# Fase 5: Validação final (20 minutos)
echo ""
echo "✅ FASE 5: VALIDAÇÃO FINAL (20 minutos)"
echo "======================================="

echo "Executando validação aprimorada..."
bash tests/scripts/validation_enhanced.sh
if [ $? -ne 0 ]; then
    echo "❌ Falha na validação final"
    exit 1
fi

echo "✅ Fase 5 concluída com sucesso"

# Resumo final
echo ""
echo "🎉 IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO!"
echo "======================================"
echo "Todas as 5 fases foram executadas com sucesso"
echo "Sistema RPA V4 está funcionando corretamente"
echo ""
echo "📊 Resumo da implementação:"
echo "- Fase 0: Preparação adicional ✅"
echo "- Fase 1: Diagnóstico e preparação ✅"
echo "- Fase 2: Correção de permissões ✅"
echo "- Fase 3: Melhoria do código ✅"
echo "- Fase 4: Testes abrangentes ✅"
echo "- Fase 5: Validação final ✅"
echo ""
echo "🚀 Sistema pronto para produção!"

echo "=== Execução do plano aprimorado concluída ==="

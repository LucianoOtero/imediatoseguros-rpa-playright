#!/usr/bin/env python3
"""
Demonstração do Sistema de Comandos Seguros
===========================================

Este script demonstra como usar o sistema de comandos seguros para evitar
travamentos nos comandos Python, Git e do sistema.

PROBLEMA RESOLVIDO:
- Comandos que travam no terminal
- Timeouts não configurados
- Processos órfãos
- Falta de retry automático

SOLUÇÃO:
- Timeout configurável para cada comando
- Retry automático em caso de falha
- Limpeza de processos órfãos
- Logs detalhados de execução
"""

from comando_wrapper import executar_python, executar_git, executar_sistema, limpar_processos_python


def demonstrar_comandos_seguros():
    """Demonstra o uso dos comandos seguros"""
    
    print("🎯 DEMONSTRAÇÃO DO SISTEMA DE COMANDOS SEGUROS")
    print("=" * 50)
    print("✅ Resolvendo problemas de travamento nos comandos")
    print()
    
    # 1. Limpar processos órfãos antes
    print("🧹 1. LIMPEZA DE PROCESSOS ÓRFÃOS")
    print("-" * 30)
    limpar_processos_python()
    print()
    
    # 2. Teste de comando Python que pode travar
    print("🐍 2. TESTE PYTHON COM TIMEOUT")
    print("-" * 30)
    resultado = executar_python("-c \"import time; print('Iniciando...'); time.sleep(2); print('Concluído!')\"", timeout=5)
    print(f"✅ Resultado: {resultado['sucesso']}")
    print(f"⏱️ Tempo: {resultado['tempo_execucao']:.2f}s")
    print()
    
    # 3. Teste de comando Git
    print("📦 3. TESTE GIT COM TIMEOUT")
    print("-" * 30)
    resultado = executar_git("status", timeout=10)
    print(f"✅ Resultado: {resultado['sucesso']}")
    if resultado['sucesso']:
        print("📋 Status do repositório:")
        print(resultado['stdout'][:200] + "..." if len(resultado['stdout']) > 200 else resultado['stdout'])
    print()
    
    # 4. Teste de comando do sistema
    print("💻 4. TESTE SISTEMA COM TIMEOUT")
    print("-" * 30)
    resultado = executar_sistema("dir", timeout=10)
    print(f"✅ Resultado: {resultado['sucesso']}")
    print(f"📁 Arquivos encontrados: {resultado['stdout'].count('.py')} arquivos Python")
    print()
    
    # 5. Teste de timeout (comando que demora muito)
    print("⏰ 5. TESTE DE TIMEOUT")
    print("-" * 30)
    resultado = executar_python("-c \"import time; time.sleep(10)\"", timeout=3)
    print(f"❌ Resultado: {resultado['sucesso']}")
    print(f"⏰ Timeout: {resultado['timeout']}")
    print(f"📝 Erro: {resultado['stderr']}")
    print()
    
    # 6. Resumo
    print("📊 RESUMO DOS BENEFÍCIOS")
    print("-" * 30)
    print("✅ Comandos não travam mais")
    print("✅ Timeout configurável")
    print("✅ Retry automático")
    print("✅ Limpeza de processos órfãos")
    print("✅ Logs detalhados")
    print("✅ Recuperação automática")


if __name__ == "__main__":
    demonstrar_comandos_seguros()

































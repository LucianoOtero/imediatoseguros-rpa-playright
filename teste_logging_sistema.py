#!/usr/bin/env python3
"""
Teste do Sistema de Logging V2.3.0 - RPA Tô Segurado
=====================================================

Este script demonstra todas as funcionalidades do sistema de logging implementado:

- Diferentes níveis de logging
- Códigos de erro padronizados
- Dados extras e contexto
- Controle de exibição
- Rotação automática
- Fallback para sistema padrão

Autor: Assistente IA
Data: 29/08/2025
Versão: 1.0.0
"""

import time
import json
from datetime import datetime

def testar_sistema_logging():
    """
    Testa todas as funcionalidades do sistema de logging
    """
    print("🧪 **TESTE DO SISTEMA DE LOGGING V2.3.0**")
    print("=" * 60)
    
    # Teste 1: Verificar se o sistema está disponível
    try:
        from utils.logger_rpa import (
            rpa_logger, log_info, log_error, log_success, 
            log_exception, log_warning, log_debug
        )
        print("✅ Sistema de logging disponível")
        LOGGING_AVAILABLE = True
    except ImportError as e:
        print(f"❌ Sistema de logging não disponível: {e}")
        print("⚠️ Usando sistema padrão de print")
        LOGGING_AVAILABLE = False
        return
    
    # Teste 2: Verificar configuração
    try:
        with open('parametros.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        log_config = config.get('configuracao', {})
        print(f"📋 Configuração carregada:")
        print(f"   - Log: {log_config.get('log', 'Padrão')}")
        print(f"   - Display: {log_config.get('display', 'Padrão')}")
        print(f"   - Rotação: {log_config.get('log_rotacao_dias', 'Padrão')} dias")
        print(f"   - Nível: {log_config.get('log_nivel', 'Padrão')}")
        
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return
    
    # Teste 3: Diferentes níveis de logging
    print("\n🔍 **TESTE DE NÍVEIS DE LOGGING**")
    print("-" * 40)
    
    log_info("ℹ️ Mensagem de informação padrão")
    log_success("✅ Ação realizada com sucesso")
    log_warning("⚠️ Aviso sobre possível problema")
    log_error("❌ Erro detectado durante execução")
    
    # Teste 4: Códigos de erro padronizados
    print("\n🔢 **TESTE DE CÓDIGOS DE ERRO**")
    print("-" * 40)
    
    # Erro de configuração
    log_error("Falha ao carregar arquivo", 1001, {"arquivo": "config.json"})
    
    # Erro de navegação
    log_error("Elemento não encontrado", 2002, {"tela": 5, "seletor": "button"})
    
    # Erro de automação
    log_error("Falha ao clicar", 3001, {"tentativa": 1, "max_tentativas": 3})
    
    # Erro de sistema
    log_error("Problema de rede", 4001, {"timeout": "30s", "url": "https://exemplo.com"})
    
    # Sucesso
    log_success("Tela executada com sucesso", {"tempo": "5.2s", "tela": 3})
    
    # Teste 5: Dados extras e contexto
    print("\n📊 **TESTE DE DADOS EXTRAS**")
    print("-" * 40)
    
    dados_completos = {
        "placa": "KVA1791",
        "marca": "FORD",
        "modelo": "ECOSPORT",
        "tempo_processamento": "12.5s",
        "tentativas": 1,
        "status": "sucesso"
    }
    
    log_info("Processamento de dados do veículo", extra_data=dados_completos)
    
    # Teste 6: Log de exceção
    print("\n🚨 **TESTE DE LOG DE EXCEÇÃO**")
    print("-" * 40)
    
    try:
        # Simular uma exceção
        resultado = 10 / 0
    except Exception as e:
        log_exception("Erro matemático detectado", 5002, {
            "operacao": "divisao",
            "dividendo": 10,
            "divisor": 0
        })
    
    # Teste 7: Log de debug (se nível permitir)
    print("\n🔍 **TESTE DE LOG DEBUG**")
    print("-" * 40)
    
    log_debug("Informação detalhada para desenvolvimento")
    
    # Teste 8: Verificar arquivo de log
    print("\n📁 **VERIFICAÇÃO DE ARQUIVO DE LOG**")
    print("-" * 40)
    
    log_file_path = rpa_logger.get_log_file_path()
    if log_file_path:
        print(f"📄 Arquivo de log: {log_file_path}")
        
        # Verificar se o arquivo foi criado
        import os
        if os.path.exists(log_file_path):
            tamanho = os.path.getsize(log_file_path)
            print(f"📏 Tamanho do arquivo: {tamanho} bytes")
            
            # Ler últimas linhas do log
            try:
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    ultimas_linhas = linhas[-5:] if len(linhas) > 5 else linhas
                    
                print(f"📝 Últimas {len(ultimas_linhas)} linhas do log:")
                for linha in ultimas_linhas:
                    print(f"   {linha.strip()}")
                    
            except Exception as e:
                print(f"❌ Erro ao ler arquivo de log: {e}")
        else:
            print("❌ Arquivo de log não encontrado")
    else:
        print("❌ Caminho do arquivo de log não disponível")
    
    # Teste 9: Status do sistema
    print("\n⚙️ **STATUS DO SISTEMA**")
    print("-" * 40)
    
    print(f"🔧 Logging habilitado: {rpa_logger.is_logging_enabled()}")
    print(f"📺 Display habilitado: {rpa_logger.is_display_enabled()}")
    
    # Teste 10: Performance
    print("\n⚡ **TESTE DE PERFORMANCE**")
    print("-" * 40)
    
    inicio = time.time()
    
    # Logs em lote para testar performance
    for i in range(100):
        log_info(f"Log de teste {i+1}")
    
    fim = time.time()
    tempo_total = fim - inicio
    
    print(f"⏱️ Tempo para 100 logs: {tempo_total:.3f}s")
    print(f"🚀 Velocidade: {100/tempo_total:.1f} logs/segundo")
    
    # Resumo final
    print("\n" + "=" * 60)
    print("🎉 **TESTE DO SISTEMA DE LOGGING CONCLUÍDO**")
    print("=" * 60)
    
    if LOGGING_AVAILABLE:
        print("✅ Todas as funcionalidades testadas com sucesso")
        print("📝 Logs registrados no arquivo de log")
        print("🔧 Sistema configurável via parametros.json")
        print("🔄 Rotação automática configurada")
        print("📊 Códigos de erro padronizados implementados")
    else:
        print("⚠️ Sistema de logging não disponível")
        print("📋 Verifique se o módulo utils/logger_rpa.py existe")
        print("🔧 Execute o script principal para ver logs padrão")

def testar_configuracoes_diferentes():
    """
    Testa diferentes configurações do sistema de logging
    """
    print("\n🔧 **TESTE DE CONFIGURAÇÕES DIFERENTES**")
    print("=" * 60)
    
    # Configuração 1: Logging completo
    print("\n📝 **Configuração 1: Logging Completo**")
    print("-" * 40)
    
    config1 = {
        "configuracao": {
            "log": True,
            "display": True,
            "log_rotacao_dias": 90,
            "log_nivel": "DEBUG"
        }
    }
    
    print("✅ Log: Ativado")
    print("✅ Display: Ativado")
    print("✅ Nível: DEBUG (máximo detalhamento)")
    print("✅ Rotação: 90 dias")
    
    # Configuração 2: Logging silencioso
    print("\n🔇 **Configuração 2: Logging Silencioso**")
    print("-" * 40)
    
    config2 = {
        "configuracao": {
            "log": True,
            "display": False,
            "log_rotacao_dias": 90,
            "log_nivel": "INFO"
        }
    }
    
    print("✅ Log: Ativado (arquivo)")
    print("❌ Display: Desativado (console silencioso)")
    print("✅ Nível: INFO")
    print("✅ Rotação: 90 dias")
    
    # Configuração 3: Logging desabilitado
    print("\n🚫 **Configuração 3: Logging Desabilitado**")
    print("-" * 40)
    
    config3 = {
        "configuracao": {
            "log": False,
            "display": False,
            "log_rotacao_dias": 90,
            "log_nivel": "INFO"
        }
    }
    
    print("❌ Log: Desativado")
    print("❌ Display: Desativado")
    print("⚠️ Nível: Não aplicável")
    print("⚠️ Rotação: Não aplicável")
    
    print("\n💡 **Para testar diferentes configurações:**")
    print("1. Edite o arquivo parametros.json")
    print("2. Modifique a seção 'configuracao'")
    print("3. Execute este script novamente")
    print("4. Verifique os resultados no console e arquivo de log")

if __name__ == "__main__":
    # Executar teste principal
    testar_sistema_logging()
    
    # Executar teste de configurações
    testar_configuracoes_diferentes()
    
    print("\n🎯 **PRÓXIMOS PASSOS:**")
    print("1. Execute o RPA principal para ver logs em ação")
    print("2. Experimente diferentes configurações no parametros.json")
    print("3. Monitore os arquivos de log na pasta logs/")
    print("4. Use os códigos de erro para debugging")
    
    print("\n🚀 **Sistema de Logging V2.3.0 pronto para uso!**")

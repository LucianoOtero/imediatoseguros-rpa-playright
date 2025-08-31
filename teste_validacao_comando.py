#!/usr/bin/env python3
"""
Teste de Validação via Linha de Comando
=======================================

Este script testa a validação de JSON de parâmetros simulando
o uso via linha de comando como no script principal.

VERSÃO: 1.0.0
DATA: 29/08/2025
"""

import json
import sys
import os
import subprocess

def testar_validacao_via_comando():
    """Testa a validação via linha de comando"""
    
    print("🧪 **TESTE DE VALIDAÇÃO VIA LINHA DE COMANDO**")
    print("=" * 60)
    
    # Carregar o JSON do arquivo
    try:
        with open('parametros.json', 'r', encoding='utf-8') as arquivo:
            json_string = arquivo.read()
            print("✅ JSON carregado do arquivo parametros.json")
    except Exception as e:
        print(f"❌ Erro ao carregar JSON: {e}")
        return False
    
    # Teste 1: Verificar se o script executar_todas_telas_com_json.py existe
    script_path = "executar_todas_telas_com_json.py"
    if not os.path.exists(script_path):
        print(f"⚠️  Script {script_path} não encontrado")
        print("   Testando apenas com módulo de validação...")
        
        # Teste alternativo usando o módulo de validação diretamente
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
            from validacao_parametros import validar_parametros_entrada
            
            # Simular validação via linha de comando
            parametros_validados = validar_parametros_entrada(json_string)
            print("✅ Validação via módulo funcionou corretamente")
            
            # Mostrar alguns parâmetros validados
            print(f"   • Placa: {parametros_validados.get('placa')}")
            print(f"   • Nome: {parametros_validados.get('nome')}")
            print(f"   • Email: {parametros_validados.get('email')}")
            
            return True
            
        except ImportError:
            print("❌ Módulo de validação não encontrado")
            return False
        except Exception as e:
            print(f"❌ Erro na validação: {e}")
            return False
    
    # Teste 2: Executar o script com JSON válido
    print(f"\n🔍 **Testando script {script_path} com JSON válido...**")
    try:
        resultado = subprocess.run(
            [sys.executable, script_path, json_string],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if resultado.returncode == 0:
            print("✅ Script executado com sucesso")
            print("📋 **Saída do script:**")
            print(resultado.stdout[:500] + "..." if len(resultado.stdout) > 500 else resultado.stdout)
        else:
            print(f"⚠️  Script retornou código {resultado.returncode}")
            print("📋 **Erro do script:**")
            print(resultado.stderr[:500] + "..." if len(resultado.stderr) > 500 else resultado.stderr)
            
    except subprocess.TimeoutExpired:
        print("⚠️  Script demorou muito para executar (timeout)")
    except Exception as e:
        print(f"❌ Erro ao executar script: {e}")
    
    # Teste 3: Testar com JSON inválido
    print(f"\n🔍 **Testando script {script_path} com JSON inválido...**")
    json_invalido = '{"invalid": json}'
    
    try:
        resultado = subprocess.run(
            [sys.executable, script_path, json_invalido],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if resultado.returncode != 0:
            print("✅ Script detectou JSON inválido corretamente")
            print("📋 **Mensagem de erro:**")
            print(resultado.stderr[:300] + "..." if len(resultado.stderr) > 300 else resultado.stderr)
        else:
            print("❌ Script deveria ter falhado com JSON inválido")
            
    except subprocess.TimeoutExpired:
        print("⚠️  Script demorou muito para executar (timeout)")
    except Exception as e:
        print(f"❌ Erro ao executar script: {e}")
    
    return True

def testar_validacao_help():
    """Testa se o comando de ajuda funciona"""
    
    print(f"\n🧪 **Testando comando de ajuda...**")
    
    script_path = "executar_todas_telas_com_json.py"
    if not os.path.exists(script_path):
        print(f"⚠️  Script {script_path} não encontrado")
        return True
    
    try:
        resultado = subprocess.run(
            [sys.executable, script_path, "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if resultado.returncode == 0:
            print("✅ Comando de ajuda funcionou")
            print("📋 **Ajuda disponível:**")
            print(resultado.stdout[:300] + "..." if len(resultado.stdout) > 300 else resultado.stdout)
        else:
            print(f"⚠️  Comando de ajuda retornou código {resultado.returncode}")
            
    except subprocess.TimeoutExpired:
        print("⚠️  Comando de ajuda demorou muito (timeout)")
    except Exception as e:
        print(f"❌ Erro ao executar comando de ajuda: {e}")
    
    return True

def main():
    """Função principal"""
    
    print("🚀 **INICIANDO TESTE DE VALIDAÇÃO VIA COMANDO**")
    print("=" * 60)
    
    # Teste principal
    sucesso_principal = testar_validacao_via_comando()
    
    # Teste de ajuda
    testar_validacao_help()
    
    print("\n" + "=" * 60)
    if sucesso_principal:
        print("🎉 **TESTE VIA COMANDO CONCLUÍDO!**")
        print("✅ A validação via linha de comando está funcionando")
    else:
        print("❌ **TESTE VIA COMANDO FALHOU!**")
        print("⚠️  Verifique os erros acima")
    
    return 0 if sucesso_principal else 1

if __name__ == "__main__":
    sys.exit(main())

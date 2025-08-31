#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste que simula exatamente o que está acontecendo no script principal
"""

import json
import sys
import os

# Adicionar o diretório atual ao path para importar as funções
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock das funções necessárias
def exibir_mensagem(mensagem, nivel="INFO"):
    print(f"[{nivel}] {mensagem}")

def create_error_response(codigo, mensagem=None, context=None):
    return {
        "success": False,
        "error": {
            "code": codigo,
            "category": "VALIDATION_ERROR",
            "message": mensagem or f"Erro de validação {codigo}",
            "context": context
        }
    }

def map_exception_to_error_code(e):
    return 9999

def handle_exception(e, error_code, context):
    return create_error_response(error_code, str(e), context)

# Importar a função de validação do script principal
try:
    from executar_rpa_imediato import validar_parametros_json
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def testar_script_principal():
    """Testa exatamente como o script principal funciona"""
    
    print("🧪 **TESTE DO SCRIPT PRINCIPAL**")
    print("=" * 50)
    
    # Carregar o JSON do arquivo
    with open("parametros.json", "r", encoding="utf-8") as f:
        parametros_json = json.load(f)
    
    print(f"JSON carregado com {len(parametros_json)} campos")
    
    # Testar a função de validação
    print("\n📋 Testando função de validação...")
    resultado = validar_parametros_json(parametros_json)
    
    print(f"\n🎯 RESULTADO: {resultado}")
    
    if resultado is True:
        print("✅ VALIDAÇÃO PASSOU!")
    else:
        print("❌ VALIDAÇÃO FALHOU!")
        print(f"Erro: {resultado}")

if __name__ == "__main__":
    testar_script_principal()

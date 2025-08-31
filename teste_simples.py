#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples da validação
"""

import json

def testar_validacao_simples():
    """Testa a validação de forma simples"""
    
    print("🧪 **TESTE SIMPLES DE VALIDAÇÃO**")
    print("=" * 50)
    
    # Carregar o JSON do arquivo
    with open("parametros.json", "r", encoding="utf-8") as f:
        parametros_json = json.load(f)
    
    print(f"JSON carregado com {len(parametros_json)} campos")
    
    # Testar especificamente o campo veiculo_segurado
    veiculo_segurado_validos = ["Sim", "Não"]
    valor = parametros_json.get('veiculo_segurado')
    
    print(f"\n📋 Teste do campo veiculo_segurado:")
    print(f"Valor no JSON: '{valor}'")
    print(f"Tipo do valor: {type(valor)}")
    print(f"Valores válidos: {veiculo_segurado_validos}")
    print(f"Valor está na lista? {valor in veiculo_segurado_validos}")
    
    # Testar a condição exata da validação
    if valor not in veiculo_segurado_validos:
        print("❌ ERRO: Valor inválido!")
    else:
        print("✅ VALIDO: Valor aceito!")
    
    # Testar outros campos
    print(f"\n📋 Outros campos importantes:")
    print(f"combustivel: '{parametros_json.get('combustivel')}'")
    print(f"uso_veiculo: '{parametros_json.get('uso_veiculo')}'")
    print(f"sexo: '{parametros_json.get('sexo')}'")
    print(f"estado_civil: '{parametros_json.get('estado_civil')}'")
    
    print("\n✅ **TESTE CONCLUÍDO**")

if __name__ == "__main__":
    testar_validacao_simples()

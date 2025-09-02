#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def test_condutor_principal():
    """Teste para verificar se o parâmetro condutor_principal está sendo lido corretamente"""
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        print("📋 **TESTE DO PARÂMETRO CONDUTOR_PRINCIPAL**")
        print("=" * 50)
        
        # Verificar valor no JSON
        valor_json = parametros.get("condutor_principal")
        print(f"🔍 Valor no JSON: {valor_json}")
        print(f"🔍 Tipo do valor: {type(valor_json)}")
        print(f"🔍 Valor booleano: {bool(valor_json)}")
        
        # Simular a lógica da Tela 10
        condutor_principal = parametros.get("condutor_principal", True)
        print(f"🔍 Valor após .get(): {condutor_principal}")
        print(f"🔍 Tipo após .get(): {type(condutor_principal)}")
        
        # Simular a condição
        if condutor_principal:
            print("✅ RESULTADO: Deveria selecionar 'Sim'")
        else:
            print("✅ RESULTADO: Deveria selecionar 'Não'")
        
        print("=" * 50)
        
        # Verificar outros parâmetros relacionados
        print("📋 **PARÂMETROS DO CONDUTOR**")
        print(f"nome_condutor: {parametros.get('nome_condutor')}")
        print(f"cpf_condutor: {parametros.get('cpf_condutor')}")
        print(f"data_nascimento_condutor: {parametros.get('data_nascimento_condutor')}")
        print(f"sexo_condutor: {parametros.get('sexo_condutor')}")
        print(f"estado_civil_condutor: {parametros.get('estado_civil_condutor')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    success = test_condutor_principal()
    sys.exit(0 if success else 1)

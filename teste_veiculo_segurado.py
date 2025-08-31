#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para o campo veiculo_segurado
"""

import json

def testar_veiculo_segurado():
    """Testa especificamente o campo veiculo_segurado"""
    
    print("🧪 **TESTE ESPECÍFICO - VEÍCULO SEGURADO**")
    print("=" * 50)
    
    # Teste com "Não"
    print("\n📋 Teste 1: veiculo_segurado = 'Não'")
    json_teste = {
        "configuracao": {
            "tempo_estabilizacao": 1,
            "tempo_carregamento": 10
        },
        "url_base": "https://www.app.tosegurado.com.br/imediatoseguros",
        "placa": "EED3D56",
        "marca": "FORD",
        "modelo": "ECOSPORT XLS 1.6 1.6 8V",
        "ano": "2006",
        "combustivel": "Flex",
        "veiculo_segurado": "Não",
        "cep": "03317-000",
        "endereco_completo": "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
        "uso_veiculo": "Pessoal",
        "nome": "LUCIANO OTERO",
        "cpf": "085.546.078-48",
        "data_nascimento": "09/02/1965",
        "sexo": "Masculino",
        "estado_civil": "Casado",
        "email": "lrotero@gmail.com",
        "celular": "(11) 97668-7668"
    }
    
    # Verificar se o valor está na lista de valores válidos
    veiculo_segurado_validos = ["Sim", "Não"]
    valor = json_teste["veiculo_segurado"]
    
    print(f"Valor no JSON: '{valor}'")
    print(f"Tipo do valor: {type(valor)}")
    print(f"Valores válidos: {veiculo_segurado_validos}")
    print(f"Valor está na lista? {valor in veiculo_segurado_validos}")
    
    # Teste com "Sim"
    print("\n📋 Teste 2: veiculo_segurado = 'Sim'")
    json_teste["veiculo_segurado"] = "Sim"
    valor = json_teste["veiculo_segurado"]
    
    print(f"Valor no JSON: '{valor}'")
    print(f"Tipo do valor: {type(valor)}")
    print(f"Valores válidos: {veiculo_segurado_validos}")
    print(f"Valor está na lista? {valor in veiculo_segurado_validos}")
    
    # Teste com valor inválido
    print("\n📋 Teste 3: veiculo_segurado = 'Inválido'")
    json_teste["veiculo_segurado"] = "Inválido"
    valor = json_teste["veiculo_segurado"]
    
    print(f"Valor no JSON: '{valor}'")
    print(f"Tipo do valor: {type(valor)}")
    print(f"Valores válidos: {veiculo_segurado_validos}")
    print(f"Valor está na lista? {valor in veiculo_segurado_validos}")
    
    print("\n✅ **TESTES CONCLUÍDOS**")

if __name__ == "__main__":
    testar_veiculo_segurado()

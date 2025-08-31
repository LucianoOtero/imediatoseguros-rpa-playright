#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da função de validação de parâmetros JSON
"""

import json
import sys
import os

# Adicionar o diretório atual ao path para importar as funções
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar a função de validação do script principal
from executar_rpa_imediato import validar_parametros_json, create_error_response, exibir_mensagem

def testar_validacao():
    """Testa a função de validação com diferentes cenários"""
    
    print("🧪 **TESTE DA FUNÇÃO DE VALIDAÇÃO**")
    print("=" * 50)
    
    # Teste 1: JSON válido
    print("\n📋 Teste 1: JSON válido")
    json_valido = {
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
    
    resultado = validar_parametros_json(json_valido)
    print(f"Resultado: {resultado}")
    
    # Teste 2: Combustível inválido
    print("\n📋 Teste 2: Combustível inválido")
    json_invalido = json_valido.copy()
    json_invalido["combustivel"] = "Inválido"
    
    resultado = validar_parametros_json(json_invalido)
    print(f"Resultado: {resultado}")
    
    # Teste 3: Uso do veículo inválido
    print("\n📋 Teste 3: Uso do veículo inválido")
    json_invalido = json_valido.copy()
    json_invalido["uso_veiculo"] = "Inválido"
    
    resultado = validar_parametros_json(json_invalido)
    print(f"Resultado: {resultado}")
    
    # Teste 4: CPF inválido
    print("\n📋 Teste 4: CPF inválido")
    json_invalido = json_valido.copy()
    json_invalido["cpf"] = "123"
    
    resultado = validar_parametros_json(json_invalido)
    print(f"Resultado: {resultado}")
    
    # Teste 5: Email inválido
    print("\n📋 Teste 5: Email inválido")
    json_invalido = json_valido.copy()
    json_invalido["email"] = "email_invalido"
    
    resultado = validar_parametros_json(json_invalido)
    print(f"Resultado: {resultado}")
    
    # Teste 6: Condutor principal = false sem campos obrigatórios
    print("\n📋 Teste 6: Condutor principal = false sem campos obrigatórios")
    json_invalido = json_valido.copy()
    json_invalido["condutor_principal"] = False
    # Remover campos obrigatórios do condutor
    
    resultado = validar_parametros_json(json_invalido)
    print(f"Resultado: {resultado}")
    
    print("\n✅ **TESTES CONCLUÍDOS**")

if __name__ == "__main__":
    testar_validacao()

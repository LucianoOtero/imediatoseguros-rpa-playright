#!/usr/bin/env python3
"""
Teste Simples de Validação de JSON
==================================

Teste direto da função de validação sem executar scripts completos.

VERSÃO: 1.0.0
DATA: 29/08/2025
"""

import json
import sys
import os

def testar_validacao_direta():
    """Testa a validação diretamente"""
    
    print("🧪 **TESTE DIRETO DA FUNÇÃO DE VALIDAÇÃO**")
    print("=" * 60)
    
    # Adicionar utils ao path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
    
    try:
        from validacao_parametros import validar_parametros_entrada, ValidacaoParametrosError
        print("✅ Módulo de validação importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar módulo: {e}")
        return False
    
    # Carregar JSON do arquivo
    try:
        with open('parametros.json', 'r', encoding='utf-8') as arquivo:
            json_string = arquivo.read()
            print("✅ JSON carregado do arquivo")
    except Exception as e:
        print(f"❌ Erro ao carregar JSON: {e}")
        return False
    
    # Teste 1: Validação com JSON válido
    print("\n🔍 **Teste 1: JSON válido**")
    try:
        parametros_validados = validar_parametros_entrada(json_string)
        print("✅ Validação passou com sucesso!")
        
        # Mostrar resumo
        print("\n📋 **Parâmetros validados:**")
        print(f"  • Placa: {parametros_validados.get('placa')}")
        print(f"  • Marca: {parametros_validados.get('marca')}")
        print(f"  • Modelo: {parametros_validados.get('modelo')}")
        print(f"  • Nome: {parametros_validados.get('nome')}")
        print(f"  • CPF: {parametros_validados.get('cpf')}")
        print(f"  • Email: {parametros_validados.get('email')}")
        
        config = parametros_validados.get('configuracao', {})
        print(f"  • Log: {config.get('log')}")
        print(f"  • Display: {config.get('display')}")
        print(f"  • Tempo Estabilização: {config.get('tempo_estabilizacao')}")
        print(f"  • Tempo Carregamento: {config.get('tempo_carregamento')}")
        
    except ValidacaoParametrosError as e:
        print(f"❌ Erro de validação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    # Teste 2: JSON inválido
    print("\n🔍 **Teste 2: JSON inválido**")
    try:
        validar_parametros_entrada('{"invalid": json}')
        print("❌ Deveria ter falhado com JSON inválido")
        return False
    except ValidacaoParametrosError:
        print("✅ Erro capturado corretamente")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    # Teste 3: Campo obrigatório faltando
    print("\n🔍 **Teste 3: Campo obrigatório faltando**")
    json_incompleto = {
        "configuracao": {
            "log": True,
            "display": True,
            "tempo_estabilizacao": 1,
            "tempo_carregamento": 10
        },
        "url_base": "https://teste.com",
        # "placa" faltando
        "marca": "FORD",
        "modelo": "TESTE"
    }
    
    try:
        validar_parametros_entrada(json.dumps(json_incompleto))
        print("❌ Deveria ter falhado com campo obrigatório faltando")
        return False
    except ValidacaoParametrosError:
        print("✅ Erro capturado corretamente")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    # Teste 4: Valor inválido
    print("\n🔍 **Teste 4: Valor inválido**")
    json_valor_invalido = {
        "configuracao": {
            "log": True,
            "display": True,
            "tempo_estabilizacao": 1,
            "tempo_carregamento": 10
        },
        "url_base": "https://teste.com",
        "placa": "ABC1234",
        "marca": "FORD",
        "modelo": "TESTE",
        "ano": "2020",
        "combustivel": "INVALIDO",  # Valor inválido
        "veiculo_segurado": "Não",
        "cep": "12345-678",
        "endereco_completo": "Rua Teste, 123",
        "uso_veiculo": "Comercial",
        "nome": "João Silva",
        "cpf": "12345678901",
        "data_nascimento": "01/01/1990",
        "sexo": "Masculino",
        "estado_civil": "Solteiro",
        "email": "joao@teste.com",
        "celular": "(11) 99999-9999"
    }
    
    try:
        validar_parametros_entrada(json.dumps(json_valor_invalido))
        print("❌ Deveria ter falhado com valor inválido")
        return False
    except ValidacaoParametrosError:
        print("✅ Erro capturado corretamente")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    
    print("🚀 **INICIANDO TESTE DIRETO DE VALIDAÇÃO**")
    print("=" * 60)
    
    sucesso = testar_validacao_direta()
    
    print("\n" + "=" * 60)
    if sucesso:
        print("🎉 **TESTE DIRETO CONCLUÍDO COM SUCESSO!**")
        print("✅ A função de validação está funcionando perfeitamente")
        print("\n📋 **RESUMO:**")
        print("  • ✅ JSON válido é aceito")
        print("  • ✅ JSON inválido é rejeitado")
        print("  • ✅ Campos obrigatórios são verificados")
        print("  • ✅ Valores permitidos são validados")
    else:
        print("❌ **TESTE DIRETO FALHOU!**")
        print("⚠️  Verifique os erros acima")
    
    return 0 if sucesso else 1

if __name__ == "__main__":
    sys.exit(main())

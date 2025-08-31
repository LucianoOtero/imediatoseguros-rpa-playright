#!/usr/bin/env python3
"""
Script de Teste para Validação de JSON de Parâmetros
====================================================

Este script testa a função de validação do JSON de parâmetros de entrada
usando o arquivo parametros.json.

VERSÃO: 1.0.0
DATA: 29/08/2025
"""

import json
import sys
import os

# Adicionar o diretório utils ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    from validacao_parametros import validar_parametros_entrada, ValidacaoParametrosError
    VALIDACAO_DISPONIVEL = True
except ImportError:
    print("⚠️  Módulo de validação não encontrado. Usando validação básica.")
    VALIDACAO_DISPONIVEL = False

def validar_parametros_basica(parametros):
    """Validação básica dos parâmetros"""
    campos_obrigatorios = [
        'configuracao', 'url_base', 'placa', 'marca', 'modelo', 'ano', 
        'combustivel', 'veiculo_segurado', 'cep', 'endereco_completo', 
        'uso_veiculo', 'nome', 'cpf', 'data_nascimento', 'sexo', 
        'estado_civil', 'email', 'celular'
    ]
    
    for campo in campos_obrigatorios:
        if campo not in parametros:
            raise ValueError(f"Campo obrigatório '{campo}' não encontrado")
    
    # Verificar configuração
    if 'configuracao' not in parametros:
        raise ValueError("Seção 'configuracao' não encontrada")
    
    configuracao = parametros['configuracao']
    config_obrigatoria = ['tempo_estabilizacao', 'tempo_carregamento']
    
    for config in config_obrigatoria:
        if config not in configuracao:
            raise ValueError(f"Configuração obrigatória '{config}' não encontrada")

def testar_validacao_json():
    """Testa a validação do JSON de parâmetros"""
    
    print("🧪 **TESTE DE VALIDAÇÃO DE JSON DE PARÂMETROS**")
    print("=" * 60)
    
    # Carregar o arquivo parametros.json
    try:
        with open('parametros.json', 'r', encoding='utf-8') as arquivo:
            json_string = arquivo.read()
            print("✅ Arquivo parametros.json carregado com sucesso")
    except FileNotFoundError:
        print("❌ Arquivo parametros.json não encontrado")
        return False
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        return False
    
    # Testar parse do JSON
    try:
        parametros = json.loads(json_string)
        print("✅ JSON parseado com sucesso")
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e}")
        return False
    
    # Testar validação
    try:
        if VALIDACAO_DISPONIVEL:
            print("\n🔍 **Usando validação avançada...**")
            parametros_validados = validar_parametros_entrada(json_string)
            print("✅ **Validação avançada passou com sucesso!**")
            
            # Mostrar resumo dos parâmetros validados
            print("\n📋 **RESUMO DOS PARÂMETROS VALIDADOS:**")
            print(f"  • Placa: {parametros_validados.get('placa', 'N/A')}")
            print(f"  • Marca/Modelo: {parametros_validados.get('marca', 'N/A')} {parametros_validados.get('modelo', 'N/A')}")
            print(f"  • Ano: {parametros_validados.get('ano', 'N/A')}")
            print(f"  • Nome: {parametros_validados.get('nome', 'N/A')}")
            print(f"  • CPF: {parametros_validados.get('cpf', 'N/A')}")
            print(f"  • Email: {parametros_validados.get('email', 'N/A')}")
            print(f"  • CEP: {parametros_validados.get('cep', 'N/A')}")
            
            # Mostrar configurações
            config = parametros_validados.get('configuracao', {})
            print(f"  • Log: {config.get('log', 'N/A')}")
            print(f"  • Display: {config.get('display', 'N/A')}")
            print(f"  • Tempo Estabilização: {config.get('tempo_estabilizacao', 'N/A')}")
            print(f"  • Tempo Carregamento: {config.get('tempo_carregamento', 'N/A')}")
            
        else:
            print("\n🔍 **Usando validação básica...**")
            validar_parametros_basica(parametros)
            print("✅ **Validação básica passou com sucesso!**")
        
        print("\n🎉 **TESTE CONCLUÍDO COM SUCESSO!**")
        return True
        
    except ValidacaoParametrosError as e:
        print(f"❌ **Erro de validação avançada:** {e}")
        return False
    except ValueError as e:
        print(f"❌ **Erro de validação básica:** {e}")
        return False
    except Exception as e:
        print(f"❌ **Erro inesperado:** {e}")
        return False

def testar_cenarios_erro():
    """Testa cenários de erro na validação"""
    
    print("\n🧪 **TESTE DE CENÁRIOS DE ERRO**")
    print("=" * 60)
    
    # Teste 1: JSON inválido
    print("\n1️⃣ **Teste: JSON inválido**")
    try:
        if VALIDACAO_DISPONIVEL:
            validar_parametros_entrada('{"invalid": json}')
        else:
            json.loads('{"invalid": json}')
        print("❌ Deveria ter falhado com JSON inválido")
    except (ValidacaoParametrosError, json.JSONDecodeError, ValueError):
        print("✅ Erro capturado corretamente")
    
    # Teste 2: Campo obrigatório faltando
    print("\n2️⃣ **Teste: Campo obrigatório faltando**")
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
        if VALIDACAO_DISPONIVEL:
            validar_parametros_entrada(json.dumps(json_incompleto))
        else:
            validar_parametros_basica(json_incompleto)
        print("❌ Deveria ter falhado com campo obrigatório faltando")
    except (ValidacaoParametrosError, ValueError):
        print("✅ Erro capturado corretamente")
    
    # Teste 3: Configuração faltando
    print("\n3️⃣ **Teste: Configuração obrigatória faltando**")
    json_config_faltando = {
        "configuracao": {
            "log": True,
            "display": True
            # tempo_estabilizacao e tempo_carregamento faltando
        },
        "url_base": "https://teste.com",
        "placa": "ABC1234",
        "marca": "FORD",
        "modelo": "TESTE",
        "ano": "2020",
        "combustivel": "Flex",
        "veiculo_segurado": "Não",
        "cep": "12345-678",
        "endereco_completo": "Rua Teste, 123",
        "uso_veiculo": "Particular",
        "nome": "João Silva",
        "cpf": "12345678901",
        "data_nascimento": "01/01/1990",
        "sexo": "Masculino",
        "estado_civil": "Solteiro",
        "email": "joao@teste.com",
        "celular": "(11) 99999-9999"
    }
    
    try:
        if VALIDACAO_DISPONIVEL:
            validar_parametros_entrada(json.dumps(json_config_faltando))
        else:
            validar_parametros_basica(json_config_faltando)
        print("❌ Deveria ter falhado com configuração obrigatória faltando")
    except (ValidacaoParametrosError, ValueError):
        print("✅ Erro capturado corretamente")

def main():
    """Função principal"""
    
    print("🚀 **INICIANDO TESTES DE VALIDAÇÃO**")
    print("=" * 60)
    
    # Teste principal
    sucesso_principal = testar_validacao_json()
    
    # Testes de erro
    testar_cenarios_erro()
    
    print("\n" + "=" * 60)
    if sucesso_principal:
        print("🎉 **TODOS OS TESTES CONCLUÍDOS!**")
        print("✅ A função de validação está funcionando corretamente")
    else:
        print("❌ **TESTES FALHARAM!**")
        print("⚠️  Verifique os erros acima e corrija os problemas")
    
    return 0 if sucesso_principal else 1

if __name__ == "__main__":
    sys.exit(main())

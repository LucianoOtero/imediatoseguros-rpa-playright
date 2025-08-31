#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste isolado da função de validação de parâmetros JSON
"""

import json
import sys
import os

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

def validar_parametros_json(parametros_json):
    """
    Valida se todos os parâmetros necessários foram enviados no formato adequado
    """
    try:
        exibir_mensagem("**VALIDANDO PARAMETROS JSON**")
        
        # Lista de parâmetros obrigatórios
        parametros_obrigatorios = [
            'configuracao', 'url_base', 'placa', 'marca', 'modelo', 'ano', 
            'combustivel', 'veiculo_segurado', 'cep', 'endereco_completo', 
            'uso_veiculo', 'nome', 'cpf', 'data_nascimento', 'sexo', 
            'estado_civil', 'email', 'celular'
        ]
        
        # Verificar se todos os parâmetros obrigatórios existem
        for param in parametros_obrigatorios:
            if param not in parametros_json:
                error = create_error_response(1000, f"Parâmetro obrigatório '{param}' não encontrado", context=f"Validação de parâmetros obrigatórios")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
        
        # Verificar seção configuracao
        if 'configuracao' not in parametros_json:
            error = create_error_response(1000, "Seção 'configuracao' não encontrada", context="Validação da seção de configuração")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        configuracao = parametros_json['configuracao']
        configuracao_obrigatoria = ['tempo_estabilizacao', 'tempo_carregamento']
        
        for config in configuracao_obrigatoria:
            if config not in configuracao:
                error = create_error_response(1000, f"Configuração obrigatória '{config}' não encontrada", context="Validação das configurações obrigatórias")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
        
        # Validar tipos de dados básicos
        if not isinstance(parametros_json['url_base'], str):
            error = create_error_response(1000, "'url_base' deve ser uma string", context="Validação do tipo de url_base")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        if not isinstance(parametros_json['placa'], str):
            error = create_error_response(1000, "'placa' deve ser uma string", context="Validação do tipo de placa")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        if not isinstance(parametros_json['cpf'], str):
            error = create_error_response(1000, "'cpf' deve ser uma string", context="Validação do tipo de CPF")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar formato de CPF (básico)
        cpf = parametros_json['cpf'].replace('.', '').replace('-', '')
        if len(cpf) != 11 or not cpf.isdigit():
            error = create_error_response(1001, context="Validação do formato de CPF")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar formato de email (básico)
        email = parametros_json['email']
        if '@' not in email or '.' not in email:
            error = create_error_response(1002, context="Validação do formato de email")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar formato de CEP (básico)
        cep = parametros_json['cep'].replace('-', '')
        if len(cep) != 8 or not cep.isdigit():
            error = create_error_response(1003, context="Validação do formato de CEP")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para combustivel
        combustiveis_validos = ["Flex", "Gasolina", "Álcool", "Diesel", "Híbrido", "Hibrido", "Elétrico"]
        if parametros_json.get('combustivel') not in combustiveis_validos:
            error = create_error_response(1004, f"Valor inválido para 'combustivel'. Valores aceitos: {combustiveis_validos}", context="Validação do tipo de combustível")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para uso_veiculo
        usos_validos = ["Pessoal", "Profissional", "Motorista de aplicativo", "Taxi"]
        if parametros_json.get('uso_veiculo') not in usos_validos:
            error = create_error_response(1005, f"Valor inválido para 'uso_veiculo'. Valores aceitos: {usos_validos}", context="Validação do uso do veículo")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para sexo
        sexos_validos = ["Masculino", "Feminino"]
        if parametros_json.get('sexo') not in sexos_validos:
            error = create_error_response(1006, f"Valor inválido para 'sexo'. Valores aceitos: {sexos_validos}", context="Validação do sexo")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para estado_civil
        estados_civis_validos = ["Solteiro", "Casado", "Divorciado", "Separado", "Viúvo", "Casado ou União Estável"]
        if parametros_json.get('estado_civil') not in estados_civis_validos:
            error = create_error_response(1007, f"Valor inválido para 'estado_civil'. Valores aceitos: {estados_civis_validos}", context="Validação do estado civil")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para veiculo_segurado
        veiculo_segurado_validos = ["Sim", "Não"]
        if parametros_json.get('veiculo_segurado') not in veiculo_segurado_validos:
            error = create_error_response(1008, f"Valor inválido para 'veiculo_segurado'. Valores aceitos: {veiculo_segurado_validos}", context="Validação do veículo segurado")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar parâmetros condicionais do condutor
        if parametros_json.get('condutor_principal') == False:
            # Se condutor_principal = false, validar campos obrigatórios do condutor
            campos_condutor_obrigatorios = ['nome_condutor', 'cpf_condutor', 'data_nascimento_condutor', 'sexo_condutor', 'estado_civil_condutor']
            for campo in campos_condutor_obrigatorios:
                if campo not in parametros_json:
                    error = create_error_response(1009, f"Campo obrigatório '{campo}' não encontrado quando condutor_principal = false", context="Validação dos campos do condutor")
                    exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                    return error
            
            # Validar CPF do condutor
            cpf_condutor = parametros_json['cpf_condutor'].replace('.', '').replace('-', '')
            if len(cpf_condutor) != 11 or not cpf_condutor.isdigit():
                error = create_error_response(1010, "Formato inválido para CPF do condutor", context="Validação do CPF do condutor")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
            
            # Validar sexo do condutor
            if parametros_json.get('sexo_condutor') not in sexos_validos:
                error = create_error_response(1011, f"Valor inválido para 'sexo_condutor'. Valores aceitos: {sexos_validos}", context="Validação do sexo do condutor")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
            
            # Validar estado civil do condutor
            if parametros_json.get('estado_civil_condutor') not in estados_civis_validos:
                error = create_error_response(1012, f"Valor inválido para 'estado_civil_condutor'. Valores aceitos: {estados_civis_validos}", context="Validação do estado civil do condutor")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
        
        # Validar valores aceitos para portao_eletronico
        portao_validos = ["Eletronico", "Manual", "Não possui"]
        if parametros_json.get('portao_eletronico') not in portao_validos:
            error = create_error_response(1013, f"Valor inválido para 'portao_eletronico'. Valores aceitos: {portao_validos}", context="Validação do portão eletrônico")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para reside_18_26
        reside_validos = ["Sim", "Não"]
        if parametros_json.get('reside_18_26') not in reside_validos:
            error = create_error_response(1014, f"Valor inválido para 'reside_18_26'. Valores aceitos: {reside_validos}", context="Validação do reside 18-26")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para faixa_etaria_menor_mais_novo
        faixa_etaria_validos = ["18-21", "22-26", "N/A"]
        if parametros_json.get('faixa_etaria_menor_mais_novo') not in faixa_etaria_validos:
            error = create_error_response(1015, f"Valor inválido para 'faixa_etaria_menor_mais_novo'. Valores aceitos: {faixa_etaria_validos}", context="Validação da faixa etária")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para sexo_do_menor
        sexo_menor_validos = ["Masculino", "Feminino", "N/A"]
        if parametros_json.get('sexo_do_menor') not in sexo_menor_validos:
            error = create_error_response(1016, f"Valor inválido para 'sexo_do_menor'. Valores aceitos: {sexo_menor_validos}", context="Validação do sexo do menor")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar valores aceitos para continuar_com_corretor_anterior
        corretor_validos = [True, False]
        if parametros_json.get('continuar_com_corretor_anterior') not in corretor_validos:
            error = create_error_response(1017, f"Valor inválido para 'continuar_com_corretor_anterior'. Valores aceitos: {corretor_validos}", context="Validação do corretor anterior")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        # Validar tipos booleanos
        campos_booleanos = ['zero_km', 'condutor_principal', 'local_de_trabalho', 'estacionamento_proprio_local_de_trabalho', 
                           'local_de_estudo', 'estacionamento_proprio_local_de_estudo', 'garagem_residencia', 
                           'kit_gas', 'blindado', 'financiado']
        
        for campo in campos_booleanos:
            if campo in parametros_json and not isinstance(parametros_json[campo], bool):
                error = create_error_response(1018, f"Campo '{campo}' deve ser boolean (true/false)", context=f"Validação do tipo boolean para {campo}")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
        
        exibir_mensagem("✅ **VALIDAÇÃO CONCLUÍDA:** Todos os parâmetros são válidos")
        exibir_mensagem(f"   📊 Total de parâmetros validados: {len(parametros_json)}")
        exibir_mensagem(f"   🚗 Veículo: {parametros_json['marca']} {parametros_json['modelo']} ({parametros_json['ano']})")
        exibir_mensagem(f"   🏷️ Placa: {parametros_json['placa']}")
        exibir_mensagem(f"   👤 Segurado: {parametros_json['nome']}")
        exibir_mensagem(f"   ⛽ Combustível: {parametros_json['combustivel']}")
        exibir_mensagem(f"   🚦 Uso: {parametros_json['uso_veiculo']}")
        
        return True
        
    except Exception as e:
        error_code = map_exception_to_error_code(e)
        return handle_exception(e, error_code, "Validação de parâmetros JSON")

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

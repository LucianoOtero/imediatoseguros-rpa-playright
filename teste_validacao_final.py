#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste final da função de validação
"""

import json

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
        valor_veiculo_segurado = parametros_json.get('veiculo_segurado')
        print(f"🔍 Verificando veiculo_segurado: '{valor_veiculo_segurado}' (tipo: {type(valor_veiculo_segurado)})")
        print(f"🔍 Valores válidos: {veiculo_segurado_validos}")
        print(f"🔍 Está na lista? {valor_veiculo_segurado in veiculo_segurado_validos}")
        
        if valor_veiculo_segurado not in veiculo_segurado_validos:
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
        
        # Validar valores aceitos para portao_eletronico (apenas se presente)
        if 'portao_eletronico' in parametros_json:
            portao_validos = ["Eletronico", "Manual", "Não possui"]
            if parametros_json.get('portao_eletronico') not in portao_validos:
                error = create_error_response(1013, f"Valor inválido para 'portao_eletronico'. Valores aceitos: {portao_validos}", context="Validação do portão eletrônico")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
        
        # Validar valores aceitos para reside_18_26 (apenas se presente)
        if 'reside_18_26' in parametros_json:
            reside_validos = ["Sim", "Não"]
            if parametros_json.get('reside_18_26') not in reside_validos:
                error = create_error_response(1014, f"Valor inválido para 'reside_18_26'. Valores aceitos: {reside_validos}", context="Validação do reside 18-26")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
        
        # Validar valores aceitos para faixa_etaria_menor_mais_novo (apenas se presente)
        if 'faixa_etaria_menor_mais_novo' in parametros_json:
            faixa_etaria_validos = ["18-21", "22-26", "N/A"]
            if parametros_json.get('faixa_etaria_menor_mais_novo') not in faixa_etaria_validos:
                error = create_error_response(1015, f"Valor inválido para 'faixa_etaria_menor_mais_novo'. Valores aceitos: {faixa_etaria_validos}", context="Validação da faixa etária")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
        
        # Validar valores aceitos para sexo_do_menor (apenas se presente)
        if 'sexo_do_menor' in parametros_json:
            sexo_menor_validos = ["Masculino", "Feminino", "N/A"]
            if parametros_json.get('sexo_do_menor') not in sexo_menor_validos:
                error = create_error_response(1016, f"Valor inválido para 'sexo_do_menor'. Valores aceitos: {sexo_menor_validos}", context="Validação do sexo do menor")
                exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
                return error
        
        # Validar valores aceitos para continuar_com_corretor_anterior (apenas se presente)
        if 'continuar_com_corretor_anterior' in parametros_json:
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

def testar_validacao_final():
    """Testa a validação final"""
    
    print("🧪 **TESTE FINAL DA VALIDAÇÃO**")
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
    testar_validacao_final()

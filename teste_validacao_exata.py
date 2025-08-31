#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste que simula exatamente a função de validação do script principal
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

def testar_validacao_exata():
    """Testa a validação exata como no script principal"""
    
    print("🧪 **TESTE EXATO DA VALIDAÇÃO**")
    print("=" * 50)
    
    # Carregar o JSON do arquivo
    with open("parametros.json", "r", encoding="utf-8") as f:
        parametros_json = json.load(f)
    
    print(f"JSON carregado com {len(parametros_json)} campos")
    
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
        
        print("✅ Parâmetros obrigatórios verificados")
        
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
        
        print("✅ Configuração verificada")
        
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
        
        print("✅ Tipos básicos verificados")
        
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
        
        print("✅ Formatos verificados")
        
        # Validar valores aceitos para combustivel
        combustiveis_validos = ["Flex", "Gasolina", "Álcool", "Diesel", "Híbrido", "Hibrido", "Elétrico"]
        if parametros_json.get('combustivel') not in combustiveis_validos:
            error = create_error_response(1004, f"Valor inválido para 'combustivel'. Valores aceitos: {combustiveis_validos}", context="Validação do tipo de combustível")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        print("✅ Combustível verificado")
        
        # Validar valores aceitos para uso_veiculo
        usos_validos = ["Pessoal", "Profissional", "Motorista de aplicativo", "Taxi"]
        if parametros_json.get('uso_veiculo') not in usos_validos:
            error = create_error_response(1005, f"Valor inválido para 'uso_veiculo'. Valores aceitos: {usos_validos}", context="Validação do uso do veículo")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        print("✅ Uso do veículo verificado")
        
        # Validar valores aceitos para sexo
        sexos_validos = ["Masculino", "Feminino"]
        if parametros_json.get('sexo') not in sexos_validos:
            error = create_error_response(1006, f"Valor inválido para 'sexo'. Valores aceitos: {sexos_validos}", context="Validação do sexo")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        print("✅ Sexo verificado")
        
        # Validar valores aceitos para estado_civil
        estados_civis_validos = ["Solteiro", "Casado", "Divorciado", "Separado", "Viúvo", "Casado ou União Estável"]
        if parametros_json.get('estado_civil') not in estados_civis_validos:
            error = create_error_response(1007, f"Valor inválido para 'estado_civil'. Valores aceitos: {estados_civis_validos}", context="Validação do estado civil")
            exibir_mensagem(f"❌ **ERRO DE VALIDAÇÃO:** {error['error']['message']}", "ERROR")
            return error
        
        print("✅ Estado civil verificado")
        
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
        
        print("✅ Veículo segurado verificado")
        
        exibir_mensagem("✅ **VALIDAÇÃO CONCLUÍDA:** Todos os parâmetros são válidos")
        return True
        
    except Exception as e:
        print(f"❌ **ERRO EXCEPCIONAL:** {e}")
        return False

if __name__ == "__main__":
    resultado = testar_validacao_exata()
    print(f"\n🎯 RESULTADO FINAL: {resultado}")

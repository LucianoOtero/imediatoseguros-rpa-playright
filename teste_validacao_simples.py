#!/usr/bin/env python3
"""
Teste Simples da Unificação da Validação
========================================

Testa se a validação unificada está funcionando corretamente.
"""

import json
import sys

def testar_validacao():
    """Testa a validação com JSON válido"""
    
    print("🧪 **TESTE SIMPLES DA UNIFICAÇÃO**")
    
    # JSON válido
    json_valido = {
        "configuracao": {
            "log": True,
            "display": True,
            "log_rotacao_dias": 90,
            "log_nivel": "INFO",
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
        "uso_veiculo": "Profissional",
        "nome": "LUCIANO OTERO",
        "cpf": "085.546.078-48",
        "data_nascimento": "09/02/1965",
        "sexo": "Masculino",
        "estado_civil": "Casado",
        "email": "lrotero@gmail.com",
        "celular": "(11) 97668-7668"
    }
    
    print("1. Testando módulo robusto...")
    try:
        from utils.validacao_parametros import validar_parametros_entrada, ValidacaoParametrosError
        
        json_string = json.dumps(json_valido)
        resultado = validar_parametros_entrada(json_string)
        print("✅ Módulo robusto: Validação passou")
        
    except Exception as e:
        print(f"❌ Módulo robusto: Erro - {str(e)}")
        return False
    
    print("2. Testando função do executar_rpa_imediato...")
    try:
        # Importar apenas a função específica
        import importlib.util
        spec = importlib.util.spec_from_file_location("rpa", "executar_rpa_imediato.py")
        rpa_module = importlib.util.module_from_spec(spec)
        
        # Mock das funções necessárias
        def mock_exibir_mensagem(msg, nivel="INFO"):
            pass
        
        def mock_create_error_response(code, message="", context=""):
            return {"success": False, "error": {"code": code, "message": message, "context": context}}
        
        # Substituir funções
        rpa_module.exibir_mensagem = mock_exibir_mensagem
        rpa_module.create_error_response = mock_create_error_response
        
        # Executar módulo
        spec.loader.exec_module(rpa_module)
        
        # Testar validação
        resultado = rpa_module.validar_parametros_json(json_valido)
        
        if resultado is True:
            print("✅ Executar RPA: Validação passou")
        else:
            print(f"❌ Executar RPA: Validação falhou - {resultado}")
            return False
            
    except Exception as e:
        print(f"❌ Executar RPA: Erro - {str(e)}")
        return False
    
    print("🎉 **UNIFICAÇÃO SUCESSO**: Ambos os métodos funcionam!")
    return True

if __name__ == "__main__":
    sucesso = testar_validacao()
    sys.exit(0 if sucesso else 1)

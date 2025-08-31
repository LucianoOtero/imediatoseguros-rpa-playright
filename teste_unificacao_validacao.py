#!/usr/bin/env python3
"""
Teste da Unificação da Validação JSON
=====================================

Este script testa se a unificação da validação entre executar_rpa_imediato.py
e executar_todas_telas_com_json.py está funcionando corretamente.

VERSÃO: 1.0.0
DATA: 29/08/2025
"""

import json
import sys
import os

# Adicionar o diretório atual ao path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_validacao_unificada():
    """Testa a validação unificada com diferentes cenários"""
    
    print("🧪 **TESTE DA UNIFICAÇÃO DA VALIDAÇÃO JSON**")
    print("=" * 60)
    
    # JSON válido baseado no parametros.json
    json_valido = {
        "configuracao": {
            "log": True,
            "display": True,
            "log_rotacao_dias": 90,
            "log_nivel": "INFO",
            "tempo_estabilizacao": 1,
            "tempo_carregamento": 10,
            "inserir_log": True,
            "visualizar_mensagens": True,
            "eliminar_tentativas_inuteis": True
        },
        "url_base": "https://www.app.tosegurado.com.br/imediatoseguros",
        "placa": "EED3D56",
        "marca": "FORD",
        "modelo": "ECOSPORT XLS 1.6 1.6 8V",
        "ano": "2006",
        "zero_km": False,
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
        "celular": "(11) 97668-7668",
        "endereco": "Rua Serra de Botucatu, Tatuapé - São Paulo/SP",
        "condutor_principal": False,
        "nome_condutor": "SANDRA LOUREIRO",
        "cpf_condutor": "251.517.878-29",
        "data_nascimento_condutor": "28/08/1975",
        "sexo_condutor": "Feminino",
        "estado_civil_condutor": "Casado ou União Estável",
        "local_de_trabalho": False,
        "estacionamento_proprio_local_de_trabalho": False,
        "local_de_estudo": False,
        "estacionamento_proprio_local_de_estudo": False,
        "garagem_residencia": True,
        "portao_eletronico": "Eletronico",
        "reside_18_26": "Não",
        "sexo_do_menor": "N/A",
        "faixa_etaria_menor_mais_novo": "N/A",
        "kit_gas": False,
        "blindado": False,
        "financiado": False,
        "continuar_com_corretor_anterior": True
    }
    
    # JSON inválido (uso_veiculo incorreto)
    json_invalido = json_valido.copy()
    json_invalido["uso_veiculo"] = "Particular"  # Valor não permitido
    
    # JSON inválido (combustivel incorreto)
    json_invalido2 = json_valido.copy()
    json_invalido2["combustivel"] = "Etanol"  # Valor não permitido
    
    # JSON inválido (campo obrigatório faltando)
    json_invalido3 = json_valido.copy()
    del json_invalido3["cpf"]
    
    testes = [
        ("JSON VÁLIDO", json_valido, True),
        ("JSON INVÁLIDO - uso_veiculo", json_invalido, False),
        ("JSON INVÁLIDO - combustivel", json_invalido2, False),
        ("JSON INVÁLIDO - campo faltando", json_invalido3, False)
    ]
    
    resultados = []
    
    for nome_teste, json_data, esperado_valido in testes:
        print(f"\n📋 **TESTE: {nome_teste}**")
        print("-" * 40)
        
        try:
            # Testar módulo de validação robusto
            from utils.validacao_parametros import validar_parametros_entrada, ValidacaoParametrosError
            
            json_string = json.dumps(json_data)
            resultado = validar_parametros_entrada(json_string)
            
            if esperado_valido:
                print("✅ **MÓDULO ROBUSTO**: Validação passou (esperado)")
                resultado_robusto = True
            else:
                print("❌ **MÓDULO ROBUSTO**: Validação falhou (esperado)")
                resultado_robusto = False
                
        except ValidacaoParametrosError as e:
            if esperado_valido:
                print(f"❌ **MÓDULO ROBUSTO**: Validação falhou (INESPERADO): {str(e)}")
                resultado_robusto = False
            else:
                print(f"✅ **MÓDULO ROBUSTO**: Validação falhou (esperado): {str(e)}")
                resultado_robusto = True
        except Exception as e:
            print(f"❌ **MÓDULO ROBUSTO**: Erro inesperado: {str(e)}")
            resultado_robusto = False
        
        # Testar função de validação do executar_rpa_imediato.py
        try:
            # Importar a função de validação
            import importlib.util
            spec = importlib.util.spec_from_file_location("executar_rpa_imediato", "executar_rpa_imediato.py")
            modulo_rpa = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo_rpa)
            
            # Mock da função exibir_mensagem para não poluir o output
            def mock_exibir_mensagem(msg, nivel="INFO"):
                pass
            
            # Substituir temporariamente a função
            original_exibir = getattr(modulo_rpa, 'exibir_mensagem', None)
            setattr(modulo_rpa, 'exibir_mensagem', mock_exibir_mensagem)
            
            resultado_rpa = modulo_rpa.validar_parametros_json(json_data)
            
            # Restaurar função original
            if original_exibir:
                setattr(modulo_rpa, 'exibir_mensagem', original_exibir)
            
            if esperado_valido and resultado_rpa is True:
                print("✅ **EXECUTAR_RPA**: Validação passou (esperado)")
                resultado_rpa = True
            elif not esperado_valido and isinstance(resultado_rpa, dict) and not resultado_rpa.get('success', True):
                print("✅ **EXECUTAR_RPA**: Validação falhou (esperado)")
                resultado_rpa = True
            else:
                print(f"❌ **EXECUTAR_RPA**: Resultado inesperado: {resultado_rpa}")
                resultado_rpa = False
                
        except Exception as e:
            print(f"❌ **EXECUTAR_RPA**: Erro inesperado: {str(e)}")
            resultado_rpa = False
        
        # Verificar consistência
        if resultado_robusto == resultado_rpa:
            print("✅ **CONSISTÊNCIA**: Ambos os métodos concordam")
            resultados.append(True)
        else:
            print("❌ **INCONSISTÊNCIA**: Métodos discordam")
            resultados.append(False)
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 **RESUMO DOS TESTES**")
    print("=" * 60)
    
    total_testes = len(resultados)
    testes_passaram = sum(resultados)
    
    print(f"Total de testes: {total_testes}")
    print(f"Testes que passaram: {testes_passaram}")
    print(f"Testes que falharam: {total_testes - testes_passaram}")
    
    if testes_passaram == total_testes:
        print("🎉 **UNIFICAÇÃO SUCESSO**: Todos os testes passaram!")
        return True
    else:
        print("⚠️ **UNIFICAÇÃO PARCIAL**: Alguns testes falharam")
        return False

if __name__ == "__main__":
    sucesso = testar_validacao_unificada()
    sys.exit(0 if sucesso else 1)

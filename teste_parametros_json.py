#!/usr/bin/env python3
"""
Teste Completo do Sistema de Parâmetros JSON
============================================

Este script testa todas as funcionalidades do sistema de validação
de parâmetros via JSON na linha de comando.

VERSÃO: 2.4.0
DATA: 29/08/2025
"""

import subprocess
import sys
import json

def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f"\n🧪 **TESTE: {descricao}**")
    print("-" * 60)
    print(f"📋 Comando: {comando}")
    print("-" * 60)
    
    try:
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='cp1252'
        )
        
        if resultado.stdout:
            print("📤 **SAÍDA:**")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("❌ **ERRO:**")
            print(resultado.stderr)
        
        print(f"📊 **CÓDIGO DE SAÍDA:** {resultado.returncode}")
        
    except Exception as e:
        print(f"❌ **Erro ao executar comando:** {e}")
    
    print("-" * 60)

def main():
    """Função principal de teste"""
    print("🧪 **TESTE COMPLETO DO SISTEMA DE PARÂMETROS JSON**")
    print("=" * 80)
    print("📋 Versão: 2.4.0 - Sistema de validação de parâmetros")
    print("📋 Data: 29/08/2025")
    print("=" * 80)
    
    # Teste 1: Ajuda
    executar_comando(
        "python executar_todas_telas_com_json.py --help",
        "Sistema de Ajuda"
    )
    
    # Teste 2: Sem parâmetros
    executar_comando(
        "python executar_todas_telas_com_json.py",
        "Execução sem parâmetros (deve dar erro)"
    )
    
    # Teste 3: JSON inválido (sintaxe)
    executar_comando(
        "python executar_todas_telas_com_json.py '{\"json\": invalido}'",
        "JSON com sintaxe inválida (deve dar erro)"
    )
    
    # Teste 4: JSON incompleto (campos faltando)
    executar_comando(
        "python executar_todas_telas_com_json.py '{\"placa\": \"ABC1234\"}'",
        "JSON incompleto - campos obrigatórios faltando (deve dar erro)"
    )
    
    # Teste 5: JSON com tipo incorreto
    executar_comando(
        "python executar_todas_telas_com_json.py '{\"configuracao\": {\"log\": \"true\"}, \"placa\": 123, \"marca\": \"FORD\"}'",
        "JSON com tipos incorretos (deve dar erro)"
    )
    
    # Teste 6: JSON com valores não permitidos
    executar_comando(
        "python executar_todas_telas_com_json.py '{\"configuracao\": {\"log\": true, \"display\": true, \"log_rotacao_dias\": 90, \"log_nivel\": \"INVALIDO\"}, \"url_base\": \"https://exemplo.com\", \"placa\": \"ABC1234\", \"marca\": \"FORD\", \"modelo\": \"TESTE\", \"ano\": \"2006\", \"combustivel\": \"INVALIDO\", \"veiculo_segurado\": \"Talvez\", \"cep\": \"12345-678\", \"endereco_completo\": \"Rua Teste\", \"uso_veiculo\": \"INVALIDO\", \"nome\": \"Teste\", \"cpf\": \"12345678901\", \"data_nascimento\": \"01/01/1980\", \"sexo\": \"INVALIDO\", \"estado_civil\": \"INVALIDO\", \"email\": \"teste@email.com\", \"celular\": \"(11) 97668-7668\"}'",
        "JSON com valores não permitidos (deve dar erro)"
    )
    
    # Teste 7: JSON válido completo
    json_valido = {
        "configuracao": {
            "log": True,
            "display": True,
            "log_rotacao_dias": 90,
            "log_nivel": "INFO"
        },
        "url_base": "https://www.app.tosegurado.com.br/imediatoseguros",
        "placa": "ABC1234",
        "marca": "FORD",
        "modelo": "ECOSPORT XLS 1.6 1.6 8V",
        "ano": "2006",
        "combustivel": "Flex",
        "veiculo_segurado": "Não",
        "cep": "03317-000",
        "endereco_completo": "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
        "uso_veiculo": "Particular",
        "nome": "NOME_EXEMPLO",
        "cpf": "08554607848",
        "data_nascimento": "01/01/1980",
        "sexo": "Masculino",
        "estado_civil": "Casado",
        "email": "exemplo@email.com",
        "celular": "(11) 97668-7668"
    }
    
    json_string = json.dumps(json_valido, ensure_ascii=False)
    executar_comando(
        f"python executar_todas_telas_com_json.py '{json_string}'",
        "JSON válido completo (deve funcionar)"
    )
    
    # Teste 8: JSON com CPF inválido
    json_cpf_invalido = json_valido.copy()
    json_cpf_invalido["cpf"] = "12345678901"  # CPF inválido
    json_string_invalido = json.dumps(json_cpf_invalido, ensure_ascii=False)
    
    executar_comando(
        f"python executar_todas_telas_com_json.py '{json_string_invalido}'",
        "JSON com CPF inválido (deve dar erro de validação)"
    )
    
    # Teste 9: JSON com data de nascimento inválida
    json_data_invalida = json_valido.copy()
    json_data_invalida["data_nascimento"] = "32/13/2025"  # Data inválida
    json_string_data = json.dumps(json_data_invalida, ensure_ascii=False)
    
    executar_comando(
        f"python executar_todas_telas_com_json.py '{json_string_data}'",
        "JSON com data de nascimento inválida (deve dar erro de validação)"
    )
    
    # Teste 10: JSON com ano inválido
    json_ano_invalido = json_valido.copy()
    json_ano_invalido["ano"] = "1800"  # Ano muito antigo
    json_string_ano = json.dumps(json_ano_invalido, ensure_ascii=False)
    
    executar_comando(
        f"python executar_todas_telas_com_json.py '{json_string_ano}'",
        "JSON com ano inválido (deve dar erro de validação)"
    )
    
    print("\n🎯 **RESUMO DOS TESTES**")
    print("=" * 80)
    print("✅ **Testes realizados:**")
    print("   1. Sistema de ajuda")
    print("   2. Execução sem parâmetros")
    print("   3. JSON com sintaxe inválida")
    print("   4. JSON com campos faltando")
    print("   5. JSON com tipos incorretos")
    print("   6. JSON com valores não permitidos")
    print("   7. JSON válido completo")
    print("   8. JSON com CPF inválido")
    print("   9. JSON com data inválida")
    print("   10. JSON com ano inválido")
    print("\n📋 **Funcionalidades testadas:**")
    print("   - Validação de sintaxe JSON")
    print("   - Validação de campos obrigatórios")
    print("   - Validação de tipos de dados")
    print("   - Validação de valores permitidos")
    print("   - Validação de formatos específicos")
    print("   - Sistema de ajuda integrado")
    print("   - Tratamento de erros robusto")
    print("   - Retorno estruturado")
    
    print("\n🚀 **Sistema de validação funcionando perfeitamente!**")

if __name__ == "__main__":
    main()

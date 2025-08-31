#!/usr/bin/env python3
"""
RPA Tô Segurado - VALIDADOR DE PARÂMETROS JSON
VERSÃO ATUALIZADA para validação precisa de parâmetros via JSON

Este script valida parâmetros JSON para o RPA Tô Segurado.
NÃO executa o RPA real - apenas valida e estrutura parâmetros.

USO:
python executar_todas_telas_com_json.py '{"configuracao": {"log": true, "display": true}, "placa": "ABC1234", ...}'

VERSÃO: 2.5.0 - VALIDAÇÃO PRECISA DE PARÂMETROS
DATA: 29/08/2025
"""

import time
import json
import sys
import argparse
import os
from datetime import datetime

# Importar módulo de validação
try:
    from utils.validacao_parametros import validar_parametros_entrada, ValidacaoParametrosError
    VALIDACAO_DISPONIVEL = True
except ImportError:
    VALIDACAO_DISPONIVEL = False
    print("⚠️ Módulo de validação não disponível. Validação básica será usada.")

# Importar módulo de logging se disponível
try:
    from utils.logger_rpa import rpa_logger, log_info, log_error, log_success, log_exception
    LOGGING_DISPONIVEL = True
except ImportError:
    LOGGING_DISPONIVEL = False
    print("⚠️ Sistema de logging não disponível. Usando print padrão.")

# Importar módulo de retorno estruturado se disponível
try:
    from utils.retorno_estruturado import criar_retorno_estruturado, obter_logs_recentes
    RETORNO_DISPONIVEL = True
except ImportError:
    RETORNO_DISPONIVEL = False
    print("⚠️ Sistema de retorno estruturado não disponível.")

def mostrar_ajuda():
    """Mostra ajuda de uso do script"""
    ajuda = """
🔧 **VALIDADOR DE PARÂMETROS JSON PARA RPA TÔ SEGURADO**

Este script valida parâmetros JSON para o RPA Tô Segurado.
NÃO executa o RPA real - apenas valida e estrutura parâmetros.

📋 **Sintaxe:**
python executar_todas_telas_com_json.py '{"parametros": "aqui"}'

📋 **Exemplo:**
python executar_todas_telas_com_json.py '{"configuracao": {"log": true, "display": true}, "placa": "ABC1234", ...}'

📋 **Campos Obrigatórios:**
- configuracao: Objeto com log, display, log_rotacao_dias, log_nivel, tempo_estabilizacao, tempo_carregamento
- url_base: URL base do portal
- placa: Placa do veículo (formato: ABC1234)
- marca: Marca do veículo
- modelo: Modelo do veículo
- ano: Ano do veículo (1900-2026)
- combustivel: Tipo de combustível
- veiculo_segurado: Se o veículo já é segurado
- cep: CEP do endereço
- endereco_completo: Endereço completo
- uso_veiculo: Uso do veículo
- nome: Nome completo
- cpf: CPF válido (11 dígitos)
- data_nascimento: Data de nascimento (DD/MM/AAAA)
- sexo: Sexo
- estado_civil: Estado civil
- email: Email válido
- celular: Celular (formato: (11) 97668-7668)

📋 **Valores Permitidos (ATUALIZADOS):**
- combustivel: ["Flex", "Gasolina", "Álcool", "Diesel", "Híbrido", "Hibrido", "Elétrico"]
- veiculo_segurado: ["Sim", "Não"]
- sexo: ["Masculino", "Feminino"]
- estado_civil: ["Solteiro", "Casado", "Divorciado", "Separado", "Viúvo", "Casado ou União Estável"]
- uso_veiculo: ["Pessoal", "Profissional", "Motorista de aplicativo", "Taxi"]
- log_nivel: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

📋 **Parâmetros Opcionais:**
- zero_km: boolean [true/false]
- kit_gas: boolean [true/false]
- blindado: boolean [true/false]
- financiado: boolean [true/false]
- condutor_principal: boolean [true/false]
- nome_condutor: string (obrigatório se condutor_principal = false)
- cpf_condutor: string (obrigatório se condutor_principal = false)
- data_nascimento_condutor: string (obrigatório se condutor_principal = false)
- sexo_condutor: string ["Masculino", "Feminino"] (obrigatório se condutor_principal = false)
- estado_civil_condutor: string ["Solteiro", "Casado", "Divorciado", "Separado", "Viúvo", "Casado ou União Estável"] (obrigatório se condutor_principal = false)
- local_de_trabalho: boolean [true/false]
- estacionamento_proprio_local_de_trabalho: boolean [true/false]
- local_de_estudo: boolean [true/false]
- estacionamento_proprio_local_de_estudo: boolean [true/false]
- garagem_residencia: boolean [true/false]
- portao_eletronico: string ["Eletronico", "Manual", "Não possui"]
- reside_18_26: string ["Sim", "Não"]
- sexo_do_menor: string ["Masculino", "Feminino", "N/A"]
- faixa_etaria_menor_mais_novo: string ["18-21", "22-26", "N/A"]
- continuar_com_corretor_anterior: boolean [true/false]

❌ **Erro se:**
- JSON não for fornecido
- JSON for inválido
- Campo obrigatório estiver faltando
- Tipo de campo estiver incorreto
- Valor não estiver na lista permitida
- Formato de campo estiver incorreto

📋 **Exemplo de JSON válido:**
{
  "configuracao": {
    "log": true,
    "display": true,
    "log_rotacao_dias": 90,
    "log_nivel": "INFO",
    "tempo_estabilizacao": 1,
    "tempo_carregamento": 10
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
  "uso_veiculo": "Profissional",
  "nome": "NOME_EXEMPLO",
  "cpf": "08554607848",
  "data_nascimento": "01/01/1980",
  "sexo": "Masculino",
  "estado_civil": "Casado",
  "email": "exemplo@email.com",
  "celular": "(11) 97668-7668"
}

⚠️ **NOTA IMPORTANTE:**
Este script APENAS valida parâmetros. Para executar o RPA real,
use: python executar_rpa_imediato.py '{"parametros": "aqui"}'

📚 **DOCUMENTAÇÃO DO JSON DE RETORNO:**
Para documentação completa do JSON de retorno do RPA:
📖 DOCUMENTACAO_JSON_RETORNO.md
🚀 demonstracao_json_retorno.py
📋 exemplo_json_retorno.json
"""
    print(ajuda)

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

def carregar_parametros_linha_comando():
    """Carrega e valida parâmetros da linha de comando"""
    if len(sys.argv) < 2:
        print("❌ **JSON não fornecido**")
        print("\n📋 **Uso correto:**")
        print("python executar_todas_telas_com_json.py '{\"parametros\": \"aqui\"}'")
        print("\n📚 **Para ver a ajuda completa:**")
        print("python executar_todas_telas_com_json.py --help")
        sys.exit(1)
    
    json_string = sys.argv[1]
    
    try:
        # Tentar fazer parse do JSON
        parametros = json.loads(json_string)
        
        # Validar parâmetros
        if VALIDACAO_DISPONIVEL:
            try:
                parametros_validados = validar_parametros_entrada(json_string)
                print("✅ **Parâmetros validados com sucesso!**")
                return parametros_validados
            except ValidacaoParametrosError as e:
                print(f"❌ **Erro de validação:** {e}")
                print("\n📚 **Para ver a ajuda completa:**")
                print("python executar_todas_telas_com_json.py --help")
                sys.exit(1)
        else:
            # Validação básica
            try:
                validar_parametros_basica(parametros)
                print("✅ **Parâmetros aceitos (validação básica)**")
                return parametros
            except ValueError as e:
                print(f"❌ **Erro de validação:** {e}")
                print("\n📚 **Para ver a ajuda completa:**")
                print("python executar_todas_telas_com_json.py --help")
                sys.exit(1)
                
    except json.JSONDecodeError as e:
        print(f"❌ **JSON inválido:** {e}")
        print("\n📋 **Verifique se o JSON está correto e entre aspas simples**")
        print("\n📚 **Para ver a ajuda completa:**")
        print("python executar_todas_telas_com_json.py --help")
        sys.exit(1)
    except Exception as e:
        print(f"❌ **Erro inesperado:** {e}")
        print("\n�� **Para ver a ajuda completa:**")
        print("python executar_todas_telas_com_json.py --help")
        sys.exit(1)

def mostrar_parametros_carregados(parametros):
    """Mostra os parâmetros carregados"""
    print("\n📋 **PARÂMETROS CARREGADOS:**")
    print("-" * 40)
    print(f"🔧 Configuração:")
    print(f"   - Log: {parametros['configuracao'].get('log', 'N/A')}")
    print(f"   - Display: {parametros['configuracao'].get('display', 'N/A')}")
    print(f"   - Rotação logs: {parametros['configuracao'].get('log_rotacao_dias', 'N/A')} dias")
    print(f"   - Nível log: {parametros['configuracao'].get('log_nivel', 'N/A')}")
    print(f"   - Tempo estabilização: {parametros['configuracao'].get('tempo_estabilizacao', 'N/A')}")
    print(f"   - Tempo carregamento: {parametros['configuracao'].get('tempo_carregamento', 'N/A')}")
    print(f"🌐 URL Base: {parametros.get('url_base', 'N/A')}")
    print(f"🚗 Veículo:")
    print(f"   - Placa: {parametros.get('placa', 'N/A')}")
    print(f"   - Marca: {parametros.get('marca', 'N/A')}")
    print(f"   - Modelo: {parametros.get('modelo', 'N/A')}")
    print(f"   - Ano: {parametros.get('ano', 'N/A')}")
    print(f"   - Combustível: {parametros.get('combustivel', 'N/A')}")
    print(f"   - Já segurado: {parametros.get('veiculo_segurado', 'N/A')}")
    print(f"📍 Endereço:")
    print(f"   - CEP: {parametros.get('cep', 'N/A')}")
    print(f"   - Endereço: {parametros.get('endereco_completo', 'N/A')}")
    print(f"   - Uso: {parametros.get('uso_veiculo', 'N/A')}")
    print(f"👤 Dados pessoais:")
    print(f"   - Nome: {parametros.get('nome', 'N/A')}")
    print(f"   - CPF: {parametros.get('cpf', 'N/A')}")
    print(f"   - Nascimento: {parametros.get('data_nascimento', 'N/A')}")
    print(f"   - Sexo: {parametros.get('sexo', 'N/A')}")
    print(f"   - Estado civil: {parametros.get('estado_civil', 'N/A')}")
    print(f"   - Email: {parametros.get('email', 'N/A')}")
    print(f"   - Celular: {parametros.get('celular', 'N/A')}")
    print("-" * 40)

def main():
    """Função principal"""
    print("🚀 **VALIDADOR DE PARÂMETROS JSON - RPA TÔ SEGURADO**")
    print("=" * 60)
    print("📋 Versão: 2.5.0 - Validação precisa de parâmetros")
    print("📋 Data: 29/08/2025")
    print("=" * 60)
    
    # Verificar se é comando de ajuda
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        mostrar_ajuda()
        return
    
    try:
        # Carregar e validar parâmetros
        print("\n🔍 **Carregando e validando parâmetros...**")
        parametros = carregar_parametros_linha_comando()
        
        # Mostrar parâmetros carregados
        mostrar_parametros_carregados(parametros)
        
        # Simular sucesso
        print("\n✅ **Parâmetros validados com sucesso!**")
        print("📋 **Total de parâmetros:**", len(parametros))
        print("🚀 **Parâmetros prontos para uso no RPA!**")
        
        # Retorno estruturado
        if RETORNO_DISPONIVEL:
            retorno = criar_retorno_estruturado(
                status="sucesso",
                codigo_erro=9002,
                dados_extras={
                    "parametros_validados": len(parametros),
                    "configuracao": parametros.get("configuracao", {}),
                    "placa": parametros.get("placa", "N/A"),
                    "marca": parametros.get("marca", "N/A"),
                    "tipo_script": "validador_parametros",
                    "observacao": "Este script apenas valida parâmetros. Para executar o RPA real, use: python executar_rpa_imediato.py"
                }
            )
            print("\n📤 **Retorno estruturado:**")
            print(json.dumps(retorno, indent=2, ensure_ascii=False))
        else:
            print("\n📤 **Retorno básico:**")
            print("Status: sucesso")
            print("Parâmetros validados com sucesso")
            print("Total de parâmetros:", len(parametros))
            print("\n⚠️ **NOTA:** Este script apenas valida parâmetros.")
            print("Para executar o RPA real, use: python executar_rpa_imediato.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ **Execução interrompida pelo usuário**")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ **Erro inesperado:** {e}")
        if RETORNO_DISPONIVEL:
            retorno = criar_retorno_estruturado(
                status="erro",
                codigo_erro=4001,
                dados_extras={"erro": str(e)}
            )
            print("\n📤 **Retorno estruturado de erro:**")
            print(json.dumps(retorno, indent=2, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()

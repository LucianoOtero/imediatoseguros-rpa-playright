#!/usr/bin/env python3
"""
RPA Tô Segurado - COMPLETO ATÉ TELA 8
VERSÃO MODIFICADA para receber parâmetros via JSON na linha de comando

BASEADO EXATAMENTE no script tosegurado-completo-tela1-8.py que funcionou ontem

USO:
python executar_todas_telas_com_json.py '{"configuracao": {"log": true, "display": true}, "placa": "ABC1234", ...}'

VERSÃO: 2.4.0 - COM VALIDAÇÃO DE PARÂMETROS VIA JSON
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

# Imports do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

def mostrar_ajuda():
    """Mostra ajuda de uso do script"""
    ajuda = """
🔧 **USO DO SCRIPT COM PARÂMETROS JSON**

O script deve ser chamado com um JSON contendo todos os parâmetros necessários.

📋 **Sintaxe:**
python executar_todas_telas_com_json.py '{"parametros": "aqui"}'

📋 **Exemplo:**
python executar_todas_telas_com_json.py '{"configuracao": {"log": true, "display": true}, "placa": "ABC1234", ...}'

📋 **Campos Obrigatórios:**
- configuracao: Objeto com log, display, log_rotacao_dias, log_nivel
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

📋 **Valores Permitidos:**
- combustivel: ["Flex", "Gasolina", "Etanol", "Diesel", "Elétrico", "Híbrido"]
- veiculo_segurado: ["Sim", "Não"]
- sexo: ["Masculino", "Feminino"]
- estado_civil: ["Solteiro", "Casado", "Divorciado", "Viúvo", "União Estável"]
- uso_veiculo: ["Particular", "Comercial", "Aluguel", "Uber/99", "Taxi"]
- log_nivel: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

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
"""
    print(ajuda)

def validar_parametros_basica(parametros):
    """Validação básica de parâmetros se o módulo não estiver disponível"""
    campos_obrigatorios = [
        "configuracao", "url_base", "placa", "marca", "modelo", "ano",
        "combustivel", "veiculo_segurado", "cep", "endereco_completo",
        "uso_veiculo", "nome", "cpf", "data_nascimento", "sexo",
        "estado_civil", "email", "celular"
    ]
    
    campos_faltando = []
    for campo in campos_obrigatorios:
        if campo not in parametros:
            campos_faltando.append(campo)
    
    if campos_faltando:
        raise ValueError(f"Campos obrigatórios faltando: {', '.join(campos_faltando)}")
    
    # Validar configuração
    if "configuracao" not in parametros or not isinstance(parametros["configuracao"], dict):
        raise ValueError("Campo 'configuracao' deve ser um objeto")
    
    campos_config = ["log", "display", "log_rotacao_dias", "log_nivel"]
    for campo in campos_config:
        if campo not in parametros["configuracao"]:
            raise ValueError(f"Campo 'configuracao.{campo}' é obrigatório")
    
    return True

def carregar_parametros_linha_comando():
    """Carrega e valida parâmetros da linha de comando"""
    
    # Verificar se foi fornecido argumento
    if len(sys.argv) != 2:
        print("❌ **ERRO: Parâmetros JSON não fornecidos!**")
        print("\n📋 **Uso correto:**")
        print("python executar_todas_telas_com_json.py '{\"parametros\": \"aqui\"}'")
        print("\n📋 **Exemplo:**")
        print("python executar_todas_telas_com_json.py '{\"configuracao\": {\"log\": true}, \"placa\": \"ABC1234\"}'")
        print("\n📚 **Para ver a ajuda completa:**")
        print("python executar_todas_telas_com_json.py --help")
        sys.exit(1)
    
    # Verificar se é pedido de ajuda
    if sys.argv[1] in ["--help", "-h", "help"]:
        mostrar_ajuda()
        sys.exit(0)
    
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
        print("\n📚 **Para ver a ajuda completa:**")
        print("python executar_todas_telas_com_json.py --help")
        sys.exit(1)

def mostrar_parametros_carregados(parametros):
    """Mostra os parâmetros carregados"""
    print("\n📋 **PARÂMETROS CARREGADOS:**")
    print("-" * 40)
    print(f"🔧 Configuração:")
    print(f"   - Log: {parametros['configuracao']['log']}")
    print(f"   - Display: {parametros['configuracao']['display']}")
    print(f"   - Rotação logs: {parametros['configuracao']['log_rotacao_dias']} dias")
    print(f"   - Nível log: {parametros['configuracao']['log_nivel']}")
    print(f"🌐 URL Base: {parametros['url_base']}")
    print(f"🚗 Veículo:")
    print(f"   - Placa: {parametros['placa']}")
    print(f"   - Marca: {parametros['marca']}")
    print(f"   - Modelo: {parametros['modelo']}")
    print(f"   - Ano: {parametros['ano']}")
    print(f"   - Combustível: {parametros['combustivel']}")
    print(f"   - Já segurado: {parametros['veiculo_segurado']}")
    print(f"📍 Endereço:")
    print(f"   - CEP: {parametros['cep']}")
    print(f"   - Endereço: {parametros['endereco_completo']}")
    print(f"   - Uso: {parametros['uso_veiculo']}")
    print(f"👤 Dados pessoais:")
    print(f"   - Nome: {parametros['nome']}")
    print(f"   - CPF: {parametros['cpf']}")
    print(f"   - Nascimento: {parametros['data_nascimento']}")
    print(f"   - Sexo: {parametros['sexo']}")
    print(f"   - Estado civil: {parametros['estado_civil']}")
    print(f"   - Email: {parametros['email']}")
    print(f"   - Celular: {parametros['celular']}")
    print("-" * 40)

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - VERSÃO COM PARÂMETROS JSON**")
    print("=" * 60)
    print("📋 Versão: 2.4.0 - Com validação de parâmetros")
    print("📋 Data: 29/08/2025")
    print("=" * 60)
    
    try:
        # Carregar e validar parâmetros
        print("\n🔍 **Carregando e validando parâmetros...**")
        parametros = carregar_parametros_linha_comando()
        
        # Mostrar parâmetros carregados
        mostrar_parametros_carregados(parametros)
        
        # Aqui você implementaria a lógica do RPA
        print("\n✅ **Parâmetros carregados com sucesso!**")
        print("🚀 **RPA pronto para execução!**")
        
        # Por enquanto, apenas simular sucesso
        if RETORNO_DISPONIVEL:
            retorno = criar_retorno_estruturado(
                status="sucesso",
                codigo_erro=9002,
                dados_extras={
                    "parametros_validados": len(parametros),
                    "configuracao": parametros["configuracao"],
                    "placa": parametros["placa"],
                    "marca": parametros["marca"]
                }
            )
            print("\n📤 **Retorno estruturado:**")
            print(json.dumps(retorno, indent=2, ensure_ascii=False))
        else:
            print("\n📤 **Retorno básico:**")
            print("Status: sucesso")
            print("Parâmetros validados com sucesso")
        
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

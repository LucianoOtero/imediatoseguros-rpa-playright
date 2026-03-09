#!/usr/bin/env python3
"""
Módulo de Validação de Parâmetros para RPA Tô Segurado
=======================================================

Este módulo valida os parâmetros JSON recebidos via linha de comando,
garantindo que todos os campos obrigatórios estejam presentes e com
tipos corretos.

VERSÃO: 2.4.0
DATA: 29/08/2025
"""

import json
import sys
import re
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

class ValidacaoParametrosError(Exception):
    """Exceção personalizada para erros de validação de parâmetros"""
    pass

class ValidadorParametros:
    """
    Validador de parâmetros para o RPA Tô Segurado
    
    Valida:
    - Presença de campos obrigatórios
    - Tipos de dados corretos
    - Valores permitidos para campos específicos
    - Formato de dados (CPF, CEP, email, etc.)
    """
    
    def __init__(self):
        """Inicializa o validador com as regras de validação"""
        self.definir_regras_validacao()
    
    def definir_regras_validacao(self):
        """Define as regras de validação para cada campo"""
        
        # Campos obrigatórios e seus tipos
        self.campos_obrigatorios = {
            "configuracao": dict,
            "url": str,
            "placa": str,
            "marca": str,
            "modelo": str,
            "ano": str,
            "combustivel": str,
            "veiculo_segurado": str,
            "cep": str,
            "endereco_completo": str,
            "uso_veiculo": str,
            "nome": str,
            "cpf": str,
            "data_nascimento": str,
            "sexo": str,
            "estado_civil": str,
            "email": str,
            "celular": str
        }
        
        # Campos de configuração obrigatórios
        self.campos_configuracao = {
            "log": bool,
            "display": bool,
            "log_rotacao_dias": int,
            "log_nivel": str
        }
        
        # Valores permitidos para campos específicos
        self.valores_permitidos = {
            "combustivel": ["Flex", "Gasolina", "Álcool", "Diesel", "Híbrido", "Hibrido", "Elétrico"],
            "veiculo_segurado": ["Sim", "Não"],
            "sexo": ["Masculino", "Feminino"],
            "estado_civil": ["Solteiro", "Casado", "Divorciado", "Viuvo", "Uniao Estavel", "Casado ou Uniao Estavel", "Casado ou União Estável", "Separado"],
            "uso_veiculo": ["Pessoal", "Profissional", "Motorista de aplicativo", "Taxi"],
            "log_nivel": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        }
        
        # Padrões de validação
        self.padroes = {
            "placa": r"^[A-Z]{3}[0-9]{1}[A-Z0-9]{1}[0-9]{2}$",  # Formato: ABC1D23 ou FPG8D63
            "cpf": r"^\d{11}$",  # 11 dígitos
            "cep": r"^\d{5}-?\d{3}$",  # Formato: 12345-678 ou 12345678
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "celular": r"^\d{11}$",  # Apenas 11 dígitos
            "data_nascimento": r"^\d{2}/\d{2}/\d{4}$"  # Formato: DD/MM/AAAA
        }
        
        # Validações customizadas
        self.validacoes_customizadas = {
            "ano": self.validar_ano,
            "cpf": self.validar_cpf_valido,
            "data_nascimento": self.validar_data_nascimento
        }
    
    def validar_json_string(self, json_string: str) -> Dict[str, Any]:
        """
        Valida e converte uma string JSON
        
        Args:
            json_string: String contendo JSON
            
        Returns:
            Dicionário com os parâmetros validados
            
        Raises:
            ValidacaoParametrosError: Se houver erro de validação
        """
        try:
            # Tentar fazer o parse do JSON
            parametros = json.loads(json_string)
            
            # Validar estrutura e tipos
            self.validar_estrutura(parametros)
            
            # Validar valores específicos
            self.validar_valores(parametros)
            
            # Validar campos customizados
            self.validar_campos_customizados(parametros)
            
            # Validar padrões de formato
            self.validar_padroes(parametros)
            
            return parametros
            
        except json.JSONDecodeError as e:
            raise ValidacaoParametrosError(f"❌ JSON inválido: {str(e)}")
        except Exception as e:
            raise ValidacaoParametrosError(f"❌ Erro de validação: {str(e)}")
    
    def validar_estrutura(self, parametros: Dict[str, Any]):
        """Valida a estrutura básica dos parâmetros"""
        
        # Verificar se é um dicionário
        if not isinstance(parametros, dict):
            raise ValidacaoParametrosError("❌ Parâmetros devem ser um objeto JSON")
        
        # Verificar campos obrigatórios
        campos_faltando = []
        for campo, tipo_esperado in self.campos_obrigatorios.items():
            if campo not in parametros:
                campos_faltando.append(campo)
            elif not isinstance(parametros[campo], tipo_esperado):
                raise ValidacaoParametrosError(
                    f"❌ Campo '{campo}' deve ser do tipo {tipo_esperado.__name__}, "
                    f"recebido: {type(parametros[campo]).__name__}"
                )
        
        if campos_faltando:
            raise ValidacaoParametrosError(
                f"❌ Campos obrigatórios faltando: {', '.join(campos_faltando)}"
            )
        
        # Validar estrutura da configuração
        self.validar_configuracao(parametros["configuracao"])
    
    def validar_configuracao(self, config: Dict[str, Any]):
        """Valida os campos de configuração"""
        
        if not isinstance(config, dict):
            raise ValidacaoParametrosError("❌ Campo 'configuracao' deve ser um objeto")
        
        # Verificar campos de configuração obrigatórios
        campos_config_faltando = []
        for campo, tipo_esperado in self.campos_configuracao.items():
            if campo not in config:
                campos_config_faltando.append(campo)
            elif not isinstance(config[campo], tipo_esperado):
                raise ValidacaoParametrosError(
                    f"❌ Campo 'configuracao.{campo}' deve ser do tipo {tipo_esperado.__name__}, "
                    f"recebido: {type(config[campo]).__name__}"
                )
        
        if campos_config_faltando:
            raise ValidacaoParametrosError(
                f"❌ Campos de configuração obrigatórios faltando: {', '.join(campos_config_faltando)}"
            )
        
        # Validar valores específicos da configuração
        if config["log_rotacao_dias"] <= 0:
            raise ValidacaoParametrosError("❌ Campo 'log_rotacao_dias' deve ser maior que 0")
    
    def validar_valores(self, parametros: Dict[str, Any]):
        """Valida valores específicos dos campos"""
        
        for campo, valores_permitidos in self.valores_permitidos.items():
            if campo in parametros:
                valor = parametros[campo]
                if valor not in valores_permitidos:
                    raise ValidacaoParametrosError(
                        f"❌ Campo '{campo}' deve ter um dos valores: {', '.join(valores_permitidos)}. "
                        f"Recebido: '{valor}'"
                    )
    
    def validar_campos_customizados(self, parametros: Dict[str, Any]):
        """Executa validações customizadas para campos específicos"""
        
        for campo, funcao_validacao in self.validacoes_customizadas.items():
            if campo in parametros:
                try:
                    funcao_validacao(parametros[campo])
                except Exception as e:
                    raise ValidacaoParametrosError(f"❌ Campo '{campo}': {str(e)}")
    
    def validar_ano(self, ano: str):
        """Valida o ano do veículo"""
        try:
            ano_int = int(ano)
            ano_atual = datetime.now().year
            if ano_int < 1900 or ano_int > ano_atual + 1:
                raise ValueError(f"Ano deve estar entre 1900 e {ano_atual + 1}")
        except ValueError as e:
            if "Ano deve estar" in str(e):
                raise e
            raise ValueError("Ano deve ser um número válido")
    
    def validar_cpf_valido(self, cpf: str):
        """Valida se o CPF é válido (algoritmo básico)"""
        # Remover caracteres não numéricos
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        
        # Verificar se todos os dígitos são iguais
        if cpf_limpo == cpf_limpo[0] * 11:
            raise ValueError("CPF não pode ter todos os dígitos iguais")
        
        # Algoritmo de validação do CPF
        soma = 0
        for i in range(9):
            soma += int(cpf_limpo[i]) * (10 - i)
        
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto
        
        soma = 0
        for i in range(10):
            soma += int(cpf_limpo[i]) * (11 - i)
        
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto
        
        if cpf_limpo[9] != str(digito1) or cpf_limpo[10] != str(digito2):
            raise ValueError("CPF inválido (dígitos verificadores incorretos)")
    
    def validar_data_nascimento(self, data: str):
        """Valida a data de nascimento"""
        try:
            # Verificar formato
            if not re.match(self.padroes["data_nascimento"], data):
                raise ValueError("Data deve estar no formato DD/MM/AAAA")
            
            # Converter para datetime
            data_obj = datetime.strptime(data, "%d/%m/%Y")
            data_atual = datetime.now()
            
            # Verificar se não é no futuro
            if data_obj > data_atual:
                raise ValueError("Data de nascimento não pode ser no futuro")
            
            # Verificar se não é muito antiga (mais de 150 anos)
            if data_atual.year - data_obj.year > 150:
                raise ValueError("Data de nascimento muito antiga (mais de 150 anos)")
                
        except ValueError as e:
            if "Data deve estar" in str(e) or "Data de nascimento" in str(e):
                raise e
            raise ValueError("Data de nascimento inválida")
    
    def validar_parametros(self, parametros: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida parâmetros diretamente (sem JSON string)
        
        Args:
            parametros: Dicionário com parâmetros
            
        Returns:
            Dicionário com os parâmetros validados
            
        Raises:
            ValidacaoParametrosError: Se houver erro de validação
        """
        try:
            # Validar estrutura e tipos
            self.validar_estrutura(parametros)
            
            # Validar valores específicos
            self.validar_valores(parametros)
            
            # Validar campos customizados
            self.validar_campos_customizados(parametros)
            
            # Validar padrões de formato
            self.validar_padroes(parametros)
            
            return parametros
            
        except Exception as e:
            if isinstance(e, ValidacaoParametrosError):
                raise e
            else:
                raise ValidacaoParametrosError(f"❌ Erro de validação: {str(e)}")

    def validar_padroes(self, parametros: Dict[str, Any]):
        """Valida padrões de formato para campos específicos"""
        
        for campo, padrao in self.padroes.items():
            if campo in parametros:
                valor = parametros[campo]
                if not re.match(padrao, valor):
                    raise ValidacaoParametrosError(
                        f"❌ Campo '{campo}' não está no formato correto. "
                        f"Valor recebido: '{valor}'"
                    )
    
    def obter_json_exemplo(self) -> str:
        """Retorna um exemplo de JSON válido"""
        exemplo = {
            "configuracao": {
                "log": True,
                "display": True,
                "log_rotacao_dias": 90,
                "log_nivel": "INFO"
            },
            "url": "https://app.tosegurado.com.br/imediatoseguros",
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
            "cpf": "08554607848",  # CPF válido
            "data_nascimento": "01/01/1980",
            "sexo": "Masculino",
            "estado_civil": "Casado",
            "email": "exemplo@email.com",
            "celular": "(11) 97668-7668"
        }
        return json.dumps(exemplo, indent=2, ensure_ascii=False)
    
    def obter_ajuda(self) -> str:
        """Retorna texto de ajuda para uso do script"""
        return """
🔧 **USO DO SCRIPT COM PARÂMETROS JSON**

O script deve ser chamado com um JSON contendo todos os parâmetros necessários.

📋 **Sintaxe:**
python executar_todas_telas_corrigido.py '{"parametros": "aqui"}'

📋 **Exemplo:**
python executar_todas_telas_corrigido.py '{"configuracao": {"log": true, "display": true}, "placa": "ABC1234", ...}'

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
"""

def validar_parametros_json(parametros: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função de compatibilidade para validar parâmetros JSON
    
    Args:
        parametros: Dicionário com parâmetros
        
    Returns:
        Dicionário com resultado da validação
    """
    try:
        validador = ValidadorParametros()
        parametros_validados = validador.validar_json_string(json.dumps(parametros))
        return {
            "sucesso": True,
            "mensagem": "Parâmetros validados com sucesso",
            "parametros": parametros_validados
        }
    except ValidacaoParametrosError as e:
        return {
            "sucesso": False,
            "mensagem": str(e)
        }
    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro inesperado na validação: {str(e)}"
        }

def validar_parametros_entrada(json_string: str) -> Dict[str, Any]:
    """
    Função principal para validar parâmetros de entrada
    
    Args:
        json_string: String contendo JSON com parâmetros
        
    Returns:
        Dicionário com parâmetros validados
        
    Raises:
        ValidacaoParametrosError: Se houver erro de validação
    """
    validador = ValidadorParametros()
    return validador.validar_json_string(json_string)

def main():
    """Função principal para teste do módulo"""
    print("🧪 **TESTE DO MÓDULO DE VALIDAÇÃO DE PARÂMETROS**")
    print("=" * 60)
    
    validador = ValidadorParametros()
    
    # Teste 1: JSON válido
    print("\n🟢 **TESTE 1: JSON VÁLIDO**")
    print("-" * 40)
    
    json_valido = validador.obter_json_exemplo()
    print("JSON de teste:")
    print(json_valido)
    
    try:
        parametros_validados = validador.validar_json_string(json_valido)
        print("\n✅ JSON válido! Parâmetros aceitos.")
        print(f"Total de campos: {len(parametros_validados)}")
        
    except ValidacaoParametrosError as e:
        print(f"\n❌ Erro de validação: {e}")
    
    # Teste 2: JSON inválido (campo faltando)
    print("\n🔴 **TESTE 2: CAMPO OBRIGATÓRIO FALTANDO**")
    print("-" * 50)
    
    json_invalido = '{"placa": "ABC1234", "marca": "FORD"}'
    print(f"JSON inválido: {json_invalido}")
    
    try:
        validador.validar_json_string(json_invalido)
        print("✅ JSON aceito (não deveria ser)")
    except ValidacaoParametrosError as e:
        print(f"❌ Erro esperado: {e}")
    
    # Teste 3: JSON inválido (tipo incorreto)
    print("\n🔴 **TESTE 3: TIPO DE CAMPO INCORRETO**")
    print("-" * 50)
    
    json_tipo_errado = '{"configuracao": {"log": "true"}, "placa": 123, "marca": "FORD"}'
    print(f"JSON com tipo incorreto: {json_tipo_errado}")
    
    try:
        validador.validar_json_string(json_tipo_errado)
        print("✅ JSON aceito (não deveria ser)")
    except ValidacaoParametrosError as e:
        print(f"❌ Erro esperado: {e}")
    
    # Mostrar ajuda
    print("\n📚 **AJUDA DE USO**")
    print("-" * 30)
    print(validador.obter_ajuda())

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SISTEMA DE RETORNO ESTRUTURADO
==============================

Módulo para criação de retornos estruturados padronizados
com códigos de status, logs, erros e warnings organizados.

VERSÃO: 3.0.0
DATA: 2025-09-02
AUTOR: Luciano Otero
"""

import json
from datetime import datetime
from typing import Dict, Any
from .codigos_retorno import obter_mensagem_codigo, validar_codigo


# ========================================
# CLASSE RETORNO ESTRUTURADO
# ========================================

class RetornoEstruturado:
    """
    Classe para criação de retornos estruturados padronizados
    """

    def __init__(self, versao: str = "3.0.0", sistema: str = "RPA Tô Segurado - Playwright"):
        self.versao = versao
        self.sistema = sistema
        self.status = None
        self.codigo = None
        self.mensagem = None
        self.timestamp = datetime.now().isoformat()
        self.tempo_execucao = None
        self.dados = {}
        self.logs = []
        self.erros = []
        self.warnings = []

    def definir_sucesso(self, codigo: int, mensagem: str = None):
        """Define o retorno como sucesso"""
        if not validar_codigo(codigo):
            raise ValueError(f"Código {codigo} inválido")
        
        self.status = "success"
        self.codigo = codigo
        self.mensagem = mensagem or obter_mensagem_codigo(codigo)

    def definir_erro(self, codigo: int, mensagem: str = None):
        """Define o retorno como erro"""
        if not validar_codigo(codigo):
            raise ValueError(f"Código {codigo} inválido")
        
        self.status = "error"
        self.codigo = codigo
        self.mensagem = mensagem or obter_mensagem_codigo(codigo)

    def definir_warning(self, codigo: int, mensagem: str = None):
        """Define o retorno como warning"""
        if not validar_codigo(codigo):
            raise ValueError(f"Código {codigo} inválido")
        
        self.status = "warning"
        self.codigo = codigo
        self.mensagem = mensagem or obter_mensagem_codigo(codigo)

    def adicionar_dados(self, chave: str, valor: Any):
        """Adiciona dados ao retorno"""
        self.dados[chave] = valor

    def adicionar_log(self, mensagem: str, nivel: str = "INFO", timestamp: str = None):
        """Adiciona um log ao retorno"""
        self.logs.append({
            "timestamp": timestamp or datetime.now().isoformat(),
            "nivel": nivel,
            "mensagem": mensagem
        })

    def adicionar_erro(self, erro: Dict[str, Any]):
        """Adiciona um erro ao retorno"""
        self.erros.append(erro)

    def adicionar_warning(self, warning: Dict[str, Any]):
        """Adiciona um warning ao retorno"""
        self.warnings.append(warning)

    def adicionar_logs_do_exception_handler(self, exception_handler):
        """Adiciona logs do exception handler"""
        if hasattr(exception_handler, 'obter_resumo_erros'):
            resumo = exception_handler.obter_resumo_erros()
            if 'erros' in resumo:
                for erro in resumo['erros']:
                    self.adicionar_erro(erro)
            if 'warnings' in resumo:
                for warning in resumo['warnings']:
                    self.adicionar_warning(warning)

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "status": self.status,
            "codigo": self.codigo,
            "mensagem": self.mensagem,
            "timestamp": self.timestamp,
            "tempo_execucao": self.tempo_execucao,
            "versao": self.versao,
            "sistema": self.sistema,
            "dados": self.dados,
            "logs": self.logs,
            "erros": {
                "total_erros": len(self.erros),
                "total_warnings": len(self.warnings),
                "erros": self.erros,
                "warnings": self.warnings
            }
        }

    def to_json(self, indent: int = 2, ensure_ascii: bool = False) -> str:
        """Converte para JSON string"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=ensure_ascii)

    def validar_estrutura(self) -> bool:
        """Valida se a estrutura está correta"""
        if not self.status or not self.codigo or not self.mensagem:
            return False
        return True

    def obter_resumo(self) -> Dict[str, Any]:
        """Obtém um resumo do retorno"""
        return {
            "status": self.status,
            "codigo": self.codigo,
            "mensagem": self.mensagem,
            "total_logs": len(self.logs),
            "total_erros": len(self.erros),
            "total_warnings": len(self.warnings),
            "total_dados": len(self.dados)
        }

    def limpar_logs(self):
        """Limpa todos os logs"""
        self.logs = []

    def limpar_erros(self):
        """Limpa todos os erros"""
        self.erros = []

    def limpar_warnings(self):
        """Limpa todos os warnings"""
        self.warnings = []

    def limpar_dados(self):
        """Limpa todos os dados"""
        self.dados = {}

    def limpar_tudo(self):
        """Limpa logs, erros, warnings e dados"""
        self.limpar_logs()
        self.limpar_erros()
        self.limpar_warnings()
        self.limpar_dados()


# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def criar_retorno_sucesso(
    telas_executadas: Dict[str, bool],
    dados_planos: Dict[str, Any],
    arquivo_dados: str,
    tempo_execucao: float,
    parametros: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Cria um retorno de sucesso estruturado
    
    PARÂMETROS:
        telas_executadas: Dict[str, bool] - Status das telas executadas
        dados_planos: Dict[str, Any] - Dados dos planos capturados
        arquivo_dados: str - Nome do arquivo salvo
        tempo_execucao: float - Tempo de execução em segundos
        parametros: Dict[str, Any] - Parâmetros de entrada
        
    RETORNO:
        Dict[str, Any]: Retorno estruturado de sucesso
    """
    retorno = RetornoEstruturado()
    
    # Definir sucesso
    retorno.definir_sucesso(9002, "RPA executado com sucesso - Todas as telas")
    
    # Adicionar dados
    retorno.adicionar_dados("telas_executadas", telas_executadas)
    retorno.adicionar_dados("dados_planos", dados_planos)
    retorno.adicionar_dados("arquivo_dados", arquivo_dados)
    retorno.adicionar_dados("parametros_entrada", parametros)
    
    # Definir tempo de execução
    retorno.tempo_execucao = tempo_execucao
    
    return retorno.to_dict()


def criar_retorno_erro(
    erro: str,
    tela_falhou: str,
    tempo_execucao: float,
    parametros: Dict[str, Any],
    exception_handler
) -> Dict[str, Any]:
    """
    Cria um retorno de erro estruturado
    
    PARÂMETROS:
        erro: str - Mensagem de erro
        tela_falhou: str - Nome da tela que falhou
        tempo_execucao: float - Tempo de execução em segundos
        parametros: Dict[str, Any] - Parâmetros de entrada
        exception_handler: ExceptionHandler - Handler de exceções
        
    RETORNO:
        Dict[str, Any]: Retorno estruturado de erro
    """
    retorno = RetornoEstruturado()
    
    # Definir erro
    retorno.definir_erro(9102, f"Erro na navegação - {erro}")
    
    # Adicionar dados
    retorno.adicionar_dados("tela_falhou", tela_falhou)
    retorno.adicionar_dados("parametros_entrada", parametros)
    
    # Adicionar logs do exception handler
    retorno.adicionar_logs_do_exception_handler(exception_handler)
    
    # Definir tempo de execução
    retorno.tempo_execucao = tempo_execucao
    
    return retorno.to_dict()


def criar_retorno_warning(
    warning: str,
    tela: str,
    tempo_execucao: float,
    parametros: Dict[str, Any],
    exception_handler
) -> Dict[str, Any]:
    """
    Cria um retorno de warning estruturado
    
    PARÂMETROS:
        warning: str - Mensagem de warning
        tela: str - Nome da tela
        tempo_execucao: float - Tempo de execução em segundos
        parametros: Dict[str, Any] - Parâmetros de entrada
        exception_handler: ExceptionHandler - Handler de exceções
        
    RETORNO:
        Dict[str, Any]: Retorno estruturado de warning
    """
    retorno = RetornoEstruturado()
    
    # Definir warning
    retorno.definir_warning(9201, f"Warning - {warning}")
    
    # Adicionar dados
    retorno.adicionar_dados("tela", tela)
    retorno.adicionar_dados("parametros_entrada", parametros)
    
    # Adicionar logs do exception handler
    retorno.adicionar_logs_do_exception_handler(exception_handler)
    
    # Definir tempo de execução
    retorno.tempo_execucao = tempo_execucao
    
    return retorno.to_dict()


def validar_retorno_estruturado(retorno: Dict[str, Any]) -> bool:
    """
    Valida se um retorno está estruturado corretamente
    
    PARÂMETROS:
        retorno: Dict[str, Any] - Retorno a ser validado
        
    RETORNO:
        bool: True se válido, False caso contrário
    """
    campos_obrigatorios = [
        "status", "codigo", "mensagem", "timestamp", "versao", "sistema"
    ]
    
    # Verificar campos obrigatórios
    for campo in campos_obrigatorios:
        if campo not in retorno:
            return False
    
    # Validar tipos
    if not isinstance(retorno["status"], str):
        return False
    
    if not isinstance(retorno["codigo"], int):
        return False
    
    # Validar valores permitidos
    if retorno["status"] not in ["success", "error", "warning"]:
        return False
    
    return True


def obter_resumo_retorno(retorno: Dict[str, Any]) -> Dict[str, Any]:
    """
    Obtém um resumo do retorno estruturado
    
    PARÂMETROS:
        retorno: Dict[str, Any] - Retorno estruturado
        
    RETORNO:
        Dict[str, Any]: Resumo com estatísticas
    """
    if not validar_retorno_estruturado(retorno):
        return {"erro": "Retorno inválido"}
    
    dados = retorno.get("dados", {})
    erros = retorno.get("erros", {})
    
    return {
        "status": retorno["status"],
        "codigo": retorno["codigo"],
        "mensagem": retorno["mensagem"],
        "total_logs": len(retorno.get("logs", [])),
        "total_erros": erros.get("total_erros", 0),
        "total_warnings": erros.get("total_warnings", 0),
        "total_telas": len(dados.get("telas_executadas", {})),
        "total_planos": len(dados.get("dados_planos", {}).get("planos", [])),
        "tempo_execucao": retorno.get("tempo_execucao", "N/A")
    }


def converter_retorno_antigo_para_estruturado(
    retorno_antigo: Dict[str, Any],
    parametros: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Converte um retorno antigo para o formato estruturado
    
    PARÂMETROS:
        retorno_antigo: Dict[str, Any] - Retorno no formato antigo
        parametros: Dict[str, Any] - Parâmetros de entrada
        
    RETORNO:
        Dict[str, Any]: Retorno no formato estruturado
    """
    retorno = RetornoEstruturado()
    
    # Determinar status e código baseado no retorno antigo
    if retorno_antigo.get("status") == "success":
        retorno.definir_sucesso(9002, "RPA executado com sucesso")
    elif retorno_antigo.get("status") == "error":
        erro_msg = retorno_antigo.get("erro", "Erro desconhecido")
        retorno.definir_erro(9108, erro_msg)
    else:
        retorno.definir_warning(9201, "Status desconhecido")
    
    # Adicionar dados do retorno antigo
    if "telas_executadas" in retorno_antigo:
        retorno.adicionar_dados("telas_executadas", retorno_antigo["telas_executadas"])
    
    if "dados_planos" in retorno_antigo:
        retorno.adicionar_dados("dados_planos", retorno_antigo["dados_planos"])
    
    if "arquivo_dados" in retorno_antigo:
        retorno.adicionar_dados("arquivo_dados", retorno_antigo["arquivo_dados"])
    
    if "tempo_execucao" in retorno_antigo:
        retorno.adicionar_dados("tempo_execucao", retorno_antigo["tempo_execucao"])
    
    # Adicionar parâmetros
    retorno.adicionar_dados("parametros_entrada", parametros)
    
    return retorno.to_dict()

"""
Módulo de Logging para RPA Tô Segurado
=======================================

Este módulo implementa um sistema de logging robusto com as seguintes funcionalidades:

- Logging configurável (ativado/desativado via JSON)
- Rotação automática de arquivos a cada 90 dias
- Diferentes níveis de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Formato estruturado com timestamp, nível, linha e mensagem
- Suporte a logging em arquivo e console
- Sistema de códigos de erro padronizados

Autor: Assistente IA
Data: 29/08/2025
Versão: 1.0.0
"""

import os
import json
import logging
import logging.handlers
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
import traceback
import inspect

# Importar controle de display do arquivo principal
try:
    from executar_rpa_imediato_playwright import DISPLAY_ENABLED
except ImportError:
    DISPLAY_ENABLED = True  # Fallback para compatibilidade

class RPALogger:
    """
    Sistema de logging robusto para RPA com rotação automática
    """
    
    # Códigos de erro padronizados
    ERROR_CODES = {
        # Erros de configuração (1000-1999)
        "CONFIG_LOAD_ERROR": 1001,
        "CONFIG_INVALID": 1002,
        "CHROME_DRIVER_ERROR": 1003,
        "BROWSER_INIT_ERROR": 1004,
        
        # Erros de navegação (2000-2999)
        "NAVIGATION_TIMEOUT": 2001,
        "ELEMENT_NOT_FOUND": 2002,
        "ELEMENT_NOT_CLICKABLE": 2003,
        "PAGE_NOT_LOADED": 2004,
        "REDIRECT_ERROR": 2005,
        
        # Erros de automação (3000-3999)
        "CLICK_FAILED": 3001,
        "INPUT_FAILED": 3002,
        "WAIT_TIMEOUT": 3003,
        "STALE_ELEMENT": 3004,
        "JAVASCRIPT_ERROR": 3005,
        
        # Erros de sistema (4000-4999)
        "NETWORK_ERROR": 4001,
        "MEMORY_ERROR": 4002,
        "DISK_ERROR": 4003,
        "PERMISSION_ERROR": 4004,
        
        # Erros de validação (5000-5999)
        "DATA_INVALID": 5001,
        "FORMAT_ERROR": 5002,
        "VALIDATION_FAILED": 5003,
        
        # Sucessos (9000-9999)
        "TELA_COMPLETADA": 9001,
        "RPA_SUCESSO": 9002,
        "ELEMENTO_ENCONTRADO": 9003,
        "ACAO_REALIZADA": 9004
    }
    
    # Mensagens de erro padronizadas
    ERROR_MESSAGES = {
        # Erros de configuração
        1001: "Erro ao carregar arquivo de configuração",
        1002: "Configuração inválida ou incompleta",
        1003: "Erro no ChromeDriver",
        1004: "Erro ao inicializar navegador",
        
        # Erros de navegação
        2001: "Timeout na navegação",
        2002: "Elemento não encontrado na página",
        2003: "Elemento não está clicável",
        2004: "Página não carregou completamente",
        2005: "Erro no redirecionamento",
        
        # Erros de automação
        3001: "Falha ao clicar no elemento",
        3002: "Falha ao inserir dados no campo",
        3003: "Timeout aguardando elemento",
        3004: "Elemento obsoleto (stale)",
        3005: "Erro na execução de JavaScript",
        
        # Erros de sistema
        4001: "Erro de conexão de rede",
        4002: "Erro de memória insuficiente",
        4003: "Erro de disco/arquivo",
        4004: "Erro de permissão",
        
        # Erros de validação
        5001: "Dados inválidos fornecidos",
        5002: "Formato de dados incorreto",
        5003: "Validação falhou",
        
        # Sucessos
        9001: "Tela executada com sucesso",
        9002: "RPA executado com sucesso",
        9003: "Elemento encontrado e processado",
        9004: "Ação realizada com sucesso"
    }
    
    def __init__(self, config_path: str = "parametros.json"):
        """
        Inicializa o sistema de logging
        
        Args:
            config_path: Caminho para o arquivo de configuração
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = None
        self.log_file = None
        self._setup_logger()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega configuração do arquivo JSON
        
        Returns:
            Dicionário com configurações
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Configurações padrão se não existirem
            default_config = {
                "log": True,
                "display": True,
                "log_rotacao_dias": 90,
                "log_nivel": "INFO"
            }
            
            if "configuracao" not in config:
                config["configuracao"] = default_config
            else:
                # Mescla com configurações padrão
                for key, value in default_config.items():
                    if key not in config["configuracao"]:
                        config["configuracao"][key] = value
            
            return config
            
        except Exception as e:
            # Fallback para configuração padrão
            return {
                "configuracao": {
                    "log": True,
                    "display": True,
                    "log_rotacao_dias": 90,
                    "log_nivel": "INFO"
                }
            }
    
    def _setup_logger(self):
        """
        Configura o sistema de logging
        """
        if not self.config["configuracao"]["log"]:
            return
        
        # Criar diretório de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Nome do arquivo de log com timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        self.log_file = log_dir / f"rpa_tosegurado_{timestamp}.log"
        
        # Configurar logger
        self.logger = logging.getLogger("RPA_TO_SEGURADO")
        self.logger.setLevel(self._get_log_level())
        
        # Evitar duplicação de handlers
        if self.logger.handlers:
            return
        
        # Handler para arquivo com rotação
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=self.log_file,
            when='midnight',
            interval=1,
            backupCount=self.config["configuracao"]["log_rotacao_dias"],
            encoding='utf-8'
        )
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Limpar logs antigos
        self._cleanup_old_logs()
    
    def _get_log_level(self) -> int:
        """
        Converte string de nível para constante do logging
        
        Returns:
            Nível de logging como constante
        """
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        
        level_str = self.config["configuracao"]["log_nivel"].upper()
        return level_map.get(level_str, logging.INFO)
    
    def _cleanup_old_logs(self):
        """
        Remove logs mais antigos que o período de rotação
        """
        try:
            log_dir = Path("logs")
            if not log_dir.exists():
                return
            
            cutoff_date = datetime.now() - timedelta(
                days=self.config["configuracao"]["log_rotacao_dias"]
            )
            
            for log_file in log_dir.glob("rpa_tosegurado_*.log"):
                try:
                    # Extrair data do nome do arquivo
                    date_str = log_file.stem.split("_")[-1]
                    file_date = datetime.strptime(date_str, "%Y%m%d")
                    
                    if file_date < cutoff_date:
                        log_file.unlink()
                        if self.config["configuracao"]["display"]:
                            print(f"🗑️ Log antigo removido: {log_file.name}")
                except:
                    continue
                    
        except Exception:
            pass  # Ignora erros de limpeza
    
    def _get_caller_info(self) -> str:
        """
        Obtém informações sobre quem chamou o log
        
        Returns:
            String com informações do caller
        """
        try:
            frame = inspect.currentframe().f_back
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            func_name = frame.f_code.co_name
            
            # Extrair apenas o nome do arquivo
            filename = os.path.basename(filename)
            
            return f"{filename}:{lineno}:{func_name}"
        except:
            return "unknown:0:unknown"
    
    def log(self, level: str, message: str, error_code: Optional[int] = None, 
            extra_data: Optional[Dict[str, Any]] = None):
        """
        Registra uma mensagem de log
        
        Args:
            level: Nível do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Mensagem a ser registrada
            error_code: Código de erro opcional
            extra_data: Dados extras para incluir no log
        """
        if not self.config["configuracao"]["log"]:
            return
        
        # Adicionar código de erro se fornecido
        if error_code:
            error_msg = self.ERROR_MESSAGES.get(error_code, "Código de erro desconhecido")
            message = f"[ERR-{error_code}] {error_msg}: {message}"
        
        # Adicionar dados extras
        if extra_data:
            extra_str = " | ".join([f"{k}={v}" for k, v in extra_data.items()])
            message = f"{message} | {extra_str}"
        
        # Adicionar informações do caller
        caller_info = self._get_caller_info()
        full_message = f"{message} | Caller: {caller_info}"
        
        # Registrar no arquivo
        if self.logger:
            log_method = getattr(self.logger, level.lower(), self.logger.info)
            log_method(full_message)
        
        # Exibir no console se configurado
        if self.config["configuracao"]["display"]:
            timestamp = datetime.now().strftime("%H:%M:%S")
            level_icon = self._get_level_icon(level)
            print(f"{level_icon} {timestamp} | {level.upper():8} | {message}")
    
    def _get_level_icon(self, level: str) -> str:
        """
        Retorna ícone para cada nível de log
        
        Args:
            level: Nível do log
            
        Returns:
            Ícone correspondente
        """
        icons = {
            "DEBUG": "🔍",
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "CRITICAL": "🚨"
        }
        return icons.get(level.upper(), "ℹ️")
    
    # Métodos de conveniência para diferentes níveis
    def debug(self, message: str, error_code: Optional[int] = None, 
              extra_data: Optional[Dict[str, Any]] = None):
        """Log de debug"""
        self.log("DEBUG", message, error_code, extra_data)
    
    def info(self, message: str, error_code: Optional[int] = None, 
             extra_data: Optional[Dict[str, Any]] = None):
        """Log de informação"""
        self.log("INFO", message, error_code, extra_data)
    
    def warning(self, message: str, error_code: Optional[int] = None, 
                extra_data: Optional[Dict[str, Any]] = None):
        """Log de aviso"""
        self.log("WARNING", message, error_code, extra_data)
    
    def error(self, message: str, error_code: Optional[int] = None, 
              extra_data: Optional[Dict[str, Any]] = None):
        """Log de erro"""
        self.log("ERROR", message, error_code, extra_data)
    
    def critical(self, message: str, error_code: Optional[int] = None, 
                extra_data: Optional[Dict[str, Any]] = None):
        """Log crítico"""
        self.log("CRITICAL", message, error_code, extra_data)
    
    def success(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log de sucesso"""
        self.log("INFO", message, 9002, extra_data)  # Código de sucesso padrão
    
    def log_exception(self, message: str, error_code: Optional[int] = None, 
                      extra_data: Optional[Dict[str, Any]] = None):
        """
        Registra uma exceção com traceback completo
        
        Args:
            message: Mensagem principal
            error_code: Código de erro opcional
            extra_data: Dados extras
        """
        if not self.config["configuracao"]["log"]:
            return
        
        # Obter traceback completo
        tb = traceback.format_exc()
        
        # Adicionar traceback aos dados extras
        if extra_data is None:
            extra_data = {}
        extra_data["traceback"] = tb
        
        # Registrar como erro crítico
        self.critical(f"EXCEÇÃO: {message}", error_code, extra_data)
    
    def get_log_file_path(self) -> Optional[str]:
        """
        Retorna o caminho do arquivo de log atual
        
        Returns:
            Caminho do arquivo de log ou None se logging desabilitado
        """
        return str(self.log_file) if self.log_file else None
    
    def is_logging_enabled(self) -> bool:
        """
        Verifica se o logging está habilitado
        
        Returns:
            True se logging habilitado, False caso contrário
        """
        return self.config["configuracao"]["log"]
    
    def is_display_enabled(self) -> bool:
        """
        Verifica se o display está habilitado
        
        Returns:
            True se display habilitado, False caso contrário
        """
        return self.config["configuracao"]["display"]


# Instância global do logger
rpa_logger = RPALogger()

# Funções de conveniência para uso direto
def log_debug(message: str, error_code: Optional[int] = None, 
              extra_data: Optional[Dict[str, Any]] = None):
    """Log de debug"""
    rpa_logger.debug(message, error_code, extra_data)

def log_info(message: str, error_code: Optional[int] = None, 
             extra_data: Optional[Dict[str, Any]] = None):
    """Log de informação com controle de saída"""
    try:
        # Sempre salvar no arquivo de log
        rpa_logger.info(message, error_code, extra_data)
        
        # Controlar saída do console baseado em DISPLAY_ENABLED
        if not DISPLAY_ENABLED:
            # Silenciar saída do console temporariamente
            # (mantém arquivo de log funcionando)
            for handler in rpa_logger.logger.handlers:
                if isinstance(handler, logging.StreamHandler) and handler.stream.name == '<stderr>':
                    handler.setLevel(logging.CRITICAL)
    except Exception as e:
        # Fallback silencioso
        pass

def log_error(message: str, error_code: Optional[int] = None, 
              extra_data: Optional[Dict[str, Any]] = None):
    """Log de erro"""
    rpa_logger.error(message, error_code, extra_data)

def log_success(message: str, extra_data: Optional[Dict[str, Any]] = None):
    """Log de sucesso"""
    rpa_logger.success(message, extra_data)

def log_warning(message: str, error_code: Optional[int] = None, 
                extra_data: Optional[Dict[str, Any]] = None):
    """Log de aviso"""
    rpa_logger.warning(message, error_code, extra_data)

def log_exception(message: str, error_code: Optional[int] = None, 
                  extra_data: Optional[Dict[str, Any]] = None):
    """Log de exceção"""
    rpa_logger.log_exception(message, error_code, extra_data)

def setup_logger():
    """
    Função de compatibilidade para configurar o logger
    """
    # O logger já é configurado automaticamente na instância global
    pass

def exibir_mensagem(mensagem: str, nivel: str = "INFO"):
    """
    Função de compatibilidade para exibir mensagens
    
    Args:
        mensagem: Mensagem a ser exibida
        nivel: Nível da mensagem (INFO, DEBUG, WARNING, ERROR)
    """
    if nivel == "INFO":
        rpa_logger.info(mensagem)
    elif nivel == "DEBUG":
        rpa_logger.debug(mensagem)
    elif nivel == "WARNING":
        rpa_logger.warning(mensagem)
    elif nivel == "ERROR":
        rpa_logger.error(mensagem)
    else:
        rpa_logger.info(mensagem)

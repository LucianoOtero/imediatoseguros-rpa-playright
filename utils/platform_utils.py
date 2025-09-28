# 🖥️ PLATFORM UTILS - DETECÇÃO E COMPATIBILIDADE MULTIPLATAFORMA
"""
Módulo para detecção de plataforma e compatibilidade multiplataforma.
Implementa detecção segura de Windows/Linux e configurações específicas.
"""

import os
import sys
import platform
import subprocess
from typing import Dict, Any, Optional
import json
import logging

class PlatformUtils:
    """Utilitário para detecção e configuração de plataforma"""
    
    _instance = None
    _platform_info = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_platform_info(cls) -> Dict[str, Any]:
        """Obtém informações detalhadas da plataforma"""
        if cls._platform_info is None:
            cls._platform_info = {
                "os": platform.system().lower(),
                "os_version": platform.version(),
                "architecture": platform.machine(),
                "python_version": sys.version,
                "python_executable": sys.executable,
                "is_windows": platform.system().lower() == "windows",
                "is_linux": platform.system().lower() == "linux",
                "is_mac": platform.system().lower() == "darwin",
                "shell": cls._detect_shell(),
                "path_separator": os.sep,
                "line_separator": os.linesep
            }
        return cls._platform_info
    
    @classmethod
    def _detect_shell(cls) -> str:
        """Detecta o shell atual"""
        try:
            if platform.system().lower() == "windows":
                # Windows - detectar PowerShell ou CMD
                shell = os.environ.get('SHELL', '')
                if 'powershell' in shell.lower() or 'pwsh' in shell.lower():
                    return 'powershell'
                elif 'cmd' in shell.lower():
                    return 'cmd'
                else:
                    return 'powershell'  # Default para Windows
            else:
                # Linux/Mac
                shell = os.environ.get('SHELL', '/bin/bash')
                return os.path.basename(shell)
        except Exception:
            return 'unknown'
    
    @classmethod
    def get_redis_config(cls) -> Dict[str, Any]:
        """Obtém configuração Redis específica da plataforma"""
        platform_info = cls.get_platform_info()
        
        if platform_info["is_windows"]:
            return {
                "host": "localhost",
                "port": 6379,
                "db": 0,
                "decode_responses": True,
                "socket_connect_timeout": 5,
                "socket_timeout": 5,
                "retry_on_timeout": True,
                "health_check_interval": 30
            }
        else:
            return {
                "host": "localhost",
                "port": 6379,
                "db": 0,
                "decode_responses": True,
                "socket_connect_timeout": 5,
                "socket_timeout": 5,
                "retry_on_timeout": True,
                "health_check_interval": 30,
                "unix_socket_path": None  # Para Linux
            }
    
    @classmethod
    def get_websocket_config(cls) -> Dict[str, Any]:
        """Obtém configuração WebSocket específica da plataforma"""
        platform_info = cls.get_platform_info()
        
        if platform_info["is_windows"]:
            return {
                "host": "localhost",
                "port": 8765,
                "max_connections": 100,
                "ping_interval": 20,
                "ping_timeout": 10,
                "close_timeout": 10,
                "max_size": 2**20,  # 1MB
                "compression": None
            }
        else:
            return {
                "host": "0.0.0.0",
                "port": 8765,
                "max_connections": 100,
                "ping_interval": 20,
                "ping_timeout": 10,
                "close_timeout": 10,
                "max_size": 2**20,  # 1MB
                "compression": None
            }
    
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """Obtém configuração de logging específica da plataforma"""
        platform_info = cls.get_platform_info()
        
        if platform_info["is_windows"]:
            return {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "handlers": ["console", "file"],
                "file_path": "logs/rpa_system.log",
                "max_bytes": 10 * 1024 * 1024,  # 10MB
                "backup_count": 5
            }
        else:
            return {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "handlers": ["console", "file", "syslog"],
                "file_path": "/var/log/rpa_system.log",
                "max_bytes": 10 * 1024 * 1024,  # 10MB
                "backup_count": 5
            }
    
    @classmethod
    def check_redis_availability(cls) -> bool:
        """Verifica se Redis está disponível"""
        try:
            import redis
            platform_info = cls.get_platform_info()
            config = cls.get_redis_config()
            
            r = redis.Redis(
                host=config["host"],
                port=config["port"],
                db=config["db"],
                socket_connect_timeout=2,
                socket_timeout=2
            )
            r.ping()
            return True
        except Exception as e:
            logging.warning(f"Redis não disponível: {e}")
            return False
    
    @classmethod
    def check_websocket_availability(cls) -> bool:
        """Verifica se WebSocket está disponível"""
        try:
            import websockets
            return True
        except ImportError:
            logging.warning("WebSocket não disponível - módulo websockets não instalado")
            return False
    
    @classmethod
    def get_system_resources(cls) -> Dict[str, Any]:
        """Obtém informações de recursos do sistema"""
        try:
            import psutil
            return {
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": psutil.disk_usage('/').percent if not platform.system().lower() == "windows" else psutil.disk_usage('C:').percent
            }
        except ImportError:
            return {
                "cpu_count": os.cpu_count(),
                "memory_total": "unknown",
                "memory_available": "unknown",
                "disk_usage": "unknown"
            }
    
    @classmethod
    def validate_environment(cls) -> Dict[str, bool]:
        """Valida o ambiente de execução"""
        return {
            "python_version_ok": sys.version_info >= (3, 8),
            "redis_available": cls.check_redis_availability(),
            "websocket_available": cls.check_websocket_availability(),
            "platform_supported": cls.get_platform_info()["os"] in ["windows", "linux"],
            "permissions_ok": cls._check_permissions()
        }
    
    @classmethod
    def _check_permissions(cls) -> bool:
        """Verifica permissões de escrita"""
        try:
            test_file = "test_permissions.tmp"
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except Exception:
            return False

# Função de conveniência para uso em outros módulos
def get_platform_info() -> Dict[str, Any]:
    """Função de conveniência para obter informações da plataforma"""
    return PlatformUtils.get_platform_info()

def get_redis_config() -> Dict[str, Any]:
    """Função de conveniência para obter configuração Redis"""
    return PlatformUtils.get_redis_config()

def get_websocket_config() -> Dict[str, Any]:
    """Função de conveniência para obter configuração WebSocket"""
    return PlatformUtils.get_websocket_config()

def validate_environment() -> Dict[str, bool]:
    """Função de conveniência para validar ambiente"""
    return PlatformUtils.validate_environment()

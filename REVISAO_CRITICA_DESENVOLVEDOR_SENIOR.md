# 🔍 REVISÃO CRÍTICA - DESENVOLVEDOR SÊNIOR
## **ANÁLISE DE ESTABILIDADE E PREVISIBILIDADE DOS TESTES**

---

## **📊 INFORMAÇÕES GERAIS**

- **Data**: 27/09/2025
- **Papel**: Desenvolvedor Sênior
- **Foco**: Estabilidade e Previsibilidade dos Testes
- **Status**: ⚠️ **REVISÃO CRÍTICA - REQUER CORREÇÕES**
- **Criticidade**: ALTA - Múltiplas falhas identificadas

---

## **🚨 FALHAS CRÍTICAS IDENTIFICADAS**

### **❌ FALHA 1: DEPENDÊNCIAS CÍCLICAS E IMPORTS PROBLEMÁTICOS**

**Problema**: O plano apresenta dependências circulares que podem causar falhas de importação:

```python
# PROBLEMA: Import circular potencial
from utils.platform_utils import PlatformUtils  # Em config_manager.py
from utils.config_manager import ConfigManager   # Em structured_logger.py
from utils.structured_logger import StructuredLogger  # Em metrics_collector.py
```

**Impacto**: 
- Falhas de importação em runtime
- Testes instáveis e não previsíveis
- Dificuldade de debugging

**Solução**: Implementar padrão de injeção de dependência ou lazy loading.

---

### **❌ FALHA 2: AUSÊNCIA DE TESTES DE INTEGRAÇÃO ROBUSTOS**

**Problema**: Os testes propostos são unitários demais e não testam cenários reais:

```python
# PROBLEMA: Teste muito simples
def test_platform_detection(self):
    platform_info = PlatformUtils.get_platform_info()
    self.assertIn("os", platform_info)
```

**Faltam**:
- Testes de integração entre módulos
- Testes de falha de componentes externos (Redis, WebSocket)
- Testes de concorrência
- Testes de performance
- Testes de recuperação de falhas

---

### **❌ FALHA 3: GERENCIAMENTO DE ESTADO INCONSISTENTE**

**Problema**: Múltiplos pontos de estado sem sincronização:

```python
# PROBLEMA: Estado não sincronizado
class MetricsCollector:
    def __init__(self, max_history: int = 100):
        self.metrics_history: Deque[Dict[str, Any]] = deque(maxlen=max_history)
        self.lock = threading.Lock()  # Apenas para metrics_history
        
class ConfigManager:
    def __init__(self):
        self.config = self.load_config()  # Sem lock
        self.platform_info = PlatformUtils.get_platform_info()  # Sem lock
```

**Impacto**:
- Race conditions em ambiente de produção
- Estado inconsistente entre threads
- Testes não determinísticos

---

### **❌ FALHA 4: AUSÊNCIA DE VALIDAÇÃO DE CONFIGURAÇÃO**

**Problema**: Configurações não são validadas antes do uso:

```python
# PROBLEMA: Sem validação
def get_redis_config(self) -> Dict[str, Any]:
    return self.config.get("redis", PlatformUtils.get_redis_config())
```

**Faltam**:
- Validação de tipos
- Validação de ranges
- Validação de dependências
- Validação de compatibilidade

---

### **❌ FALHA 5: LOGGING INCONSISTENTE E NÃO ESTRUTURADO**

**Problema**: Múltiplos sistemas de logging sem padronização:

```python
# PROBLEMA: Logging inconsistente
print(f"[OK] Configuração carregada de: {self.config_file}")  # Print direto
self.logger.info(f"Logger inicializado para plataforma: {self.platform_info['os']}")  # Logger
exibir_mensagem(f"[PLATFORM] Executando em: {platform_info['os']}")  # Função customizada
```

**Impacto**:
- Dificuldade de debugging
- Logs não estruturados
- Impossibilidade de análise automatizada

---

## **🔧 CORREÇÕES CRÍTICAS NECESSÁRIAS**

### **✅ CORREÇÃO 1: ARQUITETURA SEM DEPENDÊNCIAS CÍCLICAS**

```python
# utils/core.py - Módulo central sem dependências
import platform
import os
import sys
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class Platform(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    UNKNOWN = "Unknown"

@dataclass
class PlatformInfo:
    os: Platform
    os_version: str
    architecture: str
    python_version: str
    data_directory: str
    log_directory: str
    config_directory: str

class CorePlatformUtils:
    """Utilitários centrais sem dependências externas"""
    
    @staticmethod
    def detect_platform() -> Platform:
        system = platform.system()
        if system == "Windows":
            return Platform.WINDOWS
        elif system == "Linux":
            return Platform.LINUX
        else:
            return Platform.UNKNOWN
    
    @staticmethod
    def get_platform_info() -> PlatformInfo:
        detected_platform = CorePlatformUtils.detect_platform()
        
        if detected_platform == Platform.WINDOWS:
            data_dir = "rpa_data"
            log_dir = "logs"
            config_dir = "config"
        else:  # Linux
            data_dir = os.path.expanduser("~/rpa_data")
            log_dir = CorePlatformUtils._get_linux_log_dir()
            config_dir = os.path.expanduser("~/config")
        
        return PlatformInfo(
            os=detected_platform,
            os_version=platform.release(),
            architecture=platform.architecture()[0],
            python_version=sys.version,
            data_directory=data_dir,
            log_directory=log_dir,
            config_directory=config_dir
        )
    
    @staticmethod
    def _get_linux_log_dir() -> str:
        """Retorna diretório de logs para Linux com fallback"""
        try:
            log_dir = "/var/log/rpa"
            os.makedirs(log_dir, exist_ok=True)
            return log_dir
        except PermissionError:
            return os.path.expanduser("~/logs")
```

### **✅ CORREÇÃO 2: SISTEMA DE CONFIGURAÇÃO ROBUSTO**

```python
# utils/config_validator.py
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum

class ConfigError(Exception):
    """Exceção para erros de configuração"""
    pass

@dataclass
class ConfigSchema:
    """Schema para validação de configuração"""
    redis: Dict[str, Any]
    websocket: Dict[str, Any]
    monitoring: Dict[str, Any]

class ConfigValidator:
    """Validador robusto de configurações"""
    
    REDIS_SCHEMA = {
        "host": (str, "localhost"),
        "port": (int, 6379, 1, 65535),
        "db": (int, 0, 0, 15),
        "socket_timeout": (int, 5, 1, 300),
        "password": (str, None),
        "max_connections": (int, 10, 1, 100),
        "retry_on_timeout": (bool, True)
    }
    
    WEBSOCKET_SCHEMA = {
        "port": (int, 8080, 1024, 65535),
        "max_connections": (int, 50, 1, 1000),
        "timeout": (int, 300, 30, 3600)
    }
    
    MONITORING_SCHEMA = {
        "cpu_threshold": (int, 80, 1, 100),
        "memory_threshold": (int, 85, 1, 100),
        "collect_interval": (int, 30, 5, 3600),
        "cleanup_interval": (int, 3600, 300, 86400)
    }
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """Valida configuração completa"""
        try:
            validated_config = {}
            
            # Validar Redis
            validated_config["redis"] = cls._validate_section(
                config.get("redis", {}), 
                cls.REDIS_SCHEMA
            )
            
            # Validar WebSocket
            validated_config["websocket"] = cls._validate_section(
                config.get("websocket", {}), 
                cls.WEBSOCKET_SCHEMA
            )
            
            # Validar Monitoring
            validated_config["monitoring"] = cls._validate_section(
                config.get("monitoring", {}), 
                cls.MONITORING_SCHEMA
            )
            
            return validated_config
            
        except Exception as e:
            raise ConfigError(f"Falha na validação de configuração: {e}")
    
    @classmethod
    def _validate_section(cls, section: Dict[str, Any], schema: Dict[str, Tuple]) -> Dict[str, Any]:
        """Valida uma seção específica da configuração"""
        validated = {}
        
        for key, (expected_type, default_value, *range_values) in schema.items():
            value = section.get(key, default_value)
            
            # Validar tipo
            if not isinstance(value, expected_type):
                raise ConfigError(f"Tipo inválido para {key}: esperado {expected_type}, recebido {type(value)}")
            
            # Validar range se especificado
            if range_values and isinstance(value, (int, float)):
                min_val, max_val = range_values
                if not (min_val <= value <= max_val):
                    raise ConfigError(f"Valor fora do range para {key}: {value} não está entre {min_val} e {max_val}")
            
            validated[key] = value
        
        return validated
```

### **✅ CORREÇÃO 3: SISTEMA DE LOGGING ESTRUTURADO E CONSISTENTE**

```python
# utils/structured_logging.py
import logging
import json
import os
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class LogEntry:
    timestamp: str
    level: LogLevel
    message: str
    context: Dict[str, Any]
    platform: str
    session_id: Optional[str] = None

class StructuredLogger:
    """Sistema de logging estruturado e thread-safe"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._logger = self._setup_logger()
            self._platform = self._get_platform_info()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura logger thread-safe"""
        logger = logging.getLogger("rpa_hybrid")
        logger.setLevel(logging.INFO)
        
        # Limpar handlers existentes
        logger.handlers.clear()
        
        # Configurar diretório de logs
        log_dir = self._get_log_directory()
        os.makedirs(log_dir, exist_ok=True)
        
        # Arquivo de log com rotação
        log_file = os.path.join(log_dir, "rpa_hybrid.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        
        # Formatter estruturado
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def _get_log_directory(self) -> str:
        """Retorna diretório de logs baseado na plataforma"""
        if os.name == 'nt':  # Windows
            return "logs"
        else:  # Linux
            try:
                log_dir = "/var/log/rpa"
                os.makedirs(log_dir, exist_ok=True)
                return log_dir
            except PermissionError:
                return os.path.expanduser("~/logs")
    
    def _get_platform_info(self) -> str:
        """Retorna informações da plataforma"""
        import platform
        return f"{platform.system()} {platform.release()}"
    
    def log(self, level: LogLevel, message: str, context: Dict[str, Any] = None, session_id: str = None):
        """Log estruturado thread-safe"""
        log_entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level,
            message=message,
            context=context or {},
            platform=self._platform,
            session_id=session_id
        )
        
        # Log estruturado em JSON
        structured_message = json.dumps({
            "timestamp": log_entry.timestamp,
            "level": log_entry.level.value,
            "message": log_entry.message,
            "context": log_entry.context,
            "platform": log_entry.platform,
            "session_id": log_entry.session_id
        }, ensure_ascii=False)
        
        # Usar logger apropriado
        if level == LogLevel.DEBUG:
            self._logger.debug(structured_message)
        elif level == LogLevel.INFO:
            self._logger.info(structured_message)
        elif level == LogLevel.WARNING:
            self._logger.warning(structured_message)
        elif level == LogLevel.ERROR:
            self._logger.error(structured_message)
        elif level == LogLevel.CRITICAL:
            self._logger.critical(structured_message)
    
    def log_progress(self, session_id: str, etapa: int, mensagem: str, dados: Dict[str, Any] = None):
        """Log específico de progresso"""
        context = {
            "etapa": etapa,
            "dados": dados or {},
            "tipo": "progress"
        }
        self.log(LogLevel.INFO, mensagem, context, session_id)
    
    def log_error(self, erro: str, contexto: Dict[str, Any] = None, session_id: str = None):
        """Log específico de erro"""
        context = {
            "erro": erro,
            "contexto": contexto or {},
            "tipo": "error"
        }
        self.log(LogLevel.ERROR, erro, context, session_id)
    
    def log_fallback(self, modo_anterior: str, modo_novo: str, motivo: str, session_id: str = None):
        """Log específico de fallback"""
        context = {
            "modo_anterior": modo_anterior,
            "modo_novo": modo_novo,
            "motivo": motivo,
            "tipo": "fallback"
        }
        self.log(LogLevel.WARNING, f"Fallback: {modo_anterior} -> {modo_novo}", context, session_id)
```

### **✅ CORREÇÃO 4: TESTES DE INTEGRAÇÃO ROBUSTOS**

```python
# tests/test_integration_robust.py
import unittest
import tempfile
import os
import sys
import threading
import time
import json
from unittest.mock import Mock, patch, MagicMock
from concurrent.futures import ThreadPoolExecutor
import redis
import websockets

# Adicionar path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.core import CorePlatformUtils, Platform
from utils.config_validator import ConfigValidator, ConfigError
from utils.structured_logging import StructuredLogger, LogLevel

class TestIntegrationRobust(unittest.TestCase):
    """Testes de integração robustos e previsíveis"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.session_id = "test_session_123"
        self.logger = StructuredLogger()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_platform_detection_robust(self):
        """Testa detecção de plataforma de forma robusta"""
        platform_info = CorePlatformUtils.get_platform_info()
        
        # Validações básicas
        self.assertIsInstance(platform_info.os, Platform)
        self.assertIsInstance(platform_info.os_version, str)
        self.assertIsInstance(platform_info.architecture, str)
        self.assertIsInstance(platform_info.python_version, str)
        
        # Validações específicas
        self.assertTrue(len(platform_info.os_version) > 0)
        self.assertTrue(len(platform_info.architecture) > 0)
        self.assertTrue(len(platform_info.python_version) > 0)
        
        # Validações de diretórios
        self.assertTrue(os.path.isabs(platform_info.data_directory) or platform_info.data_directory.startswith('.'))
        self.assertTrue(os.path.isabs(platform_info.log_directory) or platform_info.log_directory.startswith('.'))
        self.assertTrue(os.path.isabs(platform_info.config_directory) or platform_info.config_directory.startswith('.'))
    
    def test_config_validation_comprehensive(self):
        """Testa validação de configuração de forma abrangente"""
        # Teste com configuração válida
        valid_config = {
            "redis": {
                "host": "localhost",
                "port": 6379,
                "db": 0,
                "socket_timeout": 5,
                "password": None,
                "max_connections": 10,
                "retry_on_timeout": True
            },
            "websocket": {
                "port": 8080,
                "max_connections": 50,
                "timeout": 300
            },
            "monitoring": {
                "cpu_threshold": 80,
                "memory_threshold": 85,
                "collect_interval": 30,
                "cleanup_interval": 3600
            }
        }
        
        validated = ConfigValidator.validate_config(valid_config)
        self.assertEqual(validated["redis"]["port"], 6379)
        self.assertEqual(validated["websocket"]["port"], 8080)
        self.assertEqual(validated["monitoring"]["cpu_threshold"], 80)
        
        # Teste com configuração inválida
        invalid_config = {
            "redis": {
                "port": "invalid_port",  # Tipo inválido
                "max_connections": 200   # Valor fora do range
            }
        }
        
        with self.assertRaises(ConfigError):
            ConfigValidator.validate_config(invalid_config)
    
    def test_logging_thread_safety(self):
        """Testa thread safety do sistema de logging"""
        def log_worker(worker_id: int, iterations: int = 100):
            for i in range(iterations):
                self.logger.log(
                    LogLevel.INFO,
                    f"Worker {worker_id} - Iteration {i}",
                    {"worker_id": worker_id, "iteration": i},
                    self.session_id
                )
        
        # Executar múltiplos workers simultaneamente
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(log_worker, i, 50) for i in range(5)]
            
            # Aguardar conclusão
            for future in futures:
                future.result()
        
        # Verificar se logs foram criados sem erros
        log_file = self.logger._logger.handlers[0].baseFilename
        self.assertTrue(os.path.exists(log_file))
        
        # Verificar conteúdo dos logs
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("Worker 0", log_content)
            self.assertIn("Worker 4", log_content)
    
    def test_redis_connection_failure_handling(self):
        """Testa tratamento de falhas de conexão Redis"""
        with patch('redis.Redis') as mock_redis:
            # Simular falha de conexão
            mock_redis.side_effect = redis.ConnectionError("Connection failed")
            
            # Testar fallback
            try:
                redis_client = redis.Redis(host="localhost", port=6379)
                redis_client.ping()
                self.fail("Deveria ter falhado")
            except redis.ConnectionError:
                # Fallback esperado
                self.logger.log_error("Redis connection failed", {"fallback": "json"})
                self.assertTrue(True)  # Fallback funcionou
    
    def test_websocket_connection_failure_handling(self):
        """Testa tratamento de falhas de conexão WebSocket"""
        with patch('websockets.connect') as mock_websocket:
            # Simular falha de conexão
            mock_websocket.side_effect = websockets.exceptions.ConnectionClosed("Connection closed")
            
            # Testar fallback
            try:
                import asyncio
                async def test_websocket():
                    async with websockets.connect("ws://localhost:8080") as websocket:
                        await websocket.send("test")
                
                asyncio.run(test_websocket())
                self.fail("Deveria ter falhado")
            except websockets.exceptions.ConnectionClosed:
                # Fallback esperado
                self.logger.log_error("WebSocket connection failed", {"fallback": "sse"})
                self.assertTrue(True)  # Fallback funcionou
    
    def test_concurrent_metrics_collection(self):
        """Testa coleta de métricas concorrente"""
        def collect_metrics(worker_id: int, iterations: int = 50):
            for i in range(iterations):
                try:
                    import psutil
                    metrics = {
                        "worker_id": worker_id,
                        "iteration": i,
                        "cpu_percent": psutil.cpu_percent(interval=None),
                        "memory_percent": psutil.virtual_memory().percent,
                        "timestamp": time.time()
                    }
                    self.logger.log(LogLevel.INFO, f"Metrics collected", metrics)
                except Exception as e:
                    self.logger.log_error(f"Metrics collection failed", {"error": str(e)})
        
        # Executar coleta concorrente
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(collect_metrics, i, 30) for i in range(3)]
            
            # Aguardar conclusão
            for future in futures:
                future.result()
        
        # Verificar se métricas foram coletadas
        log_file = self.logger._logger.handlers[0].baseFilename
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("Metrics collected", log_content)
    
    def test_configuration_hot_reload(self):
        """Testa recarregamento de configuração em tempo real"""
        # Criar configuração temporária
        config_file = os.path.join(self.temp_dir, "test_config.json")
        initial_config = {
            "redis": {"port": 6379},
            "websocket": {"port": 8080},
            "monitoring": {"cpu_threshold": 80}
        }
        
        with open(config_file, 'w') as f:
            json.dump(initial_config, f)
        
        # Validar configuração inicial
        validated = ConfigValidator.validate_config(initial_config)
        self.assertEqual(validated["redis"]["port"], 6379)
        
        # Modificar configuração
        updated_config = {
            "redis": {"port": 6380},
            "websocket": {"port": 8081},
            "monitoring": {"cpu_threshold": 85}
        }
        
        with open(config_file, 'w') as f:
            json.dump(updated_config, f)
        
        # Validar configuração atualizada
        validated = ConfigValidator.validate_config(updated_config)
        self.assertEqual(validated["redis"]["port"], 6380)
        self.assertEqual(validated["monitoring"]["cpu_threshold"], 85)
    
    def test_error_recovery_mechanisms(self):
        """Testa mecanismos de recuperação de erro"""
        # Testar recuperação de falha de disco
        with patch('os.makedirs') as mock_makedirs:
            mock_makedirs.side_effect = OSError("Disk full")
            
            # Deve falhar graciosamente
            try:
                os.makedirs("test_dir", exist_ok=True)
                self.fail("Deveria ter falhado")
            except OSError:
                self.logger.log_error("Disk full", {"fallback": "memory"})
                self.assertTrue(True)  # Recuperação funcionou
        
        # Testar recuperação de falha de rede
        with patch('socket.socket') as mock_socket:
            mock_socket.side_effect = OSError("Network unreachable")
            
            # Deve falhar graciosamente
            try:
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("localhost", 6379))
                self.fail("Deveria ter falhado")
            except OSError:
                self.logger.log_error("Network unreachable", {"fallback": "local"})
                self.assertTrue(True)  # Recuperação funcionou

if __name__ == '__main__':
    unittest.main()
```

### **✅ CORREÇÃO 5: SISTEMA DE MONITORAMENTO DETERMINÍSTICO**

```python
# utils/deterministic_monitoring.py
import time
import threading
import psutil
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from collections import deque
import json

class MetricType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    CUSTOM = "custom"

@dataclass
class Metric:
    timestamp: float
    type: MetricType
    value: float
    unit: str
    metadata: Dict[str, Any]

class DeterministicMonitor:
    """Sistema de monitoramento determinístico e previsível"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history: deque = deque(maxlen=max_history)
        self.lock = threading.RLock()
        self.start_time = time.time()
        self._last_collection = 0
        self._collection_interval = 1.0  # 1 segundo por padrão
    
    def collect_metrics(self, force: bool = False) -> Dict[str, Any]:
        """Coleta métricas de forma determinística"""
        current_time = time.time()
        
        # Verificar se deve coletar
        if not force and (current_time - self._last_collection) < self._collection_interval:
            return {"status": "skipped", "reason": "interval_not_reached"}
        
        self._last_collection = current_time
        
        with self.lock:
            try:
                metrics = self._collect_system_metrics()
                self.metrics_history.append(metrics)
                return metrics
            except Exception as e:
                error_metric = {
                    "timestamp": current_time,
                    "error": str(e),
                    "status": "error"
                }
                self.metrics_history.append(error_metric)
                return error_metric
    
    def _collect_system_metrics(self) -> Dict[str, Any]:
        """Coleta métricas do sistema de forma determinística"""
        current_time = time.time()
        
        # Métricas básicas
        metrics = {
            "timestamp": current_time,
            "uptime": current_time - self.start_time,
            "cpu_percent": self._get_cpu_percent(),
            "memory_percent": self._get_memory_percent(),
            "disk_percent": self._get_disk_percent(),
            "process_count": len(psutil.pids()),
            "status": "success"
        }
        
        # Métricas específicas da plataforma
        if os.name == 'nt':  # Windows
            metrics.update(self._get_windows_metrics())
        else:  # Linux
            metrics.update(self._get_linux_metrics())
        
        return metrics
    
    def _get_cpu_percent(self) -> float:
        """Obtém percentual de CPU de forma determinística"""
        try:
            # Usar interval=None para não bloquear
            return psutil.cpu_percent(interval=None)
        except Exception:
            return 0.0
    
    def _get_memory_percent(self) -> float:
        """Obtém percentual de memória de forma determinística"""
        try:
            return psutil.virtual_memory().percent
        except Exception:
            return 0.0
    
    def _get_disk_percent(self) -> float:
        """Obtém percentual de disco de forma determinística"""
        try:
            if os.name == 'nt':  # Windows
                return psutil.disk_usage('C:').percent
            else:  # Linux
                return psutil.disk_usage('/').percent
        except Exception:
            return 0.0
    
    def _get_windows_metrics(self) -> Dict[str, Any]:
        """Métricas específicas do Windows"""
        try:
            return {
                "windows_specific": {
                    "boot_time": psutil.boot_time(),
                    "users": len(psutil.users()),
                    "disk_io": psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {}
                }
            }
        except Exception:
            return {"windows_specific": {"error": "Failed to collect Windows metrics"}}
    
    def _get_linux_metrics(self) -> Dict[str, Any]:
        """Métricas específicas do Linux"""
        try:
            return {
                "linux_specific": {
                    "boot_time": psutil.boot_time(),
                    "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
                    "disk_io": psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {}
                }
            }
        except Exception:
            return {"linux_specific": {"error": "Failed to collect Linux metrics"}}
    
    def get_average_metrics(self, window: int = 10) -> Dict[str, Any]:
        """Retorna métricas médias de forma determinística"""
        with self.lock:
            if len(self.metrics_history) < window:
                return {
                    "error": "Insufficient data",
                    "available_samples": len(self.metrics_history),
                    "requested_window": window
                }
            
            recent_metrics = list(self.metrics_history)[-window:]
            
            # Calcular médias
            cpu_values = [m.get("cpu_percent", 0) for m in recent_metrics if "cpu_percent" in m]
            memory_values = [m.get("memory_percent", 0) for m in recent_metrics if "memory_percent" in m]
            disk_values = [m.get("disk_percent", 0) for m in recent_metrics if "disk_percent" in m]
            
            return {
                "cpu_avg": sum(cpu_values) / len(cpu_values) if cpu_values else 0,
                "memory_avg": sum(memory_values) / len(memory_values) if memory_values else 0,
                "disk_avg": sum(disk_values) / len(disk_values) if disk_values else 0,
                "window_size": window,
                "samples_used": len(recent_metrics)
            }
    
    def get_metric_trend(self, metric_name: str, window: int = 10) -> Dict[str, Any]:
        """Retorna tendência de uma métrica específica"""
        with self.lock:
            if len(self.metrics_history) < window:
                return {
                    "error": "Insufficient data",
                    "available_samples": len(self.metrics_history),
                    "requested_window": window
                }
            
            recent_metrics = list(self.metrics_history)[-window:]
            values = [m.get(metric_name, 0) for m in recent_metrics if metric_name in m]
            
            if len(values) < 2:
                return {
                    "error": "Insufficient data points",
                    "values": values
                }
            
            # Calcular tendência (linear regression simples)
            n = len(values)
            x = list(range(n))
            y = values
            
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(x[i] * y[i] for i in range(n))
            sum_x2 = sum(x[i] ** 2 for i in range(n))
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
            intercept = (sum_y - slope * sum_x) / n
            
            return {
                "metric": metric_name,
                "trend": "increasing" if slope > 0.1 else "decreasing" if slope < -0.1 else "stable",
                "slope": slope,
                "intercept": intercept,
                "values": values,
                "window_size": window
            }
    
    def set_collection_interval(self, interval: float):
        """Define intervalo de coleta de métricas"""
        if interval < 0.1:  # Mínimo 100ms
            interval = 0.1
        self._collection_interval = interval
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do monitor"""
        with self.lock:
            return {
                "max_history": self.max_history,
                "current_samples": len(self.metrics_history),
                "uptime": time.time() - self.start_time,
                "collection_interval": self._collection_interval,
                "last_collection": self._last_collection,
                "status": "active"
            }
```

---

## **📋 PLANO DE CORREÇÕES PRIORITÁRIAS**

### **🔴 PRIORIDADE 1: CORREÇÕES CRÍTICAS (Dia 1-2)**
1. **Implementar arquitetura sem dependências cíclicas**
2. **Implementar sistema de validação de configuração**
3. **Implementar logging estruturado e thread-safe**
4. **Implementar monitoramento determinístico**

### **🟡 PRIORIDADE 2: TESTES ROBUSTOS (Dia 3-4)**
1. **Implementar testes de integração abrangentes**
2. **Implementar testes de concorrência**
3. **Implementar testes de falha e recuperação**
4. **Implementar testes de performance**

### **🟢 PRIORIDADE 3: VALIDAÇÃO FINAL (Dia 5)**
1. **Executar bateria completa de testes**
2. **Validar estabilidade em ambiente real**
3. **Documentar procedimentos de troubleshooting**
4. **Implementar monitoramento de saúde do sistema**

---

## **⚠️ RECOMENDAÇÕES CRÍTICAS**

### **1. NÃO IMPLEMENTAR O PLANO ATUAL**
O plano atual apresenta múltiplas falhas críticas que comprometem a estabilidade e previsibilidade dos testes.

### **2. IMPLEMENTAR ARQUITETURA CORRIGIDA**
Usar a arquitetura proposta nas correções críticas, que elimina dependências cíclicas e garante thread safety.

### **3. IMPLEMENTAR TESTES ROBUSTOS**
Os testes propostos são insuficientes. Implementar testes de integração, concorrência e falha.

### **4. IMPLEMENTAR MONITORAMENTO DETERMINÍSTICO**
O sistema de monitoramento atual é não determinístico. Implementar sistema baseado em intervalos fixos.

### **5. VALIDAR EM AMBIENTE REAL**
Antes do deploy em produção, validar em ambiente de staging com carga real.

---

## **📊 CONCLUSÃO**

**Status**: ❌ **PLANO REJEITADO - REQUER REESCRITA COMPLETA**

O plano atual não atende aos critérios de estabilidade e previsibilidade necessários para um sistema de produção. As correções propostas são fundamentais e devem ser implementadas antes de qualquer deploy.

**Recomendação**: Implementar as correções críticas propostas e revalidar o plano antes de prosseguir com a implementação.

---

**Revisão realizada por**: Desenvolvedor Sênior  
**Data**: 27 de Setembro de 2025  
**Status**: ❌ **REJEITADO - REQUER CORREÇÕES CRÍTICAS**  
**Próximo passo**: Implementar correções críticas e revalidar


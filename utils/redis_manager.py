# 🔴 REDIS MANAGER - GERENCIAMENTO DE CACHE E COMUNICAÇÃO
"""
Módulo para gerenciamento de Redis com fallback automático.
Implementa cache inteligente e comunicação em tempo real.
"""

import json
import logging
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
import threading
import queue

# Importação condicional do Redis
try:
    import redis
    from redis.exceptions import ConnectionError, TimeoutError, RedisError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
    ConnectionError = Exception
    TimeoutError = Exception
    RedisError = Exception

from .platform_utils import PlatformUtils

class RedisManager:
    """Gerenciador de Redis com fallback automático"""
    
    _instance = None
    _connection = None
    _fallback_cache = {}
    _fallback_lock = threading.Lock()
    _health_check_thread = None
    _is_healthy = False
    _last_health_check = 0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logger = logging.getLogger(__name__)
            self.config = PlatformUtils.get_redis_config()
            self._fallback_cache = {}
            self._fallback_lock = threading.Lock()
            self._is_healthy = False
            self._last_health_check = 0
            self._start_health_check()
    
    def _start_health_check(self):
        """Inicia thread de verificação de saúde"""
        if self._health_check_thread is None or not self._health_check_thread.is_alive():
            self._health_check_thread = threading.Thread(
                target=self._health_check_loop,
                daemon=True,
                name="RedisHealthCheck"
            )
            self._health_check_thread.start()
    
    def _health_check_loop(self):
        """Loop de verificação de saúde do Redis"""
        while True:
            try:
                self._check_redis_health()
                time.sleep(30)  # Verifica a cada 30 segundos
            except Exception as e:
                self.logger.error(f"Erro no health check do Redis: {e}")
                time.sleep(60)  # Em caso de erro, espera 1 minuto
    
    def _check_redis_health(self):
        """Verifica a saúde da conexão Redis"""
        try:
            if REDIS_AVAILABLE and self._connection:
                self._connection.ping()
                self._is_healthy = True
                self._last_health_check = time.time()
            else:
                self._is_healthy = False
        except Exception as e:
            self.logger.warning(f"Redis não saudável: {e}")
            self._is_healthy = False
    
    def get_connection(self) -> Optional[redis.Redis]:
        """Obtém conexão Redis ou None se não disponível"""
        if not REDIS_AVAILABLE:
            return None
        
        try:
            if self._connection is None:
                self._connection = redis.Redis(
                    host=self.config["host"],
                    port=self.config["port"],
                    db=self.config["db"],
                    decode_responses=self.config["decode_responses"],
                    socket_connect_timeout=self.config["socket_connect_timeout"],
                    socket_timeout=self.config["socket_timeout"],
                    retry_on_timeout=self.config["retry_on_timeout"],
                    health_check_interval=self.config["health_check_interval"]
                )
            
            # Teste rápido de conexão
            self._connection.ping()
            return self._connection
            
        except Exception as e:
            self.logger.warning(f"Falha ao conectar Redis: {e}")
            self._connection = None
            return None
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Define valor no Redis ou cache local"""
        try:
            # Tentar Redis primeiro
            conn = self.get_connection()
            if conn:
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                conn.set(key, value, ex=expire)
                return True
        except Exception as e:
            self.logger.warning(f"Falha ao definir no Redis: {e}")
        
        # Fallback para cache local
        with self._fallback_lock:
            self._fallback_cache[key] = {
                'value': value,
                'timestamp': time.time(),
                'expire': expire
            }
        return True
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do Redis ou cache local"""
        try:
            # Tentar Redis primeiro
            conn = self.get_connection()
            if conn:
                value = conn.get(key)
                if value:
                    try:
                        return json.loads(value)
                    except (json.JSONDecodeError, TypeError):
                        return value
        except Exception as e:
            self.logger.warning(f"Falha ao obter do Redis: {e}")
        
        # Fallback para cache local
        with self._fallback_lock:
            if key in self._fallback_cache:
                item = self._fallback_cache[key]
                # Verificar expiração
                if item['expire'] and (time.time() - item['timestamp']) > item['expire']:
                    del self._fallback_cache[key]
                    return None
                return item['value']
        
        return None
    
    def delete(self, key: str) -> bool:
        """Remove valor do Redis ou cache local"""
        try:
            # Tentar Redis primeiro
            conn = self.get_connection()
            if conn:
                conn.delete(key)
        except Exception as e:
            self.logger.warning(f"Falha ao deletar do Redis: {e}")
        
        # Fallback para cache local
        with self._fallback_lock:
            if key in self._fallback_cache:
                del self._fallback_cache[key]
        
        return True
    
    def exists(self, key: str) -> bool:
        """Verifica se chave existe no Redis ou cache local"""
        try:
            # Tentar Redis primeiro
            conn = self.get_connection()
            if conn:
                return bool(conn.exists(key))
        except Exception as e:
            self.logger.warning(f"Falha ao verificar existência no Redis: {e}")
        
        # Fallback para cache local
        with self._fallback_lock:
            if key in self._fallback_cache:
                item = self._fallback_cache[key]
                # Verificar expiração
                if item['expire'] and (time.time() - item['timestamp']) > item['expire']:
                    del self._fallback_cache[key]
                    return False
                return True
        
        return False
    
    def set_session_data(self, session_id: str, data: Dict[str, Any], expire: int = 3600) -> bool:
        """Define dados de sessão"""
        key = f"session:{session_id}"
        return self.set(key, data, expire)
    
    def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtém dados de sessão"""
        key = f"session:{session_id}"
        return self.get(key)
    
    def set_progress_data(self, session_id: str, progress_data: Dict[str, Any], expire: int = 3600) -> bool:
        """Define dados de progresso"""
        key = f"progress:{session_id}"
        return self.set(key, progress_data, expire)
    
    def get_progress_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtém dados de progresso"""
        key = f"progress:{session_id}"
        return self.get(key)
    
    def publish_message(self, channel: str, message: Dict[str, Any]) -> bool:
        """Publica mensagem em canal Redis"""
        try:
            conn = self.get_connection()
            if conn:
                message_str = json.dumps(message, ensure_ascii=False)
                conn.publish(channel, message_str)
                return True
        except Exception as e:
            self.logger.warning(f"Falha ao publicar mensagem: {e}")
        
        return False
    
    def subscribe_to_channel(self, channel: str, callback) -> bool:
        """Inscreve-se em canal Redis"""
        try:
            conn = self.get_connection()
            if conn:
                pubsub = conn.pubsub()
                pubsub.subscribe(channel)
                
                def message_handler():
                    for message in pubsub.listen():
                        if message['type'] == 'message':
                            try:
                                data = json.loads(message['data'])
                                callback(data)
                            except Exception as e:
                                self.logger.error(f"Erro ao processar mensagem: {e}")
                
                thread = threading.Thread(target=message_handler, daemon=True)
                thread.start()
                return True
        except Exception as e:
            self.logger.warning(f"Falha ao inscrever-se no canal: {e}")
        
        return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do cache"""
        with self._fallback_lock:
            cache_size = len(self._fallback_cache)
            cache_keys = list(self._fallback_cache.keys())
        
        return {
            "redis_available": REDIS_AVAILABLE,
            "redis_healthy": self._is_healthy,
            "fallback_cache_size": cache_size,
            "fallback_cache_keys": cache_keys,
            "last_health_check": self._last_health_check
        }
    
    def clear_cache(self):
        """Limpa cache local"""
        with self._fallback_lock:
            self._fallback_cache.clear()
    
    def cleanup_expired(self):
        """Remove itens expirados do cache local"""
        current_time = time.time()
        with self._fallback_lock:
            expired_keys = []
            for key, item in self._fallback_cache.items():
                if item['expire'] and (current_time - item['timestamp']) > item['expire']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._fallback_cache[key]

# Instância global
redis_manager = RedisManager()

# Funções de conveniência
def set_cache(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """Função de conveniência para definir cache"""
    return redis_manager.set(key, value, expire)

def get_cache(key: str) -> Optional[Any]:
    """Função de conveniência para obter cache"""
    return redis_manager.get(key)

def delete_cache(key: str) -> bool:
    """Função de conveniência para deletar cache"""
    return redis_manager.delete(key)

def cache_exists(key: str) -> bool:
    """Função de conveniência para verificar existência"""
    return redis_manager.exists(key)

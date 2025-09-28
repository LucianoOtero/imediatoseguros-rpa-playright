# 🌐 WEBSOCKET MANAGER - COMUNICAÇÃO EM TEMPO REAL
"""
Módulo para gerenciamento de WebSocket com fallback automático.
Implementa comunicação bidirecional em tempo real.
"""

import json
import logging
import asyncio
import threading
import time
from typing import Dict, Any, Optional, List, Callable, Set
from datetime import datetime
import queue
import uuid

# Importação condicional do WebSocket
try:
    import websockets
    from websockets.exceptions import ConnectionClosed, WebSocketException
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    websockets = None
    ConnectionClosed = Exception
    WebSocketException = Exception

from .platform_utils import PlatformUtils
from .redis_manager import redis_manager

class WebSocketManager:
    """Gerenciador de WebSocket com fallback automático"""
    
    _instance = None
    _server = None
    _clients = set()
    _message_queue = queue.Queue()
    _fallback_mode = False
    _message_handlers = {}
    _health_check_thread = None
    _is_running = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logger = logging.getLogger(__name__)
            self.config = PlatformUtils.get_websocket_config()
            self._clients = set()
            self._message_queue = queue.Queue()
            self._fallback_mode = False
            self._message_handlers = {}
            self._is_running = False
            self._start_fallback_handler()
    
    def _start_fallback_handler(self):
        """Inicia handler de fallback para mensagens"""
        if self._health_check_thread is None or not self._health_check_thread.is_alive():
            self._health_check_thread = threading.Thread(
                target=self._fallback_message_handler,
                daemon=True,
                name="WebSocketFallbackHandler"
            )
            self._health_check_thread.start()
    
    def _fallback_message_handler(self):
        """Handler de mensagens em modo fallback"""
        while True:
            try:
                if not self._is_running and not self._message_queue.empty():
                    # Processar mensagens em modo fallback
                    message = self._message_queue.get(timeout=1)
                    self._process_fallback_message(message)
                time.sleep(0.1)
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Erro no handler de fallback: {e}")
                time.sleep(1)
    
    def _process_fallback_message(self, message: Dict[str, Any]):
        """Processa mensagem em modo fallback"""
        try:
            message_type = message.get('type', 'unknown')
            if message_type in self._message_handlers:
                handler = self._message_handlers[message_type]
                handler(message)
            else:
                self.logger.warning(f"Handler não encontrado para tipo: {message_type}")
        except Exception as e:
            self.logger.error(f"Erro ao processar mensagem fallback: {e}")
    
    async def start_server(self) -> bool:
        """Inicia servidor WebSocket"""
        if not WEBSOCKET_AVAILABLE:
            self.logger.warning("WebSocket não disponível - usando modo fallback")
            self._fallback_mode = True
            return False
        
        try:
            self._server = await websockets.serve(
                self._handle_client,
                self.config["host"],
                self.config["port"],
                max_size=self.config["max_size"],
                ping_interval=self.config["ping_interval"],
                ping_timeout=self.config["ping_timeout"],
                close_timeout=self.config["close_timeout"],
                compression=self.config["compression"]
            )
            
            self._is_running = True
            self._fallback_mode = False
            self.logger.info(f"WebSocket server iniciado em {self.config['host']}:{self.config['port']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Falha ao iniciar WebSocket server: {e}")
            self._fallback_mode = True
            return False
    
    async def _handle_client(self, websocket, path):
        """Manipula conexão de cliente"""
        client_id = str(uuid.uuid4())
        self._clients.add(websocket)
        
        try:
            self.logger.info(f"Cliente conectado: {client_id}")
            
            # Enviar mensagem de boas-vindas
            welcome_message = {
                "type": "connection",
                "status": "connected",
                "client_id": client_id,
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(welcome_message, ensure_ascii=False))
            
            # Loop de mensagens
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._process_message(websocket, data)
                except json.JSONDecodeError:
                    self.logger.warning(f"Mensagem inválida recebida: {message}")
                except Exception as e:
                    self.logger.error(f"Erro ao processar mensagem: {e}")
                    
        except ConnectionClosed:
            self.logger.info(f"Cliente desconectado: {client_id}")
        except Exception as e:
            self.logger.error(f"Erro na conexão do cliente: {e}")
        finally:
            self._clients.discard(websocket)
    
    async def _process_message(self, websocket, message: Dict[str, Any]):
        """Processa mensagem recebida"""
        try:
            message_type = message.get('type', 'unknown')
            
            # Processar mensagem localmente
            if message_type in self._message_handlers:
                handler = self._message_handlers[message_type]
                response = handler(message)
                if response:
                    await websocket.send(json.dumps(response, ensure_ascii=False))
            
            # Repassar para Redis se disponível
            if redis_manager.get_connection():
                redis_manager.publish_message(f"websocket:{message_type}", message)
                
        except Exception as e:
            self.logger.error(f"Erro ao processar mensagem: {e}")
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Registra handler para tipo de mensagem"""
        self._message_handlers[message_type] = handler
        self.logger.info(f"Handler registrado para tipo: {message_type}")
    
    def send_message(self, message: Dict[str, Any]) -> bool:
        """Envia mensagem para todos os clientes conectados"""
        if not self._is_running or not self._clients:
            # Modo fallback - adicionar à fila
            self._message_queue.put(message)
            return False
        
        try:
            message_str = json.dumps(message, ensure_ascii=False)
            
            # Enviar para todos os clientes
            for client in self._clients.copy():
                try:
                    asyncio.create_task(client.send(message_str))
                except Exception as e:
                    self.logger.warning(f"Falha ao enviar para cliente: {e}")
                    self._clients.discard(client)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar mensagem: {e}")
            return False
    
    def send_progress_update(self, session_id: str, progress_data: Dict[str, Any]) -> bool:
        """Envia atualização de progresso"""
        message = {
            "type": "progress_update",
            "session_id": session_id,
            "data": progress_data,
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(message)
    
    def send_status_update(self, session_id: str, status: str, message: str = "") -> bool:
        """Envia atualização de status"""
        message_data = {
            "type": "status_update",
            "session_id": session_id,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(message_data)
    
    def send_error(self, session_id: str, error: str, details: Dict[str, Any] = None) -> bool:
        """Envia mensagem de erro"""
        message = {
            "type": "error",
            "session_id": session_id,
            "error": error,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(message)
    
    def get_connected_clients(self) -> int:
        """Obtém número de clientes conectados"""
        return len(self._clients)
    
    def is_running(self) -> bool:
        """Verifica se servidor está rodando"""
        return self._is_running
    
    def is_fallback_mode(self) -> bool:
        """Verifica se está em modo fallback"""
        return self._fallback_mode
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do WebSocket"""
        return {
            "websocket_available": WEBSOCKET_AVAILABLE,
            "is_running": self._is_running,
            "is_fallback_mode": self._fallback_mode,
            "connected_clients": len(self._clients),
            "message_handlers": len(self._message_handlers),
            "queue_size": self._message_queue.qsize()
        }
    
    async def stop_server(self):
        """Para o servidor WebSocket"""
        self._is_running = False
        
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        
        # Fechar todas as conexões
        for client in self._clients.copy():
            try:
                await client.close()
            except Exception:
                pass
        
        self._clients.clear()
        self.logger.info("WebSocket server parado")

# Instância global
websocket_manager = WebSocketManager()

# Funções de conveniência
def send_message(message: Dict[str, Any]) -> bool:
    """Função de conveniência para enviar mensagem"""
    return websocket_manager.send_message(message)

def send_progress_update(session_id: str, progress_data: Dict[str, Any]) -> bool:
    """Função de conveniência para enviar progresso"""
    return websocket_manager.send_progress_update(session_id, progress_data)

def send_status_update(session_id: str, status: str, message: str = "") -> bool:
    """Função de conveniência para enviar status"""
    return websocket_manager.send_status_update(session_id, status, message)

def register_message_handler(message_type: str, handler: Callable):
    """Função de conveniência para registrar handler"""
    websocket_manager.register_message_handler(message_type, handler)

def get_websocket_stats() -> Dict[str, Any]:
    """Função de conveniência para obter estatísticas"""
    return websocket_manager.get_stats()

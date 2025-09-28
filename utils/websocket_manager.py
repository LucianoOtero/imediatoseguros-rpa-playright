import asyncio
import json
import logging
from typing import Dict, Any, Callable
from datetime import datetime
import websockets
from websockets.exceptions import ConnectionClosed

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Gerenciador de conexões WebSocket com fallback"""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.uri = f"ws://{host}:{port}"
        self.connection = None
        self.handlers: Dict[str, Callable] = {}
        self.is_connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        
    def register_handler(self, message_type: str, handler: Callable):
        """Registra um handler para um tipo de mensagem"""
        self.handlers[message_type] = handler
        logger.info(f"Handler registrado para tipo: {message_type}")
    
    async def connect(self) -> bool:
        """Conecta ao servidor WebSocket"""
        try:
            self.connection = await websockets.connect(self.uri)
            self.is_connected = True
            self.reconnect_attempts = 0
            logger.info(f"Conectado ao WebSocket: {self.uri}")
            
            # Iniciar loop de escuta
            asyncio.create_task(self._listen())
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar WebSocket: {e}")
            self.is_connected = False
            return False
    
    async def _listen(self):
        """Loop de escuta de mensagens"""
        try:
            async for message in self.connection:
                await self._handle_message(message)
        except ConnectionClosed:
            logger.warning("Conexão WebSocket fechada")
            self.is_connected = False
        except Exception as e:
            logger.error(f"Erro no loop de escuta: {e}")
            self.is_connected = False
    
    async def _handle_message(self, message: str):
        """Processa mensagens recebidas"""
        try:
            data = json.loads(message)
            message_type = data.get('type', 'unknown')
            
            if message_type in self.handlers:
                await self.handlers[message_type](data)
            else:
                logger.warning(f"Handler não encontrado para tipo: "
                               f"{message_type}")
                
        except json.JSONDecodeError:
            logger.error(f"Erro ao decodificar JSON: {message}")
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
    
    async def send_message(self, message: Dict[str, Any]) -> bool:
        """Envia mensagem via WebSocket"""
        if not self.is_connected or not self.connection:
            logger.warning("WebSocket não conectado")
            return False
        
        try:
            await self.connection.send(json.dumps(message))
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            self.is_connected = False
            return False
    
    async def send_status_update(self, session_id: str, status: str,
                                 message: str) -> bool:
        """Envia atualização de status"""
        msg = {
            'type': 'status_update',
            'session_id': session_id,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        return await self.send_message(msg)
    
    async def send_progress_update(self, session_id: str,
                                   progress_data: Dict[str, Any]) -> bool:
        """Envia atualização de progresso"""
        message = {
            "type": "progress_update",
            "session_id": session_id,
            "data": progress_data,
            "timestamp": datetime.now().isoformat()
        }
        return await self.send_message(message)
    
    async def disconnect(self):
        """Desconecta do WebSocket"""
        if self.connection:
            await self.connection.close()
            self.is_connected = False
            logger.info("Desconectado do WebSocket")
    
    def is_healthy(self) -> bool:
        """Verifica se o WebSocket está saudável"""
        return self.is_connected and self.connection is not None
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do WebSocket"""
        return {
            "is_running": self.is_connected,
            "is_connected": self.is_connected,
            "host": self.host,
            "port": self.port,
            "reconnect_attempts": self.reconnect_attempts,
            "handlers_count": len(self.handlers)
        }
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Registra um handler para um tipo de mensagem"""
        self.register_handler(message_type, handler)
    
    async def send_error(self, session_id: str, error: str,
                         details: Dict[str, Any] = None) -> bool:
        """Envia erro"""
        message = {
            "type": "error",
            "session_id": session_id,
            "error": error,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        return await self.send_message(message)


# Instância global
websocket_manager = WebSocketManager()


# Handlers padrão
async def default_test_handler(data):
    """Handler padrão para mensagens de teste"""
    logger.info(f"Test handler recebido: {data}")


async def default_session_handler(data):
    """Handler padrão para eventos de sessão"""
    logger.info(f"Session handler recebido: {data}")


async def default_progress_handler(data):
    """Handler padrão para atualizações de progresso"""
    logger.info(f"Progress handler recebido: {data}")


async def default_status_handler(data):
    """Handler padrão para atualizações de status"""
    logger.info(f"Status handler recebido: {data}")


# Registrar handlers padrão
websocket_manager.register_handler('test_response', default_test_handler)
websocket_manager.register_handler('session_response',
                                   default_session_handler)
websocket_manager.register_handler('progress_response',
                                   default_progress_handler)
websocket_manager.register_handler('status_response', default_status_handler)
websocket_manager.register_handler('progress_data', default_progress_handler)
websocket_manager.register_handler('status_data', default_status_handler)
websocket_manager.register_handler('session_data',
                                   default_session_handler)

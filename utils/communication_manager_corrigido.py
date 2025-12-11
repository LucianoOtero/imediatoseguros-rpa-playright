# 📡 COMMUNICATION MANAGER - ORQUESTRAÇÃO DE COMUNICAÇÃO
"""
Módulo para orquestração de comunicação entre componentes.
Integra Redis, WebSocket e comunicação bidirecional.
"""

import json
import logging
import threading
import time
import asyncio
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import uuid

from .redis_manager import redis_manager
from .websocket_manager import websocket_manager
from .platform_utils import PlatformUtils

class CommunicationManager:
    """Gerenciador de comunicação integrado"""
    
    _instance = None
    _session_handlers = {}
    _message_routing = {}
    _health_monitor_thread = None
    _is_monitoring = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logger = logging.getLogger(__name__)
            self._session_handlers = {}
            self._message_routing = {}
            self._is_monitoring = False
            self._start_health_monitor()
            self._setup_default_handlers()
    
    def _start_health_monitor(self):
        """Inicia monitoramento de saúde"""
        if self._health_monitor_thread is None or not self._health_monitor_thread.is_alive():
            self._health_monitor_thread = threading.Thread(
                target=self._health_monitor_loop,
                daemon=True,
                name="CommunicationHealthMonitor"
            )
            self._health_monitor_thread.start()
    
    def _health_monitor_loop(self):
        """Loop de monitoramento de saúde"""
        self._is_monitoring = True
        while self._is_monitoring:
            try:
                self._check_communication_health()
                time.sleep(30)  # Verifica a cada 30 segundos
            except Exception as e:
                self.logger.error(f"Erro no monitoramento de saúde: {e}")
                time.sleep(60)
    
    def _check_communication_health(self):
        """Verifica saúde da comunicação"""
        try:
            # Verificar Redis
            redis_stats = redis_manager.get_cache_stats()
            redis_healthy = redis_stats.get("redis_healthy", False)
            
            # Verificar WebSocket
            websocket_stats = websocket_manager.get_stats()
            websocket_healthy = websocket_stats.get("is_running", False)
            
            # Log de status
            if not redis_healthy:
                self.logger.warning("Redis não saudável - usando cache local")
            if not websocket_healthy:
                self.logger.warning("WebSocket não saudável - usando modo fallback")
                
        except Exception as e:
            self.logger.error(f"Erro na verificação de saúde: {e}")
    
    def _setup_default_handlers(self):
        """Configura handlers padrão"""
        # Handler para mensagens de progresso
        websocket_manager.register_message_handler("progress_request", self._handle_progress_request)
        websocket_manager.register_message_handler("status_request", self._handle_status_request)
        websocket_manager.register_message_handler("session_info", self._handle_session_info)
    
    def _handle_progress_request(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Manipula solicitação de progresso"""
        try:
            session_id = message.get("session_id")
            if not session_id:
                return {"error": "session_id obrigatório"}
            
            progress_data = redis_manager.get_progress_data(session_id)
            if progress_data:
                return {
                    "type": "progress_response",
                    "session_id": session_id,
                    "data": progress_data,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "type": "progress_response",
                    "session_id": session_id,
                    "data": None,
                    "message": "Dados de progresso não encontrados"
                }
        except Exception as e:
            self.logger.error(f"Erro ao processar solicitação de progresso: {e}")
            return {"error": str(e)}
    
    def _handle_status_request(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Manipula solicitação de status"""
        try:
            session_id = message.get("session_id")
            if not session_id:
                return {"error": "session_id obrigatório"}
            
            session_data = redis_manager.get_session_data(session_id)
            if session_data:
                return {
                    "type": "status_response",
                    "session_id": session_id,
                    "data": session_data,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "type": "status_response",
                    "session_id": session_id,
                    "data": None,
                    "message": "Dados de sessão não encontrados"
                }
        except Exception as e:
            self.logger.error(f"Erro ao processar solicitação de status: {e}")
            return {"error": str(e)}
    
    def _handle_session_info(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Manipula informações de sessão"""
        try:
            session_id = message.get("session_id")
            if not session_id:
                return {"error": "session_id obrigatório"}
            
            # Obter dados completos da sessão
            session_data = redis_manager.get_session_data(session_id)
            progress_data = redis_manager.get_progress_data(session_id)
            
            return {
                "type": "session_info_response",
                "session_id": session_id,
                "session_data": session_data,
                "progress_data": progress_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Erro ao processar informações de sessão: {e}")
            return {"error": str(e)}
    
    def create_session(self, session_data: Dict[str, Any]) -> str:
        """Cria nova sessão"""
        session_id = str(uuid.uuid4())
        
        # Salvar dados da sessão
        redis_manager.set_session_data(session_id, session_data)
        
        # Notificar criação da sessão (sem await para manter síncrono)
        try:
            asyncio.create_task(self.send_session_event(session_id, "session_created", session_data))
        except Exception as e:
            self.logger.warning(f"Erro ao enviar evento de sessão: {e}")
        
        self.logger.info(f"Sessão criada: {session_id}")
        return session_id
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Atualiza dados da sessão"""
        try:
            # Obter dados atuais
            current_data = redis_manager.get_session_data(session_id)
            if not current_data:
                current_data = {}
            
            # Mesclar atualizações
            current_data.update(updates)
            
            # Salvar dados atualizados
            redis_manager.set_session_data(session_id, current_data)
            
            # Notificar atualização (sem await para manter síncrono)
            try:
                asyncio.create_task(self.send_session_event(session_id, "session_updated", updates))
            except Exception as e:
                self.logger.warning(f"Erro ao enviar evento de sessão: {e}")
            
            return True
        except Exception as e:
            self.logger.error(f"Erro ao atualizar sessão {session_id}: {e}")
            return False
    
    def update_progress(self, session_id: str, progress_data: Dict[str, Any]) -> bool:
        """Atualiza progresso da sessão"""
        try:
            # Salvar dados de progresso
            redis_manager.set_progress_data(session_id, progress_data)
            
            # Enviar atualização via WebSocket (sem await para manter síncrono)
            try:
                asyncio.create_task(websocket_manager.send_progress_update(session_id, progress_data))
            except Exception as e:
                self.logger.warning(f"Erro ao enviar progresso via WebSocket: {e}")
            
            # Publicar no Redis
            redis_manager.publish_message(f"progress:{session_id}", progress_data)
            
            return True
        except Exception as e:
            self.logger.error(f"Erro ao atualizar progresso {session_id}: {e}")
            return False
    
    async def send_session_event(self, session_id: str, event_type: str, data: Dict[str, Any]) -> bool:
        """Envia evento de sessão"""
        try:
            message = {
                "type": "session_event",
                "session_id": session_id,
                "event_type": event_type,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            
            # Enviar via WebSocket
            await websocket_manager.send_message(message)
            
            # Publicar no Redis
            redis_manager.publish_message(f"session:{session_id}", message)
            
            return True
        except Exception as e:
            self.logger.error(f"Erro ao enviar evento de sessão: {e}")
            return False
    
    async def send_error(self, session_id: str, error: str, details: Dict[str, Any] = None) -> bool:
        """Envia erro"""
        try:
            # Enviar via WebSocket
            await websocket_manager.send_error(session_id, error, details)
            
            # Publicar no Redis
            error_message = {
                "type": "error",
                "session_id": session_id,
                "error": error,
                "details": details or {},
                "timestamp": datetime.now().isoformat()
            }
            redis_manager.publish_message(f"error:{session_id}", error_message)
            
            return True
        except Exception as e:
            self.logger.error(f"Erro ao enviar erro: {e}")
            return False
    
    def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtém dados da sessão"""
        return redis_manager.get_session_data(session_id)
    
    def get_progress_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtém dados de progresso"""
        return redis_manager.get_progress_data(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        """Remove sessão"""
        try:
            # Remover dados da sessão
            redis_manager.delete(f"session:{session_id}")
            redis_manager.delete(f"progress:{session_id}")
            
            # Notificar remoção (sem await para manter síncrono)
            try:
                asyncio.create_task(self.send_session_event(session_id, "session_deleted", {}))
            except Exception as e:
                self.logger.warning(f"Erro ao enviar evento de sessão: {e}")
            
            return True
        except Exception as e:
            self.logger.error(f"Erro ao remover sessão {session_id}: {e}")
            return False
    
    def register_session_handler(self, session_id: str, handler: Callable):
        """Registra handler para sessão específica"""
        self._session_handlers[session_id] = handler
        self.logger.info(f"Handler registrado para sessão: {session_id}")
    
    def unregister_session_handler(self, session_id: str):
        """Remove handler de sessão"""
        if session_id in self._session_handlers:
            del self._session_handlers[session_id]
            self.logger.info(f"Handler removido para sessão: {session_id}")
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas de comunicação"""
        return {
            "redis_stats": redis_manager.get_cache_stats(),
            "websocket_stats": websocket_manager.get_stats(),
            "session_handlers": len(self._session_handlers),
            "is_monitoring": self._is_monitoring
        }
    
    def stop_monitoring(self):
        """Para monitoramento"""
        self._is_monitoring = False
        if self._health_monitor_thread and self._health_monitor_thread.is_alive():
            self._health_monitor_thread.join(timeout=5)


# Instância global
communication_manager = CommunicationManager()


# Funções de conveniência
def create_session(session_data: Dict[str, Any]) -> str:
    """Função de conveniência para criar sessão"""
    return communication_manager.create_session(session_data)


def update_session(session_id: str, updates: Dict[str, Any]) -> bool:
    """Função de conveniência para atualizar sessão"""
    return communication_manager.update_session(session_id, updates)


def update_progress(session_id: str, progress_data: Dict[str, Any]) -> bool:
    """Função de conveniência para atualizar progresso"""
    return communication_manager.update_progress(session_id, progress_data)


def send_session_event(session_id: str, event_type: str, data: Dict[str, Any]) -> bool:
    """Função de conveniência para enviar evento"""
    return communication_manager.send_session_event(session_id, event_type, data)


def get_session_data(session_id: str) -> Optional[Dict[str, Any]]:
    """Função de conveniência para obter dados da sessão"""
    return communication_manager.get_session_data(session_id)


def get_progress_data(session_id: str) -> Optional[Dict[str, Any]]:
    """Função de conveniência para obter dados de progresso"""
    return communication_manager.get_progress_data(session_id)





























"""
Interface unificada para ProgressTracker
Detecção automática de backend (Redis vs JSON)
"""

import os
from typing import Optional
from .progress_database_json import DatabaseProgressTracker
from .progress_redis import RedisProgressTracker


def detectar_progress_tracker(tipo_solicitado: str = 'auto') -> Optional[type]:
    """
    Detecta automaticamente o melhor progress tracker disponível
    
    Args:
        tipo_solicitado: Tipo solicitado ('auto', 'redis', 'json', 'none')
        
    Returns:
        Classe do progress tracker ou None
    """
    if tipo_solicitado == 'none':
        return None
    
    if tipo_solicitado == 'redis':
        try:
            return RedisProgressTracker
        except ImportError:
            print("⚠️  Redis não disponível, usando JSON como fallback")
            return DatabaseProgressTracker
    
    if tipo_solicitado == 'json':
        return DatabaseProgressTracker
    
    # Modo 'auto' - detectar automaticamente
    try:
        import redis
        r = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            password=os.getenv('REDIS_PASSWORD', None),
            socket_connect_timeout=2,
            socket_timeout=2
        )
        r.ping()
        print("✅ Redis detectado, usando Redis Progress Tracker")
        return RedisProgressTracker
    except Exception:
        print("⚠️  Redis não disponível, usando JSON Progress Tracker")
        return DatabaseProgressTracker


class ProgressTracker:
    """
    Interface unificada para ProgressTracker
    Detecta automaticamente o melhor backend disponível
    """
    
    def __init__(self, total_etapas: int = 15, usar_arquivo: bool = True, session_id: str = None, tipo: str = 'auto'):
        """
        Inicializa o ProgressTracker com detecção automática
        
        Args:
            total_etapas: Número total de etapas (padrão: 15)
            usar_arquivo: Se deve usar arquivo para persistência
            session_id: ID da sessão para execução concorrente
            tipo: Tipo de backend ('auto', 'redis', 'json', 'none')
        """
        self.tipo = tipo
        self.session_id = session_id
        
        # Detectar tipo de progress tracker
        ProgressTrackerClass = detectar_progress_tracker(tipo)
        
        if ProgressTrackerClass:
            self.tracker = ProgressTrackerClass(
                total_etapas=total_etapas,
                usar_arquivo=usar_arquivo,
                session_id=session_id
            )
        else:
            self.tracker = None
    
    def update_progress(self, etapa: int, mensagem: str = "", dados_extra: dict = None):
        """Atualiza o progresso da execução"""
        if self.tracker:
            self.tracker.update_progress(etapa, mensagem, dados_extra)
    
    def add_error(self, erro: str, contexto: str = ""):
        """Adiciona um erro ao progresso"""
        if self.tracker:
            self.tracker.add_error(erro, contexto)
    
    def finalizar(self, status_final: str = "success", dados_finais: dict = None, erro_final: str = None):
        """Finaliza o progresso"""
        if self.tracker:
            self.tracker.finalizar(status_final, dados_finais, erro_final)
    
    def get_progress(self) -> dict:
        """Retorna o progresso atual"""
        if self.tracker:
            return self.tracker.get_progress()
        else:
            return {
                "etapa_atual": 0,
                "total_etapas": 15,
                "percentual": 0.0,
                "status": "iniciando",
                "mensagem": "ProgressTracker desabilitado",
                "timestamp_inicio": "",
                "timestamp_atualizacao": "",
                "dados_extra": {},
                "erros": [],
                "session_id": self.session_id,
                "backend": "none"
            }
    
    def limpar_dados(self):
        """Remove os dados da sessão"""
        if self.tracker:
            if hasattr(self.tracker, 'limpar_dados'):
                self.tracker.limpar_dados()
            elif hasattr(self.tracker, 'limpar_arquivos'):
                self.tracker.limpar_arquivos()
    
    @classmethod
    def carregar_sessao(cls, session_id: str, tipo: str = 'auto') -> Optional['ProgressTracker']:
        """
        Carrega uma sessão existente
        
        Args:
            session_id: ID da sessão
            tipo: Tipo de backend ('auto', 'redis', 'json', 'none')
            
        Returns:
            ProgressTracker carregado ou None
        """
        # Tentar carregar do Redis primeiro
        if tipo in ['auto', 'redis']:
            try:
                tracker_redis = RedisProgressTracker.carregar_sessao(session_id)
                if tracker_redis:
                    progress_tracker = cls(tipo='redis', session_id=session_id)
                    progress_tracker.tracker = tracker_redis
                    return progress_tracker
            except Exception:
                pass
        
        # Fallback para JSON
        if tipo in ['auto', 'json']:
            try:
                tracker_json = DatabaseProgressTracker.carregar_sessao(session_id)
                if tracker_json:
                    progress_tracker = cls(tipo='json', session_id=session_id)
                    progress_tracker.tracker = tracker_json
                    return progress_tracker
            except Exception:
                pass
        
        return None
    
    def __getattr__(self, name):
        """Delega atributos não encontrados para o tracker interno"""
        if self.tracker:
            return getattr(self.tracker, name)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


# Alias para compatibilidade com a v3.4.0
def criar_progress_tracker(total_etapas: int = 15, usar_arquivo: bool = True, session_id: str = None, tipo: str = 'auto') -> ProgressTracker:
    """
    Função de conveniência para criar um ProgressTracker
    
    Args:
        total_etapas: Número total de etapas
        usar_arquivo: Se deve usar arquivo para persistência
        session_id: ID da sessão
        tipo: Tipo de backend
        
    Returns:
        ProgressTracker configurado
    """
    return ProgressTracker(
        total_etapas=total_etapas,
        usar_arquivo=usar_arquivo,
        session_id=session_id,
        tipo=tipo
    )


# Função para verificar disponibilidade do Redis
def verificar_redis_disponivel() -> bool:
    """
    Verifica se o Redis está disponível
    
    Returns:
        True se Redis está disponível, False caso contrário
    """
    try:
        import redis
        r = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            password=os.getenv('REDIS_PASSWORD', None),
            socket_connect_timeout=2,
            socket_timeout=2
        )
        r.ping()
        return True
    except Exception:
        return False


# Função para obter informações do backend
def obter_info_backend() -> dict:
    """
    Obtém informações sobre o backend disponível
    
    Returns:
        Dict com informações do backend
    """
    redis_disponivel = verificar_redis_disponivel()
    
    return {
        "redis_disponivel": redis_disponivel,
        "backend_recomendado": "redis" if redis_disponivel else "json",
        "configuracao_redis": {
            "host": os.getenv('REDIS_HOST', 'localhost'),
            "port": int(os.getenv('REDIS_PORT', 6379)),
            "db": int(os.getenv('REDIS_DB', 0)),
            "password": "***" if os.getenv('REDIS_PASSWORD') else None
        }
    }
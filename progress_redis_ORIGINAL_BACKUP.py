"""
ProgressTracker baseado em Redis
Para execução concorrente e alta performance
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
import os


class RedisProgressTracker:
    """
    ProgressTracker que usa Redis como backend
    Para execução concorrente e alta performance
    """
    
    def __init__(self, total_etapas: int = 15, usar_arquivo: bool = True, session_id: str = None):
        """
        Inicializa o ProgressTracker Redis
        
        Args:
            total_etapas: Número total de etapas (padrão: 15)
            usar_arquivo: Se deve usar arquivo para persistência (fallback)
            session_id: ID da sessão para execução concorrente
        """
        self.total_etapas = total_etapas
        self.usar_arquivo = usar_arquivo
        self.session_id = session_id or "default"
        self.etapa_atual = 0
        self.percentual = 0.0
        self.status = "iniciando"
        self.mensagem = "Inicializando"
        self.timestamp_inicio = datetime.now().isoformat()
        self.timestamp_atualizacao = datetime.now().isoformat()
        self.dados_extra = {}
        self.erros = []
        
        # Configurações Redis
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_db = int(os.getenv('REDIS_DB', 0))
        self.redis_password = os.getenv('REDIS_PASSWORD', None)
        
        # Chaves Redis
        self.chave_progresso = f"rpa:progress:{self.session_id}"
        self.chave_resultado = f"rpa:result:{self.session_id}"
        self.chave_sessao = f"rpa:session:{self.session_id}"
        
        # TTL (Time To Live) em segundos (24 horas)
        self.ttl = 86400
        
        # Inicializar Redis
        self.redis_client = None
        self._conectar_redis()
        
        # Inicializar progresso
        if self.redis_client:
            self._salvar_progresso_redis()
        elif self.usar_arquivo:
            # Fallback para arquivo se Redis não disponível
            self._salvar_progresso_arquivo()
    
    def _conectar_redis(self):
        """Conecta ao Redis"""
        try:
            import redis
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                password=self.redis_password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Testar conexão
            self.redis_client.ping()
        except Exception:
            self.redis_client = None
    
    def update_progress(self, etapa: int, mensagem: str = "", dados_extra: Dict[str, Any] = None):
        """
        Atualiza o progresso da execução
        
        Args:
            etapa: Número da etapa atual (0-15)
            mensagem: Mensagem descritiva da etapa
            dados_extra: Dados adicionais para a etapa
        """
        self.etapa_atual = min(etapa, self.total_etapas)
        self.percentual = (self.etapa_atual / self.total_etapas) * 100
        # ✅ V6.13.1: Substituições terminológicas
        mensagem_formatada = mensagem or ""
        mensagem_formatada = mensagem_formatada.replace("Tela ", "Processo ")
        mensagem_formatada = mensagem_formatada.replace("concluída", "finalizou")
        self.mensagem = mensagem_formatada or f"Etapa {etapa}"
        self.timestamp_atualizacao = datetime.now().isoformat()
        
        if dados_extra:
            self.dados_extra.update(dados_extra)
        
        # Determinar status baseado no progresso
        if self.etapa_atual == 0:
            self.status = "iniciando"
        elif self.etapa_atual < self.total_etapas:
            self.status = "executando"
        else:
            self.status = "concluido"
        
        # Salvar progresso
        if self.redis_client:
            self._salvar_progresso_redis()
        elif self.usar_arquivo:
            self._salvar_progresso_arquivo()
    
    def add_estimativas(self, estimativas: Dict[str, Any]):
        """
        Adiciona estimativas da tela 5 ao progresso
        
        Args:
            estimativas: Dados das estimativas capturadas na tela 5
        """
        if estimativas:
            self.dados_extra['estimativas_tela_5'] = estimativas
            self.timestamp_atualizacao = datetime.now().isoformat()
            # Salvar progresso atualizado
            if self.redis_client:
                self._salvar_progresso_redis()
            elif self.usar_arquivo:
                self._salvar_progresso_arquivo()
    
    def add_error(self, erro: str, contexto: str = ""):
        """
        Adiciona um erro ao progresso
        
        Args:
            erro: Mensagem de erro
            contexto: Contexto onde o erro ocorreu
        """
        erro_info = {
            "erro": erro,
            "contexto": contexto,
            "timestamp": datetime.now().isoformat()
        }
        self.erros.append(erro_info)
        
        if self.redis_client:
            self._salvar_progresso_redis()
        elif self.usar_arquivo:
            self._salvar_progresso_arquivo()
    
    def finalizar(self, status_final: str = "success", dados_finais: Dict[str, Any] = None, erro_final: str = None):
        """
        Finaliza o progresso
        
        Args:
            status_final: Status final ('success', 'error', 'warning')
            dados_finais: Dados finais da execução
            erro_final: Erro final se houver
        """
        self.status = status_final
        self.etapa_atual = self.total_etapas
        self.percentual = 100.0
        self.timestamp_atualizacao = datetime.now().isoformat()
        
        if erro_final:
            self.add_error(erro_final, "finalizacao")
        
        if dados_finais:
            self.dados_extra.update(dados_finais)
        
        # Salvar progresso final
        if self.redis_client:
            self._salvar_progresso_redis()
            self._salvar_resultado_redis(dados_finais)
            self._salvar_sessao_redis()
        elif self.usar_arquivo:
            self._salvar_progresso_arquivo()
            self._salvar_resultado_arquivo(dados_finais)
            self._salvar_sessao_arquivo()
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Retorna o progresso atual
        
        Returns:
            Dict com informações de progresso
        """
        return {
            "etapa_atual": self.etapa_atual,
            "total_etapas": self.total_etapas,
            "percentual": self.percentual,
            "status": self.status,
            "mensagem": self.mensagem,
            "timestamp_inicio": self.timestamp_inicio,
            "timestamp_atualizacao": self.timestamp_atualizacao,
            "dados_extra": self.dados_extra,
            "erros": self.erros,
            "session_id": self.session_id,
            "backend": "redis" if self.redis_client else "json"
        }
    
    def _salvar_progresso_redis(self):
        """Salva o progresso atual no Redis"""
        try:
            if not self.redis_client:
                return
            
            progresso_data = self.get_progress()
            self.redis_client.setex(
                self.chave_progresso,
                self.ttl,
                json.dumps(progresso_data, ensure_ascii=False)
            )
        except Exception:
            # Não falhar se não conseguir salvar no Redis
            pass
    
    def _salvar_resultado_redis(self, dados_finais: Dict[str, Any] = None):
        """Salva o resultado final no Redis"""
        try:
            if not self.redis_client:
                return
            
            resultado_data = {
                "status": self.status,
                "timestamp_fim": datetime.now().isoformat(),
                "dados_finais": dados_finais or {},
                "session_id": self.session_id,
                "backend": "redis"
            }
            self.redis_client.setex(
                self.chave_resultado,
                self.ttl,
                json.dumps(resultado_data, ensure_ascii=False)
            )
        except Exception:
            # Não falhar se não conseguir salvar no Redis
            pass
    
    def _salvar_sessao_redis(self):
        """Salva informações da sessão no Redis"""
        try:
            if not self.redis_client:
                return
            
            sessao_data = {
                "session_id": self.session_id,
                "timestamp_inicio": self.timestamp_inicio,
                "timestamp_fim": datetime.now().isoformat(),
                "status": self.status,
                "total_etapas": self.total_etapas,
                "etapas_executadas": self.etapa_atual,
                "backend": "redis"
            }
            self.redis_client.setex(
                self.chave_sessao,
                self.ttl,
                json.dumps(sessao_data, ensure_ascii=False)
            )
        except Exception:
            # Não falhar se não conseguir salvar no Redis
            pass
    
    def _salvar_progresso_arquivo(self):
        """Fallback: salva o progresso em arquivo JSON"""
        try:
            from pathlib import Path
            import json
            
            diretorio_base = Path("rpa_data")
            diretorio_base.mkdir(exist_ok=True)
            
            arquivo_progresso = diretorio_base / f"progress_{self.session_id}.json"
            progresso_data = self.get_progress()
            
            with open(arquivo_progresso, 'w', encoding='utf-8') as f:
                json.dump(progresso_data, f, indent=2, ensure_ascii=False)
        except Exception:
            # Não falhar se não conseguir salvar
            pass
    
    def _salvar_resultado_arquivo(self, dados_finais: Dict[str, Any] = None):
        """Fallback: salva o resultado em arquivo JSON"""
        try:
            from pathlib import Path
            import json
            
            diretorio_base = Path("rpa_data")
            diretorio_base.mkdir(exist_ok=True)
            
            arquivo_resultado = diretorio_base / f"result_{self.session_id}.json"
            resultado_data = {
                "status": self.status,
                "timestamp_fim": datetime.now().isoformat(),
                "dados_finais": dados_finais or {},
                "session_id": self.session_id,
                "backend": "json"
            }
            
            with open(arquivo_resultado, 'w', encoding='utf-8') as f:
                json.dump(resultado_data, f, indent=2, ensure_ascii=False)
        except Exception:
            # Não falhar se não conseguir salvar
            pass
    
    def _salvar_sessao_arquivo(self):
        """Fallback: salva a sessão em arquivo JSON"""
        try:
            from pathlib import Path
            import json
            
            diretorio_base = Path("rpa_data")
            diretorio_base.mkdir(exist_ok=True)
            
            arquivo_sessao = diretorio_base / f"session_{self.session_id}.json"
            sessao_data = {
                "session_id": self.session_id,
                "timestamp_inicio": self.timestamp_inicio,
                "timestamp_fim": datetime.now().isoformat(),
                "status": self.status,
                "total_etapas": self.total_etapas,
                "etapas_executadas": self.etapa_atual,
                "backend": "json"
            }
            
            with open(arquivo_sessao, 'w', encoding='utf-8') as f:
                json.dump(sessao_data, f, indent=2, ensure_ascii=False)
        except Exception:
            # Não falhar se não conseguir salvar
            pass
    
    def limpar_dados(self):
        """Remove os dados da sessão do Redis e arquivos"""
        try:
            # Limpar Redis
            if self.redis_client:
                self.redis_client.delete(self.chave_progresso)
                self.redis_client.delete(self.chave_resultado)
                self.redis_client.delete(self.chave_sessao)
            
            # Limpar arquivos (fallback)
            from pathlib import Path
            diretorio_base = Path("rpa_data")
            
            arquivos = [
                diretorio_base / f"progress_{self.session_id}.json",
                diretorio_base / f"result_{self.session_id}.json",
                diretorio_base / f"session_{self.session_id}.json"
            ]
            
            for arquivo in arquivos:
                if arquivo.exists():
                    arquivo.unlink()
                    
        except Exception:
            # Não falhar se não conseguir limpar
            pass
    
    @classmethod
    def carregar_sessao(cls, session_id: str) -> Optional['RedisProgressTracker']:
        """
        Carrega uma sessão existente
        
        Args:
            session_id: ID da sessão
            
        Returns:
            RedisProgressTracker carregado ou None
        """
        try:
            # Tentar carregar do Redis primeiro
            import redis
            redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                password=os.getenv('REDIS_PASSWORD', None),
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            chave_progresso = f"rpa:progress:{session_id}"
            data_json = redis_client.get(chave_progresso)
            
            if data_json:
                data = json.loads(data_json)
                
                tracker = cls(
                    total_etapas=data.get('total_etapas', 15),
                    usar_arquivo=True,
                    session_id=session_id
                )
                
                # Restaurar estado
                tracker.etapa_atual = data.get('etapa_atual', 0)
                tracker.percentual = data.get('percentual', 0.0)
                tracker.status = data.get('status', 'iniciando')
                tracker.mensagem = data.get('mensagem', '')
                tracker.timestamp_inicio = data.get('timestamp_inicio', datetime.now().isoformat())
                tracker.timestamp_atualizacao = data.get('timestamp_atualizacao', datetime.now().isoformat())
                tracker.dados_extra = data.get('dados_extra', {})
                tracker.erros = data.get('erros', [])
                
                return tracker
            
            # Fallback: tentar carregar do arquivo
            from pathlib import Path
            arquivo_progresso = Path("rpa_data") / f"progress_{session_id}.json"
            if arquivo_progresso.exists():
                with open(arquivo_progresso, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                tracker = cls(
                    total_etapas=data.get('total_etapas', 15),
                    usar_arquivo=True,
                    session_id=session_id
                )
                
                # Restaurar estado
                tracker.etapa_atual = data.get('etapa_atual', 0)
                tracker.percentual = data.get('percentual', 0.0)
                tracker.status = data.get('status', 'iniciando')
                tracker.mensagem = data.get('mensagem', '')
                tracker.timestamp_inicio = data.get('timestamp_inicio', datetime.now().isoformat())
                tracker.timestamp_atualizacao = data.get('timestamp_atualizacao', datetime.now().isoformat())
                tracker.dados_extra = data.get('dados_extra', {})
                tracker.erros = data.get('erros', [])
                
                return tracker
            
            return None
            
        except Exception:
            return None
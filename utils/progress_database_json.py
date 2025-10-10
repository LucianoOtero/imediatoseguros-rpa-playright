"""
ProgressTracker baseado em arquivos JSON
Compatível com a v3.4.0 e preparado para Redis
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class DatabaseProgressTracker:
    """
    ProgressTracker que usa arquivos JSON como backend
    Mantém compatibilidade com a v3.4.0
    """
    
    def __init__(self, total_etapas: int = 15, usar_arquivo: bool = True,
                 session_id: str = None):
        """
        Inicializa o ProgressTracker JSON
        
        Args:
            total_etapas: Número total de etapas (padrão: 15)
            usar_arquivo: Se deve usar arquivo para persistência
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
        
        # Criar diretório se não existir
        self.diretorio_base = Path("rpa_data")
        self.diretorio_base.mkdir(exist_ok=True)
        
        # Nome do arquivo baseado na sessão
        self.arquivo_progresso = (self.diretorio_base /
                                  f"progress_{self.session_id}.json")
        self.arquivo_resultado = (self.diretorio_base /
                                 f"result_{self.session_id}.json")
        self.arquivo_sessao = (self.diretorio_base /
                              f"session_{self.session_id}.json")
        self.arquivo_historico = (self.diretorio_base /
                                 f"history_{self.session_id}.json")
        
        # Histórico sequencial
        self.historico = []
        self.historico_habilitado = True
        
        # Inicializar arquivo de progresso
        if self.usar_arquivo:
            self._salvar_progresso()
            if self.historico_habilitado:
                self._adicionar_entrada_historico(
                    "inicio", "iniciando", "ProgressTracker inicializado")
    
    def update_progress(self, etapa: int, mensagem: str = "",
                       dados_extra: Dict[str, Any] = None):
        """
        Atualiza o progresso da execução
        
        Args:
            etapa: Número da etapa atual (0-15)
            mensagem: Mensagem descritiva da etapa
            dados_extra: Dados adicionais para a etapa
        """
        self.etapa_atual = min(etapa, self.total_etapas)
        self.percentual = (self.etapa_atual / self.total_etapas) * 100
        self.mensagem = mensagem or f"Etapa {etapa}"
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
        if self.usar_arquivo:
            self._salvar_progresso()
            if self.historico_habilitado:
                self._adicionar_entrada_historico(
                    etapa, self.status, mensagem, dados_extra)
    
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
        
        if self.usar_arquivo:
            self._salvar_progresso()
            if self.historico_habilitado:
                self._adicionar_entrada_historico(
                    "erro", "error", f"Erro: {erro}", None, erro)
    
    def add_estimativas(self, estimativas: Dict[str, Any]):
        """
        Adiciona estimativas da tela 5 ao progresso
        
        Args:
            estimativas: Dados das estimativas capturadas na tela 5
        """
        if estimativas:
            self.dados_extra['estimativas_tela_5'] = estimativas
            self.timestamp_atualizacao = datetime.now().isoformat()
            
            if self.usar_arquivo:
                self._salvar_progresso()
                if self.historico_habilitado:
                    self._adicionar_entrada_historico(
                        "estimativas", "completed", "Estimativas capturadas",
                        estimativas)
    
    def finalizar(self, status_final: str = "success",
                 dados_finais: Dict[str, Any] = None, erro_final: str = None):
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
        if self.usar_arquivo:
            self._salvar_progresso()
            self._salvar_resultado(dados_finais)
            self._salvar_sessao()
            if self.historico_habilitado:
                self._adicionar_entrada_historico(
                    "final", status_final, f"RPA {status_final}",
                    dados_finais, erro_final)
                # REMOVIDO: self._salvar_historico() 
                # Motivo: O histórico agora é salvo automaticamente após cada atualização
                # no método _adicionar_entrada_historico(), então não é mais necessário
                # salvar aqui no finalizar()
    
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
            "session_id": self.session_id
        }
    
    def _salvar_progresso(self):
        """Salva o progresso atual em arquivo JSON"""
        try:
            progresso_data = self.get_progress()
            with open(self.arquivo_progresso, 'w', encoding='utf-8') as f:
                json.dump(progresso_data, f, indent=2, ensure_ascii=False)
        except Exception:
            # Não falhar se não conseguir salvar
            pass
    
    def _salvar_resultado(self, dados_finais: Dict[str, Any] = None):
        """Salva o resultado final em arquivo JSON"""
        try:
            resultado_data = {
                "status": self.status,
                "timestamp_fim": datetime.now().isoformat(),
                "dados_finais": dados_finais or {},
                "session_id": self.session_id
            }
            with open(self.arquivo_resultado, 'w', encoding='utf-8') as f:
                json.dump(resultado_data, f, indent=2, ensure_ascii=False)
        except Exception:
            # Não falhar se não conseguir salvar
            pass
    
    def _salvar_sessao(self):
        """Salva informações da sessão em arquivo JSON"""
        try:
            sessao_data = {
                "session_id": self.session_id,
                "timestamp_inicio": self.timestamp_inicio,
                "timestamp_fim": datetime.now().isoformat(),
                "status": self.status,
                "total_etapas": self.total_etapas,
                "etapas_executadas": self.etapa_atual
            }
            with open(self.arquivo_sessao, 'w', encoding='utf-8') as f:
                json.dump(sessao_data, f, indent=2, ensure_ascii=False)
        except Exception:
            # Não falhar se não conseguir salvar
            pass
    
    def limpar_arquivos(self):
        """Remove os arquivos de progresso da sessão"""
        try:
            if self.arquivo_progresso.exists():
                self.arquivo_progresso.unlink()
            if self.arquivo_resultado.exists():
                self.arquivo_resultado.unlink()
            if self.arquivo_sessao.exists():
                self.arquivo_sessao.unlink()
        except Exception:
            # Não falhar se não conseguir limpar
            pass
    
    @classmethod
    def carregar_sessao(cls, session_id: str) -> Optional['DatabaseProgressTracker']:
        """
        Carrega uma sessão existente
        
        Args:
            session_id: ID da sessão
            
        Returns:
            DatabaseProgressTracker carregado ou None
        """
        try:
            arquivo_progresso = Path("rpa_data") / f"progress_{session_id}.json"
            if not arquivo_progresso.exists():
                return None
            
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
            tracker.timestamp_inicio = data.get(
                'timestamp_inicio', datetime.now().isoformat())
            tracker.timestamp_atualizacao = data.get(
                'timestamp_atualizacao', datetime.now().isoformat())
            tracker.dados_extra = data.get('dados_extra', {})
            tracker.erros = data.get('erros', [])
            
            return tracker
            
        except Exception:
            return None
    
    def _adicionar_entrada_historico(self, etapa, status, mensagem,
                                    dados_extra=None, erro=None):
        """
        Adiciona entrada ao histórico sequencial
        
        Args:
            etapa: Número da etapa ou identificador
            status: Status da etapa
            mensagem: Mensagem descritiva
            dados_extra: Dados extras opcionais
            erro: Erro se houver
        """
        entrada = {
            "etapa": etapa,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "mensagem": mensagem,
            "dados_extra": dados_extra,
            "erro": erro
        }
        self.historico.append(entrada)
        # Salvar histórico após cada atualização para garantir persistência
        # mesmo se o processo for interrompido antes do finalizar()
        self._salvar_historico()
    
    def _salvar_historico(self):
        """Salva histórico em arquivo JSON"""
        try:
            historico_data = {
                "session_id": self.session_id,
                "timestamp_inicio": self.timestamp_inicio,
                "timestamp_fim": self.timestamp_atualizacao,
                "status_final": self.status,
                "total_etapas": self.total_etapas,
                "historico": self.historico
            }
            
            with open(self.arquivo_historico, 'w', encoding='utf-8') as f:
                json.dump(historico_data, f, indent=2, ensure_ascii=False)
        except Exception:
            # Não falhar se não conseguir salvar histórico
            pass
    
    def get_historico(self):
        """Retorna histórico completo da sessão"""
        return {
            "session_id": self.session_id,
            "timestamp_inicio": self.timestamp_inicio,
            "timestamp_fim": self.timestamp_atualizacao,
            "status_final": self.status,
            "total_etapas": self.total_etapas,
            "historico": self.historico
        }

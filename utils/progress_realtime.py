import json
import os
from datetime import datetime
from typing import Dict, Any


class ProgressTracker:
    """
    Sistema de progresso em tempo real para RPA
    """
    
    # Mapeamento de etapas para descrições compreensivas
    DESCRICOES_ETAPAS = {
        1: "Selecionando Tipo de Veiculo",
        2: "Selecionando veículo com a placa informada",
        3: "Confirmando seleção do veículo",
        4: "Calculando como novo Seguro",
        5: "Elaborando estimativas",
        6: "Seleção de detalhes do veículo",
        7: "Definição de local de pernoite com o CEP informado",
        8: "Definição do uso do veículo",
        9: "Preenchimento dos dados pessoais",
        10: "Definição do Condutor Principal",
        11: "Definição do uso do veículo",
        12: "Definição do tipo de garagem",
        13: "Definição de residentes",
        14: "Definição do Corretor",
        15: "Aguardando cálculo completo"
    }
    
    def __init__(self, total_etapas: int = 15, usar_arquivo: bool = True, session_id: str = None):
        self.total_etapas = total_etapas
        self.current_etapa = 0
        self.start_time = datetime.now()
        self.usar_arquivo = usar_arquivo
        self.session_id = session_id or "default"
        
        # Definir arquivo de progresso baseado na sessão
        if usar_arquivo:
            self.progress_file = f"temp/progress_{self.session_id}.json"
        else:
            self.progress_file = None
            
        self.progress_data = {}  # Armazenar dados em memória quando usar_arquivo=False
        self.etapas_historico = []  # Histórico completo das etapas
        
    def update_progress(self, etapa_atual: int, status: str = None,
                       details: Dict[str, Any] = None):
        """
        Atualiza o progresso de forma segura
        """
        try:
            self.current_etapa = etapa_atual
            
            # Usar descrição padrão se não fornecida
            if status is None:
                status = self.DESCRICOES_ETAPAS.get(
                    etapa_atual, f"Etapa {etapa_atual}"
                )
            
            progress_data = {
                "timestamp": datetime.now().isoformat(),
                "etapa_atual": etapa_atual,
                "total_etapas": self.total_etapas,
                "percentual": (etapa_atual / self.total_etapas) * 100,
                "status": status,
                "descricao_etapa": self.DESCRICOES_ETAPAS.get(
                    etapa_atual, f"Etapa {etapa_atual}"
                ),
                "tempo_decorrido": (
                    datetime.now() - self.start_time
                ).total_seconds(),
                "tempo_estimado_restante": self._calcular_tempo_restante(),
                "details": details or {}
            }
            
            # Adicionar ao histórico
            etapa_info = {
                "etapa": etapa_atual,
                "status": status,
                "timestamp": datetime.now().isoformat(),
                "tempo_etapa": progress_data["tempo_decorrido"]
            }
            self.etapas_historico.append(etapa_info)
            
            # Adicionar informações específicas para Etapa 5
            if etapa_atual == 5 and details:
                progress_data["json_retorno"] = "Estimativas disponíveis"
            
            if self.usar_arquivo:
                # Modo atual: salvar arquivo (compatibilidade)
                with open(self.progress_file, 'w', encoding='utf-8') as f:
                    json.dump(progress_data, f, indent=2, ensure_ascii=False)
            else:
                # Modo novo: armazenar em memória
                self.progress_data = progress_data
                
            return True
        except Exception as e:
            # Log de erro sem interromper execução
            print(f"⚠️ Erro ao atualizar progresso: {e}")
            return False
    
    def _calcular_tempo_restante(self) -> float:
        """Calcula tempo estimado restante baseado no progresso atual"""
        if self.current_etapa == 0:
            return 0
        
        tempo_medio_por_etapa = (
            datetime.now() - self.start_time
        ).total_seconds() / self.current_etapa
        etapas_restantes = self.total_etapas - self.current_etapa
        return tempo_medio_por_etapa * etapas_restantes
    
    def get_current_progress(self) -> Dict[str, Any]:
        """Retorna o progresso atual"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ Erro ao ler progresso: {e}")
            return {}
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Retorna dados de progresso para inclusão no resultado final
        """
        if self.usar_arquivo:
            # Modo compatibilidade: ler do arquivo
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Adicionar histórico se disponível
                    data["etapas_historico"] = self.etapas_historico
                    return data
            except:
                return {"erro": "Arquivo de progresso não encontrado"}
        else:
            # Modo novo: retornar dados da memória
            if self.progress_data:
                self.progress_data["etapas_historico"] = self.etapas_historico
                return self.progress_data
            else:
                return {"erro": "Dados de progresso não disponíveis"}
    
    def reset_progress(self):
        """Reseta o progresso"""
        self.current_etapa = 0
        self.start_time = datetime.now()
        self.etapas_historico = []
        self.update_progress(0, "Progresso resetado")

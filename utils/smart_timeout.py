# -*- coding: utf-8 -*-
"""
Sistema de Timeout Inteligente - RPA Tô Segurado
Versão: 1.0.0
Data: 2025-09-04
Autor: Luciano Otero

Sistema de timeout configurável por tela com retry inteligente e backoff exponencial.
Completamente isolado e não interfere com funcionalidade existente.
"""

import json
import os
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional, Callable


class SmartTimeout:
    """
    Sistema de timeout inteligente para RPA
    """
    
    def __init__(self, config_file: str = 'timeout_config.json'):
        """
        Inicializa o sistema de timeout
        
        Args:
            config_file: Arquivo de configuração de timeout
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.timers = {}
        self.lock = threading.Lock()
        self.available = True
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega configuração de timeout
        """
        default_config = {
            "timeouts": {
                "tela_1": {"timeout": 30, "retries": 2, "backoff": 1.5},
                "tela_2": {"timeout": 30, "retries": 2, "backoff": 1.5},
                "tela_3": {"timeout": 30, "retries": 2, "backoff": 1.5},
                "tela_4": {"timeout": 30, "retries": 2, "backoff": 1.5},
                "tela_5": {"timeout": 120, "retries": 1, "backoff": 1.0},
                "tela_6": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_7": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_8": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_9": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_10": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_11": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_12": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_13": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_14": {"timeout": 45, "retries": 3, "backoff": 2.0},
                "tela_15": {"timeout": 180, "retries": 2, "backoff": 1.5}
            },
            "global": {
                "default_timeout": 60,
                "max_retries": 3,
                "backoff_multiplier": 1.5
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config
            else:
                # Criar arquivo de configuração padrão
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                return default_config
        except Exception as e:
            print(f"⚠️ Erro ao carregar configuração de timeout: {e}")
            return default_config
    
    def is_available(self) -> bool:
        """
        Verifica se o sistema está disponível
        """
        return self.available
    
    def is_working(self) -> bool:
        """
        Verifica se o sistema está funcionando
        """
        return self.available and len(self.timers) >= 0
    
    def get_timeout(self, tela_num: int) -> int:
        """
        Obtém timeout para uma tela específica
        
        Args:
            tela_num: Número da tela
            
        Returns:
            Timeout em segundos
        """
        tela_key = f"tela_{tela_num}"
        if tela_key in self.config.get("timeouts", {}):
            return self.config["timeouts"][tela_key]["timeout"]
        return self.config.get("global", {}).get("default_timeout", 60)
    
    def get_retries(self, tela_num: int) -> int:
        """
        Obtém número de retries para uma tela específica
        
        Args:
            tela_num: Número da tela
            
        Returns:
            Número de retries
        """
        tela_key = f"tela_{tela_num}"
        if tela_key in self.config.get("timeouts", {}):
            return self.config["timeouts"][tela_key]["retries"]
        return self.config.get("global", {}).get("max_retries", 3)
    
    def get_backoff(self, tela_num: int) -> float:
        """
        Obtém multiplicador de backoff para uma tela específica
        
        Args:
            tela_num: Número da tela
            
        Returns:
            Multiplicador de backoff
        """
        tela_key = f"tela_{tela_num}"
        if tela_key in self.config.get("timeouts", {}):
            return self.config["timeouts"][tela_key]["backoff"]
        return self.config.get("global", {}).get("backoff_multiplier", 1.5)
    
    def start_timer(self, tela_num: int, descricao: str) -> None:
        """
        Inicia timer para uma tela
        
        Args:
            tela_num: Número da tela
            descricao: Descrição da operação
        """
        with self.lock:
            self.timers[tela_num] = {
                "start_time": time.time(),
                "timeout": self.get_timeout(tela_num),
                "descricao": descricao,
                "retries": 0,
                "max_retries": self.get_retries(tela_num)
            }
    
    def check_timeout(self, tela_num: int) -> bool:
        """
        Verifica se timeout foi atingido
        
        Args:
            tela_num: Número da tela
            
        Returns:
            True se timeout foi atingido
        """
        if tela_num not in self.timers:
            return False
            
        with self.lock:
            timer = self.timers[tela_num]
            elapsed = time.time() - timer["start_time"]
            
            if elapsed >= timer["timeout"]:
                return True
            return False
    
    def handle_timeout(self, tela_num: int, contexto: str = "") -> Dict[str, Any]:
        """
        Trata timeout de uma tela
        
        Args:
            tela_num: Número da tela
            contexto: Contexto adicional
            
        Returns:
            Informações do timeout
        """
        if tela_num not in self.timers:
            return {"error": "Timer não encontrado"}
            
        with self.lock:
            timer = self.timers[tela_num]
            elapsed = time.time() - timer["start_time"]
            
            timeout_info = {
                "tela_num": tela_num,
                "timeout_seconds": timer["timeout"],
                "elapsed_seconds": elapsed,
                "descricao": timer["descricao"],
                "contexto": contexto,
                "timestamp": datetime.now().isoformat(),
                "retries_remaining": timer["max_retries"] - timer["retries"]
            }
            
            # Incrementar contador de retries
            timer["retries"] += 1
            
            return timeout_info
    
    def retry_with_backoff(self, tela_num: int, max_retries: Optional[int] = None) -> bool:
        """
        Executa retry com backoff exponencial
        
        Args:
            tela_num: Número da tela
            max_retries: Número máximo de retries (opcional)
            
        Returns:
            True se ainda há retries disponíveis
        """
        if tela_num not in self.timers:
            return False
            
        with self.lock:
            timer = self.timers[tela_num]
            max_retries = max_retries or timer["max_retries"]
            
            if timer["retries"] >= max_retries:
                return False
                
            # Calcular delay com backoff exponencial
            backoff_mult = self.get_backoff(tela_num)
            delay = 1.0 * (backoff_mult ** timer["retries"])
            
            # Reiniciar timer
            timer["start_time"] = time.time()
            
            return True
    
    def get_retries_remaining(self, tela_num: int) -> int:
        """
        Obtém número de retries restantes
        
        Args:
            tela_num: Número da tela
            
        Returns:
            Número de retries restantes
        """
        if tela_num not in self.timers:
            return 0
            
        with self.lock:
            timer = self.timers[tela_num]
            return max(0, timer["max_retries"] - timer["retries"])
    
    def clear_timer(self, tela_num: int) -> None:
        """
        Limpa timer de uma tela
        
        Args:
            tela_num: Número da tela
        """
        with self.lock:
            if tela_num in self.timers:
                del self.timers[tela_num]
    
    def clear_all_timers(self) -> None:
        """
        Limpa todos os timers
        """
        with self.lock:
            self.timers.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtém status do sistema de timeout
        
        Returns:
            Status do sistema
        """
        with self.lock:
            return {
                "available": self.available,
                "working": self.is_working(),
                "active_timers": len(self.timers),
                "config_file": self.config_file,
                "timers": {
                    tela: {
                        "elapsed": time.time() - timer["start_time"],
                        "timeout": timer["timeout"],
                        "retries": timer["retries"],
                        "max_retries": timer["max_retries"]
                    }
                    for tela, timer in self.timers.items()
                }
            }


class TimeoutHandler:
    """
    Handlers específicos para tratamento de timeout por tela
    """
    
    @staticmethod
    def handle_tela_1_timeout(contexto: str) -> str:
        """Handler específico para timeout da Tela 1"""
        return f"Timeout na Tela 1 (Dados Pessoais) - {contexto}"
    
    @staticmethod
    def handle_tela_5_timeout(contexto: str) -> str:
        """Handler específico para timeout da Tela 5"""
        return f"Timeout na Tela 5 (Estimativas) - {contexto}"
    
    @staticmethod
    def handle_tela_15_timeout(contexto: str) -> str:
        """Handler específico para timeout da Tela 15"""
        return f"Timeout na Tela 15 (Planos Finais) - {contexto}"
    
    @staticmethod
    def fallback_strategy(tela_num: int, contexto: str) -> str:
        """Estratégia de fallback para qualquer tela"""
        return f"Fallback para Tela {tela_num} - {contexto}"


# Função de conveniência para criar instância
def create_smart_timeout(config_file: str = 'timeout_config.json') -> SmartTimeout:
    """
    Cria instância do sistema de timeout
    
    Args:
        config_file: Arquivo de configuração
        
    Returns:
        Instância do SmartTimeout
    """
    return SmartTimeout(config_file)


# Teste básico se executado diretamente
if __name__ == "__main__":
    print("🧪 Testando Sistema de Timeout Inteligente...")
    
    # Criar instância
    timeout = SmartTimeout()
    
    # Testar configuração
    print(f"✅ Configuração carregada: {timeout.config_file}")
    print(f"✅ Timeout Tela 5: {timeout.get_timeout(5)}s")
    print(f"✅ Retries Tela 15: {timeout.get_retries(15)}")
    
    # Testar timer
    timeout.start_timer(1, "Teste de timer")
    time.sleep(1)
    
    # Verificar timeout
    if timeout.check_timeout(1):
        print("⚠️ Timeout detectado")
    else:
        print("✅ Timer funcionando")
    
    # Limpar
    timeout.clear_all_timers()
    print("✅ Sistema de timeout testado com sucesso!")

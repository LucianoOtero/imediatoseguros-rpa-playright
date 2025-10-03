# -*- coding: utf-8 -*-
"""
Sistema de Comunicação Bidirecional - RPA Tô Segurado
Versão: 1.0.0
Data: 2025-09-04
Autor: Luciano Otero

Sistema de comunicação em tempo real entre PHP e Python via HTTP polling.
Completamente isolado e não interfere com funcionalidade existente.
"""

import json
import os
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse


class BidirectionalCommunication:
    """
    Sistema de comunicação bidirecional para RPA
    """
    
    def __init__(self, config_file: str = 'bidirectional_config.json'):
        """
        Inicializa o sistema de comunicação bidirecional
        
        Args:
            config_file: Arquivo de configuração
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.server = None
        self.server_thread = None
        self.status_file = "temp/bidirectional_status.json"
        self.commands_file = "temp/bidirectional_commands.json"
        self.available = True
        self.is_running = False
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega configuração do sistema de comunicação
        """
        default_config = {
            "server": {
                "host": "localhost",
                "port": 8080,
                "enable_server": True
            },
            "client": {
                "php_endpoint": "http://localhost:8000/rpa_status",
                "polling_interval": 2,
                "enable_polling": True
            },
            "commands": {
                "pause": "PAUSE",
                "resume": "RESUME", 
                "cancel": "CANCEL",
                "status": "STATUS"
            },
            "status_codes": {
                "running": "RUNNING",
                "paused": "PAUSED",
                "cancelled": "CANCELLED",
                "completed": "COMPLETED",
                "error": "ERROR"
            },
            "logging": {
                "enabled": True,
                "log_file": "logs/bidirectional.log",
                "detailed_logging": True
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
            print(f"⚠️ Erro ao carregar configuração bidirecional: {e}")
            return default_config

    def is_available(self) -> bool:
        """
        Verifica se o sistema está disponível
        """
        return self.available

    def start_server(self) -> bool:
        """
        Inicia o servidor HTTP para comunicação
        """
        if not self.is_available():
            return False

        try:
            if self.config["server"]["enable_server"]:
                self.server = HTTPServer(
                    (self.config["server"]["host"], self.config["server"]["port"]),
                    CommunicationHandler
                )
                self.server.bidirectional_system = self
                
                # Iniciar servidor em thread separada
                self.server_thread = threading.Thread(target=self.server.serve_forever)
                self.server_thread.daemon = True
                self.server_thread.start()
                
                self.is_running = True
                self.log_event("server_started", f"Servidor iniciado na porta {self.config['server']['port']}")
                return True
        except Exception as e:
            self.log_event("server_error", f"Erro ao iniciar servidor: {str(e)}")
            return False

    def stop_server(self) -> bool:
        """
        Para o servidor HTTP
        """
        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                self.is_running = False
                self.log_event("server_stopped", "Servidor parado")
                return True
        except Exception as e:
            self.log_event("server_error", f"Erro ao parar servidor: {str(e)}")
            return False

    def update_status(self, status: str, details: Dict[str, Any] = None) -> bool:
        """
        Atualiza o status do RPA para o PHP
        
        Args:
            status: Status atual (RUNNING, PAUSED, etc.)
            details: Detalhes adicionais
        """
        if not self.is_available():
            return False

        try:
            status_data = {
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "details": details or {},
                "rpa_version": "3.1.2"
            }

            # Salvar status localmente
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)

            # Enviar para PHP se configurado
            if self.config["client"]["enable_polling"]:
                self._send_to_php(status_data)

            self.log_event("status_updated", f"Status atualizado: {status}")
            return True

        except Exception as e:
            self.log_event("status_error", f"Erro ao atualizar status: {str(e)}")
            return False

    def _send_to_php(self, status_data: Dict[str, Any]) -> bool:
        """
        Envia dados para o PHP via HTTP
        """
        try:
            data = urllib.parse.urlencode(status_data).encode('utf-8')
            req = urllib.request.Request(
                self.config["client"]["php_endpoint"],
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            urllib.request.urlopen(req, timeout=5)
            return True
        except Exception as e:
            self.log_event("php_communication_error", f"Erro ao enviar para PHP: {str(e)}")
            return False

    def check_commands(self) -> Dict[str, Any]:
        """
        Verifica se há comandos do PHP
        """
        if not self.is_available():
            return {"command": None, "timestamp": None}

        try:
            if os.path.exists(self.commands_file):
                with open(self.commands_file, 'r', encoding='utf-8') as f:
                    command_data = json.load(f)
                
                # Limpar arquivo após leitura
                os.remove(self.commands_file)
                return command_data
            return {"command": None, "timestamp": None}

        except Exception as e:
            self.log_event("command_error", f"Erro ao verificar comandos: {str(e)}")
            return {"command": None, "timestamp": None}

    def pause_rpa(self) -> bool:
        """
        Pausa o RPA
        """
        self.update_status("PAUSED", {"reason": "Comando do PHP"})
        self.log_event("rpa_paused", "RPA pausado por comando do PHP")
        return True

    def resume_rpa(self) -> bool:
        """
        Retoma o RPA
        """
        self.update_status("RUNNING", {"reason": "Comando do PHP"})
        self.log_event("rpa_resumed", "RPA retomado por comando do PHP")
        return True

    def cancel_rpa(self) -> bool:
        """
        Cancela o RPA
        """
        self.update_status("CANCELLED", {"reason": "Comando do PHP"})
        self.log_event("rpa_cancelled", "RPA cancelado por comando do PHP")
        return True

    def log_event(self, event_type: str, message: str) -> None:
        """
        Registra eventos no log
        
        Args:
            event_type: Tipo do evento
            message: Mensagem do evento
        """
        if not self.config["logging"]["enabled"]:
            return

        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "message": message,
                "system_version": "1.0.0"
            }

            # Criar pasta de logs se não existir
            log_dir = os.path.dirname(self.config["logging"]["log_file"])
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # Adicionar ao log
            with open(self.config["logging"]["log_file"], 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

        except Exception as e:
            print(f"⚠️ Erro ao registrar log: {e}")

    def get_status(self) -> Dict[str, Any]:
        """
        Obtém status do sistema
        
        Returns:
            Status do sistema
        """
        return {
            "available": self.available,
            "server_running": self.is_running,
            "config_file": self.config_file,
            "version": "1.0.0",
            "logging_enabled": self.config["logging"]["enabled"]
        }


class CommunicationHandler(BaseHTTPRequestHandler):
    """
    Handler para requisições HTTP do PHP
    """
    
    def do_GET(self):
        """
        Endpoint para status do RPA
        """
        try:
            if self.path == '/status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                status_data = self.server.bidirectional_system.get_status()
                self.wfile.write(json.dumps(status_data, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def do_POST(self):
        """
        Endpoint para comandos do PHP
        """
        try:
            if self.path == '/command':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                command_data = json.loads(post_data.decode('utf-8'))
                
                # Processar comando
                if command_data.get('command') == 'PAUSE':
                    self.server.bidirectional_system.pause_rpa()
                elif command_data.get('command') == 'RESUME':
                    self.server.bidirectional_system.resume_rpa()
                elif command_data.get('command') == 'CANCEL':
                    self.server.bidirectional_system.cancel_rpa()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {"status": "success", "command": command_data.get('command')}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def log_message(self, format, *args):
        """
        Suprime logs padrão do servidor HTTP
        """
        pass


# Função de conveniência para criar instância
def create_bidirectional_system(config_file: str = 'bidirectional_config.json') -> BidirectionalCommunication:
    """
    Cria instância do sistema de comunicação bidirecional
    
    Args:
        config_file: Arquivo de configuração
        
    Returns:
        Instância do BidirectionalCommunication
    """
    return BidirectionalCommunication(config_file)


# Teste básico se executado diretamente
if __name__ == "__main__":
    print("🧪 Testando Sistema de Comunicação Bidirecional...")

    # Criar instância
    system = BidirectionalCommunication()

    # Testar configuração
    print(f"✅ Configuração carregada: {system.config_file}")
    print(f"✅ Sistema disponível: {system.is_available()}")

    # Testar atualização de status
    result = system.update_status("TESTING", {"test": True})
    print(f"✅ Status atualizado: {result}")

    # Testar verificação de comandos
    commands = system.check_commands()
    print(f"✅ Comandos verificados: {commands}")

    print("✅ Sistema de comunicação bidirecional testado com sucesso!")



























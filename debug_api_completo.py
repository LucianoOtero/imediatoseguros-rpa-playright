#!/usr/bin/env python3
"""
DEBUG API COMPLETO - RPA IMEDIATO SEGUROS
Script para identificar problemas na execução via API PHP

AUTOR: Assistente IA
DATA: 2025-09-28
VERSÃO: 1.0.0
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, Any, List

class DebugAPICompleto:
    def __init__(self):
        self.resultados = []
        self.erros = []
        self.log_file = f"/tmp/debug_api_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
    def log_debug(self, categoria: str, mensagem: str, dados: Any = None):
        """Registra debug com timestamp"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'categoria': categoria,
            'mensagem': mensagem,
            'dados': dados
        }
        self.resultados.append(log_entry)
        
        # Log para arquivo
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {categoria}: {mensagem}\n")
            if dados:
                f.write(f"  Dados: {json.dumps(dados, indent=2)}\n")
        
        print(f"[{timestamp}] {categoria}: {mensagem}")
    
    def verificar_ambiente_sistema(self):
        """Verifica ambiente do sistema"""
        self.log_debug("AMBIENTE", "Verificando ambiente do sistema")
        
        # Informações do sistema
        info_sistema = {
            'os': os.name,
            'platform': sys.platform,
            'python_version': sys.version,
            'python_executable': sys.executable,
            'current_directory': os.getcwd(),
            'path': sys.path[:5],  # Primeiros 5 itens do PATH
            'environment_vars': dict(os.environ)
        }
        
        self.log_debug("SISTEMA", "Informações do sistema", info_sistema)
        
        # Verificar se estamos no diretório correto
        if '/opt/imediatoseguros-rpa' in os.getcwd():
            self.log_debug("DIRETORIO", "Estamos no diretório correto do RPA")
        else:
            self.log_debug("DIRETORIO", f"Diretório atual: {os.getcwd()}")
    
    def verificar_redis_conexao(self):
        """Verifica conexão com Redis"""
        self.log_debug("REDIS", "Testando conexão com Redis")
        
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            r.ping()
            self.log_debug("REDIS", "Conexão com Redis OK")
            
            # Testar escrita
            test_key = f"debug_test_{int(time.time())}"
            r.set(test_key, "OK")
            value = r.get(test_key)
            r.delete(test_key)
            
            if value == "OK":
                self.log_debug("REDIS", "Escrita/leitura Redis OK")
                return True
            else:
                self.log_debug("REDIS", f"Erro na escrita Redis: esperado 'OK', obtido '{value}'")
                return False
                
        except Exception as e:
            self.log_debug("REDIS", f"Erro na conexão Redis: {str(e)}")
            return False
    
    def verificar_importacoes(self):
        """Verifica se consegue importar módulos necessários"""
        self.log_debug("IMPORT", "Verificando importações")
        
        modulos_teste = [
            'redis',
            'json',
            'time',
            'datetime',
            'os',
            'sys'
        ]
        
        for modulo in modulos_teste:
            try:
                __import__(modulo)
                self.log_debug("IMPORT", f"Módulo {modulo}: OK")
            except ImportError as e:
                self.log_debug("IMPORT", f"Módulo {modulo}: ERRO - {str(e)}")
    
    def verificar_permissoes_arquivos(self):
        """Verifica permissões de arquivos"""
        self.log_debug("PERMISSOES", "Verificando permissões de arquivos")
        
        arquivos_teste = [
            '/opt/imediatoseguros-rpa/teste_api_simples.py',
            '/opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py',
            '/opt/imediatoseguros-rpa/utils/progress_realtime.py',
            '/tmp'
        ]
        
        for arquivo in arquivos_teste:
            if os.path.exists(arquivo):
                stat_info = os.stat(arquivo)
                permissao = oct(stat_info.st_mode)[-3:]
                self.log_debug("PERMISSOES", f"Arquivo {arquivo}: {permissao}")
            else:
                self.log_debug("PERMISSOES", f"Arquivo {arquivo}: NÃO EXISTE")
    
    def verificar_ambiente_virtual(self):
        """Verifica se o ambiente virtual está ativo"""
        self.log_debug("VENV", "Verificando ambiente virtual")
        
        # Verificar se VIRTUAL_ENV está definido
        if 'VIRTUAL_ENV' in os.environ:
            self.log_debug("VENV", f"Ambiente virtual ativo: {os.environ['VIRTUAL_ENV']}")
        else:
            self.log_debug("VENV", "Ambiente virtual NÃO está ativo")
        
        # Verificar se python está no venv
        python_path = sys.executable
        if '/opt/imediatoseguros-rpa/venv' in python_path:
            self.log_debug("VENV", f"Python do venv: {python_path}")
        else:
            self.log_debug("VENV", f"Python do sistema: {python_path}")
    
    def simular_execucao_php(self):
        """Simula a execução exata do PHP"""
        self.log_debug("PHP_SIM", "Simulando execução do PHP")
        
        # Comando exato que o PHP executa
        comando_php = "cd /opt/imediatoseguros-rpa && source venv/bin/activate && python teste_api_simples.py --session debug_php_sim --modo-silencioso"
        
        self.log_debug("PHP_SIM", f"Comando: {comando_php}")
        
        try:
            # Executar comando
            resultado = subprocess.run(
                comando_php,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            self.log_debug("PHP_SIM", f"Return code: {resultado.returncode}")
            self.log_debug("PHP_SIM", f"STDOUT: {resultado.stdout}")
            self.log_debug("PHP_SIM", f"STDERR: {resultado.stderr}")
            
            if resultado.returncode == 0:
                self.log_debug("PHP_SIM", "Execução simulada: SUCESSO")
                return True
            else:
                self.log_debug("PHP_SIM", "Execução simulada: FALHOU")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_debug("PHP_SIM", "Execução simulada: TIMEOUT")
            return False
        except Exception as e:
            self.log_debug("PHP_SIM", f"Execução simulada: ERRO - {str(e)}")
            return False
    
    def verificar_logs_sistema(self):
        """Verifica logs do sistema"""
        self.log_debug("LOGS", "Verificando logs do sistema")
        
        # Verificar logs do nginx
        try:
            resultado = subprocess.run(
                "tail -10 /var/log/nginx/error.log",
                shell=True,
                capture_output=True,
                text=True
            )
            if resultado.stdout:
                self.log_debug("LOGS", "Logs Nginx", resultado.stdout)
        except:
            pass
        
        # Verificar logs do PHP
        try:
            resultado = subprocess.run(
                "tail -10 /var/log/php8.3-fpm.log",
                shell=True,
                capture_output=True,
                text=True
            )
            if resultado.stdout:
                self.log_debug("LOGS", "Logs PHP-FPM", resultado.stdout)
        except:
            pass
    
    def testar_comando_direto(self):
        """Testa o comando direto sem shell"""
        self.log_debug("DIRETO", "Testando comando direto")
        
        try:
            # Mudar para o diretório
            os.chdir('/opt/imediatoseguros-rpa')
            
            # Ativar venv
            activate_script = '/opt/imediatoseguros-rpa/venv/bin/activate'
            if os.path.exists(activate_script):
                # Executar comando direto
                resultado = subprocess.run([
                    '/opt/imediatoseguros-rpa/venv/bin/python',
                    'teste_api_simples.py',
                    '--session',
                    'debug_direto'
                ], capture_output=True, text=True, timeout=30)
                
                self.log_debug("DIRETO", f"Return code: {resultado.returncode}")
                self.log_debug("DIRETO", f"STDOUT: {resultado.stdout}")
                self.log_debug("DIRETO", f"STDERR: {resultado.stderr}")
                
                if resultado.returncode == 0:
                    self.log_debug("DIRETO", "Comando direto: SUCESSO")
                    return True
                else:
                    self.log_debug("DIRETO", "Comando direto: FALHOU")
                    return False
            else:
                self.log_debug("DIRETO", f"Script de ativação não encontrado: {activate_script}")
                return False
                
        except Exception as e:
            self.log_debug("DIRETO", f"Comando direto: ERRO - {str(e)}")
            return False
    
    def verificar_usuario_grupo(self):
        """Verifica usuário e grupo atual"""
        self.log_debug("USUARIO", "Verificando usuário e grupo")
        
        try:
            import pwd
            import grp
            
            uid = os.getuid()
            gid = os.getgid()
            
            user_info = pwd.getpwuid(uid)
            group_info = grp.getgrgid(gid)
            
            self.log_debug("USUARIO", f"UID: {uid}, Usuário: {user_info.pw_name}")
            self.log_debug("USUARIO", f"GID: {gid}, Grupo: {group_info.gr_name}")
            
        except Exception as e:
            self.log_debug("USUARIO", f"Erro ao verificar usuário: {str(e)}")
    
    def executar_debug_completo(self):
        """Executa debug completo"""
        self.log_debug("INICIO", "Iniciando debug completo da API")
        
        # Lista de verificações
        verificacoes = [
            self.verificar_ambiente_sistema,
            self.verificar_usuario_grupo,
            self.verificar_permissoes_arquivos,
            self.verificar_ambiente_virtual,
            self.verificar_importacoes,
            self.verificar_redis_conexao,
            self.simular_execucao_php,
            self.testar_comando_direto,
            self.verificar_logs_sistema
        ]
        
        # Executar verificações
        for verificacao in verificacoes:
            try:
                verificacao()
            except Exception as e:
                self.log_debug("ERRO", f"Erro na verificação {verificacao.__name__}: {str(e)}")
        
        # Gerar relatório
        self.gerar_relatorio()
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        self.log_debug("RELATORIO", "Gerando relatório final")
        
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'log_file': self.log_file,
            'verificacoes': self.resultados
        }
        
        # Salvar relatório JSON
        relatorio_file = f"/tmp/debug_api_relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(relatorio_file, 'w') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        self.log_debug("RELATORIO", f"Relatório salvo em: {relatorio_file}")
        self.log_debug("RELATORIO", f"Log detalhado em: {self.log_file}")
        
        print(f"\n{'='*60}")
        print("📊 DEBUG API COMPLETO FINALIZADO")
        print(f"{'='*60}")
        print(f"📋 Total de verificações: {len(self.resultados)}")
        print(f"📁 Relatório JSON: {relatorio_file}")
        print(f"📝 Log detalhado: {self.log_file}")

if __name__ == "__main__":
    debug = DebugAPICompleto()
    debug.executar_debug_completo()























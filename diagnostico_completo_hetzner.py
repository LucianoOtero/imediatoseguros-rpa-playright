#!/usr/bin/env python3
"""
DIAGNÓSTICO COMPLETO HETZNER - RPA IMEDIATO SEGUROS
Script abrangente para verificar todo o ambiente e funcionalidades

AUTOR: Assistente IA
DATA: 2025-09-28
VERSÃO: 1.0.0
"""

import subprocess
import json
import time
import os
import sys
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

class DiagnosticoHetzner:
    def __init__(self):
        self.resultados = {}
        self.erros = []
        self.avisos = []
        self.sucessos = []
        
    def log_resultado(self, categoria: str, teste: str, status: str, detalhes: str = ""):
        """Registra resultado de um teste"""
        resultado = {
            'teste': teste,
            'status': status,
            'detalhes': detalhes,
            'timestamp': datetime.now().isoformat()
        }
        
        if categoria not in self.resultados:
            self.resultados[categoria] = []
        self.resultados[categoria].append(resultado)
        
        if status == 'ERRO':
            self.erros.append(f"{categoria}: {teste} - {detalhes}")
        elif status == 'AVISO':
            self.avisos.append(f"{categoria}: {teste} - {detalhes}")
        else:
            self.sucessos.append(f"{categoria}: {teste} - {detalhes}")
    
    def executar_comando(self, comando: str, descricao: str = "") -> tuple:
        """Executa comando e retorna (sucesso, output, erro)"""
        try:
            resultado = subprocess.run(
                comando, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return (
                resultado.returncode == 0,
                resultado.stdout.strip(),
                resultado.stderr.strip()
            )
        except subprocess.TimeoutExpired:
            return False, "", f"Timeout após 30s: {comando}"
        except Exception as e:
            return False, "", f"Erro ao executar comando: {str(e)}"
    
    def testar_ambiente_sistema(self):
        """Testa ambiente do sistema"""
        print("🔍 TESTANDO AMBIENTE DO SISTEMA...")
        
        # 1. Verificar sistema operacional
        sucesso, output, erro = self.executar_comando("uname -a")
        if sucesso:
            self.log_resultado("SISTEMA", "Sistema Operacional", "OK", output)
        else:
            self.log_resultado("SISTEMA", "Sistema Operacional", "ERRO", erro)
        
        # 2. Verificar espaço em disco
        sucesso, output, erro = self.executar_comando("df -h /")
        if sucesso:
            self.log_resultado("SISTEMA", "Espaço em Disco", "OK", output)
        else:
            self.log_resultado("SISTEMA", "Espaço em Disco", "ERRO", erro)
        
        # 3. Verificar memória
        sucesso, output, erro = self.executar_comando("free -h")
        if sucesso:
            self.log_resultado("SISTEMA", "Memória", "OK", output)
        else:
            self.log_resultado("SISTEMA", "Memória", "ERRO", erro)
        
        # 4. Verificar processos ativos
        sucesso, output, erro = self.executar_comando("ps aux | grep -E '(nginx|redis|php)' | grep -v grep")
        if sucesso:
            self.log_resultado("SISTEMA", "Processos Ativos", "OK", output)
        else:
            self.log_resultado("SISTEMA", "Processos Ativos", "AVISO", "Nenhum processo encontrado")
    
    def testar_python_ambiente(self):
        """Testa ambiente Python"""
        print("🐍 TESTANDO AMBIENTE PYTHON...")
        
        # 1. Verificar Python
        sucesso, output, erro = self.executar_comando("/opt/imediatoseguros-rpa/venv/bin/python --version")
        if sucesso:
            self.log_resultado("PYTHON", "Versão Python", "OK", output)
        else:
            self.log_resultado("PYTHON", "Versão Python", "ERRO", erro)
        
        # 2. Verificar ambiente virtual
        sucesso, output, erro = self.executar_comando("/opt/imediatoseguros-rpa/venv/bin/python --version")
        if sucesso:
            self.log_resultado("PYTHON", "Ambiente Virtual", "OK", output)
        else:
            self.log_resultado("PYTHON", "Ambiente Virtual", "ERRO", erro)
        
        # 3. Verificar Playwright
        sucesso, output, erro = self.executar_comando("/opt/imediatoseguros-rpa/venv/bin/python -c 'import playwright; print(\"Playwright OK\")'")
        if sucesso:
            self.log_resultado("PYTHON", "Playwright", "OK", output)
        else:
            self.log_resultado("PYTHON", "Playwright", "ERRO", erro)
        
        # 4. Verificar dependências
        sucesso, output, erro = self.executar_comando("/opt/imediatoseguros-rpa/venv/bin/pip list | grep -E '(playwright|redis|requests)'")
        if sucesso:
            self.log_resultado("PYTHON", "Dependências", "OK", output)
        else:
            self.log_resultado("PYTHON", "Dependências", "AVISO", "Algumas dependências podem estar faltando")
    
    def testar_redis(self):
        """Testa Redis"""
        print("🔴 TESTANDO REDIS...")
        
        # 1. Verificar se Redis está rodando
        sucesso, output, erro = self.executar_comando("redis-cli ping")
        if sucesso and "PONG" in output:
            self.log_resultado("REDIS", "Status Redis", "OK", output)
        else:
            self.log_resultado("REDIS", "Status Redis", "ERRO", erro or output)
            return
        
        # 2. Verificar chaves existentes
        sucesso, output, erro = self.executar_comando("redis-cli keys '*'")
        if sucesso:
            chaves = output.split('\n') if output else []
            self.log_resultado("REDIS", "Chaves Existentes", "OK", f"{len(chaves)} chaves encontradas")
            if chaves:
                self.log_resultado("REDIS", "Chaves Existentes", "INFO", f"Chaves: {', '.join(chaves[:10])}")
        else:
            self.log_resultado("REDIS", "Chaves Existentes", "ERRO", erro)
        
        # 3. Testar escrita/leitura
        sucesso, output, erro = self.executar_comando("redis-cli set teste_diagnostico 'OK'")
        if sucesso:
            sucesso2, output2, erro2 = self.executar_comando("redis-cli get teste_diagnostico")
            if sucesso2 and "OK" in output2:
                self.log_resultado("REDIS", "Teste Escrita/Leitura", "OK", "Funcionando corretamente")
                self.executar_comando("redis-cli del teste_diagnostico")  # Limpar
            else:
                self.log_resultado("REDIS", "Teste Escrita/Leitura", "ERRO", erro2 or output2)
        else:
            self.log_resultado("REDIS", "Teste Escrita/Leitura", "ERRO", erro)
    
    def testar_nginx_php(self):
        """Testa Nginx e PHP"""
        print("🌐 TESTANDO NGINX E PHP...")
        
        # 1. Verificar status Nginx
        sucesso, output, erro = self.executar_comando("systemctl status nginx --no-pager")
        if sucesso:
            self.log_resultado("NGINX", "Status Nginx", "OK", "Nginx está rodando")
        else:
            self.log_resultado("NGINX", "Status Nginx", "ERRO", erro)
        
        # 2. Verificar PHP
        sucesso, output, erro = self.executar_comando("php --version")
        if sucesso:
            self.log_resultado("PHP", "Versão PHP", "OK", output.split('\n')[0])
        else:
            self.log_resultado("PHP", "Versão PHP", "ERRO", erro)
        
        # 3. Verificar arquivos PHP no diretório web
        sucesso, output, erro = self.executar_comando("ls -la /var/www/rpaimediatoseguros.com.br/*.php")
        if sucesso:
            self.log_resultado("PHP", "Arquivos PHP", "OK", f"Arquivos encontrados: {output}")
        else:
            self.log_resultado("PHP", "Arquivos PHP", "ERRO", "Arquivos PHP não encontrados")
        
        # 4. Testar endpoint HTTP
        try:
            response = requests.get("http://37.27.92.160/test.php", timeout=10)
            if response.status_code == 200:
                self.log_resultado("HTTP", "Teste Endpoint", "OK", f"Status: {response.status_code}")
            else:
                self.log_resultado("HTTP", "Teste Endpoint", "ERRO", f"Status: {response.status_code}")
        except Exception as e:
            self.log_resultado("HTTP", "Teste Endpoint", "ERRO", str(e))
    
    def testar_arquivos_rpa(self):
        """Testa arquivos do RPA"""
        print("🤖 TESTANDO ARQUIVOS RPA...")
        
        # 1. Verificar diretório RPA
        sucesso, output, erro = self.executar_comando("ls -la /opt/imediatoseguros-rpa/")
        if sucesso:
            self.log_resultado("RPA", "Diretório RPA", "OK", "Diretório existe")
        else:
            self.log_resultado("RPA", "Diretório RPA", "ERRO", erro)
        
        # 2. Verificar arquivo principal
        sucesso, output, erro = self.executar_comando("ls -la /opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py")
        if sucesso:
            self.log_resultado("RPA", "Arquivo Principal", "OK", "Arquivo existe")
        else:
            self.log_resultado("RPA", "Arquivo Principal", "ERRO", "Arquivo não encontrado")
        
        # 3. Verificar parâmetros.json
        sucesso, output, erro = self.executar_comando("ls -la /opt/imediatoseguros-rpa/parametros.json")
        if sucesso:
            self.log_resultado("RPA", "Parâmetros", "OK", "Arquivo existe")
        else:
            self.log_resultado("RPA", "Parâmetros", "ERRO", "Arquivo não encontrado")
        
        # 4. Verificar diretórios temp e logs
        sucesso, output, erro = self.executar_comando("ls -la /opt/imediatoseguros-rpa/temp/ /opt/imediatoseguros-rpa/logs/")
        if sucesso:
            self.log_resultado("RPA", "Diretórios Temp/Logs", "OK", "Diretórios existem")
        else:
            self.log_resultado("RPA", "Diretórios Temp/Logs", "AVISO", "Alguns diretórios podem estar faltando")
        
        # 5. Verificar ProgressTracker
        sucesso, output, erro = self.executar_comando("ls -la /opt/imediatoseguros-rpa/utils/progress_realtime.py")
        if sucesso:
            self.log_resultado("RPA", "ProgressTracker", "OK", "Arquivo existe")
        else:
            self.log_resultado("RPA", "ProgressTracker", "ERRO", "Arquivo não encontrado")
    
    def testar_execucao_rpa(self):
        """Testa execução do RPA"""
        print("🚀 TESTANDO EXECUÇÃO RPA...")
        
        # 1. Teste de help
        sucesso, output, erro = self.executar_comando("cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --help")
        if sucesso:
            self.log_resultado("EXECUCAO", "Teste Help", "OK", "Comando help funcionou")
        else:
            self.log_resultado("EXECUCAO", "Teste Help", "ERRO", erro)
        
        # 2. Teste de versão
        sucesso, output, erro = self.executar_comando("cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --version")
        if sucesso:
            self.log_resultado("EXECUCAO", "Teste Versão", "OK", output)
        else:
            self.log_resultado("EXECUCAO", "Teste Versão", "ERRO", erro)
        
        # 3. Teste de inicialização (sem executar)
        sucesso, output, erro = self.executar_comando("cd /opt/imediatoseguros-rpa && timeout 10 /opt/imediatoseguros-rpa/venv/bin/python teste_api_simples.py --modo-silencioso --session teste_diagnostico")
        if sucesso or "timeout" in erro.lower():
            self.log_resultado("EXECUCAO", "Teste Inicialização", "OK", "RPA iniciou corretamente")
        else:
            self.log_resultado("EXECUCAO", "Teste Inicialização", "ERRO", erro)
    
    def testar_api_endpoints(self):
        """Testa endpoints da API"""
        print("🔗 TESTANDO API ENDPOINTS...")
        
        # 1. Testar executar_rpa.php
        try:
            dados = {
                "session": "teste_diagnostico_api",
                "dados": {"placa": "ABC1234"}
            }
            response = requests.post(
                "http://37.27.92.160/executar_rpa.php",
                json=dados,
                timeout=30
            )
            if response.status_code == 200:
                resultado = response.json()
                if resultado.get('success'):
                    self.log_resultado("API", "executar_rpa.php", "OK", f"PID: {resultado.get('pid')}")
                else:
                    self.log_resultado("API", "executar_rpa.php", "ERRO", "API retornou success=false")
            else:
                self.log_resultado("API", "executar_rpa.php", "ERRO", f"Status: {response.status_code}")
        except Exception as e:
            self.log_resultado("API", "executar_rpa.php", "ERRO", str(e))
        
        # 2. Testar get_progress.php
        try:
            response = requests.get(
                "http://37.27.92.160/get_progress.php?session=teste_diagnostico_api",
                timeout=10
            )
            if response.status_code == 200:
                self.log_resultado("API", "get_progress.php", "OK", f"Status: {response.status_code}")
            else:
                self.log_resultado("API", "get_progress.php", "ERRO", f"Status: {response.status_code}")
        except Exception as e:
            self.log_resultado("API", "get_progress.php", "ERRO", str(e))
    
    def testar_integracao_completa(self):
        """Testa integração completa"""
        print("🔄 TESTANDO INTEGRAÇÃO COMPLETA...")
        
        # 1. Executar RPA via API
        session_id = f"teste_integracao_{int(time.time())}"
        try:
            dados = {
                "session": session_id,
                "dados": {"placa": "ABC1234"}
            }
            response = requests.post(
                "http://37.27.92.160/executar_rpa.php",
                json=dados,
                timeout=30
            )
            if response.status_code == 200:
                resultado = response.json()
                if resultado.get('success'):
                    pid = resultado.get('pid')
                    self.log_resultado("INTEGRACAO", "Execução via API", "OK", f"PID: {pid}")
                    
                    # 2. Aguardar e verificar progresso
                    time.sleep(5)
                    sucesso, output, erro = self.executar_comando(f"redis-cli keys '*{session_id}*'")
                    if sucesso and output:
                        self.log_resultado("INTEGRACAO", "Dados no Redis", "OK", f"Chaves encontradas: {output}")
                    else:
                        self.log_resultado("INTEGRACAO", "Dados no Redis", "AVISO", "Nenhuma chave encontrada no Redis")
                    
                    # 3. Verificar arquivos JSON
                    sucesso, output, erro = self.executar_comando(f"ls -la /opt/imediatoseguros-rpa/temp/ | grep {session_id}")
                    if sucesso and output:
                        self.log_resultado("INTEGRACAO", "Arquivos JSON", "OK", "Arquivos de progresso encontrados")
                    else:
                        self.log_resultado("INTEGRACAO", "Arquivos JSON", "AVISO", "Nenhum arquivo de progresso encontrado")
                    
                    # 4. Verificar logs
                    sucesso, output, erro = self.executar_comando(f"tail -10 /opt/imediatoseguros-rpa/logs/rpa_tosegurado_*.log | grep {session_id}")
                    if sucesso and output:
                        self.log_resultado("INTEGRACAO", "Logs", "OK", "Logs encontrados")
                    else:
                        self.log_resultado("INTEGRACAO", "Logs", "AVISO", "Nenhum log encontrado")
                        
                else:
                    self.log_resultado("INTEGRACAO", "Execução via API", "ERRO", "API retornou success=false")
            else:
                self.log_resultado("INTEGRACAO", "Execução via API", "ERRO", f"Status: {response.status_code}")
        except Exception as e:
            self.log_resultado("INTEGRACAO", "Execução via API", "ERRO", str(e))
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        print("\n" + "="*80)
        print("📊 RELATÓRIO DE DIAGNÓSTICO")
        print("="*80)
        
        # Resumo
        total_testes = sum(len(categoria) for categoria in self.resultados.values())
        total_sucessos = len(self.sucessos)
        total_avisos = len(self.avisos)
        total_erros = len(self.erros)
        
        print(f"\n📈 RESUMO GERAL:")
        print(f"   Total de testes: {total_testes}")
        print(f"   ✅ Sucessos: {total_sucessos}")
        print(f"   ⚠️  Avisos: {total_avisos}")
        print(f"   ❌ Erros: {total_erros}")
        
        # Detalhes por categoria
        for categoria, testes in self.resultados.items():
            print(f"\n🔍 {categoria}:")
            for teste in testes:
                status_icon = "✅" if teste['status'] == 'OK' else "⚠️" if teste['status'] == 'AVISO' else "❌"
                print(f"   {status_icon} {teste['teste']}: {teste['detalhes']}")
        
        # Erros críticos
        if self.erros:
            print(f"\n❌ ERROS CRÍTICOS:")
            for erro in self.erros:
                print(f"   • {erro}")
        
        # Avisos
        if self.avisos:
            print(f"\n⚠️  AVISOS:")
            for aviso in self.avisos:
                print(f"   • {aviso}")
        
        # Salvar relatório
        with open(f"diagnostico_hetzner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: diagnostico_hetzner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    def executar_diagnostico_completo(self):
        """Executa diagnóstico completo"""
        print("🚀 INICIANDO DIAGNÓSTICO COMPLETO HETZNER")
        print("="*80)
        
        self.testar_ambiente_sistema()
        self.testar_python_ambiente()
        self.testar_redis()
        self.testar_nginx_php()
        self.testar_arquivos_rpa()
        self.testar_execucao_rpa()
        self.testar_api_endpoints()
        self.testar_integracao_completa()
        
        self.gerar_relatorio()

if __name__ == "__main__":
    diagnostico = DiagnosticoHetzner()
    diagnostico.executar_diagnostico_completo()

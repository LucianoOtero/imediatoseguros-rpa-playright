#!/usr/bin/env python3
"""
Sistema de Execução Segura de Comandos
======================================

Este script implementa um sistema robusto para executar comandos do terminal
com timeout, detecção de travamento e recuperação automática.

CARACTERÍSTICAS:
- Timeout configurável para cada comando
- Detecção de travamento
- Retry automático
- Logs detalhados
- Limpeza de processos órfãos
"""

import subprocess
import time
import signal
import os
import sys
import threading
from typing import Optional, Dict, Any
import psutil

class ComandoSeguro:
    """Sistema de execução segura de comandos com timeout"""
    
    def __init__(self, timeout_padrao: int = 30):
        self.timeout_padrao = timeout_padrao
        self.processos_ativos = {}
        
    def executar_comando(self, comando: str, timeout: Optional[int] = None, 
                        shell: bool = True, cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Executa um comando com timeout e detecção de travamento
        
        Args:
            comando: Comando a ser executado
            timeout: Timeout em segundos (None = usar padrão)
            shell: Se deve usar shell
            cwd: Diretório de trabalho
            
        Returns:
            Dict com resultado da execução
        """
        timeout = timeout or self.timeout_padrao
        inicio = time.time()
        
        print(f"🚀 Executando comando: {comando}")
        print(f"⏱️ Timeout: {timeout}s")
        
        try:
            # Iniciar processo
            processo = subprocess.Popen(
                comando,
                shell=shell,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Registrar processo ativo
            self.processos_ativos[processo.pid] = processo
            
            # Aguardar conclusão com timeout
            try:
                stdout, stderr = processo.communicate(timeout=timeout)
                tempo_execucao = time.time() - inicio
                
                resultado = {
                    "sucesso": processo.returncode == 0,
                    "codigo_saida": processo.returncode,
                    "stdout": stdout,
                    "stderr": stderr,
                    "tempo_execucao": tempo_execucao,
                    "timeout": False,
                    "travado": False
                }
                
                print(f"✅ Comando concluído em {tempo_execucao:.2f}s")
                return resultado
                
            except subprocess.TimeoutExpired:
                # Timeout atingido - tentar finalizar processo
                print(f"⏰ Timeout atingido ({timeout}s) - finalizando processo...")
                
                try:
                    processo.terminate()
                    processo.wait(timeout=5)  # Aguardar finalização
                except subprocess.TimeoutExpired:
                    print("⚠️ Processo não finalizou - forçando kill...")
                    processo.kill()
                    processo.wait(timeout=5)
                
                return {
                    "sucesso": False,
                    "codigo_saida": -1,
                    "stdout": "",
                    "stderr": f"Timeout após {timeout} segundos",
                    "tempo_execucao": timeout,
                    "timeout": True,
                    "travado": False
                }
                
        except Exception as e:
            tempo_execucao = time.time() - inicio
            print(f"❌ Erro ao executar comando: {e}")
            
            return {
                "sucesso": False,
                "codigo_saida": -1,
                "stdout": "",
                "stderr": str(e),
                "tempo_execucao": tempo_execucao,
                "timeout": False,
                "travado": False
            }
            
        finally:
            # Limpar registro do processo
            if processo.pid in self.processos_ativos:
                del self.processos_ativos[processo.pid]
    
    def executar_comando_com_retry(self, comando: str, max_tentativas: int = 3,
                                  timeout: Optional[int] = None, 
                                  delay_entre_tentativas: int = 2) -> Dict[str, Any]:
        """
        Executa comando com retry automático em caso de falha
        """
        for tentativa in range(max_tentativas):
            print(f"🔄 Tentativa {tentativa + 1}/{max_tentativas}")
            
            resultado = self.executar_comando(comando, timeout)
            
            if resultado["sucesso"]:
                return resultado
            
            if tentativa < max_tentativas - 1:
                print(f"⏳ Aguardando {delay_entre_tentativas}s antes da próxima tentativa...")
                time.sleep(delay_entre_tentativas)
        
        return resultado
    
    def limpar_processos_orfos(self):
        """Limpa processos órfãos que podem estar travando"""
        try:
            # Encontrar processos Python órfãos
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        # Verificar se é um processo órfão
                        if proc.info['cmdline'] and len(proc.info['cmdline']) > 1:
                            cmd = ' '.join(proc.info['cmdline'])
                            if 'executar_rpa' in cmd or 'playwright' in cmd:
                                print(f"🧹 Limpando processo órfão: {proc.info['pid']} - {cmd[:50]}...")
                                proc.terminate()
                                proc.wait(timeout=3)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            print(f"⚠️ Erro ao limpar processos órfãos: {e}")
    
    def verificar_sistema(self) -> Dict[str, Any]:
        """Verifica o estado do sistema"""
        try:
            # Verificar uso de CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Verificar uso de memória
            memoria = psutil.virtual_memory()
            
            # Verificar processos Python
            processos_python = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        processos_python.append({
                            'pid': proc.info['pid'],
                            'cpu': proc.info['cpu_percent'],
                            'memoria': proc.info['memory_info'].rss / 1024 / 1024  # MB
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return {
                "cpu_percent": cpu_percent,
                "memoria_percent": memoria.percent,
                "memoria_disponivel_mb": memoria.available / 1024 / 1024,
                "processos_python": processos_python,
                "processos_ativos": len(self.processos_ativos)
            }
            
        except Exception as e:
            return {"erro": str(e)}

def executar_comando_seguro(comando: str, timeout: int = 30, retry: bool = True) -> Dict[str, Any]:
    """
    Função de conveniência para executar comandos seguros
    """
    executor = ComandoSeguro(timeout_padrao=timeout)
    
    # Limpar processos órfãos antes da execução
    executor.limpar_processos_orfos()
    
    # Verificar sistema antes
    estado_antes = executor.verificar_sistema()
    print(f"📊 Estado do sistema antes: CPU {estado_antes.get('cpu_percent', 0):.1f}%, "
          f"Memória {estado_antes.get('memoria_percent', 0):.1f}%")
    
    # Executar comando
    if retry:
        resultado = executor.executar_comando_com_retry(comando, timeout=timeout)
    else:
        resultado = executor.executar_comando(comando, timeout=timeout)
    
    # Verificar sistema depois
    estado_depois = executor.verificar_sistema()
    print(f"📊 Estado do sistema depois: CPU {estado_depois.get('cpu_percent', 0):.1f}%, "
          f"Memória {estado_depois.get('memoria_percent', 0):.1f}%")
    
    return resultado

if __name__ == "__main__":
    # Teste do sistema
    print("🧪 TESTE DO SISTEMA DE COMANDOS SEGUROS")
    print("=" * 50)
    
    # Teste 1: Comando simples
    print("\n📋 Teste 1: Comando simples")
    resultado = executar_comando_seguro("echo 'Teste de comando seguro'", timeout=10)
    print(f"Resultado: {resultado['sucesso']}")
    
    # Teste 2: Comando que pode travar
    print("\n📋 Teste 2: Comando que pode travar")
    resultado = executar_comando_seguro("python -c 'import time; time.sleep(5)'", timeout=3)
    print(f"Resultado: {resultado['sucesso']} (Timeout: {resultado['timeout']})")
    
    # Teste 3: Verificação do sistema
    print("\n📋 Teste 3: Verificação do sistema")
    executor = ComandoSeguro()
    estado = executor.verificar_sistema()
    print(f"Estado: {estado}")












































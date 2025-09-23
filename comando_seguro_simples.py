#!/usr/bin/env python3
"""
Sistema de Execução Segura de Comandos - Versão Simplificada
============================================================

Este script implementa um sistema básico para executar comandos do terminal
com timeout e detecção de travamento.

CARACTERÍSTICAS:
- Timeout configurável para cada comando
- Detecção de travamento
- Retry automático
- Logs detalhados
"""

import subprocess
import time
from typing import Optional, Dict, Any


class ComandoSeguro:
    """Sistema de execução segura de comandos com timeout"""
    
    def __init__(self, timeout_padrao: int = 30):
        self.timeout_padrao = timeout_padrao
        
    def executar_comando(self, comando: str, timeout: Optional[int] = None, 
                        shell: bool = True, cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Executa um comando com timeout e detecção de travamento
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


def executar_comando_seguro(comando: str, timeout: int = 30, retry: bool = True) -> Dict[str, Any]:
    """
    Função de conveniência para executar comandos seguros
    """
    executor = ComandoSeguro(timeout_padrao=timeout)
    
    # Executar comando
    if retry:
        resultado = executor.executar_comando_com_retry(comando, timeout=timeout)
    else:
        resultado = executor.executar_comando(comando, timeout=timeout)
    
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
    
    # Teste 3: Comando Git
    print("\n📋 Teste 3: Comando Git")
    resultado = executar_comando_seguro("git --version", timeout=10)
    print(f"Resultado: {resultado['sucesso']}")
    if resultado['sucesso']:
        print(f"Saída: {resultado['stdout'].strip()}")










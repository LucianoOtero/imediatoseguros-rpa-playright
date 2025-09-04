#!/usr/bin/env python3
"""
Wrapper para Comandos Seguros
=============================

Este script fornece funções para executar comandos comuns de forma segura,
evitando travamentos e implementando timeout.

USO:
    from comando_wrapper import executar_python, executar_git, executar_sistema
    
    # Executar Python com timeout
    resultado = executar_python("executar_rpa_imediato_playwright.py", timeout=300)
    
    # Executar Git com timeout
    resultado = executar_git("status", timeout=30)
    
    # Executar comando do sistema
    resultado = executar_sistema("dir", timeout=10)
"""

import subprocess
import time
from typing import Optional, Dict, Any


def executar_comando_seguro(comando: str, timeout: int = 30, 
                           retry: bool = True, cwd: Optional[str] = None) -> Dict[str, Any]:
    """
    Executa um comando com timeout e retry automático
    """
    inicio = time.time()
    
    print(f"🚀 Executando: {comando}")
    print(f"⏱️ Timeout: {timeout}s")
    
    max_tentativas = 3 if retry else 1
    
    for tentativa in range(max_tentativas):
        if tentativa > 0:
            print(f"🔄 Tentativa {tentativa + 1}/{max_tentativas}")
            time.sleep(2)  # Pausa entre tentativas
        
        try:
            processo = subprocess.Popen(
                comando,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
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
                
                print(f"✅ Concluído em {tempo_execucao:.2f}s")
                return resultado
                
            except subprocess.TimeoutExpired:
                print(f"⏰ Timeout ({timeout}s) - finalizando processo...")
                
                try:
                    processo.terminate()
                    processo.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print("⚠️ Forçando kill...")
                    processo.kill()
                    processo.wait(timeout=5)
                
                if tentativa == max_tentativas - 1:
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
            print(f"❌ Erro: {e}")
            
            if tentativa == max_tentativas - 1:
                return {
                    "sucesso": False,
                    "codigo_saida": -1,
                    "stdout": "",
                    "stderr": str(e),
                    "tempo_execucao": tempo_execucao,
                    "timeout": False,
                    "travado": False
                }
    
    return {"sucesso": False, "erro": "Todas as tentativas falharam"}


def executar_python(script: str, timeout: int = 300, cwd: Optional[str] = None) -> Dict[str, Any]:
    """
    Executa um script Python com timeout
    """
    comando = f"python {script}"
    return executar_comando_seguro(comando, timeout=timeout, cwd=cwd)


def executar_git(comando: str, timeout: int = 30, cwd: Optional[str] = None) -> Dict[str, Any]:
    """
    Executa um comando Git com timeout
    """
    comando_git = f"git {comando}"
    return executar_comando_seguro(comando_git, timeout=timeout, cwd=cwd)


def executar_sistema(comando: str, timeout: int = 30, cwd: Optional[str] = None) -> Dict[str, Any]:
    """
    Executa um comando do sistema com timeout
    """
    return executar_comando_seguro(comando, timeout=timeout, cwd=cwd)


def limpar_processos_python():
    """
    Limpa processos Python órfãos que podem estar travando
    """
    try:
        resultado = executar_sistema("tasklist /FI \"IMAGENAME eq python.exe\" /FO CSV", timeout=10)
        if resultado["sucesso"]:
            print("🧹 Processos Python ativos:")
            print(resultado["stdout"])
    except Exception as e:
        print(f"⚠️ Erro ao verificar processos: {e}")


if __name__ == "__main__":
    print("🧪 TESTE DO WRAPPER DE COMANDOS")
    print("=" * 40)
    
    # Teste Python
    print("\n📋 Teste Python:")
    resultado = executar_python("-c \"print('Teste Python')\"", timeout=10)
    print(f"Sucesso: {resultado['sucesso']}")
    
    # Teste Git
    print("\n📋 Teste Git:")
    resultado = executar_git("--version", timeout=10)
    print(f"Sucesso: {resultado['sucesso']}")
    if resultado['sucesso']:
        print(f"Versão: {resultado['stdout'].strip()}")
    
    # Teste Sistema
    print("\n📋 Teste Sistema:")
    resultado = executar_sistema("echo Teste sistema", timeout=10)
    print(f"Sucesso: {resultado['sucesso']}")
    
    # Limpar processos
    print("\n📋 Limpeza de processos:")
    limpar_processos_python()





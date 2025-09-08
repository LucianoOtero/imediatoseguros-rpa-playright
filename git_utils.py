#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extensões Git Utilitárias para RPA Tô Segurado
Funções seguras para comandos Git
"""

import subprocess
import os
from typing import Dict, Any, List, Tuple

def git_command_safe(command: str, timeout: int = 30) -> Tuple[bool, str]:
    """
    Executa comando Git de forma segura
    
    Args:
        command: Comando Git a executar
        timeout: Timeout em segundos (padrão: 30)
    
    Returns:
        Tuple[bool, str]: (sucesso, resultado/erro)
    """
    try:
        # Configurar ambiente para evitar pager
        env = os.environ.copy()
        env['GIT_PAGER'] = 'cat'
        env['PAGER'] = 'cat'
        
        # Dividir comando em lista
        cmd_parts = command.split()
        
        result = subprocess.run(
            ['git'] + cmd_parts,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            env=env
        )
        
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, f"Erro Git: {result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return False, f"Timeout após {timeout} segundos"
    except Exception as e:
        return False, f"Erro: {str(e)}"

def git_status_safe() -> Tuple[bool, Dict[str, Any]]:
    """
    Obtém status Git de forma segura
    
    Returns:
        Tuple[bool, Dict]: (sucesso, dados do status)
    """
    try:
        success, output = git_command_safe("status --porcelain")
        if not success:
            return False, {"error": output}
        
        # Parse do output
        status_data = {
            "modified": [],
            "added": [],
            "deleted": [],
            "untracked": [],
            "staged": [],
            "clean": True
        }
        
        lines = output.strip().split('\n') if output.strip() else []
        
        for line in lines:
            if line:
                status_data["clean"] = False
                status = line[:2]
                filename = line[3:]
                
                if status == "M ":
                    status_data["modified"].append(filename)
                elif status == "A ":
                    status_data["added"].append(filename)
                elif status == "D ":
                    status_data["deleted"].append(filename)
                elif status == "??":
                    status_data["untracked"].append(filename)
                elif status == "M " or status == "A " or status == "D ":
                    status_data["staged"].append(filename)
        
        return True, status_data
        
    except Exception as e:
        return False, {"error": str(e)}

def git_branch_info() -> Tuple[bool, Dict[str, Any]]:
    """
    Obtém informações da branch atual
    
    Returns:
        Tuple[bool, Dict]: (sucesso, dados da branch)
    """
    try:
        # Branch atual
        success, current_branch = git_command_safe("branch --show-current")
        if not success:
            return False, {"error": current_branch}
        
        # Lista de branches
        success, branches_output = git_command_safe("branch -a")
        if not success:
            return False, {"error": branches_output}
        
        # Parse das branches
        branches = []
        for line in branches_output.strip().split('\n'):
            if line.strip():
                branch = line.strip()
                if branch.startswith('*'):
                    branch = branch[2:]  # Remove o *
                branches.append(branch)
        
        # Último commit
        success, last_commit = git_command_safe("log -1 --oneline")
        if not success:
            last_commit = "Erro ao obter último commit"
        
        return True, {
            "current_branch": current_branch.strip(),
            "branches": branches,
            "last_commit": last_commit.strip()
        }
        
    except Exception as e:
        return False, {"error": str(e)}

def git_create_branch(branch_name: str) -> Tuple[bool, str]:
    """
    Cria nova branch
    
    Args:
        branch_name: Nome da nova branch
    
    Returns:
        Tuple[bool, str]: (sucesso, mensagem)
    """
    try:
        success, output = git_command_safe(f"checkout -b {branch_name}")
        if success:
            return True, f"Branch '{branch_name}' criada com sucesso"
        else:
            return False, f"Erro ao criar branch: {output}"
            
    except Exception as e:
        return False, f"Erro: {str(e)}"

def git_add_files(files: List[str]) -> Tuple[bool, str]:
    """
    Adiciona arquivos ao staging
    
    Args:
        files: Lista de arquivos para adicionar
    
    Returns:
        Tuple[bool, str]: (sucesso, mensagem)
    """
    try:
        if not files:
            return False, "Nenhum arquivo especificado"
        
        # Construir comando
        cmd = "add " + " ".join(files)
        success, output = git_command_safe(cmd)
        
        if success:
            return True, f"Arquivos adicionados: {', '.join(files)}"
        else:
            return False, f"Erro ao adicionar arquivos: {output}"
            
    except Exception as e:
        return False, f"Erro: {str(e)}"

def git_commit_safe(message: str) -> Tuple[bool, str]:
    """
    Faz commit com mensagem
    
    Args:
        message: Mensagem do commit
    
    Returns:
        Tuple[bool, str]: (sucesso, mensagem)
    """
    try:
        success, output = git_command_safe(f'commit -m "{message}"')
        if success:
            return True, f"Commit realizado: {message}"
        else:
            return False, f"Erro no commit: {output}"
            
    except Exception as e:
        return False, f"Erro: {str(e)}"

def git_push_safe(branch: str = None) -> Tuple[bool, str]:
    """
    Faz push para o repositório remoto
    
    Args:
        branch: Nome da branch (opcional)
    
    Returns:
        Tuple[bool, str]: (sucesso, mensagem)
    """
    try:
        if branch:
            cmd = f"push origin {branch}"
        else:
            cmd = "push"
        
        success, output = git_command_safe(cmd)
        if success:
            return True, f"Push realizado com sucesso"
        else:
            return False, f"Erro no push: {output}"
            
    except Exception as e:
        return False, f"Erro: {str(e)}"

def git_check_integrity() -> Dict[str, Any]:
    """
    Verifica integridade do repositório Git
    
    Returns:
        Dict com informações de integridade
    """
    result = {
        "repository_valid": False,
        "current_branch": None,
        "status_clean": False,
        "last_commit": None,
        "errors": []
    }
    
    try:
        # Verificar se é um repositório Git
        success, _ = git_command_safe("rev-parse --git-dir")
        if not success:
            result["errors"].append("Não é um repositório Git válido")
            return result
        
        result["repository_valid"] = True
        
        # Informações da branch
        success, branch_info = git_branch_info()
        if success:
            result["current_branch"] = branch_info["current_branch"]
            result["last_commit"] = branch_info["last_commit"]
        else:
            result["errors"].append(f"Branch info: {branch_info['error']}")
        
        # Status
        success, status_data = git_status_safe()
        if success:
            result["status_clean"] = status_data["clean"]
        else:
            result["errors"].append(f"Status: {status_data['error']}")
            
    except Exception as e:
        result["errors"].append(f"Erro geral: {str(e)}")
    
    return result

# Funções de conveniência
def quick_git_status() -> str:
    """Status Git rápido"""
    success, output = git_command_safe("status --porcelain")
    return output if success else "ERRO"

def quick_git_branch() -> str:
    """Branch atual rápida"""
    success, output = git_command_safe("branch --show-current")
    return output.strip() if success else "ERRO"

if __name__ == "__main__":
    # Testes das funções
    print("🧪 Testando extensões Git...")
    
    # Teste status
    success, status_data = git_status_safe()
    print(f"Status Test: {'Limpo' if status_data.get('clean') else 'Modificado'}")
    
    # Teste branch
    success, branch_info = git_branch_info()
    print(f"Branch Test: {branch_info.get('current_branch', 'ERRO')}")
    
    # Teste integridade
    integrity = git_check_integrity()
    print(f"Integrity Test: {'OK' if integrity['repository_valid'] else 'ERRO'}")
    
    print("✅ Testes Git concluídos!")

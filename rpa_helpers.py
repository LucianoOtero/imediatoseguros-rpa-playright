#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helpers para RPA Tô Segurado
Funções auxiliares para desenvolvimento e manutenção
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any, List, Tuple
from utils_extensions import check_file_integrity, get_file_hash
from git_utils import git_check_integrity, git_status_safe

def create_backup_directory(prefix: str = "backup") -> str:
    """
    Cria diretório de backup com timestamp
    
    Args:
        prefix: Prefixo do nome do diretório
    
    Returns:
        str: Caminho do diretório criado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{prefix}_{timestamp}"
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        return backup_dir
    except Exception as e:
        raise Exception(f"Erro ao criar diretório de backup: {str(e)}")

def backup_critical_files(files: List[str], backup_dir: str = None) -> Dict[str, Any]:
    """
    Faz backup de arquivos críticos
    
    Args:
        files: Lista de arquivos para backup
        backup_dir: Diretório de backup (opcional)
    
    Returns:
        Dict com informações do backup
    """
    result = {
        "backup_dir": None,
        "files_backed_up": [],
        "files_failed": [],
        "errors": []
    }
    
    try:
        # Criar diretório de backup se não especificado
        if not backup_dir:
            backup_dir = create_backup_directory("rpa_backup")
        
        result["backup_dir"] = backup_dir
        
        # Fazer backup de cada arquivo
        for filepath in files:
            try:
                if os.path.exists(filepath):
                    # Copiar arquivo
                    filename = os.path.basename(filepath)
                    backup_path = os.path.join(backup_dir, filename)
                    shutil.copy2(filepath, backup_path)
                    
                    # Verificar integridade
                    success, hash_original = get_file_hash(filepath)
                    success2, hash_backup = get_file_hash(backup_path)
                    
                    if success and success2 and hash_original == hash_backup:
                        result["files_backed_up"].append({
                            "original": filepath,
                            "backup": backup_path,
                            "hash": hash_original
                        })
                    else:
                        result["files_failed"].append(filepath)
                        result["errors"].append(f"Falha na verificação: {filepath}")
                else:
                    result["files_failed"].append(filepath)
                    result["errors"].append(f"Arquivo não encontrado: {filepath}")
                    
            except Exception as e:
                result["files_failed"].append(filepath)
                result["errors"].append(f"Erro no backup de {filepath}: {str(e)}")
        
        return result
        
    except Exception as e:
        result["errors"].append(f"Erro geral no backup: {str(e)}")
        return result

def verify_rpa_integrity() -> Dict[str, Any]:
    """
    Verifica integridade completa do RPA
    
    Returns:
        Dict com informações de integridade
    """
    result = {
        "rpa_files": {},
        "git_status": {},
        "overall_status": "UNKNOWN",
        "errors": []
    }
    
    # Arquivos críticos do RPA
    critical_files = [
        "executar_rpa_imediato_playwright.py",
        "parametros.json",
        "executar_rpa_telas_1_a_5.py"
    ]
    
    try:
        # Verificar cada arquivo crítico
        for filepath in critical_files:
            integrity = check_file_integrity(filepath)
            result["rpa_files"][filepath] = integrity
            
            if not integrity["exists"]:
                result["errors"].append(f"Arquivo crítico não encontrado: {filepath}")
        
        # Verificar status Git
        git_integrity = git_check_integrity()
        result["git_status"] = git_integrity
        
        if not git_integrity["repository_valid"]:
            result["errors"].append("Repositório Git inválido")
        
        # Determinar status geral
        if not result["errors"]:
            result["overall_status"] = "HEALTHY"
        elif len(result["errors"]) <= 2:
            result["overall_status"] = "WARNING"
        else:
            result["overall_status"] = "CRITICAL"
            
    except Exception as e:
        result["errors"].append(f"Erro na verificação: {str(e)}")
        result["overall_status"] = "ERROR"
    
    return result

def cleanup_temp_files(patterns: List[str] = None) -> Dict[str, Any]:
    """
    Remove arquivos temporários
    
    Args:
        patterns: Lista de padrões de arquivos para remover
    
    Returns:
        Dict com informações da limpeza
    """
    if patterns is None:
        patterns = [
            "dados_planos_seguro_*.json",
            "modal_login_*.png",
            "executar_rpa_imediato_playwright_*.py"
        ]
    
    result = {
        "files_removed": [],
        "files_failed": [],
        "errors": []
    }
    
    try:
        import glob
        
        for pattern in patterns:
            try:
                files = glob.glob(pattern)
                for filepath in files:
                    try:
                        os.remove(filepath)
                        result["files_removed"].append(filepath)
                    except Exception as e:
                        result["files_failed"].append(filepath)
                        result["errors"].append(f"Erro ao remover {filepath}: {str(e)}")
                        
            except Exception as e:
                result["errors"].append(f"Erro no padrão {pattern}: {str(e)}")
        
        return result
        
    except Exception as e:
        result["errors"].append(f"Erro geral na limpeza: {str(e)}")
        return result

def generate_deployment_report() -> Dict[str, Any]:
    """
    Gera relatório completo para deployment
    
    Returns:
        Dict com relatório completo
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "rpa_integrity": verify_rpa_integrity(),
        "git_integrity": git_check_integrity(),
        "cleanup_info": cleanup_temp_files(),
        "recommendations": []
    }
    
    # Gerar recomendações
    if report["rpa_integrity"]["overall_status"] != "HEALTHY":
        report["recommendations"].append("Verificar integridade dos arquivos RPA")
    
    if not report["git_integrity"]["repository_valid"]:
        report["recommendations"].append("Verificar repositório Git")
    
    if report["git_integrity"].get("status_clean", True) == False:
        report["recommendations"].append("Fazer commit das alterações pendentes")
    
    if len(report["cleanup_info"]["files_removed"]) > 0:
        report["recommendations"].append("Arquivos temporários removidos")
    
    return report

def safe_deployment_preparation() -> Dict[str, Any]:
    """
    Prepara deployment de forma segura
    
    Returns:
        Dict com informações da preparação
    """
    result = {
        "backup_created": False,
        "cleanup_done": False,
        "integrity_verified": False,
        "ready_for_deployment": False,
        "errors": []
    }
    
    try:
        # 1. Criar backup
        critical_files = [
            "executar_rpa_imediato_playwright.py",
            "parametros.json"
        ]
        
        backup_result = backup_critical_files(critical_files)
        if backup_result["files_backed_up"]:
            result["backup_created"] = True
        else:
            result["errors"].append("Falha na criação do backup")
        
        # 2. Limpeza
        cleanup_result = cleanup_temp_files()
        if cleanup_result["files_removed"]:
            result["cleanup_done"] = True
        
        # 3. Verificar integridade
        integrity = verify_rpa_integrity()
        if integrity["overall_status"] == "HEALTHY":
            result["integrity_verified"] = True
        else:
            result["errors"].extend(integrity["errors"])
        
        # 4. Determinar se está pronto
        if (result["backup_created"] and 
            result["integrity_verified"] and 
            len(result["errors"]) == 0):
            result["ready_for_deployment"] = True
        
        return result
        
    except Exception as e:
        result["errors"].append(f"Erro na preparação: {str(e)}")
        return result

# Funções de conveniência
def quick_integrity_check() -> str:
    """Verificação rápida de integridade"""
    integrity = verify_rpa_integrity()
    return integrity["overall_status"]

def quick_backup() -> str:
    """Backup rápido dos arquivos críticos"""
    try:
        backup_result = backup_critical_files([
            "executar_rpa_imediato_playwright.py",
            "parametros.json"
        ])
        return f"Backup criado: {backup_result['backup_dir']}"
    except Exception as e:
        return f"Erro no backup: {str(e)}"

if __name__ == "__main__":
    # Testes das funções
    print("🧪 Testando helpers RPA...")
    
    # Teste integridade
    status = quick_integrity_check()
    print(f"Integrity Test: {status}")
    
    # Teste backup
    backup_msg = quick_backup()
    print(f"Backup Test: {backup_msg}")
    
    # Teste preparação
    prep = safe_deployment_preparation()
    print(f"Deployment Prep: {'Pronto' if prep['ready_for_deployment'] else 'Não pronto'}")
    
    print("✅ Testes helpers concluídos!")

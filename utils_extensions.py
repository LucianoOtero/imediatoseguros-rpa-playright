#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extensões Utilitárias para RPA Tô Segurado
Funções seguras para comandos Python e verificações
"""

import subprocess
import json
import os
import time
import hashlib
from typing import Dict, Any, Optional, Tuple

def safe_python_command(command: str, timeout: int = 10) -> Tuple[bool, str]:
    """
    Executa comando Python de forma segura
    
    Args:
        command: Comando Python a executar
        timeout: Timeout em segundos (padrão: 10)
    
    Returns:
        Tuple[bool, str]: (sucesso, resultado/erro)
    """
    try:
        result = subprocess.run(
            ['python', '-c', command],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, f"Erro: {result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return False, f"Timeout após {timeout} segundos"
    except Exception as e:
        return False, f"Erro: {str(e)}"

def verify_json_file(filepath: str) -> Tuple[bool, str]:
    """
    Verifica se arquivo JSON é válido
    
    Args:
        filepath: Caminho do arquivo JSON
    
    Returns:
        Tuple[bool, str]: (válido, mensagem)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, "JSON válido!"
    except FileNotFoundError:
        return False, f"Arquivo não encontrado: {filepath}"
    except json.JSONDecodeError as e:
        return False, f"JSON inválido: {str(e)}"
    except Exception as e:
        return False, f"Erro: {str(e)}"

def verify_python_syntax(filepath: str) -> Tuple[bool, str]:
    """
    Verifica sintaxe Python sem executar
    
    Args:
        filepath: Caminho do arquivo Python
    
    Returns:
        Tuple[bool, str]: (válido, mensagem)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        return True, "Sintaxe Python válida!"
    except FileNotFoundError:
        return False, f"Arquivo não encontrado: {filepath}"
    except SyntaxError as e:
        return False, f"Erro de sintaxe: {str(e)}"
    except Exception as e:
        return False, f"Erro: {str(e)}"

def get_file_hash(filepath: str, algorithm: str = 'sha256') -> Tuple[bool, str]:
    """
    Calcula hash de arquivo
    
    Args:
        filepath: Caminho do arquivo
        algorithm: Algoritmo de hash (sha256, md5, etc.)
    
    Returns:
        Tuple[bool, str]: (sucesso, hash/erro)
    """
    try:
        hash_func = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return True, hash_func.hexdigest().upper()
    except FileNotFoundError:
        return False, f"Arquivo não encontrado: {filepath}"
    except Exception as e:
        return False, f"Erro: {str(e)}"

def compare_files(file1: str, file2: str) -> Tuple[bool, str]:
    """
    Compara dois arquivos usando hash
    
    Args:
        file1: Caminho do primeiro arquivo
        file2: Caminho do segundo arquivo
    
    Returns:
        Tuple[bool, str]: (idênticos, mensagem)
    """
    try:
        success1, hash1 = get_file_hash(file1)
        success2, hash2 = get_file_hash(file2)
        
        if not success1:
            return False, f"Erro no primeiro arquivo: {hash1}"
        if not success2:
            return False, f"Erro no segundo arquivo: {hash2}"
            
        if hash1 == hash2:
            return True, f"Arquivos idênticos (Hash: {hash1[:16]}...)"
        else:
            return False, f"Arquivos diferentes\nHash1: {hash1}\nHash2: {hash2}"
            
    except Exception as e:
        return False, f"Erro na comparação: {str(e)}"

def check_file_integrity(filepath: str) -> Dict[str, Any]:
    """
    Verifica integridade completa de um arquivo
    
    Args:
        filepath: Caminho do arquivo
    
    Returns:
        Dict com informações de integridade
    """
    result = {
        'filepath': filepath,
        'exists': False,
        'size': 0,
        'hash': None,
        'syntax_valid': False,
        'json_valid': False,
        'errors': []
    }
    
    try:
        # Verificar se arquivo existe
        if os.path.exists(filepath):
            result['exists'] = True
            result['size'] = os.path.getsize(filepath)
            
            # Calcular hash
            success, hash_value = get_file_hash(filepath)
            if success:
                result['hash'] = hash_value
            else:
                result['errors'].append(f"Hash: {hash_value}")
            
            # Verificar sintaxe Python (se for .py)
            if filepath.endswith('.py'):
                success, msg = verify_python_syntax(filepath)
                result['syntax_valid'] = success
                if not success:
                    result['errors'].append(f"Sintaxe: {msg}")
            
            # Verificar JSON (se for .json)
            if filepath.endswith('.json'):
                success, msg = verify_json_file(filepath)
                result['json_valid'] = success
                if not success:
                    result['errors'].append(f"JSON: {msg}")
                    
        else:
            result['errors'].append("Arquivo não encontrado")
            
    except Exception as e:
        result['errors'].append(f"Erro geral: {str(e)}")
    
    return result

# Funções de conveniência
def quick_json_check(filepath: str) -> bool:
    """Verificação rápida de JSON"""
    success, _ = verify_json_file(filepath)
    return success

def quick_python_check(filepath: str) -> bool:
    """Verificação rápida de sintaxe Python"""
    success, _ = verify_python_syntax(filepath)
    return success

def quick_hash(filepath: str) -> str:
    """Hash rápido de arquivo"""
    success, hash_value = get_file_hash(filepath)
    return hash_value if success else "ERRO"

if __name__ == "__main__":
    # Testes das funções
    print("🧪 Testando extensões...")
    
    # Teste JSON
    success, msg = verify_json_file("parametros.json")
    print(f"JSON Test: {msg}")
    
    # Teste Python
    success, msg = verify_python_syntax("executar_rpa_imediato_playwright.py")
    print(f"Python Test: {msg}")
    
    # Teste Hash
    success, hash_value = get_file_hash("parametros.json")
    print(f"Hash Test: {hash_value if success else 'ERRO'}")
    
    print("✅ Testes concluídos!")

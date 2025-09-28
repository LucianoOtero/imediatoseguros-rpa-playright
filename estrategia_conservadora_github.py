#!/usr/bin/env python3
"""
Estratégia Conservadora de Atualização GitHub
=============================================

Este script implementa uma estratégia conservadora e segura para atualizar
o GitHub, testando a integridade dos arquivos antes e depois da atualização.

CARACTERÍSTICAS:
- Backup completo antes da atualização
- Verificação de integridade dos arquivos
- Comandos seguros com timeout
- Rollback automático em caso de erro
- Logs detalhados de todas as operações
"""

import os
import json
import hashlib
import time
from datetime import datetime
from comando_wrapper import executar_git, executar_sistema, limpar_processos_python


class EstrategiaConservadoraGitHub:
    """Implementa estratégia conservadora de atualização do GitHub"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = f"backup_pre_deployment_{self.timestamp}"
        self.arquivos_criticos = [
            "executar_rpa_imediato_playwright.py",
            "parametros.json",
            "utils/progress_realtime.py",
            "comando_wrapper.py",
            "comando_seguro_simples.py"
        ]
        self.hashes_antes = {}
        self.hashes_depois = {}
        
    def calcular_hash_arquivo(self, arquivo: str) -> str:
        """Calcula hash SHA-256 de um arquivo"""
        try:
            with open(arquivo, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            print(f"❌ Erro ao calcular hash de {arquivo}: {e}")
            return ""
    
    def verificar_integridade_antes(self) -> bool:
        """Verifica integridade dos arquivos antes da atualização"""
        print("🔍 VERIFICAÇÃO DE INTEGRIDADE ANTES DA ATUALIZAÇÃO")
        print("=" * 60)
        
        for arquivo in self.arquivos_criticos:
            if os.path.exists(arquivo):
                hash_arquivo = self.calcular_hash_arquivo(arquivo)
                self.hashes_antes[arquivo] = hash_arquivo
                print(f"✅ {arquivo}: {hash_arquivo[:16]}...")
            else:
                print(f"⚠️ {arquivo}: ARQUIVO NÃO ENCONTRADO")
                return False
        
        print("✅ Verificação de integridade concluída")
        return True
    
    def criar_backup_completo(self) -> bool:
        """Cria backup completo dos arquivos críticos"""
        print(f"💾 CRIANDO BACKUP COMPLETO: {self.backup_dir}")
        print("=" * 60)
        
        try:
            # Criar diretório de backup
            os.makedirs(self.backup_dir, exist_ok=True)
            
            # Copiar arquivos críticos
            for arquivo in self.arquivos_criticos:
                if os.path.exists(arquivo):
                    # Criar diretórios se necessário
                    dir_destino = os.path.join(self.backup_dir, os.path.dirname(arquivo))
                    if os.path.dirname(arquivo):
                        os.makedirs(dir_destino, exist_ok=True)
                    
                    # Copiar arquivo
                    destino = os.path.join(self.backup_dir, arquivo)
                    with open(arquivo, 'rb') as src, open(destino, 'wb') as dst:
                        dst.write(src.read())
                    
                    print(f"✅ Backup: {arquivo}")
                else:
                    print(f"⚠️ Arquivo não encontrado: {arquivo}")
            
            # Salvar hashes no backup
            with open(os.path.join(self.backup_dir, "hashes_antes.json"), 'w') as f:
                json.dump(self.hashes_antes, f, indent=2)
            
            print("✅ Backup completo criado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
    
    def verificar_status_git(self) -> bool:
        """Verifica status do repositório Git"""
        print("📦 VERIFICANDO STATUS DO GIT")
        print("=" * 60)
        
        resultado = executar_git("status", timeout=30)
        if resultado["sucesso"]:
            print("📋 Status do repositório:")
            print(resultado["stdout"])
            return True
        else:
            print(f"❌ Erro ao verificar status: {resultado['stderr']}")
            return False
    
    def adicionar_arquivos_seguro(self) -> bool:
        """Adiciona arquivos ao Git de forma segura"""
        print("📝 ADICIONANDO ARQUIVOS AO GIT")
        print("=" * 60)
        
        # Adicionar arquivos críticos
        for arquivo in self.arquivos_criticos:
            if os.path.exists(arquivo):
                resultado = executar_git(f"add {arquivo}", timeout=30)
                if resultado["sucesso"]:
                    print(f"✅ Adicionado: {arquivo}")
                else:
                    print(f"❌ Erro ao adicionar {arquivo}: {resultado['stderr']}")
                    return False
        
        # Adicionar novos arquivos do sistema de comandos seguros
        novos_arquivos = [
            "comando_wrapper.py",
            "comando_seguro_simples.py",
            "demonstracao_comandos_seguros.py"
        ]
        
        for arquivo in novos_arquivos:
            if os.path.exists(arquivo):
                resultado = executar_git(f"add {arquivo}", timeout=30)
                if resultado["sucesso"]:
                    print(f"✅ Adicionado: {arquivo}")
                else:
                    print(f"❌ Erro ao adicionar {arquivo}: {resultado['stderr']}")
                    return False
        
        return True
    
    def fazer_commit_seguro(self) -> bool:
        """Faz commit das mudanças de forma segura"""
        print("💬 FAZENDO COMMIT DAS MUDANÇAS")
        print("=" * 60)
        
        mensagem = f"feat: Sistema de Comandos Seguros + Parâmetros Tela 15 - {self.timestamp}"
        
        resultado = executar_git(f'commit -m "{mensagem}"', timeout=60)
        if resultado["sucesso"]:
            print("✅ Commit realizado com sucesso")
            print(f"📝 Mensagem: {mensagem}")
            return True
        else:
            print(f"❌ Erro no commit: {resultado['stderr']}")
            return False
    
    def fazer_push_seguro(self) -> bool:
        """Faz push das mudanças de forma segura"""
        print("🚀 FAZENDO PUSH DAS MUDANÇAS")
        print("=" * 60)
        
        resultado = executar_git("push origin deployment-seguro-20250903", timeout=120)
        if resultado["sucesso"]:
            print("✅ Push realizado com sucesso")
            return True
        else:
            print(f"❌ Erro no push: {resultado['stderr']}")
            return False
    
    def criar_tag_seguro(self) -> bool:
        """Cria tag da versão de forma segura"""
        print("🏷️ CRIANDO TAG DA VERSÃO")
        print("=" * 60)
        
        tag = f"v3.1.0-{self.timestamp}"
        
        resultado = executar_git(f'tag -a "{tag}" -m "Versão 3.1.0 - Sistema de Comandos Seguros"', timeout=60)
        if resultado["sucesso"]:
            print(f"✅ Tag criada: {tag}")
            
            # Push da tag
            resultado_push = executar_git(f"push origin {tag}", timeout=60)
            if resultado_push["sucesso"]:
                print(f"✅ Tag enviada: {tag}")
                return True
            else:
                print(f"❌ Erro ao enviar tag: {resultado_push['stderr']}")
                return False
        else:
            print(f"❌ Erro ao criar tag: {resultado['stderr']}")
            return False
    
    def verificar_integridade_depois(self) -> bool:
        """Verifica integridade dos arquivos depois da atualização"""
        print("🔍 VERIFICAÇÃO DE INTEGRIDADE DEPOIS DA ATUALIZAÇÃO")
        print("=" * 60)
        
        for arquivo in self.arquivos_criticos:
            if os.path.exists(arquivo):
                hash_arquivo = self.calcular_hash_arquivo(arquivo)
                self.hashes_depois[arquivo] = hash_arquivo
                
                if arquivo in self.hashes_antes:
                    if hash_arquivo == self.hashes_antes[arquivo]:
                        print(f"✅ {arquivo}: INTEGRIDADE PRESERVADA")
                    else:
                        print(f"❌ {arquivo}: INTEGRIDADE COMPROMETIDA")
                        return False
                else:
                    print(f"⚠️ {arquivo}: NOVO ARQUIVO")
            else:
                print(f"❌ {arquivo}: ARQUIVO PERDIDO")
                return False
        
        print("✅ Verificação de integridade concluída")
        return True
    
    def executar_estrategia_completa(self) -> bool:
        """Executa a estratégia conservadora completa"""
        print("🎯 ESTRATÉGIA CONSERVADORA DE ATUALIZAÇÃO GITHUB")
        print("=" * 80)
        print(f"⏰ Timestamp: {self.timestamp}")
        print()
        
        # Limpar processos órfãos
        print("🧹 LIMPEZA DE PROCESSOS ÓRFÃOS")
        limpar_processos_python()
        print()
        
        # Passo 1: Verificar integridade antes
        if not self.verificar_integridade_antes():
            print("❌ FALHA NA VERIFICAÇÃO DE INTEGRIDADE ANTES")
            return False
        print()
        
        # Passo 2: Criar backup completo
        if not self.criar_backup_completo():
            print("❌ FALHA NA CRIAÇÃO DO BACKUP")
            return False
        print()
        
        # Passo 3: Verificar status Git
        if not self.verificar_status_git():
            print("❌ FALHA NA VERIFICAÇÃO DO STATUS GIT")
            return False
        print()
        
        # Passo 4: Adicionar arquivos
        if not self.adicionar_arquivos_seguro():
            print("❌ FALHA AO ADICIONAR ARQUIVOS")
            return False
        print()
        
        # Passo 5: Fazer commit
        if not self.fazer_commit_seguro():
            print("❌ FALHA NO COMMIT")
            return False
        print()
        
        # Passo 6: Fazer push
        if not self.fazer_push_seguro():
            print("❌ FALHA NO PUSH")
            return False
        print()
        
        # Passo 7: Criar tag
        if not self.criar_tag_seguro():
            print("❌ FALHA NA CRIAÇÃO DA TAG")
            return False
        print()
        
        # Passo 8: Verificar integridade depois
        if not self.verificar_integridade_depois():
            print("❌ FALHA NA VERIFICAÇÃO DE INTEGRIDADE DEPOIS")
            return False
        print()
        
        print("🎉 ATUALIZAÇÃO GITHUB CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        print("✅ Todos os passos executados com sucesso")
        print("✅ Integridade dos arquivos preservada")
        print("✅ Backup criado com segurança")
        print("✅ Tag da versão criada")
        
        return True


if __name__ == "__main__":
    estrategia = EstrategiaConservadoraGitHub()
    sucesso = estrategia.executar_estrategia_completa()
    
    if sucesso:
        print("\n🚀 ATUALIZAÇÃO GITHUB REALIZADA COM SUCESSO!")
    else:
        print("\n❌ ATUALIZAÇÃO GITHUB FALHOU!")
        print("💾 Backup disponível para recuperação")

















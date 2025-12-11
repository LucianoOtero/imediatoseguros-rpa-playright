#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIMPADOR DE COMENTÁRIOS JAVASCRIPT
==================================

Programa para remover comentários de arquivos JavaScript mantendo a funcionalidade.

Tipos de comentários suportados:
- Comentários de linha única: // comentário
- Comentários de bloco: /* comentário */
- Comentários HTML: <!-- comentário -->

Autor: Assistente IA
Data: 19/10/2025
Versão: 1.0.0
"""

import re
import os
import sys
from pathlib import Path

class LimpadorComentariosJS:
    def __init__(self):
        self.arquivo_original = None
        self.arquivo_backup = None
        self.conteudo_original = ""
        self.conteudo_limpo = ""
        self.estatisticas = {
            'linhas_originais': 0,
            'linhas_finais': 0,
            'comentarios_linha': 0,
            'comentarios_bloco': 0,
            'comentarios_html': 0,
            'caracteres_removidos': 0
        }
    
    def carregar_arquivo(self, caminho_arquivo):
        """Carrega o arquivo JavaScript para processamento."""
        try:
            self.arquivo_original = Path(caminho_arquivo)
            
            if not self.arquivo_original.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
            
            if not self.arquivo_original.suffix.lower() in ['.js', '.html']:
                raise ValueError(f"Arquivo deve ser .js ou .html, encontrado: {self.arquivo_original.suffix}")
            
            # Ler arquivo com encoding UTF-8
            with open(self.arquivo_original, 'r', encoding='utf-8') as f:
                self.conteudo_original = f.read()
            
            self.estatisticas['linhas_originais'] = len(self.conteudo_original.splitlines())
            print(f"✅ Arquivo carregado: {self.arquivo_original.name}")
            print(f"📊 Tamanho original: {len(self.conteudo_original):,} caracteres")
            print(f"📊 Linhas originais: {self.estatisticas['linhas_originais']:,}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar arquivo: {e}")
            return False
    
    def criar_backup(self):
        """Cria backup do arquivo original."""
        try:
            timestamp = self.arquivo_original.stem + "_backup_" + str(int(__import__('time').time()))
            self.arquivo_backup = self.arquivo_original.parent / f"{timestamp}{self.arquivo_original.suffix}"
            
            with open(self.arquivo_backup, 'w', encoding='utf-8') as f:
                f.write(self.conteudo_original)
            
            print(f"💾 Backup criado: {self.arquivo_backup.name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
    
    def limpar_comentarios_html(self, conteudo):
        """Remove comentários HTML: <!-- comentário -->"""
        # Padrão para comentários HTML
        padrao_html = r'<!--.*?-->'
        
        # Encontrar todos os comentários HTML
        comentarios_html = re.findall(padrao_html, conteudo, re.DOTALL)
        self.estatisticas['comentarios_html'] = len(comentarios_html)
        
        # Remover comentários HTML
        conteudo_limpo = re.sub(padrao_html, '', conteudo, flags=re.DOTALL)
        
        if comentarios_html:
            print(f"🗑️ Removidos {len(comentarios_html)} comentários HTML")
        
        return conteudo_limpo
    
    def limpar_comentarios_bloco(self, conteudo):
        """Remove comentários de bloco: /* comentário */"""
        # Padrão para comentários de bloco
        padrao_bloco = r'/\*.*?\*/'
        
        # Encontrar todos os comentários de bloco
        comentarios_bloco = re.findall(padrao_bloco, conteudo, re.DOTALL)
        self.estatisticas['comentarios_bloco'] = len(comentarios_bloco)
        
        # Remover comentários de bloco
        conteudo_limpo = re.sub(padrao_bloco, '', conteudo, flags=re.DOTALL)
        
        if comentarios_bloco:
            print(f"🗑️ Removidos {len(comentarios_bloco)} comentários de bloco")
        
        return conteudo_limpo
    
    def limpar_comentarios_linha(self, conteudo):
        """Remove comentários de linha: // comentário"""
        linhas = conteudo.split('\n')
        linhas_limpas = []
        comentarios_linha = 0
        
        for linha in linhas:
            # Verificar se linha contém comentário de linha
            if '//' in linha:
                # Dividir linha em código e comentário
                partes = linha.split('//', 1)
                codigo = partes[0].rstrip()
                
                # Se há código antes do comentário, manter
                if codigo.strip():
                    linhas_limpas.append(codigo)
                else:
                    # Linha só com comentário, remover completamente
                    comentarios_linha += 1
            else:
                linhas_limpas.append(linha)
        
        self.estatisticas['comentarios_linha'] = comentarios_linha
        
        if comentarios_linha > 0:
            print(f"🗑️ Removidas {comentarios_linha} linhas só com comentários")
        
        return '\n'.join(linhas_limpas)
    
    def limpar_espacos_duplicados(self, conteudo):
        """Remove espaços em branco duplicados e linhas vazias excessivas."""
        # Remover múltiplas linhas vazias consecutivas
        conteudo = re.sub(r'\n\s*\n\s*\n+', '\n\n', conteudo)
        
        # Remover espaços em branco no final das linhas
        linhas = conteudo.split('\n')
        linhas_limpas = [linha.rstrip() for linha in linhas]
        
        return '\n'.join(linhas_limpas)
    
    def processar_arquivo(self):
        """Processa o arquivo removendo comentários."""
        print("\n🔄 Iniciando limpeza de comentários...")
        
        # Aplicar limpezas em sequência
        self.conteudo_limpo = self.conteudo_original
        
        # 1. Remover comentários HTML
        self.conteudo_limpo = self.limpar_comentarios_html(self.conteudo_limpo)
        
        # 2. Remover comentários de bloco
        self.conteudo_limpo = self.limpar_comentarios_bloco(self.conteudo_limpo)
        
        # 3. Remover comentários de linha
        self.conteudo_limpo = self.limpar_comentarios_linha(self.conteudo_limpo)
        
        # 4. Limpar espaços duplicados
        self.conteudo_limpo = self.limpar_espacos_duplicados(self.conteudo_limpo)
        
        # Calcular estatísticas finais
        self.estatisticas['linhas_finais'] = len(self.conteudo_limpo.splitlines())
        self.estatisticas['caracteres_removidos'] = len(self.conteudo_original) - len(self.conteudo_limpo)
        
        print("✅ Limpeza concluída!")
    
    def salvar_arquivo(self, caminho_saida=None):
        """Salva o arquivo limpo."""
        try:
            if caminho_saida:
                arquivo_saida = Path(caminho_saida)
            else:
                # Salvar no mesmo local com sufixo _limpo
                arquivo_saida = self.arquivo_original.parent / f"{self.arquivo_original.stem}_limpo{self.arquivo_original.suffix}"
            
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write(self.conteudo_limpo)
            
            print(f"💾 Arquivo limpo salvo: {arquivo_saida.name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
            return False
    
    def mostrar_estatisticas(self):
        """Exibe estatísticas da limpeza."""
        print("\n📊 ESTATÍSTICAS DA LIMPEZA:")
        print("=" * 50)
        print(f"📄 Arquivo original: {self.arquivo_original.name}")
        print(f"📏 Tamanho original: {len(self.conteudo_original):,} caracteres")
        print(f"📏 Tamanho final: {len(self.conteudo_limpo):,} caracteres")
        print(f"📉 Caracteres removidos: {self.estatisticas['caracteres_removidos']:,}")
        print(f"📊 Redução: {(self.estatisticas['caracteres_removidos'] / len(self.conteudo_original) * 100):.1f}%")
        print(f"📝 Linhas originais: {self.estatisticas['linhas_originais']:,}")
        print(f"📝 Linhas finais: {self.estatisticas['linhas_finais']:,}")
        print(f"🗑️ Comentários HTML: {self.estatisticas['comentarios_html']}")
        print(f"🗑️ Comentários de bloco: {self.estatisticas['comentarios_bloco']}")
        print(f"🗑️ Linhas só com comentários: {self.estatisticas['comentarios_linha']}")
        
        if self.arquivo_backup:
            print(f"💾 Backup: {self.arquivo_backup.name}")
    
    def processar_completo(self, caminho_arquivo, caminho_saida=None):
        """Executa o processo completo de limpeza."""
        print("🧹 LIMPADOR DE COMENTÁRIOS JAVASCRIPT")
        print("=" * 50)
        
        # 1. Carregar arquivo
        if not self.carregar_arquivo(caminho_arquivo):
            return False
        
        # 2. Criar backup
        if not self.criar_backup():
            return False
        
        # 3. Processar arquivo
        self.processar_arquivo()
        
        # 4. Salvar arquivo limpo
        if not self.salvar_arquivo(caminho_saida):
            return False
        
        # 5. Mostrar estatísticas
        self.mostrar_estatisticas()
        
        return True

def main():
    """Função principal do programa."""
    print("🧹 LIMPADOR DE COMENTÁRIOS JAVASCRIPT")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("❌ Uso: python limpar_comentarios_js.py <arquivo.js> [arquivo_saida.js]")
        print("\nExemplos:")
        print("  python limpar_comentarios_js.py webflow_injection_definitivo.js")
        print("  python limpar_comentarios_js.py arquivo.js arquivo_limpo.js")
        return
    
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Criar instância do limpador
    limpador = LimpadorComentariosJS()
    
    # Processar arquivo
    sucesso = limpador.processar_completo(arquivo_entrada, arquivo_saida)
    
    if sucesso:
        print("\n🎉 Processo concluído com sucesso!")
    else:
        print("\n❌ Processo falhou!")
        sys.exit(1)

if __name__ == "__main__":
    main()


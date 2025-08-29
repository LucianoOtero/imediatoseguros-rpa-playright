#!/usr/bin/env python3
"""
Análise Profunda da Tela 7 - RPA Tô Segurado
Analisa detalhadamente o que aconteceu após o clique na Tela 6
"""

import os
import re
from datetime import datetime

def analisar_html(arquivo, descricao):
    """Analisa um arquivo HTML em busca de informações específicas"""
    print(f"\n🔍 **ANÁLISE: {descricao}**")
    print("=" * 60)
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        print(f"📁 Arquivo: {arquivo}")
        print(f"📏 Tamanho: {len(conteudo)} caracteres")
        
        # Buscar elementos de carregamento
        print("\n⏳ **ELEMENTOS DE CARREGAMENTO:**")
        loading_patterns = [
            r'aguarde',
            r'loading',
            r'calculando',
            r'carregando',
            r'processando',
            r'aguardando'
        ]
        
        for pattern in loading_patterns:
            matches = re.findall(pattern, conteudo, re.IGNORECASE)
            if matches:
                print(f"✅ '{pattern}': {len(matches)} ocorrências")
                # Mostrar contexto das primeiras ocorrências
                for i, match in enumerate(matches[:3]):
                    start = conteudo.lower().find(match)
                    if start != -1:
                        context = conteudo[max(0, start-50):start+len(match)+50]
                        print(f"   {i+1}. ...{context}...")
            else:
                print(f"❌ '{pattern}': Não encontrado")
        
        # Buscar possíveis erros
        print("\n⚠️ **POSSÍVEIS ERROS:**")
        error_patterns = [
            r'error',
            r'erro',
            r'exception',
            r'falha',
            r'problema',
            r'failed',
            r'timeout'
        ]
        
        for pattern in error_patterns:
            matches = re.findall(pattern, conteudo, re.IGNORECASE)
            if matches:
                print(f"⚠️ '{pattern}': {len(matches)} ocorrências")
                for i, match in enumerate(matches[:2]):
                    start = conteudo.lower().find(match)
                    if start != -1:
                        context = conteudo[max(0, start-50):start+len(match)+50]
                        print(f"   {i+1}. ...{context}...")
        
        # Buscar elementos esperados da Tela 7
        print("\n🎯 **ELEMENTOS ESPERADOS DA TELA 7:**")
        expected_patterns = [
            r'estimativa',
            r'carrossel',
            r'cobertura',
            r'plano',
            r'franquia',
            r'valor',
            r'seguro',
            r'cotacao'
        ]
        
        for pattern in expected_patterns:
            matches = re.findall(pattern, conteudo, re.IGNORECASE)
            if matches:
                print(f"✅ '{pattern}': {len(matches)} ocorrências")
            else:
                print(f"❌ '{pattern}': Não encontrado")
        
        # Buscar JavaScript ou redirecionamentos
        print("\n�� **JAVASCRIPT E REDIRECIONAMENTOS:**")
        js_patterns = [
            r'window\.location',
            r'redirect',
            r'location\.href',
            r'setTimeout',
            r'setInterval',
            r'fetch',
            r'ajax',
            r'xmlhttprequest'
        ]
        
        for pattern in js_patterns:
            matches = re.findall(pattern, conteudo, re.IGNORECASE)
            if matches:
                print(f"🌐 '{pattern}': {len(matches)} ocorrências")
                for i, match in enumerate(matches[:2]):
                    start = conteudo.lower().find(match)
                    if start != -1:
                        context = conteudo[max(0, start-50):start+len(match)+50]
                        print(f"   {i+1}. ...{context}...")
        
        # Buscar formulários ou botões
        print("\n🔘 **FORMULÁRIOS E BOTÕES:**")
        form_patterns = [
            r'<form',
            r'<button',
            r'<input',
            r'onclick',
            r'onsubmit'
        ]
        
        for pattern in form_patterns:
            matches = re.findall(pattern, conteudo, re.IGNORECASE)
            if matches:
                print(f"🔘 '{pattern}': {len(matches)} ocorrências")
        
        # Análise de estrutura
        print("\n��️ **ESTRUTURA DA PÁGINA:**")
        if '<title>' in conteudo:
            title_match = re.search(r'<title[^>]*>(.*?)</title>', conteudo, re.IGNORECASE)
            if title_match:
                print(f"📄 Título: {title_match.group(1).strip()}")
        
        if '<body' in conteudo:
            body_start = conteudo.find('<body')
            body_end = conteudo.find('</body>')
            if body_start != -1 and body_end != -1:
                body_content = conteudo[body_start:body_end]
                print(f"📄 Conteúdo do body: {len(body_content)} caracteres")
                
                # Verificar se há conteúdo visível
                visible_text = re.sub(r'<[^>]+>', '', body_content)
                visible_text = re.sub(r'\s+', ' ', visible_text).strip()
                print(f"📝 Texto visível: {len(visible_text)} caracteres")
                if len(visible_text) < 100:
                    print(f"⚠️ POUCO TEXTO VISÍVEL: '{visible_text}'")
        
    except Exception as e:
        print(f"❌ **ERRO AO ANALISAR {arquivo}:** {e}")

def main():
    """Função principal"""
    print("�� **ANÁLISE PROFUNDA DA TELA 7**")
    print("=" * 60)
    print(f"⏰ Análise: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Analisar arquivos salvos
    arquivos = [
        ("temp/tela_06_antes_clique.html", "TELA 6 - Antes do clique"),
        ("temp/tela_07_investigacao.html", "TELA 7 - Após clique (estado final)")
    ]
    
    for arquivo, descricao in arquivos:
        analisar_html(arquivo, descricao)
    
    print(f"\n�� **ANÁLISE PROFUNDA CONCLUÍDA!**")
    print(f"📁 Verifique os resultados acima para entender o problema")

if __name__ == "__main__":
    main()

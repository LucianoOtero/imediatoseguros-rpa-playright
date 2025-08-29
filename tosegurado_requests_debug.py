#!/usr/bin/env python3
"""
Debug do ToSegurado usando requests (sem navegador)
"""

import requests
from bs4 import BeautifulSoup
import json

def debug_tosegurado_requests():
    try:
        print("🚀 Iniciando debug com requests...")
        
        # Headers para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(" Navegando para ToSegurado...")
        response = requests.get("https://www.app.tosegurado.com.br/imediatosolucoes", headers=headers)
        
        print(f"�� Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página carregada com sucesso!")
            
            # Salvar HTML para análise
            html_path = "/opt/imediatoseguros-rpa/temp/tosegurado_page.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"💾 HTML salvo em: {html_path}")
            
            # Analisar HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Procurar por elementos relacionados a carro/seguro
            car_elements = soup.find_all(text=lambda text: text and 'carro' in text.lower())
            auto_elements = soup.find_all(text=lambda text: text and 'auto' in text.lower())
            seguro_elements = soup.find_all(text=lambda text: text and 'seguro' in text.lower())
            
            print(f"🔍 Elementos encontrados:")
            print(f"   - Carro: {len(car_elements)} elementos")
            print(f"   - Auto: {len(auto_elements)} elementos")
            print(f"   - Seguro: {len(seguro_elements)} elementos")
            
            # Mostrar alguns exemplos
            if car_elements:
                print(f"📝 Exemplos de elementos 'carro': {car_elements[:3]}")
            
            # Salvar análise em JSON
            analysis = {
                'status_code': response.status_code,
                'url': response.url,
                'elements_found': {
                    'carro': len(car_elements),
                    'auto': len(auto_elements),
                    'seguro': len(seguro_elements)
                },
                'html_file': html_path
            }
            
            json_path = "/opt/imediatoseguros-rpa/temp/analysis.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"📊 Análise salva em: {json_path}")
            
        else:
            print(f"❌ Erro ao carregar página: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    debug_tosegurado_requests()

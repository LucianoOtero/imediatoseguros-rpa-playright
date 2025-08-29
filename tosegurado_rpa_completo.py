#!/usr/bin/env python3
"""
RPA COMPLETO - TÔ SEGURADO - COTAÇÃO DE SEGURO AUTO
Navega por todas as 15 telas sequencialmente
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re

class ToSeguradoRPA:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.base_url = "https://www.app.tosegurado.com.br"
        self.current_url = None
        self.cotacao_data = {}
        
    def log_step(self, step, action, details=""):
        """Registra cada passo do processo"""
        print(f"�� **Tela {step}:** {action}")
        if details:
            print(f"   📝 {details}")
        print()
        
    def save_html(self, step, html_content):
        """Salva o HTML de cada tela para debug"""
        filename = f"/opt/imediatoseguros-rpa/temp/tela_{step:02d}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"   💾 HTML salvo: {filename}")
        
    def wait_for_calculation(self, max_wait=180):
        """Aguarda o cálculo automático (Tela 14)"""
        print(f"   ⏳ Aguardando cálculo automático (máximo {max_wait}s)...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = self.session.get(self.current_url)
                if "Parabéns, chegamos ao resultado final" in response.text:
                    print(f"   ✅ Cálculo concluído em {int(time.time() - start_time)}s!")
                    return response
                time.sleep(2)
            except Exception as e:
                print(f"   ⚠️ Erro ao verificar cálculo: {e}")
                time.sleep(2)
                
        print(f"   ⚠️ Timeout após {max_wait}s")
        return None
        
    def extract_cotacao_data(self, html_content):
        """Extrai dados das cotações (Tela 15)"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Procurar por valores de cotação
        cotacoes = []
        
        # Padrões para encontrar valores
        price_patterns = [
            r'R\$\s*([\d.,]+)',
            r'([\d.,]+)\s*anual',
            r'R\$\s*([\d.,]+)\s*anual'
        ]
        
        # Procurar por elementos de cotação
        cotacao_elements = soup.find_all(text=re.compile(r'Plano|recomendado|anual|R\$'))
        
        for element in cotacao_elements:
            if element.strip():
                for pattern in price_patterns:
                    match = re.search(pattern, element)
                    if match:
                        valor = match.group(1).replace('.', '').replace(',', '.')
                        try:
                            valor_float = float(valor)
                            cotacoes.append({
                                'tipo': 'Preço',
                                'valor': valor_float,
                                'texto': element.strip()
                            })
                        except ValueError:
                            continue
                            
        # Procurar por coberturas
        coberturas = []
        cobertura_keywords = ['Franquia', 'Valor de Mercado', 'Assistência', 'Vidros', 'Carro Reserva', 
                             'Danos Materiais', 'Danos Corporais', 'Danos Morais', 'Morte/Invalidez']
        
        for keyword in cobertura_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
            for element in elements:
                if element.strip():
                    coberturas.append({
                        'tipo': keyword,
                        'texto': element.strip()
                    })
                    
        return {
            'cotacoes': cotacoes,
            'coberturas': coberturas,
            'html_content': html_content
        }
        
    def execute_complete_flow(self):
        """Executa o fluxo completo das 15 telas"""
        try:
            print("🚀 **INICIANDO RPA COMPLETO - TÔ SEGURADO**")
            print("=" * 60)
            
            # TELA 1: Seleção do tipo de seguro
            self.log_step(1, "Navegando para página inicial")
            response = self.session.get(f"{self.base_url}/imediatosolucoes")
            self.current_url = response.url
            self.save_html(1, response.text)
            
            # Verificar se estamos na tela correta
            if "Qual seguro você deseja cotar?" not in response.text:
                print("   ❌ Página inicial não carregou corretamente")
                return False
                
            print("   ✅ Página inicial carregada")
            
            # TELA 2: Formulário de placa (simular clique no botão Carro)
            self.log_step(2, "Simulando clique no botão 'Carro'")
            # Aqui precisamos simular o clique via POST ou JavaScript
            # Por enquanto, vamos tentar acessar diretamente a URL da tela de placa
            
            placa_url = f"{self.base_url}/cotacao/carro"
            response = self.session.get(placa_url)
            self.current_url = response.url
            self.save_html(2, response.text)
            
            if "Qual é a placa do carro?" not in response.text:
                print("   ❌ Tela de placa não carregou")
                return False
                
            print("   ✅ Tela de placa carregada")
            
            # TELA 3-13: Simular preenchimento das outras telas
            # Como não temos acesso direto via requests, vamos documentar o que precisa ser feito
            
            self.log_step(3, "Confirmação do veículo", "Precisamos simular seleção 'Sim'")
            self.log_step(4, "Veículo já segurado", "Precisamos simular seleção 'Não'")
            self.log_step(5, "Carrossel de coberturas", "Precisamos clicar 'Continuar'")
            self.log_step(6, "Questionário do veículo", "Precisamos selecionar 'Flex'")
            self.log_step(7, "Endereço noturno", "Precisamos preencher CEP")
            self.log_step(8, "Uso do veículo", "Precisamos selecionar 'Pessoal'")
            self.log_step(9, "Dados pessoais", "Precisamos preencher todos os campos")
            self.log_step(10, "Condutor principal", "Precisamos selecionar 'Sim'")
            self.log_step(11, "Local trabalho/estudo", "Precisamos selecionar 'Local de trabalho'")
            self.log_step(12, "Garagem e portão", "Precisamos selecionar 'Sim' + 'Eletrônico'")
            self.log_step(13, "Reside com 18-26 anos", "Precisamos selecionar 'Não'")
            
            # TELA 14: Aguardar cálculo
            self.log_step(14, "Aguardando cálculo automático")
            print("   ⚠️ Esta tela requer interação JavaScript que não pode ser simulada via requests")
            
            # TELA 15: Resultado final
            self.log_step(15, "Extraindo dados das cotações")
            print("   ⚠️ Esta tela só aparece após o cálculo automático")
            
            print("\n" + "=" * 60)
            print("📋 **ANÁLISE DO PROBLEMA:**")
            print("   ❌ O fluxo completo NÃO pode ser executado apenas com requests")
            print("   ❌ Precisamos de Selenium ou Playwright para simular cliques e interações")
            print("   ❌ As telas 3-15 requerem interação JavaScript")
            
            print("\n�� **SOLUÇÃO RECOMENDADA:**")
            print("   ✅ Usar Selenium WebDriver para simular navegador real")
            print("   ✅ Simular cliques, preenchimentos e navegação")
            print("   ✅ Aguardar carregamentos e cálculos automáticos")
            
            return False
            
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            return False
            
    def save_final_report(self):
        """Salva relatório final"""
        report = {
            'status': 'ANALISADO',
            'problem': 'Fluxo requer interação JavaScript',
            'solution': 'Usar Selenium WebDriver',
            'total_telas': 15,
            'telas_analisadas': ['1', '2'],
            'telas_requerem_selenium': ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'],
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        report_path = "/opt/imediatoseguros-rpa/temp/relatorio_final.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"📊 Relatório final salvo: {report_path}")

def main():
    """Função principal"""
    rpa = ToSeguradoRPA()
    
    # Executar análise
    success = rpa.execute_complete_flow()
    
    # Salvar relatório
    rpa.save_final_report()
    
    if not success:
        print("\n�� **PRÓXIMO PASSO:**")
        print("   ✅ Instalar Selenium: pip install selenium")
        print("   ✅ Criar RPA com WebDriver para simular navegador real")
        print("   ✅ Implementar fluxo completo das 15 telas")

if __name__ == "__main__":
    main()

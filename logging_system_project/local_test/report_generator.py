#!/usr/bin/env python3
"""
📊 REPORT GENERATOR - SISTEMA DE LOGGING PHP
Gera relatórios HTML e JSON dos resultados dos testes
"""

import json
from datetime import datetime
from pathlib import Path
from jinja2 import Template

class ReportGenerator:
    def __init__(self, test_results):
        """Inicializa gerador de relatórios"""
        self.results = test_results
        self.template_dir = Path(__file__).parent / 'templates'
        self.output_dir = Path(__file__).parent / 'results'
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_html_report(self):
        """Gera relatório HTML"""
        template_content = self.get_html_template()
        template = Template(template_content)
        
        # Preparar dados para o template
        template_data = self.prepare_template_data()
        
        # Renderizar template
        html_content = template.render(**template_data)
        
        # Salvar arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.html"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def prepare_template_data(self):
        """Prepara dados para o template"""
        summary = self.results.get('summary', {})
        
        return {
            'title': 'Relatório de Testes - Sistema de Logging PHP',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': summary.get('total_tests', 0),
            'passed_tests': summary.get('passed_tests', 0),
            'failed_tests': summary.get('failed_tests', 0),
            'warning_tests': summary.get('warning_tests', 0),
            'success_rate': summary.get('success_rate', 0),
            'total_duration': summary.get('total_duration', 0),
            'tests': self.results.get('tests', {}),
            'errors': self.results.get('errors', []),
            'start_time': self.results.get('start_time', datetime.now()),
            'end_time': datetime.now()
        }
    
    def get_html_template(self):
        """Retorna template HTML"""
        return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .timestamp {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .summary {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .summary h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .metric {
            text-align: center;
            padding: 20px;
            border-radius: 8px;
            background: #f8f9fa;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9em;
        }
        
        .status-passed { color: #28a745; }
        .status-failed { color: #dc3545; }
        .status-warning { color: #ffc107; }
        .status-unknown { color: #6c757d; }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }
        
        .test-details {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .test-details h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .test-category {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
        }
        
        .test-category h3 {
            color: #495057;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .test-status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        
        .test-status.passed {
            background-color: #d4edda;
            color: #155724;
        }
        
        .test-status.failed {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .test-status.warning {
            background-color: #fff3cd;
            color: #856404;
        }
        
        .test-message {
            color: #666;
            margin-bottom: 10px;
        }
        
        .test-duration {
            color: #999;
            font-size: 0.9em;
        }
        
        .errors {
            background: #f8d7da;
            color: #721c24;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .errors h3 {
            margin-bottom: 15px;
        }
        
        .errors ul {
            list-style-type: disc;
            margin-left: 20px;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            border-top: 1px solid #e9ecef;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .metrics {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 {{ title }}</h1>
            <div class="timestamp">Gerado em: {{ timestamp }}</div>
        </div>
        
        <div class="summary">
            <h2>📊 Resumo dos Testes</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{{ total_tests }}</div>
                    <div class="metric-label">Total de Testes</div>
                </div>
                <div class="metric">
                    <div class="metric-value status-passed">{{ passed_tests }}</div>
                    <div class="metric-label">✅ Passou</div>
                </div>
                <div class="metric">
                    <div class="metric-value status-failed">{{ failed_tests }}</div>
                    <div class="metric-label">❌ Falhou</div>
                </div>
                <div class="metric">
                    <div class="metric-value status-warning">{{ warning_tests }}</div>
                    <div class="metric-label">⚠️ Avisos</div>
                </div>
                <div class="metric">
                    <div class="metric-value status-passed">{{ "%.1f"|format(success_rate) }}%</div>
                    <div class="metric-label">📈 Taxa de Sucesso</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{{ "%.1f"|format(total_duration) }}s</div>
                    <div class="metric-label">⏱️ Duração Total</div>
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ success_rate }}%"></div>
            </div>
        </div>
        
        <div class="test-details">
            <h2>🔍 Detalhes dos Testes</h2>
            
            {% for test_name, test_data in tests.items() %}
            <div class="test-category">
                <h3>{{ test_name|title }}</h3>
                <div class="test-status {{ test_data.get('status', 'unknown').lower() }}">
                    {{ test_data.get('status', 'UNKNOWN') }}
                </div>
                <div class="test-message">{{ test_data.get('message', 'Sem mensagem') }}</div>
                <div class="test-duration">Duração: {{ "%.2f"|format(test_data.get('duration', 0)) }}s</div>
                
                {% if test_data.get('metrics') %}
                <div style="margin-top: 15px;">
                    <strong>Métricas:</strong>
                    <ul style="margin-top: 10px; margin-left: 20px;">
                        {% for metric_name, metric_value in test_data.metrics.items() %}
                        <li><strong>{{ metric_name }}:</strong> {{ metric_value }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
                
                {% if test_data.get('errors') %}
                <div style="margin-top: 15px;">
                    <strong>Erros:</strong>
                    <ul style="margin-top: 10px; margin-left: 20px;">
                        {% for error in test_data.errors %}
                        <li>{{ error }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        {% if errors %}
        <div class="errors">
            <h3>❌ Erros Encontrados</h3>
            <ul>
                {% for error in errors %}
                <li>{{ error }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <div class="footer">
            <p>Sistema de Logging PHP - Relatório gerado automaticamente</p>
            <p>Início: {{ start_time.strftime('%Y-%m-%d %H:%M:%S') }} | Fim: {{ end_time.strftime('%Y-%m-%d %H:%M:%S') }}</p>
        </div>
    </div>
</body>
</html>
        """
    
    def generate_json_report(self):
        """Gera relatório JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str, ensure_ascii=False)
        
        return filepath
    
    def generate_csv_report(self):
        """Gera relatório CSV"""
        import csv
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.csv"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Cabeçalho
            writer.writerow(['Teste', 'Status', 'Duração', 'Mensagem', 'Métricas'])
            
            # Dados dos testes
            for test_name, test_data in self.results.get('tests', {}).items():
                metrics_str = json.dumps(test_data.get('metrics', {}), ensure_ascii=False) if test_data.get('metrics') else ''
                writer.writerow([
                    test_name,
                    test_data.get('status', 'UNKNOWN'),
                    test_data.get('duration', 0),
                    test_data.get('message', ''),
                    metrics_str
                ])
        
        return filepath

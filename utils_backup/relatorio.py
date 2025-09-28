#!/usr/bin/env python3
"""
Sistema de relatórios
"""

import json
import os
from datetime import datetime

class RelatorioCotacao:
    def __init__(self):
        self.inicio = datetime.now()
        self.telas = {}
        self.erros = []
        self.sucessos = []
        
        # Criar diretório de relatórios
        if not os.path.exists("relatorios"):
            os.makedirs("relatorios")
    
    def registrar_tela(self, numero_tela, etapa, status, detalhes=None):
        """Registra uma etapa da tela"""
        if numero_tela not in self.telas:
            self.telas[numero_tela] = []
        
        registro = {
            "etapa": etapa,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "detalhes": detalhes
        }
        
        self.telas[numero_tela].append(registro)
        
        if status == "sucesso":
            self.sucessos.append(f"Tela {numero_tela} - {etapa}")
        elif status == "erro":
            self.erros.append(f"Tela {numero_tela} - {etapa}: {detalhes}")
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        fim = datetime.now()
        duracao = fim - self.inicio
        
        relatorio = {
            "resumo": {
                "inicio": self.inicio.isoformat(),
                "fim": fim.isoformat(),
                "duracao_segundos": duracao.total_seconds(),
                "duracao_formatada": str(duracao),
                "total_telas": len(self.telas),
                "total_sucessos": len(self.sucessos),
                "total_erros": len(self.erros)
            },
            "telas": self.telas,
            "sucessos": self.sucessos,
            "erros": self.erros
        }
        
        # Salvar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorios/relatorio_{timestamp}.json"
        
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        # Gerar relatório em texto
        nome_texto = f"relatorios/relatorio_{timestamp}.txt"
        with open(nome_texto, "w", encoding="utf-8") as f:
            f.write("RELATÓRIO DE COTAÇÃO DE SEGURO\n")
            f.write("=" * 40 + "\n\n")
            
            f.write(f"Início: {self.inicio.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Fim: {fim.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Duração: {str(duracao)}\n\n")
            
            f.write(f"Total de telas: {len(self.telas)}\n")
            f.write(f"Sucessos: {len(self.sucessos)}\n")
            f.write(f"Erros: {len(self.erros)}\n\n")
            
            f.write("DETALHES POR TELA:\n")
            f.write("-" * 20 + "\n")
            
            for numero_tela, etapas in self.telas.items():
                f.write(f"\nTELA {numero_tela}:\n")
                for etapa in etapas:
                    f.write(f"  {etapa['etapa']}: {etapa['status']}\n")
                    if etapa['detalhes']:
                        f.write(f"    Detalhes: {etapa['detalhes']}\n")
            
            if self.erros:
                f.write("\nERROS ENCONTRADOS:\n")
                f.write("-" * 20 + "\n")
                for erro in self.erros:
                    f.write(f"  {erro}\n")
        
        print(f"📊 Relatório gerado: {nome_arquivo}")
        print(f"�� Relatório em texto: {nome_texto}")
        
        return relatorio
    
    def imprimir_resumo(self):
        """Imprime resumo do relatório"""
        print("\n" + "=" * 60)
        print("�� RESUMO DA EXECUÇÃO")
        print("=" * 60)
        
        fim = datetime.now()
        duracao = fim - self.inicio
        
        print(f"⏱️  Duração total: {str(duracao)}")
        print(f"📱 Total de telas: {len(self.telas)}")
        print(f"✅ Sucessos: {len(self.sucessos)}")
        print(f"❌ Erros: {len(self.erros)}")
        
        if self.erros:
            print(f"\n❌ ERROS ENCONTRADOS:")
            for erro in self.erros:
                print(f"   {erro}")
        
        print("=" * 60)

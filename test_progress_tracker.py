#!/usr/bin/env python3
"""
Testes de validação para o ProgressTracker
Estratégia conservadora - testa cada componente individualmente
"""

import os
import sys
import time
import json
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.progress_database_json import DatabaseProgressTracker
from utils.progress_redis import RedisProgressTracker
from utils.progress_realtime import ProgressTracker, detectar_progress_tracker, verificar_redis_disponivel, obter_info_backend


def test_database_progress_tracker():
    """Testa o DatabaseProgressTracker (JSON)"""
    print("🧪 Testando DatabaseProgressTracker...")
    
    try:
        # Criar tracker
        tracker = DatabaseProgressTracker(
            total_etapas=15,
            usar_arquivo=True,
            session_id="test_json"
        )
        
        # Testar atualização de progresso
        tracker.update_progress(1, "Teste etapa 1")
        progresso = tracker.get_progress()
        
        assert progresso["etapa_atual"] == 1
        assert progresso["percentual"] == (1/15) * 100
        assert progresso["status"] == "executando"
        assert progresso["mensagem"] == "Teste etapa 1"
        assert progresso["session_id"] == "test_json"
        
        # Testar adição de erro
        tracker.add_error("Erro de teste", "teste")
        progresso = tracker.get_progress()
        assert len(progresso["erros"]) == 1
        assert progresso["erros"][0]["erro"] == "Erro de teste"
        
        # Testar finalização
        tracker.finalizar("success", {"teste": "dados"})
        progresso = tracker.get_progress()
        assert progresso["status"] == "success"
        assert progresso["percentual"] == 100.0
        assert progresso["etapa_atual"] == 15
        
        # Verificar se arquivos foram criados
        arquivo_progresso = Path("rpa_data/progress_test_json.json")
        arquivo_resultado = Path("rpa_data/result_test_json.json")
        arquivo_sessao = Path("rpa_data/session_test_json.json")
        
        assert arquivo_progresso.exists()
        assert arquivo_resultado.exists()
        assert arquivo_sessao.exists()
        
        # Testar carregamento de sessão
        tracker_carregado = DatabaseProgressTracker.carregar_sessao("test_json")
        assert tracker_carregado is not None
        assert tracker_carregado.session_id == "test_json"
        assert tracker_carregado.status == "success"
        
        # Limpar arquivos
        tracker.limpar_arquivos()
        
        print("✅ DatabaseProgressTracker: OK")
        return True
        
    except Exception as e:
        print(f"❌ DatabaseProgressTracker: ERRO - {e}")
        return False


def test_redis_progress_tracker():
    """Testa o RedisProgressTracker"""
    print("🧪 Testando RedisProgressTracker...")
    
    try:
        # Verificar se Redis está disponível
        if not verificar_redis_disponivel():
            print("⚠️ Redis não disponível, pulando teste")
            return True
        
        # Criar tracker
        tracker = RedisProgressTracker(
            total_etapas=15,
            usar_arquivo=True,
            session_id="test_redis"
        )
        
        # Testar atualização de progresso
        tracker.update_progress(1, "Teste etapa 1")
        progresso = tracker.get_progress()
        
        assert progresso["etapa_atual"] == 1
        assert progresso["percentual"] == (1/15) * 100
        assert progresso["status"] == "executando"
        assert progresso["mensagem"] == "Teste etapa 1"
        assert progresso["session_id"] == "test_redis"
        assert progresso["backend"] == "redis"
        
        # Testar adição de erro
        tracker.add_error("Erro de teste", "teste")
        progresso = tracker.get_progress()
        assert len(progresso["erros"]) == 1
        
        # Testar finalização
        tracker.finalizar("success", {"teste": "dados"})
        progresso = tracker.get_progress()
        assert progresso["status"] == "success"
        assert progresso["percentual"] == 100.0
        
        # Testar carregamento de sessão
        tracker_carregado = RedisProgressTracker.carregar_sessao("test_redis")
        assert tracker_carregado is not None
        assert tracker_carregado.session_id == "test_redis"
        assert tracker_carregado.status == "success"
        
        # Limpar dados
        tracker.limpar_dados()
        
        print("✅ RedisProgressTracker: OK")
        return True
        
    except Exception as e:
        print(f"❌ RedisProgressTracker: ERRO - {e}")
        return False


def test_progress_tracker_unificado():
    """Testa o ProgressTracker unificado"""
    print("🧪 Testando ProgressTracker unificado...")
    
    try:
        # Testar detecção automática
        tracker_auto = ProgressTracker(
            total_etapas=15,
            usar_arquivo=True,
            session_id="test_auto",
            tipo="auto"
        )
        
        progresso = tracker_auto.get_progress()
        assert progresso["session_id"] == "test_auto"
        assert "backend" in progresso
        
        # Testar tipo JSON
        tracker_json = ProgressTracker(
            total_etapas=15,
            usar_arquivo=True,
            session_id="test_json_unified",
            tipo="json"
        )
        
        if tracker_json.tracker:  # Verificar se tracker foi criado
            tracker_json.update_progress(5, "Teste JSON")
            progresso = tracker_json.get_progress()
            assert progresso["etapa_atual"] == 5
            assert progresso["backend"] == "json"
        
        # Testar tipo none
        tracker_none = ProgressTracker(
            total_etapas=15,
            usar_arquivo=True,
            session_id="test_none",
            tipo="none"
        )
        
        progresso = tracker_none.get_progress()
        assert progresso["backend"] == "none"
        assert progresso["status"] == "iniciando"
        
        # Limpar dados
        if tracker_auto.tracker:
            tracker_auto.limpar_dados()
        if tracker_json.tracker:
            tracker_json.limpar_dados()
        
        print("✅ ProgressTracker unificado: OK")
        return True
        
    except Exception as e:
        print(f"❌ ProgressTracker unificado: ERRO - {e}")
        return False


def test_deteccao_automatica():
    """Testa a detecção automática de backend"""
    print("🧪 Testando detecção automática...")
    
    try:
        # Testar detecção automática
        tracker_class = detectar_progress_tracker('auto')
        assert tracker_class is not None
        
        # Testar tipo específico
        tracker_class_json = detectar_progress_tracker('json')
        assert tracker_class_json == DatabaseProgressTracker
        
        # Testar tipo none
        tracker_class_none = detectar_progress_tracker('none')
        assert tracker_class_none is None
        
        # Testar verificação de Redis
        redis_disponivel = verificar_redis_disponivel()
        assert isinstance(redis_disponivel, bool)
        
        # Testar informações do backend
        info_backend = obter_info_backend()
        assert "redis_disponivel" in info_backend
        assert "backend_recomendado" in info_backend
        assert "configuracao_redis" in info_backend
        
        print("✅ Detecção automática: OK")
        return True
        
    except Exception as e:
        print(f"❌ Detecção automática: ERRO - {e}")
        return False


def test_compatibilidade_v34():
    """Testa compatibilidade com a v3.4.0"""
    print("🧪 Testando compatibilidade com v3.4.0...")
    
    try:
        # Testar se a interface é compatível
        tracker = ProgressTracker(
            total_etapas=15,
            usar_arquivo=True,
            session_id="test_compat"
        )
        
        # Testar métodos da v3.4.0
        tracker.update_progress(0, "Iniciando")
        tracker.update_progress(1, "Etapa 1")
        tracker.update_progress(15, "Concluído")
        
        progresso = tracker.get_progress()
        assert progresso["etapa_atual"] == 15
        assert progresso["percentual"] == 100.0
        
        # Testar finalização
        tracker.finalizar("success", {"dados": "teste"})
        
        # Limpar dados
        tracker.limpar_dados()
        
        print("✅ Compatibilidade v3.4.0: OK")
        return True
        
    except Exception as e:
        print(f"❌ Compatibilidade v3.4.0: ERRO - {e}")
        return False


def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes de validação do ProgressTracker")
    print("=" * 60)
    
    testes = [
        test_database_progress_tracker,
        test_redis_progress_tracker,
        test_progress_tracker_unificado,
        test_deteccao_automatica,
        test_compatibilidade_v34
    ]
    
    resultados = []
    
    for teste in testes:
        try:
            resultado = teste()
            resultados.append(resultado)
        except Exception as e:
            print(f"❌ Erro inesperado no teste {teste.__name__}: {e}")
            resultados.append(False)
        
        print()  # Linha em branco entre testes
    
    # Resumo dos resultados
    print("=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    testes_ok = sum(resultados)
    total_testes = len(resultados)
    
    print(f"✅ Testes aprovados: {testes_ok}/{total_testes}")
    print(f"❌ Testes falharam: {total_testes - testes_ok}/{total_testes}")
    
    if testes_ok == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM!")
        return True
    else:
        print("⚠️ ALGUNS TESTES FALHARAM!")
        return False


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)

# 📋 DOCUMENTO PARA CODIFICADOR - CORREÇÕES UBUNTU/HETZNER

## **📊 INFORMAÇÕES GERAIS**

- **Data**: 27/09/2025
- **Revisão**: Engenheiro de Software
- **Status**: ✅ APROVADO COM CORREÇÕES
- **Ambiente**: Servidor Hetzner com Ubuntu
- **Criticidade**: Baixa (100-150 req/dia, max 2-3 concorrentes)

---

## **🎯 RESUMO EXECUTIVO**

O plano original foi **APROVADO** pelo engenheiro de software, mas requer **4 correções específicas** para o ambiente Ubuntu/Hetzner antes da implementação em produção.

### **✅ Pontos Aprovados**
- Correções críticas identificadas e corrigidas
- Arquitetura híbrida adequada para baixa criticidade
- Modificação mínima do arquivo principal (0.3%)
- Sistema de fallbacks robusto

### **⚠️ Correções Necessárias**
- Ajustar paths para Linux/Ubuntu
- Configurar Redis para produção
- Implementar script de deploy
- Simplificar coleta de métricas para baixo volume

---

## **🔧 CORREÇÃO 1: PATHS PARA UBUNTU/LINUX**

### **Arquivo**: `utils/metrics_collector.py`

#### **❌ Código Atual (Problema)**
```python
# Linha 198 - Path hardcoded para Windows
"disk_percent": psutil.disk_usage('/').percent,
```

#### **✅ Código Corrigido**
```python
import platform
import os

def get_disk_usage():
    """Detecta sistema operacional e retorna uso de disco apropriado"""
    try:
        if platform.system() == "Windows":
            return psutil.disk_usage('C:').percent
        else:  # Linux/Ubuntu
            return psutil.disk_usage('/').percent
    except Exception as e:
        return 0.0

# No método collect_lightweight_metrics():
def collect_lightweight_metrics(self) -> Dict[str, Any]:
    try:
        import psutil
        metrics = {
            "timestamp": time.time(),
            "uptime": time.time() - self.start_time,
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": get_disk_usage(),  # CORREÇÃO: Função adaptativa
            "process_count": len(psutil.pids()),
            "os": platform.system()  # Adicionar info do OS
        }
        with self.lock:
            self.metrics_history.append(metrics)
        return metrics
    except Exception as e:
        return {"error": f"Falha: {e}"}
```

---

## **🔧 CORREÇÃO 2: LOGS PARA UBUNTU**

### **Arquivo**: `utils/structured_logger.py`

#### **❌ Código Atual (Problema)**
```python
# Logs em diretório relativo pode causar problemas de permissão
file_handler = logging.FileHandler('logs/rpa_hybrid.log')
```

#### **✅ Código Corrigido**
```python
import logging
import json
import os
import platform
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    def __init__(self, name: str = "rpa_hybrid"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # CORREÇÃO: Detectar sistema e usar path apropriado
        log_dir = self.get_log_directory()
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"{name}.log")
        file_handler = logging.FileHandler(log_file)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def get_log_directory(self) -> str:
        """Retorna diretório de logs apropriado para o sistema"""
        if platform.system() == "Windows":
            return os.path.expanduser("~/logs")
        else:  # Linux/Ubuntu
            # Tentar /var/log primeiro, fallback para home
            try:
                log_dir = "/var/log/rpa"
                os.makedirs(log_dir, exist_ok=True)
                return log_dir
            except PermissionError:
                return os.path.expanduser("~/logs")
    
    def log_progress(self, session_id: str, etapa: int, mensagem: str, dados: Dict[str, Any] = None):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "etapa": etapa,
            "mensagem": mensagem,
            "dados": dados or {},
            "tipo": "progress",
            "os": platform.system()
        }
        self.logger.info(json.dumps(log_data))
    
    def log_fallback(self, modo_anterior: str, modo_novo: str, motivo: str):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "modo_anterior": modo_anterior,
            "modo_novo": modo_novo,
            "motivo": motivo,
            "tipo": "fallback",
            "os": platform.system()
        }
        self.logger.warning(json.dumps(log_data))
```

---

## **🔧 CORREÇÃO 3: CONFIGURAÇÃO REDIS PARA PRODUÇÃO**

### **Arquivo**: `config/redis_config.json`

#### **❌ Configuração Atual (Problema)**
```json
{
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "socket_timeout": 1,
        "password": null
    }
}
```

#### **✅ Configuração Corrigida**
```json
{
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "socket_timeout": 5,
        "password": "sua_senha_redis_aqui",
        "max_connections": 10,
        "retry_on_timeout": true,
        "decode_responses": true,
        "health_check_interval": 30
    },
    "websocket": {
        "port": 8080,
        "max_connections": 50,
        "timeout": 300
    },
    "monitoring": {
        "cpu_threshold": 80,
        "memory_threshold": 85,
        "collect_interval": 30,
        "cleanup_interval": 3600
    }
}
```

### **Arquivo**: `utils/config_manager.py` (Atualizado)

```python
import json
import os
import platform
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_file: str = "config/redis_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # CORREÇÃO: Ajustar configurações para Ubuntu
                    return self.adjust_for_os(config)
            return self.get_default_config()
        except Exception as e:
            print(f"[ERROR] Config: {e}")
            return self.get_default_config()
    
    def adjust_for_os(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Ajusta configurações baseado no sistema operacional"""
        if platform.system() != "Windows":
            # Ajustes para Linux/Ubuntu
            if "redis" in config:
                config["redis"]["socket_timeout"] = 5  # Timeout maior para Linux
                config["redis"]["max_connections"] = 10  # Limite conservador
        return config
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "redis": {
                "host": "localhost",
                "port": 6379,
                "db": 0,
                "socket_timeout": 5,
                "password": None,
                "max_connections": 10,
                "retry_on_timeout": True
            },
            "websocket": {
                "port": 8080,
                "max_connections": 50,
                "timeout": 300
            },
            "monitoring": {
                "cpu_threshold": 80,
                "memory_threshold": 85,
                "collect_interval": 30,
                "cleanup_interval": 3600
            }
        }
    
    def get_redis_config(self) -> Dict[str, Any]:
        return self.config.get("redis", {})
    
    def get_websocket_config(self) -> Dict[str, Any]:
        return self.config.get("websocket", {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        return self.config.get("monitoring", {})
```

---

## **🔧 CORREÇÃO 4: COLETA DE MÉTRICAS OTIMIZADA**

### **Arquivo**: `utils/integrated_monitoring.py` (Atualizado)

```python
"""
Sistema de monitoramento integrado ao RPA - Otimizado para baixo volume
"""
import psutil
import time
import json
import os
import platform
from typing import Dict, Any, List
from datetime import datetime
from utils.config_manager import ConfigManager
from utils.structured_logger import StructuredLogger
from utils.metrics_collector import MetricsCollector

class IntegratedRPAMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.config = ConfigManager()
        self.logger = StructuredLogger()
        self.metrics_collector = MetricsCollector()
        self.monitoring_config = self.config.get_monitoring_config()
        
        # CORREÇÃO: Coleta menos frequente para baixo volume
        self.collect_interval = self.monitoring_config.get("collect_interval", 30)
        self.last_collection = 0
        
        self.alert_thresholds = {
            "cpu_percent": self.monitoring_config.get("cpu_threshold", 80),
            "memory_percent": self.monitoring_config.get("memory_threshold", 85),
            "websocket_connections": 100,
            "response_time_ms": 1000
        }
        
        # CORREÇÃO: Path adaptativo para Ubuntu
        self.monitoring_file = self.get_monitoring_file_path()
    
    def get_monitoring_file_path(self) -> str:
        """Retorna path apropriado para arquivo de monitoramento"""
        if platform.system() == "Windows":
            return "rpa_data/monitoring.json"
        else:  # Linux/Ubuntu
            return os.path.expanduser("~/rpa_data/monitoring.json")
    
    def should_collect_metrics(self) -> bool:
        """CORREÇÃO: Determina se deve coletar métricas (otimização para baixo volume)"""
        return time.time() - self.last_collection > self.collect_interval
    
    def collect_rpa_metrics(self) -> Dict[str, Any]:
        # CORREÇÃO: Coletar apenas quando necessário
        if not self.should_collect_metrics():
            return {"status": "skipped", "reason": "interval_not_reached"}
        
        self.last_collection = time.time()
        
        # Usar coletor otimizado
        metrics = self.metrics_collector.collect_lightweight_metrics()
        
        # Adicionar métricas específicas do RPA
        metrics.update({
            "rpa_status": self.get_rpa_status(),
            "progress_tracker_status": self.get_progress_tracker_status(),
            "websocket_status": self.get_websocket_status(),
            "redis_status": self.get_redis_status(),
            "os": platform.system(),
            "collect_interval": self.collect_interval
        })
        
        # Verificar alertas
        alerts = self.check_alerts(metrics)
        if alerts:
            metrics["alerts"] = alerts
        
        # Salvar métricas
        self.save_metrics(metrics)
        
        return metrics
    
    def get_rpa_status(self) -> Dict[str, Any]:
        return {
            "active_sessions": self.count_active_sessions(),
            "completed_executions": self.count_completed_executions(),
            "failed_executions": self.count_failed_executions(),
            "average_execution_time": self.get_average_execution_time()
        }
    
    def get_progress_tracker_status(self) -> Dict[str, Any]:
        return {
            "mode": self.get_current_mode(),
            "active_connections": self.count_active_connections(),
            "messages_sent": self.count_messages_sent(),
            "last_update": self.get_last_update_time()
        }
    
    def get_websocket_status(self) -> Dict[str, Any]:
        try:
            # CORREÇÃO: Path adaptativo
            status_file = self.get_status_file_path("websocket_status.json")
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    return json.load(f)
            return {"status": "not_available"}
        except:
            return {"status": "error"}
    
    def get_redis_status(self) -> Dict[str, Any]:
        try:
            import redis
            redis_config = self.config.get_redis_config()
            redis_client = redis.Redis(**redis_config)
            redis_client.ping()
            return {"status": "available", **redis_config}
        except:
            return {"status": "not_available"}
    
    def get_status_file_path(self, filename: str) -> str:
        """Retorna path apropriado para arquivos de status"""
        if platform.system() == "Windows":
            return f"rpa_data/{filename}"
        else:  # Linux/Ubuntu
            return os.path.expanduser(f"~/rpa_data/{filename}")
    
    def count_active_sessions(self) -> int:
        try:
            # CORREÇÃO: Path adaptativo
            data_dir = os.path.expanduser("~/rpa_data") if platform.system() != "Windows" else "rpa_data"
            if os.path.exists(data_dir):
                progress_files = [f for f in os.listdir(data_dir) if f.startswith("progress_")]
                return len(progress_files)
            return 0
        except:
            return 0
    
    def count_completed_executions(self) -> int:
        try:
            data_dir = os.path.expanduser("~/rpa_data") if platform.system() != "Windows" else "rpa_data"
            if os.path.exists(data_dir):
                result_files = [f for f in os.listdir(data_dir) if f.startswith("dados_planos_seguro_")]
                return len(result_files)
            return 0
        except:
            return 0
    
    def count_failed_executions(self) -> int:
        try:
            log_dir = self.logger.get_log_directory()
            if os.path.exists(log_dir):
                log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
                return len(log_files)
            return 0
        except:
            return 0
    
    def get_average_execution_time(self) -> float:
        return self.metrics_collector.get_average_metrics().get("execution_time_avg", 0.0)
    
    def get_current_mode(self) -> str:
        try:
            data_dir = os.path.expanduser("~/rpa_data") if platform.system() != "Windows" else "rpa_data"
            if os.path.exists(data_dir):
                progress_files = [f for f in os.listdir(data_dir) if f.startswith("progress_")]
                if progress_files:
                    latest_file = max(progress_files)
                    file_path = os.path.join(data_dir, latest_file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        return data.get("modo", "unknown")
            return "unknown"
        except:
            return "unknown"
    
    def count_active_connections(self) -> int:
        try:
            status_file = self.get_status_file_path("websocket_status.json")
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    data = json.load(f)
                    return data.get("total_connections", 0)
            return 0
        except:
            return 0
    
    def count_messages_sent(self) -> int:
        try:
            data_dir = os.path.expanduser("~/rpa_data") if platform.system() != "Windows" else "rpa_data"
            if os.path.exists(data_dir):
                progress_files = [f for f in os.listdir(data_dir) if f.startswith("progress_")]
                return len(progress_files)
            return 0
        except:
            return 0
    
    def get_last_update_time(self) -> str:
        try:
            data_dir = os.path.expanduser("~/rpa_data") if platform.system() != "Windows" else "rpa_data"
            if os.path.exists(data_dir):
                progress_files = [f for f in os.listdir(data_dir) if f.startswith("progress_")]
                if progress_files:
                    latest_file = max(progress_files)
                    file_path = os.path.join(data_dir, latest_file)
                    if os.path.exists(file_path):
                        return datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            return "never"
        except:
            return "never"
    
    def check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        alerts = []
        
        system_metrics = metrics.get("system_metrics", {})
        
        if system_metrics.get("cpu_percent", 0) > self.alert_thresholds["cpu_percent"]:
            alerts.append({
                "type": "cpu_high",
                "message": f"CPU usage: {system_metrics['cpu_percent']}%",
                "severity": "warning"
            })
        
        if system_metrics.get("memory_percent", 0) > self.alert_thresholds["memory_percent"]:
            alerts.append({
                "type": "memory_high", 
                "message": f"Memory usage: {system_metrics['memory_percent']}%",
                "severity": "critical"
            })
        
        return alerts
    
    def save_metrics(self, metrics: Dict[str, Any]):
        try:
            os.makedirs(os.path.dirname(self.monitoring_file), exist_ok=True)
            with open(self.monitoring_file, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.log_fallback("save_metrics", "error", str(e))
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "uptime_seconds": time.time() - self.start_time,
            "metrics_collected": len(self.metrics_collector.metrics_history),
            "monitoring_file": self.monitoring_file,
            "alert_thresholds": self.alert_thresholds,
            "collect_interval": self.collect_interval,
            "os": platform.system()
        }
```

---

## **🔧 CORREÇÃO 5: SCRIPT DE DEPLOY PARA UBUNTU**

### **Arquivo**: `deploy_ubuntu.sh`

```bash
#!/bin/bash
# Script de deploy para Ubuntu/Hetzner
# Autor: Codificador RPA
# Data: 27/09/2025

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy do RPA Hybrid para Ubuntu..."

# 1. Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update
sudo apt upgrade -y

# 2. Instalar dependências do sistema
echo "🔧 Instalando dependências do sistema..."
sudo apt install -y python3-pip python3-venv redis-server nginx

# 3. Configurar Redis
echo "🔴 Configurando Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verificar se Redis está rodando
if systemctl is-active --quiet redis-server; then
    echo "✅ Redis está rodando"
else
    echo "❌ Erro: Redis não está rodando"
    exit 1
fi

# 4. Criar ambiente virtual Python
echo "🐍 Criando ambiente virtual Python..."
python3 -m venv ~/rpa_env
source ~/rpa_env/bin/activate

# 5. Instalar dependências Python
echo "📚 Instalando dependências Python..."
pip install redis websockets psutil playwright

# 6. Instalar navegadores Playwright
echo "🌐 Instalando navegadores Playwright..."
playwright install

# 7. Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p ~/logs ~/rpa_data ~/config
mkdir -p /var/log/rpa

# 8. Configurar permissões
echo "🔐 Configurando permissões..."
chmod 755 ~/logs ~/rpa_data ~/config
sudo chown -R $USER:$USER /var/log/rpa
chmod 755 /var/log/rpa

# 9. Criar arquivo de configuração
echo "⚙️ Criando arquivo de configuração..."
cat > ~/config/redis_config.json << 'EOF'
{
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "socket_timeout": 5,
        "password": null,
        "max_connections": 10,
        "retry_on_timeout": true,
        "decode_responses": true,
        "health_check_interval": 30
    },
    "websocket": {
        "port": 8080,
        "max_connections": 50,
        "timeout": 300
    },
    "monitoring": {
        "cpu_threshold": 80,
        "memory_threshold": 85,
        "collect_interval": 30,
        "cleanup_interval": 3600
    }
}
EOF

# 10. Criar script de inicialização
echo "🚀 Criando script de inicialização..."
cat > ~/start_rpa.sh << 'EOF'
#!/bin/bash
source ~/rpa_env/bin/activate
cd ~/imediatoseguros-rpa-playwright
python3 executar_rpa_imediato_playwright.py "$@"
EOF

chmod +x ~/start_rpa.sh

# 11. Criar script de limpeza automática
echo "🧹 Criando script de limpeza automática..."
cat > ~/cleanup_rpa.sh << 'EOF'
#!/bin/bash
# Limpar arquivos antigos
find ~/rpa_data -name "progress_*.json" -mtime +1 -delete
find ~/rpa_data -name "dados_planos_seguro_*.json" -mtime +7 -delete
find ~/logs -name "*.log" -mtime +30 -delete

# Limpar logs do sistema
find /var/log/rpa -name "*.log" -mtime +30 -delete

echo "Limpeza automática concluída: $(date)"
EOF

chmod +x ~/cleanup_rpa.sh

# 12. Configurar cron para limpeza automática
echo "⏰ Configurando limpeza automática..."
(crontab -l 2>/dev/null; echo "0 2 * * * ~/cleanup_rpa.sh") | crontab -

# 13. Testar instalação
echo "🧪 Testando instalação..."
source ~/rpa_env/bin/activate
python3 -c "
import redis
import websockets
import psutil
print('✅ Todas as dependências estão funcionando')
"

echo "🎉 Deploy concluído com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Copiar arquivos do projeto para ~/imediatoseguros-rpa-playwright"
echo "2. Executar: ~/start_rpa.sh"
echo "3. Verificar logs em: ~/logs/rpa_hybrid.log"
echo "4. Monitorar Redis: redis-cli ping"
echo ""
echo "🔧 Comandos úteis:"
echo "- Iniciar RPA: ~/start_rpa.sh"
echo "- Ver logs: tail -f ~/logs/rpa_hybrid.log"
echo "- Status Redis: redis-cli ping"
echo "- Limpeza manual: ~/cleanup_rpa.sh"
```

---

## **🔧 CORREÇÃO 6: MODIFICAÇÃO NO ARQUIVO PRINCIPAL**

### **Arquivo**: `executar_rpa_imediato_playwright.py` (Atualizado)

```python
# SISTEMA HÍBRIDO DE PROGRESSTRACKER - CORRIGIDO PARA UBUNTU
# ========================================
if PROGRESS_TRACKER_AVAILABLE:
    session_id = str(uuid.uuid4())
    
    try:
        # Tentar inicializar sistema híbrido corrigido
        from utils.hybrid_progress_tracker import HybridProgressTracker
        progress_tracker = HybridProgressTracker(session_id=session_id)
        
        # Inicializar monitoramento integrado corrigido
        from utils.integrated_monitoring import IntegratedRPAMonitor
        monitor = IntegratedRPAMonitor()
        
        exibir_mensagem(f"[OK] ProgressTracker híbrido ativado - Modo: {progress_tracker.mode}")
        exibir_mensagem(f"[OK] Monitoramento integrado ativado")
        
        # CORREÇÃO: Coletar métricas apenas em etapas críticas (otimização para baixo volume)
        initial_metrics = monitor.collect_rpa_metrics()
        exibir_mensagem(f"[METRICS] Métricas iniciais coletadas")
        
    except Exception as e:
        exibir_mensagem(f"[FALLBACK] Sistema híbrido falhou: {e}")
        exibir_mensagem("[FALLBACK] Usando ProgressTracker básico")
        
        # Fallback para sistema básico
        progress_tracker = ProgressTracker(session_id=session_id)
        monitor = None
else:
    progress_tracker = None
    monitor = None

# INTEGRAÇÃO COM SISTEMA DE MONITORAMENTO OTIMIZADO
# ========================================
if monitor:
    # CORREÇÃO: Coletar métricas apenas em etapas críticas
    def log_progress_metrics(etapa, mensagem):
        if monitor and etapa in [1, 5, 15]:  # Apenas etapas importantes
            metrics = monitor.collect_rpa_metrics()
            exibir_mensagem(f"[METRICS] Etapa {etapa}: Métricas coletadas")
    
    # Integrar com atualizações de progresso
    original_update_progress = progress_tracker.update_progress
    def enhanced_update_progress(etapa, mensagem, dados_extra=None):
        original_update_progress(etapa, mensagem, dados_extra)
        log_progress_metrics(etapa, mensagem)
    
    progress_tracker.update_progress = enhanced_update_progress
```

---

## **📋 CHECKLIST DE IMPLEMENTAÇÃO**

### **✅ Correções Críticas Originais**
- [x] Referência `websocket` corrigida em `process_message()`
- [x] Asyncio thread-safe implementado
- [x] Coleta de métricas não bloqueante
- [x] Configuração centralizada funcionando

### **✅ Correções para Ubuntu/Hetzner**
- [ ] Implementar `get_disk_usage()` adaptativo em `metrics_collector.py`
- [ ] Implementar `get_log_directory()` em `structured_logger.py`
- [ ] Atualizar `redis_config.json` com configurações de produção
- [ ] Implementar `adjust_for_os()` em `config_manager.py`
- [ ] Implementar `should_collect_metrics()` em `integrated_monitoring.py`
- [ ] Implementar paths adaptativos em todos os módulos
- [ ] Criar script `deploy_ubuntu.sh`
- [ ] Atualizar modificação no arquivo principal

### **✅ Validação Final**
- [ ] Teste em ambiente Ubuntu
- [ ] Validação de permissões de diretórios
- [ ] Teste de conectividade Redis
- [ ] Validação de logs estruturados
- [ ] Teste de coleta de métricas otimizada
- [ ] Validação de limpeza automática

---

## **🚀 COMANDOS DE DEPLOY**

### **1. Preparar Ambiente**
```bash
# Tornar script executável
chmod +x deploy_ubuntu.sh

# Executar deploy
./deploy_ubuntu.sh
```

### **2. Testar Instalação**
```bash
# Ativar ambiente virtual
source ~/rpa_env/bin/activate

# Testar dependências
python3 -c "import redis, websockets, psutil; print('OK')"

# Testar Redis
redis-cli ping
```

### **3. Executar RPA**
```bash
# Usar script de inicialização
~/start_rpa.sh

# Ou executar diretamente
source ~/rpa_env/bin/activate
cd ~/imediatoseguros-rpa-playwright
python3 executar_rpa_imediato_playwright.py
```

---

## **📊 RESULTADO ESPERADO**

### **✅ Funcionalidades Implementadas**
1. **Sistema Híbrido**: Detecção automática + fallbacks robustos
2. **WebSocket Thread-Safe**: Comunicação segura entre threads
3. **Monitoramento Otimizado**: Métricas não bloqueantes + coleta inteligente
4. **Configuração Adaptativa**: Ajustes automáticos para Ubuntu/Linux
5. **Logging Estruturado**: Logs em JSON com paths adaptativos
6. **Deploy Automatizado**: Script completo para Ubuntu/Hetzner
7. **Limpeza Automática**: Manutenção automática de arquivos antigos

### **📈 Benefícios para Ubuntu/Hetzner**
- **Compatibilidade**: Funciona nativamente no Ubuntu
- **Performance**: Otimizado para baixo volume (100-150 req/dia)
- **Confiabilidade**: Fallbacks robustos para ambiente de produção
- **Manutenibilidade**: Scripts automatizados para deploy e manutenção
- **Escalabilidade**: Configurações flexíveis para crescimento futuro

---

**Documento elaborado por**: Engenheiro de Software  
**Data**: 27 de Setembro de 2025  
**Status**: ✅ **CORREÇÕES ESPECÍFICAS PARA UBUNTU/HETZNER**  
**Recomendação**: Implementar todas as correções antes do deploy em produção



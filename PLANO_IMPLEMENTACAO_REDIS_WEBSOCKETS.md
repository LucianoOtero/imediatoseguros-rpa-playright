# 📋 Plano de Implementação - Redis/WebSockets para RPA

## **🎯 Resumo Executivo**

Este documento apresenta um plano detalhado para implementar comunicação real-time usando Redis e WebSockets no sistema RPA. O sistema atual possui **75% da infraestrutura necessária** implementada, necessitando apenas da implementação dos componentes de comunicação real-time.

---

## **📊 Status Atual do Sistema**

### **✅ Componentes Implementados (75%)**
- **ProgressTracker**: Sistema completo com suporte a Redis e JSON
- **Comunicação Bidirecional**: Wrapper de integração implementado
- **Timeout Inteligente**: Sistema de timeout configurável por tela
- **Logger Avançado**: Sistema de logging estruturado
- **Fallback Systems**: Sistemas de fallback robustos

### **❌ Componentes Pendentes (25%)**
- **WebSocket Server**: Servidor WebSocket para comunicação real-time
- **Redis Pub/Sub**: Sistema de publicação/assinatura para broadcasting
- **WebSocket Client**: Cliente WebSocket para frontend
- **Real-time Integration**: Integração completa entre componentes

---

## **🏗️ Arquitetura Atual vs. Arquitetura Alvo**

### **Arquitetura Atual**
```
RPA Script → ProgressTracker → Redis Storage → PHP Polling → Frontend
```

### **Arquitetura Alvo**
```
RPA Script → ProgressTracker → Redis Pub/Sub → WebSocket Server → WebSocket Client → Frontend
```

---

## **📋 Plano de Implementação**

### **Fase 1: WebSocket Server (Semana 1)**

#### **Objetivo**
Implementar servidor WebSocket para comunicação real-time entre RPA e frontend.

#### **Tarefas**

**1.1 Criar WebSocket Server**
```python
# Arquivo: utils/websocket_server.py
import asyncio
import websockets
import json
import redis
from typing import Set, Dict, Any

class RPAWebSocketServer:
    def __init__(self, redis_client, host='localhost', port=8080):
        self.redis_client = redis_client
        self.host = host
        self.port = port
        self.connections: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}
        self.pubsub = redis_client.pubsub()
    
    async def start_server(self):
        """Inicia o servidor WebSocket"""
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Run forever
    
    async def handle_client(self, websocket, path):
        """Manipula conexões de clientes WebSocket"""
        session_id = self.extract_session_id(path)
        if session_id not in self.connections:
            self.connections[session_id] = set()
        
        self.connections[session_id].add(websocket)
        
        try:
            async for message in websocket:
                await self.process_message(session_id, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connections[session_id].discard(websocket)
    
    async def broadcast_to_session(self, session_id: str, data: Dict[str, Any]):
        """Transmite dados para todos os clientes de uma sessão"""
        if session_id in self.connections:
            message = json.dumps(data)
            await asyncio.gather(
                *[ws.send(message) for ws in self.connections[session_id]],
                return_exceptions=True
            )
```

**1.2 Integrar com Redis Pub/Sub**
```python
# Arquivo: utils/redis_pubsub.py
import redis
import json
import asyncio
from typing import Dict, Any, Callable

class RedisPubSubManager:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.pubsub = redis_client.pubsub()
        self.subscribers: Dict[str, Callable] = {}
    
    def subscribe_to_progress(self, session_id: str, callback: Callable):
        """Inscreve-se em atualizações de progresso de uma sessão"""
        channel = f"rpa_progress:{session_id}"
        self.pubsub.subscribe(channel)
        self.subscribers[channel] = callback
    
    def publish_progress(self, session_id: str, data: Dict[str, Any]):
        """Publica atualização de progresso"""
        channel = f"rpa_progress:{session_id}"
        self.redis_client.publish(channel, json.dumps(data))
    
    async def listen_for_messages(self):
        """Escuta mensagens do Redis Pub/Sub"""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel'].decode('utf-8')
                data = json.loads(message['data'])
                if channel in self.subscribers:
                    await self.subscribers[channel](data)
```

**1.3 Testes Básicos**
```python
# Arquivo: tests/test_websocket_server.py
import pytest
import asyncio
import websockets
import json

@pytest.mark.asyncio
async def test_websocket_connection():
    """Teste de conexão WebSocket básica"""
    uri = "ws://localhost:8080/rpa/test-session"
    async with websockets.connect(uri) as websocket:
        # Teste de conexão
        assert websocket.open
        
        # Teste de recebimento de mensagem
        test_data = {"etapa": 1, "mensagem": "Teste"}
        await websocket.send(json.dumps(test_data))
        response = await websocket.recv()
        assert json.loads(response) == test_data
```

#### **Entregáveis**
- [ ] WebSocket Server implementado
- [ ] Integração com Redis Pub/Sub
- [ ] Testes básicos funcionando
- [ ] Documentação da API

---

### **Fase 2: Integração ProgressTracker (Semana 2)**

#### **Objetivo**
Integrar ProgressTracker existente com Redis Pub/Sub para comunicação real-time.

#### **Tarefas**

**2.1 Modificar ProgressTracker para Redis Pub/Sub**
```python
# Arquivo: utils/progress_redis.py (modificação)
class RedisProgressTracker:
    def __init__(self, session_id: str, redis_client=None):
        self.session_id = session_id
        self.redis_client = redis_client
        self.pubsub_manager = RedisPubSubManager(redis_client) if redis_client else None
    
    def update_progress(self, etapa: int, mensagem: str = "", dados_extra: dict = None):
        """Atualiza progresso e publica via Redis Pub/Sub"""
        # Lógica existente de atualização
        self.dados_progresso = {
            "etapa": etapa,
            "mensagem": mensagem,
            "timestamp": datetime.now().isoformat(),
            "dados_extra": dados_extra or {}
        }
        
        # Salvar no Redis (lógica existente)
        if self.redis_client:
            self._salvar_progresso_redis()
        
        # Publicar via Pub/Sub (nova funcionalidade)
        if self.pubsub_manager:
            self.pubsub_manager.publish_progress(self.session_id, self.dados_progresso)
    
    def update_progress_with_estimativas(self, etapa: int, mensagem: str = "", dados_extra: dict = None, estimativas: dict = None):
        """Atualiza progresso incluindo estimativas da Tela 5"""
        # Lógica existente
        if estimativas:
            self.add_estimativas(estimativas)
        
        # Atualizar progresso com estimativas
        progress_data = {
            "etapa": etapa,
            "mensagem": mensagem,
            "timestamp": datetime.now().isoformat(),
            "dados_extra": dados_extra or {},
            "estimativas": estimativas
        }
        
        # Salvar no Redis
        if self.redis_client:
            self._salvar_progresso_redis()
        
        # Publicar via Pub/Sub
        if self.pubsub_manager:
            self.pubsub_manager.publish_progress(self.session_id, progress_data)
```

**2.2 Modificar Arquivo RPA Principal**
```python
# Arquivo: executar_rpa_imediato_playwright.py (modificação)
# Linha 5334-5341: Modificar inicialização do ProgressTracker
if PROGRESS_TRACKER_AVAILABLE:
    session_id = str(uuid.uuid4())
    
    # Inicializar Redis client se disponível
    redis_client = None
    try:
        import redis
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        redis_client.ping()  # Teste de conexão
        exibir_mensagem("[OK] Redis conectado para comunicação real-time")
    except:
        exibir_mensagem("[AVISO] Redis não disponível, usando JSON Progress Tracker")
    
    progress_tracker = ProgressTracker(session_id=session_id, redis_client=redis_client)
    exibir_mensagem("[OK] ProgressTracker ativado com comunicação real-time")
else:
    progress_tracker = None
```

**2.3 Implementar WebSocket Server como Serviço**
```python
# Arquivo: utils/websocket_service.py
import asyncio
import signal
import sys
from utils.websocket_server import RPAWebSocketServer
from utils.redis_pubsub import RedisPubSubManager

class WebSocketService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.websocket_server = RPAWebSocketServer(self.redis_client)
        self.pubsub_manager = RedisPubSubManager(self.redis_client)
    
    async def start_service(self):
        """Inicia o serviço WebSocket"""
        # Configurar handlers de sinal para shutdown graceful
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Iniciar servidor WebSocket
        await self.websocket_server.start_server()
    
    def signal_handler(self, signum, frame):
        """Handler para shutdown graceful"""
        print(f"Recebido sinal {signum}, encerrando serviço...")
        sys.exit(0)

if __name__ == "__main__":
    service = WebSocketService()
    asyncio.run(service.start_service())
```

#### **Entregáveis**
- [ ] ProgressTracker integrado com Redis Pub/Sub
- [ ] Arquivo RPA modificado para suporte real-time
- [ ] WebSocket Server como serviço
- [ ] Testes de integração funcionando

---

### **Fase 3: WebSocket Client (Semana 3)**

#### **Objetivo**
Implementar cliente WebSocket para frontend com reconexão automática e tratamento de erros.

#### **Tarefas**

**3.1 Implementar WebSocket Client JavaScript**
```javascript
// Arquivo: webflow_progress_tracker.js (modificação)
class RPAWebSocketClient {
    constructor(sessionId, options = {}) {
        this.sessionId = sessionId;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
        this.reconnectInterval = options.reconnectInterval || 5000;
        this.heartbeatInterval = options.heartbeatInterval || 30000;
        this.heartbeatTimer = null;
        this.isConnected = false;
        
        // Callbacks
        this.onProgressUpdate = options.onProgressUpdate || (() => {});
        this.onConnectionChange = options.onConnectionChange || (() => {});
        this.onError = options.onError || (() => {});
    }
    
    connect() {
        try {
            this.ws = new WebSocket(`ws://localhost:8080/rpa/${this.sessionId}`);
            this.setupEventHandlers();
        } catch (error) {
            this.onError('Erro ao conectar WebSocket', error);
            this.scheduleReconnect();
        }
    }
    
    setupEventHandlers() {
        this.ws.onopen = () => {
            console.log('WebSocket conectado');
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.onConnectionChange(true);
            this.startHeartbeat();
        };
        
        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (error) {
                this.onError('Erro ao processar mensagem', error);
            }
        };
        
        this.ws.onclose = (event) => {
            console.log('WebSocket desconectado', event.code, event.reason);
            this.isConnected = false;
            this.onConnectionChange(false);
            this.stopHeartbeat();
            
            if (!event.wasClean) {
                this.scheduleReconnect();
            }
        };
        
        this.ws.onerror = (error) => {
            this.onError('Erro no WebSocket', error);
        };
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'progress_update':
                this.onProgressUpdate(data);
                break;
            case 'estimativas':
                this.handleEstimativas(data);
                break;
            case 'error':
                this.onError('Erro do servidor', data);
                break;
            default:
                console.log('Mensagem desconhecida:', data);
        }
    }
    
    handleEstimativas(data) {
        // Atualizar UI com estimativas da Tela 5
        if (data.estimativas && data.estimativas.coberturas_detalhadas) {
            this.updateEstimativasUI(data.estimativas);
        }
    }
    
    updateEstimativasUI(estimativas) {
        // Implementar atualização da UI com estimativas
        const estimativasContainer = document.getElementById('estimativas-container');
        if (estimativasContainer) {
            estimativasContainer.innerHTML = '';
            
            estimativas.coberturas_detalhadas.forEach(cobertura => {
                const coberturaElement = document.createElement('div');
                coberturaElement.className = 'cobertura-item';
                coberturaElement.innerHTML = `
                    <h3>${cobertura.nome}</h3>
                    <p>De: ${cobertura.valores.de}</p>
                    <p>Até: ${cobertura.valores.ate}</p>
                `;
                estimativasContainer.appendChild(coberturaElement);
            });
        }
    }
    
    startHeartbeat() {
        this.heartbeatTimer = setInterval(() => {
            if (this.isConnected) {
                this.ws.send(JSON.stringify({ type: 'ping' }));
            }
        }, this.heartbeatInterval);
    }
    
    stopHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
    }
    
    scheduleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1);
            
            console.log(`Tentando reconectar em ${delay}ms (tentativa ${this.reconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        } else {
            this.onError('Máximo de tentativas de reconexão atingido');
        }
    }
    
    disconnect() {
        this.isConnected = false;
        this.stopHeartbeat();
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Uso do cliente WebSocket
const rpaClient = new RPAWebSocketClient('session-id-here', {
    onProgressUpdate: (data) => {
        // Atualizar barra de progresso
        updateProgressBar(data.etapa, data.mensagem);
        
        // Atualizar status
        updateStatusMessage(data.mensagem);
    },
    onConnectionChange: (connected) => {
        // Atualizar indicador de conexão
        updateConnectionStatus(connected);
    },
    onError: (message, error) => {
        // Exibir erro
        showError(message, error);
    }
});

// Conectar
rpaClient.connect();
```

**3.2 Implementar Fallback para SSE**
```javascript
// Arquivo: webflow_progress_tracker.js (adicionar fallback)
class RPAProgressClient {
    constructor(sessionId, options = {}) {
        this.sessionId = sessionId;
        this.options = options;
        this.websocketClient = null;
        this.sseClient = null;
        this.useWebSocket = true;
    }
    
    connect() {
        if (this.useWebSocket) {
            this.connectWebSocket();
        } else {
            this.connectSSE();
        }
    }
    
    connectWebSocket() {
        this.websocketClient = new RPAWebSocketClient(this.sessionId, this.options);
        this.websocketClient.onError = (message, error) => {
            console.log('WebSocket falhou, tentando SSE:', message);
            this.useWebSocket = false;
            this.connectSSE();
        };
        this.websocketClient.connect();
    }
    
    connectSSE() {
        this.sseClient = new EventSource(`/rpa_progress_sse.php?session_id=${this.sessionId}`);
        
        this.sseClient.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.options.onProgressUpdate(data);
            } catch (error) {
                this.options.onError('Erro ao processar SSE', error);
            }
        };
        
        this.sseClient.onerror = (error) => {
            this.options.onError('Erro no SSE', error);
        };
    }
}
```

#### **Entregáveis**
- [ ] WebSocket Client JavaScript implementado
- [ ] Sistema de reconexão automática
- [ ] Fallback para SSE
- [ ] Testes de frontend funcionando

---

### **Fase 4: Testes e Otimização (Semana 4)**

#### **Objetivo**
Realizar testes completos, otimização de performance e preparação para produção.

#### **Tarefas**

**4.1 Testes de Integração**
```python
# Arquivo: tests/test_integration.py
import pytest
import asyncio
import redis
import websockets
import json

@pytest.mark.asyncio
async def test_full_integration():
    """Teste de integração completa"""
    # Conectar Redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    # Conectar WebSocket
    uri = "ws://localhost:8080/rpa/test-session"
    async with websockets.connect(uri) as websocket:
        # Simular atualização de progresso
        progress_data = {
            "etapa": 5,
            "mensagem": "Tela 5 concluída",
            "estimativas": {
                "coberturas_detalhadas": [
                    {"nome": "CompreensivaDe", "valores": {"de": "R$ 1.000", "ate": "R$ 5.000"}}
                ]
            }
        }
        
        # Publicar via Redis Pub/Sub
        redis_client.publish("rpa_progress:test-session", json.dumps(progress_data))
        
        # Verificar recebimento via WebSocket
        response = await websocket.recv()
        received_data = json.loads(response)
        assert received_data["etapa"] == 5
        assert "estimativas" in received_data
```

**4.2 Testes de Performance**
```python
# Arquivo: tests/test_performance.py
import pytest
import time
import asyncio
import redis
import websockets

@pytest.mark.asyncio
async def test_concurrent_connections():
    """Teste de conexões concorrentes"""
    connections = []
    
    # Criar 100 conexões simultâneas
    for i in range(100):
        uri = f"ws://localhost:8080/rpa/session-{i}"
        websocket = await websockets.connect(uri)
        connections.append(websocket)
    
    # Enviar mensagem para todas as conexões
    start_time = time.time()
    
    for websocket in connections:
        await websocket.send(json.dumps({"test": "message"}))
    
    # Verificar tempo de resposta
    end_time = time.time()
    response_time = end_time - start_time
    
    assert response_time < 1.0  # Deve responder em menos de 1 segundo
    
    # Fechar conexões
    for websocket in connections:
        await websocket.close()
```

**4.3 Monitoramento e Logs**
```python
# Arquivo: utils/monitoring.py
import time
import psutil
import redis
from typing import Dict, Any

class RPAMonitor:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.metrics = {}
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Coleta métricas do sistema"""
        metrics = {
            "timestamp": time.time(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "redis_connections": self.redis_client.info()["connected_clients"],
            "websocket_connections": self.get_websocket_connections(),
            "active_sessions": self.get_active_sessions()
        }
        
        return metrics
    
    def get_websocket_connections(self) -> int:
        """Obtém número de conexões WebSocket ativas"""
        # Implementar contagem de conexões WebSocket
        pass
    
    def get_active_sessions(self) -> int:
        """Obtém número de sessões ativas"""
        # Implementar contagem de sessões ativas
        pass
```

#### **Entregáveis**
- [ ] Testes de integração completos
- [ ] Testes de performance
- [ ] Sistema de monitoramento
- [ ] Documentação de produção

---

## **📋 Cronograma de Implementação**

### **Semana 1: WebSocket Server**
- **Dia 1-2**: Implementar WebSocket Server básico
- **Dia 3-4**: Integrar com Redis Pub/Sub
- **Dia 5**: Testes básicos e documentação

### **Semana 2: Integração ProgressTracker**
- **Dia 1-2**: Modificar ProgressTracker para Redis Pub/Sub
- **Dia 3-4**: Modificar arquivo RPA principal
- **Dia 5**: Testes de integração

### **Semana 3: WebSocket Client**
- **Dia 1-2**: Implementar WebSocket Client JavaScript
- **Dia 3-4**: Implementar sistema de reconexão
- **Dia 5**: Testes de frontend

### **Semana 4: Testes e Otimização**
- **Dia 1-2**: Testes de integração completos
- **Dia 3-4**: Testes de performance
- **Dia 5**: Documentação final e deploy

---

## **🔧 Requisitos Técnicos**

### **Dependências**
```bash
# Python
pip install redis websockets asyncio psutil

# Node.js (para testes)
npm install ws

# Redis Server
# Instalar Redis Server 6.0+
```

### **Configuração Redis**
```bash
# redis.conf
port 6379
bind 127.0.0.1
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### **Configuração WebSocket**
```python
# websocket_config.json
{
    "server": {
        "host": "localhost",
        "port": 8080,
        "max_connections": 1000
    },
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0
    }
}
```

---

## **📊 Métricas de Sucesso**

### **Performance**
- **Latência**: < 100ms para atualizações de progresso
- **Throughput**: Suporte a 100+ conexões simultâneas
- **Uptime**: 99.9% de disponibilidade

### **Funcionalidade**
- **Real-time**: Atualizações instantâneas de progresso
- **Reliability**: Reconexão automática em caso de falha
- **Scalability**: Suporte a múltiplas sessões simultâneas

### **Qualidade**
- **Testes**: 90%+ de cobertura de código
- **Documentação**: Documentação completa da API
- **Monitoramento**: Métricas em tempo real

---

## **🚨 Riscos e Mitigações**

### **Risco 1: Falha de Conexão Redis**
- **Mitigação**: Implementar fallback para JSON
- **Probabilidade**: Baixa
- **Impacto**: Médio

### **Risco 2: Falha de Conexão WebSocket**
- **Mitigação**: Implementar fallback para SSE
- **Probabilidade**: Média
- **Impacto**: Baixo

### **Risco 3: Performance Degradada**
- **Mitigação**: Implementar cache e otimizações
- **Probabilidade**: Baixa
- **Impacto**: Alto

---

## **📞 Suporte e Manutenção**

### **Contatos**
- **Desenvolvedor Principal**: [Nome do Desenvolvedor]
- **Email**: [email@exemplo.com]
- **Telefone**: [telefone]

### **Documentação**
- **API Reference**: `/docs/api`
- **Troubleshooting**: `/docs/troubleshooting`
- **Deployment Guide**: `/docs/deployment`

---

**Documento criado por**: Engenheiro de Software  
**Data**: 26 de Setembro de 2025  
**Versão**: 1.0  
**Status**: 📋 **PRONTO PARA IMPLEMENTAÇÃO**





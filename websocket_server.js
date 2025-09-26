// WebSocket Server para RPA Progress Tracking
// Salvar como: /var/www/rpaimediatoseguros.com.br/websocket/server.js

const WebSocket = require('ws');
const redis = require('redis');

// Configuração
const WS_PORT = 8080;
const REDIS_HOST = 'localhost';
const REDIS_PORT = 6379;

// Cliente Redis
const redisClient = redis.createClient({
    host: REDIS_HOST,
    port: REDIS_PORT
});

redisClient.on('error', (err) => {
    console.error('Redis Client Error:', err);
});

redisClient.on('connect', () => {
    console.log('✅ Conectado ao Redis');
});

// WebSocket Server
const wss = new WebSocket.Server({ 
    port: WS_PORT,
    perMessageDeflate: false
});

console.log(`🚀 WebSocket Server iniciado na porta ${WS_PORT}`);

// Armazenar conexões por sessão
const sessions = new Map();

wss.on('connection', (ws, req) => {
    console.log('🔌 Nova conexão WebSocket');
    
    // Extrair session_id da URL
    const url = new URL(req.url, `http://${req.headers.host}`);
    const sessionId = url.searchParams.get('session_id');
    
    if (!sessionId) {
        ws.close(1008, 'Session ID obrigatório');
        return;
    }
    
    // Armazenar conexão
    if (!sessions.has(sessionId)) {
        sessions.set(sessionId, new Set());
    }
    sessions.get(sessionId).add(ws);
    
    console.log(`📱 Cliente conectado para sessão: ${sessionId}`);
    
    // Configurar subscriber Redis para esta sessão
    const subscriber = redis.createClient({
        host: REDIS_HOST,
        port: REDIS_PORT
    });
    
    subscriber.subscribe(`rpa_progress_${sessionId}`);
    
    subscriber.on('message', (channel, message) => {
        try {
            const data = JSON.parse(message);
            console.log(`📨 Mensagem Redis para ${sessionId}:`, data);
            
            // Enviar para todos os clientes desta sessão
            sessions.get(sessionId)?.forEach(client => {
                if (client.readyState === WebSocket.OPEN) {
                    client.send(JSON.stringify(data));
                }
            });
        } catch (error) {
            console.error('❌ Erro ao processar mensagem Redis:', error);
        }
    });
    
    // Limpar quando desconectar
    ws.on('close', () => {
        console.log(`🔌 Cliente desconectado da sessão: ${sessionId}`);
        sessions.get(sessionId)?.delete(ws);
        
        if (sessions.get(sessionId)?.size === 0) {
            sessions.delete(sessionId);
            subscriber.unsubscribe();
            subscriber.quit();
        }
    });
    
    ws.on('error', (error) => {
        console.error('❌ Erro WebSocket:', error);
    });
    
    // Enviar mensagem de boas-vindas
    ws.send(JSON.stringify({
        type: 'connected',
        session_id: sessionId,
        timestamp: Date.now()
    }));
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('🛑 Encerrando WebSocket Server...');
    wss.close(() => {
        redisClient.quit();
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('🛑 Encerrando WebSocket Server...');
    wss.close(() => {
        redisClient.quit();
        process.exit(0);
    });
});

console.log('✅ WebSocket Server configurado e pronto!');







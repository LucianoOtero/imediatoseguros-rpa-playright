const WebSocket = require('ws');
const http = require('http');

const server = http.createServer();
const wss = new WebSocket.Server({ server });

console.log('🚀 WebSocket Server iniciado na porta 8080');

wss.on('connection', (ws) => {
    console.log('Cliente conectado');
    
    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            
            // Handlers para diferentes tipos de mensagem
            switch(data.type) {
                case 'test_message':
                    console.log('Test message recebida:', data);
                    ws.send(JSON.stringify({
                        type: 'test_response',
                        message: 'Test message processada com sucesso',
                        timestamp: new Date().toISOString()
                    }));
                    break;
                    
                case 'session_event':
                    console.log('Session event recebida:', data);
                    ws.send(JSON.stringify({
                        type: 'session_response',
                        message: 'Session event processada',
                        timestamp: new Date().toISOString()
                    }));
                    break;
                    
                case 'progress_update':
                    console.log('Progress update recebida:', data);
                    ws.send(JSON.stringify({
                        type: 'progress_response',
                        message: 'Progress update processada',
                        timestamp: new Date().toISOString()
                    }));
                    break;
                    
                case 'status_update':
                    console.log('Status update recebida:', data);
                    ws.send(JSON.stringify({
                        type: 'status_response',
                        message: 'Status update processada',
                        timestamp: new Date().toISOString()
                    }));
                    break;
                    
                case 'progress_request':
                    console.log('Progress request recebida:', data);
                    ws.send(JSON.stringify({
                        type: 'progress_data',
                        progress: 50,
                        status: 'running',
                        timestamp: new Date().toISOString()
                    }));
                    break;
                    
                case 'status_request':
                    console.log('Status request recebida:', data);
                    ws.send(JSON.stringify({
                        type: 'status_data',
                        status: 'active',
                        timestamp: new Date().toISOString()
                    }));
                    break;
                    
                case 'session_info':
                    console.log('Session info recebida:', data);
                    ws.send(JSON.stringify({
                        type: 'session_data',
                        session_id: data.session_id || 'default',
                        timestamp: new Date().toISOString()
                    }));
                    break;
                    
                default:
                    console.log('Tipo de mensagem não reconhecido:', data.type);
                    ws.send(JSON.stringify({
                        type: 'error',
                        message: `Tipo de mensagem não reconhecido: ${data.type}`,
                        timestamp: new Date().toISOString()
                    }));
            }
        } catch (error) {
            console.error('Erro ao processar mensagem:', error);
            ws.send(JSON.stringify({
                type: 'error',
                message: 'Erro ao processar mensagem',
                error: error.message,
                timestamp: new Date().toISOString()
            }));
        }
    });
    
    ws.on('close', () => {
        console.log('Cliente desconectado');
    });
    
    ws.on('error', (error) => {
        console.error('Erro no WebSocket:', error);
    });
});

server.listen(8080, () => {
    console.log('✅ WebSocket Server configurado e pronto!');
});

// Tratamento de erros
process.on('uncaughtException', (error) => {
    console.error('Erro não capturado:', error);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Promise rejeitada não tratada:', reason);
});
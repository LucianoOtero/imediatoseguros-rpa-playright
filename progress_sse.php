<?php
/**
 * SERVER-SENT EVENTS ENDPOINT PARA PROGRESS TRACKER
 * Solução híbrida para Windows - usa arquivos temporários
 */

// Configurações para evitar timeout
ini_set('max_execution_time', 0);
ini_set('default_socket_timeout', 0);
set_time_limit(0);

header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
header('Connection: keep-alive');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Verificar se é uma requisição OPTIONS (CORS preflight)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

class ProgressSSE {
    
    private $session_id;
    private $progress_file;
    private $timeout;
    private $start_time;
    
    public function __construct() {
        $this->session_id = $_GET['session_id'] ?? uniqid();
        $this->progress_file = "temp/progress_{$this->session_id}.json";
        $this->timeout = 300; // 5 minutos
        $this->start_time = time();
        
        // Criar diretório temp se não existir
        if (!is_dir('temp')) {
            mkdir('temp', 0755, true);
        }
    }
    
    /**
     * Iniciar RPA em background
     */
    public function iniciarRPA() {
        echo "data: " . json_encode([
            'status' => 'starting',
            'session_id' => $this->session_id,
            'message' => 'Iniciando cotação...'
        ]) . "\n\n";
        flush();
        
        // Comando para executar RPA real com session_id
        $comando = "python executar_rpa_imediato_playwright.py --config parametros.json --session {$this->session_id}";
        
        // Executar em background (Windows)
        if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
            $comando = "start /B $comando";
        } else {
            $comando .= " > /dev/null 2>&1 &";
        }
        
        exec($comando);
        
        echo "data: " . json_encode([
            'status' => 'started',
            'session_id' => $this->session_id,
            'message' => 'RPA iniciado com sucesso'
        ]) . "\n\n";
        flush();
    }
    
    /**
     * Monitorar progresso
     */
    public function monitorarProgresso() {
        $ultima_etapa = 0;
        
        while (true) {
            // Verificar timeout
            if (time() - $this->start_time > $this->timeout) {
                echo "data: " . json_encode([
                    'status' => 'timeout',
                    'session_id' => $this->session_id,
                    'message' => 'Timeout atingido'
                ]) . "\n\n";
                break;
            }
            
            // Verificar se arquivo de progresso existe
            if (file_exists($this->progress_file)) {
                $progresso = json_decode(file_get_contents($this->progress_file), true);
                
                if ($progresso && $progresso['etapa_atual'] > $ultima_etapa) {
                    // Adicionar informações da sessão
                    $progresso['session_id'] = $this->session_id;
                    $progresso['timestamp'] = date('Y-m-d H:i:s');
                    
                    // Enviar progresso
                    echo "data: " . json_encode($progresso) . "\n\n";
                    flush();
                    
                    $ultima_etapa = $progresso['etapa_atual'];
                    
                    // Verificar se terminou
                    if ($progresso['etapa_atual'] >= 15) {
                        echo "data: " . json_encode([
                            'status' => 'completed',
                            'session_id' => $this->session_id,
                            'message' => 'Cotação concluída com sucesso',
                            'progresso' => $progresso
                        ]) . "\n\n";
                        flush();
                        break;
                    }
                }
            }
            
            // Aguardar 1 segundo
            sleep(1);
        }
        
        // Cleanup
        $this->limparArquivos();
    }
    
    /**
     * Limpar arquivos temporários
     */
    private function limparArquivos() {
        if (file_exists($this->progress_file)) {
            unlink($this->progress_file);
        }
    }
    
    /**
     * Executar monitoramento completo
     */
    public function executar() {
        try {
            $this->iniciarRPA();
            $this->monitorarProgresso();
        } catch (Exception $e) {
            echo "data: " . json_encode([
                'status' => 'error',
                'session_id' => $this->session_id,
                'message' => 'Erro: ' . $e->getMessage()
            ]) . "\n\n";
            flush();
        }
    }
}

// Executar SSE
$sse = new ProgressSSE();
$sse->executar();
?>

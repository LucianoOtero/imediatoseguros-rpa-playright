<?php
/**
 * FileHandler - Fallback para logs em arquivo
 * Sistema de Logging RPA - Imediato Seguros
 */

class FileHandler {
    private $logFile;
    private $maxFileSize;
    
    public function __construct($logFile, $maxFileSize = '10MB') {
        $this->logFile = $logFile;
        $this->maxFileSize = $this->parseSize($maxFileSize);
        $this->ensureLogFile();
    }
    
    private function parseSize($size) {
        $units = ['B' => 1, 'K' => 1024, 'M' => 1024*1024, 'G' => 1024*1024*1024];
        $size = strtoupper(trim($size));
        
        foreach ($units as $unit => $multiplier) {
            if (strpos($size, $unit) !== false) {
                return (int) $size * $multiplier;
            }
        }
        
        return 10 * 1024 * 1024; // Default 10MB
    }
    
    private function ensureLogFile() {
        $dir = dirname($this->logFile);
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }
        
        if (!file_exists($this->logFile)) {
            touch($this->logFile);
            chmod($this->logFile, 0644);
        }
    }
    
    public function save($logEntry) {
        try {
            // Verificar tamanho do arquivo
            if (file_exists($this->logFile) && filesize($this->logFile) > $this->maxFileSize) {
                $this->rotateLogFile();
            }
            
            // Formatar entrada do log
            $logLine = sprintf(
                '[%s] [%s] [%s] %s | %s | %s | %s' . PHP_EOL,
                $logEntry['timestamp'],
                $logEntry['level'],
                $logEntry['session_id'],
                $logEntry['message'],
                $logEntry['url'],
                $logEntry['ip_address'],
                json_encode($logEntry['data'])
            );
            
            // Escrever no arquivo
            $result = file_put_contents($this->logFile, $logLine, FILE_APPEND | LOCK_EX);
            
            if ($result === false) {
                throw new Exception('Failed to write to log file');
            }
            
            return [
                'success' => true,
                'method' => 'file',
                'bytes_written' => $result,
                'log_file' => $this->logFile
            ];
            
        } catch (Exception $e) {
            throw new Exception('File save failed: ' . $e->getMessage());
        }
    }
    
    private function rotateLogFile() {
        $timestamp = date('Y-m-d_H-i-s');
        $rotatedFile = $this->logFile . '.' . $timestamp;
        
        if (file_exists($this->logFile)) {
            rename($this->logFile, $rotatedFile);
        }
        
        // Manter apenas os últimos 5 arquivos rotacionados
        $pattern = $this->logFile . '.*';
        $files = glob($pattern);
        
        if (count($files) > 5) {
            usort($files, function($a, $b) {
                return filemtime($a) - filemtime($b);
            });
            
            for ($i = 0; $i < count($files) - 5; $i++) {
                unlink($files[$i]);
            }
        }
    }
    
    public function getLogFile() {
        return $this->logFile;
    }
}



































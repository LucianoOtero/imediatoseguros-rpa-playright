<?php

namespace RPA\Services;

use RPA\Interfaces\LoggerInterface;

class LoggerService implements LoggerInterface
{
    private string $logPath;
    private string $level;
    private int $maxFiles;

    public function __construct(array $config)
    {
        $this->logPath = $config['path'] ?? '/tmp/rpa.log';
        $this->level = $config['level'] ?? 'info';
        $this->maxFiles = $config['max_files'] ?? 30;
        
        // Criar diretório se não existir
        $dir = dirname($this->logPath);
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }
    }

    public function info(string $message, array $context = []): void
    {
        $this->log('INFO', $message, $context);
    }

    public function warning(string $message, array $context = []): void
    {
        $this->log('WARNING', $message, $context);
    }

    public function error(string $message, array $context = []): void
    {
        $this->log('ERROR', $message, $context);
    }

    public function debug(string $message, array $context = []): void
    {
        if ($this->shouldLog('debug')) {
            $this->log('DEBUG', $message, $context);
        }
    }

    private function log(string $level, string $message, array $context = []): void
    {
        if (!$this->shouldLog(strtolower($level))) {
            return;
        }

        $logEntry = [
            'timestamp' => date('Y-m-d H:i:s'),
            'level' => $level,
            'message' => $message,
            'context' => $context,
            'memory' => memory_get_usage(true),
            'pid' => getmypid()
        ];

        $logLine = json_encode($logEntry, JSON_UNESCAPED_UNICODE) . "\n";
        
        file_put_contents($this->logPath, $logLine, FILE_APPEND | LOCK_EX);
        
        $this->rotateLogs();
    }

    private function shouldLog(string $level): bool
    {
        $levels = ['debug' => 0, 'info' => 1, 'warning' => 2, 'error' => 3];
        $currentLevel = $levels[$this->level] ?? 1;
        $messageLevel = $levels[$level] ?? 1;
        
        return $messageLevel >= $currentLevel;
    }

    private function rotateLogs(): void
    {
        if (!file_exists($this->logPath)) {
            return;
        }

        $fileSize = filesize($this->logPath);
        $maxSize = 10 * 1024 * 1024; // 10MB

        if ($fileSize > $maxSize) {
            $this->rotate();
        }
    }

    private function rotate(): void
    {
        // Rotacionar arquivos existentes
        for ($i = $this->maxFiles - 1; $i > 0; $i--) {
            $oldFile = $this->logPath . '.' . $i;
            $newFile = $this->logPath . '.' . ($i + 1);
            
            if (file_exists($oldFile)) {
                if ($i === $this->maxFiles - 1) {
                    unlink($oldFile);
                } else {
                    rename($oldFile, $newFile);
                }
            }
        }

        // Mover arquivo atual
        if (file_exists($this->logPath)) {
            rename($this->logPath, $this->logPath . '.1');
        }
    }
}

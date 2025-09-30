<?php

namespace RPA\Repositories;

class SessionRepository
{
    private string $sessionsPath;
    private string $dataPath;

    public function __construct(string $sessionsPath, string $dataPath)
    {
        $this->sessionsPath = $sessionsPath;
        $this->dataPath = $dataPath;
        
        // Criar diretórios se não existirem
        if (!is_dir($this->sessionsPath)) {
            mkdir($this->sessionsPath, 0755, true);
        }
        
        if (!is_dir($this->dataPath)) {
            mkdir($this->dataPath, 0755, true);
        }
    }

    public function createSession(array $data): string
    {
        $sessionId = $this->generateSessionId();
        $sessionPath = $this->sessionsPath . '/' . $sessionId;
        
        // Criar diretório da sessão
        if (!is_dir($sessionPath)) {
            mkdir($sessionPath, 0755, true);
        }
        
        // Salvar dados da sessão
        $sessionData = [
            'session_id' => $sessionId,
            'created_at' => date('Y-m-d H:i:s'),
            'status' => 'pending',
            'data' => $data,
            'progress' => 0,
            'current_step' => 'initializing'
        ];
        
        file_put_contents(
            $sessionPath . '/session.json',
            json_encode($sessionData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)
        );
        
        return $sessionId;
    }

    public function getSession(string $sessionId): ?array
    {
        $sessionPath = $this->sessionsPath . '/' . $sessionId;
        $sessionFile = $sessionPath . '/session.json';
        
        if (!file_exists($sessionFile)) {
            return null;
        }
        
        $content = file_get_contents($sessionFile);
        return json_decode($content, true);
    }

    public function updateSession(string $sessionId, array $data): bool
    {
        $sessionPath = $this->sessionsPath . '/' . $sessionId;
        $sessionFile = $sessionPath . '/session.json';
        
        if (!file_exists($sessionFile)) {
            return false;
        }
        
        $currentData = $this->getSession($sessionId);
        if (!$currentData) {
            return false;
        }
        
        $updatedData = array_merge($currentData, $data);
        $updatedData['updated_at'] = date('Y-m-d H:i:s');
        
        return file_put_contents(
            $sessionFile,
            json_encode($updatedData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)
        ) !== false;
    }

    public function deleteSession(string $sessionId): bool
    {
        $sessionPath = $this->sessionsPath . '/' . $sessionId;
        
        if (!is_dir($sessionPath)) {
            return false;
        }
        
        return $this->removeDirectory($sessionPath);
    }

    public function listSessions(): array
    {
        $sessions = [];
        
        if (!is_dir($this->sessionsPath)) {
            return $sessions;
        }
        
        $directories = scandir($this->sessionsPath);
        
        foreach ($directories as $dir) {
            if ($dir === '.' || $dir === '..') {
                continue;
            }
            
            $sessionPath = $this->sessionsPath . '/' . $dir;
            if (is_dir($sessionPath)) {
                $session = $this->getSession($dir);
                if ($session) {
                    $sessions[] = $session;
                }
            }
        }
        
        // Ordenar por data de criação (mais recente primeiro)
        usort($sessions, function($a, $b) {
            return strtotime($b['created_at']) - strtotime($a['created_at']);
        });
        
        return $sessions;
    }

    public function getProgress(string $sessionId): ?array
    {
        $sessionPath = $this->sessionsPath . '/' . $sessionId;
        $progressFile = $sessionPath . '/progress.json';
        
        if (!file_exists($progressFile)) {
            return null;
        }
        
        $content = file_get_contents($progressFile);
        return json_decode($content, true);
    }

    public function updateProgress(string $sessionId, array $progress): bool
    {
        $sessionPath = $this->sessionsPath . '/' . $sessionId;
        
        if (!is_dir($sessionPath)) {
            return false;
        }
        
        $progress['updated_at'] = date('Y-m-d H:i:s');
        
        return file_put_contents(
            $sessionPath . '/progress.json',
            json_encode($progress, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)
        ) !== false;
    }

    public function cleanupOldSessions(int $daysOld = 7): int
    {
        $cleaned = 0;
        $cutoffTime = time() - ($daysOld * 24 * 60 * 60);
        
        if (!is_dir($this->sessionsPath)) {
            return $cleaned;
        }
        
        $directories = scandir($this->sessionsPath);
        
        foreach ($directories as $dir) {
            if ($dir === '.' || $dir === '..') {
                continue;
            }
            
            $sessionPath = $this->sessionsPath . '/' . $dir;
            if (is_dir($sessionPath)) {
                $session = $this->getSession($dir);
                if ($session && strtotime($session['created_at']) < $cutoffTime) {
                    if ($this->removeDirectory($sessionPath)) {
                        $cleaned++;
                    }
                }
            }
        }
        
        return $cleaned;
    }

    private function generateSessionId(): string
    {
        $timestamp = date('Ymd_His');
        $random = substr(md5(uniqid()), 0, 8);
        return "rpa_v4_{$timestamp}_{$random}";
    }

    private function removeDirectory(string $dir): bool
    {
        if (!is_dir($dir)) {
            return false;
        }
        
        $files = array_diff(scandir($dir), ['.', '..']);
        
        foreach ($files as $file) {
            $path = $dir . '/' . $file;
            if (is_dir($path)) {
                $this->removeDirectory($path);
            } else {
                unlink($path);
            }
        }
        
        return rmdir($dir);
    }
}

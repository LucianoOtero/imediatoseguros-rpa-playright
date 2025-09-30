<?php

namespace RPA\Interfaces;

interface MonitorServiceInterface
{
    /**
     * Monitorar progresso de uma sessão
     */
    public function monitor(string $sessionId): array;
    
    /**
     * Obter logs de uma sessão
     */
    public function getLogs(string $sessionId, int $limit = 100): array;
    
    /**
     * Verificar saúde do sistema
     */
    public function healthCheck(): array;
    
    /**
     * Obter métricas do sistema
     */
    public function getMetrics(): array;
}

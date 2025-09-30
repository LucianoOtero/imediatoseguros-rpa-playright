<?php

namespace RPA\Interfaces;

interface SessionServiceInterface
{
    /**
     * Criar uma nova sessão RPA
     */
    public function create(array $data): array;
    
    /**
     * Obter status de uma sessão
     */
    public function getStatus(string $sessionId): array;
    
    /**
     * Listar todas as sessões
     */
    public function list(): array;
    
    /**
     * Parar uma sessão
     */
    public function stop(string $sessionId): array;
    
    /**
     * Limpar sessões antigas
     */
    public function cleanup(): array;
}

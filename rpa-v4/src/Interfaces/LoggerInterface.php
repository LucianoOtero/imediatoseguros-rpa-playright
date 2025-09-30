<?php

namespace RPA\Interfaces;

interface LoggerInterface
{
    /**
     * Log de informação
     */
    public function info(string $message, array $context = []): void;
    
    /**
     * Log de aviso
     */
    public function warning(string $message, array $context = []): void;
    
    /**
     * Log de erro
     */
    public function error(string $message, array $context = []): void;
    
    /**
     * Log de debug
     */
    public function debug(string $message, array $context = []): void;
}

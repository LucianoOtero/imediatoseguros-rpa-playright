<?php

namespace RPA\Services;

class RateLimitService
{
    private ?\Redis $redis;
    private int $maxRequests;
    private int $window;

    public function __construct(array $config)
    {
        $this->maxRequests = $config['max_requests'] ?? 100;
        $this->window = $config['window'] ?? 3600;

        if (extension_loaded('redis')) {
            $this->redis = new \Redis();
            try {
                $this->redis->connect(
                    $config['host'] ?? '127.0.0.1',
                    $config['port'] ?? 6379
                );
                
                if (isset($config['password'])) {
                    $this->redis->auth($config['password']);
                }
                
                if (isset($config['database'])) {
                    $this->redis->select($config['database']);
                }
            } catch (\Exception $e) {
                $this->redis = null;
            }
        } else {
            $this->redis = null;
        }
    }

    public function isAllowed(string $identifier): bool
    {
        if (!$this->redis) {
            return true; // Se Redis não estiver disponível, permitir
        }

        $key = "rate_limit:{$identifier}";
        
        try {
            $current = $this->redis->incr($key);
            
            if ($current === 1) {
                $this->redis->expire($key, $this->window);
            }
            
            return $current <= $this->maxRequests;
        } catch (\Exception $e) {
            return true; // Em caso de erro, permitir
        }
    }

    public function getRemainingRequests(string $identifier): int
    {
        if (!$this->redis) {
            return $this->maxRequests;
        }

        $key = "rate_limit:{$identifier}";
        
        try {
            $current = $this->redis->get($key) ?: 0;
            return max(0, $this->maxRequests - $current);
        } catch (\Exception $e) {
            return $this->maxRequests;
        }
    }

    public function getResetTime(string $identifier): int
    {
        if (!$this->redis) {
            return time() + $this->window;
        }

        $key = "rate_limit:{$identifier}";
        
        try {
            $ttl = $this->redis->ttl($key);
            return $ttl > 0 ? time() + $ttl : time() + $this->window;
        } catch (\Exception $e) {
            return time() + $this->window;
        }
    }

    public function reset(string $identifier): bool
    {
        if (!$this->redis) {
            return true;
        }

        $key = "rate_limit:{$identifier}";
        
        try {
            return $this->redis->del($key) > 0;
        } catch (\Exception $e) {
            return false;
        }
    }
}

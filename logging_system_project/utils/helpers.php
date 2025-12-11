<?php
/**
 * utils/helpers.php - Funções Auxiliares
 * Sistema de Logging PHP - RPA Imediato Seguros
 */

/**
 * Formata timestamp para exibição
 * @param string $timestamp
 * @return string
 */
function formatTimestamp($timestamp) {
    $date = new DateTime($timestamp);
    return $date->format('d/m/Y H:i:s');
}

/**
 * Formata duração em segundos para formato legível
 * @param int $seconds
 * @return string
 */
function formatDuration($seconds) {
    if ($seconds < 60) {
        return $seconds . 's';
    } elseif ($seconds < 3600) {
        return floor($seconds / 60) . 'm ' . ($seconds % 60) . 's';
    } else {
        $hours = floor($seconds / 3600);
        $minutes = floor(($seconds % 3600) / 60);
        return $hours . 'h ' . $minutes . 'm';
    }
}

/**
 * Formata tamanho em bytes para formato legível
 * @param int $bytes
 * @return string
 */
function formatBytes($bytes) {
    $units = ['B', 'KB', 'MB', 'GB', 'TB'];
    $bytes = max($bytes, 0);
    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
    $pow = min($pow, count($units) - 1);
    
    $bytes /= pow(1024, $pow);
    
    return round($bytes, 2) . ' ' . $units[$pow];
}

/**
 * Gera cor para nível de log
 * @param string $level
 * @return string
 */
function getLogLevelColor($level) {
    $colors = [
        'DEBUG' => '#6c757d',
        'INFO' => '#17a2b8',
        'WARNING' => '#ffc107',
        'ERROR' => '#dc3545'
    ];
    
    return $colors[strtoupper($level)] ?? '#6c757d';
}

/**
 * Gera ícone para nível de log
 * @param string $level
 * @return string
 */
function getLogLevelIcon($level) {
    $icons = [
        'DEBUG' => '🔍',
        'INFO' => 'ℹ️',
        'WARNING' => '⚠️',
        'ERROR' => '❌'
    ];
    
    return $icons[strtoupper($level)] ?? '❓';
}

/**
 * Trunca texto mantendo palavras inteiras
 * @param string $text
 * @param int $length
 * @return string
 */
function truncateText($text, $length = 100) {
    if (strlen($text) <= $length) {
        return $text;
    }
    
    $truncated = substr($text, 0, $length);
    $lastSpace = strrpos($truncated, ' ');
    
    if ($lastSpace !== false) {
        $truncated = substr($truncated, 0, $lastSpace);
    }
    
    return $truncated . '...';
}

/**
 * Valida formato de email
 * @param string $email
 * @return bool
 */
function isValidEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Valida formato de URL
 * @param string $url
 * @return bool
 */
function isValidUrl($url) {
    return filter_var($url, FILTER_VALIDATE_URL) !== false;
}

/**
 * Extrai domínio de URL
 * @param string $url
 * @return string
 */
function extractDomain($url) {
    $parsed = parse_url($url);
    return $parsed['host'] ?? '';
}

/**
 * Gera hash seguro
 * @param string $data
 * @return string
 */
function generateSecureHash($data) {
    return hash('sha256', $data . time() . random_bytes(16));
}

/**
 * Converte array para JSON seguro
 * @param mixed $data
 * @return string
 */
function safeJsonEncode($data) {
    return json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
}

/**
 * Converte JSON para array seguro
 * @param string $json
 * @return mixed
 */
function safeJsonDecode($json) {
    return json_decode($json, true);
}

/**
 * Gera ID único
 * @param string $prefix
 * @return string
 */
function generateUniqueId($prefix = '') {
    return $prefix . uniqid() . '_' . bin2hex(random_bytes(4));
}

/**
 * Verifica se string é JSON válido
 * @param string $string
 * @return bool
 */
function isValidJson($string) {
    json_decode($string);
    return json_last_error() === JSON_ERROR_NONE;
}

/**
 * Limpa dados de entrada
 * @param mixed $data
 * @return mixed
 */
function cleanInput($data) {
    if (is_string($data)) {
        return trim(strip_tags($data));
    }
    
    if (is_array($data)) {
        return array_map('cleanInput', $data);
    }
    
    return $data;
}

/**
 * Converte timestamp para formato ISO
 * @param mixed $timestamp
 * @return string
 */
function toIsoTimestamp($timestamp) {
    if (is_numeric($timestamp)) {
        return date('c', $timestamp);
    }
    
    if (is_string($timestamp)) {
        return date('c', strtotime($timestamp));
    }
    
    return date('c');
}

/**
 * Calcula diferença entre timestamps
 * @param string $start
 * @param string $end
 * @return int
 */
function calculateTimeDifference($start, $end) {
    $startTime = new DateTime($start);
    $endTime = new DateTime($end);
    
    return $endTime->getTimestamp() - $startTime->getTimestamp();
}

/**
 * Gera estatísticas de array
 * @param array $data
 * @return array
 */
function generateArrayStats($data) {
    if (empty($data)) {
        return [
            'count' => 0,
            'min' => 0,
            'max' => 0,
            'avg' => 0,
            'sum' => 0
        ];
    }
    
    return [
        'count' => count($data),
        'min' => min($data),
        'max' => max($data),
        'avg' => array_sum($data) / count($data),
        'sum' => array_sum($data)
    ];
}

/**
 * Agrupa dados por campo
 * @param array $data
 * @param string $field
 * @return array
 */
function groupByField($data, $field) {
    $grouped = [];
    
    foreach ($data as $item) {
        $key = $item[$field] ?? 'unknown';
        if (!isset($grouped[$key])) {
            $grouped[$key] = [];
        }
        $grouped[$key][] = $item;
    }
    
    return $grouped;
}

/**
 * Ordena array por campo
 * @param array $data
 * @param string $field
 * @param string $direction
 * @return array
 */
function sortByField($data, $field, $direction = 'asc') {
    usort($data, function($a, $b) use ($field, $direction) {
        $aVal = $a[$field] ?? '';
        $bVal = $b[$field] ?? '';
        
        if ($direction === 'desc') {
            return $bVal <=> $aVal;
        }
        
        return $aVal <=> $bVal;
    });
    
    return $data;
}

/**
 * Pagina array de dados
 * @param array $data
 * @param int $page
 * @param int $perPage
 * @return array
 */
function paginateArray($data, $page = 1, $perPage = 20) {
    $total = count($data);
    $offset = ($page - 1) * $perPage;
    $items = array_slice($data, $offset, $perPage);
    
    return [
        'items' => $items,
        'pagination' => [
            'current_page' => $page,
            'per_page' => $perPage,
            'total' => $total,
            'total_pages' => ceil($total / $perPage),
            'has_next' => $offset + $perPage < $total,
            'has_prev' => $page > 1
        ]
    ];
}

/**
 * Gera CSV de dados
 * @param array $data
 * @param array $headers
 * @return string
 */
function generateCsv($data, $headers = []) {
    $output = fopen('php://temp', 'r+');
    
    if (!empty($headers)) {
        fputcsv($output, $headers);
    }
    
    foreach ($data as $row) {
        if (is_array($row)) {
            fputcsv($output, array_values($row));
        } else {
            fputcsv($output, [$row]);
        }
    }
    
    rewind($output);
    $csv = stream_get_contents($output);
    fclose($output);
    
    return $csv;
}

/**
 * Gera XML de dados
 * @param array $data
 * @param string $rootElement
 * @return string
 */
function generateXml($data, $rootElement = 'data') {
    $xml = new SimpleXMLElement("<$rootElement></$rootElement>");
    
    foreach ($data as $key => $value) {
        if (is_array($value)) {
            $child = $xml->addChild($key);
            arrayToXml($value, $child);
        } else {
            $xml->addChild($key, htmlspecialchars($value));
        }
    }
    
    return $xml->asXML();
}

/**
 * Converte array para XML recursivamente
 * @param array $data
 * @param SimpleXMLElement $xml
 */
function arrayToXml($data, &$xml) {
    foreach ($data as $key => $value) {
        if (is_array($value)) {
            $child = $xml->addChild($key);
            arrayToXml($value, $child);
        } else {
            $xml->addChild($key, htmlspecialchars($value));
        }
    }
}

/**
 * Valida formato de data
 * @param string $date
 * @param string $format
 * @return bool
 */
function isValidDate($date, $format = 'Y-m-d H:i:s') {
    $d = DateTime::createFromFormat($format, $date);
    return $d && $d->format($format) === $date;
}

/**
 * Converte timezone de data
 * @param string $date
 * @param string $fromTimezone
 * @param string $toTimezone
 * @return string
 */
function convertTimezone($date, $fromTimezone, $toTimezone) {
    $dt = new DateTime($date, new DateTimeZone($fromTimezone));
    $dt->setTimezone(new DateTimeZone($toTimezone));
    return $dt->format('Y-m-d H:i:s');
}

/**
 * Gera senha segura
 * @param int $length
 * @return string
 */
function generateSecurePassword($length = 12) {
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
    return substr(str_shuffle($chars), 0, $length);
}

/**
 * Verifica força da senha
 * @param string $password
 * @return array
 */
function checkPasswordStrength($password) {
    $score = 0;
    $feedback = [];
    
    if (strlen($password) >= 8) {
        $score += 1;
    } else {
        $feedback[] = 'Senha deve ter pelo menos 8 caracteres';
    }
    
    if (preg_match('/[a-z]/', $password)) {
        $score += 1;
    } else {
        $feedback[] = 'Adicione letras minúsculas';
    }
    
    if (preg_match('/[A-Z]/', $password)) {
        $score += 1;
    } else {
        $feedback[] = 'Adicione letras maiúsculas';
    }
    
    if (preg_match('/[0-9]/', $password)) {
        $score += 1;
    } else {
        $feedback[] = 'Adicione números';
    }
    
    if (preg_match('/[^a-zA-Z0-9]/', $password)) {
        $score += 1;
    } else {
        $feedback[] = 'Adicione caracteres especiais';
    }
    
    $strength = 'Muito Fraca';
    if ($score >= 4) {
        $strength = 'Forte';
    } elseif ($score >= 3) {
        $strength = 'Média';
    } elseif ($score >= 2) {
        $strength = 'Fraca';
    }
    
    return [
        'score' => $score,
        'strength' => $strength,
        'feedback' => $feedback
    ];
}
?>





































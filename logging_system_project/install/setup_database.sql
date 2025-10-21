-- =====================================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS - SISTEMA DE LOGGING
-- =====================================================
-- 
-- Este script cria o banco de dados e tabelas necessárias
-- para o sistema de logging PHP do projeto RPA Imediato Seguros
--
-- Executar no MySQL do servidor mdmidia.com.br
-- =====================================================

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS rpa_logs 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar o banco de dados
USE rpa_logs;

-- =====================================================
-- TABELA PRINCIPAL: debug_logs
-- =====================================================
CREATE TABLE IF NOT EXISTS debug_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    log_id VARCHAR(50) NOT NULL UNIQUE,
    session_id VARCHAR(50) NOT NULL,
    timestamp DATETIME(3) NOT NULL,
    client_timestamp DATETIME(3),
    level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR') NOT NULL,
    message TEXT NOT NULL,
    data JSON,
    url VARCHAR(500),
    user_agent TEXT,
    ip_address VARCHAR(45),
    server_time DECIMAL(15,6),
    request_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices para performance
    INDEX idx_session_timestamp (session_id, timestamp),
    INDEX idx_level_timestamp (level, timestamp),
    INDEX idx_url_timestamp (url, timestamp),
    INDEX idx_timestamp (timestamp),
    INDEX idx_log_id (log_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA DE MÉTRICAS: log_metrics
-- =====================================================
CREATE TABLE IF NOT EXISTS log_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    total_logs INT DEFAULT 0,
    debug_logs INT DEFAULT 0,
    info_logs INT DEFAULT 0,
    warning_logs INT DEFAULT 0,
    error_logs INT DEFAULT 0,
    unique_sessions INT DEFAULT 0,
    avg_session_duration DECIMAL(10,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_date (date),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA DE SESSÕES: sessions
-- =====================================================
CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL UNIQUE,
    start_time DATETIME(3) NOT NULL,
    end_time DATETIME(3),
    total_logs INT DEFAULT 0,
    url VARCHAR(500),
    user_agent TEXT,
    ip_address VARCHAR(45),
    status ENUM('ACTIVE', 'COMPLETED', 'ERROR') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_session_id (session_id),
    INDEX idx_start_time (start_time),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA DE CONFIGURAÇÕES: config
-- =====================================================
CREATE TABLE IF NOT EXISTS config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_config_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- INSERIR CONFIGURAÇÕES PADRÃO
-- =====================================================
INSERT INTO config (config_key, config_value, description) VALUES
('max_log_size', '10000', 'Tamanho máximo de dados em caracteres'),
('retention_days', '30', 'Dias para manter logs antigos'),
('rate_limit_per_minute', '100', 'Limite de requisições por minuto por IP'),
('enable_metrics', '1', 'Habilitar coleta de métricas'),
('cleanup_enabled', '1', 'Habilitar limpeza automática de logs antigos')
ON DUPLICATE KEY UPDATE 
    config_value = VALUES(config_value),
    updated_at = CURRENT_TIMESTAMP;

-- =====================================================
-- PROCEDURES PARA MANUTENÇÃO
-- =====================================================

-- Procedure para limpeza de logs antigos
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS CleanupOldLogs()
BEGIN
    DECLARE retention_days INT DEFAULT 30;
    
    -- Obter configuração de retenção
    SELECT CAST(config_value AS UNSIGNED) INTO retention_days 
    FROM config 
    WHERE config_key = 'retention_days';
    
    -- Deletar logs antigos
    DELETE FROM debug_logs 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL retention_days DAY);
    
    -- Deletar sessões antigas
    DELETE FROM sessions 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL retention_days DAY);
    
    -- Log da operação
    INSERT INTO debug_logs (
        log_id, session_id, timestamp, level, message, 
        data, url, user_agent, ip_address, server_time, request_id
    ) VALUES (
        CONCAT('cleanup_', UNIX_TIMESTAMP()),
        'system',
        NOW(3),
        'INFO',
        'Limpeza automática de logs antigos executada',
        JSON_OBJECT('retention_days', retention_days, 'deleted_logs', ROW_COUNT()),
        'system://cleanup',
        'MySQL Procedure',
        '127.0.0.1',
        UNIX_TIMESTAMP(NOW(6)),
        CONCAT('cleanup_', UNIX_TIMESTAMP())
    );
END //
DELIMITER ;

-- Procedure para atualizar métricas diárias
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS UpdateDailyMetrics(IN target_date DATE)
BEGIN
    DECLARE total_logs_count INT DEFAULT 0;
    DECLARE debug_logs_count INT DEFAULT 0;
    DECLARE info_logs_count INT DEFAULT 0;
    DECLARE warning_logs_count INT DEFAULT 0;
    DECLARE error_logs_count INT DEFAULT 0;
    DECLARE unique_sessions_count INT DEFAULT 0;
    DECLARE avg_duration DECIMAL(10,3) DEFAULT 0;
    
    -- Contar logs por nível
    SELECT COUNT(*) INTO total_logs_count
    FROM debug_logs 
    WHERE DATE(timestamp) = target_date;
    
    SELECT COUNT(*) INTO debug_logs_count
    FROM debug_logs 
    WHERE DATE(timestamp) = target_date AND level = 'DEBUG';
    
    SELECT COUNT(*) INTO info_logs_count
    FROM debug_logs 
    WHERE DATE(timestamp) = target_date AND level = 'INFO';
    
    SELECT COUNT(*) INTO warning_logs_count
    FROM debug_logs 
    WHERE DATE(timestamp) = target_date AND level = 'WARNING';
    
    SELECT COUNT(*) INTO error_logs_count
    FROM debug_logs 
    WHERE DATE(timestamp) = target_date AND level = 'ERROR';
    
    -- Contar sessões únicas
    SELECT COUNT(DISTINCT session_id) INTO unique_sessions_count
    FROM debug_logs 
    WHERE DATE(timestamp) = target_date;
    
    -- Calcular duração média das sessões
    SELECT AVG(TIMESTAMPDIFF(SECOND, start_time, end_time)) INTO avg_duration
    FROM sessions 
    WHERE DATE(start_time) = target_date AND end_time IS NOT NULL;
    
    -- Inserir ou atualizar métricas
    INSERT INTO log_metrics (
        date, total_logs, debug_logs, info_logs, warning_logs, 
        error_logs, unique_sessions, avg_session_duration
    ) VALUES (
        target_date, total_logs_count, debug_logs_count, info_logs_count, 
        warning_logs_count, error_logs_count, unique_sessions_count, avg_duration
    ) ON DUPLICATE KEY UPDATE
        total_logs = VALUES(total_logs),
        debug_logs = VALUES(debug_logs),
        info_logs = VALUES(info_logs),
        warning_logs = VALUES(warning_logs),
        error_logs = VALUES(error_logs),
        unique_sessions = VALUES(unique_sessions),
        avg_session_duration = VALUES(avg_session_duration),
        updated_at = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- =====================================================
-- TRIGGERS PARA AUTOMAÇÃO
-- =====================================================

-- Trigger para atualizar contador de logs na sessão
DELIMITER //
CREATE TRIGGER IF NOT EXISTS update_session_log_count
AFTER INSERT ON debug_logs
FOR EACH ROW
BEGIN
    UPDATE sessions 
    SET total_logs = total_logs + 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE session_id = NEW.session_id;
END //
DELIMITER ;

-- Trigger para criar sessão automaticamente
DELIMITER //
CREATE TRIGGER IF NOT EXISTS create_session_if_not_exists
BEFORE INSERT ON debug_logs
FOR EACH ROW
BEGIN
    DECLARE session_exists INT DEFAULT 0;
    
    SELECT COUNT(*) INTO session_exists
    FROM sessions 
    WHERE session_id = NEW.session_id;
    
    IF session_exists = 0 THEN
        INSERT INTO sessions (
            session_id, start_time, url, user_agent, ip_address, status
        ) VALUES (
            NEW.session_id, 
            NEW.timestamp, 
            NEW.url, 
            NEW.user_agent, 
            NEW.ip_address, 
            'ACTIVE'
        );
    END IF;
END //
DELIMITER ;

-- =====================================================
-- VIEWS PARA ANÁLISE
-- =====================================================

-- View para análise de sessões
CREATE OR REPLACE VIEW session_analysis AS
SELECT 
    s.session_id,
    s.start_time,
    s.end_time,
    s.total_logs,
    s.url,
    s.status,
    TIMESTAMPDIFF(SECOND, s.start_time, s.end_time) as duration_seconds,
    COUNT(CASE WHEN dl.level = 'ERROR' THEN 1 END) as error_count,
    COUNT(CASE WHEN dl.level = 'WARNING' THEN 1 END) as warning_count,
    COUNT(CASE WHEN dl.level = 'INFO' THEN 1 END) as info_count,
    COUNT(CASE WHEN dl.level = 'DEBUG' THEN 1 END) as debug_count
FROM sessions s
LEFT JOIN debug_logs dl ON s.session_id = dl.session_id
GROUP BY s.session_id, s.start_time, s.end_time, s.total_logs, s.url, s.status;

-- View para análise de performance
CREATE OR REPLACE VIEW performance_analysis AS
SELECT 
    DATE(timestamp) as log_date,
    COUNT(*) as total_logs,
    COUNT(DISTINCT session_id) as unique_sessions,
    AVG(TIMESTAMPDIFF(MICROSECOND, LAG(timestamp) OVER (PARTITION BY session_id ORDER BY timestamp), timestamp)) as avg_time_between_logs_microseconds,
    COUNT(CASE WHEN level = 'ERROR' THEN 1 END) as error_count,
    COUNT(CASE WHEN level = 'WARNING' THEN 1 END) as warning_count
FROM debug_logs
GROUP BY DATE(timestamp)
ORDER BY log_date DESC;

-- =====================================================
-- EVENTOS AGENDADOS (CRON JOBS)
-- =====================================================

-- Habilitar event scheduler
SET GLOBAL event_scheduler = ON;

-- Evento para limpeza diária
CREATE EVENT IF NOT EXISTS daily_cleanup
ON SCHEDULE EVERY 1 DAY
STARTS TIMESTAMP(CURDATE() + INTERVAL 1 DAY, '02:00:00')
DO
BEGIN
    CALL CleanupOldLogs();
END;

-- Evento para atualização de métricas
CREATE EVENT IF NOT EXISTS daily_metrics_update
ON SCHEDULE EVERY 1 DAY
STARTS TIMESTAMP(CURDATE() + INTERVAL 1 DAY, '03:00:00')
DO
BEGIN
    CALL UpdateDailyMetrics(CURDATE() - INTERVAL 1 DAY);
END;

-- =====================================================
-- USUÁRIO E PERMISSÕES
-- =====================================================

-- Criar usuário específico para logging
CREATE USER IF NOT EXISTS 'rpa_logger'@'localhost' IDENTIFIED BY 'senha_super_segura_123!';

-- Conceder permissões necessárias
GRANT SELECT, INSERT, UPDATE, DELETE ON rpa_logs.* TO 'rpa_logger'@'localhost';
GRANT EXECUTE ON PROCEDURE rpa_logs.CleanupOldLogs TO 'rpa_logger'@'localhost';
GRANT EXECUTE ON PROCEDURE rpa_logs.UpdateDailyMetrics TO 'rpa_logger'@'localhost';

-- Aplicar mudanças
FLUSH PRIVILEGES;

-- =====================================================
-- DADOS DE TESTE (OPCIONAL)
-- =====================================================

-- Inserir alguns logs de teste para validação
INSERT INTO debug_logs (
    log_id, session_id, timestamp, client_timestamp, level, message, 
    data, url, user_agent, ip_address, server_time, request_id
) VALUES 
(
    'test_log_001',
    'test_session_001',
    NOW(3),
    NOW(3),
    'INFO',
    'Sistema de logging inicializado com sucesso',
    JSON_OBJECT('version', '1.0.0', 'environment', 'production'),
    'https://mdmidia.com.br/logging_system',
    'MySQL Setup Script',
    '127.0.0.1',
    UNIX_TIMESTAMP(NOW(6)),
    'setup_001'
),
(
    'test_log_002',
    'test_session_001',
    NOW(3),
    NOW(3),
    'DEBUG',
    'Banco de dados configurado corretamente',
    JSON_OBJECT('tables_created', 4, 'procedures_created', 2, 'triggers_created', 2),
    'https://mdmidia.com.br/logging_system',
    'MySQL Setup Script',
    '127.0.0.1',
    UNIX_TIMESTAMP(NOW(6)),
    'setup_002'
);

-- =====================================================
-- VERIFICAÇÃO FINAL
-- =====================================================

-- Verificar estrutura criada
SELECT 'TABELAS CRIADAS:' as info;
SHOW TABLES;

SELECT 'ÍNDICES CRIADOS:' as info;
SHOW INDEX FROM debug_logs;

SELECT 'PROCEDURES CRIADAS:' as info;
SHOW PROCEDURE STATUS WHERE Db = 'rpa_logs';

SELECT 'TRIGGERS CRIADOS:' as info;
SHOW TRIGGERS FROM rpa_logs;

SELECT 'EVENTOS CRIADOS:' as info;
SHOW EVENTS FROM rpa_logs;

SELECT 'CONFIGURAÇÕES:' as info;
SELECT * FROM config;

SELECT 'LOGS DE TESTE:' as info;
SELECT log_id, session_id, level, message, timestamp FROM debug_logs LIMIT 5;

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================
SELECT '✅ Banco de dados configurado com sucesso!' as status;



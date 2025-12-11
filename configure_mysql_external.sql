-- Configurar MySQL para conexões externas (MySQL 8.0+)
CREATE USER IF NOT EXISTS 'rpa_user'@'%' IDENTIFIED BY 'RpaLogs2025!';
GRANT ALL PRIVILEGES ON rpa_logs.* TO 'rpa_user'@'%';
FLUSH PRIVILEGES;

-- Verificar usuários criados
SELECT User, Host FROM mysql.user WHERE User = 'rpa_user';
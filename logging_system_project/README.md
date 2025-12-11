# 🚀 SISTEMA DE LOGGING PHP COM BANCO DE DADOS
## **PROJETO COMPLETO PARA MDMIDIA.COM.BR**

---

## 📋 **VISÃO GERAL**

Sistema completo de logging para análise profunda do fluxo de execução dos JavaScripts no projeto RPA Imediato Seguros, com foco na investigação do problema "RPA não executa no segurosimediato.com.br".

### **🎯 OBJETIVOS:**
- ✅ Logging estruturado em banco de dados MySQL
- ✅ Análise temporal precisa de fluxos de execução
- ✅ Correlação automática de logs por sessão
- ✅ Interface web para visualização e análise
- ✅ Segurança robusta contra ataques
- ✅ Performance otimizada para investigação

---

## 🏗️ **ARQUITETURA DO SISTEMA**

### **📊 Componentes:**
```
mdmidia.com.br/
├── 📁 logging_system/
│   ├── 📄 debug_logger_db.php          # Endpoint principal de logging
│   ├── 📄 config/database.php          # Configuração segura do banco
│   ├── 📄 config/security.php          # Configurações de segurança
│   ├── 📄 install/setup_database.sql   # Script de criação do banco
│   ├── 📄 viewer/log_viewer.php        # Interface web de visualização
│   ├── 📄 viewer/api/analytics.php     # API para análises
│   ├── 📄 utils/helpers.php            # Funções auxiliares
│   ├── 📄 utils/cleanup.php            # Limpeza automática de logs
│   └── 📄 docs/                        # Documentação completa
```

### **🔗 Fluxo de Dados:**
```
JavaScript (Footer Code/Injection) 
    ↓ POST JSON
debug_logger_db.php 
    ↓ INSERT
MySQL Database 
    ↓ SELECT
log_viewer.php (Interface Web)
```

---

## 🚀 **CARACTERÍSTICAS PRINCIPAIS**

### **✅ LOGGING ESTRUTURADO:**
- **Campos:** session_id, timestamp, level, message, data, url, user_agent, ip
- **Níveis:** DEBUG, INFO, WARNING, ERROR
- **Formato:** JSON estruturado para análise fácil
- **Correlação:** Por session_id para rastreamento completo

### **✅ ANÁLISE AVANÇADA:**
- **Temporal:** Análise de timing entre eventos
- **Correlação:** Identificação de padrões de falha
- **Estatística:** Métricas de performance e erro
- **Filtros:** Por URL, nível, data, sessão

### **✅ SEGURANÇA:**
- **Validação:** Entrada rigorosamente validada
- **Sanitização:** Proteção contra SQL injection
- **Rate Limiting:** Proteção contra spam
- **CORS:** Configuração segura para Webflow

### **✅ PERFORMANCE:**
- **Índices:** Otimizados para consultas frequentes
- **Prepared Statements:** Reutilização de queries
- **Connection Pooling:** Conexões eficientes
- **Cleanup:** Limpeza automática de logs antigos

---

## 📊 **SCHEMA DO BANCO DE DADOS**

### **🗄️ Tabela Principal:**
```sql
CREATE TABLE debug_logs (
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
    INDEX idx_log_id (log_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### **📈 Tabela de Métricas:**
```sql
CREATE TABLE log_metrics (
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
    
    UNIQUE KEY unique_date (date)
) ENGINE=InnoDB;
```

---

## 🔧 **INSTALAÇÃO E CONFIGURAÇÃO**

### **1. Preparação do Servidor:**
```bash
# Conectar via SSH
ssh mdmidiac@mdmidia.com.br

# Criar diretório do projeto
mkdir -p /home/mdmidiac/public_html/logging_system
cd /home/mdmidiac/public_html/logging_system
```

### **2. Configuração do Banco:**
```sql
-- Executar no MySQL
CREATE DATABASE rpa_logs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rpa_logger'@'localhost' IDENTIFIED BY 'senha_super_segura_123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON rpa_logs.* TO 'rpa_logger'@'localhost';
FLUSH PRIVILEGES;
```

### **3. Upload dos Arquivos:**
- Upload de todos os arquivos PHP
- Configurar permissões adequadas
- Testar conectividade

---

## 📱 **INTERFACE WEB**

### **🔍 Log Viewer:**
- **URL:** `https://mdmidia.com.br/logging_system/viewer/log_viewer.php`
- **Funcionalidades:**
  - Visualização em tempo real
  - Filtros avançados
  - Análise de sessões
  - Exportação de dados
  - Gráficos de performance

### **📊 Analytics API:**
- **Endpoint:** `https://mdmidia.com.br/logging_system/viewer/api/analytics.php`
- **Funcionalidades:**
  - Métricas de performance
  - Análise de erros
  - Correlação de eventos
  - Relatórios automáticos

---

## 🔒 **SEGURANÇA**

### **🛡️ Medidas Implementadas:**
- **Validação de entrada:** Todos os dados validados
- **Prepared statements:** Proteção contra SQL injection
- **Rate limiting:** Máximo 100 requests/minuto por IP
- **CORS seguro:** Apenas domínios autorizados
- **Logs de segurança:** Auditoria de acessos
- **Sanitização:** Limpeza de dados maliciosos

### **🔐 Configurações:**
- **Senhas:** Complexas e únicas
- **Permissões:** Mínimas necessárias
- **Backup:** Automático e criptografado
- **Monitoramento:** Alertas de segurança

---

## 📈 **ANÁLISES DISPONÍVEIS**

### **🔍 Para Investigação do RPA:**
1. **Fluxo Completo por Sessão**
2. **Análise de Timing entre Eventos**
3. **Identificação de Pontos de Falha**
4. **Correlação Footer Code + Injection**
5. **Análise de Performance**
6. **Detecção de Padrões de Erro**

### **📊 Métricas Automáticas:**
- Taxa de sucesso por URL
- Tempo médio de execução
- Frequência de erros
- Distribuição de logs por nível
- Análise de sessões únicas

---

## 🚀 **PRÓXIMOS PASSOS**

1. **Implementar** o sistema no servidor mdmidia
2. **Configurar** integração com Footer Code e Injection
3. **Testar** logging em ambiente de desenvolvimento
4. **Analisar** logs para identificar problema do RPA
5. **Otimizar** baseado nos resultados

---

## 📞 **SUPORTE**

Para dúvidas ou problemas:
- **Documentação:** `/docs/` completa
- **Logs de erro:** Sistema interno de logging
- **Monitoramento:** Interface web com métricas

---

**Status:** ✅ **PRONTO PARA IMPLEMENTAÇÃO**
**Versão:** 1.0.0
**Data:** Janeiro 2025




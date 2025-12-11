# RPA V2 - Sistema PHP Avançado

## 📋 Visão Geral

O **RPA V2** é um sistema PHP completo que executa o RPA modular com controle total de ambiente, logs detalhados e monitoramento em tempo real.

## 🚀 Características

### ✅ **Controle de Ambiente**
- Variáveis de ambiente controladas
- Validação de dependências
- Verificação de permissões
- Health check completo

### ✅ **Sistema de Logs**
- Logs estruturados por sessão
- Níveis: DEBUG, INFO, WARNING, ERROR
- Rotação automática por data
- Contexto detalhado

### ✅ **Execução Controlada**
- Processo em background
- Monitoramento de PID
- Timeout configurável
- Retry automático

### ✅ **Gerenciamento de Parâmetros**
- Arquivos temporários seguros
- Validação de entrada
- Template base configurável
- Limpeza automática

### ✅ **Monitoramento**
- Status em tempo real
- Verificação de estimativas
- Health check do sistema
- Métricas de performance

## 📁 Estrutura de Arquivos

```
executar_rpa_v2.php          # Sistema principal
test_rpa_v2.php             # Script de teste
README_RPA_V2.md            # Esta documentação
logs/                       # Diretório de logs
├── rpa_v2_YYYY-MM-DD.log  # Logs diários
├── rpa_execution_*.log     # Logs de execução
└── rpa_errors.log          # Logs de erro
temp/                       # Arquivos temporários
├── parametros_*.json       # Parâmetros temporários
├── progress_*.json         # Arquivos de progresso
└── json_compreensivo_*.json # Estimativas
```

## 🔧 Configuração

### **Variáveis de Ambiente**
```php
define('BASE_DIR', '/opt/imediatoseguros-rpa');
define('LOGS_DIR', BASE_DIR . '/logs');
define('TEMP_DIR', BASE_DIR . '/temp');
define('PYTHON_VENV', BASE_DIR . '/venv/bin/python');
define('DEFAULT_TIMEOUT', 300);
```

### **Ambiente Controlado**
```php
$environment = [
    'PATH' => '/opt/imediatoseguros-rpa/venv/bin:/usr/local/bin:/usr/bin:/bin',
    'PYTHONPATH' => '/opt/imediatoseguros-rpa',
    'DISPLAY' => ':99',
    'HOME' => '/opt/imediatoseguros-rpa',
    'USER' => 'www-data',
    'PWD' => '/opt/imediatoseguros-rpa'
];
```

## 📡 API Endpoints

### **1. Iniciar RPA**
```bash
POST /executar_rpa_v2.php
Content-Type: application/json

{
    "action": "start",
    "dados": {
        "placa": "FPG8D63",
        "marca": "TOYOTA",
        "modelo": "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
        "ano": "2009",
        "cep": "03317-000",
        "nome": "TESTE RPA V2",
        "cpf": "12345678901",
        "email": "teste@imediatoseguros.com.br",
        "celular": "11999999999"
    }
}
```

**Resposta:**
```json
{
    "success": true,
    "message": "RPA iniciado com sucesso",
    "session_id": "rpa_v2_20250110_143045_a1b2c3d4",
    "pid": 12345,
    "command": "python executar_rpa_modular_telas_1_a_5.py...",
    "timestamp": "2025-01-10 14:30:45"
}
```

### **2. Verificar Status**
```bash
POST /executar_rpa_v2.php
Content-Type: application/json

{
    "action": "status",
    "session_id": "rpa_v2_20250110_143045_a1b2c3d4"
}
```

**Resposta:**
```json
{
    "success": true,
    "data": {
        "etapa_atual": 5,
        "total_etapas": 5,
        "progresso": 100,
        "status": "concluido",
        "mensagem": "RPA executado com sucesso"
    },
    "has_estimates": true,
    "estimates_file": "json_compreensivo_tela_5_20250110_143045.json",
    "progress_file": "progress_rpa_v2_20250110_143045_a1b2c3d4.json",
    "session_id": "rpa_v2_20250110_143045_a1b2c3d4",
    "timestamp": "2025-01-10 14:35:00"
}
```

### **3. Parar RPA**
```bash
POST /executar_rpa_v2.php
Content-Type: application/json

{
    "action": "stop",
    "session_id": "rpa_v2_20250110_143045_a1b2c3d4"
}
```

### **4. Health Check**
```bash
POST /executar_rpa_v2.php
Content-Type: application/json

{
    "action": "health"
}
```

**Resposta:**
```json
{
    "success": true,
    "health": {
        "timestamp": "2025-01-10 14:30:45",
        "system": {
            "php_version": "8.1.0",
            "memory_usage": 2097152,
            "memory_limit": "256M",
            "disk_space": 1073741824
        },
        "environment": {
            "python_available": true,
            "rpa_script_available": true,
            "redis_available": true,
            "xvfb_available": true
        },
        "files": {
            "rpa_script_exists": true,
            "python_venv_exists": true,
            "logs_dir_writable": true,
            "temp_dir_writable": true
        }
    }
}
```

## 🧪 Testes

### **Executar Teste Completo**
```bash
php test_rpa_v2.php
```

### **Teste Manual com cURL**
```bash
# Health Check
curl -X POST http://localhost/executar_rpa_v2.php \
  -H "Content-Type: application/json" \
  -d '{"action": "health"}'

# Iniciar RPA
curl -X POST http://localhost/executar_rpa_v2.php \
  -H "Content-Type: application/json" \
  -d '{
    "action": "start",
    "dados": {
      "placa": "FPG8D63",
      "marca": "TOYOTA",
      "modelo": "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
      "ano": "2009"
    }
  }'
```

## 📊 Logs

### **Estrutura do Log**
```
[2025-01-10 14:30:45] [INFO] [SESSION:rpa_v2_20250110_143045_a1b2c3d4] Sistema RPA V2 inicializado {"session_id":"rpa_v2_20250110_143045_a1b2c3d4","timestamp":"2025-01-10 14:30:45","memory_usage":2097152}
[2025-01-10 14:30:46] [INFO] [SESSION:rpa_v2_20250110_143045_a1b2c3d4] Iniciando execução RPA {"placa":"FPG8D63","marca":"TOYOTA"}
[2025-01-10 14:30:47] [INFO] [SESSION:rpa_v2_20250110_143045_a1b2c3d4] Arquivo de parâmetros temporário criado {"file":"/opt/imediatoseguros-rpa/temp/parametros_rpa_v2_20250110_143045_a1b2c3d4.json","size":2048}
[2025-01-10 14:30:48] [INFO] [SESSION:rpa_v2_20250110_143045_a1b2c3d4] Executando comando RPA {"command":"python executar_rpa_modular_telas_1_a_5.py...","timeout":300}
[2025-01-10 14:30:49] [INFO] [SESSION:rpa_v2_20250110_143045_a1b2c3d4] Processo iniciado em background {"pid":12345,"log_file":"/opt/imediatoseguros-rpa/logs/rpa_execution_rpa_v2_20250110_143045_a1b2c3d4.log"}
```

### **Níveis de Log**
- **DEBUG**: Informações detalhadas para debug
- **INFO**: Eventos normais de execução
- **WARNING**: Avisos que não impedem a execução
- **ERROR**: Erros que podem afetar a execução

## 🔍 Troubleshooting

### **Problemas Comuns**

#### **1. Ambiente não válido**
```json
{
    "success": false,
    "error": "Ambiente inválido: Python virtual environment não encontrado"
}
```
**Solução:** Verificar se o venv existe em `/opt/imediatoseguros-rpa/venv/`

#### **2. Permissões insuficientes**
```json
{
    "success": false,
    "error": "Ambiente inválido: Diretório de logs não é gravável"
}
```
**Solução:** `chmod 755 /opt/imediatoseguros-rpa/logs`

#### **3. Processo não inicia**
```json
{
    "success": false,
    "error": "Processo RPA falhou ao iniciar"
}
```
**Solução:** Verificar logs de execução em `logs/rpa_execution_*.log`

### **Comandos de Diagnóstico**
```bash
# Verificar logs
tail -f /opt/imediatoseguros-rpa/logs/rpa_v2_$(date +%Y-%m-%d).log

# Verificar processos
ps aux | grep rpa_v2

# Verificar arquivos temporários
ls -la /opt/imediatoseguros-rpa/temp/

# Verificar permissões
ls -la /opt/imediatoseguros-rpa/logs/
ls -la /opt/imediatoseguros-rpa/temp/
```

## 🚀 Deploy

### **1. Upload dos arquivos**
```bash
scp executar_rpa_v2.php root@37.27.92.160:/opt/imediatoseguros-rpa/
scp test_rpa_v2.php root@37.27.92.160:/opt/imediatoseguros-rpa/
```

### **2. Configurar permissões**
```bash
chmod 755 /opt/imediatoseguros-rpa/executar_rpa_v2.php
chmod 755 /opt/imediatoseguros-rpa/test_rpa_v2.php
chmod 755 /opt/imediatoseguros-rpa/logs/
chmod 755 /opt/imediatoseguros-rpa/temp/
```

### **3. Testar**
```bash
cd /opt/imediatoseguros-rpa
php test_rpa_v2.php
```

## 📈 Monitoramento

### **Métricas Importantes**
- **Tempo de execução**: Monitorar timeout
- **Uso de memória**: Verificar limites
- **Taxa de sucesso**: RPA completado com estimativas
- **Logs de erro**: Identificar problemas recorrentes

### **Alertas Recomendados**
- Processo RPA não inicia
- Timeout de execução
- Erros de ambiente
- Falta de espaço em disco

## 🔄 Atualizações

### **Versão 2.0.0** (Atual)
- Sistema completo com controle de ambiente
- Logs estruturados
- Monitoramento em tempo real
- Health check
- Tratamento de erros robusto

### **Próximas Versões**
- **2.1.0**: Dashboard web
- **2.2.0**: Métricas avançadas
- **2.3.0**: Notificações automáticas
- **2.4.0**: API REST completa

---

**Desenvolvido por:** Assistente IA  
**Data:** 10 de Janeiro de 2025  
**Versão:** 2.0.0



























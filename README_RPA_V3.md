# RPA V3 - Sistema de Execução em Background com Systemd

## Visão Geral

A versão 3 do sistema RPA implementa execução em background confiável usando systemd, com monitoramento em tempo real e suporte a múltiplas sessões simultâneas.

## Arquitetura

### Componentes Principais

1. **executar_rpa_v3.php** - API REST principal
2. **scripts/start_rpa_v3.sh** - Script de inicialização
3. **scripts/monitor_rpa_v3.sh** - Script de monitoramento
4. **scripts/cleanup_rpa_v3.sh** - Script de limpeza
5. **Sistema systemd** - Gerenciamento de processos

### Estrutura de Diretórios

```
/opt/imediatoseguros-rpa/
├── sessions/                      # Sessões ativas
│   ├── {session_id}/
│   │   ├── config.json           # Configuração da sessão
│   │   ├── progress.json         # Progresso em tempo real
│   │   ├── status.json           # Status da execução
│   │   └── logs/                 # Logs da sessão
│   │       ├── rpa.log
│   │       └── progress.log
├── systemd/                      # Service units
│   └── rpa-session-{id}.service
├── scripts/                      # Scripts de controle
│   ├── start_rpa_v3.sh
│   ├── monitor_rpa_v3.sh
│   └── cleanup_rpa_v3.sh
└── executar_rpa_v3.php           # API principal
```

## Instalação

### 1. Preparar Diretórios

```bash
# Criar diretórios
sudo mkdir -p /opt/imediatoseguros-rpa/{sessions,systemd,scripts}
sudo chown -R www-data:www-data /opt/imediatoseguros-rpa
sudo chmod -R 755 /opt/imediatoseguros-rpa
```

### 2. Instalar Scripts

```bash
# Copiar scripts
sudo cp scripts/*.sh /opt/imediatoseguros-rpa/scripts/
sudo chmod +x /opt/imediatoseguros-rpa/scripts/*.sh
```

### 3. Configurar PHP

```bash
# Copiar API PHP
sudo cp executar_rpa_v3.php /var/www/rpaimediatoseguros.com.br/
sudo chown www-data:www-data /var/www/rpaimediatoseguros.com.br/executar_rpa_v3.php
```

### 4. Verificar Dependências

```bash
# Verificar Python e venv
ls -la /opt/imediatoseguros-rpa/venv/bin/python
ls -la /opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py

# Verificar xvfb
which xvfb-run
```

## API Endpoints

### 1. Iniciar RPA

**POST** `/executar_rpa_v3.php`

```json
{
    "cpf": "12345678901",
    "nome": "João da Silva",
    "data_nascimento": "1990-01-01",
    "sexo": "M",
    "estado_civil": "SOLTEIRO",
    "cep": "01234567",
    "endereco": "Rua Teste",
    "numero": "123",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "uf": "SP",
    "telefone": "11999999999",
    "email": "joao@teste.com",
    "veiculo_placa": "ABC1234",
    "veiculo_ano": "2020",
    "veiculo_combustivel": "FLEX"
}
```

**Resposta:**
```json
{
    "success": true,
    "session_id": "rpa_v3_20241229_143022_a1b2c3d4",
    "message": "RPA iniciado com sucesso",
    "timestamp": "2024-12-29 14:30:22"
}
```

### 2. Obter Status

**GET** `/executar_rpa_v3.php?action=status&session_id={session_id}`

**Resposta:**
```json
{
    "success": true,
    "data": {
        "session_id": "rpa_v3_20241229_143022_a1b2c3d4",
        "service_status": "active",
        "process_running": true,
        "pid": "12345",
        "progress": {
            "session_id": "rpa_v3_20241229_143022_a1b2c3d4",
            "etapa_atual": 3,
            "total_etapas": 5,
            "status": "executando",
            "mensagem": "Processando Tela 3",
            "timestamp": "2024-12-29T14:30:45+00:00",
            "percentual": 60
        },
        "status": {
            "session_id": "rpa_v3_20241229_143022_a1b2c3d4",
            "status": "running",
            "mensagem": "Executando RPA",
            "timestamp": "2024-12-29T14:30:22+00:00",
            "pid": "12345"
        },
        "logs": "Logs de progresso...",
        "rpa_logs": "Logs de execução...",
        "result_files": "arquivo1.json,arquivo2.json",
        "timestamp": "2024-12-29T14:30:45+00:00"
    }
}
```

### 3. Listar Sessões

**GET** `/executar_rpa_v3.php?action=sessions`

**Resposta:**
```json
{
    "success": true,
    "sessions": [
        {
            "session_id": "rpa_v3_20241229_143022_a1b2c3d4",
            "status": "running",
            "timestamp": "2024-12-29T14:30:22+00:00"
        }
    ],
    "timestamp": "2024-12-29 14:30:45"
}
```

### 4. Parar RPA

**DELETE** `/executar_rpa_v3.php?action=stop&session_id={session_id}`

**Resposta:**
```json
{
    "success": true,
    "message": "RPA parado com sucesso",
    "timestamp": "2024-12-29 14:35:22"
}
```

### 5. Health Check

**GET** `/executar_rpa_v3.php?action=health`

**Resposta:**
```json
{
    "success": true,
    "healthy": true,
    "checks": {
        "directories": {
            "sessions": true,
            "systemd": true,
            "scripts": true
        },
        "scripts": {
            "start_rpa_v3.sh": true,
            "monitor_rpa_v3.sh": true
        },
        "python": {
            "venv_exists": true,
            "python_executable": true,
            "modular_script": true
        },
        "systemd": {
            "running": true,
            "status": "running"
        }
    },
    "timestamp": "2024-12-29 14:30:22"
}
```

## Monitoramento

### 1. Status do Serviço

```bash
# Verificar status
systemctl status rpa-session-{session_id}

# Verificar logs
journalctl -u rpa-session-{session_id} -f
```

### 2. Arquivos de Progresso

```bash
# Progresso em tempo real
cat /opt/imediatoseguros-rpa/sessions/{session_id}/progress.json

# Status da execução
cat /opt/imediatoseguros-rpa/sessions/{session_id}/status.json

# Logs
tail -f /opt/imediatoseguros-rpa/sessions/{session_id}/logs/progress.log
tail -f /opt/imediatoseguros-rpa/sessions/{session_id}/logs/rpa.log
```

### 3. Limpeza Automática

```bash
# Limpeza manual
/opt/imediatoseguros-rpa/scripts/cleanup_rpa_v3.sh {session_id}

# Limpeza forçada
/opt/imediatoseguros-rpa/scripts/cleanup_rpa_v3.sh {session_id} force
```

## Testes

### 1. Teste Automático

```bash
# Executar teste completo
php test_rpa_v3.php
```

### 2. Teste Manual

```bash
# Health check
curl "http://localhost/executar_rpa_v3.php?action=health"

# Iniciar RPA
curl -X POST "http://localhost/executar_rpa_v3.php" \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678901","nome":"João da Silva","data_nascimento":"1990-01-01"}'

# Status
curl "http://localhost/executar_rpa_v3.php?action=status&session_id={session_id}"
```

## Vantagens da V3

### 1. Execução Confiável
- **Systemd**: Gerenciamento robusto de processos
- **Restart automático**: Recuperação de falhas
- **Logs centralizados**: Via journalctl

### 2. Monitoramento em Tempo Real
- **Status via systemd**: Estado do serviço
- **Progresso JSON**: Atualizações em tempo real
- **Logs estruturados**: Por sessão

### 3. Escalabilidade
- **Múltiplas sessões**: Execuções simultâneas
- **Isolamento**: Cada sessão independente
- **Limpeza automática**: Gerenciamento de recursos

### 4. Manutenibilidade
- **Scripts modulares**: Fácil manutenção
- **Logs estruturados**: Debug facilitado
- **API REST**: Integração simples

## Troubleshooting

### 1. Serviço não inicia

```bash
# Verificar logs
journalctl -u rpa-session-{session_id} -n 50

# Verificar permissões
ls -la /opt/imediatoseguros-rpa/sessions/{session_id}/

# Verificar Python
/opt/imediatoseguros-rpa/venv/bin/python --version
```

### 2. Processo não executa

```bash
# Verificar xvfb
xvfb-run -a echo "test"

# Verificar script modular
ls -la /opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py

# Testar execução manual
cd /opt/imediatoseguros-rpa
xvfb-run -a /opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --help
```

### 3. Arquivos não são gerados

```bash
# Verificar permissões de escrita
touch /opt/imediatoseguros-rpa/sessions/{session_id}/test.txt

# Verificar espaço em disco
df -h /opt/imediatoseguros-rpa

# Verificar logs de erro
grep -i error /opt/imediatoseguros-rpa/sessions/{session_id}/logs/rpa.log
```

## Logs e Debug

### 1. Logs do Sistema

```bash
# Logs do systemd
journalctl -u rpa-session-{session_id} -f

# Logs da aplicação
tail -f /opt/imediatoseguros-rpa/sessions/{session_id}/logs/rpa.log

# Logs de progresso
tail -f /opt/imediatoseguros-rpa/sessions/{session_id}/logs/progress.log
```

### 2. Debug de Problemas

```bash
# Verificar status completo
systemctl status rpa-session-{session_id} -l

# Verificar processos
ps aux | grep rpa-session

# Verificar arquivos abertos
lsof | grep rpa-session
```

## Manutenção

### 1. Limpeza Regular

```bash
# Limpeza automática (cron)
0 2 * * * /opt/imediatoseguros-rpa/scripts/cleanup_rpa_v3.sh

# Limpeza manual
find /opt/imediatoseguros-rpa/sessions -type d -mtime +7 -exec rm -rf {} \;
```

### 2. Monitoramento

```bash
# Verificar sessões ativas
ls -la /opt/imediatoseguros-rpa/sessions/

# Verificar serviços ativos
systemctl list-units --type=service | grep rpa-session

# Verificar uso de recursos
systemctl status rpa-session-* | grep -E "(Active|Main PID)"
```

## Conclusão

A versão 3 do sistema RPA oferece:

- ✅ **Execução confiável** em background via systemd
- ✅ **Monitoramento em tempo real** com JSON tracker
- ✅ **Suporte a múltiplas sessões** simultâneas
- ✅ **API REST completa** para controle
- ✅ **Logs estruturados** para debug
- ✅ **Limpeza automática** de recursos
- ✅ **Health check** do sistema
- ✅ **Escalabilidade** e manutenibilidade

**Status:** Implementação completa e pronta para produção.














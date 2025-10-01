# Testes API V4 - Progress Tracker

## Visão Geral
Scripts de teste para validar a execução do RPA via API V4 com captura de progresso em tempo real.

## Estrutura
```
tests/
├── scripts/
│   ├── test_prepare.sh      # Preparação do ambiente
│   ├── test_modular.sh      # Teste RPA Modular (5 telas)
│   ├── test_principal.sh    # Teste RPA Principal (15 telas)
│   ├── test_concurrent.sh   # Teste de execuções concorrentes
│   ├── test_validation.sh   # Validação de arquivos
│   ├── test_monitor.sh      # Monitoramento em tempo real
│   └── test_report.sh       # Geração de relatórios
├── config/
│   └── test_config.sh       # Configurações centralizadas
├── deploy_tests.sh          # Deploy para servidor Hetzner
├── run_all_tests.sh         # Execução completa dos testes
└── README.md
```

## Pré-requisitos
- Servidor Hetzner (ubuntu-2gb-hel1-1)
- Serviços ativos: nginx, php8.3-fpm, redis-server
- API V4 respondendo
- Comandos: curl, jq (ou python3)

## Execução

### 1. Preparação
```bash
cd tests/scripts
chmod +x *.sh
./test_prepare.sh
```

### 2. Teste RPA Modular
```bash
./test_modular.sh
```

### 3. Teste RPA Principal
```bash
./test_principal.sh
```

### 4. Teste Concorrente
```bash
./test_concurrent.sh
```

### 5. Validação
```bash
./test_validation.sh
```

### 6. Monitoramento em Tempo Real
```bash
# Monitorar sessão específica
./test_monitor.sh -s SESSION_ID

# Monitorar todas as sessões ativas
./test_monitor.sh -a

# Monitorar com intervalo personalizado
./test_monitor.sh -s SESSION_ID -i 5
```

### 7. Relatório de Testes
```bash
./test_report.sh
```

### 8. Execução Completa
```bash
# Executar todos os testes em sequência
./run_all_tests.sh
```

## Configurações
Edite `config/test_config.sh` para ajustar:
- URLs e endpoints
- Timeouts e intervalos
- Dados de teste
- Diretórios

## Logs
Os scripts geram logs coloridos:
- 🔵 [INFO] - Informações gerais
- 🟢 [SUCCESS] - Sucessos
- 🟡 [WARNING] - Avisos
- 🔴 [ERROR] - Erros

## Deploy para Servidor Hetzner
```bash
# Fazer deploy dos testes
./deploy_tests.sh

# Conectar ao servidor e executar
ssh root@37.27.92.160
cd /opt/imediatoseguros-rpa/tests/scripts
./test_prepare.sh
```

## Troubleshooting
- Verificar se está no servidor correto
- Verificar se os serviços estão ativos
- Verificar se a API está respondendo
- Verificar permissões de escrita
- Verificar implementação --data nos scripts Python
- Usar `test_monitor.sh` para debug em tempo real
- Gerar relatório com `test_report.sh` para análise

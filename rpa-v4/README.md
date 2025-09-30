# RPA V4 - Sistema de Automação Robótica de Processos

## Visão Geral

O RPA V4 é uma evolução incremental do sistema RPA existente, implementando uma arquitetura modular, logs estruturados, validação robusta e dashboard web em tempo real.

## Características

- ✅ **Arquitetura Modular**: Separação clara de responsabilidades
- ✅ **Logs Estruturados**: Sistema de logging com rotação automática
- ✅ **Validação Robusta**: Validação de entrada com regras customizáveis
- ✅ **Rate Limiting**: Proteção contra abuso com Redis
- ✅ **Dashboard Web**: Interface responsiva com atualização em tempo real
- ✅ **Health Checks**: Monitoramento do sistema
- ✅ **API REST**: Endpoints padronizados
- ✅ **Compatibilidade**: Mantém compatibilidade com RPA V3

## Estrutura do Projeto

```
rpa-v4/
├── src/
│   ├── Controllers/
│   │   └── RPAController.php
│   ├── Services/
│   │   ├── SessionService.php
│   │   ├── MonitorService.php
│   │   ├── ConfigService.php
│   │   ├── LoggerService.php
│   │   ├── ValidationService.php
│   │   └── RateLimitService.php
│   ├── Repositories/
│   │   └── SessionRepository.php
│   └── Interfaces/
│       ├── SessionServiceInterface.php
│       ├── MonitorServiceInterface.php
│       └── LoggerInterface.php
├── config/
│   └── app.php
├── public/
│   ├── index.php
│   ├── dashboard.html
│   └── js/
│       └── dashboard.js
├── logs/
│   └── rpa/
├── tests/
├── composer.json
└── README.md
```

## Instalação

### 1. Dependências

```bash
# Instalar dependências PHP
composer install

# Verificar extensões necessárias
php -m | grep -E "(json|curl|redis)"
```

### 2. Configuração

Edite o arquivo `config/app.php` conforme necessário:

```php
'rpa' => [
    'base_path' => '/opt/imediatoseguros-rpa',
    'sessions_path' => '/opt/imediatoseguros-rpa/sessions',
    'data_path' => '/opt/imediatoseguros-rpa/rpa_data',
    'scripts_path' => '/opt/imediatoseguros-rpa/scripts',
],
```

### 3. Permissões

```bash
# Criar diretórios necessários
sudo mkdir -p /opt/imediatoseguros-rpa/sessions
sudo mkdir -p /opt/imediatoseguros-rpa/rpa_data
sudo mkdir -p /opt/imediatoseguros-rpa/scripts
sudo mkdir -p /opt/imediatoseguros-rpa/logs

# Definir permissões
sudo chown -R www-data:www-data /opt/imediatoseguros-rpa
sudo chmod -R 755 /opt/imediatoseguros-rpa
```

### 4. Nginx Configuration

```nginx
server {
    listen 80;
    server_name rpa-v4.local;
    root /path/to/rpa-v4/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

## API Endpoints

### Iniciar RPA
```http
POST /api/rpa/start
Content-Type: application/json

{
    "cpf": "12345678901",
    "nome": "João da Silva",
    "email": "joao@email.com",
    "telefone": "11999999999"
}
```

### Status da Sessão
```http
GET /api/rpa/status/{session_id}
```

### Listar Sessões
```http
GET /api/rpa/sessions
```

### Monitorar Sessão
```http
GET /api/rpa/monitor/{session_id}
```

### Logs da Sessão
```http
GET /api/rpa/logs/{session_id}?limit=100
```

### Parar Sessão
```http
DELETE /api/rpa/stop/{session_id}
```

### Health Check
```http
GET /api/rpa/health
```

### Métricas
```http
GET /api/rpa/metrics
```

### Limpeza
```http
POST /api/rpa/cleanup
```

## Dashboard Web

Acesse `/dashboard.html` para usar a interface web:

- **Métricas em Tempo Real**: Total de sessões, ativas, taxa de sucesso
- **Lista de Sessões**: Status, progresso, timestamps
- **Logs em Tempo Real**: Logs das sessões selecionadas
- **Controles**: Iniciar nova sessão, parar sessões, health check
- **Atualização Automática**: Refresh a cada 5 segundos

## Validação

O sistema inclui validação robusta para:

- **CPF**: Validação de formato e dígitos verificadores
- **Nome**: Comprimento mínimo e máximo
- **Email**: Formato válido
- **Telefone**: Formato brasileiro

## Rate Limiting

- **Limite**: 100 requests por hora por IP
- **Backend**: Redis (opcional, fallback para permitir se indisponível)
- **Headers**: Inclui informações sobre limites restantes

## Logs

### Estrutura dos Logs
```json
{
    "timestamp": "2025-09-30 08:18:00",
    "level": "INFO",
    "message": "RPA session created successfully",
    "context": {
        "session_id": "rpa_v4_20250930_081800_abc123",
        "data": {...}
    },
    "memory": 1048576,
    "pid": 12345
}
```

### Níveis de Log
- **DEBUG**: Informações detalhadas (apenas em desenvolvimento)
- **INFO**: Informações gerais
- **WARNING**: Avisos
- **ERROR**: Erros

### Rotação Automática
- **Tamanho máximo**: 10MB por arquivo
- **Arquivos mantidos**: 30 arquivos
- **Compressão**: Automática

## Monitoramento

### Health Checks
- **Diretórios**: Verificação de existência e permissões
- **Processos Python**: Contagem de processos RPA ativos
- **Espaço em disco**: Uso de disco
- **Memória**: Uso de memória do sistema

### Métricas
- **Sessões**: Total, por status, últimas 24h
- **Performance**: Taxa de sucesso, tempo de execução
- **Sistema**: Uso de recursos

## Testes

```bash
# Executar testes
composer test

# Cobertura de testes
composer test-coverage
```

## Deploy

### 1. Backup
```bash
# Backup da versão atual
cp -r /opt/imediatoseguros-rpa /opt/imediatoseguros-rpa-backup-$(date +%Y%m%d_%H%M%S)
```

### 2. Atualização
```bash
# Atualizar código
cd /opt/imediatoseguros-rpa-v4
git pull origin main

# Instalar dependências
composer install --no-dev

# Executar testes
composer test
```

### 3. Reiniciar Serviços
```bash
# Reiniciar serviços
sudo systemctl reload nginx
sudo systemctl restart php8.1-fpm
```

## Compatibilidade

### RPA V3
- **Mantém compatibilidade**: RPA V3 continua funcionando
- **Migração gradual**: Substituição controlada
- **Rollback seguro**: Possibilidade de voltar ao V3

### Dependências
- **PHP**: 8.1+
- **Redis**: Opcional (para rate limiting)
- **Nginx**: Proxy reverso
- **Python**: Para execução do RPA

## Troubleshooting

### Problemas Comuns

1. **Erro de permissão**
   ```bash
   sudo chown -R www-data:www-data /opt/imediatoseguros-rpa
   sudo chmod -R 755 /opt/imediatoseguros-rpa
   ```

2. **Redis não disponível**
   - Rate limiting será desabilitado automaticamente
   - Sistema continua funcionando normalmente

3. **Logs não aparecem**
   - Verificar permissões do diretório de logs
   - Verificar configuração de logging

### Logs de Debug
```bash
# Verificar logs do sistema
tail -f /opt/imediatoseguros-rpa/logs/rpa/app.log

# Verificar logs do Nginx
tail -f /var/log/nginx/error.log

# Verificar logs do PHP
tail -f /var/log/php8.1-fpm.log
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é proprietário da Imediato Soluções em Seguros.

## Suporte

Para suporte técnico, entre em contato com a equipe de desenvolvimento.

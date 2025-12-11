# 🔍 DIAGNÓSTICO COMPLETO HETZNER - RPA IMEDIATO SEGUROS

## 📋 Descrição

Este conjunto de scripts foi criado para realizar um diagnóstico completo e abrangente do ambiente Hetzner, verificando todos os componentes necessários para o funcionamento do RPA.

## 🚀 Arquivos Incluídos

### 1. `diagnostico_completo_hetzner.py`
- **Função**: Script Python principal que executa todos os testes
- **Testa**: Sistema, Python, Redis, Nginx, PHP, RPA, API, Integração
- **Saída**: Relatório JSON detalhado

### 2. `executar_diagnostico_hetzner.sh`
- **Função**: Script bash que executa o diagnóstico Python + testes manuais
- **Inclui**: Verificações adicionais via comandos diretos
- **Saída**: Resultados no terminal

### 3. `teste_progress_tracker.py`
- **Função**: Teste específico do ProgressTracker
- **Foca**: Identificar problemas no sistema de progresso
- **Saída**: Relatório JSON específico

### 4. `upload_diagnostico_hetzner.sh`
- **Função**: Upload automático dos arquivos para o servidor
- **Configura**: Permissões e verifica upload
- **Saída**: Instruções para execução

## 🎯 Como Usar

### Opção 1: Upload e Execução Automática
```bash
# 1. Fazer upload dos arquivos
./upload_diagnostico_hetzner.sh

# 2. Conectar ao servidor
ssh root@37.27.92.160

# 3. Executar diagnóstico completo
cd /opt/imediatoseguros-rpa
./executar_diagnostico_hetzner.sh
```

### Opção 2: Execução Manual
```bash
# 1. Conectar ao servidor
ssh root@37.27.92.160

# 2. Navegar para o diretório
cd /opt/imediatoseguros-rpa

# 3. Executar diagnóstico Python
python3 diagnostico_completo_hetzner.py

# 4. Executar teste específico ProgressTracker
python3 teste_progress_tracker.py
```

## 📊 O que é Testado

### 🔍 Ambiente do Sistema
- Sistema operacional
- Espaço em disco
- Memória disponível
- Processos ativos (nginx, redis, php)

### 🐍 Ambiente Python
- Versão do Python
- Ambiente virtual
- Playwright instalado
- Dependências principais

### 🔴 Redis
- Status do serviço
- Chaves existentes
- Teste de escrita/leitura
- Conexão funcional

### 🌐 Nginx e PHP
- Status do Nginx
- Versão do PHP
- Arquivos PHP no diretório web
- Endpoints HTTP funcionais

### 🤖 Arquivos RPA
- Diretório do projeto
- Arquivo principal
- Parâmetros de configuração
- Diretórios temp/logs
- ProgressTracker

### 🚀 Execução RPA
- Comando help
- Comando version
- Inicialização básica
- Timeout e erros

### 🔗 API Endpoints
- executar_rpa.php
- get_progress.php
- Respostas HTTP
- JSON válido

### 🔄 Integração Completa
- Execução via API
- Dados no Redis
- Arquivos JSON
- Logs gerados
- Fluxo completo

## 📈 Interpretação dos Resultados

### ✅ Status OK
- Componente funcionando corretamente
- Nenhuma ação necessária

### ⚠️ Status AVISO
- Componente funcionando com limitações
- Pode afetar performance
- Monitorar

### ❌ Status ERRO
- Componente com falha crítica
- Ação imediata necessária
- Bloqueia funcionamento

## 🛠️ Solução de Problemas

### Redis não conecta
```bash
# Verificar status
systemctl status redis

# Reiniciar se necessário
systemctl restart redis
```

### Python/venv não funciona
```bash
# Ativar ambiente
cd /opt/imediatoseguros-rpa
source venv/bin/activate

# Verificar Python
which python
python --version
```

### Nginx/PHP não responde
```bash
# Verificar status
systemctl status nginx
systemctl status php8.3-fpm

# Reiniciar se necessário
systemctl restart nginx
systemctl restart php8.3-fpm
```

### RPA não executa
```bash
# Verificar arquivo
ls -la /opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py

# Testar execução
cd /opt/imediatoseguros-rpa
source venv/bin/activate
python executar_rpa_modular_telas_1_a_5.py --help
```

## 📋 Relatórios Gerados

### `diagnostico_hetzner_YYYYMMDD_HHMMSS.json`
- Relatório completo do diagnóstico Python
- Estrutura JSON detalhada
- Timestamps e status de cada teste

### `teste_progress_tracker_YYYYMMDD_HHMMSS.json`
- Relatório específico do ProgressTracker
- Testes de importação, criação, métodos
- Status de cada componente

## 🔧 Personalização

### Modificar servidor
Edite as variáveis no início dos scripts:
```bash
SERVER="37.27.92.160"
USER="root"
DEST_DIR="/opt/imediatoseguros-rpa"
```

### Adicionar testes
Modifique `diagnostico_completo_hetzner.py` para incluir novos testes:
```python
def testar_novo_componente(self):
    # Seu código de teste aqui
    pass
```

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs gerados
2. Execute os testes individuais
3. Consulte a documentação do projeto
4. Verifique a conectividade com o servidor

---

**AUTOR**: Assistente IA  
**DATA**: 2025-09-28  
**VERSÃO**: 1.0.0




























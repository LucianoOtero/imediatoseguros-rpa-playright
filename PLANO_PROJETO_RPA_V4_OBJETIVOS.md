# Plano de Projeto - RPA V4 - Objetivos e Especificações

## Objetivo Principal
Implementar sistema RPA V4 para execução de `executar_imediato_playwright.py` em sessões concorrentes em segundo plano, integrado ao website segurosimediato.com.br (Webflow) com monitoramento em tempo real via modal.

## Especificações Técnicas

### 1. Execução do RPA
**Arquivo Principal**: `executar_imediato_playwright.py`
- **Execução**: Sessões concorrentes em segundo plano
- **Parâmetros**: JSON passado via linha de comando
- **Ambiente**: Servidor Hetzner
- **Concorrência**: Múltiplas sessões simultâneas

### 2. Integração com Website
**Website**: segurosimediato.com.br
- **Plataforma**: Webflow
- **Integração**: Código JavaScript inserido
- **Comunicação**: API REST para iniciar sessões
- **Interface**: Modal para monitoramento

### 3. Monitoramento em Tempo Real
**Arquivo PHP**: Endpoint para status de execução
- **Fonte de Dados**: Arquivos JSON do progress tracker
- **Frequência**: Consulta periódica
- **Interface**: Modal no website

## Funcionalidades do Modal

### 1. Evolução da Execução (15 Telas)
**Objetivo**: Mostrar progresso passo-a-passo
- **Fonte**: Progress tracker JSON
- **Informações**:
  - Tela atual (1-15)
  - Percentual de conclusão
  - Status da execução
  - Mensagens de progresso
  - Timestamp de cada etapa

**Exemplo de Dados**:
```json
{
  "etapa_atual": 7,
  "total_etapas": 15,
  "percentual": 46.7,
  "status": "running",
  "mensagem": "Processando dados do veículo",
  "timestamp_atualizacao": "2025-09-30T20:15:30.123456"
}
```

### 2. Estimativa Inicial (Tela 4)
**Objetivo**: Mostrar estimativa quando disponível
- **Fonte**: Progress tracker JSON (tela 4)
- **Informações**:
  - Valores estimados
  - Coberturas disponíveis
  - Benefícios incluídos
  - Timestamp da captura

**Exemplo de Dados**:
```json
{
  "estimativas_tela_4": {
    "timestamp": "2025-09-30T20:10:15.789012",
    "coberturas_detalhadas": [
      {
        "nome_cobertura": "CompreensivaDe",
        "valores": {
          "de": "R$ 2.400,00",
          "ate": "R$ 2.900,00"
        },
        "beneficios": [...]
      }
    ],
    "resumo": {
      "total_coberturas": 3,
      "total_beneficios": 12,
      "valores_encontrados": 6
    }
  }
}
```

### 3. Cálculo Final (Tela 15)
**Objetivo**: Mostrar resultado final após execução completa
- **Fonte**: Progress tracker JSON (tela 15)
- **Informações**:
  - Valores finais
  - Coberturas selecionadas
  - Benefícios incluídos
  - Timestamp da conclusão

**Exemplo de Dados**:
```json
{
  "resultado_final_tela_15": {
    "timestamp": "2025-09-30T20:25:45.456789",
    "status": "completed",
    "valores_finais": {
      "premio_total": "R$ 2.650,00",
      "parcelamento": "12x sem juros"
    },
    "coberturas_selecionadas": [...],
    "beneficios_incluidos": [...]
  }
}
```

### 4. Tratamento de Erros
**Objetivo**: Mostrar erros de forma compreensível
- **Fonte**: Progress tracker JSON (erros)
- **Informações**:
  - Tipo de erro
  - Mensagem descritiva
  - Sugestões de correção
  - Timestamp do erro

**Exemplo de Dados**:
```json
{
  "erros": [
    {
      "tipo": "validacao_cpf",
      "mensagem": "CPF inválido ou não encontrado",
      "sugestao": "Verifique o CPF digitado",
      "timestamp": "2025-09-30T20:12:30.123456"
    }
  ]
}
```

## Arquitetura do Sistema

### 1. Frontend (Webflow + JavaScript)
**Localização**: segurosimediato.com.br
- **Modal**: Interface de monitoramento
- **JavaScript**: Comunicação com API
- **Polling**: Consulta periódica de status
- **UX**: Feedback visual em tempo real

### 2. Backend (PHP V4)
**Localização**: Servidor Hetzner
- **API REST**: Endpoints para gerenciamento
- **Session Management**: Controle de sessões
- **Progress Tracker**: Leitura de arquivos JSON
- **Monitoramento**: Status em tempo real

### 3. RPA Engine (Python)
**Arquivo**: `executar_imediato_playwright.py`
- **Execução**: 15 telas sequenciais
- **Progress Tracker**: Geração de JSONs
- **Concorrência**: Múltiplas sessões
- **Background**: Execução em segundo plano

## Fluxo de Execução

### 1. Inicialização
1. **Usuário** acessa segurosimediato.com.br
2. **JavaScript** coleta dados do formulário
3. **API Call** para `/api/rpa/start` com JSON
4. **PHP** cria sessão e inicia RPA
5. **Python** executa `executar_imediato_playwright.py`

### 2. Monitoramento
1. **Modal** abre automaticamente
2. **JavaScript** inicia polling (2 segundos)
3. **API Call** para `/api/rpa/progress/{session_id}`
4. **PHP** lê progress tracker JSON
5. **Modal** atualiza interface

### 3. Conclusão
1. **RPA** completa execução (Tela 15)
2. **Progress Tracker** marca como concluído
3. **Modal** mostra resultado final
4. **Usuário** visualiza estimativas/cálculo
5. **Sessão** é arquivada

## Endpoints da API

### 1. Iniciar Sessão
```
POST /api/rpa/start
Content-Type: application/json

{
  "cpf": "12345678901",
  "nome": "João Silva",
  "email": "joao@email.com",
  "placa": "ABC1234",
  "marca": "Toyota",
  "modelo": "Corolla",
  "ano": "2020",
  "cep": "01234567"
}
```

### 2. Status da Sessão
```
GET /api/rpa/progress/{session_id}

Resposta:
{
  "success": true,
  "session_id": "rpa_v4_20250930_201530_abc123",
  "progress": {
    "etapa_atual": 7,
    "total_etapas": 15,
    "percentual": 46.7,
    "status": "running",
    "mensagem": "Processando dados do veículo",
    "estimativas": {...},
    "erros": []
  }
}
```

### 3. Health Check
```
GET /api/rpa/health

Resposta:
{
  "status": "healthy",
  "timestamp": "2025-09-30T20:15:30.123456",
  "active_sessions": 3,
  "system_load": 0.45
}
```

## Implementação Técnica Detalhada

### 1. Sistema de Progress Tracker

#### 1.1 Arquitetura do Progress Tracker
**Classe Principal**: `DatabaseProgressTracker` (Python)
**Localização**: `/opt/imediatoseguros-rpa/utils/progress_database_json.py`

**Funcionamento**:
```python
class DatabaseProgressTracker:
    def __init__(self, total_etapas: int = 15, session_id: str = None):
        self.session_id = session_id or "default"
        self.etapa_atual = 0
        self.percentual = 0.0
        self.status = "iniciando"
        self.timestamp_inicio = datetime.now().isoformat()
        self.dados_extra = {}
        self.erros = []
        
        # Arquivos por sessão
        self.arquivo_progresso = f"rpa_data/progress_{self.session_id}.json"
        self.arquivo_historico = f"rpa_data/history_{self.session_id}.json"
        self.arquivo_resultado = f"rpa_data/result_{self.session_id}.json"
```

#### 1.2 Alimentação Incremental
**Método**: `update_progress()`
```python
def update_progress(self, etapa: int, mensagem: str = "", dados_extra: Dict[str, Any] = None):
    # Atualiza estado interno
    self.etapa_atual = min(etapa, self.total_etapas)
    self.percentual = (self.etapa_atual / self.total_etapas) * 100
    self.mensagem = mensagem or f"Etapa {etapa}"
    self.timestamp_atualizacao = datetime.now().isoformat()
    
    # Adiciona dados extras (estimativas, resultados)
    if dados_extra:
        self.dados_extra.update(dados_extra)
    
    # Salva incrementalmente
    self._salvar_progresso()      # Estado atual
    self._salvar_historico()      # Histórico completo
```

#### 1.3 Estrutura dos Arquivos JSON

**progress_{session_id}.json** (Estado Atual):
```json
{
  "etapa_atual": 7,
  "total_etapas": 15,
  "percentual": 46.7,
  "status": "running",
  "mensagem": "Processando dados do veículo",
  "timestamp_inicio": "2025-09-30T20:01:28.631422",
  "timestamp_atualizacao": "2025-09-30T20:01:42.960883",
  "dados_extra": {
    "estimativas_tela_4": {
      "coberturas_detalhadas": [...],
      "resumo": {...}
    }
  },
  "erros": [],
  "session_id": "rpa_v4_20250930_201530_abc123"
}
```

**history_{session_id}.json** (Histórico Incremental):
```json
{
  "session_id": "rpa_v4_20250930_201530_abc123",
  "timestamp_inicio": "2025-09-30T20:01:28.631422",
  "timestamp_fim": "2025-09-30T20:15:45.123456",
  "status_final": "success",
  "total_etapas": 15,
  "historico": [
    {
      "etapa": "inicio",
      "timestamp": "2025-09-30T20:01:28.631422",
      "status": "iniciando",
      "mensagem": "ProgressTracker inicializado",
      "dados_extra": null,
      "erro": null
    },
    {
      "etapa": 1,
      "timestamp": "2025-09-30T20:01:30.123456",
      "status": "executando",
      "mensagem": "Selecionando Tipo de Veiculo",
      "dados_extra": null,
      "erro": null
    },
    {
      "etapa": 4,
      "timestamp": "2025-09-30T20:05:15.789012",
      "status": "completed",
      "mensagem": "Estimativas capturadas",
      "dados_extra": {
        "estimativas_tela_4": {
          "coberturas_detalhadas": [...],
          "resumo": {...}
        }
      },
      "erro": null
    },
    {
      "etapa": 15,
      "timestamp": "2025-09-30T20:15:45.123456",
      "status": "success",
      "mensagem": "Execução concluída",
      "dados_extra": {
        "resultado_final": {...}
      },
      "erro": null
    }
  ]
}
```

### 2. Sistema get_progress_completo.php

#### 2.1 Arquitetura de Leitura
**Localização**: `get_progress_completo.php`
**Funcionamento**: Leitura inteligente de arquivos JSON

```php
// Detecção automática de arquivos
$history_file = "/opt/imediatoseguros-rpa/rpa_data/history_{$session_id}.json";
$progress_file = "/opt/imediatoseguros-rpa/rpa_data/progress_{$session_id}.json";

$use_history = file_exists($history_file);
$use_progress = file_exists($progress_file) && !$use_history;

// Prioridade: history > progress > status inicial
if ($use_history) {
    $data = processarHistorico($history_file, $session_id);
} else {
    $data = processarProgress($progress_file, $session_id);
}
```

#### 2.2 Processamento de Histórico
**Função**: `processarHistorico()`
```php
function processarHistorico($history_file, $session_id) {
    $content = file_get_contents($history_file);
    $history_data = json_decode($content, true);
    $historico = $history_data['historico'] ?? [];
    
    // Processa array incremental
    $processed = processarHistoricoArray($historico, $history_data);
    
    // Detecta estimativas (Tela 4)
    $estimativas_info = detectarEstimativas($historico);
    
    // Detecta resultados finais (Tela 15)
    $resultados_info = detectarResultadosFinais($historico);
    
    return [
        'etapa_atual' => $processed['current_etapa'],
        'total_etapas' => $history_data['total_etapas'] ?? 15,
        'percentual' => ($processed['current_etapa'] / 15) * 100,
        'status' => $processed['current_status'],
        'mensagem' => $processed['current_mensagem'],
        'estimativas' => [
            'capturadas' => $estimativas_info['estimativas_capturadas'],
            'dados' => $estimativas_info['estimativas_capturadas'] 
                ? extrairDadosEstimativas($estimativas_info['estimativas_entry'])
                : null
        ],
        'resultados_finais' => [
            'rpa_finalizado' => $resultados_info['rpa_finalizado'],
            'dados' => $resultados_info['rpa_finalizado'] 
                ? processarPlanos(lerResultadosFinais($session_id))
                : null
        ],
        'timeline' => array_slice($processed['timeline'], -10), // Últimas 10 entradas
        'source' => 'history'
    ];
}
```

#### 2.3 Detecção de Estimativas
**Função**: `detectarEstimativas()`
```php
function detectarEstimativas($historico) {
    $estimativas_entry = null;
    $execucao_posterior = false;
    
    // Busca entrada "estimativas" no histórico
    foreach ($historico as $index => $entry) {
        if ($entry['etapa'] === 'estimativas') {
            $estimativas_entry = $entry;
            break;
        }
    }
    
    // Verifica se há execução posterior (estimativas capturadas)
    if ($estimativas_entry !== null && count($historico) > $index + 1) {
        $execucao_posterior = true;
    }
    
    return [
        'estimativas_encontradas' => $estimativas_entry !== null,
        'estimativas_capturadas' => $execucao_posterior,
        'estimativas_entry' => $estimativas_entry
    ];
}
```

### 3. Execução Concorrente

#### 3.1 Arquitetura de Sessões
**Sistema**: Múltiplas sessões simultâneas
**Identificação**: Session ID único por execução

```php
// Geração de Session ID único
$session_id = 'rpa_v4_' . date('Ymd_His') . '_' . substr(md5(uniqid()), 0, 8);
// Exemplo: rpa_v4_20250930_201530_abc12345
```

#### 3.2 Fluxo de Execução Concorrente

**Passo 1: Inicialização (Website → API)**
```javascript
// JavaScript no Webflow
const sessionData = {
    cpf: "12345678901",
    nome: "João Silva",
    email: "joao@email.com",
    placa: "ABC1234",
    marca: "Toyota",
    modelo: "Corolla",
    ano: "2020",
    cep: "01234567"
};

// Chamada para API V4
fetch('http://37.27.92.160/api/rpa/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sessionData)
})
.then(response => response.json())
.then(data => {
    const sessionId = data.session_id;
    startMonitoring(sessionId);
});
```

**Passo 2: Criação de Sessão (API V4)**
```php
// RPAController.php
public function startRPA(array $data): array {
    // Validação de entrada
    $validation = $this->validationService->validate($data);
    
    // Criação de sessão única
    $sessionId = 'rpa_v4_' . date('Ymd_His') . '_' . substr(md5(uniqid()), 0, 8);
    
    // Armazenamento de sessão
    $this->sessionService->create($data, $sessionId);
    
    // Início do RPA em background
    $this->sessionService->startRPABackground($sessionId, $data);
    
    return [
        'success' => true,
        'session_id' => $sessionId,
        'message' => 'Sessão RPA criada com sucesso'
    ];
}
```

**Passo 3: Execução em Background (SessionService)**
```php
// SessionService.php
private function startRPABackground(string $sessionId, array $data): void {
    // Gera script específico para a sessão
    $scriptContent = $this->generateStartScript($sessionId, $data);
    $scriptPath = "/opt/imediatoseguros-rpa/scripts/start_rpa_v4_{$sessionId}.sh";
    
    file_put_contents($scriptPath, $scriptContent);
    chmod($scriptPath, 0755);
    
    // Executa em background (não bloqueia)
    $command = "nohup {$scriptPath} > /dev/null 2>&1 &";
    exec($command);
}

private function generateStartScript(string $sessionId, array $data): string {
    $dataJson = json_encode($data, JSON_UNESCAPED_UNICODE);
    
    return <<<SCRIPT
#!/bin/bash
SESSION_ID="{$sessionId}"
DATA='{$dataJson}'

# Log de início
echo "$(date): Iniciando RPA para sessão \$SESSION_ID" >> /opt/imediatoseguros-rpa/logs/rpa_v4_\$SESSION_ID.log

# Executar RPA com session ID específico
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python executar_imediato_playwright.py --data "\$DATA" --session \$SESSION_ID

# Verificar resultado
if [ \$? -eq 0 ]; then
    echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > /opt/imediatoseguros-rpa/sessions/\$SESSION_ID/status.json
else
    echo '{"status": "failed", "failed_at": "'$(date -Iseconds)'"}' > /opt/imediatoseguros-rpa/sessions/\$SESSION_ID/status.json
fi

# Limpar script temporário
rm -f "\$0"
SCRIPT;
}
```

**Passo 4: Execução do RPA Python**
```python
# executar_imediato_playwright.py
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, help='JSON data for RPA execution')
    parser.add_argument('--session', type=str, help='Session ID for concurrent execution')
    args = parser.parse_args()
    
    # Inicializa Progress Tracker com session ID
    progress_tracker = DatabaseProgressTracker(
        total_etapas=15,
        session_id=args.session
    )
    
    # Processa dados JSON
    if args.data:
        data = json.loads(args.data)
    else:
        # Fallback para parametros.json
        with open('parametros.json', 'r') as f:
            data = json.load(f)
    
    # Execução das 15 telas
    for tela in range(1, 16):
        progress_tracker.update_progress(tela, f"Processando Tela {tela}")
        
        if tela == 4:
            # Captura estimativas
            estimativas = capturar_estimativas()
            progress_tracker.update_progress(
                tela, 
                "Estimativas capturadas",
                dados_extra={'estimativas_tela_4': estimativas}
            )
        
        if tela == 15:
            # Resultado final
            resultado = processar_resultado_final()
            progress_tracker.update_progress(
                tela,
                "Execução concluída",
                dados_extra={'resultado_final': resultado}
            )
```

#### 3.3 Monitoramento em Tempo Real

**Passo 5: Polling do Website**
```javascript
// JavaScript no Webflow
function startMonitoring(sessionId) {
    const modal = document.getElementById('rpa-modal');
    modal.style.display = 'block';
    
    // Polling a cada 2 segundos
    const interval = setInterval(() => {
        fetch(`http://37.27.92.160/api/rpa/progress/${sessionId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateModal(data.data);
                
                // Para polling quando concluído
                if (data.data.status === 'completed' || data.data.status === 'success') {
                    clearInterval(interval);
                }
            }
        })
        .catch(error => {
            console.error('Erro ao obter progresso:', error);
        });
    }, 2000);
}

function updateModal(progressData) {
    // Atualiza barra de progresso
    document.getElementById('progress-bar').style.width = progressData.percentual + '%';
    document.getElementById('progress-text').textContent = progressData.mensagem;
    
    // Mostra estimativas quando disponíveis
    if (progressData.estimativas && progressData.estimativas.capturadas) {
        displayEstimativas(progressData.estimativas.dados);
    }
    
    // Mostra resultado final quando disponível
    if (progressData.resultados_finais && progressData.resultados_finais.rpa_finalizado) {
        displayResultadoFinal(progressData.resultados_finais.dados);
    }
}
```

**Passo 6: API de Progress (V4)**
```php
// RPAController.php
public function getProgress(string $sessionId): array {
    try {
        // Usa get_progress_completo.php como base
        $progressData = $this->monitorService->getProgress($sessionId);
        
        return [
            'success' => true,
            'session_id' => $sessionId,
            'progress' => $progressData
        ];
        
    } catch (Exception $e) {
        return [
            'success' => false,
            'error' => $e->getMessage()
        ];
    }
}

// MonitorService.php
public function getProgress(string $sessionId): array {
    // Chama get_progress_completo.php internamente
    $url = "http://localhost/get_progress_completo.php?session={$sessionId}";
    $response = file_get_contents($url);
    $data = json_decode($response, true);
    
    if ($data['success']) {
        return $data['data'];
    } else {
        throw new Exception($data['message']);
    }
}
```

### 4. Fluxo Completo de Execução Concorrente

#### 4.1 Cenário: 3 Usuários Simultâneos

**Usuário 1** (Session: `rpa_v4_20250930_201530_abc123`):
- Website → API V4 → RPA Python → Progress Tracker → get_progress

**Usuário 2** (Session: `rpa_v4_20250930_201535_def456`):
- Website → API V4 → RPA Python → Progress Tracker → get_progress

**Usuário 3** (Session: `rpa_v4_20250930_201540_ghi789`):
- Website → API V4 → RPA Python → Progress Tracker → get_progress

#### 4.2 Arquivos Gerados por Sessão
```
/opt/imediatoseguros-rpa/rpa_data/
├── progress_rpa_v4_20250930_201530_abc123.json
├── history_rpa_v4_20250930_201530_abc123.json
├── result_rpa_v4_20250930_201530_abc123.json
├── progress_rpa_v4_20250930_201535_def456.json
├── history_rpa_v4_20250930_201535_def456.json
├── result_rpa_v4_20250930_201535_def456.json
├── progress_rpa_v4_20250930_201540_ghi789.json
├── history_rpa_v4_20250930_201540_ghi789.json
└── result_rpa_v4_20250930_201540_ghi789.json
```

#### 4.3 Isolamento de Sessões
- **Session ID único** por execução
- **Arquivos separados** por sessão
- **Progress Tracker independente** por sessão
- **Logs separados** por sessão
- **Status independente** por sessão

### 5. Vantagens da Arquitetura

#### 5.1 Escalabilidade
- **Múltiplas sessões** simultâneas
- **Isolamento completo** entre execuções
- **Recursos compartilhados** (Python, Playwright)
- **Monitoramento independente** por sessão

#### 5.2 Confiabilidade
- **Progress Tracker robusto** com histórico
- **Recuperação de falhas** por sessão
- **Logs detalhados** para debugging
- **Status em tempo real** via polling

#### 5.3 Performance
- **Execução em background** não bloqueia API
- **Polling eficiente** (2 segundos)
- **Cache de progresso** em arquivos JSON
- **Processamento incremental** de dados

### 6. Modificações no RPA Principal

#### 6.1 Suporte a JSON Dinâmico
**Arquivo**: `executar_imediato_playwright.py`
```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, help='JSON data for RPA execution')
    parser.add_argument('--session', type=str, help='Session ID for concurrent execution')
    args = parser.parse_args()
    
    # Processa dados JSON
    if args.data:
        data = json.loads(args.data)
        # Usa dados dinâmicos do website
    else:
        # Fallback para parametros.json
        with open('parametros.json', 'r') as f:
            data = json.load(f)
    
    # Inicializa Progress Tracker com session ID
    progress_tracker = DatabaseProgressTracker(
        total_etapas=15,
        session_id=args.session
    )
    
    # Execução das 15 telas com progress tracking
    for tela in range(1, 16):
        progress_tracker.update_progress(tela, f"Processando Tela {tela}")
        
        # Lógica específica por tela
        if tela == 4:
            estimativas = capturar_estimativas()
            progress_tracker.update_progress(
                tela, 
                "Estimativas capturadas",
                dados_extra={'estimativas_tela_4': estimativas}
            )
        
        if tela == 15:
            resultado = processar_resultado_final()
            progress_tracker.update_progress(
                tela,
                "Execução concluída",
                dados_extra={'resultado_final': resultado}
            )
```

#### 6.2 Integração com Progress Tracker
- **Session ID obrigatório** para execução concorrente
- **Progress tracking** em cada tela
- **Captura de estimativas** na Tela 4
- **Resultado final** na Tela 15
- **Tratamento de erros** por sessão

### 7. API PHP V4

#### 7.1 SessionService
**Arquivo**: `rpa-v4/src/Services/SessionService.php`
```php
class SessionService implements SessionServiceInterface {
    public function create(array $data): array {
        $sessionId = $this->generateSessionId();
        
        // Armazena dados da sessão
        $this->repository->createSession($sessionId, $data);
        
        // Inicia RPA em background
        $this->startRPABackground($sessionId, $data);
        
        return [
            'success' => true,
            'session_id' => $sessionId,
            'message' => 'Sessão RPA criada com sucesso'
        ];
    }
    
    private function generateSessionId(): string {
        return 'rpa_v4_' . date('Ymd_His') . '_' . substr(md5(uniqid()), 0, 8);
    }
}
```

#### 7.2 MonitorService
**Arquivo**: `rpa-v4/src/Services/MonitorService.php`
```php
class MonitorService implements MonitorServiceInterface {
    public function getProgress(string $sessionId): array {
        // Usa get_progress_completo.php como base
        $url = "http://localhost/get_progress_completo.php?session={$sessionId}";
        $response = file_get_contents($url);
        $data = json_decode($response, true);
        
        if ($data['success']) {
            return $data['data'];
        } else {
            throw new Exception($data['message']);
        }
    }
}
```

### 8. JavaScript para Webflow

#### 8.1 Integração com Website
**Arquivo**: `webflow-integration.js`
```javascript
class RPAWebflowIntegration {
    constructor() {
        this.apiBaseUrl = 'http://37.27.92.160/api/rpa';
        this.currentSessionId = null;
        this.pollingInterval = null;
    }
    
    async startRPA(formData) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentSessionId = data.session_id;
                this.showModal();
                this.startPolling();
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError('Erro de comunicação com o servidor');
        }
    }
    
    startPolling() {
        this.pollingInterval = setInterval(async () => {
            try {
                const response = await fetch(`${this.apiBaseUrl}/progress/${this.currentSessionId}`);
                const data = await response.json();
                
                if (data.success) {
                    this.updateModal(data.progress);
                    
                    // Para polling quando concluído
                    if (data.progress.status === 'completed' || data.progress.status === 'success') {
                        this.stopPolling();
                    }
                }
            } catch (error) {
                console.error('Erro ao obter progresso:', error);
            }
        }, 2000);
    }
    
    updateModal(progressData) {
        // Atualiza barra de progresso
        document.getElementById('progress-bar').style.width = progressData.percentual + '%';
        document.getElementById('progress-text').textContent = progressData.mensagem;
        
        // Mostra estimativas quando disponíveis
        if (progressData.estimativas && progressData.estimativas.capturadas) {
            this.displayEstimativas(progressData.estimativas.dados);
        }
        
        // Mostra resultado final quando disponível
        if (progressData.resultados_finais && progressData.resultados_finais.rpa_finalizado) {
            this.displayResultadoFinal(progressData.resultados_finais.dados);
        }
    }
}
```

## Resumo da Arquitetura

### Como o get_progress Obtém o Progresso da Sessão

1. **Identificação da Sessão**: O `get_progress_completo.php` recebe o `session_id` via parâmetro GET
2. **Detecção de Arquivos**: Verifica se existe `history_{session_id}.json` ou `progress_{session_id}.json`
3. **Prioridade de Leitura**: 
   - Se `history_{session_id}.json` existe → usa histórico completo
   - Se não existe, mas `progress_{session_id}.json` existe → usa progresso atual
   - Se nenhum existe → retorna status inicial
4. **Processamento Incremental**: Lê o array `historico` que foi alimentado incrementalmente pelo RPA Python
5. **Detecção de Dados**: Identifica estimativas (Tela 4) e resultados finais (Tela 15) no histórico
6. **Retorno Estruturado**: Retorna JSON com progresso, estimativas, resultados e timeline

### Como a Execução Concorrente Funciona

1. **Múltiplas Sessões**: Cada usuário no website gera um `session_id` único
2. **Isolamento Completo**: Cada sessão tem seus próprios arquivos JSON e logs
3. **Execução em Background**: O RPA Python roda em segundo plano via `nohup`
4. **Progress Tracker Independente**: Cada sessão tem seu próprio `DatabaseProgressTracker`
5. **Monitoramento Paralelo**: O website faz polling independente para cada sessão
6. **Recursos Compartilhados**: Python, Playwright e sistema de arquivos são compartilhados

### Vantagens da V4

- **Escalabilidade**: Suporta múltiplas sessões simultâneas
- **Confiabilidade**: Progress tracker robusto com histórico completo
- **Performance**: Execução em background não bloqueia a API
- **Monitoramento**: Feedback em tempo real via polling
- **Isolamento**: Cada sessão é independente e isolada
- **Flexibilidade**: Suporte a JSON dinâmico do website

## Testes Necessários

### 1. Testes Unitários
- Validação de entrada
- Geração de sessões
- Leitura de progress tracker
- Tratamento de erros

### 2. Testes de Integração
- API REST completa
- Comunicação Webflow ↔ Hetzner
- Execução do RPA
- Monitoramento em tempo real

### 3. Testes de Carga
- Múltiplas sessões simultâneas
- Performance do sistema
- Estabilidade em 24h
- Recuperação de falhas

## Cronograma de Implementação

### Fase 1: Preparação (Semana 1)
- Análise do `executar_imediato_playwright.py`
- Modificação para suporte JSON
- Implementação de progress tracker
- Testes básicos

### Fase 2: API Backend (Semana 2)
- Endpoints REST completos
- Session management
- Progress tracker reading
- Validação de entrada

### Fase 3: Integração Webflow (Semana 3)
- JavaScript para modal
- Comunicação com API
- Polling em tempo real
- Interface de usuário

### Fase 4: Testes e Deploy (Semana 4)
- Testes integrados
- Testes de carga
- Ajustes finais
- Deploy em produção

## Critérios de Sucesso

### Funcionalidades
- ✅ Execução de 15 telas funcionando
- ✅ Sessões concorrentes estáveis
- ✅ Modal com monitoramento em tempo real
- ✅ Estimativas capturadas (Tela 4)
- ✅ Cálculo final exibido (Tela 15)
- ✅ Erros tratados adequadamente

### Performance
- ✅ Tempo de execução < 5 minutos
- ✅ Suporte a 10+ sessões simultâneas
- ✅ Tempo de resposta API < 2 segundos
- ✅ Polling eficiente (2 segundos)

### Estabilidade
- ✅ Uptime 99.9%
- ✅ Recuperação automática de falhas
- ✅ Logs estruturados
- ✅ Monitoramento ativo

## Riscos e Mitigações

### Riscos Técnicos
- **Risco**: Instabilidade do RPA principal
- **Mitigação**: Testes extensivos e rollback

- **Risco**: Performance com múltiplas sessões
- **Mitigação**: Otimizações e monitoramento

- **Risco**: Integração Webflow complexa
- **Mitigação**: Desenvolvimento incremental

### Riscos de Negócio
- **Risco**: Experiência do usuário ruim
- **Mitigação**: UX cuidadosamente planejada

- **Risco**: Falhas durante execução
- **Mitigação**: Tratamento robusto de erros

## Próximos Passos Imediatos

### 1. Análise do RPA Principal
- Examinar `executar_imediato_playwright.py`
- Identificar pontos de modificação
- Planejar suporte a JSON
- Implementar progress tracker

### 2. Modificação da API V4
- Atualizar SessionService para JSON
- Implementar MonitorService
- Criar endpoints de progress
- Testes de integração

### 3. Desenvolvimento do Modal
- Criar interface JavaScript
- Implementar polling
- Design responsivo
- Testes de UX

## Conclusão

Este plano estabelece os objetivos claros para implementar o sistema RPA V4 integrado ao website segurosimediato.com.br, com monitoramento em tempo real via modal. A abordagem incremental permite testar cada componente antes da integração completa, garantindo estabilidade e performance.

**Objetivo Final**: Sistema completo funcionando em produção com 15 telas, sessões concorrentes, monitoramento em tempo real e integração perfeita com o website Webflow.

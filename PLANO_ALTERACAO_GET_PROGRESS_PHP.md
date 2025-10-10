# PLANO: ALTERAÇÃO DO GET_PROGRESS.PHP PARA USAR HISTÓRICO SEQUENCIAL

## **Análise Atual do get_progress.php**

### **Estrutura Atual:**
- **Arquivo:** `/var/www/rpaimediatoseguros.com.br/get_progress.php`
- **Função:** Lê `progress_{session_id}.json` e retorna estado atual
- **Resposta:** JSON com dados do progresso atual

### **Limitações Identificadas:**
1. **Apenas estado atual:** Não mostra histórico de execução
2. **Sem rastreabilidade:** Não permite ver o que aconteceu em cada etapa
3. **Sem timeline:** Não mostra quando cada etapa foi executada
4. **Dados limitados:** Só mostra o último estado, não o processo

## **Análise do Novo Histórico Sequencial**

### **Estrutura do history_{session_id}.json:**
```json
{
  "session_id": "teste_historico_real_001",
  "timestamp_inicio": "2025-09-29T18:06:46.696914",
  "timestamp_fim": "2025-09-29T18:07:00.997393",
  "status_final": "success",
  "total_etapas": 5,
  "historico": [
    {
      "etapa": "inicio",
      "timestamp": "2025-09-29T18:06:46.697141",
      "status": "iniciando",
      "mensagem": "ProgressTracker inicializado",
      "dados_extra": null,
      "erro": null
    },
    // ... mais entradas sequenciais
  ]
}
```

### **Vantagens do Histórico:**
1. **Rastreabilidade completa:** Cada etapa com timestamp
2. **Timeline detalhada:** Quando cada ação aconteceu
3. **Dados ricos:** Estimativas, erros, status intermediários
4. **Debug facilitado:** Possibilidade de identificar onde falhou

## **Plano de Alteração**

### **Objetivo:**
Modificar `get_progress.php` para usar o histórico sequencial, mantendo compatibilidade com o frontend atual.

### **Estratégia:**
1. **Manter compatibilidade:** Resposta atual preservada
2. **Adicionar histórico:** Novo campo `historico` na resposta
3. **Fallback inteligente:** Usar `progress_*.json` se `history_*.json` não existir
4. **Parâmetros opcionais:** Permitir diferentes modos de resposta

## **Implementação Detalhada**

### **Fase 1: Estrutura Base (1 dia)**

#### **1.1 Parâmetros de Entrada**
```php
// Novos parâmetros opcionais
$mode = $_GET['mode'] ?? 'current'; // 'current', 'history', 'both'
$include_history = $_GET['include_history'] ?? 'true';
$history_limit = (int)($_GET['history_limit'] ?? 50); // Limite de entradas
```

#### **1.2 Detecção de Arquivos**
```php
// Priorizar histórico, fallback para progress
$history_file = "/opt/imediatoseguros-rpa/rpa_data/history_{$session_id}.json";
$progress_file = "/opt/imediatoseguros-rpa/rpa_data/progress_{$session_id}.json";

$use_history = file_exists($history_file);
$use_progress = file_exists($progress_file) && !$use_history;
```

#### **1.3 Estrutura de Resposta**
```php
$response = [
    'success' => true,
    'data' => [
        // Dados atuais (compatibilidade)
        'etapa_atual' => $current_etapa,
        'total_etapas' => $total_etapas,
        'percentual' => $percentual,
        'status' => $status,
        'mensagem' => $mensagem,
        'timestamp_inicio' => $timestamp_inicio,
        'timestamp_atualizacao' => $timestamp_atualizacao,
        'dados_extra' => $dados_extra,
        'erros' => $erros,
        'session_id' => $session_id,
        
        // NOVO: Histórico sequencial
        'historico' => $historico_array,
        'historico_count' => count($historico_array),
        'timeline' => $timeline_summary,
        
        // Metadados
        'source' => $use_history ? 'history' : 'progress',
        'file_used' => basename($use_history ? $history_file : $progress_file)
    ],
    'timestamp' => date('Y-m-d H:i:s')
];
```

### **Fase 2: Lógica de Processamento (2 dias)**

#### **2.1 Processamento do Histórico**
```php
function processHistory($history_data) {
    $historico = $history_data['historico'] ?? [];
    $timeline = [];
    $current_status = 'waiting';
    $current_etapa = 0;
    $dados_extra = [];
    $erros = [];
    
    // Processar cada entrada do histórico
    foreach ($historico as $entry) {
        $timeline[] = [
            'etapa' => $entry['etapa'],
            'timestamp' => $entry['timestamp'],
            'status' => $entry['status'],
            'mensagem' => $entry['mensagem'],
            'tempo_decorrido' => calculateElapsedTime($entry['timestamp'])
        ];
        
        // Atualizar estado atual
        if ($entry['status'] === 'completed' || $entry['status'] === 'success') {
            $current_status = $entry['status'];
            $current_etapa = is_numeric($entry['etapa']) ? $entry['etapa'] : $current_etapa;
        }
        
        // Coletar dados extras
        if ($entry['dados_extra']) {
            $dados_extra = array_merge($dados_extra, $entry['dados_extra']);
        }
        
        // Coletar erros
        if ($entry['erro']) {
            $erros[] = [
                'etapa' => $entry['etapa'],
                'erro' => $entry['erro'],
                'timestamp' => $entry['timestamp']
            ];
        }
    }
    
    return [
        'historico' => $historico,
        'timeline' => $timeline,
        'current_status' => $current_status,
        'current_etapa' => $current_etapa,
        'dados_extra' => $dados_extra,
        'erros' => $erros
    ];
}
```

#### **2.2 Processamento do Progress (Fallback)**
```php
function processProgress($progress_data) {
    // Manter lógica atual para compatibilidade
    return [
        'historico' => [], // Vazio para progress
        'timeline' => [],
        'current_status' => $progress_data['status'] ?? 'waiting',
        'current_etapa' => $progress_data['etapa_atual'] ?? 0,
        'dados_extra' => $progress_data['dados_extra'] ?? [],
        'erros' => $progress_data['erros'] ?? []
    ];
}
```

#### **2.3 Funções Auxiliares**
```php
function calculateElapsedTime($timestamp) {
    $start = new DateTime($GLOBALS['session_start_time']);
    $current = new DateTime($timestamp);
    return $current->diff($start)->format('%H:%I:%S');
}

function formatTimeline($timeline) {
    $summary = [];
    foreach ($timeline as $entry) {
        $summary[] = sprintf(
            "[%s] %s: %s",
            $entry['tempo_decorrido'],
            $entry['etapa'],
            $entry['mensagem']
        );
    }
    return $summary;
}
```

### **Fase 3: Modos de Resposta (1 dia)**

#### **3.1 Modo 'current' (Padrão)**
```php
// Resposta atual + histórico básico
$response['data']['historico'] = array_slice($processed['historico'], -10); // Últimas 10
$response['data']['timeline'] = array_slice($processed['timeline'], -10);
```

#### **3.2 Modo 'history'**
```php
// Apenas histórico completo
$response['data'] = [
    'historico' => $processed['historico'],
    'timeline' => $processed['timeline'],
    'session_id' => $session_id,
    'timestamp_inicio' => $history_data['timestamp_inicio'],
    'timestamp_fim' => $history_data['timestamp_fim'],
    'status_final' => $history_data['status_final']
];
```

#### **3.3 Modo 'both'**
```php
// Dados atuais + histórico completo
$response['data']['historico'] = $processed['historico'];
$response['data']['timeline'] = $processed['timeline'];
$response['data']['historico_count'] = count($processed['historico']);
```

### **Fase 4: Otimizações e Tratamento de Erros (1 dia)**

#### **4.1 Cache e Performance**
```php
// Cache simples para sessões ativas
$cache_key = "progress_{$session_id}";
$cache_time = 5; // 5 segundos

if (apcu_exists($cache_key)) {
    $cached_data = apcu_fetch($cache_key);
    if (time() - $cached_data['timestamp'] < $cache_time) {
        echo json_encode($cached_data['data']);
        exit();
    }
}

// Salvar no cache após processamento
apcu_store($cache_key, [
    'data' => $response,
    'timestamp' => time()
], $cache_time);
```

#### **4.2 Tratamento de Erros Robusto**
```php
try {
    // Processamento principal
} catch (JsonException $e) {
    // Erro de JSON
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Erro ao processar dados JSON',
        'error' => $e->getMessage(),
        'file' => basename($file_used)
    ]);
} catch (Exception $e) {
    // Erro geral
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Erro interno do servidor',
        'error' => $e->getMessage()
    ]);
}
```

#### **4.3 Validação de Dados**
```php
function validateHistoryData($data) {
    $required_fields = ['session_id', 'timestamp_inicio', 'historico'];
    foreach ($required_fields as $field) {
        if (!isset($data[$field])) {
            throw new Exception("Campo obrigatório ausente: {$field}");
        }
    }
    
    if (!is_array($data['historico'])) {
        throw new Exception("Histórico deve ser um array");
    }
    
    return true;
}
```

## **Estrutura da Nova Resposta**

### **Resposta Padrão (modo 'current'):**
```json
{
  "success": true,
  "data": {
    "etapa_atual": 5,
    "total_etapas": 5,
    "percentual": 100.0,
    "status": "success",
    "mensagem": "Tela Zero KM concluída",
    "timestamp_inicio": "2025-09-29T18:06:46.696914",
    "timestamp_atualizacao": "2025-09-29T18:07:00.997393",
    "dados_extra": {
      "estimativas_tela_5": { ... }
    },
    "erros": [],
    "session_id": "teste_historico_real_001",
    
    "historico": [
      {
        "etapa": "estimativas",
        "timestamp": "2025-09-29T18:06:59.570029",
        "status": "completed",
        "mensagem": "Estimativas capturadas",
        "dados_extra": { ... }
      }
    ],
    "timeline": [
      "[00:00:00] inicio: ProgressTracker inicializado",
      "[00:00:02] 1: Selecionando Tipo de Veiculo",
      "[00:00:04] 1: Tela 1 concluída"
    ],
    "historico_count": 16,
    "source": "history",
    "file_used": "history_teste_historico_real_001.json"
  },
  "timestamp": "2025-09-29T18:07:01.000000"
}
```

### **Resposta de Histórico Completo (modo 'history'):**
```json
{
  "success": true,
  "data": {
    "historico": [
      // Todas as 16 entradas do histórico
    ],
    "timeline": [
      // Timeline completa formatada
    ],
    "session_id": "teste_historico_real_001",
    "timestamp_inicio": "2025-09-29T18:06:46.696914",
    "timestamp_fim": "2025-09-29T18:07:00.997393",
    "status_final": "success",
    "total_etapas": 5,
    "duracao_total": "00:00:14"
  }
}
```

## **Cronograma de Implementação**

### **Semana 1:**
- **Dia 1:** Fase 1 - Estrutura base e parâmetros
- **Dia 2-3:** Fase 2 - Lógica de processamento
- **Dia 4:** Fase 3 - Modos de resposta
- **Dia 5:** Fase 4 - Otimizações e testes

### **Semana 2:**
- **Dia 1:** Testes de integração
- **Dia 2:** Deploy e validação
- **Dia 3:** Monitoramento e ajustes

## **Riscos e Mitigações**

### **Risco 1: Incompatibilidade com Frontend**
- **Mitigação:** Manter estrutura atual + adicionar campos novos
- **Teste:** Validar com frontend existente

### **Risco 2: Performance com Histórico Grande**
- **Mitigação:** Limite padrão de 50 entradas + cache
- **Teste:** Medir tempo de resposta

### **Risco 3: Arquivo de Histórico Corrompido**
- **Mitigação:** Fallback para progress + validação JSON
- **Teste:** Simular arquivos corrompidos

### **Risco 4: Sessões Antigas sem Histórico**
- **Mitigação:** Fallback automático para progress
- **Teste:** Testar com sessões antigas

## **Critérios de Sucesso**

### **Funcionais:**
- [ ] Compatibilidade com frontend atual mantida
- [ ] Histórico sequencial disponível
- [ ] Timeline formatada funcionando
- [ ] Fallback para progress funcionando

### **Não Funcionais:**
- [ ] Tempo de resposta < 200ms
- [ ] Cache funcionando corretamente
- [ ] Tratamento de erros robusto
- [ ] Validação de dados completa

## **Próximos Passos**

1. **Aprovação do plano**
2. **Implementação da Fase 1**
3. **Testes incrementais**
4. **Deploy em ambiente de teste**
5. **Validação com frontend**
6. **Deploy em produção**

---

**Data:** 29/09/2024  
**Versão:** 1.0  
**Autor:** Sistema RPA  
**Status:** Aguardando aprovação























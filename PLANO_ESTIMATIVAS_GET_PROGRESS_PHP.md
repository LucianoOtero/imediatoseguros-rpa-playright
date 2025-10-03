# PLANO: LÓGICA DE ESTIMATIVAS NO GET_PROGRESS.PHP

## **Análise da Lógica Atual**

### **Estrutura do Histórico:**
- **Total de entradas:** 16
- **Índice das estimativas:** 12 (entrada "estimativas")
- **Entradas após estimativas:** 3
- **Última entrada:** "final - RPA success"

### **Sequência Identificada:**
```
12: "estimativas" - "Estimativas capturadas" (completed)
13: "5.5" - "Processando Zero KM" (concluido)
14: "5.5" - "Tela Zero KM concluída" (concluido)
15: "final" - "RPA success" (success)
```

### **Conclusão:**
✅ **A lógica está correta!** Se há execução posterior às estimativas, significa que as estimativas foram capturadas com sucesso.

## **Plano de Implementação**

### **Objetivo:**
Implementar lógica no `get_progress.php` para:
1. **Detectar se as estimativas foram capturadas** (verificar execução posterior)
2. **Extrair as estimativas** do passo correto do histórico
3. **Retornar as estimativas** na resposta da API

### **Estratégia:**
1. **Buscar entrada "estimativas"** no histórico
2. **Verificar se há execução posterior** às estimativas
3. **Extrair dados das estimativas** se capturadas
4. **Incluir estimativas na resposta** da API

## **Implementação Detalhada**

### **Fase 1: Função de Detecção de Estimativas (1 dia)**

#### **1.1 Função Principal**
```php
function detectarEstimativas($historico) {
    $estimativas_idx = null;
    $estimativas_entry = null;
    $execucao_posterior = false;
    
    // Buscar entrada "estimativas"
    foreach ($historico as $index => $entry) {
        if ($entry['etapa'] === 'estimativas') {
            $estimativas_idx = $index;
            $estimativas_entry = $entry;
            break;
        }
    }
    
    // Verificar se há execução posterior
    if ($estimativas_idx !== null && count($historico) > $estimativas_idx + 1) {
        $execucao_posterior = true;
    }
    
    return [
        'estimativas_encontradas' => $estimativas_entry !== null,
        'estimativas_capturadas' => $execucao_posterior,
        'estimativas_entry' => $estimativas_entry,
        'estimativas_idx' => $estimativas_idx,
        'execucao_posterior' => $execucao_posterior
    ];
}
```

#### **1.2 Função de Extração de Dados**
```php
function extrairDadosEstimativas($estimativas_entry) {
    if (!$estimativas_entry || !isset($estimativas_entry['dados_extra'])) {
        return null;
    }
    
    $dados_extra = $estimativas_entry['dados_extra'];
    
    // Extrair coberturas detalhadas
    $coberturas = $dados_extra['coberturas_detalhadas'] ?? [];
    $resumo = $dados_extra['resumo'] ?? [];
    
    // Processar coberturas
    $coberturas_processadas = [];
    foreach ($coberturas as $cobertura) {
        $coberturas_processadas[] = [
            'nome' => $cobertura['nome_cobertura'] ?? 'N/A',
            'valores' => $cobertura['valores'] ?? [],
            'beneficios' => $cobertura['beneficios'] ?? [],
            'indice' => $cobertura['indice'] ?? 0
        ];
    }
    
    return [
        'coberturas' => $coberturas_processadas,
        'resumo' => $resumo,
        'timestamp' => $estimativas_entry['timestamp'],
        'status' => $estimativas_entry['status'],
        'mensagem' => $estimativas_entry['mensagem']
    ];
}
```

### **Fase 2: Integração com get_progress.php (1 dia)**

#### **2.1 Modificação da Resposta**
```php
// No processamento do histórico
$estimativas_info = detectarEstimativas($historico);

// Adicionar à resposta
$response['data']['estimativas'] = [
    'capturadas' => $estimativas_info['estimativas_capturadas'],
    'encontradas' => $estimativas_info['estimativas_encontradas'],
    'dados' => $estimativas_info['estimativas_capturadas'] 
        ? extrairDadosEstimativas($estimativas_info['estimativas_entry'])
        : null,
    'status' => $estimativas_info['estimativas_entry']['status'] ?? 'not_found',
    'mensagem' => $estimativas_info['estimativas_entry']['mensagem'] ?? 'Estimativas não encontradas'
];
```

#### **2.2 Estrutura da Nova Resposta**
```json
{
  "success": true,
  "data": {
    "etapa_atual": 5,
    "status": "success",
    "mensagem": "Tela Zero KM concluída",
    
    "estimativas": {
      "capturadas": true,
      "encontradas": true,
      "dados": {
        "coberturas": [
          {
            "nome": "CompreensivaDe",
            "valores": {
              "de": "R$ 2.400,00",
              "ate": "R$ 2.900,00"
            },
            "beneficios": [...],
            "indice": 1
          }
        ],
        "resumo": {
          "total_coberturas": 3,
          "total_beneficios": 12,
          "valores_encontrados": 6
        },
        "timestamp": "2025-09-29T18:06:59.570029",
        "status": "completed",
        "mensagem": "Estimativas capturadas"
      },
      "status": "completed",
      "mensagem": "Estimativas capturadas"
    },
    
    "historico": [...],
    "timeline": [...]
  }
}
```

### **Fase 3: Tratamento de Casos Especiais (1 dia)**

#### **3.1 Casos de Erro**
```php
function tratarCasosEspeciais($estimativas_info, $historico) {
    $casos = [
        'estimativas_nao_encontradas' => !$estimativas_info['estimativas_encontradas'],
        'estimativas_nao_capturadas' => $estimativas_info['estimativas_encontradas'] && !$estimativas_info['estimativas_capturadas'],
        'estimativas_com_erro' => $estimativas_info['estimativas_entry']['status'] === 'error',
        'rpa_nao_finalizado' => !$this->rpaFinalizado($historico)
    ];
    
    return $casos;
}

function rpaFinalizado($historico) {
    $ultima_entrada = end($historico);
    return $ultima_entrada['etapa'] === 'final' && $ultima_entrada['status'] === 'success';
}
```

#### **3.2 Mensagens de Status**
```php
function getMensagemEstimativas($casos) {
    if ($casos['estimativas_nao_encontradas']) {
        return 'Estimativas não encontradas no histórico';
    }
    
    if ($casos['estimativas_nao_capturadas']) {
        return 'Estimativas encontradas mas não capturadas (RPA interrompido)';
    }
    
    if ($casos['estimativas_com_erro']) {
        return 'Erro ao capturar estimativas';
    }
    
    if ($casos['rpa_nao_finalizado']) {
        return 'RPA ainda em execução';
    }
    
    return 'Estimativas capturadas com sucesso';
}
```

### **Fase 4: Otimizações e Validações (1 dia)**

#### **4.1 Cache de Estimativas**
```php
function getCacheKeyEstimativas($session_id) {
    return "estimativas_{$session_id}";
}

function getEstimativasFromCache($session_id) {
    $cache_key = getCacheKeyEstimativas($session_id);
    if (apcu_exists($cache_key)) {
        return apcu_fetch($cache_key);
    }
    return null;
}

function setEstimativasCache($session_id, $estimativas_data) {
    $cache_key = getCacheKeyEstimativas($session_id);
    apcu_store($cache_key, $estimativas_data, 30); // 30 segundos
}
```

#### **4.2 Validação de Dados**
```php
function validarEstimativas($estimativas_data) {
    if (!$estimativas_data) {
        return false;
    }
    
    $required_fields = ['coberturas', 'resumo', 'timestamp'];
    foreach ($required_fields as $field) {
        if (!isset($estimativas_data[$field])) {
            return false;
        }
    }
    
    // Validar coberturas
    if (!is_array($estimativas_data['coberturas']) || empty($estimativas_data['coberturas'])) {
        return false;
    }
    
    // Validar resumo
    $resumo = $estimativas_data['resumo'];
    if (!isset($resumo['total_coberturas']) || $resumo['total_coberturas'] <= 0) {
        return false;
    }
    
    return true;
}
```

## **Estrutura Final da Resposta**

### **Resposta com Estimativas Capturadas:**
```json
{
  "success": true,
  "data": {
    "etapa_atual": 5,
    "status": "success",
    "mensagem": "Tela Zero KM concluída",
    
    "estimativas": {
      "capturadas": true,
      "encontradas": true,
      "dados": {
        "coberturas": [
          {
            "nome": "CompreensivaDe",
            "valores": {"de": "R$ 2.400,00", "ate": "R$ 2.900,00"},
            "beneficios": [
              {"nome": "Colisão e Acidentes", "status": "incluido"},
              {"nome": "Roubo e Furto", "status": "incluido"}
            ],
            "indice": 1
          },
          {
            "nome": "Roubo",
            "valores": {"de": "R$ 1.300,00", "ate": "R$ 1.700,00"},
            "beneficios": [...],
            "indice": 13
          },
          {
            "nome": "RCFDe",
            "valores": {"de": "R$ 1.300,00", "ate": "R$ 1.700,00"},
            "beneficios": [...],
            "indice": 15
          }
        ],
        "resumo": {
          "total_coberturas": 3,
          "total_beneficios": 12,
          "valores_encontrados": 6
        },
        "timestamp": "2025-09-29T18:06:59.570029",
        "status": "completed",
        "mensagem": "Estimativas capturadas"
      },
      "status": "completed",
      "mensagem": "Estimativas capturadas"
    },
    
    "historico": [...],
    "timeline": [...]
  }
}
```

### **Resposta sem Estimativas:**
```json
{
  "success": true,
  "data": {
    "etapa_atual": 3,
    "status": "executando",
    "mensagem": "Tela 3 concluída",
    
    "estimativas": {
      "capturadas": false,
      "encontradas": false,
      "dados": null,
      "status": "not_found",
      "mensagem": "Estimativas não encontradas no histórico"
    },
    
    "historico": [...],
    "timeline": [...]
  }
}
```

## **Cronograma de Implementação**

### **Semana 1:**
- **Dia 1:** Fase 1 - Função de detecção de estimativas
- **Dia 2:** Fase 2 - Integração com get_progress.php
- **Dia 3:** Fase 3 - Tratamento de casos especiais
- **Dia 4:** Fase 4 - Otimizações e validações
- **Dia 5:** Testes e ajustes

### **Semana 2:**
- **Dia 1:** Testes de integração
- **Dia 2:** Deploy e validação
- **Dia 3:** Monitoramento e ajustes

## **Riscos e Mitigações**

### **Risco 1: Estimativas não encontradas**
- **Mitigação:** Fallback para dados_extra do progress atual
- **Teste:** Validar com sessões antigas

### **Risco 2: Dados corrompidos**
- **Mitigação:** Validação robusta + fallback
- **Teste:** Simular dados corrompidos

### **Risco 3: Performance**
- **Mitigação:** Cache de estimativas + processamento otimizado
- **Teste:** Medir tempo de resposta

## **Critérios de Sucesso**

### **Funcionais:**
- [ ] Detecção correta de estimativas capturadas
- [ ] Extração correta dos dados das estimativas
- [ ] Resposta estruturada com estimativas
- [ ] Tratamento de casos especiais

### **Não Funcionais:**
- [ ] Tempo de resposta < 100ms
- [ ] Cache funcionando
- [ ] Validação robusta
- [ ] Compatibilidade mantida

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















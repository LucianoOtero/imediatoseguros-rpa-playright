# 📋 ESPECIFICAÇÃO TÉCNICA
## Registro de Conversões e Chamadas aos Endpoints
### Imediato Seguros - Análise Completa

---

## 🎯 OBJETIVO
Documentar como são realizadas as 3 chamadas principais:
1. **Registro de Conversões no Google Ads**
2. **Chamada ao endpoint `add_travelangels` (EspoCRM)**
3. **Chamada ao endpoint `add_webflow_octa` (Octadesk)**

---

## 1️⃣ REGISTRO DE CONVERSÕES NO GOOGLE ADS

### 📍 Localização no Código
- **Arquivo**: `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.js`
- **Linhas**: 962-970, 1024-1031, 1085-1092

### 🔧 Implementação Atual

#### **Evento: `form_submit_valid`**
**Disparado quando**: Dados do formulário são válidos

```javascript
// Linha 962-970 do Footer Code
console.log('🎯 [GTM] Registrando conversão - dados válidos');
if (typeof window.dataLayer !== 'undefined') {
  window.dataLayer.push({
    'event': 'form_submit_valid',
    'form_type': 'cotacao_seguro',
    'validation_status': 'valid'
  });
}
```

#### **Evento: `form_submit_invalid_proceed`**
**Disparado quando**: Usuário prossegue com dados inválidos

```javascript
// Linha 1024-1031 do Footer Code
console.log('🎯 [GTM] Registrando conversão - usuário prosseguiu com dados inválidos');
if (typeof window.dataLayer !== 'undefined') {
  window.dataLayer.push({
    'event': 'form_submit_invalid_proceed',
    'form_type': 'cotacao_seguro',
    'validation_status': 'invalid_proceed'
  });
}
```

#### **Evento: `form_submit_network_error_proceed`**
**Disparado quando**: Usuário prossegue após erro de rede

```javascript
// Linha 1085-1092 do Footer Code
console.log('🎯 [GTM] Registrando conversão - usuário prosseguiu após erro de rede');
if (typeof window.dataLayer !== 'undefined') {
  window.dataLayer.push({
    'event': 'form_submit_network_error_proceed',
    'form_type': 'cotacao_seguro',
    'validation_status': 'network_error_proceed'
  });
}
```

### 🔍 Configuração GTM
- **Container ID**: `GTM-PD6J398`
- **Tag responsável**: "Disparo form"
- **Acionador**: "Clique no botão submit_button_auto"
- **Tipo**: Google Ads Conversion

### 📊 Estrutura dos Eventos
Todos os eventos seguem o padrão:
```javascript
{
  'event': 'nome_do_evento',
  'form_type': 'cotacao_seguro',
  'validation_status': 'status_atual'
}
```

---

## 2️⃣ CHAMADA AO ENDPOINT `add_travelangels` (EspoCRM)

### 📍 Localizações no Código

#### **A) No arquivo `start.php`**
- **Linhas**: 207-216
- **Contexto**: Executado após receber dados da API RPA

```php
echo "📞 Chamando add_travelangels.php (EspoCRM)...\n";
$travelangels_result = callWebhook('https://mdmidia.com.br/add_travelangels.php', $webhook_data);
$webhook_results['travelangels'] = $travelangels_result;

if ($travelangels_result['success']) {
    $webhook_success_count++;
    echo "✅ EspoCRM: Lead criado com sucesso\n";
} else {
    echo "❌ EspoCRM: Falha - " . $travelangels_result['error'] . "\n";
}
```

#### **B) No arquivo `RPAController_novo.php`**
- **Linhas**: 151-159
- **Contexto**: Controller da API RPA

```php
$this->logger->info('Calling EspoCRM webhook');
$travelangels_result = $this->callWebhook('https://mdmidia.com.br/add_travelangels.php', $webhook_data);
$webhook_results['travelangels'] = $travelangels_result;

if ($travelangels_result['success']) {
    $webhook_success_count++;
    $this->logger->info('EspoCRM webhook successful');
} else {
    $this->logger->error('EspoCRM webhook failed', ['error' => $travelangels_result['error']]);
}
```

### 🔧 Função `callWebhook()`

```php
function callWebhook($url, $data) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'User-Agent: RPA-API-v6.9.0'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    return [
        'success' => $http_code >= 200 && $http_code < 300,
        'http_code' => $http_code,
        'response' => $response,
        'error' => $error
    ];
}
```

### 📦 Estrutura dos Dados Enviados

```php
$webhook_data = [
    'data' => [
        'NOME' => $data['nome'],
        'DDD-CELULAR' => $data['ddd_celular'] ?? '11',
        'CELULAR' => $data['celular'] ?? substr($data['telefone'], 2),
        'Email' => $data['email'],
        'CEP' => $data['cep'],
        'CPF' => $data['cpf'],
        'MARCA' => $data['marca'] ?? '',
        'PLACA' => $data['placa'],
        'VEICULO' => $data['marca'] ?? '',
        'ANO' => $data['ano'] ?? '',
        'GCLID_FLD' => $data['gclid'] ?? '',
        'SEXO' => $data['sexo'] ?? '',
        'DATA-DE-NASCIMENTO' => $data['data_nascimento'] ?? '',
        'ESTADO-CIVIL' => $data['estado_civil'] ?? '',
        'produto' => $data['produto'] ?? 'seguro-auto',
        'landing_url' => $data['landing_url'] ?? '',
        'utm_source' => $data['utm_source'] ?? '',
        'utm_campaign' => $data['utm_campaign'] ?? ''
    ],
    'd' => date('c'),
    'name' => 'Formulário de Cotação RPA'
];
```

### 🔗 URL do Endpoint
- **Produção**: `https://bpsegurosimediato.com.br/add_travelangels.php`
- **Desenvolvimento**: `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php`

### ⏱️ Configurações
- **Timeout**: 30 segundos
- **Connect Timeout**: 10 segundos
- **Método**: POST
- **Content-Type**: application/json

---

## 3️⃣ CHAMADA AO ENDPOINT `add_webflow_octa` (Octadesk)

### 📍 Localizações no Código

#### **A) No arquivo `start.php`**
- **Linhas**: 218-227
- **Contexto**: Executado após chamada ao EspoCRM

```php
echo "📱 Chamando add_webflow_octa.php (Octadesk)...\n";
$octa_result = callWebhook('https://mdmidia.com.br/add_webflow_octa.php', $webhook_data);
$webhook_results['octadesk'] = $octa_result;

if ($octa_result['success']) {
    $webhook_success_count++;
    echo "✅ Octadesk: Mensagem WhatsApp enviada\n";
} else {
    echo "❌ Octadesk: Falha - " . $octa_result['error'] . "\n";
}
```

#### **B) No arquivo `RPAController_novo.php`**
- **Linhas**: 161-170
- **Contexto**: Controller da API RPA

```php
$this->logger->info('Calling Octadesk webhook');
$octa_result = $this->callWebhook('https://mdmidia.com.br/add_webflow_octa.php', $webhook_data);
$webhook_results['octadesk'] = $octa_result;

if ($octa_result['success']) {
    $webhook_success_count++;
    $this->logger->info('Octadesk webhook successful');
} else {
    $this->logger->error('Octadesk webhook failed', ['error' => $octa_result['error']]);
}
```

### 🔧 Função `callWebhook()`
Utiliza a mesma função do endpoint `add_travelangels` (ver seção 2).

### 📦 Estrutura dos Dados Enviados
Utiliza a mesma estrutura do endpoint `add_travelangels` (ver seção 2).

### 🔗 URL do Endpoint
- **Produção**: `https://bpsegurosimediato.com.br/add_webflow_octa.php`
- **Desenvolvimento**: `https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php`

### ⏱️ Configurações
- **Timeout**: 30 segundos
- **Connect Timeout**: 10 segundos
- **Método**: POST
- **Content-Type**: application/json

---

## 🔄 FLUXO COMPLETO DE EXECUÇÃO

### **Sequência de Chamadas:**

1. **Usuário submete formulário**
   - Validação de campos (CPF, CEP, PLACA, CELULAR, EMAIL)
   - Evento registrado no GTM: `form_submit_valid` / `form_submit_invalid_proceed` / `form_submit_network_error_proceed`

2. **API RPA recebe dados** (`/api/rpa/start`)
   - Processamento dos dados
   - Preparação do `$webhook_data`

3. **Chamada ao EspoCRM** (`add_travelangels.php`)
   - Criação do lead no EspoCRM
   - Retorno: sucesso ou erro

4. **Chamada ao Octadesk** (`add_webflow_octa.php`)
   - Envio de mensagem WhatsApp via Octadesk
   - Retorno: sucesso ou erro

5. **Iniciar RPA** (se webhooks foram bem-sucedidos)
   - Processo RPA executado em background
   - Modal de progresso exibido ao usuário

---

## 🌍 AMBIENTES: DESENVOLVIMENTO vs PRODUÇÃO

### **📋 Resumo dos Endpoints por Ambiente**

| Endpoint | Ambiente | URL | Uso |
|----------|----------|-----|-----|
| **EspoCRM** | 🧪 **DEV** | `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php` | Testes e desenvolvimento |
| **EspoCRM** | 🚀 **PROD** | `https://bpsegurosimediato.com.br/add_travelangels.php` | Produção (usuários reais) |
| **Octadesk** | 🧪 **DEV** | `https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php` | Testes e desenvolvimento |
| **Octadesk** | 🚀 **PROD** | `https://bpsegurosimediato.com.br/add_webflow_octa.php` | Produção (usuários reais) |
| **Google Ads** | 🧪 **DEV** | GTM-PD6J398 (configurar tag de teste) | Testes com preview mode |
| **Google Ads** | 🚀 **PROD** | GTM-PD6J398 | Produção (conversões reais) |

### **🔧 Arquivo de Configuração de Desenvolvimento**

**Localização**: `dev_config.php`

```php
// URLs dos webhooks de desenvolvimento
$DEV_WEBHOOK_URLS = [
    'travelangels' => 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php',
    'octadesk' => 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php',
    'health' => 'https://bpsegurosimediato.com.br/dev/webhooks/health.php'
];
```

### **📝 Estratégia de Implementação**

1. **FASE 1: DESENVOLVIMENTO** 🧪
   - Implementar usando URLs de desenvolvimento
   - Testar todas as funcionalidades
   - Validar integrações
   - Verificar logs em `/var/www/html/dev/logs/`

2. **FASE 2: MIGRAÇÃO PARA PRODUÇÃO** 🚀
   - Após testes bem-sucedidos, alterar URLs para produção
   - Validar em ambiente de staging (se disponível)
   - Deploy gradual com monitoramento

### **🔍 Como Identificar Ambiente**

```javascript
// Detectar se está em desenvolvimento
function isDevelopmentEnvironment() {
  // Opção 1: Verificar hostname
  if (window.location.hostname.includes('dev.') || 
      window.location.hostname.includes('localhost')) {
    return true;
  }
  
  // Opção 2: Verificar URL
  if (window.location.href.includes('/dev/')) {
    return true;
  }
  
  // Opção 3: Variável global configurada
  if (window.ENVIRONMENT === 'development') {
    return true;
  }
  
  return false;
}

// Função para obter URL do endpoint baseado no ambiente
function getEndpointUrl(endpoint) {
  const isDev = isDevelopmentEnvironment();
  
  const endpoints = {
    travelangels: {
      dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php',
      prod: 'https://bpsegurosimediato.com.br/add_travelangels.php'
    },
    octadesk: {
      dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php',
      prod: 'https://bpsegurosimediato.com.br/add_webflow_octa.php'
    }
  };
  
  return endpoints[endpoint][isDev ? 'dev' : 'prod'];
}
```

### **📁 Estrutura de Diretórios no Servidor**

```
/var/www/html/
├── add_travelangels.php          # PRODUÇÃO
├── add_webflow_octa.php          # PRODUÇÃO
├── dev/                          # AMBIENTE DE DESENVOLVIMENTO
│   ├── webhooks/
│   │   ├── add_travelangels.php  # DEV
│   │   ├── add_webflow_octa.php  # DEV
│   │   └── health.php
│   └── logs/
│       ├── travelangels_dev.txt
│       ├── octadesk_dev.txt
│       ├── general_dev.txt
│       └── errors_dev.txt
└── logs/                         # LOGS DE PRODUÇÃO
```

---

## 📊 RESUMO DAS ESPECIFICAÇÕES

| Endpoint / Evento | Método | URL DEV | URL PROD | Timeout | Content-Type |
|-------------------|--------|---------|----------|---------|--------------|
| **Google Ads Conversion** | dataLayer.push() | GTM-PD6J398 (test mode) | GTM-PD6J398 | - | Event Object |
| **EspoCRM** | POST | `bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php` | `bpsegurosimediato.com.br/add_travelangels.php` | 30s | application/json |
| **Octadesk** | POST | `bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php` | `bpsegurosimediato.com.br/add_webflow_octa.php` | 30s | application/json |

---

## 🔍 PONTOS DE ATENÇÃO

1. **Ordem de Execução**: Os webhooks são chamados ANTES do processo RPA
2. **Estrutura de Dados**: Ambos os webhooks recebem a mesma estrutura `$webhook_data`
3. **Tratamento de Erros**: Falhas nos webhooks não bloqueiam o processo RPA
4. **GCLID**: Capturado dos cookies e incluído em `GCLID_FLD`
5. **Validações**: Os campos são validados antes do registro de conversão

---

## 📝 OBSERVAÇÕES

- O registro de conversão no Google Ads acontece **no frontend** (JavaScript)
- As chamadas aos endpoints `add_travelangels` e `add_webflow_octa` acontecem **no backend** (PHP)
- A função `callWebhook()` é reutilizada para ambos os endpoints
- Os dados são preparados uma única vez e enviados para ambos os webhooks

---

**Data de Criação**: 2025-01-23  
**Versão**: 1.0  
**Autor**: Análise Automatizada de Código


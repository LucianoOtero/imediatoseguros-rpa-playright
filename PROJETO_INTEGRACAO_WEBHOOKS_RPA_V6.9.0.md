# 🚀 PROJETO INTEGRACAO WEBHOOKS RPA V6.9.0

## 📝 **ESPECIFICAÇÃO DETALHADA DO CLIENTE**

### **🎯 OBJETIVO PRINCIPAL**
Integrar a API RPA existente com os webhooks já utilizados no site Webflow (`segurosimediato.com.br`), mantendo a funcionalidade atual e adicionando a captura de GCLID para rastreamento de campanhas.

### **📋 REQUISITOS ESPECÍFICOS**

#### **1. ANÁLISE DOS WEBHOOKS EXISTENTES**
- **Webhook 1**: `add_travelangels.php` (EspoCRM)
  - Localização: `https://mdmidia.com.br/add_travelangels.php`
  - Função: Adicionar lead no EspoCRM com dados do formulário
  - Campos esperados: NOME, DDD-CELULAR, CELULAR, Email, CEP, CPF, MARCA, PLACA, ANO, GCLID_FLD

- **Webhook 2**: `add_webflow_octa.php` (Octadesk)
  - Localização: `https://mdmidia.com.br/add_webflow_octa.php`
  - Função: Criar mensagem no Octadesk para WhatsApp do cliente
  - Campos esperados: NOME, DDD-CELULAR, CELULAR, Email, CEP, CPF, MARCA, PLACA, ANO, GCLID_FLD

#### **2. INTEGRAÇÃO COM API PH3A**
- **Problema identificado**: API PH3A desabilitada no Webflow (`VALIDAR_PH3A = false`)
- **Motivo**: Performance lenta afetando experiência do usuário
- **Solução**: Consultar PH3A no endpoint RPA quando campos estiverem em branco
- **Campos PH3A**: SEXO, DATA-DE-NASCIMENTO, ESTADO-CIVIL
- **Endpoint**: `https://mdmidia.com.br/cpf-validate.php`

#### **3. CAPTURA DE GCLID**
- **Campo obrigatório**: `id="GCLID_FLD"`
- **Origem**: JavaScript já existente no Webflow (Inside Head Tag Pagina.js)
- **Função**: Rastreamento de campanhas Google Ads
- **Status**: ✅ **JÁ IMPLEMENTADO** - GCLID é capturado automaticamente e preenchido no campo
- **Inclusão**: Campo deve ser enviado na chamada da API RPA

#### **4. ORDEM DE EXECUÇÃO SOLICITADA**
1. **PH3A primeiro**: Consultar API se campos em branco
2. **Webhooks segundo**: Chamar EspoCRM e Octadesk imediatamente
3. **RPA terceiro**: Processar cotação em background

#### **5. MODIFICAÇÕES EM ARQUIVOS HTML**
- **index.html**: Adicionar campo `GCLID_FLD` com valor padrão "TesteRPA123"
- **teste_js_atualizado.html**: Adicionar campo `GCLID_FLD` com valor padrão "TesteRPA123"

#### **6. BENEFÍCIOS ESPERADOS**
- **Resposta imediata**: Cliente recebe WhatsApp em <5 segundos
- **Dados completos**: PH3A preenche campos automaticamente
- **CRM atualizado**: EspoCRM sensibilizado antes do RPA
- **Proteção de dados**: Lead salvo mesmo se RPA falhar
- **Métricas precisas**: Conversão registrada imediatamente

### **🔧 IMPLEMENTAÇÃO TÉCNICA - FASE 1**

#### **📋 ESCOPO DA FASE 1**
Implementação mínima focada em segurança básica e funcionalidade essencial, conforme observações do engenheiro de software.

#### **Endpoint RPA Modificado**
- **URL**: `https://rpaimediatoseguros.com.br/api/rpa/start`
- **Método**: POST
- **Content-Type**: application/json
- **Funcionalidades (Fase 1)**:
  - ✅ Validação básica de campos obrigatórios
  - ✅ Sanitização de entrada
  - ✅ Consulta PH3A condicional
  - ✅ Chamada sequencial dos 2 webhooks
  - ✅ Inicialização do RPA em background
  - ✅ Logs essenciais com mascaramento de CPF
  - ✅ Timeout de 30s para chamadas externas

#### **Estrutura de Dados**
```json
{
  "cpf": "12345678901",
  "nome": "João Silva",
  "placa": "ABC1234",
  "cep": "01234567",
  "email": "joao@email.com",
  "telefone": "11987654321",
  "gclid": "TesteRPA123",
  "sexo": "Masculino",
  "data_nascimento": "01/01/1990",
  "estado_civil": "Solteiro"
}
```

#### **Resposta da API**
```json
{
  "success": true,
  "session_id": "rpa_v6.9.0_20250110_153000_abc12345",
  "message": "PH3A consultado, webhooks executados e RPA iniciado com sucesso",
  "ph3a_consulted": true,
  "ph3a_fields_filled": ["sexo", "data_nascimento", "estado_civil"],
  "webhook_results": {
    "travelangels": {"success": true, "http_code": 200},
    "octadesk": {"success": true, "http_code": 200}
  },
  "webhook_success_count": 2,
  "rpa_pid": "12345",
  "execution_order": "ph3a_then_webhooks_then_rpa"
}
```

### **📊 MÉTRICAS DE SUCESSO**
- **Taxa de sucesso PH3A**: >90%
- **Taxa de sucesso webhooks**: >95%
- **Tempo de resposta PH3A**: <3 segundos
- **Tempo de resposta webhooks**: <2 segundos
- **Tempo de resposta WhatsApp**: <5 segundos
- **Captura de GCLID**: 100% dos casos

### **⚠️ CONSIDERAÇÕES IMPORTANTES**
- **Compatibilidade**: Manter 100% com sistema atual
- **Performance**: PH3A consultado apenas quando necessário
- **Fallback**: Sistema funciona mesmo se PH3A falhar
- **Logs**: Registro detalhado para debugging
- **Monitoramento**: Acompanhamento de todas as etapas

---

## 👨‍💻 **OBSERVAÇÕES DO ENGENHEIRO DE SOFTWARE**

### **📋 ANÁLISE ATUALIZADA DO PROJETO**
**Base**: Decisão de adiar implementações avançadas (queues assíncronas, autenticação API) para fase posterior. Foco na estabilidade da versão atual sem adicionar complexidade. Mitigações enfatizam soluções simples e imediatas, compatíveis com código PHP existente.

### **🚨 RISCOS IDENTIFICADOS E MITIGAÇÕES (FASE 1)**

| **Risco** | **Descrição** | **Impacto Potencial** | **Mitigações Sugeridas (Fase Atual)** |
|-----------|---------------|----------------------|--------------------------------------|
| **Falha nos webhooks ou APIs externas** | Dependência de endpoints como add_travelangels.php, add_webflow_octa.php e cpf-validate.php (PH3A). Se indisponíveis, podem bloquear o fluxo. | Atrasos no envio de WhatsApp ou criação de leads, perda de conversões. | Manter chamadas síncronas com timeouts configuráveis no cURL (30s para webhooks, 15s para PH3A). Registrar erros detalhados nos logs existentes. Implementar fallback simples: continuar RPA mesmo em falhas. |
| **Timeout ou lentidão no RPA** | Processo RPA em background pode exceder 3 minutos, especialmente com alto volume. | Usuários recebem feedback atrasado, afetando UX. | Otimizar script Python existente com verificações básicas de performance. Usar polling existente no JavaScript (intervalo de 2s) com timeout após 90 polls. |
| **Dados inválidos ou incompletos** | Validações no PHP são básicas; campos como CPF podem ser inválidos ou formatados errados. PH3A pode retornar dados inconsistentes. | Erros em integrações downstream, como CRM ou WhatsApp inválido. | Expandir validações inline no PHP (regex para CPF e email). Para PH3A, adicionar checks simples para dados nulos ou inválidos, preenchendo com defaults se necessário. |
| **Conflitos de sessões** | Múltiplos requests simultâneos podem sobrescrever sessões ou logs. | Perda de dados ou rastreamento incorreto de sessões. | Reforçar uso de session_id único (md5 + uniqid) e locking em arquivos via file_put_contents com LOCK_EX. |
| **Vazamento de dados sensíveis** | Dados como CPF, email e telefone são enviados via POST sem proteções adicionais. Logs armazenam inputs completos. | Violação de privacidade (LGPD), exposição a ataques como MITM. | Garantir HTTPS em todas as URLs. Mascarar dados sensíveis nos logs (substituir CPF por últimos 4 dígitos). Monitorar acessos via logs de servidor. |
| **Falhas no JavaScript client-side** | Captura de GCLID/UTM depende de regex e DOM manipulation; pode falhar em browsers antigos ou com adblockers. | Perda de rastreamento de campanhas, métricas imprecisas. | Adicionar logs de console simples para debugging. Testar manualmente em browsers comuns e adicionar fallbacks básicos (valor default se gclid null). |
| **Sobrecarga de servidor** | Chamadas sequenciais (PH3A → webhooks → RPA) em alto tráfego podem esgotar recursos do servidor. | Downtime ou lentidão geral. | Monitorar via logs existentes e ferramentas básicas do servidor (top/htop). Limitar requests via configuração de nginx/Apache se necessário. |
| **Incompatibilidades futuras** | Dependência de estruturas fixas (JSON específico para webhooks) pode quebrar com atualizações em EspoCRM ou Octadesk. | Interrupção do fluxo de integração. | Documentar estruturas JSON no código e adicionar testes manuais no checklist de deploy. |
| **Erros de configuração ou deploy** | Paths hardcoded (ex.: /opt/imediatoseguros-rpa) e dependências como venv podem falhar em ambientes diferentes. | Falhas em produção pós-deploy. | Usar comentários no código para paths críticos e testar deploy em staging antes de produção. |

### **🎯 OPORTUNIDADES DE MELHORIAS (FASE 1)**

#### **✅ IMPLEMENTAÇÕES IMEDIATAS (FASE 1)**
1. **Otimização de Performance Básica**: Adicionar medições de tempo simples (microtime() antes/depois de chamadas cURL) para logs
2. **Monitoramento Melhorado**: Expandir logs existentes para incluir timestamps por etapa
3. **Documentação Atualizada**: Atualizar documento do projeto com notas sobre adiamentos
4. **Compliance LGPD**: Verificar HTTPS e mascarar logs sensíveis (CPF por últimos 4 dígitos)
5. **Feedback ao Usuário**: Melhorar mensagens no modal de progresso com textos mais amigáveis

#### **⏳ ADIADAS PARA FASE POSTERIOR**
- **Testes Automatizados**: Implementar testes unitários básicos para funções como callWebhook
- **Integração com Ferramentas Modernas**: Migração para GraphQL ou Google Tag Manager
- **Escalabilidade Horizontal**: Containerização com Docker ou auto-scaling
- **Autenticação API**: API keys ou JWT
- **Processamento Assíncrono**: Queues como Redis para webhooks

### **⚠️ PONTO CRÍTICO IDENTIFICADO**
**Vazamento de dados sensíveis (LGPD)**: Como não há autenticação agora, verificar HTTPS e mascarar logs sensíveis como tarefa rápida antes do deploy para evitar multas potenciais. Se ambiente for interno/controlado, pode esperar.

### **📊 VERIFICAÇÃO DE CONFORMIDADE COM OBSERVAÇÕES**
**Status**: ✅ **ALTO ALINHAMENTO** - Documento reflete precisamente as observações do engenheiro

#### **✅ CONFORMIDADES CONFIRMADAS**
- **Estrutura de fases**: Separação clara Fase 1 (mínima) vs Fase 2 (adiada)
- **Riscos e mitigações**: Tabela completa com soluções simples e imediatas
- **LGPD crítico**: Tratado como prioridade máxima com ações específicas
- **Fluxo sequencial**: PH3A síncrona → webhooks síncronos → RPA background
- **Timeouts configuráveis**: 30s webhooks, 15s PH3A
- **Logs mascarados**: CPF por últimos 4 dígitos
- **Validações inline**: Regex para CPF/email no PHP

#### **🔧 REFINAMENTOS SUGERIDOS**
- **Medições de tempo**: Adicionar `microtime(true)` para logs de performance
- **Validação pós-deploy**: Monitorar logs por 1-2 semanas antes da Fase 2
- **Cronograma**: Atualizar datas para refletir revisões atuais

---

## 🎯 **OBJETIVO**
Modificar a API RPA para chamar automaticamente os 2 webhooks existentes (`add_travelangels.php` e `add_webflow_octa.php`) com os dados recebidos, incluindo a coleta do GCLID no Webflow e sua inclusão na chamada da API RPA.

---

## 🚀 **FASES DE IMPLEMENTAÇÃO**

### **📋 FASE 1: IMPLEMENTAÇÃO MÍNIMA (PRODUÇÃO)**
**Objetivo**: Implementar apenas o essencial para segurança e funcionalidade básica

#### **✅ IMPLEMENTAÇÕES OBRIGATÓRIAS (BASEADAS NAS OBSERVAÇÕES DO ENGENHEIRO)**
1. **Validação de entrada básica**
   - Sanitização de campos obrigatórios
   - Validação de formato CPF, CEP, email (regex inline no PHP)
   - Timeout de 30s para webhooks, 15s para PH3A
   - Checks simples para dados nulos ou inválidos do PH3A

2. **Consulta PH3A condicional**
   - Verificação de campos em branco
   - Chamada apenas quando necessário
   - Fallback se PH3A falhar (continuar RPA mesmo em falhas)
   - Preenchimento com defaults se dados inconsistentes

3. **Chamada dos webhooks**
   - EspoCRM e Octadesk em sequência (síncrono)
   - Logs básicos de sucesso/falha com timestamps por etapa
   - Timeout de 30s por webhook
   - Medições de tempo simples (microtime() antes/depois)

4. **Inicialização do RPA**
   - Processo em background
   - PID tracking
   - Status básico
   - Verificações básicas de performance no script Python

5. **Logs essenciais com segurança**
   - Session ID único (md5 + uniqid)
   - Timestamp por etapa
   - Resultado dos webhooks
   - Dados de entrada mascarados (CPF por últimos 4 dígitos)
   - Locking em arquivos via file_put_contents com LOCK_EX

6. **Compliance LGPD (CRÍTICO)**
   - Verificar HTTPS em todas as URLs
   - Mascarar dados sensíveis nos logs
   - Monitorar acessos via logs de servidor

#### **🔒 SEGURANÇA MÍNIMA (BASEADA NAS OBSERVAÇÕES)**
- HTTPS obrigatório com verificação de certificados válidos
- Validação de Content-Type
- Sanitização rigorosa de entrada
- Mascaramento de CPF nos logs (últimos 4 dígitos)
- Monitoramento de acessos via logs de servidor
- Session ID único com locking em arquivos

#### **⚡ PERFORMANCE MÍNIMA (BASEADA NAS OBSERVAÇÕES)**
- Timeout configurável (30s webhooks, 15s PH3A)
- Processamento sequencial (síncrono)
- Logs em arquivo local com timestamps por etapa
- Medições de tempo simples (microtime())
- Verificações básicas de performance no Python

---

### **📋 FASE 2: MELHORIAS AVANÇADAS (PÓS-PRODUÇÃO)**
**Status**: ⏳ **PENDENTE - REQUER AUTORIZAÇÃO**

#### **🔒 SEGURANÇA AVANÇADA**
- [ ] Rate limiting por IP
- [ ] Validação de certificados SSL
- [ ] Criptografia de dados sensíveis
- [ ] Auditoria de acesso

#### **⚡ PERFORMANCE AVANÇADA**
- [ ] Cache PH3A (Redis/Memcached)
- [ ] Processamento paralelo de webhooks
- [ ] Connection pooling
- [ ] Compressão gzip

#### **🛡️ TRATAMENTO DE ERROS AVANÇADO**
- [ ] Retry logic com backoff exponencial
- [ ] Circuit breaker pattern
- [ ] Alertas automáticos
- [ ] Rollback automático

#### **📊 MONITORAMENTO AVANÇADO**
- [ ] Health checks endpoints
- [ ] Métricas detalhadas (Prometheus)
- [ ] Distributed tracing
- [ ] Dashboard em tempo real

#### **🧪 TESTES E QUALIDADE**
- [ ] Testes unitários (80% cobertura)
- [ ] Testes de integração
- [ ] Testes de carga
- [ ] Ambiente de staging

#### **📚 DOCUMENTAÇÃO AVANÇADA**
- [ ] Swagger/OpenAPI
- [ ] Runbooks operacionais
- [ ] Diagramas de arquitetura
- [ ] Changelog automatizado

---

### **⚠️ IMPORTANTE**
- **Fase 1**: Implementação imediata para produção
- **Fase 2**: Melhorias futuras após estabilização
- **Autorização**: Fase 2 requer aprovação explícita do cliente
- **Prioridade**: Foco na funcionalidade básica e segurança mínima
- **Validação pós-deploy**: Monitorar logs por 1-2 semanas antes da Fase 2
- **Cronograma**: Revisões atualizadas em outubro 2025

---

## 📊 **ANÁLISE DOS WEBHOOKS EXISTENTES**

### **🔍 ESTRUTURA JSON ESPERADA**

#### **📋 WEBHOOK 1: add_travelangels.php (EspoCRM)**
**Função**: Adicionar registro no EspoCRM com dados do formulário
**URL**: `https://mdmidia.com.br/add_travelangels.php`

**Estrutura JSON Esperada**:
```json
{
  "data": {
    "NOME": "João Silva",
    "DDD-CELULAR": "11",
    "CELULAR": "999999999",
    "Email": "joao@email.com",
    "CEP": "01234567",
    "CPF": "12345678901",
    "MARCA": "Honda",
    "PLACA": "ABC1234",
    "ANO": "2020",
    "GCLID_FLD": "Cj0KCQiA..."
  },
  "d": "2025-01-10T15:30:00Z",
  "name": "Formulário de Cotação"
}
```

**Campos Mapeados para EspoCRM**:
- `firstName` ← `NOME`
- `emailAddress` ← `Email`
- `cCelular` ← `DDD-CELULAR` + `CELULAR`
- `addressPostalCode` ← `CEP`
- `cCpftext` ← `CPF`
- `cMarca` ← `MARCA`
- `cPlaca` ← `PLACA`
- `cAnoMod` ← `ANO`
- `cGclid` ← `GCLID_FLD`
- `cWebpage` ← `name`

#### **📋 WEBHOOK 2: add_webflow_octa.php (Octadesk)**
**Função**: Criar mensagem no Octadesk para o cliente
**URL**: `https://mdmidia.com.br/add_webflow_octa.php`

**Estrutura JSON Esperada**:
```json
{
  "data": {
    "NOME": "João Silva",
    "DDD-CELULAR": "11",
    "CELULAR": "999999999",
    "Email": "joao@email.com",
    "CEP": "01234567",
    "CPF": "12345678901",
    "PLACA": "ABC1234",
    "VEICULO": "Honda Civic",
    "ANO": "2020",
    "GCLID_FLD": "Cj0KCQiA...",
    "produto": "seguro-auto",
    "landing_url": "https://segurosimediato.com.br/cotacao",
    "utm_source": "google",
    "utm_campaign": "seguros-2025"
  }
}
```

**Funcionalidades do Octadesk**:
- Upsert de contato (busca por telefone/e-mail)
- Criação de conversa com template `site_cotacao`
- Custom fields: CPF, CEP, PLACA, VEICULO, ANO
- Tags automáticas: `lead-webflow`, `produto:seguro-auto`

---

## 🔧 **IMPLEMENTAÇÃO DO PROJETO**

### **FASE 1: VERIFICAÇÃO DO GCLID EXISTENTE NO WEBFLOW**

#### **1.1 Status Atual do GCLID**
✅ **GCLID JÁ IMPLEMENTADO** - Não é necessário criar novo código

**Arquivo**: `Inside Head Tag Pagina.js` (linhas 14-26)
```javascript
// Captura gclid OU gbraid (qualquer um dos dois)
var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");

// Define prioridade: se gclid existir, usa ele. Se não, usa gbraid.
var trackingId = gclid || gbraid;

if (trackingId) {
  var gclsrc = getParam("gclsrc");
  if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
    setCookie("gclid", trackingId, 90); // ✅ SALVA EM COOKIE POR 90 DIAS
  }
}
```

**Preenchimento Automático** (linhas 40-44):
```javascript
document.addEventListener("DOMContentLoaded", function () {
  const gclidFields = document.getElementsByName("GCLID_FLD");
  for (var i = 0; i < gclidFields.length; i++) {
    gclidFields[i].value = readCookie("gclid"); // ✅ PREENCHE AUTOMATICAMENTE
  }
});
```

#### **1.2 Campo Oculto Necessário no Formulário**
```html
<!-- Campo oculto para GCLID (será preenchido automaticamente) -->
<input type="hidden" id="GCLID_FLD" name="GCLID_FLD" value="">
```

#### **1.3 Campos Ocultos Adicionais para UTM (Opcionais)**
```html
<!-- Campos ocultos para UTM parameters -->
<input type="hidden" id="utm_source" name="utm_source" value="">
<input type="hidden" id="utm_medium" name="utm_medium" value="">
<input type="hidden" id="utm_campaign" name="utm_campaign" value="">
<input type="hidden" id="utm_term" name="utm_term" value="">
<input type="hidden" id="utm_content" name="utm_content" value="">
<input type="hidden" id="landing_url" name="landing_url" value="">
```

---

### **FASE 2: MODIFICAÇÃO DA API RPA**

#### **2.1 Estrutura do Endpoint Atualizado**
**Endpoint**: `POST /api/rpa/start`

**Request Atualizado**:
```json
{
  "cpf": "12345678901",
  "nome": "João Silva",
  "placa": "ABC1234",
  "cep": "01234567",
  "email": "joao@email.com",
  "telefone": "11999999999",
  "tipo_veiculo": "carro",
  "ddd_celular": "11",
  "celular": "999999999",
  "marca": "Honda",
  "ano": "2020",
  "gclid": "Cj0KCQiA...",
  "utm_source": "google",
  "utm_medium": "cpc",
  "utm_campaign": "seguros-2025",
  "utm_term": "seguro auto",
  "utm_content": "banner-principal",
  "landing_url": "https://segurosimediato.com.br/cotacao",
  "produto": "seguro-auto"
}
```

#### **2.2 Implementação PHP do Endpoint - WEBHOOKS PRIMEIRO**
```php
<?php
// arquivo: /opt/imediatoseguros-rpa-v4/public/api/rpa/start.php

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method not allowed']);
    exit;
}

// Get JSON input
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON']);
    exit;
}

// Validate required fields
$required_fields = ['cpf', 'nome', 'placa', 'cep', 'email', 'telefone'];
foreach ($required_fields as $field) {
    if (empty($data[$field])) {
        http_response_code(400);
        echo json_encode(['status' => 'error', 'message' => "Campo obrigatório: $field"]);
        exit;
    }
}

// Generate session ID
$session_id = 'rpa_v6.9.0_' . date('Ymd_His') . '_' . substr(md5(uniqid()), 0, 8);

// ========================================
// ETAPA 1: CONSULTAR API PH3A (SE NECESSÁRIO)
// ========================================
$start_time = microtime(true);
echo "🔍 ETAPA 1: VERIFICANDO CAMPOS PH3A\n";
echo "====================================\n";

// Verificar se campos PH3A estão em branco
$campos_ph3a_vazios = [];
if (empty($data['sexo'])) $campos_ph3a_vazios[] = 'sexo';
if (empty($data['data_nascimento'])) $campos_ph3a_vazios[] = 'data_nascimento';
if (empty($data['estado_civil'])) $campos_ph3a_vazios[] = 'estado_civil';

$ph3a_data = [];
if (!empty($campos_ph3a_vazios) && !empty($data['cpf'])) {
    echo "📞 Consultando API PH3A para campos: " . implode(', ', $campos_ph3a_vazios) . "\n";
    
    // Function to call PH3A API
    function callPH3AApi($cpf) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://mdmidia.com.br/cpf-validate.php');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['cpf' => $cpf]));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'User-Agent: RPA-API-v6.9.0'
        ]);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 15);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
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
    
    $ph3a_result = callPH3AApi($data['cpf']);
    
    if ($ph3a_result['success']) {
        $ph3a_json = json_decode($ph3a_result['response'], true);
        
        if ($ph3a_json && $ph3a_json['codigo'] == 1 && isset($ph3a_json['data'])) {
            $ph3a_data = $ph3a_json['data'];
            
            // Mapear sexo
            if (empty($data['sexo']) && isset($ph3a_data['sexo'])) {
                $data['sexo'] = ($ph3a_data['sexo'] == 1) ? 'Masculino' : 'Feminino';
                echo "✅ SEXO preenchido: " . $data['sexo'] . "\n";
            }
            
            // Mapear estado civil
            if (empty($data['estado_civil']) && isset($ph3a_data['estado_civil'])) {
                $estado_civil_map = [0 => 'Solteiro', 1 => 'Casado', 2 => 'Divorciado', 3 => 'Viúvo'];
                $data['estado_civil'] = $estado_civil_map[$ph3a_data['estado_civil']] ?? '';
                if ($data['estado_civil']) {
                    echo "✅ ESTADO-CIVIL preenchido: " . $data['estado_civil'] . "\n";
                }
            }
            
            // Mapear data de nascimento (ISO para DD/MM/YYYY)
            if (empty($data['data_nascimento']) && isset($ph3a_data['data_nascimento'])) {
                try {
                    $date = new DateTime($ph3a_data['data_nascimento']);
                    $data['data_nascimento'] = $date->format('d/m/Y');
                    echo "✅ DATA-DE-NASCIMENTO preenchida: " . $data['data_nascimento'] . "\n";
                } catch (Exception $e) {
                    $data['data_nascimento'] = $ph3a_data['data_nascimento'];
                    echo "✅ DATA-DE-NASCIMENTO preenchida (formato original): " . $data['data_nascimento'] . "\n";
                }
            }
        } else {
            echo "⚠️ PH3A: CPF válido mas não encontrado na base\n";
        }
    } else {
        echo "❌ PH3A: Falha na consulta - " . $ph3a_result['error'] . "\n";
    }
} else {
    echo "✅ PH3A: Campos já preenchidos ou CPF vazio\n";
}

$ph3a_time = microtime(true) - $start_time;
echo "⏱️ Tempo PH3A: " . round($ph3a_time, 3) . "s\n";

// ========================================
// ETAPA 2: CHAMAR WEBHOOKS PRIMEIRO
// ========================================
$webhooks_start = microtime(true);
echo "\n🚀 ETAPA 2: CHAMANDO WEBHOOKS PRIMEIRO\n";
echo "========================================\n";

// Prepare webhook data for both webhooks
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

// Function to call webhook
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

// Call both webhooks FIRST
$webhook_results = [];
$webhook_success_count = 0;

echo "📞 Chamando add_travelangels.php (EspoCRM)...\n";
$travelangels_result = callWebhook('https://mdmidia.com.br/add_travelangels.php', $webhook_data);
$webhook_results['travelangels'] = $travelangels_result;

if ($travelangels_result['success']) {
    $webhook_success_count++;
    echo "✅ EspoCRM: Lead criado com sucesso\n";
} else {
    echo "❌ EspoCRM: Falha - " . $travelangels_result['error'] . "\n";
}

echo "📱 Chamando add_webflow_octa.php (Octadesk)...\n";
$octa_result = callWebhook('https://mdmidia.com.br/add_webflow_octa.php', $webhook_data);
$webhook_results['octadesk'] = $octa_result;

if ($octa_result['success']) {
    $webhook_success_count++;
    echo "✅ Octadesk: Mensagem WhatsApp enviada\n";
} else {
    echo "❌ Octadesk: Falha - " . $octa_result['error'] . "\n";
}

echo "📊 Resultado dos Webhooks: $webhook_success_count/2 sucessos\n";

$webhooks_time = microtime(true) - $webhooks_start;
echo "⏱️ Tempo Webhooks: " . round($webhooks_time, 3) . "s\n";

// Log webhook results
$log_data = [
    'session_id' => $session_id,
    'timestamp' => date('c'),
    'performance' => [
        'ph3a_time' => round($ph3a_time, 3),
        'webhooks_time' => round($webhooks_time, 3),
        'rpa_time' => round($rpa_time, 3),
        'total_time' => round($total_time, 3)
    ],
    'ph3a_result' => $ph3a_result ?? null,
    'ph3a_data' => $ph3a_data ?? null,
    'campos_ph3a_vazios' => $campos_ph3a_vazios ?? [],
    'webhook_results' => $webhook_results,
    'webhook_success_count' => $webhook_success_count,
    'input_data' => $data
];

$log_file = "/opt/imediatoseguros-rpa/logs/webhook_calls_" . date('Y-m-d') . ".log";
file_put_contents($log_file, json_encode($log_data) . "\n", FILE_APPEND | LOCK_EX);

// ========================================
// ETAPA 2: INICIAR RPA APÓS WEBHOOKS
// ========================================
$rpa_start = microtime(true);
echo "\n🤖 ETAPA 2: INICIANDO RPA APÓS WEBHOOKS\n";
echo "========================================\n";

// Start RPA process
$rpa_command = "cd /opt/imediatoseguros-rpa && source venv/bin/activate && python executar_rpa_imediato_playwright.py '" . json_encode($data) . "' > /dev/null 2>&1 & echo $!";
$rpa_pid = shell_exec($rpa_command);
$rpa_pid = trim($rpa_pid);

if ($rpa_pid) {
    echo "✅ RPA iniciado com PID: $rpa_pid\n";
} else {
    echo "❌ Falha ao iniciar RPA\n";
}

$rpa_time = microtime(true) - $rpa_start;
echo "⏱️ Tempo RPA: " . round($rpa_time, 3) . "s\n";

$total_time = microtime(true) - $start_time;
echo "⏱️ Tempo Total: " . round($total_time, 3) . "s\n";

// Save session info
$session_info = [
    'session_id' => $session_id,
    'rpa_pid' => $rpa_pid,
    'status' => 'started',
    'started_at' => date('c'),
    'webhook_results' => $webhook_results,
    'webhook_success_count' => $webhook_success_count,
    'execution_order' => 'webhooks_first_then_rpa'
];

$session_file = "/opt/imediatoseguros-rpa/sessions/$session_id/status.json";
if (!is_dir(dirname($session_file))) {
    mkdir(dirname($session_file), 0755, true);
}
file_put_contents($session_file, json_encode($session_info, JSON_PRETTY_PRINT));

// Return response
$response = [
    'success' => true,
    'session_id' => $session_id,
    'message' => 'PH3A consultado, webhooks executados e RPA iniciado com sucesso',
    'performance' => [
        'ph3a_time' => round($ph3a_time, 3),
        'webhooks_time' => round($webhooks_time, 3),
        'rpa_time' => round($rpa_time, 3),
        'total_time' => round($total_time, 3)
    ],
    'ph3a_consulted' => !empty($campos_ph3a_vazios) && !empty($data['cpf']),
    'ph3a_fields_filled' => array_diff(['sexo', 'data_nascimento', 'estado_civil'], $campos_ph3a_vazios ?? []),
    'webhook_results' => $webhook_results,
    'webhook_success_count' => $webhook_success_count,
    'rpa_pid' => $rpa_pid,
    'execution_order' => 'ph3a_then_webhooks_then_rpa',
    'timestamp' => date('c')
];

http_response_code(200);
echo json_encode($response, JSON_PRETTY_PRINT);
?>
```

---

### **FASE 3: JAVASCRIPT SIMPLIFICADO PARA WEBFLOW**

#### **3.1 Status do JavaScript Existente**
✅ **GCLID JÁ CAPTURADO** - Não é necessário criar novo código de captura

**Arquivo existente**: `Inside Head Tag Pagina.js`
- ✅ Captura GCLID da URL
- ✅ Salva em cookie por 90 dias
- ✅ Preenche automaticamente campos `name="GCLID_FLD"`
- ✅ Armazena no localStorage

#### **3.2 JavaScript Simplificado para Integração RPA**
```javascript
// RPA Integration v6.9.0 - Webflow Integration (Simplificado)
const RPAIntegration = {
    // Configurações
    config: {
        apiBaseUrl: 'https://rpaimediatoseguros.com.br',
        webhookUrls: {
            rpaStart: 'https://rpaimediatoseguros.com.br/api/rpa/start',
            rpaProgress: 'https://rpaimediatoseguros.com.br/api/rpa/progress'
        },
        pollingInterval: 2000, // 2 segundos
        maxPolls: 90, // 3 minutos (180 segundos)
        timeoutMessage: 'O cálculo está demorando mais que o esperado. Tente novamente em alguns minutos.'
    },
    
    // Coletar dados do formulário (GCLID já preenchido automaticamente)
    collectFormData() {
        const form = document.getElementById('cotacaoForm');
        if (!form) {
            throw new Error('Formulário de cotação não encontrado');
        }
        
        const formData = new FormData(form);
        const data = {};
        
        // Coletar todos os campos do formulário (incluindo GCLID_FLD já preenchido)
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Validar campos obrigatórios
        const requiredFields = ['cpf', 'nome', 'placa', 'cep', 'email', 'telefone'];
        const missingFields = requiredFields.filter(field => !data[field]);
        
        if (missingFields.length > 0) {
            throw new Error(`Campos obrigatórios não preenchidos: ${missingFields.join(', ')}`);
        }
        
        return data;
    },
    
    // Iniciar RPA
    async startRPA(formData) {
        try {
            const response = await fetch(this.config.webhookUrls.rpaStart, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            if (!data.success) {
                throw new Error(data.message || 'Erro ao iniciar RPA');
            }
            
            return data.session_id;
        } catch (error) {
            console.error('Erro ao iniciar RPA:', error);
            throw error;
        }
    },
    
    // Monitorar progresso
    async getProgress(sessionId) {
        try {
            const response = await fetch(`${this.config.webhookUrls.rpaProgress}/${sessionId}`);
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.message || 'Erro ao obter progresso');
            }
            
            return data.progress;
        } catch (error) {
            console.error('Erro ao obter progresso:', error);
            throw error;
        }
    },
    
    // Função principal de execução
    async execute() {
        try {
            // 1. Coletar dados do formulário (GCLID já incluído)
            const formData = this.collectFormData();
            console.log('Dados coletados:', formData);
            
            // 2. Abrir modal de progresso
            this.openProgressModal();
            
            // 3. Iniciar RPA
            const sessionId = await this.startRPA(formData);
            console.log('Sessão RPA criada:', sessionId);
            
            // 4. Monitorar progresso
            let pollCount = 0;
            const progressInterval = setInterval(async () => {
                try {
                    pollCount++;
                    const progress = await this.getProgress(sessionId);
                    
                    // Atualizar interface
                    this.updateProgressUI(progress);
                    
                    // Verificar conclusão
                    if (progress.status === 'success') {
                        clearInterval(progressInterval);
                        this.showResults(progress.resultados_finais);
                        return;
                    }
                    
                    // Verificar timeout
                    if (pollCount >= this.config.maxPolls) {
                        clearInterval(progressInterval);
                        this.showTimeout();
                    }
                    
                } catch (error) {
                    clearInterval(progressInterval);
                    this.showError('Erro no monitoramento: ' + error.message);
                }
            }, this.config.pollingInterval);
            
        } catch (error) {
            console.error('Erro na execução:', error);
            this.showError('Erro ao iniciar cálculo: ' + error.message);
        }
    },
    
    // Métodos de interface (implementar conforme necessário)
    openProgressModal() {
        console.log('Abrindo modal de progresso...');
    },
    
    updateProgressUI(progress) {
        console.log('Atualizando progresso:', progress);
    },
    
    showResults(results) {
        console.log('Exibindo resultados:', results);
    },
    
    showError(message) {
        console.error('Erro:', message);
        alert('Erro: ' + message);
    },
    
    showTimeout() {
        console.warn('Timeout atingido');
        alert(this.config.timeoutMessage);
    }
};

// Event listener para o formulário
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cotacaoForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            await RPAIntegration.execute();
        });
    }
});
```

---

### **FASE 4: ESTRUTURA DE ARQUIVOS**

#### **4.1 Arquivos a serem Criados/Modificados**
```
/opt/imediatoseguros-rpa-v4/
├── public/
│   └── api/
│       └── rpa/
│           ├── start.php                 # ✅ MODIFICADO - Endpoint com webhooks
│           └── progress.php              # ✅ EXISTENTE - Manter como está
├── logs/
│   └── webhook_calls_YYYY-MM-DD.log     # ✅ NOVO - Logs de webhooks
└── sessions/
    └── {session_id}/
        └── status.json                   # ✅ EXISTENTE - Manter como está
```

#### **4.2 Configuração do Webflow**
```
Webflow Designer:
├── Formulário de Cotação
│   ├── Campos visíveis (CPF, Nome, Placa, etc.)
│   └── Campos ocultos:
│       ├── GCLID_FLD                    # ✅ JÁ EXISTE - Preenchido automaticamente
│       ├── utm_source                   # ✅ OPCIONAL - Para tracking adicional
│       ├── utm_medium                   # ✅ OPCIONAL - Para tracking adicional
│       ├── utm_campaign                 # ✅ OPCIONAL - Para tracking adicional
│       ├── utm_term                     # ✅ OPCIONAL - Para tracking adicional
│       ├── utm_content                  # ✅ OPCIONAL - Para tracking adicional
│       └── landing_url                  # ✅ OPCIONAL - Para tracking adicional
└── Custom Code (Before </body> tag)
    └── rpa-integration-v6.9.0.js       # ✅ NOVO - Script simplificado
```

#### **4.3 Status dos Arquivos JavaScript Existentes**
```
Arquivos Webflow Existentes:
├── Inside Head Tag Pagina.js           # ✅ JÁ IMPLEMENTADO - Captura GCLID
├── Footer Code Site.js                 # ✅ JÁ IMPLEMENTADO - Usa GCLID no WhatsApp
└── Head code Site.js                   # ✅ JÁ IMPLEMENTADO - GTM e configurações
```

---

### **FASE 5: TESTES E VALIDAÇÃO**

#### **5.1 Testes de Webhook**
```bash
# Teste 1: Verificar se webhooks recebem dados corretamente
curl -X POST https://mdmidia.com.br/add_travelangels.php \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "NOME": "Teste",
      "DDD-CELULAR": "11",
      "CELULAR": "999999999",
      "Email": "teste@email.com",
      "CEP": "01234567",
      "CPF": "12345678901",
      "PLACA": "ABC1234",
      "GCLID_FLD": "test-gclid"
    },
    "d": "2025-01-10T15:30:00Z",
    "name": "Teste"
  }'

# Teste 2: Verificar se webhooks respondem corretamente
curl -X POST https://mdmidia.com.br/add_webflow_octa.php \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "NOME": "Teste",
      "DDD-CELULAR": "11",
      "CELULAR": "999999999",
      "Email": "teste@email.com",
      "CPF": "12345678901",
      "PLACA": "ABC1234",
      "GCLID_FLD": "test-gclid"
    }
  }'
```

#### **5.2 Testes de API RPA**
```bash
# Teste 3: Verificar se API RPA chama webhooks corretamente
curl -X POST https://rpaimediatoseguros.com.br/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "Teste",
    "placa": "ABC1234",
    "cep": "01234567",
    "email": "teste@email.com",
    "telefone": "11999999999",
    "gclid": "test-gclid-123"
  }'
```

#### **5.3 Testes de GCLID**
```bash
# Teste 4: Verificar se GCLID é capturado corretamente
# Acessar: https://segurosimediato.com.br/cotacao?gclid=test-gclid-123
# Verificar se campo GCLID_FLD é preenchido automaticamente
```

---

### **FASE 6: MONITORAMENTO E LOGS**

#### **6.1 Logs de Webhook**
```php
// Estrutura do log de webhook
{
  "session_id": "rpa_v6.9.0_20250110_153000_abc12345",
  "timestamp": "2025-01-10T15:30:00Z",
  "webhook_results": {
    "travelangels": {
      "success": true,
      "http_code": 200,
      "response": "...",
      "error": null
    },
    "octadesk": {
      "success": true,
      "http_code": 200,
      "response": "...",
      "error": null
    }
  },
  "input_data": {
    "cpf": "12345678901",
    "nome": "João Silva",
    "gclid": "Cj0KCQiA..."
  }
}
```

#### **6.2 Monitoramento de Erros**
```bash
# Verificar logs de webhook
tail -f /opt/imediatoseguros-rpa/logs/webhook_calls_$(date +%Y-%m-%d).log

# Verificar logs do RPA
tail -f /opt/imediatoseguros-rpa/logs/rpa_v6.9.0_*.log

# Verificar status das sessões
ls -la /opt/imediatoseguros-rpa/sessions/
```

---

## 🎯 **RESULTADO ESPERADO**

### **📊 FLUXO COMPLETO - PH3A + WEBHOOKS PRIMEIRO**
1. **Usuário preenche formulário** no Webflow
2. **JavaScript captura GCLID e UTM** parameters
3. **Formulário é enviado** para API RPA
4. **🔍 ETAPA 1: API RPA consulta PH3A** (se campos em branco):
   - **📋 SEXO**: Preenchido automaticamente
   - **📅 DATA-DE-NASCIMENTO**: Preenchida automaticamente
   - **💍 ESTADO-CIVIL**: Preenchido automaticamente
5. **🚀 ETAPA 2: API RPA chama IMEDIATAMENTE** os 2 webhooks:
   - **📞 EspoCRM**: Lead criado instantaneamente
   - **📱 Octadesk**: Mensagem WhatsApp enviada imediatamente
6. **🤖 ETAPA 3: RPA processa cotação** em background
7. **Resultados são exibidos** no modal

### **🚀 BENEFÍCIOS**
1. **🔍 Dados completos**: PH3A preenche campos automaticamente
2. **⚡ Resposta imediata**: Cliente recebe WhatsApp instantaneamente
3. **📊 CRM atualizado**: EspoCRM sensibilizado antes do RPA
4. **🎯 Melhor UX**: Feedback imediato para o usuário
5. **🛡️ Dados protegidos**: Lead salvo mesmo se RPA falhar
6. **📈 Métricas precisas**: Conversão registrada imediatamente
7. **🔄 Processo paralelo**: PH3A, webhooks e RPA executam independentemente
8. **📝 Logs detalhados** para debugging e monitoramento

### **📈 MÉTRICAS DE SUCESSO**
- **Taxa de sucesso PH3A**: >90%
- **Taxa de sucesso dos webhooks**: >95%
- **Tempo de resposta PH3A**: <3 segundos
- **Tempo de resposta webhooks**: <2 segundos
- **Tempo de resposta WhatsApp**: <5 segundos
- **Captura de GCLID**: 100% dos casos
- **Compatibilidade**: 100% com sistema atual
- **Ordem de execução**: PH3A → Webhooks → RPA

---

## 📋 **PENDÊNCIAS PARA FASE 2**

### **🔒 MELHORIAS DE SEGURANÇA**
- [ ] **Rate limiting por IP**: Proteção contra spam e ataques DDoS
- [ ] **Autenticação API**: API keys ou JWT para acesso
- [ ] **Criptografia de dados sensíveis**: Proteção adicional de CPF e dados pessoais
- [ ] **Auditoria de acesso**: Log de todas as operações sensíveis
- [ ] **Validação de origem**: Verificação de headers e tokens

### **⚡ OTIMIZAÇÕES DE PERFORMANCE**
- [ ] **Cache PH3A**: Implementar Redis/Memcached para evitar consultas repetidas
- [ ] **Processamento assíncrono**: Queues como Redis para webhooks
- [ ] **Connection pooling**: Reutilização de conexões HTTP
- [ ] **Compressão gzip**: Redução do tamanho das respostas
- [ ] **CDN**: Aceleração de conteúdo estático

### **🛡️ TRATAMENTO DE ERROS AVANÇADO**
- [ ] **Retry logic**: Tentativas automáticas com backoff exponencial
- [ ] **Circuit breaker**: Proteção contra serviços externos instáveis
- [ ] **Alertas automáticos**: Notificações para falhas críticas
- [ ] **Rollback automático**: Capacidade de reverter para versão anterior
- [ ] **Dead letter queue**: Processamento de falhas persistentes

### **📊 MONITORAMENTO E OBSERVABILIDADE**
- [ ] **Health checks**: Endpoints para verificação de saúde do sistema
- [ ] **Métricas detalhadas**: Prometheus/Grafana para monitoramento
- [ ] **Distributed tracing**: Rastreamento completo de requisições
- [ ] **Alertas proativos**: Notificações antes de problemas críticos
- [ ] **Dashboard em tempo real**: Visualização do status do sistema

### **🧪 TESTES E QUALIDADE**
- [ ] **Testes unitários**: Implementar testes unitários básicos para funções como callWebhook usando PHPUnit
- [ ] **Testes de integração**: Validação completa do fluxo end-to-end
- [ ] **Testes de carga**: Simulação de tráfego real com K6/JMeter
- [ ] **Testes de segurança**: Validação contra vulnerabilidades OWASP
- [ ] **Ambiente de staging**: Testes completos antes da produção

### **📚 DOCUMENTAÇÃO E MANUTENÇÃO**
- [ ] **Swagger/OpenAPI**: Documentação completa da API
- [ ] **Runbooks operacionais**: Procedimentos detalhados para operação
- [ ] **Diagramas de arquitetura**: Visualização atualizada do sistema
- [ ] **Changelog automatizado**: Registro de todas as mudanças
- [ ] **Versionamento semântico**: Controle rigoroso de versões

### **🚀 MELHORIAS FUTURAS**
- [ ] **Integração com ferramentas modernas**: Migração para GraphQL ou Google Tag Manager para UTM/GCLID
- [ ] **Escalabilidade horizontal**: Containerização com Docker ou auto-scaling
- [ ] **Microserviços**: Separação de responsabilidades
- [ ] **CI/CD**: Pipeline automatizado de deploy
- [ ] **Backup automático**: Proteção de dados críticos
- [ ] **Disaster recovery**: Plano de recuperação de desastres

### **⚠️ IMPORTANTE**
- **Status**: Todas as pendências estão marcadas como **PENDENTE**
- **Autorização**: Implementação requer aprovação explícita do cliente
- **Prioridade**: Foco na estabilização da Fase 1 antes de avançar
- **Cronograma**: A ser definido após validação da Fase 1 em produção

---

## ⚠️ **RISCOS E MITIGAÇÕES**

### **🚨 RISCOS IDENTIFICADOS**
1. **Falha nos webhooks**: Webhooks existentes podem estar indisponíveis
2. **Timeout de RPA**: Processo RPA pode demorar mais que 3 minutos
3. **Dados inválidos**: Campos obrigatórios podem estar vazios
4. **Conflito de sessões**: Múltiplas execuções simultâneas

### **🛡️ MITIGAÇÕES**
1. **Fallback gracioso**: Continuar RPA mesmo se webhook falhar
2. **Timeout configurável**: Ajustar tempo limite conforme necessário
3. **Validação rigorosa**: Verificar campos obrigatórios antes de enviar
4. **Session management**: Isolar execuções por session_id

---

## 📋 **CHECKLIST DE IMPLEMENTAÇÃO**

### **✅ PREPARAÇÃO**
- [ ] Backup completo do sistema atual
- [ ] Análise dos webhooks existentes concluída
- [ ] Estrutura JSON documentada
- [ ] Scripts de teste preparados

### **✅ IMPLEMENTAÇÃO**
- [ ] Endpoint API RPA modificado
- [ ] JavaScript Webflow implementado
- [ ] Campos ocultos adicionados ao formulário
- [ ] Logs de webhook configurados

### **✅ TESTES**
- [ ] Testes de webhook executados
- [ ] Testes de API RPA executados
- [ ] Testes de GCLID executados
- [ ] Testes de integração completos

### **✅ DEPLOY**
- [ ] Código deployado em produção
- [ ] Webflow atualizado
- [ ] Monitoramento ativado
- [ ] Documentação atualizada

---

### **FASE 7: MODIFICAÇÃO DOS ARQUIVOS HTML DE TESTE**

#### **7.1 Modificação do index.html Principal**
**Arquivo**: `index.html`
**Modificação**: Adicionar campo oculto GCLID_FLD com valor padrão "TesteRPA123"

```html
<!-- Adicionar após a linha 422 (antes do botão de ação) -->
<!-- Campos Ocultos para Tracking -->
<div style="display: none;">
    <input type="hidden" id="GCLID_FLD" name="GCLID_FLD" value="TesteRPA123">
    <input type="hidden" id="utm_source" name="utm_source" value="">
    <input type="hidden" id="utm_medium" name="utm_medium" value="">
    <input type="hidden" id="utm_campaign" name="utm_campaign" value="">
    <input type="hidden" id="utm_term" name="utm_term" value="">
    <input type="hidden" id="utm_content" name="utm_content" value="">
    <input type="hidden" id="landing_url" name="landing_url" value="">
</div>
```

#### **7.2 Modificação do teste_js_atualizado.html**
**Arquivo**: `teste_js_atualizado.html`
**Modificação**: Adicionar campo oculto GCLID_FLD com valor padrão "TesteRPA123"

```html
<!-- Adicionar após a linha 24 (após o campo placa) -->
<!-- Campo Oculto para GCLID -->
<input type="hidden" id="GCLID_FLD" name="GCLID_FLD" value="TesteRPA123">
```

#### **7.3 Status do JavaScript Existente**
**Arquivo**: `Inside Head Tag Pagina.js`
**Status**: ✅ **JÁ IMPLEMENTADO** - Não é necessário modificar

**Funcionalidades já existentes**:
- ✅ Captura GCLID da URL (`gclid`, `GCLID`, `gclId`)
- ✅ Captura GBRAID da URL (`gbraid`, `GBRAID`, `gBraid`)
- ✅ Salva em cookie por 90 dias
- ✅ Preenche automaticamente campos `name="GCLID_FLD"`
- ✅ Armazena no localStorage
- ✅ Usado nos links do WhatsApp

**Código existente** (linhas 14-26):
```javascript
// Captura gclid OU gbraid (qualquer um dos dois)
var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");

// Define prioridade: se gclid existir, usa ele. Se não, usa gbraid.
var trackingId = gclid || gbraid;

if (trackingId) {
  var gclsrc = getParam("gclsrc");
  if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
    setCookie("gclid", trackingId, 90); // ✅ SALVA EM COOKIE POR 90 DIAS
  }
}
```

**Preenchimento automático** (linhas 40-44):
```javascript
document.addEventListener("DOMContentLoaded", function () {
  const gclidFields = document.getElementsByName("GCLID_FLD");
  for (var i = 0; i < gclidFields.length; i++) {
    gclidFields[i].value = readCookie("gclid"); // ✅ PREENCHE AUTOMATICAMENTE
  }
});
```

#### **7.4 Estrutura HTML Atualizada**
```html
<!-- Exemplo de formulário completo com campos ocultos -->
<form id="rpa-form" class="rpa-form">
    <!-- Campos visíveis existentes -->
    <input type="text" id="CPF" name="CPF" required>
    <input type="text" id="nome" name="nome" required>
    <!-- ... outros campos ... -->
    
    <!-- Campos Ocultos para Tracking -->
    <div style="display: none;">
        <input type="hidden" id="GCLID_FLD" name="GCLID_FLD" value="TesteRPA123">
        <input type="hidden" id="utm_source" name="utm_source" value="">
        <input type="hidden" id="utm_medium" name="utm_medium" value="">
        <input type="hidden" id="utm_campaign" name="utm_campaign" value="">
        <input type="hidden" id="utm_term" name="utm_term" value="">
        <input type="hidden" id="utm_content" name="utm_content" value="">
        <input type="hidden" id="landing_url" name="landing_url" value="">
    </div>
    
    <!-- Botão de envio -->
    <button type="submit">CALCULE AGORA!</button>
</form>
```

#### **7.5 Teste de Funcionamento do GCLID Existente**
```javascript
// Teste para verificar se GCLID está sendo capturado automaticamente
function testarGCLIDExistente() {
    console.log('🔍 Testando captura automática de GCLID...');
    
    // Verificar campo GCLID_FLD (preenchido automaticamente)
    var gclidField = document.getElementById('GCLID_FLD');
    if (gclidField) {
        console.log('✅ Campo GCLID_FLD encontrado:', gclidField.value);
        
        // Verificar se está preenchido automaticamente
        if (gclidField.value) {
            console.log('✅ GCLID capturado automaticamente:', gclidField.value);
        } else {
            console.log('⚠️ Campo GCLID_FLD vazio - aguardando captura...');
        }
    } else {
        console.error('❌ Campo GCLID_FLD não encontrado!');
    }
    
    // Verificar cookie do GCLID
    var gclidCookie = (document.cookie.match(/(^|;)\s*gclid=([^;]+)/) || [])[2];
    if (gclidCookie) {
        console.log('✅ GCLID salvo em cookie:', decodeURIComponent(gclidCookie));
    } else {
        console.log('⚠️ GCLID não encontrado em cookie');
    }
    
    // Verificar localStorage
    var gclidLocalStorage = window.localStorage.getItem('GCLID_FLD');
    if (gclidLocalStorage) {
        console.log('✅ GCLID salvo no localStorage:', gclidLocalStorage);
    } else {
        console.log('⚠️ GCLID não encontrado no localStorage');
    }
}

// Executar teste quando página carregar
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(testarGCLIDExistente, 1000); // Aguardar 1 segundo
});
```

---

## 📦 **BACKUP DE SEGURANÇA CRIADO**

### **📅 INFORMAÇÕES DO BACKUP**
- **Data/Hora**: 2025-10-09 às 09:11:20
- **Diretório**: `backup_2025-10-09_09-11-20/`
- **Motivo**: Backup de segurança antes das modificações do projeto

### **📋 ARQUIVOS BACKUPADOS**
| Arquivo Original | Arquivo Backup | Tamanho | Status |
|------------------|----------------|---------|--------|
| `index.html` | `index.html.backup` | 17.755 bytes | ✅ Backup criado |
| `teste_js_atualizado.html` | `teste_js_atualizado.html.backup` | 3.765 bytes | ✅ Backup criado |
| `PROJETO_INTEGRACAO_WEBHOOKS_RPA_V6.9.0.md` | `PROJETO_INTEGRACAO_WEBHOOKS_RPA_V6.9.0.md.backup` | 54.949 bytes | ✅ Backup criado |

### **🔄 PROCESSO DE RESTAURAÇÃO**
```bash
# Restaurar arquivos originais se necessário
Copy-Item "backup_2025-10-09_09-11-20\index.html.backup" "index.html"
Copy-Item "backup_2025-10-09_09-11-20\teste_js_atualizado.html.backup" "teste_js_atualizado.html"
Copy-Item "backup_2025-10-09_09-11-20\PROJETO_INTEGRACAO_WEBHOOKS_RPA_V6.9.0.md.backup" "PROJETO_INTEGRACAO_WEBHOOKS_RPA_V6.9.0.md"
```

---

## 📝 **PRÓXIMOS PASSOS**

1. **🔧 Implementar endpoint modificado** da API RPA (`start.php`)
2. **📝 Adicionar campo oculto GCLID_FLD** ao formulário Webflow
3. **🌐 Implementar JavaScript simplificado** para integração RPA
4. **✅ Modificar arquivos HTML** de teste com campo GCLID_FLD
5. **🧪 Executar testes** de integração
6. **📊 Monitorar logs** e performance
7. **📋 Documentar** resultados e ajustes

### **🎯 RESUMO DAS ALTERAÇÕES NECESSÁRIAS**

#### **✅ O QUE JÁ EXISTE (NÃO PRECISA ALTERAR)**
- **GCLID capturado automaticamente** no Webflow
- **JavaScript de captura** já implementado
- **Armazenamento em cookie** por 90 dias
- **Preenchimento automático** de campos `name="GCLID_FLD"`
- **Uso nos links WhatsApp** já funcionando

#### **🔧 O QUE PRECISA SER IMPLEMENTADO**
- **Endpoint RPA modificado** (`start.php`) com webhooks
- **Campo oculto GCLID_FLD** no formulário Webflow
- **JavaScript simplificado** para integração RPA
- **Arquivos HTML de teste** atualizados
- **Logs de webhook** configurados

---

**📅 Data de Criação**: 2025-01-10  
**👤 Responsável**: Sistema RPA Imediato Seguros  
**🏷️ Versão**: V6.9.0  
**📋 Status**: Pronto para Implementação

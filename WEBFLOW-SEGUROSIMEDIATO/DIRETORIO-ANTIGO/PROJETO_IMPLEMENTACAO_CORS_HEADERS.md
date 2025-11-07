# PROJETO: IMPLEMENTAÇÃO DE CORS HEADERS NOS ENDPOINTS DE DESENVOLVIMENTO

**Data de Criação:** 29/10/2025  
**Versão:** 1.0  
**Status:** Planejamento (NÃO EXECUTAR)

---

## 📋 OBJETIVO

Implementar headers CORS nos endpoints `add_travelangels_dev.php` e `add_webflow_octa_dev.php` para permitir requisições cross-origin do Webflow, resolvendo os erros de bloqueio CORS no navegador.

---

## 🎯 PROBLEMA ATUAL

Os endpoints retornam erro CORS quando chamados do Webflow:
```
Access to fetch at 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php' 
from origin 'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io' 
has been blocked by CORS policy: Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos a Modificar:
1. `C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\dev\webhooks\add_travelangels_dev.php`
2. `C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\dev\webhooks\add_webflow_octa_dev.php`

### Backups Criados:
- ✅ `add_travelangels_dev.php.backup_20251029_182917`
- ✅ `add_webflow_octa_dev.php.backup_20251029_182917`

### Destino no Servidor:
- `/var/www/html/dev/webhooks/add_travelangels_dev.php`
- `/var/www/html/dev/webhooks/add_webflow_octa_dev.php`

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DAS ALTERAÇÕES

### 1.1. Alteração em `add_travelangels_dev.php`

**Localização:** Após a linha 12 (após `require_once dev_config.php`), **ANTES** da linha 14 (`validateDevEnvironment()`)

**Motivo:** Os headers CORS devem ser enviados **ANTES** de qualquer `exit()`, `validateDevEnvironment()` ou outros headers existentes.

**Código a Adicionar:**
```php
// ==================== CONFIGURAÇÃO CORS ====================
// Permitir requisições do Webflow staging, produção e dev.bpsegurosimediato.com.br
$allowed_origins = array(
    'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io',
    'https://www.segurosimediato.com.br',
    'https://segurosimediato.com.br',
    'https://dev.bpsegurosimediato.com.br',
    'http://localhost',
    'http://localhost:8080'
);

$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
if (in_array($origin, $allowed_origins)) {
    header('Access-Control-Allow-Origin: ' . $origin);
}

header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Webflow-Signature, X-Webflow-Timestamp, X-Requested-With');
header('Access-Control-Allow-Credentials: true');
header('Access-Control-Max-Age: 86400'); // 24 horas

// Responder a requisições OPTIONS (preflight) - DEVE VIR ANTES DE validateDevEnvironment()
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}
// ==================== FIM CONFIGURAÇÃO CORS ====================
```

**Linhas Exatas:**
- **Inserir após:** Linha 12 (`require_once __DIR__ . '/../config/dev_config.php';`)
- **Inserir antes:** Linha 14 (`validateDevEnvironment();`)

---

### 1.2. Alteração em `add_webflow_octa_dev.php`

**Localização:** Após a linha 12 (após `require_once dev_config.php`), **ANTES** da linha 14 (função `logDevWebhook`)

**Código a Adicionar:**
```php
// ==================== CONFIGURAÇÃO CORS ====================
// Permitir requisições do Webflow staging, produção e dev.bpsegurosimediato.com.br
$allowed_origins = array(
    'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io',
    'https://www.segurosimediato.com.br',
    'https://segurosimediato.com.br',
    'https://dev.bpsegurosimediato.com.br',
    'http://localhost',
    'http://localhost:8080'
);

$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
if (in_array($origin, $allowed_origins)) {
    header('Access-Control-Allow-Origin: ' . $origin);
}

header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Webflow-Signature, X-Webflow-Timestamp, X-Requested-With');
header('Access-Control-Allow-Credentials: true');
header('Access-Control-Max-Age: 86400'); // 24 horas

// Responder a requisições OPTIONS (preflight)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}
// ==================== FIM CONFIGURAÇÃO CORS ====================
```

**Linhas Exatas:**
- **Inserir após:** Linha 12 (`require_once __DIR__ . '/../config/dev_config.php';`)
- **Inserir antes:** Linha 14 (`function logDevWebhook`)

---

## 📤 FASE 2: CÓPIA DOS ARQUIVOS PARA O SERVIDOR

### 2.1. Verificar Conexão SSH

**Comando:**
```bash
ssh root@46.62.174.150 "echo 'Conexão OK'"
```

### 2.2. Criar Backup no Servidor (Antes de Copiar)

**Comandos:**
```bash
# Backup do add_travelangels_dev.php
ssh root@46.62.174.150 "cp /var/www/html/dev/webhooks/add_travelangels_dev.php /var/www/html/dev/webhooks/add_travelangels_dev.php.backup_$(date +%Y%m%d_%H%M%S)"

# Backup do add_webflow_octa_dev.php
ssh root@46.62.174.150 "cp /var/www/html/dev/webhooks/add_webflow_octa_dev.php /var/www/html/dev/webhooks/add_webflow_octa_dev.php.backup_$(date +%Y%m%d_%H%M%S)"
```

### 2.3. Copiar Arquivos Modificados

**Comandos SCP:**
```bash
# Copiar add_travelangels_dev.php
scp "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\dev\webhooks\add_travelangels_dev.php" root@46.62.174.150:/var/www/html/dev/webhooks/add_travelangels_dev.php

# Copiar add_webflow_octa_dev.php
scp "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\dev\webhooks\add_webflow_octa_dev.php" root@46.62.174.150:/var/www/html/dev/webhooks/add_webflow_octa_dev.php
```

### 2.4. Verificar Permissões

**Comando:**
```bash
ssh root@46.62.174.150 "chmod 644 /var/www/html/dev/webhooks/add_travelangels_dev.php /var/www/html/dev/webhooks/add_webflow_octa_dev.php"
```

---

## 🧪 FASE 3: ARQUIVO DE TESTE CORS PARA WINDOWS

### 3.1. Arquivo: `test_cors_endpoints.html`

**Localização:** `C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\dev\webhooks\test_cors_endpoints.html`

**Funcionalidades:**
- Teste de requisição OPTIONS (preflight)
- Teste de requisição POST real
- Validação de headers CORS na resposta
- Simulação de origem Webflow
- Exibição de resultados detalhados

**Estrutura do Teste:**
1. Teste Preflight (OPTIONS)
2. Teste POST com JSON válido
3. Verificação de headers CORS
4. Validação de resposta

---

### 3.2. Arquivo: `test_cors_endpoints.ps1` (PowerShell)

**Localização:** `C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\dev\webhooks\test_cors_endpoints.ps1`

**Funcionalidades:**
- Teste via PowerShell (Invoke-WebRequest)
- Teste de OPTIONS e POST
- Verificação programática de headers
- Geração de relatório

---

## ✅ FASE 4: TESTE E VERIFICAÇÃO

### 4.1. Testes Locais (Windows)

#### Teste 1: Arquivo HTML no Navegador
1. Abrir `test_cors_endpoints.html` no navegador
2. Clicar em "Testar CORS"
3. Verificar resultados no console
4. Verificar se headers CORS estão presentes

#### Teste 2: PowerShell
1. Executar `test_cors_endpoints.ps1`
2. Verificar output do script
3. Confirmar status 200 para OPTIONS
4. Confirmar status 200/400 para POST (400 pode ser esperado se faltar dados)

---

### 4.2. Testes no Servidor (via SSH)

#### Teste 1: Verificar Arquivos no Servidor
```bash
ssh root@46.62.174.150 "head -30 /var/www/html/dev/webhooks/add_travelangels_dev.php | grep -A 20 'CONFIGURAÇÃO CORS'"
```

#### Teste 2: Teste de Requisição OPTIONS
```bash
curl -X OPTIONS \
  -H "Origin: https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v \
  https://dev.bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php
```

**Resultado Esperado:**
- Status: 200
- Header: `Access-Control-Allow-Origin: https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io`
- Header: `Access-Control-Allow-Methods: POST, OPTIONS`

---

### 4.3. Testes no Webflow (Browser Console)

#### Teste 1: Preflight no Console
```javascript
fetch('https://dev.bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php', {
  method: 'OPTIONS',
  headers: {
    'Origin': 'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io',
    'Access-Control-Request-Method': 'POST',
    'Access-Control-Request-Headers': 'Content-Type'
  }
})
.then(r => {
  console.log('Status:', r.status);
  console.log('Headers CORS:', r.headers.get('Access-Control-Allow-Origin'));
  return r;
});
```

#### Teste 2: POST Real no Console
```javascript
fetch('https://dev.bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Origin': 'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io'
  },
  body: JSON.stringify({
    payload: JSON.stringify({
      data: {
        'NOME': 'Teste CORS',
        'Email': 'teste@cors.com',
        'DDD-CELULAR': '11',
        'CELULAR': '987654321'
      }
    })
  })
})
.then(r => r.json())
.then(data => console.log('Sucesso:', data))
.catch(err => console.error('Erro:', err));
```

---

### 4.4. Checklist de Verificação

**Após Implementação:**
- [ ] Headers CORS adicionados antes de qualquer `exit()`
- [ ] Tratamento de OPTIONS implementado corretamente
- [ ] Origem do Webflow na lista de permitidos
- [ ] Arquivos copiados para o servidor
- [ ] Backups criados (local e servidor)
- [ ] Teste OPTIONS retorna 200
- [ ] Headers CORS presentes na resposta OPTIONS
- [ ] POST não é bloqueado pelo navegador
- [ ] Console do navegador não mostra erro CORS
- [ ] Teste HTML funciona localmente

---

## 📝 ANOTAÇÕES IMPORTANTES

### ⚠️ PONTOS CRÍTICOS:

1. **Ordem dos Headers CORS:**
   - DEVE vir ANTES de `validateDevEnvironment()`
   - DEVE vir ANTES de qualquer `exit()` ou saída
   - DEVE vir ANTES dos outros headers existentes

2. **Tratamento de OPTIONS:**
   - Deve retornar 200 imediatamente
   - Deve fazer `exit(0)` para não processar além

3. **Validação de Origem:**
   - Usar `in_array()` para verificar origem permitida
   - NUNCA usar `*` em produção (segurança)

4. **Headers Necessários:**
   - `Access-Control-Allow-Origin` (específico por origem)
   - `Access-Control-Allow-Methods: POST, OPTIONS`
   - `Access-Control-Allow-Headers` (incluir X-Webflow-Signature e X-Webflow-Timestamp)
   - `Access-Control-Max-Age: 86400` (cache de preflight)

---

## 🔄 ROLLBACK (Se Necessário)

### Restaurar do Backup Local:
```bash
# No Windows
cp "add_travelangels_dev.php.backup_20251029_182917" "add_travelangels_dev.php"
cp "add_webflow_octa_dev.php.backup_20251029_182917" "add_webflow_octa_dev.php"
```

### Restaurar do Backup no Servidor:
```bash
# Via SSH
ssh root@46.62.174.150 "cp /var/www/html/dev/webhooks/add_travelangels_dev.php.backup_* /var/www/html/dev/webhooks/add_travelangels_dev.php"
ssh root@46.62.174.150 "cp /var/www/html/dev/webhooks/add_webflow_octa_dev.php.backup_* /var/www/html/dev/webhooks/add_webflow_octa_dev.php"
```

---

## 📊 CRONOGRAMA SUGERIDO

1. **Fase 1:** Implementação local (10 min)
2. **Fase 2:** Backup e cópia para servidor (5 min)
3. **Fase 3:** Criação dos arquivos de teste (15 min)
4. **Fase 4:** Execução dos testes (20 min)
5. **Validação:** Testes no Webflow real (10 min)

**Total Estimado:** ~60 minutos

---

## 🎯 RESULTADO ESPERADO

Após implementação:
- ✅ Requisições OPTIONS retornam 200 com headers CORS
- ✅ Requisições POST do Webflow não são bloqueadas
- ✅ Console do navegador não mostra erros CORS
- ✅ Endpoints respondem normalmente ao processamento
- ✅ Headers CORS presentes em todas as respostas

---

## 📌 PRÓXIMOS PASSOS (APÓS APROVAÇÃO)

1. Executar Fase 1 (Implementação)
2. Executar Fase 2 (Cópia para Servidor)
3. Criar arquivos de teste (Fase 3)
4. Executar testes (Fase 4)
5. Validar no Webflow real
6. Documentar resultados

---

**STATUS:** Projeto preparado e pronto para aprovação. **NÃO EXECUTAR ATÉ APROVAÇÃO.**












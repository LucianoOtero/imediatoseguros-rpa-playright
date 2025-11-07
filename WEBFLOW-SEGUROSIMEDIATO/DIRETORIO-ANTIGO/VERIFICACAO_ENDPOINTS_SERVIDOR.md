# 🔍 VERIFICAÇÃO DE ENDPOINTS NO SERVIDOR
## bpsegurosimediato.com.br

---

## 📋 RESUMO DOS CAMINHOS ENCONTRADOS NO CÓDIGO

Com base na análise dos arquivos de configuração e health checks, os caminhos esperados são:

### **🚀 PRODUÇÃO**

| Endpoint | Caminho no Servidor | URL HTTP |
|----------|---------------------|----------|
| **EspoCRM** | `/var/www/html/add_travelangels.php` | `https://bpsegurosimediato.com.br/add_travelangels.php` |
| **Octadesk** | `/var/www/html/add_webflow_octa.php` | `https://bpsegurosimediato.com.br/add_webflow_octa.php` |

### **🧪 DESENVOLVIMENTO**

| Endpoint | Caminho no Servidor | URL HTTP |
|----------|---------------------|----------|
| **EspoCRM** | `/var/www/html/dev/webhooks/add_travelangels.php` | `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php` |
| **Octadesk** | `/var/www/html/dev/webhooks/add_webflow_octa.php` | `https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php` |

---

## 📝 EVIDÊNCIAS ENCONTRADAS NO CÓDIGO

### **1. Arquivo `dev_config.php` (linhas 28-29)**
```php
$DEV_WEBHOOK_URLS = [
    'travelangels' => 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php',
    'octadesk' => 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php',
    'health' => 'https://bpsegurosimediato.com.br/dev/webhooks/health.php'
];
```

### **2. Arquivo `dev_webhooks_health.php` (linhas 39-40)**
```php
$dev_webhooks = [
    'travelangels_dev' => '/var/www/html/dev/webhooks/add_travelangels.php',
    'octadesk_dev' => '/var/www/html/dev/webhooks/add_webflow_octa.php',
    'health_dev' => '/var/www/html/dev/webhooks/health.php'
];
```

### **3. Arquivo `dev_health.php` (linhas 30-31 e 163-164)**
```php
// Desenvolvimento
'travelangels_dev' => '/var/www/html/dev/webhooks/add_travelangels.php',
'octadesk_dev' => '/var/www/html/dev/webhooks/add_webflow_octa.php',

// Produção (para comparação)
'travelangels_prod' => '/var/www/html/add_travelangels.php',
'octadesk_prod' => '/var/www/html/add_webflow_octa.php',
```

### **4. Arquivo `health.php` (linhas 31-32)**
```php
$webhooks = [
    'travelangels' => '/var/www/html/add_travelangels.php',
    'octadesk' => '/var/www/html/add_webflow_octa.php',
    'debug_logger' => '/var/www/html/debug_logger_db.php'
];
```

### **5. Arquivo `webhook_health.php` (linhas 22 e 27)**
```php
'travelangels' => [
    'file' => '/var/www/html/add_travelangels.php',
    'url' => 'https://bpsegurosimediato.com.br/add_travelangels.php'
],
'octadesk' => [
    'file' => '/var/www/html/add_webflow_octa.php',
    'url' => 'https://bpsegurosimediato.com.br/add_webflow_octa.php'
],
```

---

## ✅ CONCLUSÃO BASEADA NO CÓDIGO

**Os nomes dos arquivos NÃO possuem sufixo `_dev`:**

- ✅ `add_travelangels.php` (mesmo nome em dev e prod)
- ✅ `add_webflow_octa.php` (mesmo nome em dev e prod)

**A diferenciação é feita pelo caminho:**

- **DEV**: `/var/www/html/dev/webhooks/`
- **PROD**: `/var/www/html/`

---

## 🔍 COMANDOS PARA VERIFICAR NO SERVIDOR

Para confirmar se os arquivos realmente existem, execute no servidor:

### **Verificar arquivos de desenvolvimento:**
```bash
# Verificar se os arquivos existem
ls -la /var/www/html/dev/webhooks/add_travelangels.php
ls -la /var/www/html/dev/webhooks/add_webflow_octa.php

# Listar todo o diretório de desenvolvimento
ls -la /var/www/html/dev/webhooks/

# Verificar permissões
stat /var/www/html/dev/webhooks/add_travelangels.php
stat /var/www/html/dev/webhooks/add_webflow_octa.php
```

### **Verificar arquivos de produção:**
```bash
# Verificar se os arquivos existem
ls -la /var/www/html/add_travelangels.php
ls -la /var/www/html/add_webflow_octa.php

# Listar arquivos na raiz
ls -la /var/www/html/add_*.php
```

### **Verificar se há versões com `_dev`:**
```bash
# Procurar por arquivos com sufixo _dev
find /var/www/html -name "*_dev.php" -type f

# Procurar especificamente os endpoints
find /var/www/html -name "add_travelangels*" -type f
find /var/www/html -name "add_webflow_octa*" -type f
```

---

## 🧪 VERIFICAÇÃO VIA HTTP

Também é possível verificar se os endpoints respondem via HTTP:

### **Testar endpoints de desenvolvimento:**
```bash
# Testar EspoCRM DEV (deve retornar erro de método ou validação, não 404)
curl -X POST https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# Testar Octadesk DEV
curl -X POST https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### **Testar endpoints de produção:**
```bash
# Testar EspoCRM PROD
curl -X POST https://bpsegurosimediato.com.br/add_travelangels.php \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# Testar Octadesk PROD
curl -X POST https://bpsegurosimediato.com.br/add_webflow_octa.php \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

**Resposta esperada:**
- ✅ **200 ou 400**: Arquivo existe (erro de validação é esperado)
- ❌ **404**: Arquivo não encontrado

---

## 📊 ESTRUTURA ESPERADA NO SERVIDOR

```
/var/www/html/
├── add_travelangels.php          # ✅ PRODUÇÃO
├── add_webflow_octa.php          # ✅ PRODUÇÃO
├── dev/
│   ├── webhooks/
│   │   ├── add_travelangels.php  # ✅ DESENVOLVIMENTO
│   │   ├── add_webflow_octa.php  # ✅ DESENVOLVIMENTO
│   │   └── health.php
│   └── logs/
│       ├── travelangels_dev.txt
│       ├── octadesk_dev.txt
│       └── general_dev.txt
└── logs/                         # Logs de produção
```

---

## ⚠️ POSSÍVEIS VARIAÇÕES

Se os arquivos não existirem com os nomes esperados, verificar:

1. **Versões com `_dev` no nome:**
   - `/var/www/html/dev/webhooks/add_travelangels_dev.php`
   - `/var/www/html/dev/webhooks/add_webflow_octa_dev.php`

2. **Outras variações:**
   - `add_travelangels_v2.php`
   - `add_webflow_octa_v2.php`
   - `webhook_travelangels.php`
   - `webhook_octadesk.php`

---

## 📝 PRÓXIMOS PASSOS

1. **Executar comandos de verificação no servidor** (acima)
2. **Confirmar nomes exatos dos arquivos**
3. **Atualizar documentação se necessário**
4. **Atualizar código JavaScript com URLs corretas**

---

**Data de Criação**: 2025-01-23  
**Status**: ⏳ Aguardando verificação no servidor  
**Baseado em**: Análise dos arquivos de configuração e health checks












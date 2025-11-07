# 📋 GUIA DE CONSULTA DE LOGS DOS ENDPOINTS
## Referência Completa para Verificação de Chamadas
### add_travelangels.php e add_webflow_octa.php

---

## 🎯 OBJETIVO

Este documento serve como referência rápida para consultar os logs internos dos endpoints `add_travelangels.php` e `add_webflow_octa.php` em **ambiente de desenvolvimento**, garantindo que as chamadas foram feitas corretamente e com sucesso.

---

## 📍 LOCALIZAÇÃO DOS LOGS

### **🧪 DESENVOLVIMENTO**

#### **EspoCRM (`add_travelangels.php`)**
- **Caminho no Servidor**: `/var/www/html/dev/logs/travelangels_dev.txt`
- **URL do Endpoint**: `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php`
- **Arquivo do Endpoint**: `/var/www/html/dev/webhooks/add_travelangels.php`

#### **Octadesk (`add_webflow_octa.php`)**
- **Caminho no Servidor**: `/var/www/html/dev/logs/octadesk_dev.txt`
- **URL do Endpoint**: `https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php`
- **Arquivo do Endpoint**: `/var/www/html/dev/webhooks/add_webflow_octa.php`

### **🚀 PRODUÇÃO** (Referência)

#### **EspoCRM (`add_travelangels.php`)**
- **Caminho no Servidor**: `/var/www/html/logs_travelangels.txt`
- **URL do Endpoint**: `https://bpsegurosimediato.com.br/add_travelangels.php`
- **Arquivo do Endpoint**: `/var/www/html/add_travelangels.php`

#### **Octadesk (`add_webflow_octa.php`)**
- **Caminho no Servidor**: `/var/www/html/octa_webflow_webhook.log`
- **URL do Endpoint**: `https://bpsegurosimediato.com.br/add_webflow_octa.php`
- **Arquivo do Endpoint**: `/var/www/html/add_webflow_octa.php`

---

## 🔍 COMANDOS PARA CONSULTAR LOGS (SSH)

### **1. Verificar Últimas Entradas do Log EspoCRM (DEV)**

```bash
# Últimas 50 linhas
tail -n 50 /var/www/html/dev/logs/travelangels_dev.txt

# Últimas 100 linhas com numeração
tail -n 100 /var/www/html/dev/logs/travelangels_dev.txt | cat -n

# Ver em tempo real (fique observando novas entradas)
tail -f /var/www/html/dev/logs/travelangels_dev.txt

# Buscar por palavra-chave específica (ex: GCLID específico)
grep "GCLID_FLD" /var/www/html/dev/logs/travelangels_dev.txt | tail -20

# Buscar por telefone específico (últimos 4 dígitos)
grep "9999" /var/www/html/dev/logs/travelangels_dev.txt | tail -20

# Contar total de registros hoje
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | wc -l

# Ver registros das últimas horas (ex: últimas 2 horas)
grep "$(date -d '2 hours ago' +'%Y-%m-%d %H')" /var/www/html/dev/logs/travelangels_dev.txt | tail -30
```

### **2. Verificar Últimas Entradas do Log Octadesk (DEV)**

```bash
# Últimas 50 linhas
tail -n 50 /var/www/html/dev/logs/octadesk_dev.txt

# Últimas 100 linhas com numeração
tail -n 100 /var/www/html/dev/logs/octadesk_dev.txt | cat -n

# Ver em tempo real (fique observando novas entradas)
tail -f /var/www/html/dev/logs/octadesk_dev.txt

# Buscar por palavra-chave específica
grep "CELULAR" /var/www/html/dev/logs/octadesk_dev.txt | tail -20

# Buscar por telefone específico
grep "9999" /var/www/html/dev/logs/octadesk_dev.txt | tail -20

# Contar total de registros hoje
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/octadesk_dev.txt | wc -l

# Ver registros das últimas horas
grep "$(date -d '2 hours ago' +'%Y-%m-%d %H')" /var/www/html/dev/logs/octadesk_dev.txt | tail -30
```

### **3. Verificar se Logs Existem**

```bash
# Verificar se arquivos de log existem e tamanho
ls -lh /var/www/html/dev/logs/travelangels_dev.txt
ls -lh /var/www/html/dev/logs/octadesk_dev.txt

# Verificar permissões dos arquivos de log
stat /var/www/html/dev/logs/travelangels_dev.txt
stat /var/www/html/dev/logs/octadesk_dev.txt

# Verificar última modificação
stat -c '%y' /var/www/html/dev/logs/travelangels_dev.txt
stat -c '%y' /var/www/html/dev/logs/octadesk_dev.txt

# Listar todos os arquivos de log no diretório DEV
ls -lht /var/www/html/dev/logs/
```

### **4. Buscar Registros por Período (DEV)**

```bash
# Registros de hoje (EspoCRM)
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt

# Registros de hoje (Octadesk)
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/octadesk_dev.txt

# Registros de uma data específica (formato: YYYY-MM-DD)
grep "2025-10-29" /var/www/html/dev/logs/travelangels_dev.txt
grep "2025-10-29" /var/www/html/dev/logs/octadesk_dev.txt

# Registros de uma hora específica (ex: 14h de hoje)
grep "$(date +%Y-%m-%d) 14:" /var/www/html/dev/logs/travelangels_dev.txt
grep "$(date +%Y-%m-%d) 14:" /var/www/html/dev/logs/octadesk_dev.txt

# Últimos 30 minutos (aproximado)
grep "$(date +'%Y-%m-%d %H')" /var/www/html/dev/logs/travelangels_dev.txt | tail -50
grep "$(date +'%Y-%m-%d %H')" /var/www/html/dev/logs/octadesk_dev.txt | tail -50
```

### **5. Filtrar por Status de Sucesso/Erro**

```bash
# Buscar apenas registros de sucesso (EspoCRM)
grep -i "PROCESSAMENTO CONCLUÍDO COM SUCESSO\|Lead criado com ID" /var/www/html/dev/logs/travelangels_dev.txt | tail -20

# Buscar apenas erros (EspoCRM)
grep -i "ERRO\|PROCESSAMENTO FALHOU" /var/www/html/dev/logs/travelangels_dev.txt | tail -20

# Buscar apenas sucessos (Octadesk)
grep -i "sucesso\|success\|enviado" /var/www/html/dev/logs/octadesk_dev.txt | tail -20

# Buscar apenas erros (Octadesk)
grep -i "erro\|error\|falhou\|failed" /var/www/html/dev/logs/octadesk_dev.txt | tail -20
```

### **6. Extrair Informações Específicas**

```bash
# Extrair apenas IDs de leads criados (EspoCRM)
grep "Lead criado com ID:" /var/www/html/dev/logs/travelangels_dev.txt | grep -oP 'ID: \K[^\s]+' | tail -20

# Extrair apenas GCLIDs registrados (EspoCRM)
grep "GCLID:" /var/www/html/dev/logs/travelangels_dev.txt | grep -oP 'GCLID: \K[^\s]+' | tail -20

# Contar total de sucessos hoje (EspoCRM)
grep "PROCESSAMENTO CONCLUÍDO COM SUCESSO" /var/www/html/dev/logs/travelangels_dev.txt | grep "$(date +%Y-%m-%d)" | wc -l

# Contar total de erros hoje (EspoCRM)
grep "PROCESSAMENTO FALHOU" /var/www/html/dev/logs/travelangels_dev.txt | grep "$(date +%Y-%m-%d)" | wc -l
```

---

## 📊 ESTRUTURA DOS LOGS ESPERADA

### **Log do EspoCRM (`travelangels_dev.txt`)**

Estrutura baseada nos arquivos `add_travelangels_v2.php` e `add_travelangels_v3.php`:

```
=== INÍCIO PROCESSAMENTO - 2025-10-29 11:00:00 ===
1. JSON recebido: {"data":{"DDD-CELULAR":"11","CELULAR":"999999999",...},"d":"2025-10-29T11:00:00.000Z","name":"Modal WhatsApp - Primeiro Contato (V2)"}
2. JSON decodificado: Array(...)
3. Verificando estrutura dos dados...
4. Dados extraídos:
   Nome: 
   Email: 
   DDD Celular: 11
   Celular: 999999999
   CEP: 
   CPF: 
   Marca: 
   Placa: 
   Ano: 
   GCLID: CjwKCAjw...
   Data: 2025-10-29T11:00:00.000Z
   Webpage: Modal WhatsApp - Primeiro Contato (V2)
5. Processando telefone...
   DDD antes: 11
   Telefone final: 11999999999
6. Criando cliente EspoCRM...
   Cliente criado com sucesso
7. Dados para API: {"firstName":"","emailAddress":"","cCelular":"11999999999",...}
8. Fazendo requisição para EspoCRM...
9. Resposta do EspoCRM: {"id":"abc123",...}
   Sucesso! Lead criado com ID: abc123
10. Enviando resposta de sucesso
=== PROCESSAMENTO CONCLUÍDO COM SUCESSO ===

```

### **Log do Octadesk (`octadesk_dev.txt`)**

Estrutura esperada (baseada no padrão de webhooks):

```
[2025-10-29 11:00:00] INÍCIO - Chamada recebida
[2025-10-29 11:00:00] JSON recebido: {"data":{"DDD-CELULAR":"11","CELULAR":"999999999",...}}
[2025-10-29 11:00:00] Dados extraídos: DDD=11, CELULAR=999999999, GCLID=...
[2025-10-29 11:00:01] Enviando mensagem para Octadesk...
[2025-10-29 11:00:02] Resposta Octadesk: {"success":true,...}
[2025-10-29 11:00:02] SUCESSO - Mensagem enviada
```

**Nota**: A estrutura exata do log do Octadesk pode variar. Verifique o arquivo real no servidor para confirmar o formato.

---

## ✅ COMO VERIFICAR SE CHAMADA FOI BEM-SUCEDIDA

### **EspoCRM - Indicadores de Sucesso**

```bash
# Verificar última chamada bem-sucedida
grep "PROCESSAMENTO CONCLUÍDO COM SUCESSO" /var/www/html/dev/logs/travelangels_dev.txt | tail -1

# Verificar se há ID de lead retornado (última chamada)
grep "Lead criado com ID:" /var/www/html/dev/logs/travelangels_dev.txt | tail -1

# Verificar última resposta do EspoCRM
grep "9. Resposta do EspoCRM:" /var/www/html/dev/logs/travelangels_dev.txt | tail -1
```

**Indicadores de Sucesso**:
- ✅ Presença de: "PROCESSAMENTO CONCLUÍDO COM SUCESSO"
- ✅ Presença de: "Lead criado com ID: [algum ID]"
- ✅ Resposta do EspoCRM contém `"id"`
- ✅ HTTP Status 200 (não há mensagens de erro)

### **Octadesk - Indicadores de Sucesso**

```bash
# Verificar última chamada bem-sucedida
grep -i "sucesso\|success\|enviado\|sent" /var/www/html/dev/logs/octadesk_dev.txt | tail -1

# Verificar última resposta do Octadesk
grep -i "resposta\|response" /var/www/html/dev/logs/octadesk_dev.txt | tail -1
```

**Indicadores de Sucesso**:
- ✅ Presença de: "SUCESSO" ou "success"
- ✅ Resposta contém `"success": true`
- ✅ HTTP Status 200 (não há mensagens de erro)

---

## 🔍 VERIFICAÇÃO CORRELACIONADA (Mesma Chamada)

Para verificar se uma chamada específica apareceu em ambos os logs:

```bash
# Buscar por timestamp específico (ex: 11:00:00)
grep "2025-10-29 11:00:00" /var/www/html/dev/logs/travelangels_dev.txt
grep "2025-10-29 11:00:00" /var/www/html/dev/logs/octadesk_dev.txt

# Buscar por GCLID específico
GCLID="CjwKCAjw..."
grep "$GCLID" /var/www/html/dev/logs/travelangels_dev.txt
grep "$GCLID" /var/www/html/dev/logs/octadesk_dev.txt

# Buscar por telefone específico (últimos 4 dígitos)
TELEFONE="9999"
grep "$TELEFONE" /var/www/html/dev/logs/travelangels_dev.txt
grep "$TELEFONE" /var/www/html/dev/logs/octadesk_dev.txt
```

---

## 📝 COMANDOS DE ANÁLISE AVANÇADA

### **Estatísticas Gerais**

```bash
# Total de registros hoje (EspoCRM)
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "INÍCIO PROCESSAMENTO" | wc -l

# Total de sucessos hoje (EspoCRM)
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "PROCESSAMENTO CONCLUÍDO COM SUCESSO" | wc -l

# Total de erros hoje (EspoCRM)
grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "PROCESSAMENTO FALHOU" | wc -l

# Taxa de sucesso (em percentual)
SUCCESS=$(grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "PROCESSAMENTO CONCLUÍDO COM SUCESSO" | wc -l)
TOTAL=$(grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "INÍCIO PROCESSAMENTO" | wc -l)
if [ $TOTAL -gt 0 ]; then
  echo "Taxa de sucesso: $(( SUCCESS * 100 / TOTAL ))%"
fi
```

### **Extrair Último Registro Completo**

```bash
# Último registro completo do EspoCRM (desde "INÍCIO" até "CONCLUÍDO")
tail -n 100 /var/www/html/dev/logs/travelangels_dev.txt | grep -A 50 "INÍCIO PROCESSAMENTO" | tail -50

# Último registro completo do Octadesk
tail -n 100 /var/www/html/dev/logs/octadesk_dev.txt | tail -20
```

### **Monitoramento em Tempo Real**

```bash
# Monitorar ambos os logs simultaneamente (em terminais separados)
# Terminal 1:
tail -f /var/www/html/dev/logs/travelangels_dev.txt

# Terminal 2:
tail -f /var/www/html/dev/logs/octadesk_dev.txt

# OU usar multitail (se instalado)
multitail /var/www/html/dev/logs/travelangels_dev.txt /var/www/html/dev/logs/octadesk_dev.txt
```

---

## 🔧 VERIFICAÇÃO VIA HEALTH CHECK

### **Via HTTP - Health Check dos Webhooks**

```bash
# Consultar health check dos webhooks (verifica arquivos e logs)
curl https://bpsegurosimediato.com.br/webhook_health.php | jq

# Apenas verificar status dos logs
curl https://bpsegurosimediato.com.br/webhook_health.php | jq '.webhooks.travelangels.logs_check'
curl https://bpsegurosimediato.com.br/webhook_health.php | jq '.webhooks.octadesk.logs_check'
```

**Resposta esperada (JSON)**:
```json
{
  "webhooks": {
    "travelangels": {
      "logs_check": {
        "status": "ok",
        "path": "/var/www/html/logs_travelangels.txt",
        "last_modified": "2025-10-29 11:00:00",
        "recently_modified": true,
        "line_count": 1234
      }
    },
    "octadesk": {
      "logs_check": {
        "status": "ok",
        "path": "/var/www/html/octa_webflow_webhook.log",
        "last_modified": "2025-10-29 11:00:00",
        "recently_modified": true
      }
    }
  }
}
```

---

## 📋 CHECKLIST DE VERIFICAÇÃO

Use este checklist ao testar se uma chamada foi realizada corretamente:

### **EspoCRM (`add_travelangels.php`)**

- [ ] 1. Arquivo de log existe: `/var/www/html/dev/logs/travelangels_dev.txt`
- [ ] 2. Arquivo foi modificado recentemente (últimas horas/minutos)
- [ ] 3. Última entrada contém: "INÍCIO PROCESSAMENTO"
- [ ] 4. JSON recebido aparece no log com dados corretos:
  - [ ] DDD-CELULAR
  - [ ] CELULAR
  - [ ] GCLID_FLD
  - [ ] `name: "Modal WhatsApp - Primeiro Contato (V2)"` ou similar
- [ ] 5. Verificar resposta do EspoCRM contém `"id"` (ID do lead)
- [ ] 6. Última entrada contém: "PROCESSAMENTO CONCLUÍDO COM SUCESSO"
- [ ] 7. NÃO há mensagens de erro no registro

### **Octadesk (`add_webflow_octa.php`)**

- [ ] 1. Arquivo de log existe: `/var/www/html/dev/logs/octadesk_dev.txt`
- [ ] 2. Arquivo foi modificado recentemente (últimas horas/minutos)
- [ ] 3. Última entrada contém registro de chamada recebida
- [ ] 4. JSON recebido aparece no log com dados corretos:
  - [ ] DDD-CELULAR
  - [ ] CELULAR
  - [ ] GCLID_FLD
- [ ] 5. Resposta indica sucesso (`"success": true` ou similar)
- [ ] 6. NÃO há mensagens de erro no registro

### **Correlação (Ambos)**

- [ ] 1. Timestamp da chamada EspoCRM corresponde ao Octadesk (aproximado, pode variar alguns segundos)
- [ ] 2. GCLID ou telefone aparecem em ambos os logs
- [ ] 3. Ambos os endpoints foram chamados com sucesso

---

## 🚨 TROUBLESHOOTING

### **Problema: Log não existe**

```bash
# Criar diretório de logs se não existir
mkdir -p /var/www/html/dev/logs

# Verificar permissões
chmod 755 /var/www/html/dev/logs
chown www-data:www-data /var/www/html/dev/logs

# Criar arquivos de log com permissões corretas
touch /var/www/html/dev/logs/travelangels_dev.txt
touch /var/www/html/dev/logs/octadesk_dev.txt
chmod 644 /var/www/html/dev/logs/*.txt
chown www-data:www-data /var/www/html/dev/logs/*.txt
```

### **Problema: Log não está sendo atualizado**

```bash
# Verificar se o arquivo PHP existe
ls -la /var/www/html/dev/webhooks/add_travelangels.php
ls -la /var/www/html/dev/webhooks/add_webflow_octa.php

# Verificar permissões de escrita
ls -la /var/www/html/dev/logs/

# Verificar se o usuário www-data tem permissão
sudo -u www-data touch /var/www/html/dev/logs/test_write.txt && rm /var/www/html/dev/logs/test_write.txt && echo "Permissão OK"
```

### **Problema: Não encontro a chamada no log**

```bash
# Buscar em período mais amplo (últimas 24 horas)
find /var/www/html/dev/logs -name "*.txt" -o -name "*.log" -mtime -1 -exec grep -l "INÍCIO PROCESSAMENTO" {} \;

# Verificar se há outros arquivos de log
find /var/www/html/dev -name "*log*" -o -name "*travelangels*" -o -name "*octadesk*"

# Verificar logs do diretório pai
ls -la /var/www/html/dev/logs/
ls -la /var/www/html/dev/webhooks/

# Buscar em todo o diretório dev
grep -r "Modal WhatsApp - Primeiro Contato" /var/www/html/dev/
```

---

## 📊 EXEMPLO DE USO PRÁTICO

### **Cenário: Testei o modal e quero verificar se funcionou**

```bash
# 1. Verificar última chamada ao EspoCRM
tail -n 100 /var/www/html/dev/logs/travelangels_dev.txt | grep -A 30 "INÍCIO PROCESSAMENTO" | tail -35

# 2. Verificar última chamada ao Octadesk
tail -n 50 /var/www/html/dev/logs/octadesk_dev.txt

# 3. Verificar se ambos tiveram sucesso
echo "=== ESPOCRM ==="
grep "PROCESSAMENTO CONCLUÍDO COM SUCESSO" /var/www/html/dev/logs/travelangels_dev.txt | tail -1
echo ""
echo "=== OCTADESK ==="
grep -i "sucesso\|success" /var/www/html/dev/logs/octadesk_dev.txt | tail -1

# 4. Extrair ID do lead criado (se houver)
grep "Lead criado com ID:" /var/www/html/dev/logs/travelangels_dev.txt | tail -1
```

### **Cenário: Verificar todas as chamadas de hoje**

```bash
# Relatório completo de hoje
echo "=== RELATÓRIO DIÁRIO - $(date +%Y-%m-%d) ==="
echo ""
echo "ESPOCRM:"
echo "  Total de chamadas: $(grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "INÍCIO PROCESSAMENTO" | wc -l)"
echo "  Sucessos: $(grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "PROCESSAMENTO CONCLUÍDO COM SUCESSO" | wc -l)"
echo "  Erros: $(grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/travelangels_dev.txt | grep "PROCESSAMENTO FALHOU" | wc -l)"
echo ""
echo "OCTADESK:"
echo "  Total de chamadas: $(grep "$(date +%Y-%m-%d)" /var/www/html/dev/logs/octadesk_dev.txt | wc -l)"
```

---

## 🔐 CONEXÃO SSH

Para executar esses comandos, você precisa de acesso SSH ao servidor:

```bash
# Conectar ao servidor
ssh usuario@bpsegurosimediato.com.br

# OU se usar IP
ssh usuario@[IP_DO_SERVIDOR]

# Verificar se está no diretório correto
pwd

# Navegar até diretório de logs
cd /var/www/html/dev/logs/
ls -lht
```

---

## ⚠️ NOTAS IMPORTANTES

1. **Permissões**: Os arquivos de log precisam ter permissão de escrita para o usuário `www-data` (ou o usuário do servidor web).

2. **Rotação de Logs**: Os logs podem ser rotacionados automaticamente. Verifique se há arquivos com sufixos de data (ex: `travelangels_dev_2025-10-29.txt`).

3. **Localização Alternativa**: Dependendo da implementação do endpoint, os logs podem estar em:
   - Mesmo diretório do arquivo PHP (ex: `/var/www/html/dev/webhooks/logs_travelangels.txt`)
   - Diretório `/var/www/html/dev/logs/` (conforme `dev_config.php`)

4. **Formato do Log**: O formato exato pode variar entre versões dos endpoints. Sempre verifique o arquivo real no servidor.

5. **Timezone**: Os timestamps nos logs usam o timezone do servidor. Verifique com `date` no servidor.

---

## 📞 CONTATO E SUPORTE

Se os logs não estiverem aparecendo:
1. Verificar se os endpoints estão realmente sendo chamados (usar Network tab do navegador)
2. Verificar permissões dos arquivos de log
3. Verificar se os endpoints PHP existem e estão corretos
4. Consultar logs de erro do PHP: `/var/log/apache2/error.log` ou `/var/log/nginx/error.log`

---

**Data de Criação**: 2025-10-29  
**Última Atualização**: 2025-10-29  
**Versão**: 1.0  
**Status**: ✅ Pronto para uso











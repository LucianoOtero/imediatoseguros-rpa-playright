# PROJETO: CORREÇÃO DA CAPTURA DE GCLID NO ARQUIVO UNIFICADO

**Data de Criação:** 01/11/2025 09:30  
**Status:** Planejamento (NÃO EXECUTAR)  
**Workspace:** imediatoseguros-rpa-playwright

---

## 📋 OBJETIVO

Corrigir o problema de captura de GCLID identificado no arquivo unificado `FooterCodeSiteDefinitivoCompleto.js`, garantindo que o código de captura imediata de GCLID/GBRAID da URL funcione corretamente e preencha os campos `GCLID_FLD` do formulário, mantendo 100% de compatibilidade com o comportamento do código original que está em produção no Head Code do Webflow.

---

## 🎯 PROBLEMA ATUAL

### Sintomas Identificados:
1. **GCLID não está sendo capturado da URL** quando o script é carregado
2. **Campos `GCLID_FLD` chegam vazios** no webhook (`"GCLID_FLD": ""`)
3. **Logs de captura não aparecem no console**:
   - Ausente: `✅ [GCLID] Capturado da URL e salvo em cookie:`
   - Ausente: `✅ [GCLID] Campo GCLID_FLD preenchido:`
4. **URL testada tinha GCLID válido**: `?gclid=test-lro-2025-11-01-09-20`

### Evidências dos Logs:
- **Console do navegador**: Não há logs de captura de GCLID
- **Log do webhook**: Campo `GCLID_FLD` sempre chega vazio (`""`)
- **Log do servidor**: URL da página tinha `pageUrl: ".../?gclid=test-lro-2025-11-01-09-20"` mas `GCLID_FLD` chegou vazio

### Diagnóstico Técnico:

**Código Original (Head Tag - FUNCIONANDO):**
- Executa no `<head>` (antes do parsing do body)
- Funções `getParam()` e `setCookie()` são globais
- Código de captura executa imediatamente na primeira linha do script
- Não está dentro de IIFE ou try-catch que possa interromper

**Código Unificado (Footer - NÃO FUNCIONANDO):**
- Carregado com `<script defer>` no footer
- Funções `getParam()` e `setCookie()` estão dentro de IIFE (linha 708-724)
- Código de captura está na linha 726-737, dentro do try-catch
- Executa quando o script carrega, mas pode haver problemas de timing ou escopo

### Causa Raiz Identificada:

O código de captura (linha 726-737) **deveria** executar imediatamente quando o script carrega, mas:
1. O código está dentro de uma IIFE com try-catch que pode estar capturando erros silenciosamente
2. A verificação de `gclsrc` (linha 733) pode estar bloqueando incorretamente
3. Pode haver problema de timing quando `window.location.search` é acessado durante o carregamento com `defer`
4. Falta de logs de debug para identificar exatamente onde o fluxo está falhando

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos a Modificar:
1. `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js` (local e servidor DEV)
   - Correção do código de captura GCLID (linhas 726-737)
   - Adição de logs de debug para diagnóstico
   - Garantir que código execute no momento correto

### Arquivos de Referência:
- `02-DEVELOPMENT/custom-codes/Inside Head Tag Pagina.js` (código original funcionando)
- `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo WEBFLOW.js` (carregamento do script)

### Backups a Criar:
- ⚠️ **Backup será criado antes da implementação**: `FooterCodeSiteDefinitivoCompleto.js.backup_20251101_HHMMSS`

### Destino no Servidor:
- `/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js`

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DAS ALTERAÇÕES

### 1.1 Análise do Código Atual

**Localização do Problema:** Linhas 726-737 de `FooterCodeSiteDefinitivoCompleto.js`

```javascript
// Captura imediata de GCLID/GBRAID da URL (executa ANTES do DOM)
var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");
var trackingId = gclid || gbraid;

if (trackingId) {
  var gclsrc = getParam("gclsrc");
  if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
    setCookie("gclid", trackingId, 90);
    console.log('✅ [GCLID] Capturado da URL e salvo em cookie:', trackingId);
  }
}
```

### 1.2 Alterações Propostas

**Objetivo:** Alinhar comportamento com código original e adicionar diagnóstico

1. **Adicionar logs de debug imediatos** antes do `if (trackingId)` para verificar:
   - Se `getParam()` está retornando valores corretos
   - Se `window.location.search` está disponível
   - Valor de `trackingId` antes da verificação

2. **Simplificar verificação de `gclsrc`** para alinhar com código original:
   - Código original não verifica `gclsrc` da mesma forma
   - Manter verificação, mas garantir que está funcionando corretamente

3. **Garantir que código execute no escopo correto**:
   - Verificar se funções `getParam()` e `setCookie()` estão acessíveis
   - Adicionar fallback caso haja problema de escopo

4. **Adicionar verificação adicional no `DOMContentLoaded`**:
   - Se a captura imediata falhar, tentar novamente quando o DOM estiver pronto
   - Garantir que o cookie seja lido corretamente

### 1.3 Implementação Técnica

**Alteração 1: Adicionar Logs de Debug**
```javascript
// Captura imediata de GCLID/GBRAID da URL (executa ANTES do DOM)
console.log('🔍 [GCLID] Iniciando captura - URL:', window.location.href);
console.log('🔍 [GCLID] window.location.search:', window.location.search);

var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");
var trackingId = gclid || gbraid;

console.log('🔍 [GCLID] Valores capturados:', { gclid, gbraid, trackingId });

if (trackingId) {
  var gclsrc = getParam("gclsrc");
  console.log('🔍 [GCLID] gclsrc:', gclsrc);
  
  if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
    try {
      setCookie("gclid", trackingId, 90);
      console.log('✅ [GCLID] Capturado da URL e salvo em cookie:', trackingId);
      
      // Verificar se cookie foi salvo corretamente
      var cookieVerificado = readCookie("gclid");
      console.log('🔍 [GCLID] Cookie verificado após salvamento:', cookieVerificado);
    } catch (error) {
      console.error('❌ [GCLID] Erro ao salvar cookie:', error);
    }
  } else {
    console.warn('⚠️ [GCLID] gclsrc bloqueou salvamento:', gclsrc);
  }
} else {
  console.warn('⚠️ [GCLID] Nenhum trackingId encontrado na URL');
}
```

**Alteração 2: Fallback no DOMContentLoaded**
```javascript
// 2.1. Gerenciamento GCLID (DOMContentLoaded)
document.addEventListener("DOMContentLoaded", function () {
  // Tentar capturar novamente se não foi capturado antes
  var cookieExistente = window.readCookie ? window.readCookie("gclid") : null;
  
  if (!cookieExistente) {
    console.log('🔍 [GCLID] Cookie não encontrado, tentando captura novamente...');
    var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
    var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");
    var trackingId = gclid || gbraid;
    
    if (trackingId) {
      setCookie("gclid", trackingId, 90);
      console.log('✅ [GCLID] Capturado no DOMContentLoaded e salvo em cookie:', trackingId);
      cookieExistente = trackingId;
    }
  }
  
  // Preencher campos com nome GCLID_FLD
  const gclidFields = document.getElementsByName("GCLID_FLD");
  console.log('🔍 [GCLID] Campos GCLID_FLD encontrados:', gclidFields.length);
  
  for (var i = 0; i < gclidFields.length; i++) {
    var cookieValue = window.readCookie ? window.readCookie("gclid") : cookieExistente;
    
    if (cookieValue) {
      gclidFields[i].value = cookieValue;
      console.log('✅ [GCLID] Campo GCLID_FLD[' + i + '] preenchido:', cookieValue);
    } else {
      console.warn('⚠️ [GCLID] Campo GCLID_FLD[' + i + '] não preenchido - cookie não encontrado');
    }
  }
  
  // ... resto do código existente ...
});
```

**Alteração 3: Atualizar Header do Arquivo**
- Incrementar versão para `1.3`
- Atualizar `ÚLTIMA ALTERAÇÃO`
- Adicionar descrição das correções na lista de alterações

---

## 📤 FASE 2: CÓPIA DOS ARQUIVOS PARA O SERVIDOR

### 2.1 Backup Local (ANTES DE QUALQUER ALTERAÇÃO)
```powershell
# Criar backup com timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js" "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js.backup_$timestamp"
```

### 2.2 Cópia para Servidor DEV
```powershell
# Copiar arquivo para servidor
scp "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js" root@46.62.174.150:/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js
```

### 2.3 Verificação no Servidor
```bash
# Verificar se arquivo foi copiado
ssh root@46.62.174.150 "ls -lh /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js"

# Verificar se arquivo é acessível via HTTP
curl -I https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js
```

---

## 🧪 FASE 3: TESTE E VERIFICAÇÃO

### 3.1 Testes de Captura GCLID

**Teste 1: Captura com GCLID na URL**
1. Acessar: `https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io/?gclid=test-correcao-20251101`
2. Abrir console do navegador
3. Verificar logs:
   - `🔍 [GCLID] Iniciando captura - URL:`
   - `🔍 [GCLID] Valores capturados:`
   - `✅ [GCLID] Capturado da URL e salvo em cookie:`
   - `🔍 [GCLID] Cookie verificado após salvamento:`
4. Verificar se cookie foi criado: `document.cookie` deve conter `gclid=test-correcao-20251101`
5. Preencher formulário e enviar
6. Verificar no log do webhook se `GCLID_FLD` foi enviado corretamente

**Teste 2: Preenchimento de Campos**
1. Com GCLID na URL, aguardar carregamento completo
2. Verificar no console:
   - `🔍 [GCLID] Campos GCLID_FLD encontrados: X`
   - `✅ [GCLID] Campo GCLID_FLD[0] preenchido: [valor]`
3. Inspecionar elemento do formulário com `name="GCLID_FLD"` e verificar se `value` foi preenchido

**Teste 3: Fallback no DOMContentLoaded**
1. Limpar cookies do navegador
2. Acessar URL com GCLID
3. Verificar se captura ocorre no `DOMContentLoaded` quando a captura imediata falha
4. Verificar logs correspondentes

**Teste 4: Sem GCLID na URL**
1. Acessar URL sem parâmetro GCLID
2. Verificar se logs aparecem corretamente:
   - `⚠️ [GCLID] Nenhum trackingId encontrado na URL`
3. Verificar que não há erro no console

### 3.2 Verificação no Webhook

Após enviar formulário com GCLID:
1. Consultar log do webhook: `/var/www/html/dev/logs/travelangels_dev.txt`
2. Verificar que `GCLID_FLD` contém o valor esperado (não vazio)
3. Verificar que `cGclid` no payload do CRM contém o valor

### 3.3 Checklist de Verificação Final

- [ ] Backup local criado com sucesso
- [ ] Arquivo modificado localmente
- [ ] Logs de debug adicionados corretamente
- [ ] Versão atualizada no header (1.3)
- [ ] Arquivo copiado para servidor DEV
- [ ] Arquivo acessível via HTTP (Status 200)
- [ ] Teste 1: Captura com GCLID na URL - ✅
- [ ] Teste 2: Preenchimento de campos - ✅
- [ ] Teste 3: Fallback no DOMContentLoaded - ✅
- [ ] Teste 4: Sem GCLID na URL - ✅
- [ ] Webhook recebe GCLID corretamente - ✅
- [ ] Console sem erros relacionados a GCLID - ✅
- [ ] Comportamento idêntico ao código original - ✅

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### Preparação:
- [ ] Backup local criado
- [ ] Código original (`Inside Head Tag Pagina.js`) revisado
- [ ] Diagnóstico do problema confirmado

### Implementação:
- [ ] Logs de debug adicionados (linha 726-737)
- [ ] Fallback no DOMContentLoaded implementado
- [ ] Header do arquivo atualizado (versão 1.3)
- [ ] Código testado localmente (sintaxe)

### Deploy:
- [ ] Arquivo copiado para servidor DEV
- [ ] Arquivo acessível via HTTP
- [ ] Cache do navegador limpo para teste

### Testes:
- [ ] Teste 1: Captura com GCLID - ✅
- [ ] Teste 2: Preenchimento de campos - ✅
- [ ] Teste 3: Fallback DOMContentLoaded - ✅
- [ ] Teste 4: Sem GCLID - ✅
- [ ] Verificação no webhook - ✅

### Documentação:
- [ ] Este projeto atualizado com resultados
- [ ] `PROJETOS_imediatoseguros-rpa-playwright.md` atualizado

---

## 🔄 ROLLBACK (Se Necessário)

### Procedimento de Reversão:
1. **Restaurar backup local:**
   ```powershell
   Copy-Item "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js.backup_YYYYMMDD_HHMMSS" "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js" -Force
   ```

2. **Copiar backup para servidor:**
   ```powershell
   scp "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js.backup_YYYYMMDD_HHMMSS" root@46.62.174.150:/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js
   ```

3. **Verificar restauração:**
   ```bash
   ssh root@46.62.174.150 "tail -20 /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js"
   ```

4. **Limpar cache do navegador e testar novamente**

---

## 📊 CRONOGRAMA

1. **Fase 1 - Implementação:** ~45 minutos
   - Análise do código (10 min)
   - Implementação das alterações (25 min)
   - Revisão do código (10 min)

2. **Fase 2 - Deploy:** ~15 minutos
   - Criação de backup (2 min)
   - Cópia para servidor (3 min)
   - Verificação de acesso (10 min)

3. **Fase 3 - Testes:** ~60 minutos
   - Teste 1: Captura com GCLID (15 min)
   - Teste 2: Preenchimento de campos (15 min)
   - Teste 3: Fallback DOMContentLoaded (15 min)
   - Teste 4: Sem GCLID (10 min)
   - Verificação no webhook (5 min)

**Total Estimado:** ~2 horas

---

## 🎯 RESULTADO ESPERADO

### Comportamento Esperado Após Correção:

1. **Captura Imediata Funcionando:**
   - Quando URL contém `?gclid=valor`, o código captura imediatamente
   - Cookie `gclid` é salvo com valor correto
   - Logs aparecem no console confirmando captura

2. **Preenchimento de Campos:**
   - Campos com `name="GCLID_FLD"` são preenchidos automaticamente
   - Logs confirmam preenchimento de cada campo encontrado

3. **Envio no Webhook:**
   - Campo `GCLID_FLD` é enviado com valor correto (não vazio)
   - Campo `cGclid` no payload do CRM contém o valor

4. **Comportamento Idêntico ao Original:**
   - Funcionalidade 100% compatível com código do Head Tag
   - Sem regressões ou mudanças de comportamento

### Métricas de Sucesso:
- ✅ Logs de captura aparecem no console quando GCLID está na URL
- ✅ Cookie `gclid` é criado corretamente
- ✅ Campos `GCLID_FLD` são preenchidos automaticamente
- ✅ Webhook recebe `GCLID_FLD` com valor (não vazio)
- ✅ Zero erros no console relacionados a GCLID

---

## 🔍 REVISÃO TÉCNICA

### Engenheiro de Software: [A DEFINIR]
**Data da Revisão:** [A DEFINIR]

#### Comentários:
- [Aguardando revisão]

#### Alterações Recomendadas:
- [Aguardando revisão]

#### Status da Revisão:
- [ ] Aprovado sem alterações
- [ ] Aprovado com alterações
- [ ] Requer nova revisão

---

## 📝 NOTAS IMPORTANTES

### ⚠️ PONTOS CRÍTICOS:
1. **SEMPRE criar backup** antes de qualquer alteração
2. **NUNCA executar** sem aprovação explícita do engenheiro
3. **SEMPRE testar** todas as funcionalidades após implementação
4. **SEMPRE documentar** todas as alterações no header do arquivo

### 📋 PROCEDIMENTOS ESPECÍFICOS:
1. Este projeto corrige problema crítico identificado nos testes do Projeto 7
2. O código original (Head Tag) está funcionando corretamente em produção
3. A correção deve manter 100% de compatibilidade com comportamento original
4. Logs de debug devem ser mantidos inicialmente para validação
5. Após confirmação de funcionamento, considerar remover logs excessivos (manter apenas críticos)

### 🔗 RELAÇÃO COM OUTROS PROJETOS:
- **Projeto 7** (Unificação Inside Head/Footer): Este projeto corrige problema identificado após implementação do Projeto 7
- **Projeto 5** (Unificação Footer Code): Arquivo alvo deste projeto foi criado no Projeto 5

---

## 📋 RESUMO EXECUTIVO

**Problema:** Código de captura GCLID no arquivo unificado não está funcionando, resultando em campos `GCLID_FLD` vazios no webhook.

**Solução:** Adicionar logs de debug detalhados, implementar fallback no DOMContentLoaded, e garantir que código execute no momento correto.

**Impacto:** Alto - GCLID é crítico para rastreamento de conversões do Google Ads.

**Risco:** Baixo - Correção baseada em código que já funciona em produção.

**Complexidade:** Média - Alterações pontuais em código existente.

---

**Status:** Aguardando Revisão Técnica  
**Próxima ação:** Submeter para análise do engenheiro de software


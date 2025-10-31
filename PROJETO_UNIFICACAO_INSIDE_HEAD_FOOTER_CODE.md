# PROJETO: UNIFICAÇÃO DO INSIDE HEAD TAG PAGINA COM FOOTER CODE

**Data de Criação:** 31/10/2025 13:23  
**Status:** Planejamento (NÃO EXECUTAR)  
**Workspace:** imediatoseguros-rpa-playwright

---

## 📋 OBJETIVO

Unificar o código do arquivo `Inside Head Tag Pagina.js` (atualmente inserido no Head Code do Webflow) com o arquivo unificado `FooterCodeSiteDefinitivoCompleto.js`, consolidando toda a funcionalidade GCLID em um único arquivo JavaScript servido externamente.

### Objetivos Específicos:

1. **Eliminar dependência do Head Code:** Remover a necessidade de inserir código no `<head>` de cada página do Webflow
2. **Centralizar código GCLID:** Integrar toda lógica de captura e tratamento de GCLID no arquivo unificado
3. **Manter funcionalidade 100%:** Garantir que todas as funcionalidades atuais sejam preservadas
4. **Simplificar manutenção:** Ter apenas um arquivo JavaScript para manter e atualizar
5. **Melhorar performance:** Reduzir código duplicado e otimizar carregamento

---

## 🎯 PROBLEMA ATUAL

### Situação Atual:

1. **Arquivo `Inside Head Tag Pagina.js`:**
   - Inserido manualmente no Head Code do Webflow (Inside `<head>` tag)
   - Precisa ser atualizado em cada página que contém formulário
   - Código duplicado (funções `setCookie`, `readCookie` já existem no arquivo unificado)
   - Difícil manutenção e versionamento

2. **Arquivo `FooterCodeSiteDefinitivoCompleto.js`:**
   - Já contém função `readCookie()` (linha 76)
   - Já lê o cookie GCLID para uso em links WhatsApp (linhas 832-850)
   - Não captura GCLID da URL (depende do cookie já estar setado)
   - Não preenche campos `GCLID_FLD` automaticamente
   - Não configura `window.CollectChatAttributes`

### Problemas Identificados:

- **Duplicação de código:** Função `readCookie()` existe em ambos arquivos
- **Dependência de Head Code:** Requer configuração manual no Webflow
- **Ordem de execução:** Head Code executa antes, mas pode ser movido para footer sem problemas
- **Manutenção complexa:** Alterações precisam ser feitas em dois lugares

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos a Modificar:

1. **`02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js`**
   - **Ação:** Adicionar código de captura GCLID da URL e preenchimento de campos
   - **Localização no servidor:** `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js`
   - **Versão atual:** 1.1
   - **Versão após modificação:** 1.2

2. **`02-DEVELOPMENT/DOCUMENTACAO_MIGRACAO_PRODUCAO_SAFETYMAILS.md`**
   - **Ação:** Atualizar documentação para remover referência ao Head Code
   - **Observação:** Documentação de migração que ainda menciona o Head Code

### Arquivos que Não Serão Modificados (mas serão descontinuados):

1. **`02-DEVELOPMENT/custom-codes/Inside Head Tag Pagina.js`**
   - **Status:** Será mantido como referência, mas não mais usado
   - **Ação:** Marcar como descontinuado após migração bem-sucedida

### Backups Criados:

- ✅ `FooterCodeSiteDefinitivoCompleto.js.backup_antes_unificacao_gclid_[timestamp].js`
- ✅ `Inside Head Tag Pagina.js.backup_antes_unificacao_[timestamp].js`

**Nota:** Backups serão criados durante a execução do projeto. Os arquivos estão prontos para backup quando necessário.

### Destino no Servidor:

- `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js` (DEV)
- `https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js` (PRODUÇÃO - futuro)

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DAS ALTERAÇÕES

### 1.1 Análise Técnica do Código Atual

#### **Inside Head Tag Pagina.js - Funcionalidades:**

1. **Captura imediata de GCLID da URL (linhas 34-46):**
   ```javascript
   // Captura gclid OU gbraid (qualquer um dos dois)
   var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
   var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");
   var trackingId = gclid || gbraid;
   if (trackingId) {
     var gclsrc = getParam("gclsrc");
     if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
       setCookie("gclid", trackingId, 90);
     }
   }
   ```
   - **Executa imediatamente** (não depende do DOM)
   - **Salva cookie** por 90 dias
   - **Prioridade:** gclid > gbraid

2. **Preenchimento de campos GCLID_FLD (linhas 60-64):**
   ```javascript
   document.addEventListener("DOMContentLoaded", function () {
     const gclidFields = document.getElementsByName("GCLID_FLD");
     for (var i = 0; i < gclidFields.length; i++) {
       gclidFields[i].value = readCookie("gclid");
     }
   });
   ```
   - **Depende do DOM** (usa `DOMContentLoaded`)
   - **Preenche campos** com nome `GCLID_FLD`

3. **Listeners em anchors (linhas 66-89):**
   ```javascript
   var anchors = document.querySelectorAll("[whenClicked='set']");
   for (var i = 0; i < anchors.length; i++) {
     anchors[i].onclick = function () {
       // Salva valores no localStorage
     };
   }
   ```
   - **Salva valores** no `localStorage` quando anchors são clicados

4. **CollectChatAttributes (linhas 92-100):**
   ```javascript
   document.addEventListener("DOMContentLoaded", function () {
     var gclidCookie = (document.cookie.match(/(^|;)\s*gclid=([^;]+)/) || [])[2];
     if (gclidCookie) {
       window.CollectChatAttributes = {
         gclid: decodeURIComponent(gclidCookie)
       };
     }
   });
   ```
   - **Configura** `window.CollectChatAttributes` para Collect.chat

#### **FooterCodeSiteDefinitivoCompleto.js - Funcionalidades Atuais:**

1. **Função `readCookie()` (linha 76):**
   - Já existe e funciona
   - Usada para ler cookie GCLID (linha 836)

2. **Inicialização GCLID para WhatsApp (linhas 832-850):**
   - Lê cookie GCLID
   - Usado em links WhatsApp

### 1.2 Estratégia de Integração

#### **Ordem de Execução (Confirmada pela Análise Técnica):**

✅ **CONFIRMADO:** O código pode ser movido para o footer sem problemas:

1. **Captura da URL (linhas 34-46):**
   - Funciona no footer porque a URL está disponível imediatamente
   - Cookie é salvo antes do código unificado precisar dele
   - Executa de forma síncrona

2. **Dependências do DOM:**
   - Todas usam `DOMContentLoaded`
   - Funcionam normalmente no footer

3. **FooterCodeSiteDefinitivoCompleto.js:**
   - Usa `defer`, então aguarda parsing do DOM
   - Lê cookie após ele ser setado

### 1.3 Implementação Detalhada

#### **Modificação 1: Adicionar funções auxiliares no início do `init()`**

**Localização:** Dentro da função `init()`, após a seção de constantes globais e antes da seção de RPA

**Código a adicionar:**

```javascript
// ======================
// CAPTURA E GERENCIAMENTO DE GCLID
// ======================

/**
 * Captura parâmetro da URL
 * @param {string} p - Nome do parâmetro
 * @returns {string|null} Valor do parâmetro ou null
 */
function getParam(p) {
  var params = new URLSearchParams(window.location.search);
  return params.get(p) ? decodeURIComponent(params.get(p)) : null;
}

/**
 * Define cookie com expiração
 * @param {string} name - Nome do cookie
 * @param {string} value - Valor do cookie
 * @param {number} days - Dias até expiração
 */
function setCookie(name, value, days) {
  var date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  var expires = "; expires=" + date.toUTCString();
  document.cookie = name + "=" + value + expires + ";path=/";
}

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

// Preencher campos GCLID_FLD quando DOM estiver pronto
document.addEventListener("DOMContentLoaded", function () {
  // Preencher campos com nome GCLID_FLD
  const gclidFields = document.getElementsByName("GCLID_FLD");
  for (var i = 0; i < gclidFields.length; i++) {
    var cookieValue = window.readCookie ? window.readCookie("gclid") : null;
    if (cookieValue) {
      gclidFields[i].value = cookieValue;
      console.log('✅ [GCLID] Campo GCLID_FLD preenchido:', cookieValue);
    }
  }
  
  // Configurar listeners em anchors [whenClicked='set']
  var anchors = document.querySelectorAll("[whenClicked='set']");
  for (var i = 0; i < anchors.length; i++) {
    anchors[i].onclick = function () {
      // Verificação defensiva antes de acessar .value
      var emailEl = document.getElementById("email");
      var gclidEl = document.getElementById("GCLID_FLD");
      var gclidWpEl = document.getElementById("GCLID_FLD_WP");
      
      var global_email = emailEl ? emailEl.value : null;
      var global_gclid = gclidEl ? gclidEl.value : null;
      var global_gclid_wp = gclidWpEl ? gclidWpEl.value : null;
      
      // Salvar apenas valores válidos no localStorage
      if (global_gclid) {
        window.localStorage.setItem("GCLID_FLD", global_gclid);
      }
      if (global_gclid_wp) {
        window.localStorage.setItem("GCLID_FLD_WP", global_gclid_wp);
      }
      if (global_email) {
        window.localStorage.setItem("EMAIL_FLD", global_email);
      }
    };
  }
  
  // Configurar CollectChatAttributes
  var gclidCookie = (document.cookie.match(/(^|;)\s*gclid=([^;]+)/) || [])[2];
  if (gclidCookie) {
    window.CollectChatAttributes = {
      gclid: decodeURIComponent(gclidCookie)
    };
    console.log("✅ [GCLID] CollectChatAttributes configurado:", decodeURIComponent(gclidCookie));
  }
});
```

#### **Modificação 2: Atualizar header do arquivo**

**Localização:** Linhas 1-17 (cabeçalho do arquivo)

**Atualização:**

```javascript
/**
 * PROJETO: UNIFICAÇÃO DE ARQUIVOS FOOTER CODE
 * INÍCIO: 30/10/2025 19:55
 * ÚLTIMA ALTERAÇÃO: 31/10/2025 13:23
 * 
 * VERSÃO: 1.2 - Unificação do Inside Head Tag Pagina.js
 * 
 * Arquivo unificado contendo:
 * - FooterCodeSiteDefinitivoUtils.js (Parte 1)
 * - Footer Code Site Definitivo.js (Parte 2 - modificado)
 * - Inside Head Tag Pagina.js (Parte 3 - GCLID integrado)
 * 
 * ALTERAÇÕES NESTA VERSÃO:
 * - Integração completa do código GCLID do Inside Head Tag Pagina.js
 * - Captura imediata de GCLID/GBRAID da URL e salvamento em cookie
 * - Preenchimento automático de campos GCLID_FLD
 * - Configuração de CollectChatAttributes
 * - Listeners em anchors para salvar valores no localStorage
 * - Eliminação da necessidade de Head Code no Webflow
 * 
 * Localização: https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js
 * 
 * ⚠️ AMBIENTE: DEV
 * - SafetyMails Ticket: fc5e18c10c4aa883b2c31a305f1c09fea3834138
 * - SafetyMails API Key: 20a7a1c297e39180bd80428ac13c363e882a531f
 * - Ver documentação: DOCUMENTACAO_MIGRACAO_PRODUCAO_SAFETYMAILS.md
 */
```

### 1.4 Posicionamento do Código

**Localização ideal:** Dentro da função `init()`, após as constantes globais e antes da seção de RPA

**Estrutura sugerida:**

```
init() {
  // 1. Constantes globais (já existe)
  // 2. CAPTURA E GERENCIAMENTO DE GCLID (NOVO)
  // 3. Configuração RPA (já existe)
  // 4. WhatsApp links com GCLID (já existe - usar cookie já setado)
  // ... resto do código
}
```

### 1.5 Validações e Testes Necessários

#### **Funcionalidades a Testar:**

1. ✅ **Captura de GCLID da URL:**
   - Testar com `?gclid=teste123`
   - Testar com `?GBRAID=teste456`
   - Verificar cookie sendo salvo

2. ✅ **Preenchimento de campos:**
   - Verificar campos `name="GCLID_FLD"` sendo preenchidos
   - Verificar múltiplos campos com mesmo nome

3. ✅ **localStorage em anchors:**
   - Clicar em elemento com `whenClicked='set'`
   - Verificar valores salvos no localStorage

4. ✅ **CollectChatAttributes:**
   - Verificar `window.CollectChatAttributes.gclid` configurado
   - Testar integração com Collect.chat

5. ✅ **Links WhatsApp:**
   - Verificar que GCLID ainda funciona nos links WhatsApp
   - Testar clique em `whatsapplink`, `whatsapplinksucesso`, etc.

6. ✅ **Ordem de execução:**
   - Verificar que cookie é setado antes de ser lido
   - Verificar que campos são preenchidos após DOMContentLoaded

---

## 📤 FASE 2: CÓPIA DOS ARQUIVOS PARA O SERVIDOR

### 2.1 Comando SCP (Windows PowerShell)

```powershell
# Navegar para o diretório do arquivo
cd "02-DEVELOPMENT\custom-codes"

# Copiar para servidor DEV
scp FooterCodeSiteDefinitivoCompleto.js usuario@dev.bpsegurosimediato.com.br:/caminho/webhooks/
```

### 2.2 Verificação de Upload

```powershell
# Verificar acesso ao arquivo
$response = Invoke-WebRequest -Uri 'https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js?v=1.2' -UseBasicParsing
$response.StatusCode  # Deve retornar 200
```

### 2.3 Verificação de Conteúdo

```powershell
# Verificar se código GCLID está presente
$content = (Invoke-WebRequest -Uri 'https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js?v=1.2').Content
if ($content -match 'Captura imediata de GCLID') {
  Write-Host '✅ Código GCLID encontrado no servidor'
}
```

---

## 🧪 FASE 3: TESTE E VERIFICAÇÃO

### 3.1 Testes Funcionais

#### **Teste 1: Captura de GCLID da URL**
- [ ] Acessar página com `?gclid=teste-123`
- [ ] Verificar console: "✅ [GCLID] Capturado da URL e salvo em cookie: teste-123"
- [ ] Verificar cookie `gclid` no DevTools (Application > Cookies)
- [ ] Verificar expiração do cookie (90 dias)

#### **Teste 2: Preenchimento de Campos**
- [ ] Verificar campos `name="GCLID_FLD"` preenchidos automaticamente
- [ ] Verificar console: "✅ [GCLID] Campo GCLID_FLD preenchido: [valor]"
- [ ] Testar múltiplos campos com mesmo nome

#### **Teste 3: localStorage em Anchors**
- [ ] Clicar em elemento com `whenClicked='set'`
- [ ] Verificar `localStorage.getItem("GCLID_FLD")`
- [ ] Verificar `localStorage.getItem("EMAIL_FLD")`

#### **Teste 4: CollectChatAttributes**
- [ ] Verificar `window.CollectChatAttributes.gclid` no console
- [ ] Verificar console: "✅ [GCLID] CollectChatAttributes configurado: [valor]"
- [ ] Testar integração com Collect.chat (se aplicável)

#### **Teste 5: Links WhatsApp**
- [ ] Clicar em `whatsapplink`, `whatsapplinksucesso`, `whatsappfone1`, `whatsappfone2`
- [ ] Verificar que GCLID está presente na URL do WhatsApp
- [ ] Verificar que modal é aberto corretamente

#### **Teste 6: Compatibilidade com Cookie Existente**
- [ ] Acessar página SEM parâmetro GCLID na URL
- [ ] Verificar que cookie existente é usado
- [ ] Verificar que campos são preenchidos com cookie antigo

#### **Teste 7: Prioridade GCLID vs GBRAID**
- [ ] Acessar com `?gclid=teste1&gbraid=teste2`
- [ ] Verificar que `gclid` tem prioridade
- [ ] Acessar apenas com `?gbraid=teste2`
- [ ] Verificar que `gbraid` é usado

### 3.2 Testes de Regressão

#### **Funcionalidades que NÃO devem ser afetadas:**
- [ ] Validação de formulários (CPF, CEP, Placa, Email, Celular)
- [ ] Máscaras de input (jQuery Mask)
- [ ] SweetAlert2
- [ ] Integração RPA
- [ ] Modal WhatsApp
- [ ] Envio de formulários
- [ ] GTM (Google Tag Manager)

### 3.3 Testes em Múltiplos Navegadores

- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (se possível)

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### Pré-Implementação:
- [x] Backups criados
- [x] Documentação do projeto criada
- [x] Análise técnica completa
- [ ] Revisão técnica do engenheiro

### Implementação:
- [ ] Código GCLID adicionado ao FooterCodeSiteDefinitivoCompleto.js
- [ ] Header do arquivo atualizado (versão 1.2)
- [ ] Funções `getParam()` e `setCookie()` adicionadas
- [ ] Captura imediata de GCLID/GBRAID implementada
- [ ] Preenchimento de campos GCLID_FLD implementado
- [ ] Listeners em anchors implementados
- [ ] CollectChatAttributes configurado
- [ ] Código posicionado corretamente (após constantes, antes de RPA)

### Deploy:
- [ ] Arquivo copiado para servidor DEV
- [ ] Verificação de acesso ao arquivo (HTTP 200)
- [ ] Verificação de conteúdo no servidor
- [ ] Cache do navegador limpo (testar com `?v=1.2`)

### Testes:
- [ ] Teste 1: Captura de GCLID da URL ✅
- [ ] Teste 2: Preenchimento de Campos ✅
- [ ] Teste 3: localStorage em Anchors ✅
- [ ] Teste 4: CollectChatAttributes ✅
- [ ] Teste 5: Links WhatsApp ✅
- [ ] Teste 6: Compatibilidade com Cookie Existente ✅
- [ ] Teste 7: Prioridade GCLID vs GBRAID ✅
- [ ] Todos os testes de regressão ✅
- [ ] Testes em múltiplos navegadores ✅

### Documentação:
- [ ] Atualizar DOCUMENTACAO_MIGRACAO_PRODUCAO_SAFETYMAILS.md
- [ ] Remover referências ao Head Code do Webflow
- [ ] Documentar remoção do Head Code
- [ ] Atualizar PROJETOS_imediatoseguros-rpa-playwright.md
- [ ] Marcar Inside Head Tag Pagina.js como descontinuado (após validação)

### Webflow (Após Validação):
- [ ] Remover código do Head Code do Webflow (todas as páginas)
- [ ] Verificar que não há dependências do Head Code
- [ ] Testar todas as páginas com formulários

---

## 🔄 ROLLBACK (Se Necessário)

### Procedimento de Reversão:

1. **Restaurar arquivo do backup:**
   ```powershell
   Copy-Item "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js.backup_antes_unificacao_gclid_[timestamp]" -Destination "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js" -Force
   ```

2. **Copiar versão anterior para servidor:**
   ```powershell
   scp FooterCodeSiteDefinitivoCompleto.js usuario@dev.bpsegurosimediato.com.br:/caminho/webhooks/
   ```

3. **Verificar versão anterior no servidor:**
   - Acessar: `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js?v=1.1`
   - Verificar que código GCLID não está presente

4. **Restaurar Head Code no Webflow (se necessário):**
   - Restaurar código do arquivo `Inside Head Tag Pagina.js`
   - Inserir em todas as páginas que contêm formulários

---

## 📊 CRONOGRAMA

1. **Fase 1: Implementação:** ~45 minutos
   - Adicionar código GCLID ao arquivo
   - Atualizar header
   - Validar estrutura

2. **Fase 2: Deploy:** ~15 minutos
   - Copiar arquivo para servidor
   - Verificar acesso e conteúdo

3. **Fase 3: Testes:** ~60 minutos
   - Testes funcionais completos
   - Testes de regressão
   - Testes em múltiplos navegadores

4. **Fase 4: Documentação:** ~30 minutos
   - Atualizar documentação
   - Atualizar controle de projetos

5. **Fase 5: Webflow (após validação):** ~30 minutos
   - Remover Head Code
   - Verificar todas as páginas

**Total Estimado:** ~3 horas

---

## 🎯 RESULTADO ESPERADO

### Após Implementação:

1. **Arquivo unificado completo:**
   - Toda funcionalidade GCLID integrada
   - Código consolidado em um único arquivo
   - Sem duplicação de funções

2. **Webflow simplificado:**
   - Head Code vazio (ou apenas GTM noscript)
   - Footer Code apenas com referência ao arquivo externo
   - Manutenção centralizada

3. **Funcionalidade preservada:**
   - Todas as funcionalidades atuais funcionando
   - Captura de GCLID da URL
   - Preenchimento automático de campos
   - Integração com Collect.chat
   - Links WhatsApp com GCLID

4. **Manutenção facilitada:**
   - Um único arquivo para manter
   - Versionamento simplificado
   - Deploy único

---

## 🔍 REVISÃO TÉCNICA

### Engenheiro de Software: [AGUARDANDO REVISÃO]
**Data da Revisão:** [A PREENCHER]

#### Pontos para Revisão:

1. **Ordem de execução:**
   - Confirmar que captura da URL funciona no footer
   - Validar timing entre captura e uso do cookie

2. **Estrutura do código:**
   - Posicionamento dentro da função `init()`
   - Dependências e ordem de execução

3. **Performance:**
   - Impacto do código adicional
   - Otimizações possíveis

4. **Compatibilidade:**
   - Funcionamento em diferentes navegadores
   - Tratamento de edge cases

#### Comentários:
- [Aguardando comentários do engenheiro]

#### Alterações Recomendadas:
- [Aguardando recomendações]

#### Status da Revisão:
- [ ] Aprovado sem alterações
- [ ] Aprovado com alterações
- [ ] Requer nova revisão

---

## 📝 NOTAS IMPORTANTES

### ⚠️ PONTOS CRÍTICOS:

1. **Ordem de execução é crítica:**
   - Captura da URL DEVE executar antes do código depender do cookie
   - Código está posicionado corretamente (síncrono antes de DOMContentLoaded)

2. **Não remover Head Code imediatamente:**
   - Aguardar validação completa antes de remover
   - Manter backup do código atual no Webflow

3. **Testar em todas as páginas:**
   - Páginas com formulários principais
   - Páginas com formulários secundários
   - Páginas sem formulários (verificar que não quebra)

4. **Versionamento:**
   - Incrementar versão para 1.2
   - Atualizar query string no Webflow: `?v=1.2`

### 📋 CONSIDERAÇÕES TÉCNICAS:

1. **Compatibilidade com cookie existente:**
   - Se cookie já existir, não sobrescrever
   - Usar cookie existente para preencher campos

2. **Prioridade de parâmetros:**
   - GCLID tem prioridade sobre GBRAID
   - Parâmetro da URL tem prioridade sobre cookie (apenas na primeira visita)

3. **Defensive coding:**
   - Verificações de existência de elementos
   - Tratamento de erros
   - Fallbacks quando necessário

---

**Status:** Aguardando Revisão Técnica  
**Próximo passo:** Submeter para revisão do engenheiro


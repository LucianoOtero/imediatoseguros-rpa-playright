# 📋 ESPECIFICAÇÃO FINAL - IMPLEMENTAÇÃO MODAL WHATSAPP

## ✅ SITUAÇÃO ATUAL

**Código existente no Footer Code** (linhas ~160-181):
```javascript
$(function () {
  ['whatsapplink', 'whatsapplinksucesso', 'whatsappfone1', 'whatsappfone2'].forEach(function (id) {
    var $el = $('#' + id);
    if ($el.length) {
      $el.on('click', function () {
        window.open("https://api.whatsapp.com/send?phone=551132301422&text=Ola.%20Quero%20fazer%20uma%20cotacao%20de%20seguro.%20Codigo%20de%20Desconto=%20" + gclid);
      });
    }
  });
});
```

✅ **Interceptação JÁ FUNCIONA** para os 4 elementos: whatsapplink, whatsapplinksucesso, whatsappfone1, whatsappfone2

---

## 🎯 MODIFICAÇÕES NECESSÁRIAS

### **1. Substituir window.open() por abertura do modal**

**Código atual abre WhatsApp DIRETO**: `window.open("https://api...")`  
**Novo código abrirá MODAL**: Carregar modal → Abrir modal → WhatsApp no final

---

## 📝 IMPLEMENTAÇÃO DETALHADA

### **MODIFICAÇÃO 1: Inside Head Tag Pagina.js**

**LOCALIZAR**: Fim do arquivo (após linha 68)

**ADICIONAR**:
```javascript
document.addEventListener("DOMContentLoaded", function () {
  var gclidCookie = (document.cookie.match(/(^|;)\s*gclid=([^;]+)/) || [])[2];
  
  if (gclidCookie) {
    window.segurosimediatoGCLID = decodeURIComponent(gclidCookie);
    console.log("GCLID capturado para WhatsApp:", gclidCookie);
  }
});
```

**O que faz**: Captura GCLID e coloca em `window.segurosimediatoGCLID` para o modal usar.

---

### **MODIFICAÇÃO 2: Footer Code Site Definitivo.js**

**LOCALIZAR**: Linhas ~160-181 (já identificado)

**SUBSTITUIR TODO O BLOCO** por:

```javascript
$(function () {
  // Função para carregar modal dinamicamente
  function loadWhatsAppModal() {
    if (window.whatsappModalLoaded) {
      console.log('✅ [MODAL] Modal já carregado');
      return;
    }
    
    console.log('🔄 [MODAL] Carregando modal de dev.bpsegurosimediato.com.br...');
    const script = document.createElement('script');
    script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js';
    script.onload = function() {
      window.whatsappModalLoaded = true;
      console.log('✅ [MODAL] Modal carregado com sucesso');
    };
    script.onerror = function() {
      console.error('❌ [MODAL] Erro ao carregar modal');
    };
    document.head.appendChild(script);
  }
  
  // Interceptar clicks (MANTÉM ESTRUTURA ORIGINAL)
  ['whatsapplink', 'whatsapplinksucesso', 'whatsappfone1', 'whatsappfone2'].forEach(function (id) {
    var $el = $('#' + id);
    if ($el.length) {
      $el.on('click', function (e) {
        e.preventDefault(); // ✅ NOVO: Bloqueia window.open direto
        
        // Se modal já existe, apenas abrir
        if ($('#whatsapp-modal').length) {
          $('#whatsapp-modal').fadeIn(300);
        } else {
          // Modal não existe, carregar
          loadWhatsAppModal();
          
          // Aguardar modal ser criado pelo script
          const checkModal = setInterval(function() {
            if ($('#whatsapp-modal').length) {
              clearInterval(checkModal);
              $('#whatsapp-modal').fadeIn(300);
            }
          }, 100);
          
          // Timeout de 3 segundos
          setTimeout(function() {
            clearInterval(checkModal);
            if ($('#whatsapp-modal').length) {
              $('#whatsapp-modal').fadeIn(300);
            }
          }, 3000);
        }
      });
    }
  });
});
```

**O que muda**:
- ❌ Remove `window.open()` direto
- ✅ Adiciona `e.preventDefault()`
- ✅ Carrega modal de bpsegurosimediato.com.br
- ✅ Abre modal ao invés de WhatsApp
- ✅ Mantém estrutura original (4 IDs)

---

### **MODIFICAÇÃO 3: MODAL_WHATSAPP_DEFINITIVO.js**

#### **3.1 Modificar openWhatsApp() (linha 77-82)**

**ATUAL**:
```javascript
function openWhatsApp(dados) {
  const mensagem = buildWhatsAppMessage(dados);
  const url = `https://api.whatsapp.com/send?phone=${MODAL_CONFIG.whatsapp.phone}&text=${mensagem}`;
  console.log('🚀 [MODAL] Abrindo WhatsApp:', url);
  window.open(url, '_blank');
}
```

**NOVO**:
```javascript
function openWhatsApp(dados) {
  const mensagem = buildWhatsAppMessage(dados);
  const url = `https://api.whatsapp.com/send?phone=${MODAL_CONFIG.whatsapp.phone}&text=${mensagem}`;
  
  console.log('🚀 [MODAL] Abrindo WhatsApp:', url);
  window.open(url, '_blank');
}
```

**NOTA**: GCLID **NÃO será enviado** na URL do WhatsApp. O GCLID ainda será capturado e armazenado em `window.segurosimediatoGCLID` para uso futuro (espoCRM/Octadesk).

#### **3.2 Modificar buildWhatsAppMessage() (linha 61-75)**

**ATUAL** (mensagem com formatação de dados):
```javascript
function buildWhatsAppMessage(dados) {
  let mensagem = MODAL_CONFIG.whatsapp.message;
  
  if (dados.TELEFONE) mensagem += `%0ATelefone: ${dados.TELEFONE}`;
  if (dados.CPF) mensagem += `%0ACPF: ${dados.CPF}`;
  if (dados.NOME) mensagem += `%0ANome: ${dados.NOME}`;
  if (dados.CEP) mensagem += `%0ACEP: ${dados.CEP}`;
  if (dados.PLACA) mensagem += `%0APlaca: ${dados.PLACA}`;
  if (dados.ENDERECO) mensagem += `%0AEndereço: ${dados.ENDERECO}`;
  
  const gclid = getGCLID();
  if (gclid) mensagem += `%0ACódigo: ${gclid}`;
  
  return mensagem;
}
```

**NOVO** (mensagem simples):
```javascript
function buildWhatsAppMessage(dados) {
  // Mensagem simples como especificado
  return 'Ola.%20Quero%20fazer%20uma%20cotacao%20de%20seguro.';
}
```

---

## 📤 UPLOAD DO MODAL

### **Arquivo**: MODAL_WHATSAPP_DEFINITIVO.js
### **Diretório**: `/var/www/html/dev/webhooks/` (servidor 46.62.174.150)
### **Status**: ✅ JÁ COPIADO E FUNCIONANDO

**URL final**: `https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`

---

## 🔄 FLUXO COMPLETO

```
1. Usuário visita site
   └─ Inside Head Tag captura GCLID
   └─ window.segurosimediatoGCLID = "ABC123"

2. Usuário clica em qualquer #whatsapplink (4 elementos)
   └─ Footer Code intercepta click
   └─ e.preventDefault() bloqueia navegação direta
   
3. Modal não existe no DOM
   └─ loadWhatsAppModal() carrega script de dev.bpsegurosimediato.com.br
   └─ Script cria HTML do modal
   
4. Modal aparece automaticamente
   └─ DIV 1: DDD + CELULAR (obrigatório)
   └─ Usuário preenche → DIV 2 aparece
   └─ DIV 2: CPF, NOME, CEP, PLACA (opcional)
   
5. Usuário clica "Ir para WhatsApp"
   └─ openWhatsApp(dados) é chamado
   └─ buildWhatsAppMessage() retorna mensagem simples
   └─ URL: https://api.whatsapp.com/send?phone=551132301422&text=...
   └─ window.open() abre WhatsApp
   └─ GCLID permanece disponível em window.segurosimediatoGCLID
   
6. Integração Futura
   └─ GCLID será usado no espoCRM/Octadesk (fase 2)
   └─ Conversões offline registradas via integração com CRM
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### **Upload**
- [x] Upload MODAL_WHATSAPP_DEFINITIVO.js para `/var/www/html/dev/webhooks/`
- [x] Testar URL: https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js
- [x] Verificar que script é acessível
- [x] Configurar Nginx para domínio dev
- [x] Gerar certificado SSL via Certbot

### **Modificação de Arquivos**
- [ ] Adicionar captura GCLID no Inside Head Tag Pagina.js
- [ ] Modificar Footer Code (substituir window.open por modal)
- [ ] Modificar openWhatsApp() no modal (remover lógica de GCLID da URL)
- [ ] Modificar buildWhatsAppMessage() no modal (mensagem simples)

### **Testes DEV**
- [ ] Testar carregamento do modal
- [ ] Verificar GCLID capturado em window.segurosimediatoGCLID
- [ ] Validar URL do WhatsApp (SIMPLES, sem GCLID)
- [ ] Testar todos os 4 elementos de click
- [ ] Validar comportamento em desktop e mobile

### **Deploy Produção**
- [ ] Deploy para STAGING
- [ ] Testar no Webflow DEV
- [ ] Deploy para PRODUÇÃO
- [ ] Desabilitar Collect Chat no GTM
- [ ] Monitorar por 24-48h

---

## 📊 COMPARAÇÃO

### ANTES
```javascript
// Clica em whatsapplink
window.open("https://api.whatsapp.com/send?...") // WhatsApp abre direto
```

### DEPOIS
```javascript
// Clica em whatsapplink
e.preventDefault() // Bloqueia
loadWhatsAppModal() // Carrega modal
$('#whatsapp-modal').fadeIn() // Abre modal
// Usuário preenche dados
// Clica "Ir para WhatsApp"
openWhatsApp() // Abre WhatsApp (URL simples)
// GCLID permanece em window.segurosimediatoGCLID
```

---

## 🎯 RESUMO

### 3 Arquivos a Modificar:
1. ✅ Inside Head Tag Pagina.js - Adicionar captura GCLID
2. ✅ Footer Code Site Definitivo.js - Substituir window.open por modal
3. ✅ MODAL_WHATSAPP_DEFINITIVO.js - Simplicar mensagem (GCLID não vai na URL)

### 1 Arquivo a Upload:
1. ✅ MODAL_WHATSAPP_DEFINITIVO.js → `/var/www/html/dev/webhooks/` (CONCLUÍDO)

**Tempo estimado**: 4-6 horas  
**Complexidade**: Média  
**Risco**: Baixo (mudanças isoladas e testáveis)

---

**Versão**: 1.0  
**Data**: 2025-01-28  
**Status**: ESPECIFICAÇÃO FINALIZADA ✅


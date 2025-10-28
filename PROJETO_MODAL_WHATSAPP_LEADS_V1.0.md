# 📱 PROJETO: MODAL WHATSAPP LEADS - SUBSTITUIÇÃO COLLECT CHAT

**Data:** 27/10/2025  
**Versão:** 1.0  
**Status:** ✅ PRONTO PARA IMPLEMENTAÇÃO  
**Desenvolvedor:** Assistente AI - Cursor

---

## 📋 SUMÁRIO

1. [Objetivo](#objetivo)
2. [Análise do Sistema Atual](#análise-do-sistema-atual)
3. [Design Visual](#design-visual)
4. [Arquitetura Técnica](#arquitetura-técnica)
5. [Código Completo](#código-completo)
6. [Integração](#integração)
7. [Testes](#testes)
8. [Próximos Passos](#próximos-passos)

---

## 🎯 OBJETIVO

Desenvolver um modal de captura de leads para substituir o Collect Chat, que será aberto quando o cliente clicar em um link com ID `whatsapplink`. O modal deve:

1. ✅ Coletar dados: DDD, Telefone Celular, CPF, CEP e Placa
2. ✅ Validar campos em tempo real (on blur) e no submit
3. ✅ Usar as mesmas funções de validação do Footer Code existente
4. ✅ Exibir SweetAlert com opções "Corrigir" ou "Prosseguir"
5. ✅ Após validação, fechar o modal e abrir WhatsApp com GCLID
6. ✅ Seguir identidade visual do modal RPA existente

---

## 🔍 ANÁLISE DO SISTEMA ATUAL

### **Validações Existentes (Footer Code Site Definitivo.js)**

#### **1. CPF** (linhas 351-476)
- **Endpoint API**: `https://mdmidia.com.br/cpf-validate.php`
- **Validação Local**: Algoritmo matemático
- **Validação API**: Consulta PH3A (quando `VALIDAR_PH3A = true`)
- **Função**: `validarCPFApi()`, `validarCPFAlgoritmo()`
- **Alert**: `saWarnConfirmCancel()`, `saInfoConfirmCancel()`

#### **2. CEP** (linhas 478-486)
- **Endpoint API**: `https://viacep.com.br/ws/{cep}/json/`
- **Validação**: Formato 8 dígitos
- **Função**: `validarCepViaCep()`
- **Alert**: `saWarnConfirmCancel()`

#### **3. Placa** (linhas 489-583)
- **Endpoint API**: `https://mdmidia.com.br/placa-validate.php`
- **Validação**: Formato antigo ou Mercosul
- **Função**: `validarPlacaApi()`, `validarPlacaFormato()`
- **Alert**: `saWarnConfirmCancel()`

#### **4. Celular** (linhas 591-611)
- **Endpoint API**: `https://apilayer.net/api/validate?access_key=dce92fa84152098a3b5b7b8db24debbc&country_code=BR&number=...`
- **Validação**: DDD (2 dígitos) + Número (9 dígitos, começando com 9)
- **Função**: `validarTelefoneAsync()`, `validarCelularLocal()`, `validarCelularApi()`
- **Alert**: `saWarnConfirmCancel()`

#### **5. E-mail** (linhas 613-615)
- **Validação**: Regex + SafetyMails (opcional)
- **Função**: `validarEmailLocal()`, `validarEmailSafetyMails()`
- **Alert**: `saWarnConfirmCancel()`

### **Máscaras jQuery Existentes**
```javascript
// Footer Code já possui:
$('#CPF').mask('000.000.000-00');
$('#CEP').mask('00000-000');
$('#PLACA').mascaraPlaca('SSS-0A00');
$('#DDD-CELULAR').mask('00');
$('#CELULAR').mask('00000-0000');
```

### **SweetAlert2**
- Já carregado no Footer Code
- Tema Imediato aplicado
- Funções: `saWarnConfirmCancel()`, `saInfoConfirmCancel()`

---

## 🎨 DESIGN VISUAL

### **📊 Paleta de Cores Imediato Seguros**

```css
:root {
    --imediato-dark-blue: #003366;      /* Azul Escuro Principal */
    --imediato-light-blue: #0099CC;     /* Azul Claro Secundário */
    --imediato-white: #FFFFFF;          /* Branco Neutro */
    --imediato-gray: #F8F9FA;          /* Cinza Claro */
    --imediato-text: #333333;          /* Texto Principal */
    --imediato-text-light: #666666;    /* Texto Secundário */
    --imediato-border: #E0E0E0;        /* Bordas */
    --imediato-shadow: rgba(0, 51, 102, 0.1);      /* Sombra Suave */
    --imediato-shadow-hover: rgba(0, 51, 102, 0.2); /* Sombra Hover */
}
```

### **📝 Tipografia**

- **Fonte Principal**: `Titillium Web` (Google Fonts)
- **Pesos**: 300, 400, 600, 700
- **Tamanhos**:
  - Labels: 14px (font-weight: 600)
  - Inputs: 16px (font-weight: 400)
  - Título: 28px (font-weight: 700)
  - Botão: 18px (font-weight: 700)

### **🎭 Elementos Visuais**

- **Overlay**: `rgba(0, 51, 102, 0.35)` - Azul escuro translúcido
- **Header**: Gradiente `linear-gradient(135deg, #003366 0%, #0099CC 100%)`
- **Border Radius**: 10px (inputs), 12px (botão), 20px (modal)
- **Sombras**: `0 30px 60px rgba(0, 51, 102, 0.15)`
- **Hovers**: Transform + sombra suave
- **Focus**: Border azul + shadow ring

---

## 🏗️ ARQUITETURA TÉCNICA

### **Fluxo de Funcionamento**

```
1. Cliente clica no link #whatsapplink
   ↓
2. Modal abre com fadeIn (300ms)
   ↓
3. Cliente preenche campos:
   ├─ DDD → valida no BLUR
   ├─ Celular → valida no BLUR (com API)
   ├─ CPF → valida no CHANGE (com API PH3A)
   ├─ CEP → valida no CHANGE (com ViaCEP)
   └─ Placa → valida no CHANGE (com API Placa)
   ↓
4. Cliente clica em "Solicitar Cotação"
   ↓
5. Re-valida TODAS as informações
   ↓
   ├─ ✅ TUDO OK? 
   │   └─ Fechar modal → Abrir WhatsApp (com GCLID)
   │
   ├─ ❌ DADOS INVÁLIDOS?
   │   ├─ SweetAlert: "Corrigir" → Foca primeiro campo inválido
   │   └─ SweetAlert: "Prosseguir" → Fechar modal → Abrir WhatsApp
   │
   └─ ⚠️ ERRO DE REDE?
       ├─ SweetAlert: "Corrigir" → Permite preencher novamente
       └─ SweetAlert: "Prosseguir" → Fechar modal → Abrir WhatsApp
```

### **Estrutura de Arquivos**

```plaintext
📁 Documentação/
├── PROJETO_MODAL_WHATSAPP_LEADS_V1.0.md  ← Este arquivo
│
├── 📁 Código para implementação/
│   ├── footer-code-whatsapp-modal.js      ← Código para Footer Code
│   └── teste-modal-whatsapp.html          ← Página de teste HTML
│
└── 📁 Análise/
    └── analise-validoes-exitentes.txt     ← Análise das validações
```

---

## 💻 CÓDIGO COMPLETO

### **1. Link no HTML (já existe no site)**

```html
<!-- Exemplo: Link que abre o modal -->
<a href="#" id="whatsapplink" class="btn-whatsapp">
  📱 Solicitar Cotação via WhatsApp
</a>
```

### **2. Código JavaScript para o Footer Code**

**Arquivo**: `footer-code-whatsapp-modal.js`

```javascript
<!-- ====================== -->
<!-- MODAL WHATSAPP LEADS - SUBSTITUIÇÃO COLLECT CHAT -->
<!-- COM IDENTIDADE VISUAL RPA -->
<!-- ====================== -->
<script>
$(function() {
  
  // ==================== 1. CRIAR HTML DO MODAL DINAMICAMENTE ====================
  
  const modalHTML = `
    <!-- Modal Container -->
    <div id="whatsapp-modal" style="display: none; position: fixed; z-index: 99999; left: 0; top: 0; width: 100%; height: 100%; overflow: auto;">
      <!-- Overlay -->
      <div class="whatsapp-modal-overlay" style="position: fixed; z-index: 99998; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0, 51, 102, 0.35);"></div>
      
      <!-- Conteúdo do Modal -->
      <div class="whatsapp-modal-content" style="position: relative; z-index: 99999; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); margin: 50px auto; padding: 0; border-radius: 20px; box-shadow: 0 30px 60px rgba(0, 51, 102, 0.15); width: 90%; max-width: 600px; max-height: 90vh; overflow-y: auto; font-family: 'Titillium Web', sans-serif;">
        
        <!-- Header com Gradiente -->
        <div class="whatsapp-modal-header" style="background: linear-gradient(135deg, #003366 0%, #0099CC 100%); padding: 30px 30px 20px; text-align: center; border-radius: 20px 20px 0 0; position: relative;">
          
          <!-- Botão Fechar -->
          <button class="whatsapp-modal-close" style="position: absolute; right: 15px; top: 15px; font-size: 32px; font-weight: bold; color: #FFFFFF; cursor: pointer; border: none; background: rgba(255, 255, 255, 0.1); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease; z-index: 100000;">&times;</button>
          
          <h2 style="color: #FFFFFF; font-size: 28px; margin: 0 0 10px; font-weight: 700;">Solicitar Cotação</h2>
          <p style="color: rgba(255, 255, 255, 0.95); font-size: 16px; margin: 0; line-height: 1.5; font-weight: 400;">
            Antes de prosseguirmos para o whatsapp, preencha os campos abaixo, necessários para que o cálculo do seu seguro seja efetuado com precisão
          </p>
        </div>
        
        <!-- Formulário -->
        <form id="whatsapp-form-modal" class="whatsapp-form" style="padding: 30px; background: #FFFFFF;">
          
          <!-- DDD -->
          <div class="whatsapp-field-group" style="margin-bottom: 25px;">
            <label for="modal-ddd-celular" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">DDD*</label>
            <input type="text" id="modal-ddd-celular" name="DDD" style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" maxlength="2" />
          </div>
          
          <!-- Telefone Celular -->
          <div class="whatsapp-field-group" style="margin-bottom: 25px;">
            <label for="modal-celular-completo" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Telefone Celular*</label>
            <input type="text" id="modal-celular-completo" name="CELULAR" style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" />
          </div>
          
          <!-- CPF -->
          <div class="whatsapp-field-group" style="margin-bottom: 25px;">
            <label for="modal-cpf-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">CPF*</label>
            <input type="text" id="modal-cpf-modal" name="CPF" style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" />
          </div>
          
          <!-- CEP -->
          <div class="whatsapp-field-group" style="margin-bottom: 25px;">
            <label for="modal-cep-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">CEP*</label>
            <input type="text" id="modal-cep-modal" name="CEP" style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" />
          </div>
          
          <!-- Placa -->
          <div class="whatsapp-field-group" style="margin-bottom: 25px;">
            <label for="modal-placa-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Placa*</label>
            <input type="text" id="modal-placa-modal" name="PLACA" style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333; text-transform: uppercase;" />
          </div>
          
          <!-- Botão Submit -->
          <button type="submit" class="whatsapp-submit-btn" style="width: 100%; padding: 16px 24px; background: linear-gradient(135deg, #0099CC 0%, #003366 100%); color: #FFFFFF; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; font-family: 'Titillium Web', sans-serif; box-shadow: 0 4px 15px rgba(0, 51, 102, 0.2);">
            Solicitar Cotação
          </button>
          
        </form>
      </div>
    </div>
  `;
  
  // Inserir modal no body
  $('body').append(modalHTML);
  
  // ==================== 2. CSS ADICIONAL PARA HOVERS ====================
  
  $('<style>').html(`
    #whatsapp-modal .whatsapp-modal-close:hover {
      background: rgba(255, 255, 255, 0.2) !important;
      transform: scale(1.1);
    }
    
    #whatsapp-modal input[type="text"]:focus {
      outline: none !important;
      border-color: #0099CC !important;
      box-shadow: 0 0 0 3px rgba(0, 153, 204, 0.1) !important;
    }
    
    #whatsapp-modal .whatsapp-submit-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 51, 102, 0.3) !important;
    }
    
    #whatsapp-modal .whatsapp-submit-btn:active {
      transform: translateY(0);
    }
    
    @media (max-width: 767px) {
      #whatsapp-modal .whatsapp-modal-content {
        width: 95% !important;
        margin: 20px auto !important;
      }
      
      #whatsapp-modal .whatsapp-modal-header {
        padding: 25px 20px 15px !important;
      }
      
      #whatsapp-modal .whatsapp-modal-header h2 {
        font-size: 24px !important;
      }
      
      #whatsapp-modal .whatsapp-form {
        padding: 20px !important;
      }
    }
  `).appendTo('head');
  
  // ==================== 3. VARIÁVEIS ====================
  
  const $modal = $('#whatsapp-modal');
  const $overlay = $('.whatsapp-modal-overlay');
  const $closeBtn = $('.whatsapp-modal-close');
  const $form = $('#whatsapp-form-modal');
  
  // Campos do formulário modal
  const $modalDDD = $('#modal-ddd-celular');
  const $modalCELULAR = $('#modal-celular-completo');
  const $modalCPF = $('#modal-cpf-modal');
  const $modalCEP = $('#modal-cep-modal');
  const $modalPLACA = $('#modal-placa-modal');
  
  // ==================== 4. MÁSCARAS ====================
  
  // Aplicar máscaras nos campos do modal (mesmas do formulário principal)
  if ($modalDDD.length) $modalDDD.mask('00', { clearIfNotMatch: false });
  if ($modalCELULAR.length) $modalCELULAR.mask('00000-0000', { clearIfNotMatch: false });
  if ($modalCPF.length) $modalCPF.mask('000.000.000-00');
  if ($modalCEP.length) $modalCEP.mask('00000-000');
  if ($modalPLACA.length) aplicarMascaraPlaca($modalPLACA);
  
  // ==================== 5. VALIDAÇÕES EM TEMPO REAL (ON BLUR) ====================
  
  // DDD → valida no BLUR
  $modalDDD.on('blur.siWhatsAppModal', function(){
    const dddDigits = onlyDigits($(this).val()).length;
    
    if (dddDigits > 0 && dddDigits < 2) {
      saWarnConfirmCancel({
        title: 'DDD incompleto',
        html: 'O DDD precisa ter 2 dígitos.<br><br>Deseja corrigir?'
      }).then(r => { if (r.isConfirmed) $modalDDD.focus(); });
      return;
    }
    
    if (dddDigits > 2) {
      saWarnConfirmCancel({
        title: 'DDD inválido',
        html: 'O DDD deve ter exatamente 2 dígitos.<br><br>Deseja corrigir?'
      }).then(r => { if (r.isConfirmed) $modalDDD.focus(); });
      return;
    }
  });
  
  // CELULAR → valida no BLUR
  $modalCELULAR.on('blur.siWhatsAppModal', function(){
    const dddDigits = onlyDigits($modalDDD.val()).length;
    const celDigits = onlyDigits($(this).val()).length;
    
    if (dddDigits !== 2) {
      saWarnConfirmCancel({
        title: 'DDD inválido',
        html: 'O DDD precisa ter 2 dígitos.<br><br>Deseja corrigir?'
      }).then(r => { if (r.isConfirmed) $modalDDD.focus(); });
      return;
    }
    
    if (celDigits > 0 && celDigits < 9) {
      saWarnConfirmCancel({
        title: 'Celular incompleto',
        html: 'O celular precisa ter 9 dígitos.<br><br>Deseja corrigir?'
      }).then(r => { if (r.isConfirmed) $modalCELULAR.focus(); });
      return;
    }
    
    if (dddDigits === 2 && celDigits === 9){
      showLoading('Validando celular…');
      validarTelefoneAsync($modalDDD, $modalCELULAR).then(res => {
        hideLoading();
        if (!res.ok){
          const numero = `${($modalDDD.val()||'').trim()}-${($modalCELULAR.val()||'').trim()}`;
          saWarnConfirmCancel({
            title: 'Celular inválido',
            html: `Parece que o celular informado<br><br><b>${numero}</b><br><br>não é válido.<br><br>Deseja corrigir?`
          }).then(r => { if (r.isConfirmed) $modalCELULAR.focus(); });
        }
      }).catch(_ => hideLoading());
    }
  });
  
  // CPF → valida no CHANGE
  $modalCPF.on('change.siWhatsAppModal', function(){
    const cpfValue = $(this).val();
    
    if (!validarCPFAlgoritmo(cpfValue)) {
      saWarnConfirmCancel({
        title: 'CPF inválido',
        html: 'Deseja corrigir?'
      }).then(r => { if (r.isConfirmed) $modalCPF.focus(); });
      return;
    }
    
    if (!VALIDAR_PH3A) {
      return;
    }
    
    showLoading('Consultando dados do CPF…');
    validarCPFApi(cpfValue).then(res => {
      hideLoading();
      
      if (res.ok && res.parsed) {
        console.log('✅ CPF válido no modal');
      } else if (res.reason === 'nao_encontrado') {
        saInfoConfirmCancel({
          title: 'CPF não encontrado',
          html: 'O CPF é válido, mas não foi encontrado na nossa base de dados.<br><br>Deseja preencher os dados manualmente?'
        }).then(r => {
          if (r.isConfirmed) {
            console.log('✅ CPF válido mas não encontrado - prosseguindo');
          }
        });
      }
    }).catch(_ => {
      hideLoading();
      console.log('Erro na consulta da API PH3A no modal');
    });
  });
  
  // CEP → valida no CHANGE
  $modalCEP.on('change.siWhatsAppModal', function(){
    const val = $(this).val();
    showLoading('Validando CEP…');
    validarCepViaCep(val).then(res => {
      hideLoading();
      if (!res.ok){
        saWarnConfirmCancel({
          title: 'CEP inválido',
          html: 'Deseja corrigir?'
        }).then(r => { if (r.isConfirmed) $modalCEP.focus(); });
      }
    }).catch(_ => hideLoading());
  });
  
  // PLACA → valida no CHANGE
  $modalPLACA.on('change.siWhatsAppModal', function(){
    showLoading('Validando placa…');
    validarPlacaApi($(this).val()).then(res => {
      hideLoading();
      if (!res.ok){
        saWarnConfirmCancel({
          title: 'Placa inválida',
          html: 'Deseja corrigir?'
        }).then(r => { if (r.isConfirmed) $modalPLACA.focus(); });
      }
    }).catch(_ => hideLoading());
  });
  
  // ==================== 6. EVENTOS DE ABERTURA/FECHAMENTO ====================
  
  // Abrir modal ao clicar no link whatsapplink
  $(document).on('click', '#whatsapplink', function(e) {
    e.preventDefault();
    e.stopPropagation();
    console.log('🎯 [MODAL] Abrindo modal WhatsApp');
    $modal.fadeIn(300);
  });
  
  // Fechar modal ao clicar no X
  $closeBtn.on('click', function() {
    console.log('🎯 [MODAL] Fechando modal (X)');
    $modal.fadeOut(300);
  });
  
  // Fechar modal ao clicar no overlay
  $overlay.on('click', function() {
    console.log('🎯 [MODAL] Fechando modal (overlay)');
    $modal.fadeOut(300);
  });
  
  // Fechar modal com ESC
  $(document).on('keydown', function(e) {
    if (e.key === 'Escape' && $modal.is(':visible')) {
      console.log('🎯 [MODAL] Fechando modal (ESC)');
      $modal.fadeOut(300);
    }
  });
  
  // ==================== 7. VALIDAÇÃO NO SUBMIT ====================
  
  $form.on('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    console.log('🎯 [MODAL] Submit do formulário modal');
    
    // Mostrar loading
    showLoading('Validando seus dados…');
    
    // Executar todas as validações em paralelo
    Promise.all([
      $modalDDD.val() && $modalCELULAR.val() 
        ? validarTelefoneAsync($modalDDD, $modalCELULAR) 
        : Promise.resolve({ok: ($modalDDD.val().length === 2 && $modalCELULAR.val().length >= 9)}),
      $modalCPF.val() ? validarCPFApi($modalCPF.val()) : Promise.resolve({ok: true}),
      $modalCEP.val() ? validarCepViaCep($modalCEP.val()) : Promise.resolve({ok: true}),
      $modalPLACA.val() ? validarPlacaApi($modalPLACA.val()) : Promise.resolve({ok: true})
    ])
    .then(([telRes, cpfRes, cepRes, placaRes]) => {
      hideLoading();
      
      const invalido = (!telRes.ok) || (!cpfRes.ok) || (!cepRes.ok) || (!placaRes.ok);
      console.log('🔍 [MODAL] Dados inválidos?', invalido);
      
      if (!invalido) {
        // ✅ Dados válidos - Fechar modal e abrir WhatsApp
        console.log('✅ [MODAL] Dados válidos - Fechando modal e abrindo WhatsApp');
        $modal.fadeOut(300, function() {
          // Construir URL do WhatsApp com GCLID
          let gclid = '';
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.indexOf('gclid=') === 0) {
              gclid = cookie.substring(6);
              break;
            }
          }
          
          const whatsappUrl = gclid 
            ? `https://api.whatsapp.com/send?phone=551132301422&text=Olá.%20Quero%20fazer%20uma%20cotação%20de%20seguro.%20Código%20de%20Desconto=%20${gclid}`
            : `https://api.whatsapp.com/send?phone=551132301422&text=Olá.%20Quero%20fazer%20uma%20cotação%20de%20seguro.`;
          
          window.open(whatsappUrl, '_blank');
        });
        
      } else {
        // ❌ Dados inválidos - Mostrar SweetAlert
        console.log('❌ [MODAL] Dados inválidos - Mostrando SweetAlert');
        
        let linhas = "";
        if (!telRes.ok)   linhas += "• DDD/Celular inválido\n";
        if (!cpfRes.ok)   linhas += "• CPF inválido\n";
        if (!cepRes.ok)   linhas += "• CEP inválido\n";
        if (!placaRes.ok) linhas += "• Placa inválida\n";
        
        Swal.fire({
          icon: 'info',
          title: 'Atenção!',
          html:
            "⚠️ Os campos DDD, Celular, CPF, CEP e Placa corretamente preenchidos são necessários para efetuar o cálculo do seguro.\n\n" +
            "Campos com problema:\n\n" + linhas + "\n" +
            "Caso decida prosseguir assim mesmo, um especialista entrará em contato para coletar esses dados.",
          showCancelButton: true,
          confirmButtonText: 'Prosseguir assim mesmo',
          cancelButtonText: 'Corrigir',
          reverseButtons: true,
          allowOutsideClick: false,
          allowEscapeKey: true
        }).then(r => {
          if (r.isConfirmed) {
            // Usuário escolheu prosseguir - Fechar modal e abrir WhatsApp
            console.log('🎯 [MODAL] Usuário escolheu prosseguir com dados inválidos');
            $modal.fadeOut(300, function() {
              let gclid = '';
              const cookies = document.cookie.split(';');
              for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.indexOf('gclid=') === 0) {
                  gclid = cookie.substring(6);
                  break;
                }
              }
              
              const whatsappUrl = gclid 
                ? `https://api.whatsapp.com/send?phone=551132301422&text=Olá.%20Quero%20fazer%20uma%20cotação%20de%20seguro.%20Código%20de%20Desconto=%20${gclid}`
                : `https://api.whatsapp.com/send?phone=551132301422&text=Olá.%20Quero%20fazer%20uma%20cotação%20de%20seguro.`;
              
              window.open(whatsappUrl, '_blank');
            });
          } else {
            // Usuário escolheu corrigir - Focar no primeiro campo inválido
            if (!telRes.ok && $modalDDD.length) { $modalDDD.focus(); return; }
            if (!cpfRes.ok && $modalCPF.length) { $modalCPF.focus(); return; }
            if (!cepRes.ok && $modalCEP.length) { $modalCEP.focus(); return; }
            if (!placaRes.ok && $modalPLACA.length) { $modalPLACA.focus(); return; }
          }
        });
      }
    })
    .catch(_ => {
      hideLoading();
      Swal.fire({
        icon: 'info',
        title: 'Não foi possível validar agora',
        html: 'Deseja prosseguir assim mesmo?',
        showCancelButton: true,
        confirmButtonText: 'Prosseguir assim mesmo',
        cancelButtonText: 'Corrigir',
        reverseButtons: true,
        allowOutsideClick: false,
        allowEscapeKey: true
      }).then(r => {
        if (r.isConfirmed) {
          // Usuário escolheu prosseguir após erro de rede
          console.log('🎯 [MODAL] Usuário escolheu prosseguir após erro de rede');
          $modal.fadeOut(300, function() {
            let gclid = '';
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.indexOf('gclid=') === 0) {
                gclid = cookie.substring(6);
                break;
              }
            }
            
            const whatsappUrl = gclid 
              ? `https://api.whatsapp.com/send?phone=551132301422&text=Olá.%20Quero%20fazer%20uma%20cotação%20de%20seguro.%20Código%20de%20Desconto=%20${gclid}`
              : `https://api.whatsapp.com/send?phone=551132301422&text=Olá.%20Quero%20fazer%20uma%20cotação%20de%20seguro.`;
            
            window.open(whatsappUrl, '_blank');
          });
        }
      });
    });
  });
  
  console.log('✅ [MODAL] Sistema de modal WhatsApp inicializado');
});
</script>
<!-- ====================== -->
```

---

## 🔗 INTEGRAÇÃO

### **Passo 1: Fonte Titillium Web**

Adicionar no `<head>` do Footer Code (se ainda não existir):

```html
<link href="https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&display=swap" rel="stylesheet">
```

### **Passo 2: Inserir Código no Footer Code**

1. Abrir `Footer Code Site Definitivo.js`
2. Localizar o final do último `<script>` (antes de `</script>` ou `<!-- ====================== -->`)
3. Inserir todo o código do bloco JavaScript fornecido acima
4. Salvar

### **Passo 3: Verificar Dependências**

Garantir que o Footer Code já possui:
- ✅ jQuery (`$`)
- ✅ jQuery Mask
- ✅ SweetAlert2
- ✅ Funções de validação (`validarCPFApi`, `validarPlacaApi`, etc.)
- ✅ Funções de alert (`saWarnConfirmCancel`, `saInfoConfirmCancel`)
- ✅ Função de loading (`showLoading`, `hideLoading`)

---

## 🧪 TESTES

### **Página de Teste**

Criar arquivo `teste-modal-whatsapp.html`:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teste Modal WhatsApp</title>
    
    <!-- jQuery -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    
    <!-- jQuery Mask -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
    
    <!-- SweetAlert2 -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.14.0/dist/sweetalert2.all.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.14.0/dist/sweetalert2.min.css"/>
    
    <!-- Titillium Web -->
    <link href="https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Titillium Web', sans-serif;
            max-width: 1200px;
            margin: 50px auto;
            padding: 20px;
            background: #F8F9FA;
        }
        
        .test-button {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(135deg, #0099CC 0%, #003366 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s ease;
        }
        
        .test-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 51, 102, 0.3);
        }
    </style>
</head>
<body>
    <h1>🎯 Teste Modal WhatsApp</h1>
    <p>
        <button id="whatsapplink" class="test-button">
            📱 Abrir Modal WhatsApp
        </button>
    </p>
    
    <!-- Copiar todo o código JavaScript do modal aqui -->
    <!-- [CÓDIGO JAVASCRIPT DO MODAL] -->
    
</body>
</html>
```

### **Cenários de Teste**

1. ✅ Abrir modal (click em #whatsapplink)
2. ✅ Fechar modal (botão X)
3. ✅ Fechar modal (overlay)
4. ✅ Fechar modal (ESC)
5. ✅ Validação DDD (blur)
6. ✅ Validação Celular (blur + API)
7. ✅ Validação CPF (change)
8. ✅ Validação CEP (change)
9. ✅ Validação Placa (change)
10. ✅ Submit com dados válidos
11. ✅ Submit com dados inválidos (SweetAlert)
12. ✅ Abertura do WhatsApp

---

## 📝 PRÓXIMOS PASSOS

### **Fase 1: Implementação** ⏳
- [ ] Inserir código no Footer Code
- [ ] Adicionar link Titillium Web no head
- [ ] Fazer backup do Footer Code

### **Fase 2: Testes** ⏳
- [ ] Testar em ambiente de desenvolvimento
- [ ] Validar todos os cenários
- [ ] Ajustar CSS se necessário

### **Fase 3: Deploy** ⏳
- [ ] Publicar no Webflow
- [ ] Testar em produção
- [ ] Monitorar conversões

---

## 📚 REFERÊNCIAS

- **Footer Code**: `Footer Code Site Definitivo.js`
- **Modal RPA**: `webflow_injection_limpo.js`
- **SweetAlert2**: [Documentação](https://sweetalert2.github.io/)
- **jQuery Mask**: [Documentação](https://igorescobar.github.io/jQuery-Mask-Plugin/)

---

## 🎯 RESUMO

O modal WhatsApp é uma alternativa ao Collect Chat que:

✅ **Coleta dados necessários** antes de abrir WhatsApp  
✅ **Valida em tempo real** (blur) e no submit  
✅ **Mantém identidade visual** do modal RPA  
✅ **Integra com GCLID** para rastreamento  
✅ **Permite prosseguir** mesmo com dados inválidos  
✅ **Respeita acessibilidade** (ESC para fechar, teclado, etc.)  

**Status**: ✅ PRONTO PARA IMPLEMENTAÇÃO


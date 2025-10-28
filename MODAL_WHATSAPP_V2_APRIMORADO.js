// ======================
// MODAL WHATSAPP LEADS V2.0 - VERSÃO APRIMORADA
// Baseado na análise do Engenheiro de Software
// ======================

$(function() {
  
  // ==================== CONSTANTES E CONFIGURAÇÕES ====================
  
  const MODAL_CONFIG = {
    selectors: {
      trigger: '#whatsapplink',
      modal: '#whatsapp-modal',
      overlay: '.whatsapp-modal-overlay',
      closeBtn: '.whatsapp-modal-close',
      form: '#whatsapp-form-modal'
    },
    fieldIds: {
      ddd: '#modal-ddd-celular',
      celular: '#modal-celular-completo',
      cpf: '#modal-cpf-modal',
      cep: '#modal-cep-modal',
      placa: '#modal-placa-modal'
    },
    whatsapp: {
      phone: '551132301422',
      messages: {
        withGCLID: 'Olá.%20Quero%20fazer%20uma%20cotação%20de%20seguro.%20Código%20de%20Desconto=%20',
        withoutGCLID: 'Olá.%20Quero%20fazer%20uma%20cotação%20de%20seguro.'
      }
    },
    debounce: {
      ddd: 300,
      celular: 500,
      cpf: 400,
      cep: 400,
      placa: 400
    }
  };
  
  // Timers para debounce
  const timers = {};
  
  // ==================== UTILITÁRIOS ====================
  
  /**
   * Escapa HTML para prevenir XSS
   */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  /**
   * Obtém GCLID dos cookies
   */
  function getGCLID() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.indexOf('gclid=') === 0) {
        return cookie.substring(6);
      }
    }
    return '';
  }
  
  /**
   * Constrói URL do WhatsApp com GCLID
   */
  function buildWhatsAppURL(gclid = '') {
    const baseUrl = 'https://api.whatsapp.com/send';
    const phone = MODAL_CONFIG.whatsapp.phone;
    const message = gclid 
      ? `${MODAL_CONFIG.whatsapp.messages.withGCLID}${gclid}`
      : MODAL_CONFIG.whatsapp.messages.withoutGCLID;
    
    return `${baseUrl}?phone=${phone}&text=${message}`;
  }
  
  /**
   * Abre WhatsApp após fechar modal
   */
  function openWhatsApp(delay = 300) {
    const gclid = getGCLID();
    const whatsappUrl = buildWhatsAppURL(gclid);
    console.log('🚀 [MODAL] Abrindo WhatsApp:', whatsappUrl);
    window.open(whatsappUrl, '_blank');
  }
  
  /**
   * Aplica debounce em função
   */
  function debounce(func, delay, context = null) {
    return function(...args) {
      const self = context || this;
      clearTimeout(timers[func.name]);
      timers[func.name] = setTimeout(() => func.apply(self, args), delay);
    };
  }
  
  // ==================== 1. CRIAR HTML DO MODAL DINAMICAMENTE ====================
  
  const modalHTML = `
    <!-- Modal Container -->
    <div id="whatsapp-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title" aria-describedby="modal-description" style="display: none; position: fixed; z-index: 99999; left: 0; top: 0; width: 100%; height: 100%; overflow: auto;">
      <!-- Overlay -->
      <div class="whatsapp-modal-overlay" style="position: fixed; z-index: 99998; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0, 51, 102, 0.35);"></div>
      
      <!-- Conteúdo do Modal -->
      <div class="whatsapp-modal-content" style="position: relative; z-index: 99999; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); margin: 50px auto; padding: 0; border-radius: 20px; box-shadow: 0 30px 60px rgba(0, 51, 102, 0.15); width: 90%; max-width: 600px; max-height: 90vh; overflow-y: auto; font-family: 'Titillium Web', sans-serif;">
        
        <!-- Header com Gradiente -->
        <div class="whatsapp-modal-header" style="background: linear-gradient(135deg, #003366 0%, #0099CC 100%); padding: 30px 30px 20px; text-align: center; border-radius: 20px 20px 0 0; position: relative;">
          
          <!-- Botão Fechar -->
          <button 
            class="whatsapp-modal-close" 
            aria-label="Fechar modal"
            role="button"
            tabindex="0"
            style="position: absolute; right: 15px; top: 15px; font-size: 32px; font-weight: bold; color: #FFFFFF; cursor: pointer; border: none; background: rgba(255, 255, 255, 0.1); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease; z-index: 100000;">
            &times;
          </button>
          
          <h2 id="modal-title" style="color: #FFFFFF; font-size: 28px; margin: 0 0 10px; font-weight: 700;">Solicitar Cotação</h2>
          <p id="modal-description" style="color: rgba(255, 255, 255, 0.95); font-size: 16px; margin: 0; line-height: 1.5; font-weight: 400;">
            Antes de prosseguirmos para o whatsapp, preencha os campos abaixo, necessários para que o cálculo do seu seguro seja efetuado com precisão
          </p>
        </div>
        
        <!-- Formulário -->
        <form id="whatsapp-form-modal" class="whatsapp-form" style="padding: 30px; background: #FFFFFF;">
          
          <!-- DDD e Telefone na mesma linha -->
          <div style="display: flex; gap: 1.5%; margin-bottom: 25px; align-items: flex-start;">
            <!-- DDD -->
            <div class="whatsapp-field-group" style="flex: 0 0 14.3%;">
              <label for="modal-ddd-celular" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">DDD*</label>
              <input 
                type="text" 
                id="modal-ddd-celular" 
                name="DDD" 
                aria-required="true"
                aria-describedby="ddd-help"
                maxlength="2"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
              />
              <small id="ddd-help" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;">DDD deve ter 2 dígitos</small>
            </div>
            
            <!-- Telefone Celular -->
            <div class="whatsapp-field-group" style="flex: 1; min-width: 0;">
              <label for="modal-celular-completo" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Telefone Celular*</label>
              <input 
                type="text" 
                id="modal-celular-completo" 
                name="CELULAR"
                aria-required="true"
                aria-describedby="celular-help"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
              />
              <small id="celular-help" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;">Celular deve ter 9 dígitos</small>
            </div>
          </div>
          
          <!-- CPF -->
          <div class="whatsapp-field-group" style="margin-bottom: 25px;">
            <label for="modal-cpf-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">CPF*</label>
            <input 
              type="text" 
              id="modal-cpf-modal" 
              name="CPF"
              aria-required="true"
              aria-describedby="cpf-help"
              style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
            />
            <small id="cpf-help" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;">CPF deve ter 11 dígitos válidos</small>
          </div>
          
          <!-- NOME -->
          <div class="whatsapp-field-group" style="margin-bottom: 25px;">
            <label for="modal-nome-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Nome</label>
            <input 
              type="text" 
              id="modal-nome-modal" 
              name="NOME"
              style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
            />
          </div>
          
          <!-- CEP e Placa na mesma linha -->
          <div style="display: flex; gap: 1.5%; margin-bottom: 25px; align-items: flex-start;">
            <!-- CEP -->
            <div class="whatsapp-field-group" style="flex: 1; min-width: 0;">
              <label for="modal-cep-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">CEP*</label>
              <input 
                type="text" 
                id="modal-cep-modal" 
                name="CEP"
                aria-required="true"
                aria-describedby="cep-help"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
              />
              <small id="cep-help" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;">CEP deve ter 8 dígitos</small>
            </div>
            
            <!-- Placa -->
            <div class="whatsapp-field-group" style="flex: 1; min-width: 0;">
              <label for="modal-placa-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Placa*</label>
              <input 
                type="text" 
                id="modal-placa-modal" 
                name="PLACA"
                aria-required="true"
                aria-describedby="placa-help"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333; text-transform: uppercase;" 
              />
              <small id="placa-help" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;">Placa deve ter formato ABC1D23 ou ABC1234</small>
            </div>
          </div>
          
          <!-- Botão Submit -->
          <button 
            type="submit" 
            class="whatsapp-submit-btn"
            aria-label="Prosseguir para o WhatsApp"
            style="width: 100%; padding: 16px 24px; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: #FFFFFF; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; font-family: 'Titillium Web', sans-serif; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3); display: flex; align-items: center; justify-content: center; gap: 10px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="background: white; border-radius: 50%; padding: 4px;">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" fill="#128C7E"/>
            </svg>
            PROSSEGUIR PARA O WHATSAPP
          </button>
          
        </form>
      </div>
    </div>
  `;
  
  // Inserir modal no body
  $('body').append(modalHTML);
  
  // ==================== 2. CSS ADICIONAL PARA HOVERS E FEEDBACK VISUAL ====================
  
  $('<style>').html(`
    #whatsapp-modal .whatsapp-modal-close:hover {
      background: rgba(255, 255, 255, 0.2) !important;
      transform: scale(1.1);
    }
    
    /* Feedback visual de validação */
    #whatsapp-modal input[type="text"].field-error {
      border-color: #e74c3c !important;
      background-color: #fff5f5 !important;
    }
    
    #whatsapp-modal input[type="text"].field-success {
      border-color: #27ae60 !important;
      background-color: #f0fff4 !important;
    }
    
    #whatsapp-modal input[type="text"]:focus {
      outline: none !important;
      border-color: #0099CC !important;
      box-shadow: 0 0 0 3px rgba(0, 153, 204, 0.1) !important;
    }
    
    #whatsapp-modal .whatsapp-submit-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4) !important;
    }
    
    #whatsapp-modal .whatsapp-submit-btn:active {
      transform: translateY(0);
    }
    
    /* Animação de loading */
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    
    .loading-indicator {
      display: inline-block;
      width: 12px;
      height: 12px;
      border: 2px solid #fff;
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 0.6s linear infinite;
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
  
  // ==================== 3. REFERÊNCIAS AOS ELEMENTOS ====================
  
  const $modal = $(MODAL_CONFIG.selectors.modal);
  const $overlay = $(MODAL_CONFIG.selectors.overlay);
  const $closeBtn = $(MODAL_CONFIG.selectors.closeBtn);
  const $form = $(MODAL_CONFIG.selectors.form);
  
  // Campos do formulário modal
  const $modalDDD = $(MODAL_CONFIG.fieldIds.ddd);
  const $modalCELULAR = $(MODAL_CONFIG.fieldIds.celular);
  const $modalCPF = $(MODAL_CONFIG.fieldIds.cpf);
  const $modalCEP = $(MODAL_CONFIG.fieldIds.cep);
  const $modalPLACA = $(MODAL_CONFIG.fieldIds.placa);
  
  // Referência ao botão de submit
  const $submitBtn = $('.whatsapp-submit-btn');
  
  // ==================== 4. FUNÇÕES HELPER PARA FEEDBACK VISUAL ====================
  
  function showFieldError($field, message) {
    $field.addClass('field-error');
    const helpId = $field.attr('aria-describedby');
    if (helpId) {
      const $help = $(`#${helpId}`);
      if ($help.length) {
        $help.text(message).show();
      }
    }
  }
  
  function showFieldSuccess($field) {
    $field.removeClass('field-error').addClass('field-success');
    const helpId = $field.attr('aria-describedby');
    if (helpId) {
      $(`#${helpId}`).hide();
    }
  }
  
  function clearFieldStatus($field) {
    $field.removeClass('field-error field-success');
    const helpId = $field.attr('aria-describedby');
    if (helpId) {
      $(`#${helpId}`).hide();
    }
  }
  
  // ==================== 5. MÁSCARAS ====================
  
  if ($modalDDD.length) $modalDDD.mask('00', { clearIfNotMatch: false });
  if ($modalCELULAR.length) $modalCELULAR.mask('00000-0000', { clearIfNotMatch: false });
  if ($modalCPF.length) $modalCPF.mask('000.000.000-00');
  if ($modalCEP.length) $modalCEP.mask('00000-000');
  if ($modalPLACA.length) aplicarMascaraPlaca($modalPLACA);
  
  // ==================== 6. VALIDAÇÕES EM TEMPO REAL COM DEBOUNCE ====================
  
  // DDD → valida no BLUR (sem debounce para validar imediatamente)
  $modalDDD.on('blur.siWhatsAppModal', function(){
    const value = $(this).val();
    clearFieldStatus($(this));
    
    if (!value) {
      return; // Campo vazio, não validar ainda
    }
    
    const dddDigits = onlyDigits(value).length;
    
    if (dddDigits !== 2) {
      showFieldError($(this), 'DDD deve ter 2 dígitos');
      setTimeout(() => $(this).focus(), 10); // Volta o foco imediatamente
      return;
    }
    
    showFieldSuccess($(this));
  });
  
  // CELULAR → valida no BLUR (com debounce e API)
  $modalCELULAR.on('blur.siWhatsAppModal', debounce(function(){
    const value = $(this).val();
    clearFieldStatus($(this));
    
    if (!value) {
      return;
    }
    
    const dddDigits = onlyDigits($modalDDD.val()).length;
    const celDigits = onlyDigits(value).length;
    
    if (dddDigits !== 2) {
      showFieldError($(this), 'DDD inválido');
      setTimeout(() => $modalDDD.focus(), 10);
      return;
    }
    
    if (celDigits < 9) {
      showFieldError($(this), 'Celular incompleto');
      setTimeout(() => $(this).focus(), 10);
      return;
    }
    
    // Validar via API
    if (celDigits === 9) {
      showLoading('Validando celular…');
      validarTelefoneAsync($modalDDD, $modalCELULAR).then(res => {
        hideLoading();
        if (!res.ok){
          showFieldError($modalCELULAR, 'Celular inválido');
          setTimeout(() => $modalCELULAR.focus(), 50); // API já tem delay, então 50ms é suficiente
        } else {
          showFieldSuccess($modalCELULAR);
        }
      }).catch(_ => hideLoading());
    }
  }, MODAL_CONFIG.debounce.celular));
  
  // CPF → valida no CHANGE (com debounce)
  $modalCPF.on('change.siWhatsAppModal', debounce(function(){
    const cpfValue = $(this).val();
    clearFieldStatus($(this));
    
    if (!cpfValue) {
      return;
    }
    
    if (!validarCPFAlgoritmo(cpfValue)) {
      showFieldError($(this), 'CPF inválido');
      setTimeout(() => $(this).focus(), 10);
      return;
    }
    
    if (!VALIDAR_PH3A) {
      showFieldSuccess($(this));
      return;
    }
    
    showLoading('Consultando dados do CPF…');
    validarCPFApi(cpfValue).then(res => {
      hideLoading();
      
      if (res.ok && res.parsed) {
        showFieldSuccess($(this));
        console.log('✅ CPF válido no modal');
      } else if (res.reason === 'nao_encontrado') {
        showFieldSuccess($(this)); // CPF válido mas não encontrado
      }
    }).catch(_ => {
      hideLoading();
      console.log('Erro na consulta da API PH3A no modal');
    });
  }, MODAL_CONFIG.debounce.cpf));
  
  // CEP → valida no CHANGE (com debounce)
  $modalCEP.on('change.siWhatsAppModal', debounce(function(){
    const val = $(this).val();
    clearFieldStatus($(this));
    
    if (!val) {
      return;
    }
    
    showLoading('Validando CEP…');
    const $cepField = $(this); // Guardar referência
    validarCepViaCep(val).then(res => {
      hideLoading();
      if (!res.ok){
        showFieldError($cepField, 'CEP inválido');
        setTimeout(() => $cepField.focus(), 50); // API já tem delay
      } else {
        showFieldSuccess($cepField);
      }
    }).catch(_ => hideLoading());
  }, MODAL_CONFIG.debounce.cep));
  
  // PLACA → valida no CHANGE (com debounce)
  $modalPLACA.on('change.siWhatsAppModal', debounce(function(){
    const value = $(this).val();
    clearFieldStatus($(this));
    
    if (!value) {
      return;
    }
    
    showLoading('Validando placa…');
    const $placaField = $(this); // Guardar referência
    validarPlacaApi(value).then(res => {
      hideLoading();
      if (!res.ok){
        showFieldError($placaField, 'Placa inválida');
        setTimeout(() => $placaField.focus(), 50); // API já tem delay
      } else {
        showFieldSuccess($placaField);
      }
    }).catch(_ => hideLoading());
  }, MODAL_CONFIG.debounce.placa));
  
  // ==================== 7. EVENTOS DE ABERTURA/FECHAMENTO ====================
  
  // Abrir modal ao clicar no link whatsapplink
  $(document).on('click', MODAL_CONFIG.selectors.trigger, function(e) {
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
  
  // ==================== 8. VALIDAÇÃO NO SUBMIT ====================
  
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
        : Promise.resolve({ok: false, reason: 'campo_vazio'}),
      $modalCPF.val() ? validarCPFApi($modalCPF.val()) : Promise.resolve({ok: false, reason: 'campo_vazio'}),
      $modalCEP.val() ? validarCepViaCep($modalCEP.val()) : Promise.resolve({ok: false, reason: 'campo_vazio'}),
      $modalPLACA.val() ? validarPlacaApi($modalPLACA.val()) : Promise.resolve({ok: false, reason: 'campo_vazio'})
    ])
    .then(([telRes, cpfRes, cepRes, placaRes]) => {
      hideLoading();
      
      const invalido = (!telRes.ok) || (!cpfRes.ok) || (!cepRes.ok) || (!placaRes.ok);
      console.log('🔍 [MODAL] Dados inválidos?', invalido);
      
      // Sempre permitir prosseguir, com feedback visual nos campos
      if (invalido) {
        console.log('⚠️ [MODAL] Dados inválidos detectados, mas prosseguindo mesmo assim');
      }
      console.log('✅ [MODAL] Fechando modal e abrindo WhatsApp');
      $modal.fadeOut(300, openWhatsApp);
    })
    .catch(error => {
      hideLoading();
      console.error('[MODAL] Erro na validação:', error);
      // Em caso de erro, prosseguir mesmo assim
      console.log('⚠️ [MODAL] Erro na validação, mas prosseguindo');
      $modal.fadeOut(300, openWhatsApp);
    });
  });
  
  console.log('✅ [MODAL] Sistema de modal WhatsApp inicializado (V2.0)');
});


// ======================
// MODAL WHATSAPP DEFINITIVO
// Conceito: DDD + CELULAR → Expansão automática com campos opcionais
// Versão: Definitiva
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
      ddd: '#DDD-CELULAR-MODAL',
      celular: '#CELULAR-MODAL',
      cpf: '#CPF-MODAL',
      nome: '#NOME-MODAL',
      cep: '#CEP-MODAL',
      placa: '#PLACA-MODAL',
      endereco: '#ENDERECO-MODAL'
    },
    whatsapp: {
      phone: '551132301422',
      message: 'Olá! Quero uma cotação de seguro.'
    }
  };
  
  const timers = {};
  
  // ==================== UTILITÁRIOS ====================
  
  function onlyDigits(str) {
    return (str || '').replace(/\D+/g, '');
  }
  
  function debounce(func, delay, context = null) {
    return function(...args) {
      const self = context || this;
      clearTimeout(timers[func.name]);
      timers[func.name] = setTimeout(() => func.apply(self, args), delay);
    };
  }
  
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
  
  function buildWhatsAppMessage(dados) {
    // Mensagem simples como especificado
    return 'Ola.%20Quero%20fazer%20uma%20cotacao%20de%20seguro.';
  }
  
  function openWhatsApp(dados) {
    const mensagem = buildWhatsAppMessage(dados);
    const url = `https://api.whatsapp.com/send?phone=${MODAL_CONFIG.whatsapp.phone}&text=${mensagem}`;
    console.log('🚀 [MODAL] Abrindo WhatsApp:', url);
    window.open(url, '_blank');
  }
  
  function coletarTodosDados() {
    return {
      TELEFONE: $(MODAL_CONFIG.fieldIds.ddd).val() + $(MODAL_CONFIG.fieldIds.celular).val(),
      CPF: $(MODAL_CONFIG.fieldIds.cpf).val() || '',
      NOME: $(MODAL_CONFIG.fieldIds.nome).val() || '',
      CEP: $(MODAL_CONFIG.fieldIds.cep).val() || '',
      PLACA: $(MODAL_CONFIG.fieldIds.placa).val() || '',
      ENDERECO: $(MODAL_CONFIG.fieldIds.endereco).val() || ''
    };
  }
  
  // ==================== 1. CRIAR HTML DO MODAL ====================
  
  const modalHTML = `
    <!-- Modal Container -->
    <div id="whatsapp-modal" style="display: none; position: fixed; inset: 0; z-index: 99999;">
      
      <!-- Overlay -->
      <div class="whatsapp-modal-overlay" style="position: fixed; inset: 0; background-color: rgba(0, 51, 102, 0.35);"></div>
      
      <!-- Conteúdo do Modal -->
      <div class="whatsapp-modal-content" style="position: fixed; z-index: 100000; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); padding: 0; border-radius: 20px; box-shadow: 0 30px 60px rgba(0, 51, 102, 0.15); width: auto; max-height: 85vh; overflow-y: auto; font-family: 'Titillium Web', sans-serif;">
        
        <!-- Header -->
        <div class="whatsapp-modal-header" style="background: linear-gradient(135deg, #003366 0%, #0099CC 100%); padding: 30px 30px 20px; text-align: center; border-radius: 20px 20px 0 0; position: relative;">
          
          <!-- Botão Fechar -->
          <button 
            class="whatsapp-modal-close" 
            style="position: absolute; right: 15px; top: 15px; font-size: 32px; font-weight: bold; color: #FFFFFF; cursor: pointer; border: none; background: rgba(255, 255, 255, 0.1); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease; z-index: 100000;">
            &times;
          </button>
          
          <h2 style="color: #FFFFFF; font-size: 28px; margin: 0 0 10px; font-weight: 700;">Solicitar Cotação</h2>
          <p style="color: rgba(255, 255, 255, 0.95); font-size: 16px; margin: 0; line-height: 1.5; font-weight: 400;">
            Quer uma cotação de seguro? Comece pelo seu telefone!
          </p>
        </div>
        
        <!-- Formulário -->
        <form id="whatsapp-form-modal" style="padding: 30px; background: #FFFFFF;">
          
          <!-- DIV 1: DDD + CELULAR (Sempre Visível) -->
          <div id="div-etapa-1" class="modal-div">
            
            <!-- DDD e Celular na mesma linha -->
            <div style="display: flex; gap: 1.5%; margin-bottom: 25px; align-items: flex-start;">
              <!-- DDD -->
              <div class="field-group" style="flex: 0 0 30%;">
                <label for="DDD-CELULAR-MODAL" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">DDD*</label>
                <input 
                  type="text" 
                  id="DDD-CELULAR-MODAL" 
                  name="DDD" 
                  placeholder="11"
                  maxlength="2"
                  style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
                />
                <small class="help-message" style="display: none; font-size: 12px; margin-top: 4px;"></small>
              </div>
              
              <!-- Telefone Celular -->
              <div class="field-group" style="flex: 1; min-width: 0;">
                <label for="CELULAR-MODAL" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Telefone Celular*</label>
                <input 
                  type="tel" 
                  id="CELULAR-MODAL" 
                  name="CELULAR"
                  placeholder="99999-9999"
                  autocomplete="tel"
                  style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
                />
                <small class="help-message" style="display: none; font-size: 12px; margin-top: 4px;"></small>
              </div>
            </div>
            
          </div>
          
          <!-- DIV 2: CAMPOS OPCIONAIS (Aparece após preencher DDD + Celular) -->
          <div id="div-etapa-2" class="modal-div" style="display: none; margin-top: 20px; padding-top: 20px; border-top: 2px solid #f0f0f0;">
            
            <!-- Mensagem Central no Topo -->
            <div class="optional-message" style="text-align: center; padding: 20px 15px; margin-bottom: 25px; background: linear-gradient(135deg, #f8f9fa 0%, #f0f7ff 100%); border-radius: 12px; border: 1px solid #e0e7ff;">
              <p style="margin: 0; font-size: 15px; color: #003366; font-weight: 600; line-height: 1.5;">
                Esses campos são <strong>opcionais</strong>, mas, ao preenchê-los, você garante um cálculo <strong>mais rápido, completo e personalizado</strong>. Agradecemos sua colaboração!
              </p>
            </div>
            
            <!-- CPF -->
            <div class="field-group" style="margin-bottom: 20px;">
              <label for="CPF-MODAL" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">CPF</label>
              <input 
                type="text" 
                id="CPF-MODAL" 
                name="CPF" 
                placeholder="000.000.000-00"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
              />
              <small class="help-message" style="display: none; font-size: 12px; margin-top: 4px;"></small>
            </div>
            
            <!-- Nome -->
            <div class="field-group" style="margin-bottom: 20px;">
              <label for="NOME-MODAL" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Nome Completo</label>
              <input 
                type="text" 
                id="NOME-MODAL" 
                name="NOME" 
                placeholder="João da Silva"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
              />
            </div>
            
            <!-- CEP e Placa na mesma linha -->
            <div style="display: flex; gap: 1.5%; margin-bottom: 20px; align-items: flex-start;">
              <!-- CEP -->
              <div class="field-group" style="flex: 1; min-width: 0;">
                <label for="CEP-MODAL" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">CEP</label>
                <input 
                  type="text" 
                  id="CEP-MODAL" 
                  name="CEP" 
                  placeholder="01234-567"
                  style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
                />
                <small class="help-message" style="display: none; font-size: 12px; margin-top: 4px;"></small>
              </div>
              
              <!-- Placa -->
              <div class="field-group" style="flex: 1; min-width: 0;">
                <label for="PLACA-MODAL" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Placa do Veículo</label>
                <input 
                  type="text" 
                  id="PLACA-MODAL" 
                  name="PLACA" 
                  placeholder="ABC-1234"
                  maxlength="8"
                  style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333; text-transform: uppercase;" 
                />
                <small class="help-message" style="display: none; font-size: 12px; margin-top: 4px;"></small>
              </div>
            </div>
            
            <!-- Endereço (se CEP for preenchido) -->
            <div class="field-group" id="endereco-container" style="display: none; margin-bottom: 20px;">
              <label for="ENDERECO-MODAL" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Endereço Completo</label>
              <input 
                type="text" 
                id="ENDERECO-MODAL" 
                name="ENDERECO" 
                placeholder="Será preenchido automaticamente"
                readonly
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333; background: #f8f9fa;" 
              />
            </div>
            
            <!-- Botão Principal -->
            <button 
              type="submit" 
              class="whatsapp-submit-btn"
              style="width: 100%; padding: 16px 24px; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: #FFFFFF; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; font-family: 'Titillium Web', sans-serif; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3); display: flex; align-items: center; justify-content: center; gap: 10px;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
              IR PARA O WHATSAPP
            </button>
            
          </div>
          
        </form>
      </div>
    </div>
  `;
  
  // Inserir modal no body
  $('body').append(modalHTML);
  
  // ==================== 2. CSS ADICIONAL ====================
  
  $('<style>').html(`
    #whatsapp-modal input[type="text"].field-error,
    #whatsapp-modal input[type="tel"].field-error {
      border-color: #e74c3c !important;
      background-color: #fff5f5 !important;
    }
    
    #whatsapp-modal input[type="text"].field-warning,
    #whatsapp-modal input[type="tel"].field-warning {
      border-color: #FFB300 !important;
      background-color: #fffbf0 !important;
    }
    
    #whatsapp-modal .help-message {
      color: #FFB300 !important;
    }
    
    #whatsapp-modal input[type="text"].field-success,
    #whatsapp-modal input[type="tel"].field-success {
      border-color: #27ae60 !important;
      background-color: #f0fff4 !important;
    }
    
    #whatsapp-modal input[type="text"]:focus,
    #whatsapp-modal input[type="tel"]:focus {
      outline: none !important;
      border-color: #0099CC !important;
      box-shadow: 0 0 0 3px rgba(0, 153, 204, 0.1) !important;
    }
    
    #whatsapp-modal .whatsapp-submit-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4) !important;
    }
    
    .whatsapp-modal-close:hover {
      background: rgba(255, 255, 255, 0.2) !important;
      transform: scale(1.1);
    }
    
    /* Animação de expansão suave */
    @keyframes slideDown {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    #div-etapa-2 {
      animation: slideDown 0.4s ease;
    }
    
    /* Desktop: posição fixa no canto inferior direito */
    .whatsapp-modal-content {
      position: fixed !important;
      right: 30px !important;
      bottom: 92px !important;
      width: 450px !important;
      max-width: 450px !important;
      min-width: 300px !important;
      z-index: 100000 !important;
      box-sizing: border-box !important;
    }
    
    /* Tablet/Mobile: margens IGUAIS em ambos os lados */
    @media (max-width: 992px) {
      .whatsapp-modal-content {
        left: 15px !important;
        right: 15px !important;
        bottom: 75px !important;
        width: auto !important;
        max-width: 100% !important;
      }
    }
    
    /* Small Mobile: margens menores mas IGUAIS */
    @media (max-width: 480px) {
      .whatsapp-modal-content {
        left: 10px !important;
        right: 10px !important;
        bottom: 70px !important;
      }
    }
  `).appendTo('head');
  
  // ==================== 3. REFERÊNCIAS ====================
  
  const $modal = $(MODAL_CONFIG.selectors.modal);
  const $overlay = $(MODAL_CONFIG.selectors.overlay);
  const $closeBtn = $(MODAL_CONFIG.selectors.closeBtn);
  const $form = $(MODAL_CONFIG.selectors.form);
  
  // Posicionamento agora é controlado 100% via CSS - SEM JavaScript dinâmico
  
  // Referências aos DIVs
  const $divEtapa1 = $('#div-etapa-1');
  const $divEtapa2 = $('#div-etapa-2');
  
  // ==================== 4. MÁSCARAS ====================
  
  $(MODAL_CONFIG.fieldIds.ddd).mask('00', { clearIfNotMatch: false });
  $(MODAL_CONFIG.fieldIds.celular).mask('00000-0000', { clearIfNotMatch: false });
  $(MODAL_CONFIG.fieldIds.cpf).mask('000.000.000-00');
  $(MODAL_CONFIG.fieldIds.cep).mask('00000-000');
  $(MODAL_CONFIG.fieldIds.placa).mask('SSS-0A00', {
    translation: {
      'S': { pattern: /[A-Za-z]/, recursive: true },
      '0': { pattern: /\d/ },
      'A': { pattern: /[A-Za-z0-9]/ }
    },
    clearIfNotMatch: false,
    onKeyPress: function(value, e, field, options) {
      field.val(value.toUpperCase());
    }
  });
  
  // ==================== 5. EXPANSÃO AUTOMÁTICA ====================
  
  // Detectar quando DDD + Celular são preenchidos e expandir DIV 2
  $(MODAL_CONFIG.fieldIds.celular).on('blur', function() {
    const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
    const celular = $(this).val();
    
    const dddDigits = onlyDigits(ddd).length;
    const celularDigits = onlyDigits(celular).length;
    
    // Verificar se DDD tem 2 dígitos e celular tem 9 dígitos
    if (dddDigits === 2 && celularDigits === 9 && $divEtapa2.is(':hidden')) {
      console.log('🔍 [MODAL] DDD + Celular preenchidos, expandindo DIV 2');
      $divEtapa2.slideDown(400, function() {
        // Focar no CPF após animação de abertura
        setTimeout(function() {
          $(MODAL_CONFIG.fieldIds.cpf).focus();
        }, 100);
      });
    }
  });
  
  // ==================== 6. VALIDAÇÕES INDIVIDUAIS (ÂMBAR, SEM BLOQUEIO) ====================
  
  // DDD → valida no BLUR
  $(MODAL_CONFIG.fieldIds.ddd).on('blur', function() {
    const ddd = $(this).val();
    clearFieldStatus($(this));
    
    if (!ddd) return;
    
    const dddDigits = onlyDigits(ddd).length;
    
    if (dddDigits !== 2) {
      showFieldWarning($(this), 'DDD deve ter 2 dígitos');
      return;
    }
    
    showFieldSuccess($(this));
  });
  
  // CELULAR → valida no BLUR (com checagem de DDD e API)
  $(MODAL_CONFIG.fieldIds.celular).on('blur', debounce(function() {
    const celular = $(this).val();
    const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
    clearFieldStatus($(this));
    
    if (!celular) return;
    
    const dddDigits = onlyDigits(ddd).length;
    const celularDigits = onlyDigits(celular).length;
    
    // Validar se DDD é válido
    if (dddDigits !== 2) {
      showFieldWarning($(this), 'DDD inválido');
      return;
    }
    
    // Validar se celular tem 9 dígitos
    if (celularDigits < 9) {
      showFieldWarning($(this), 'Celular deve ter 9 dígitos');
      return;
    }
    
    // Validar via API (se função existir)
    if (celularDigits === 9 && typeof validarTelefoneAsync === 'function') {
      showLoading('Validando celular…');
      validarTelefoneAsync($(MODAL_CONFIG.fieldIds.ddd), $(this)).then(res => {
        hideLoading();
        if (!res.ok) {
          showFieldWarning($(this), 'Celular inválido');
        } else {
          showFieldSuccess($(this));
        }
      }).catch(_ => hideLoading());
    } else {
      // Se não houver função de API, apenas valida formato
      showFieldSuccess($(this));
    }
  }, 500));
  
  // CPF → valida no BLUR
  $(MODAL_CONFIG.fieldIds.cpf).on('blur', function() {
    const cpf = $(this).val();
    clearFieldStatus($(this));
    
    if (!cpf) return;
    
    const cpfDigits = onlyDigits(cpf);
    
    // Validar formato básico
    if (cpfDigits.length !== 11) {
      showFieldWarning($(this), 'CPF deve ter 11 dígitos');
      return;
    }
    
    // Validar algoritmo (evitar números repetidos)
    if (/^(\d)\1+$/.test(cpfDigits)) {
      showFieldWarning($(this), 'CPF inválido');
      return;
    }
    
    // Validar dígitos verificadores
    let soma = 0;
    for (let i = 0; i < 9; i++) {
      soma += parseInt(cpfDigits[i]) * (10 - i);
    }
    let resto = soma % 11;
    let digito1 = resto < 2 ? 0 : 11 - resto;
    
    if (parseInt(cpfDigits[9]) !== digito1) {
      showFieldWarning($(this), 'CPF inválido');
      return;
    }
    
    soma = 0;
    for (let i = 0; i < 10; i++) {
      soma += parseInt(cpfDigits[i]) * (11 - i);
    }
    resto = soma % 11;
    let digito2 = resto < 2 ? 0 : 11 - resto;
    
    if (parseInt(cpfDigits[10]) !== digito2) {
      showFieldWarning($(this), 'CPF inválido');
      return;
    }
    
    showFieldSuccess($(this));
  });
  
  // CEP → valida e busca endereço
  $(MODAL_CONFIG.fieldIds.cep).on('blur', function() {
    const cep = $(this).val();
    clearFieldStatus($(this));
    
    if (!cep) return;
    
    const cepDigits = onlyDigits(cep);
    
    if (cepDigits.length !== 8) {
      showFieldWarning($(this), 'CEP deve ter 8 dígitos');
      return;
    }
    
    // Buscar endereço via ViaCEP
    showLoading('Buscando endereço...');
    
    $.getJSON(`https://viacep.com.br/ws/${cepDigits}/json/`)
      .done(function(data) {
        if (!data.erro && data.logradouro) {
          const endereco = `${data.logradouro}, ${data.bairro} - ${data.localidade}/${data.uf}`;
          $(MODAL_CONFIG.fieldIds.endereco).val(endereco);
          $('#endereco-container').slideDown(200);
          showFieldSuccess($('#CEP-MODAL'));
        } else {
          showFieldWarning($('#CEP-MODAL'), 'CEP não encontrado');
        }
      })
      .fail(function() {
        showFieldWarning($('#CEP-MODAL'), 'Erro ao buscar CEP');
      })
      .always(function() {
        hideLoading();
      });
  });
  
  // PLACA → valida formato antigo e Mercosul
  $(MODAL_CONFIG.fieldIds.placa).on('blur', function() {
    const placa = $(this).val().toUpperCase();
    clearFieldStatus($(this));
    
    if (!placa) return;
    
    const placaLimpa = placa.replace(/\W/g, '');
    
    // Formato antigo: ABC1234 ou ABC-1234
    const formatoAntigo = /^[A-Z]{3}[0-9]{4}$/.test(placaLimpa);
    
    // Formato Mercosul: ABC1D23 ou ABC1D2
    const formatoMercosul = /^[A-Z]{3}[0-9][A-Z][0-9]{2}$/.test(placaLimpa);
    
    if (!formatoAntigo && !formatoMercosul) {
      showFieldWarning($(this), 'Placa deve ter formato ABC-1234 ou ABC1D23');
      return;
    }
    
    showFieldSuccess($(this));
  });
  
  // ==================== 7. FUNÇÕES HELPER ====================
  
  function clearFieldStatus($field) {
    $field.removeClass('field-error field-warning field-success');
    const $help = $field.siblings('.help-message');
    if ($help.length) {
      $help.hide();
    }
  }
  
  function showFieldWarning($field, message) {
    $field.removeClass('field-success field-error').addClass('field-warning');
    const $help = $field.siblings('.help-message');
    if ($help.length) {
      $help.text(message).show();
    }
  }
  
  function showFieldSuccess($field) {
    $field.removeClass('field-error field-warning').addClass('field-success');
    const $help = $field.siblings('.help-message');
    if ($help.length) {
      $help.hide();
    }
  }
  
  // ==================== 8. EVENTOS DE ABERTURA/FECHAMENTO ====================
  
  $(document).on('click', MODAL_CONFIG.selectors.trigger, function(e) {
    e.preventDefault();
    e.stopPropagation();
    console.log('🎯 [MODAL] Abrindo modal WhatsApp');
    $modal.fadeIn(300);
    
    // Debug após abrir modal
    setTimeout(function() {
      const $content = $('.whatsapp-modal-content');
      console.log('🔍 [DEBUG AO ABRIR] Elementos encontrados:', $content.length);
      if ($content.length) {
        const computed = window.getComputedStyle($content[0]);
        console.log('📊 [DEBUG AO ABRIR] Position:', computed.position);
        console.log('📊 [DEBUG AO ABRIR] Right:', computed.right);
        console.log('📊 [DEBUG AO ABRIR] Bottom:', computed.bottom);
        console.log('📊 [DEBUG AO ABRIR] Width:', computed.width);
      }
    }, 350);
  });
  
  $closeBtn.on('click', function() {
    console.log('🎯 [MODAL] Fechando modal (X)');
    $modal.fadeOut(300);
  });
  
  $overlay.on('click', function() {
    console.log('🎯 [MODAL] Fechando modal (overlay)');
    $modal.fadeOut(300);
  });
  
  $(document).on('keydown', function(e) {
    if (e.key === 'Escape' && $modal.is(':visible')) {
      console.log('🎯 [MODAL] Fechando modal (ESC)');
      $modal.fadeOut(300);
    }
  });
  
  // ==================== 9. SUBMIT ====================
  
  $form.on('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    console.log('🎯 [MODAL] Submit do formulário');
    
    // Validar DDD + Celular
    const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
    const celular = $(MODAL_CONFIG.fieldIds.celular).val();
    
    if (!ddd || onlyDigits(ddd).length !== 2) {
      alert('Por favor, preencha o DDD corretamente.');
      $(MODAL_CONFIG.fieldIds.ddd).focus();
      return;
    }
    
    if (!celular || onlyDigits(celular).length !== 9) {
      alert('Por favor, preencha o celular corretamente.');
      $(MODAL_CONFIG.fieldIds.celular).focus();
      return;
    }
    
    // Coletar todos os dados
    const dados = coletarTodosDados();
    console.log('📋 [MODAL] Dados coletados:', dados);
    
    // Fechar modal e abrir WhatsApp
    console.log('✅ [MODAL] Fechando modal e abrindo WhatsApp');
    $modal.fadeOut(300, function() {
      openWhatsApp(dados);
    });
  });
  
  console.log('✅ [MODAL] Sistema de modal WhatsApp Definitivo inicializado');
  
});




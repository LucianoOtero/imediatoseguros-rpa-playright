// ======================
// MODAL WHATSAPP PROGRESSIVO HÍBRIDO V1.2
// Conceito: "Começar Simples, Expandir Conforme Necessidade"
// Baseado em: ESPECIFICACAO_TECNICA_MODAL_PROGRESSIVO_v1.1.md + ANALISE_DESENVOLVEDOR_MODAL_PROGRESSIVO.md
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
      telefone: '#telefone-modal',
      placa: '#placa-modal',
      cpf: '#cpf-modal',
      nome: '#nome-modal',
      cep: '#cep-modal',
      endereco: '#endereco-modal'
    },
    whatsapp: {
      phone: '551132301422',
      message: 'Olá! Quero uma cotação de seguro.'
    }
  };
  
  // Estados do modal
  const ModalStates = {
    SIMPLES: 'simples',      // DIV 1 apenas
    EXPANDIDO: 'expandido',   // DIV 1 + DIV 2
    COMPLETO: 'completo'      // DIV 1 + DIV 2 + DIV 3
  };
  
  let estadoAtual = ModalStates.SIMPLES;
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
   * Aplica debounce em função
   */
  function debounce(func, delay, context = null) {
    return function(...args) {
      const self = context || this;
      clearTimeout(timers[func.name]);
      timers[func.name] = setTimeout(() => func.apply(self, args), delay);
    };
  }
  
  /**
   * Extrai apenas dígitos de uma string
   */
  function onlyDigits(str) {
    return (str || '').replace(/\D+/g, '');
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
   * Constrói mensagem para WhatsApp com dados coletados
   */
  function buildWhatsAppMessage(dados) {
    let mensagem = MODAL_CONFIG.whatsapp.message;
    
    // Adicionar dados coletados
    if (dados.PLACA) {
      mensagem += `%0APlaca: ${dados.PLACA}`;
    }
    
    if (dados.CPF) {
      mensagem += `%0ACPF: ${dados.CPF}`;
    }
    
    if (dados.NOME) {
      mensagem += `%0ANome: ${dados.NOME}`;
    }
    
    if (dados.CEP) {
      mensagem += `%0ACEP: ${dados.CEP}`;
    }
    
    if (dados.ENDERECO) {
      mensagem += `%0AEndereço: ${dados.ENDERECO}`;
    }
    
    // Adicionar GCLID
    const gclid = getGCLID();
    if (gclid) {
      mensagem += `%0ACódigo: ${gclid}`;
    }
    
    return mensagem;
  }
  
  /**
   * Abre WhatsApp com mensagem construída
   */
  function openWhatsApp(dados) {
    const mensagem = buildWhatsAppMessage(dados);
    const url = `https://api.whatsapp.com/send?phone=${MODAL_CONFIG.whatsapp.phone}&text=${mensagem}`;
    
    console.log('🚀 [MODAL] Abrindo WhatsApp:', url);
    window.open(url, '_blank');
  }
  
  /**
   * Coleta todos os dados do formulário
   */
  function coletarTodosDados() {
    return {
      TELEFONE: $(MODAL_CONFIG.fieldIds.telefone).val(),
      PLACA: $(MODAL_CONFIG.fieldIds.placa).val(),
      CPF: $(MODAL_CONFIG.fieldIds.cpf).val() || '',
      NOME: $(MODAL_CONFIG.fieldIds.nome).val() || '',
      CEP: $(MODAL_CONFIG.fieldIds.cep).val() || '',
      ENDERECO: $(MODAL_CONFIG.fieldIds.endereco).val() || ''
    };
  }
  
  // ==================== 1. CRIAR HTML DO MODAL ====================
  
  const modalHTML = `
    <!-- Modal Container -->
    <div id="whatsapp-modal" style="display: none; position: fixed; z-index: 99999; left: 0; top: 0; width: 100%; height: 100%; overflow: auto;">
      
      <!-- Overlay -->
      <div class="whatsapp-modal-overlay" style="position: fixed; z-index: 99998; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0, 51, 102, 0.35);"></div>
      
      <!-- Conteúdo do Modal -->
      <div class="whatsapp-modal-content" style="position: relative; z-index: 99999; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); margin: 50px auto; padding: 0; border-radius: 20px; box-shadow: 0 30px 60px rgba(0, 51, 102, 0.15); width: 90%; max-width: 600px; max-height: 90vh; overflow-y: auto; font-family: 'Titillium Web', sans-serif;">
        
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
            Deixe seu telefone e placa que entramos em contato!
          </p>
        </div>
        
        <!-- Formulário -->
        <form id="whatsapp-form-modal" style="padding: 30px; background: #FFFFFF;">
          
          <!-- DIV 1: SEMPRE VISÍVEL -->
          <div id="div-etapa-1" class="modal-div">
            
            <!-- Telefone -->
            <div class="field-group" style="margin-bottom: 25px;">
              <label for="telefone-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Telefone *</label>
              <input 
                type="tel" 
                id="telefone-modal" 
                name="TELEFONE" 
                placeholder="(11) 99999-9999"
                autocomplete="tel"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
              />
              <small class="help-message" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;"></small>
            </div>
            
            <!-- Placa -->
            <div class="field-group" style="margin-bottom: 25px;">
              <label for="placa-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Placa do Veículo *</label>
              <input 
                type="text" 
                id="placa-modal" 
                name="PLACA" 
                placeholder="ABC-1234"
                maxlength="8"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333; text-transform: uppercase;" 
              />
              <small class="help-message" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;"></small>
            </div>
   <!-- Botão Principal -->
            <button 
              type="submit" 
              class="whatsapp-submit-btn"
              style="width: 100%; padding: 16px 24px; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: #FFFFFF; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; font-family: 'Titillium Web', sans-serif; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3); display: flex; align-items: center; justify-content: center; gap: 10px;">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="background: white; border-radius: 50%; padding: 4px;">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" fill="#128C7E"/>
              </svg>
              IR PARA O WHATSAPP
            </button>
            
            <!-- Botão Expandir (opcional) -->
            <button 
              type="button" 
              id="btn-expandir" 
              class="btn-link"
              style="width: 100%; background: none; border: none; color: #0099CC; font-size: 14px; font-weight: 600; cursor: pointer; text-decoration: underline; margin: 15px 0 0; padding: 10px;">
              + Preencher mais dados (opcional)
            </button>
            
          </div>
          
          <!-- DIV 2: OPÇÃO EXPANDIDA (hidden por padrão) -->
          <div id="div-etapa-2" class="modal-div" style="display: none; margin-top: 20px; padding-top: 20px; border-top: 2px solid #f0f0f0;">
            
            <!-- CPF -->
            <div class="field-group" style="margin-bottom: 25px;">
              <label for="cpf-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">
                CPF <small style="font-weight: 400; color: #666;">(opcional)</small>
              </label>
              <input 
                type="text" 
                id="cpf-modal" 
                name="CPF" 
                placeholder="000.000.000-00"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
              />
              <small class="help-message" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;"></small>
            </div>
            
            <!-- Nome -->
            <div class="field-group" style="margin-bottom: 25px;">
              <label for="nome-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Nome Completo</label>
              <input 
                type="text" 
                id="nome-modal" 
                name="NOME" 
                placeholder="João da Silva"
                style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
              />
            </div>
            
            <!-- Mensagem Info -->
            <div class="info-box" style="padding: 15px; background: #f8f9fa; border-left: 4px solid #0099CC; margin: 20px 0; font-size: 14px; color: #666;">
              ℹ️ Dados adicionais ajudam a personalizar sua cotação.
            </div>
            
            <!-- Botão para adicionar CEP (dentro da DIV 2) -->
            <button 
              type="button" 
              id="btn-adicionar-cep" 
              class="btn-link"
              style="width: 100%; background: none; border: none; color: #0099CC; font-size: 14px; font-weight: 600; cursor: pointer; text-decoration: underline; margin: 10px 0; padding: 10px;">
              + Adicionar CEP (opcional)
            </button>
            
            <!-- DIV 3: CEP E ENDEREÇO (dentro da DIV 2) -->
            <div id="div-etapa-3" class="modal-div" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #f0f0f0;">
              
              <!-- CEP -->
              <div class="field-group" style="margin-bottom: 25px;">
                <label for="cep-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">
                  CEP <small style="font-weight: 400; color: #666;">(opcional)</small>
                </label>
                <input 
                  type="text" 
                  id="cep-modal" 
                  name="CEP" 
                  placeholder="01234-567"
                  style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
                />
                <small class="help-message" style="display: none; color: #e74c3c; font-size: 12px; margin-top: 4px;"></small>
              </div>
              
              <!-- Endereço -->
              <div class="field-group" style="margin-bottom: 25px;">
                <label for="endereco-modal" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Endereço Completo</label>
                <input 
                  type="text" 
                  id="endereco-modal" 
                  name="ENDERECO" 
                  placeholder="Será preenchido automaticamente"
                  readonly
                  style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333; background: #f8f9fa;" 
                />
              </div>
              
              <!-- Botão Remover CEP -->
              <button 
                type="button" 
                id="btn-remover-cep" 
                class="btn-link-danger"
                style="width: 100%; background: none; border: none; color: #e74c3c; font-size: 12px; font-weight: 600; cursor: pointer; text-decoration: underline; margin: 5px 0; padding: 5px;">
                Remover CEP
              </button>
              
            </div>
            
            <!-- Botão Colapsar -->
            <button 
              type="button" 
              id="btn-colapsar" 
              class="btn-link"
              style="width: 100%; background: none; border: none; color: #0099CC; font-size: 14px; font-weight: 600; cursor: pointer; text-decoration: underline; margin: 15px 0 0; padding: 10px;">
              ↓ Ocultar campos extras
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
    /* Feedback visual de validação */
    #whatsapp-modal input[type="text"].field-error,
    #whatsapp-modal input[type="tel"].field-error {
      border-color: #e74c3c !important;
      background-color: #fff5f5 !important;
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
    
    .btn-link:hover {
      color: #003366 !important;
    }
    
    .btn-link-danger:hover {
      color: #c0392b !important;
    }
    
    #whatsapp-modal .whatsapp-submit-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4) !important;
    }
    
    .whatsapp-modal-close:hover {
      background: rgba(255, 255, 255, 0.2) !important;
      transform: scale(1.1);
    }
    
    /* Animação de expansão */
    @keyframes slideDown {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    #div-etapa-2 {
      animation: slideDown 0.3s ease;
    }
    
    #div-etapa-3 {
      animation: slideDown 0.2s ease;
    }
    
    @media (max-width: 767px) {
      #whatsapp-modal .whatsapp-modal-content {
        width: 95% !important;
        margin: 20px auto !important;
      }
    }
  `).appendTo('head');
  
  // ==================== 3. REFERÊNCIAS ====================
  
  const $modal = $(MODAL_CONFIG.selectors.modal);
  const $overlay = $(MODAL_CONFIG.selectors.overlay);
  const $closeBtn = $(MODAL_CONFIG.selectors.closeBtn);
  const $form = $(MODAL_CONFIG.selectors.form);
  
  // Referências aos botões de controle
  const $btnExpandir = $('#btn-expandir');
  const $btnColapsar = $('#btn-colapsar');
  const $btnAdicionarCep = $('#btn-adicionar-cep');
  const $btnRemoverCep = $('#btn-remover-cep');
  
  // Referências aos DIVs
  const $divEtapa1 = $('#div-etapa-1');
  const $divEtapa2 = $('#div-etapa-2');
  const $divEtapa3 = $('#div-etapa-3');
  
  // ==================== 4. MÁSCARAS ====================
  
  $(MODAL_CONFIG.fieldIds.telefone).mask('(00) 00000-0000');
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
  
  $(MODAL_CONFIG.fieldIds.cpf).mask('000.000.000-00');
  $(MODAL_CONFIG.fieldIds.cep).mask('00000-000');
  
  // ==================== 5. LÓGICA DE EXPANSÃO ====================
  
  // Expandir DIV 2 (CPF + Nome)
  $btnExpandir.on('click', function() {
    console.log('🔍 [MODAL] Expandindo DIV 2');
    estadoAtual = ModalStates.EXPANDIDO;
    $divEtapa2.slideDown(300);
    $(this).hide();
    $btnColapsar.show();
  });
  
  // Colapsar DIV 2
  $btnColapsar.on('click', function() {
    console.log('🔍 [MODAL] Colapsando DIV 2');
    estadoAtual = ModalStates.SIMPLES;
    $divEtapa2.slideUp(300);
    $divEtapa3.slideUp(200); // Colapsar DIV 3 também
    $btnAdicionarCep.show();
    $btnRemoverCep.hide();
    $btnExpandir.show();
    $(this).hide();
  });
  
  // Expandir DIV 3 (CEP + Endereço)
  $btnAdicionarCep.on('click', function() {
    console.log('🔍 [MODAL] Expandindo DIV 3');
    estadoAtual = ModalStates.COMPLETO;
    $divEtapa3.slideDown(200);
    $(this).hide();
    $btnRemoverCep.show();
  });
  
  // Colapsar DIV 3
  $btnRemoverCep.on('click', function() {
    console.log('🔍 [MODAL] Colapsando DIV 3');
    estadoAtual = ModalStates.EXPANDIDO;
    $divEtapa3.slideUp(200);
    $(this).hide();
    $btnAdicionarCep.show();
    
    // Limpar campos CEP e Endereço
    $(MODAL_CONFIG.fieldIds.cep).val('');
    $(MODAL_CONFIG.fieldIds.endereco).val('');
  });
  
  // ==================== 6. VALIDAÇÕES OPCIONAIS ====================
  
  // CEP → Buscar endereço via ViaCEP (debounce de 500ms)
  $(MODAL_CONFIG.fieldIds.cep).on('blur.siWhatsAppModal', debounce(function() {
    const cep = $(this).val();
    if (!cep || cep.length < 9) return;
    
    const cepLimpo = onlyDigits(cep);
    if (cepLimpo.length !== 8) return;
    
    showLoading('Buscando endereço...');
    
    $.getJSON(`https://viacep.com.br/ws/${cepLimpo}/json/`)
      .done(function(data) {
        if (!data.erro && data.logradouro) {
          const endereco = `${data.logradouro}, ${data.bairro} - ${data.localidade}/${data.uf}`;
          $(MODAL_CONFIG.fieldIds.endereco).val(endereco);
          showFieldSuccess($(MODAL_CONFIG.fieldIds.cep));
        } else {
          showFieldError($(MODAL_CONFIG.fieldIds.cep), 'CEP não encontrado');
        }
      })
      .fail(function() {
        showFieldError($(MODAL_CONFIG.fieldIds.cep), 'Erro ao buscar CEP');
      })
      .always(function() {
        hideLoading();
      });
  }, 500));
  
  // ==================== 7. FUNÇÕES HELPER ====================
  
  function showFieldError($field, message) {
    $field.addClass('field-error');
    const $help = $field.siblings('.help-message');
    if ($help.length) {
      $help.text(message).show();
    }
  }
  
  function showFieldSuccess($field) {
    $field.removeClass('field-error').addClass('field-success');
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
  });
  
  $closeBtn.on('click', function() {
    console.log('🎯 [MODAL] Fechando modal (X)');
    $modal.fadeOut(300);
    resetarModal();
  });
  
  $overlay.on('click', function() {
    console.log('🎯 [MODAL] Fechando modal (overlay)');
    $modal.fadeOut(300);
    resetarModal();
  });
  
  $(document).on('keydown', function(e) {
    if (e.key === 'Escape' && $modal.is(':visible')) {
      console.log('🎯 [MODAL] Fechando modal (ESC)');
      $modal.fadeOut(300);
      resetarModal();
    }
  });
  
  function resetarModal() {
    // Resetar estado
    estadoAtual = ModalStates.SIMPLES;
    
    // Colapsar DIVs
    $divEtapa2.slideUp(0);
    $divEtapa3.slideUp(0);
    
    // Resetar botões
    $btnExpandir.show();
    $btnColapsar.hide();
    $btnAdicionarCep.show();
    $btnRemoverCep.hide();
    
    // Limpar campos opcionais
    $(MODAL_CONFIG.fieldIds.cpf).val('');
    $(MODAL_CONFIG.fieldIds.nome).val('');
    $(MODAL_CONFIG.fieldIds.cep).val('');
    $(MODAL_CONFIG.fieldIds.endereco).val('');
  }
  
  // ==================== 9. SUBMIT ====================
  
  $form.on('submit', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    console.log('🎯 [MODAL] Submit do formulário');
    
    // Validar campos essenciais
    const telefone = $(MODAL_CONFIG.fieldIds.telefone).val();
    const placa = $(MODAL_CONFIG.fieldIds.placa).val();
    
    if (!telefone || telefone.length < 14) {
      alert('Por favor, preencha um telefone válido.');
      $(MODAL_CONFIG.fieldIds.telefone).focus();
      return;
    }
    
    if (!placa || placa.length < 8) {
      alert('Por favor, preencha a placa do veículo.');
      $(MODAL_CONFIG.fieldIds.placa).focus();
      return;
    }
    
    // Coletar todos os dados
    const dados = coletarTodosDados();
    console.log('📋 [MODAL] Dados coletados:', dados);
    
    // Fechar modal e abrir WhatsApp
    console.log('✅ [MODAL] Fechando modal e abrindo WhatsApp');
    $modal.fadeOut(300, function() {
      openWhatsApp(dados);
      resetarModal();
    });
  });
  
  console.log('✅ [MODAL] Sistema de modal WhatsApp Progressivo Híbrido V1.2 inicializado');
  
});





















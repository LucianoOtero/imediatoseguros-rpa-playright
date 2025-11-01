/**
 * PROJETO: UNIFICAÇÃO DE ARQUIVOS FOOTER CODE
 * INÍCIO: 30/10/2025 19:55
 * ÚLTIMA ALTERAÇÃO: 01/11/2025 10:12
 * 
 * VERSÃO: 1.3 - Correção da captura de GCLID
 * 
 * Arquivo unificado contendo:
 * - FooterCodeSiteDefinitivoUtils.js (Parte 1)
 * - Footer Code Site Definitivo.js (Parte 2 - modificado)
 * - Inside Head Tag Pagina.js (Parte 3 - GCLID integrado)
 * 
 * ALTERAÇÕES NESTA VERSÃO:
 * - Adicionados logs de debug detalhados na captura imediata de GCLID
 * - Implementado fallback no DOMContentLoaded para re-tentar captura se cookie não existir
 * - Adicionado tratamento de erros com try-catch na captura imediata
 * - Adicionado log de verificação do cookie após salvamento
 * - Melhorados logs no preenchimento de campos GCLID_FLD (mostra quantidade encontrada e índice)
 * - Logs adicionais para diagnóstico: URL, window.location.search, valores capturados, gclsrc
 * - Garantido que código execute corretamente mesmo se captura imediata falhar
 * 
 * ALTERAÇÕES VERSÃO 1.2:
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

// ======================
// TRATAMENTO DE ERRO GLOBAL (Recomendação do Engenheiro)
// ======================
(function() {
  'use strict';
  
  try {
    
    // ======================
    // PARTE 1: FOOTER CODE UTILS (sem modificações)
    // ======================
// ====================== 
// 🛠️ FOOTER CODE UTILS - Funções Utilitárias
// Versão: 2.0 | Data: 2025-10-30
// Atualizado: Adicionadas funções de validação de API e loading
(function() {
  'use strict';
  
  console.log('🔄 [UTILS] Carregando Footer Code Utils...');
  
  // ========= MANIPULAÇÃO DE DADOS =========
  
  /**
   * Extrai apenas dígitos de uma string
   * @param {string} s - String a processar
   * @returns {string} String contendo apenas dígitos
   */
  function onlyDigits(s) {
    return (s || '').replace(/\D+/g, '');
  }
  
  /**
   * Converte para maiúsculas e remove espaços
   * @param {string} s - String a processar
   * @returns {string} String em maiúsculas sem espaços
   */
  function toUpperNospace(s) {
    return (s || '').toUpperCase().trim();
  }
  
  /**
   * Define valor em campo do formulário
   * @param {string} id - ID ou nome do campo
   * @param {string} val - Valor a definir
   */
  function setFieldValue(id, val) {
    var $f = $('#' + id + ', [name="' + id + '"]');
    if ($f.length) {
      $f.val(val).trigger('input').trigger('change');
    }
  }
  
  /**
   * Lê valor de cookie pelo nome
   * @param {string} name - Nome do cookie
   * @returns {string|null} Valor do cookie ou null
   */
  function readCookie(name) {
    var n = name + "=", cookie = document.cookie.split(';');
    for (var i = 0; i < cookie.length; i++) {
      var c = cookie[i].trim();
      if (c.indexOf(n) === 0) return c.substring(n.length);
    }
    return null;
  }
  
  /**
   * Gera ID único de sessão
   * @returns {string} ID de sessão
   */
  function generateSessionId() {
    if (!window.sessionId) {
      window.sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    return window.sessionId;
  }
  
  /**
   * Submete formulário de forma nativa
   * @param {jQuery} $form - Objeto jQuery do formulário
   */
  function nativeSubmit($form) {
    var f = $form.get(0);
    if (!f) return;
    (typeof f.requestSubmit === 'function') ? f.requestSubmit() : f.submit();
  }
  
  // ========= VALIDAÇÃO LOCAL =========
  
  /**
   * Valida formato de email via regex
   * @param {string} v - Email a validar
   * @returns {boolean} true se válido
   */
  function validarEmailLocal(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i.test((v || '').trim());
  }
  
  /**
   * Valida formato básico do CPF
   * @param {string} cpf - CPF a validar
   * @returns {boolean} true se formato válido
   */
  function validarCPFFormato(cpf) {
    const cpfLimpo = onlyDigits(cpf);
    return cpfLimpo.length === 11 && !/^(\d)\1{10}$/.test(cpfLimpo);
  }
  
  /**
   * Valida CPF usando algoritmo de dígitos verificadores
   * @param {string} cpf - CPF a validar
   * @returns {boolean} true se válido
   */
  function validarCPFAlgoritmo(cpf) {
    cpf = onlyDigits(cpf);
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
    
    let soma = 0, resto = 0;
    for (let i = 1; i <= 9; i++) {
      soma += parseInt(cpf[i-1], 10) * (11 - i);
    }
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf[9], 10)) return false;
    
    soma = 0;
    for (let i = 1; i <= 10; i++) {
      soma += parseInt(cpf[i-1], 10) * (12 - i);
    }
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    return resto === parseInt(cpf[10], 10);
  }
  
  /**
   * Valida formato de placa (antigo ou Mercosul)
   * @param {string} p - Placa a validar
   * @returns {boolean} true se formato válido
   */
  function validarPlacaFormato(p) {
    const placaLimpa = p.toUpperCase().replace(/[^A-Z0-9]/g, '');
    const antigo = /^[A-Z]{3}[0-9]{4}$/;
    const mercosul = /^[A-Z]{3}[0-9][A-Z][0-9]{2}$/;
    return antigo.test(placaLimpa) || mercosul.test(placaLimpa);
  }
  
  /**
   * Valida formato local de celular (DDD + número)
   * @param {string} ddd - DDD
   * @param {string} numero - Número do celular
   * @returns {Object} {ok: boolean, reason?: string, national?: string}
   */
  function validarCelularLocal(ddd, numero) {
    const d = onlyDigits(ddd), n = onlyDigits(numero);
    if (d.length !== 2) return {ok: false, reason: 'ddd'};
    if (n.length !== 9) return {ok: false, reason: 'len'};
    if (n[0] !== '9') return {ok: false, reason: 'pattern'};
    return {ok: true, national: d + n};
  }
  
  /**
   * Aplica máscara jQuery Mask em campo de placa
   * @param {jQuery} $i - Objeto jQuery do campo
   */
  function aplicarMascaraPlaca($i) {
    const t = {'S': {pattern: /[A-Za-z]/}, '0': {pattern: /\d/}, 'A': {pattern: /[A-Za-z0-9]/}};
    $i.on('input', function() {
      this.value = this.value.toUpperCase();
    });
    $i.mask('SSS-0A00', {translation: t, clearIfNotMatch: false});
  }
  
  // ========= CRIPTOGRAFIA =========
  
  /**
   * Gera hash SHA-1 de texto
   * @param {string} text - Texto a processar
   * @returns {Promise<string>} Hash SHA-1 em hexadecimal
   */
  async function sha1(text) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest("SHA-1", data);
    return [...new Uint8Array(hashBuffer)]
      .map(byte => byte.toString(16).padStart(2, "0"))
      .join("");
  }
  
  /**
   * Gera assinatura HMAC SHA-256
   * @param {string} value - Valor a assinar
   * @param {string} key - Chave secreta
   * @returns {Promise<string>} Assinatura HMAC em hexadecimal
   */
  async function hmacSHA256(value, key) {
    const encoder = new TextEncoder();
    const keyData = encoder.encode(key);
    const valueData = encoder.encode(value);

    const cryptoKey = await crypto.subtle.importKey(
      "raw", keyData, { name: "HMAC", hash: { name: "SHA-256" } }, false, ["sign"]
    );
    const signature = await crypto.subtle.sign("HMAC", cryptoKey, valueData);
    return [...new Uint8Array(signature)]
      .map(byte => byte.toString(16).padStart(2, "0"))
      .join("");
  }
  
  // ========= EXTRAÇÃO/TRANSFORMAÇÃO DE DADOS =========
  
  /**
   * Extrai e formata dados do CPF da API PH3A
   * @param {Object} apiJson - Resposta JSON da API PH3A
   * @returns {Object} {sexo, dataNascimento, estadoCivil}
   */
  function extractDataFromPH3A(apiJson) {
    const data = apiJson && apiJson.data;
    if (!data || typeof data !== 'object') {
      return {
        sexo: '',
        dataNascimento: '',
        estadoCivil: ''
      };
    }
    
    // Mapear sexo
    let sexo = '';
    if (data.sexo !== undefined) {
      switch (data.sexo) {
        case 1: sexo = 'Masculino'; break;
        case 2: sexo = 'Feminino'; break;
        default: sexo = ''; break;
      }
    }
    
    // Mapear estado civil
    let estadoCivil = '';
    if (data.estado_civil !== undefined) {
      switch (data.estado_civil) {
        case 0: estadoCivil = 'Solteiro'; break;
        case 1: estadoCivil = 'Casado'; break;
        case 2: estadoCivil = 'Divorciado'; break;
        case 3: estadoCivil = 'Viúvo'; break;
        default: estadoCivil = ''; break;
      }
    }
    
    // Formatar data de nascimento (de ISO para DD/MM/YYYY)
    let dataNascimento = '';
    if (data.data_nascimento) {
      try {
        const date = new Date(data.data_nascimento);
        if (!isNaN(date.getTime())) {
          const day = String(date.getDate()).padStart(2, '0');
          const month = String(date.getMonth() + 1).padStart(2, '0');
          const year = date.getFullYear();
          dataNascimento = `${day}/${month}/${year}`;
        }
      } catch (e) {
        dataNascimento = data.data_nascimento;
      }
    }
    
    return {
      sexo: sexo,
      dataNascimento: dataNascimento,
      estadoCivil: estadoCivil
    };
  }
  
  /**
   * Preenche campos de endereço com dados do ViaCEP
   * @param {Object} data - Dados do ViaCEP
   */
  function preencherEnderecoViaCEP(data) {
    setFieldValue('CIDADE', data.localidade || '');
    setFieldValue('ESTADO', data.uf || '');
  }
  
  /**
   * Extrai dados do veículo da API Placa Fipe
   * @param {Object} apiJson - Resposta JSON da API Placa Fipe
   * @returns {Object} {marcaTxt, anoModelo, tipoVeiculo}
   */
  function extractVehicleFromPlacaFipe(apiJson) {
    const r = apiJson && (apiJson.informacoes_veiculo || apiJson);
    if (!r || typeof r !== 'object') return {marcaTxt: '', anoModelo: '', tipoVeiculo: ''};
    
    // Extrair dados da API Placa Fipe
    const fabricante = r.marca || '';
    const modelo = r.modelo || '';
    const anoMod = r.ano || r.ano_modelo || '';
    
    // Determinar tipo de veículo baseado no segmento
    let tipoVeiculo = '';
    if (r.segmento) {
      const segmento = r.segmento.toLowerCase();
      if (segmento.includes('moto')) {
        tipoVeiculo = 'moto';
      } else if (segmento.includes('auto')) {
        tipoVeiculo = 'carro';
      } else {
        // Fallback baseado em marcas conhecidas
        const modeloLower = modelo.toLowerCase();
        const marcaLower = fabricante.toLowerCase();
        
        if (marcaLower.includes('honda') || marcaLower.includes('yamaha') || 
            marcaLower.includes('suzuki') || marcaLower.includes('kawasaki') ||
            modeloLower.includes('cg') || modeloLower.includes('cb') || 
            modeloLower.includes('fazer') || modeloLower.includes('ninja')) {
          tipoVeiculo = 'moto';
        } else {
          tipoVeiculo = 'carro';
        }
      }
    } else {
      // Fallback baseado em marcas conhecidas
      const modeloLower = modelo.toLowerCase();
      const marcaLower = fabricante.toLowerCase();
      
      if (marcaLower.includes('honda') || marcaLower.includes('yamaha') || 
          marcaLower.includes('suzuki') || marcaLower.includes('kawasaki') ||
          modeloLower.includes('cg') || modeloLower.includes('cb') || 
          modeloLower.includes('fazer') || modeloLower.includes('ninja')) {
        tipoVeiculo = 'moto';
      } else {
        tipoVeiculo = 'carro';
      }
    }
    
    return { 
      marcaTxt: [fabricante, modelo].filter(Boolean).join(' / '), 
      anoModelo: onlyDigits(String(anoMod)).slice(0, 4),
      tipoVeiculo: tipoVeiculo
    };
  }
  
  // ========= VALIDAÇÃO API =========
  
  /**
   * Valida CPF via API PH3A
   * @param {string} cpf - CPF a validar
   * @returns {Promise<Object>} {ok: boolean, reason?: string, parsed?: Object}
   */
  function validarCPFApi(cpf) {
    if (typeof window.onlyDigits !== 'function' || typeof window.validarCPFFormato !== 'function' || typeof window.validarCPFAlgoritmo !== 'function') {
      console.error('❌ [UTILS] Funções de CPF não disponíveis');
      return Promise.resolve({ok: false, reason: 'erro_utils'});
    }
    
    const cpfLimpo = window.onlyDigits(cpf);
    
    // Primeiro validar formato e algoritmo
    if (!window.validarCPFFormato(cpfLimpo) || !window.validarCPFAlgoritmo(cpfLimpo)) {
      return Promise.resolve({
        ok: false, 
        reason: 'formato'
      });
    }
    
    // Verificar se VALIDAR_PH3A está habilitado
    if (typeof window.VALIDAR_PH3A === 'undefined') {
      console.warn('⚠️ [UTILS] VALIDAR_PH3A não disponível, assumindo false');
    }
    
    // Se não deve validar via API, retornar apenas validação local
    if (window.VALIDAR_PH3A === false || typeof window.VALIDAR_PH3A === 'undefined') {
      return Promise.resolve({
        ok: true,
        reason: 'ok'
      });
    }
    
    // Consultar API PH3A via proxy
    return fetch('https://mdmidia.com.br/cpf-validate.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cpf: cpfLimpo
      })
    })
    .then(r => r.json())
    .then(j => {
      const ok = !!j && (j.codigo === 1 || j.success === true);
      return {
        ok, 
        reason: ok ? 'ok' : 'nao_encontrado', 
        parsed: ok && typeof window.extractDataFromPH3A === 'function' ? window.extractDataFromPH3A(j) : {
          sexo: '',
          dataNascimento: '',
          estadoCivil: ''
        }
      };
    })
    .catch(_ => ({
      ok: false, 
      reason: 'erro_api'
    }));
  }
  
  /**
   * Valida CEP via ViaCEP
   * @param {string} cep - CEP a validar
   * @returns {Promise<Object>} {ok: boolean, reason?: string, viacep?: Object}
   */
  function validarCepViaCep(cep) {
    if (typeof window.onlyDigits !== 'function') {
      console.error('❌ [UTILS] onlyDigits não disponível');
      return Promise.resolve({ok: false, reason: 'erro_utils'});
    }
    cep = window.onlyDigits(cep);
    if (cep.length !== 8) return Promise.resolve({ok: false, reason: 'formato'});
    return fetch('https://viacep.com.br/ws/' + cep + '/json/')
      .then(r => r.json())
      .then(d => ({ok: !d?.erro, reason: d?.erro ? 'nao_encontrado' : 'ok', viacep: d}))
      .catch(_ => ({ok: false, reason: 'erro_api'}));
  }
  
  /**
   * Valida placa via API Placa Fipe
   * @param {string} placa - Placa a validar
   * @returns {Promise<Object>} {ok: boolean, reason?: string, parsed?: Object}
   */
  function validarPlacaApi(placa) {
    if (typeof window.validarPlacaFormato !== 'function') {
      console.error('❌ [UTILS] validarPlacaFormato não disponível');
      return Promise.resolve({ok: false, reason: 'erro_utils'});
    }
    const raw = placa.toUpperCase().replace(/[^A-Z0-9]/g, '');
    if (!window.validarPlacaFormato(raw)) return Promise.resolve({ok: false, reason: 'formato'});
    
    return fetch('https://mdmidia.com.br/placa-validate.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        placa: raw
      })
    })
      .then(r => r.json())
      .then(j => {
        const ok = !!j && (j.codigo === 1 || j.success === true);
        return {
          ok, 
          reason: ok ? 'ok' : 'nao_encontrada', 
          parsed: ok && typeof window.extractVehicleFromPlacaFipe === 'function' ? window.extractVehicleFromPlacaFipe(j) : {marcaTxt: '', anoModelo: '', tipoVeiculo: ''}
        };
      })
      .catch(_ => ({ok: false, reason: 'erro_api'}));
  }
  
  /**
   * Valida celular via API Layer
   * @param {string} nat - Número nacional (DDD + número)
   * @returns {Promise<Object>} {ok: boolean}
   */
  function validarCelularApi(nat) {
    if (typeof window.APILAYER_KEY === 'undefined') {
      console.warn('⚠️ [UTILS] APILAYER_KEY não disponível, usando fallback');
      return Promise.resolve({ok: true}); // fallback - falha externa não bloqueia
    }
    return fetch('https://apilayer.net/api/validate?access_key=' + window.APILAYER_KEY + '&country_code=BR&number=' + nat)
      .then(r => r.json())
      .then(j => ({ok: !!j?.valid}))
      .catch(_ => ({ok: true})); // falha externa não bloqueia
  }
  
  /**
   * Valida telefone completo (DDD + Celular)
   * @param {jQuery} $DDD - Objeto jQuery do campo DDD
   * @param {jQuery} $CEL - Objeto jQuery do campo Celular
   * @returns {Promise<Object>} {ok: boolean, reason?: string}
   */
  function validarTelefoneAsync($DDD, $CEL) {
    if (typeof window.validarCelularLocal !== 'function') {
      console.error('❌ [UTILS] validarCelularLocal não disponível');
      return Promise.resolve({ok: false, reason: 'erro_utils'});
    }
    const local = window.validarCelularLocal($DDD.val(), $CEL.val());
    if (!local.ok) return Promise.resolve({ok: false, reason: local.reason});
    
    if (typeof window.USE_PHONE_API === 'undefined') {
      console.warn('⚠️ [UTILS] USE_PHONE_API não disponível, assumindo false');
      return Promise.resolve({ok: true});
    }
    
    if (!window.USE_PHONE_API) return Promise.resolve({ok: true});
    return validarCelularApi(local.national).then(api => ({ok: api.ok}));
  }
  
  /**
   * Valida email via SafetyMails
   * @param {string} email - Email a validar
   * @returns {Promise<Object|null>} Resposta da API ou null
   */
  async function validarEmailSafetyMails(email) {
    try {
      if (typeof window.sha1 !== 'function' || typeof window.hmacSHA256 !== 'function') {
        console.error('❌ [UTILS] sha1 ou hmacSHA256 não disponíveis');
        return null;
      }
      
      if (typeof window.SAFETY_TICKET === 'undefined' || typeof window.SAFETY_API_KEY === 'undefined') {
        console.warn('⚠️ [UTILS] SAFETY_TICKET ou SAFETY_API_KEY não disponíveis');
        return null;
      }
      
      const code = await window.sha1(window.SAFETY_TICKET);
      const url = `https://${window.SAFETY_TICKET}.safetymails.com/api/${code}`;
      const hmac = await window.hmacSHA256(email, window.SAFETY_API_KEY);

      let form = new FormData();
      form.append('email', email);

      const response = await fetch(url, {
        method: "POST",
        headers: { "Sf-Hmac": hmac },
        body: form
      });
      
      if (!response.ok) {
        console.error(`SafetyMails HTTP Error: ${response.status}`);
        return null;
      }
      
      const data = await response.json();
      return data.Success ? data : null;
    } catch (error) {
      console.error('SafetyMails request failed:', error);
      return null;
    }
  }
  
  // ========= LOADING UI =========
  
  /**
   * Inicializa overlay de loading
   */
  function initLoading() {
    // Verificar se já existe (evitar duplicação)
    if (document.getElementById('si-loading-overlay')) return;
    
    const style = document.createElement('style');
    style.textContent = `
    #si-loading-overlay{position:fixed;inset:0;background:rgba(0,0,0,.35);display:none;z-index:99998;align-items:center;justify-content:center}
    #si-loading-box{background:#fff;border-radius:12px;padding:18px 22px;box-shadow:0 10px 30px rgba(0,0,0,.2);display:flex;gap:12px;align-items:center;font-family:system-ui}
    .si-spinner{width:20px;height:20px;border:3px solid #e5e7eb;border-top-color:#111827;border-radius:50%;animation:si-spin .8s linear infinite}
    @keyframes si-spin{to{transform:rotate(360deg)}}
    `;
    document.head.appendChild(style);

    const overlay = document.createElement('div');
    overlay.id = 'si-loading-overlay';
    overlay.innerHTML = `<div id="si-loading-box"><div class="si-spinner"></div><div id="si-loading-text">Validando dados…</div></div>`;
    document.body.appendChild(overlay);
  }
  
  // Variável de controle de loading (escopo do IIFE)
  let __siLoadingCount = 0;
  
  /**
   * Mostra overlay de loading
   * @param {string} txt - Texto a exibir (opcional)
   */
  function showLoading(txt) {
    const o = document.getElementById('si-loading-overlay');
    const t = document.getElementById('si-loading-text');
    if (!o || !t) return;
    if (txt) t.textContent = txt;
    __siLoadingCount++;
    o.style.display = 'flex';
  }
  
  /**
   * Oculta overlay de loading
   */
  function hideLoading() {
    const o = document.getElementById('si-loading-overlay');
    if (!o) return;
    __siLoadingCount = Math.max(0, __siLoadingCount - 1);
    if (__siLoadingCount === 0) o.style.display = 'none';
  }
  
  // Inicializar loading ao carregar Utils.js
  initLoading();
  
  // ========= EXPOSIÇÃO GLOBAL =========
  
  // Expor funções globalmente para uso no Footer Code principal
  window.onlyDigits = onlyDigits;
  window.toUpperNospace = toUpperNospace;
  window.setFieldValue = setFieldValue;
  window.readCookie = readCookie;
  window.generateSessionId = generateSessionId;
  window.nativeSubmit = nativeSubmit;
  window.validarEmailLocal = validarEmailLocal;
  window.validarCPFFormato = validarCPFFormato;
  window.validarCPFAlgoritmo = validarCPFAlgoritmo;
  window.validarPlacaFormato = validarPlacaFormato;
  window.validarCelularLocal = validarCelularLocal;
  window.aplicarMascaraPlaca = aplicarMascaraPlaca;
  window.sha1 = sha1;
  window.hmacSHA256 = hmacSHA256;
  window.extractDataFromPH3A = extractDataFromPH3A;
  window.extractVehicleFromPlacaFipe = extractVehicleFromPlacaFipe;
  window.preencherEnderecoViaCEP = preencherEnderecoViaCEP;
  
  // ✅ NOVAS FUNÇÕES: Validação de API
  window.validarCPFApi = validarCPFApi;
  window.validarCepViaCep = validarCepViaCep;
  window.validarPlacaApi = validarPlacaApi;
  window.validarCelularApi = validarCelularApi;
  window.validarTelefoneAsync = validarTelefoneAsync;
  window.validarEmailSafetyMails = validarEmailSafetyMails;
  
  // ✅ NOVAS FUNÇÕES: Loading UI
  window.initLoading = initLoading;
  window.showLoading = showLoading;
  window.hideLoading = hideLoading;
  
  // Verificar se todas as funções foram expostas corretamente
  const requiredFunctions = [
    'onlyDigits', 'toUpperNospace', 'setFieldValue', 'readCookie',
    'generateSessionId', 'nativeSubmit', 'validarEmailLocal',
    'validarCPFFormato', 'validarCPFAlgoritmo', 'validarPlacaFormato',
    'validarCelularLocal', 'aplicarMascaraPlaca', 'sha1', 'hmacSHA256',
    'extractDataFromPH3A', 'extractVehicleFromPlacaFipe',
    'preencherEnderecoViaCEP', 'validarCPFApi', 'validarCepViaCep',
    'validarPlacaApi', 'validarCelularApi', 'validarTelefoneAsync',
    'validarEmailSafetyMails', 'initLoading', 'showLoading', 'hideLoading'
  ];
  
  const missing = requiredFunctions.filter(fn => typeof window[fn] !== 'function');
  if (missing.length > 0) {
    console.error('❌ [UTILS] Funções faltando:', missing);
  } else {
    console.log('✅ [UTILS] Footer Code Utils carregado - 26 funções disponíveis');
  }
  
  // ✅ Verificar se constantes estão disponíveis (recomendação do engenheiro)
  const requiredConstants = ['USE_PHONE_API', 'APILAYER_KEY', 'SAFETY_TICKET', 'SAFETY_API_KEY', 'VALIDAR_PH3A'];
  const missingConstants = requiredConstants.filter(c => typeof window[c] === 'undefined');
  if (missingConstants.length > 0) {
    console.warn('⚠️ [UTILS] Constantes faltando:', missingConstants);
  } else {
    console.log('✅ [UTILS] Todas as constantes disponíveis');
  }
})();
// ======================

    
    // ======================
    // FIM DA PARTE 1: FOOTER CODE UTILS
    // ======================
    
    // ======================
    // PARTE 2: FOOTER CODE PRINCIPAL (modificado)
    // ======================
    
    // Constantes globais (expor ANTES de qualquer uso - Recomendação do Engenheiro)
    // ⚠️ AMBIENTE: DEV (segurosimediato dev)
    window.USE_PHONE_API = true;
    window.APILAYER_KEY = 'dce92fa84152098a3b5b7b8db24debbc';
    window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138'; // DEV: segurosimediato dev
    window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f'; // Mesmo para DEV e PROD
    window.VALIDAR_PH3A = false;
    
    // ======================
    // CAPTURA E GERENCIAMENTO DE GCLID (Integrado do Inside Head Tag Pagina.js)
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
    console.log('🔍 [GCLID] Iniciando captura - URL:', window.location.href);
    console.log('🔍 [GCLID] window.location.search:', window.location.search);
    
    var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
    var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");
    var trackingId = gclid || gbraid;
    
    console.log('🔍 [GCLID] Valores capturados:', { gclid: gclid, gbraid: gbraid, trackingId: trackingId });
    
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
    
    // Função de verificação defensiva de dependências (Recomendação do Engenheiro)
    function waitForDependencies(callback, maxWait = 5000) {
      const startTime = Date.now();
      
      function check() {
        const hasJQuery = typeof jQuery !== 'undefined';
        const hasUtils = typeof window.onlyDigits === 'function';
        
        if (hasJQuery && hasUtils) {
          callback();
        } else if (Date.now() - startTime < maxWait) {
          setTimeout(check, 50);
        } else {
          console.error('[FOOTER COMPLETO] Timeout aguardando dependências:', {
            jQuery: hasJQuery,
            Utils: hasUtils
          });
          // Executar mesmo assim - pode haver fallbacks no código
          callback();
        }
      }
      
      check();
    }
    
    // Função de inicialização consolidada
    function init() {
      // 1. WhatsApp form submit especial
      document.addEventListener('DOMContentLoaded', function () {
        var form = document.getElementById('form-wp');
        if (!form) return;
        form.addEventListener('submit', function (e) {
          e.preventDefault();
          var whatsappUrl = "https://api.whatsapp.com/send?phone=551141718837&text=Ola.%20Quero%20fazer%20uma%20cotacao%20de%20seguro.";
          window.open(whatsappUrl, '_blank');
          form.submit();
        });
      });
      
      // 2. Configuração RPA Global
      window.rpaEnabled = false;
      console.log('🎯 [CONFIG] RPA habilitado:', window.rpaEnabled);
      
      // 2.1. Gerenciamento GCLID (DOMContentLoaded)
      document.addEventListener("DOMContentLoaded", function () {
        // Tentar capturar novamente se não foi capturado antes (FALLBACK)
        var cookieExistente = window.readCookie ? window.readCookie("gclid") : null;
        
        if (!cookieExistente) {
          console.log('🔍 [GCLID] Cookie não encontrado, tentando captura novamente no DOMContentLoaded...');
          var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
          var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");
          var trackingId = gclid || gbraid;
          
          if (trackingId) {
            var gclsrc = getParam("gclsrc");
            if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
              try {
                setCookie("gclid", trackingId, 90);
                console.log('✅ [GCLID] Capturado no DOMContentLoaded e salvo em cookie:', trackingId);
                cookieExistente = trackingId;
              } catch (error) {
                console.error('❌ [GCLID] Erro ao salvar cookie no DOMContentLoaded:', error);
              }
            }
          } else {
            console.warn('⚠️ [GCLID] Nenhum trackingId encontrado na URL no DOMContentLoaded');
          }
        } else {
          console.log('✅ [GCLID] Cookie já existe:', cookieExistente);
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
      
      // Função básica de logging para teste
      function logDebug(level, message, data = null) {
        const logData = {
          level: level,
          message: message,
          data: data,
          timestamp: new Date().toISOString(),
          sessionId: window.sessionId || (typeof window.generateSessionId === 'function' ? window.generateSessionId() : 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)),
          url: window.location.href,
          userAgent: navigator.userAgent
        };
        
        // Enviar para sistema PHP de logging com tratamento completo de resposta
        fetch('https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(logData),
          mode: 'cors',
          credentials: 'omit'
        })
        .then(response => {
          console.log(`[LOG DEBUG] Status: ${response.status} ${response.statusText}`);
          console.log(`[LOG DEBUG] Headers:`, Object.fromEntries(response.headers.entries()));
          
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
          
          return response.text();
        })
        .then(text => {
          console.log(`[LOG DEBUG] Resposta bruta:`, text);
          
          try {
            const result = JSON.parse(text);
            console.log(`[LOG DEBUG] Sucesso:`, result);
            
            if (result.success) {
              console.log(`[LOG DEBUG] Log enviado com sucesso! ID: ${result.logged?.log_id || 'N/A'}`);
            } else {
              console.error(`[LOG DEBUG] Erro no servidor:`, result.error);
            }
          } catch (parseError) {
            console.error(`[LOG DEBUG] Erro ao fazer parse da resposta:`, parseError);
            console.error(`[LOG DEBUG] Resposta que causou erro:`, text);
          }
        })
        .catch(error => {
          console.error(`[LOG DEBUG] Erro na requisição:`, error);
          console.error(`[LOG DEBUG] Tipo do erro:`, error.constructor.name);
          console.error(`[LOG DEBUG] Mensagem:`, error.message);
          
          // Log adicional para debugging
          if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
            console.error(`[LOG DEBUG] Possível problema de CORS ou rede`);
          }
        });
        
        // Manter console.log para desenvolvimento local
        console.log(`[${level}] ${message}`, data);
      }
      
      // Expor funções globalmente
      window.logDebug = logDebug;
      
      // Teste da funcionalidade de logging
      logDebug('INFO', '[CONFIG] RPA habilitado via PHP Log', {rpaEnabled: window.rpaEnabled});
      
      // 3. Função para carregar script RPA dinamicamente
      function loadRPAScript() {
        return new Promise((resolve, reject) => {
          // Verificar se já foi carregado
          if (window.MainPage && window.ProgressModalRPA) {
            console.log('🎯 Script RPA já carregado');
            resolve();
            return;
          }

          console.log('🎯 Carregando script RPA...');
          
          const script = document.createElement('script');
          script.src = 'https://mdmidia.com.br/webflow_injection_limpo.js';
          script.onload = () => {
            console.log('✅ Script RPA carregado com sucesso');
            resolve();
          };
          script.onerror = () => {
            console.error('❌ Erro ao carregar script RPA');
            reject(new Error('Falha ao carregar script RPA'));
          };
          document.head.appendChild(script);
        });
      }

      // Expor função globalmente
      window.loadRPAScript = loadRPAScript;
      
      // 4. WhatsApp links com GCLID
      var gclid = null;
      
      function initGCLID() {
        if (typeof window.readCookie === 'function') {
          gclid = window.readCookie('gclid');
        } else {
          // Fallback se Utils.js não carregou
          console.warn('⚠️ [FOOTER] readCookie não disponível, tentando novamente...');
          setTimeout(initGCLID, 100);
        }
      }
      
      // Tentar inicializar imediatamente ou aguardar carregamento do Utils
      if (typeof window.readCookie === 'function') {
        gclid = window.readCookie('gclid');
      } else {
        window.addEventListener('footerUtilsLoaded', initGCLID);
        setTimeout(initGCLID, 500); // Fallback após 500ms
      }

      // Função para carregar modal dinamicamente
      function loadWhatsAppModal() {
        if (window.whatsappModalLoaded) {
          console.log('✅ [MODAL] Modal já carregado');
          return;
        }
        
        console.log('🔄 [MODAL] Carregando modal de dev.bpsegurosimediato.com.br...');
        const script = document.createElement('script');
        script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
        script.onload = function() {
          window.whatsappModalLoaded = true;
          console.log('✅ [MODAL] Modal carregado com sucesso');
        };
        script.onerror = function() {
          console.error('❌ [MODAL] Erro ao carregar modal');
        };
        document.head.appendChild(script);
      }
      
      // Aguardar jQuery para inicializar validações
      $(function () {
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
        
        // 5. Validações unificadas: CPF, CEP, PLACA, CELULAR, E-MAIL
        // Campos
        const $CPF   = $('#CPF, [name="CPF"]');
        const $CEP   = $('#CEP, [name="CEP"]');
        const $PLACA = $('#PLACA, [name="PLACA"]');
        const $MARCA = $('#MARCA, [name="MARCA"]');
        const $ANO   = $('#ANO, [name="ANO"]');
        const $DDD   = $('#DDD-CELULAR, [name="DDD-CELULAR"]');
        const $CEL   = $('#CELULAR, [name="CELULAR"]');
        const $EMAIL = $('#email, [name="email"], #EMAIL, [name="EMAIL"]');

        // Máscaras
        if ($CPF.length)   $CPF.mask('000.000.000-00');
        if ($CEP.length)   $CEP.mask('00000-000');
        if ($PLACA.length && typeof window.aplicarMascaraPlaca === 'function') {
          window.aplicarMascaraPlaca($PLACA);
        }
        if ($DDD.length)   $DDD.off('.siPhone').mask('00', { clearIfNotMatch:false });
        if ($CEL.length)   $CEL.off('.siPhone').mask('00000-0000', { clearIfNotMatch:false });

        // ============ Helpers de Alert (SweetAlert2) ============
        function saWarnConfirmCancel(opts) {
          return Swal.fire(Object.assign({
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Corrigir',
            cancelButtonText: 'Não',
            reverseButtons: true,
            allowOutsideClick: false,
            allowEscapeKey: true
          }, opts));
        }
        function saInfoConfirmCancel(opts) {
          return Swal.fire(Object.assign({
            icon: 'info',
            showCancelButton: true,
            confirmButtonText: 'Prosseguir assim mesmo',
            cancelButtonText: 'Corrigir',
            reverseButtons: true,
            allowOutsideClick: false,
            allowEscapeKey: true
          }, opts));
        }

        // CPF → change (com/sem API PH3A)
        $CPF.on('change', function(){
          const cpfValue = $(this).val();
          
          // Validação local primeiro
          if (typeof window.validarCPFAlgoritmo !== 'function') {
            console.error('❌ [FOOTER] validarCPFAlgoritmo não disponível');
            return;
          }
          if (!window.validarCPFAlgoritmo(cpfValue)) {
            saWarnConfirmCancel({
              title: 'CPF inválido',
              html: 'Deseja corrigir?'
            }).then(r => { 
              if (r.isConfirmed) $CPF.focus(); 
            });
            return;
          }
          
          // Se flag VALIDAR_PH3A estiver desabilitada, apenas validar formato
          if (!window.VALIDAR_PH3A) {
            // CPF válido, mas sem consulta à API - limpar campos para preenchimento manual
            if (typeof window.setFieldValue === 'function') {
              window.setFieldValue('SEXO', '');
              window.setFieldValue('DATA-DE-NASCIMENTO', '');
              window.setFieldValue('ESTADO-CIVIL', '');
            }
            return;
          }
          
          // Se CPF válido e flag ativa, consultar API PH3A
          if (typeof window.showLoading === 'function') window.showLoading('Consultando dados do CPF…');
          if (typeof window.validarCPFApi === 'function') {
            window.validarCPFApi(cpfValue).then(res => {
              if (typeof window.hideLoading === 'function') window.hideLoading();
              
              if (res.ok && res.parsed && typeof window.setFieldValue === 'function') {
                // Preencher campos automaticamente
                if (res.parsed.sexo) window.setFieldValue('SEXO', res.parsed.sexo);
                if (res.parsed.dataNascimento) window.setFieldValue('DATA-DE-NASCIMENTO', res.parsed.dataNascimento);
                if (res.parsed.estadoCivil) window.setFieldValue('ESTADO-CIVIL', res.parsed.estadoCivil);
              } else if (res.reason === 'nao_encontrado') {
                // CPF válido mas não encontrado na base
                saInfoConfirmCancel({
                  title: 'CPF não encontrado',
                  html: 'O CPF é válido, mas não foi encontrado na nossa base de dados.<br><br>Deseja preencher os dados manualmente?'
                }).then(r => {
                  if (r.isConfirmed) {
                    // Limpar campos e permitir preenchimento manual
                    if (typeof window.setFieldValue === 'function') {
                      window.setFieldValue('SEXO', '');
                      window.setFieldValue('DATA-DE-NASCIMENTO', '');
                      window.setFieldValue('ESTADO-CIVIL', '');
                    }
                  }
                });
              }
            }).catch(_ => {
              if (typeof window.hideLoading === 'function') window.hideLoading();
              // Em caso de erro na API, não bloquear o usuário
              console.log('Erro na consulta da API PH3A');
            });
          }
        });

        // CEP → change (ViaCEP)
        $CEP.on('change', function(){
          const val = $(this).val();
          if (typeof window.showLoading === 'function') window.showLoading('Validando CEP…');
          if (typeof window.validarCepViaCep === 'function') {
            window.validarCepViaCep(val).then(res=>{
              if (typeof window.hideLoading === 'function') window.hideLoading();
              if (!res.ok){
                saWarnConfirmCancel({
                  title: 'CEP inválido',
                  html: 'Deseja corrigir?'
                }).then(r=>{ if (r.isConfirmed) $CEP.focus(); });
              } else if (res.viacep && typeof window.preencherEnderecoViaCEP === 'function'){
                window.preencherEnderecoViaCEP(res.viacep);
              }
            }).catch(_=>{
              if (typeof window.hideLoading === 'function') window.hideLoading();
            });
          }
        });

        // PLACA → change (preenche MARCA/ANO/TIPO se ok)
        $PLACA.on('change', function(){
          if (typeof window.showLoading === 'function') window.showLoading('Validando placa…');
          if (typeof window.validarPlacaApi === 'function') {
            window.validarPlacaApi($(this).val()).then(res=>{
              if (typeof window.hideLoading === 'function') window.hideLoading();
              if (!res.ok){
                saWarnConfirmCancel({
                  title: 'Placa inválida',
                  html: 'Deseja corrigir?'
                }).then(r=>{ if (r.isConfirmed) $PLACA.focus(); });
                if (typeof window.setFieldValue === 'function') {
                  window.setFieldValue('MARCA',''); 
                  window.setFieldValue('ANO',''); 
                  window.setFieldValue('TIPO-DE-VEICULO','');
                }
              } else {
                if (typeof window.setFieldValue === 'function' && res.parsed) {
                  if (res.parsed.marcaTxt) window.setFieldValue('MARCA', res.parsed.marcaTxt);
                  if (res.parsed.anoModelo) window.setFieldValue('ANO', res.parsed.anoModelo);
                  if (res.parsed.tipoVeiculo) window.setFieldValue('TIPO-DE-VEICULO', res.parsed.tipoVeiculo);
                }
              }
            }).catch(_=>{
              if (typeof window.hideLoading === 'function') window.hideLoading();
            });
          }
        });

        // CELULAR → valida SÓ no BLUR do CELULAR
        $DDD.off('change'); $CEL.off('change'); // remove handlers antigos
        
        // DDD → valida no BLUR do DDD
        $DDD.on('blur.siPhone', function(){
          if (typeof window.onlyDigits !== 'function') {
            console.error('❌ [FOOTER] onlyDigits não disponível');
            return;
          }
          const dddDigits = window.onlyDigits($DDD.val()).length;
          
          // Se DDD incompleto (não tem 2 dígitos)
          if (dddDigits > 0 && dddDigits < 2) {
            saWarnConfirmCancel({
              title: 'DDD incompleto',
              html: 'O DDD precisa ter 2 dígitos.<br><br>Deseja corrigir?'
            }).then(r=>{ if (r.isConfirmed) $DDD.focus(); });
            return;
          }
          
          // Se DDD inválido (mais de 2 dígitos)
          if (dddDigits > 2) {
            saWarnConfirmCancel({
              title: 'DDD inválido',
              html: 'O DDD deve ter exatamente 2 dígitos.<br><br>Deseja corrigir?'
            }).then(r=>{ if (r.isConfirmed) $DDD.focus(); });
            return;
          }
        });
        
        $CEL.on('blur.siPhone', function(){
          if (typeof window.onlyDigits !== 'function') {
            console.error('❌ [FOOTER] onlyDigits não disponível');
            return;
          }
          const dddDigits = window.onlyDigits($DDD.val()).length;
          const celDigits = window.onlyDigits($CEL.val()).length;

          // Validação DDD: deve ter exatamente 2 dígitos
          if (dddDigits !== 2) {
            saWarnConfirmCancel({
              title: 'DDD inválido',
              html: 'O DDD precisa ter 2 dígitos.<br><br>Deseja corrigir?'
            }).then(r=>{ if (r.isConfirmed) $DDD.focus(); });
            return;
          }

          // Validação Celular: deve ter exatamente 9 dígitos
          if (celDigits > 0 && celDigits < 9) {
            saWarnConfirmCancel({
              title: 'Celular incompleto',
              html: 'O celular precisa ter 9 dígitos.<br><br>Deseja corrigir?'
            }).then(r=>{ if (r.isConfirmed) $CEL.focus(); });
            return;
          }

          // Se DDD=2 e celular=9 → valida via API
          if (dddDigits === 2 && celDigits === 9){
            if (typeof window.showLoading === 'function') window.showLoading('Validando celular…');
            if (typeof window.validarTelefoneAsync === 'function') {
              window.validarTelefoneAsync($DDD,$CEL).then(res=>{
                if (typeof window.hideLoading === 'function') window.hideLoading();
                if (!res.ok){
                  const numero = `${($DDD.val()||'').trim()}-${($CEL.val()||'').trim()}`;
                  saWarnConfirmCancel({
                    title: 'Celular inválido',
                    html: `Parece que o celular informado<br><br><b>${numero}</b><br><br>não é válido.<br><br>Deseja corrigir?`
                  }).then(r=>{ if (r.isConfirmed) $CEL.focus(); });
                }
              }).catch(_=>{
                if (typeof window.hideLoading === 'function') window.hideLoading();
              });
            }
          }
          // Se DDD incompleto ou celular vazio → não valida agora (submit cuida)
        });

        // E-MAIL → change (regex bloqueia; SafetyMails só avisa)
        $EMAIL.on('change.siMail', function(){
          const v = ($(this).val()||'').trim();
          if (!v) return;
          if (typeof window.validarEmailLocal !== 'function') {
            console.error('❌ [FOOTER] validarEmailLocal não disponível');
            return;
          }
          if (!window.validarEmailLocal(v)){
            saWarnConfirmCancel({
              title: 'E-mail inválido',
              html: `O e-mail informado:<br><br><b>${v}</b><br><br>não parece válido.<br><br>Deseja corrigir?`,
              cancelButtonText: 'Não Corrigir',
              confirmButtonText: 'Corrigir'
            }).then(r=>{ if (r.isConfirmed) $EMAIL.focus(); });
            return;
          }
          // Aviso opcional via SafetyMails (não bloqueia)
          if (typeof window.validarEmailSafetyMails === 'function') {
            window.validarEmailSafetyMails(v).then(resp=>{
              if (resp && resp.StatusEmail && resp.StatusEmail !== 'VALIDO'){
                saWarnConfirmCancel({
                  title: 'Atenção',
                  html: `O e-mail informado:<br><br><b>${v}</b><br><br>pode não ser válido segundo verificador externo.<br><br>Deseja corrigir?`,
                  cancelButtonText: 'Manter',
                  confirmButtonText: 'Corrigir'
                }).then(r=>{ if (r.isConfirmed) $EMAIL.focus(); });
              }
            }).catch(()=>{ /* silêncio em erro externo */ });
          }
        });


        // CONTROLE MANUAL DO BOTÃO SUBMIT
        $('#submit_button_auto').on('click', function(e) {
          console.log('🎯 [DEBUG] Botão CALCULE AGORA! clicado');
          e.preventDefault(); // Bloquear submit natural para validação
          e.stopPropagation();
          
          // Encontrar o formulário e disparar validação
          const $form = $(this).closest('form');
          if ($form.length) {
            console.log('🔍 [DEBUG] Disparando validação manual do formulário');
            $form.trigger('submit');
          }
        });

        // SUBMIT — revalida tudo e oferece Corrigir / Prosseguir
        $('form').each(function(){
          const $form=$(this);
          
          $form.on('submit', function(ev){
            if ($form.data('validated-ok') === true) { $form.removeData('validated-ok'); return true; }
            if ($form.data('skip-validate') === true){ $form.removeData('skip-validate');  return true; }

            console.log('🔍 [DEBUG] Submit do formulário interceptado');
            ev.preventDefault();
            ev.stopPropagation();
            if (typeof window.showLoading === 'function') window.showLoading('Validando seus dados…');

            Promise.all([
              $CPF.length ? (window.VALIDAR_PH3A ? (typeof window.validarCPFApi === 'function' ? window.validarCPFApi($CPF.val()) : Promise.resolve({ok: false})) : Promise.resolve({ok: typeof window.validarCPFAlgoritmo === 'function' ? window.validarCPFAlgoritmo($CPF.val()) : false})) : Promise.resolve({ok: true}),
              $CEP.length   ? (typeof window.validarCepViaCep === 'function' ? window.validarCepViaCep($CEP.val()) : Promise.resolve({ok:true}))  : Promise.resolve({ok:true}),
              $PLACA.length ? (typeof window.validarPlacaApi === 'function' ? window.validarPlacaApi($PLACA.val()) : Promise.resolve({ok:true})) : Promise.resolve({ok:true}),
              // TELEFONE no submit — considera incompleto como inválido
              ($DDD.length && $CEL.length && typeof window.onlyDigits === 'function')
                ? (function(){
                    const d = window.onlyDigits($DDD.val()).length;
                    const n = window.onlyDigits($CEL.val()).length;
                    if (d === 2 && n === 9) return (typeof window.validarTelefoneAsync === 'function' ? window.validarTelefoneAsync($DDD,$CEL) : Promise.resolve({ok:false}));    // completo → valida API
                    if (d === 2 && n > 0 && n < 9) return Promise.resolve({ok:false});  // incompleto → inválido
                    return Promise.resolve({ok:false}); // ddd incompleto ou vazio → inválido
                  })()
                : Promise.resolve({ok:false}),
              // E-mail: regex (bloqueante)
              $EMAIL.length ? Promise.resolve({ok: typeof window.validarEmailLocal === 'function' ? window.validarEmailLocal(($EMAIL.val()||'').trim()) : false}) : Promise.resolve({ok:true})
            ])
            .then(([cpfRes, cepRes, placaRes, telRes, mailRes])=>{
              if (typeof window.hideLoading === 'function') window.hideLoading();

              // autopreenche MARCA/ANO/TIPO de novo se validou placa
              if (placaRes.ok && placaRes.parsed && typeof window.setFieldValue === 'function'){
                if (placaRes.parsed.marcaTxt) window.setFieldValue('MARCA', placaRes.parsed.marcaTxt);
                if (placaRes.parsed.anoModelo) window.setFieldValue('ANO', placaRes.parsed.anoModelo);
                if (placaRes.parsed.tipoVeiculo) window.setFieldValue('TIPO-DE-VEICULO', placaRes.parsed.tipoVeiculo);
              }

              // autopreenche SEXO/DATA/ESTADO-CIVIL se validou CPF com API
              if (cpfRes.ok && cpfRes.parsed && window.VALIDAR_PH3A && typeof window.setFieldValue === 'function') {
                if (cpfRes.parsed.sexo) window.setFieldValue('SEXO', cpfRes.parsed.sexo);
                if (cpfRes.parsed.dataNascimento) window.setFieldValue('DATA-DE-NASCIMENTO', cpfRes.parsed.dataNascimento);
                if (cpfRes.parsed.estadoCivil) window.setFieldValue('ESTADO-CIVIL', cpfRes.parsed.estadoCivil);
              }

              const invalido = (!cpfRes.ok) || (!cepRes.ok) || (!placaRes.ok) || (!telRes.ok) || (!mailRes.ok);
              console.log('🔍 [DEBUG] Dados inválidos?', invalido);

              if (!invalido){
                console.log('✅ [DEBUG] Dados válidos - verificando RPA');
                
                // 🎯 CAPTURAR CONVERSÃO GTM - DADOS VÁLIDOS
                console.log('🎯 [GTM] Registrando conversão - dados válidos');
                if (typeof window.dataLayer !== 'undefined') {
                  window.dataLayer.push({
                    'event': 'form_submit_valid',
                    'form_type': 'cotacao_seguro',
                    'validation_status': 'valid'
                  });
                }
                
                if (window.rpaEnabled === true) {
                  console.log('🎯 [RPA] RPA habilitado - iniciando processo RPA');
                  window.loadRPAScript()
                    .then(() => {
                      console.log('🎯 [RPA] Script RPA carregado - executando processo');
                      if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                        const mainPageInstance = new window.MainPage();
                        mainPageInstance.handleFormSubmit($form[0]);
                      } else {
                        console.warn('🎯 [RPA] Função handleFormSubmit não encontrada - usando fallback');
                        $form.data('validated-ok', true);
                        if (typeof window.nativeSubmit === 'function') {
                          window.nativeSubmit($form);
                        } else {
                          $form[0].submit();
                        }
                      }
                    })
                    .catch((error) => {
                      console.error('🎯 [RPA] Erro ao carregar script RPA:', error);
                      console.log('🎯 [RPA] Fallback para processamento Webflow');
                      $form.data('validated-ok', true);
                      if (typeof window.nativeSubmit === 'function') {
                        window.nativeSubmit($form);
                      } else {
                        $form[0].submit();
                      }
                    });
                } else {
                  console.log('🎯 [RPA] RPA desabilitado - processando apenas com Webflow');
                  $form.data('validated-ok', true);
                  if (typeof window.nativeSubmit === 'function') {
                    window.nativeSubmit($form);
                  } else {
                    $form[0].submit();
                  }
                }
              } else {
                console.log('❌ [DEBUG] Dados inválidos - mostrando SweetAlert');
                let linhas = "";
                if (!cpfRes.ok)       linhas += "• CPF inválido\n";
                if (!cepRes.ok)   linhas += "• CEP inválido\n";
                if (!placaRes.ok) linhas += "• Placa inválida\n";
                if (!telRes.ok)   linhas += "• Celular inválido\n";
                if (!mailRes.ok)  linhas += "• E-mail inválido\n";

                Swal.fire({
                  icon: 'info',
                  title: 'Atenção!',
                  html:
                    "⚠️ Os campos CPF, CEP, PLACA, CELULAR e E-MAIL corretamente preenchidos são necessários para efetuar o cálculo do seguro.\n\n" +
                    "Campos com problema:\n\n" + linhas + "\n" +
                    "Caso decida prosseguir assim mesmo, um especialista entrará em contato para coletar esses dados.",
                  showCancelButton: true,
                  confirmButtonText: 'Prosseguir assim mesmo',
                  cancelButtonText: 'Corrigir',
                  reverseButtons: true,
                  allowOutsideClick: false,
                  allowEscapeKey: true
                }).then(r=>{
                  if (r.isConfirmed){
                    console.log('🎯 [RPA] Usuário escolheu prosseguir com dados inválidos');
                    
                    // 🎯 CAPTURAR CONVERSÃO GTM - USUÁRIO PROSSEGUIU COM DADOS INVÁLIDOS
                    console.log('🎯 [GTM] Registrando conversão - usuário prosseguiu com dados inválidos');
                    if (typeof window.dataLayer !== 'undefined') {
                      window.dataLayer.push({
                        'event': 'form_submit_invalid_proceed',
                        'form_type': 'cotacao_seguro',
                        'validation_status': 'invalid_proceed'
                      });
                    }
                    
                    if (window.rpaEnabled === true) {
                      console.log('🎯 [RPA] RPA habilitado - iniciando processo RPA com dados inválidos');
                      window.loadRPAScript()
                        .then(() => {
                          console.log('🎯 [RPA] Script RPA carregado - executando processo com dados inválidos');
                          if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                            const mainPageInstance = new window.MainPage();
                            mainPageInstance.handleFormSubmit($form[0]);
                          } else {
                            console.warn('🎯 [RPA] Função handleFormSubmit não encontrada - usando fallback');
                            $form.data('skip-validate', true);
                            if (typeof window.nativeSubmit === 'function') {
                              window.nativeSubmit($form);
                            } else {
                              $form[0].submit();
                            }
                          }
                        })
                        .catch((error) => {
                          console.error('🎯 [RPA] Erro ao carregar script RPA:', error);
                          console.log('🎯 [RPA] Fallback para processamento Webflow');
                          $form.data('skip-validate', true);
                          if (typeof window.nativeSubmit === 'function') {
                            window.nativeSubmit($form);
                          } else {
                            $form[0].submit();
                          }
                        });
                    } else {
                      console.log('🎯 [RPA] RPA desabilitado - processando apenas com Webflow');
                      $form.data('skip-validate', true);
                      if (typeof window.nativeSubmit === 'function') {
                        window.nativeSubmit($form);
                      } else {
                        $form[0].submit();
                      }
                    }
                  } else {
                    if (!cpfRes.ok && $CPF.length)        { $CPF.focus(); return; }
                    if (!cepRes.ok && $CEP.length)    { $CEP.focus(); return; }
                    if (!placaRes.ok && $PLACA.length){ $PLACA.focus(); return; }
                    if (!telRes.ok && ($DDD.length && $CEL.length)) { $CEL.focus(); return; }
                    if (!mailRes.ok && $EMAIL.length) { $EMAIL.focus(); return; }
                  }
                });
              }
            })
            .catch(_=>{
              if (typeof window.hideLoading === 'function') window.hideLoading();
              Swal.fire({
                icon: 'info',
                title: 'Não foi possível validar agora',
                html:  'Deseja prosseguir assim mesmo?',
                showCancelButton: true,
                confirmButtonText: 'Prosseguir assim mesmo',
                cancelButtonText: 'Corrigir',
                reverseButtons: true,
                allowOutsideClick: false,
                allowEscapeKey: true
              }).then(r=>{
                if (r.isConfirmed) { 
                  console.log('🎯 [RPA] Usuário escolheu prosseguir após erro de rede');
                  
                  // 🎯 CAPTURAR CONVERSÃO GTM - USUÁRIO PROSSEGUIU APÓS ERRO DE REDE
                  console.log('🎯 [GTM] Registrando conversão - usuário prosseguiu após erro de rede');
                  if (typeof window.dataLayer !== 'undefined') {
                    window.dataLayer.push({
                      'event': 'form_submit_network_error_proceed',
                      'form_type': 'cotacao_seguro',
                      'validation_status': 'network_error_proceed'
                    });
                  }
                  
                  if (window.rpaEnabled === true) {
                    console.log('🎯 [RPA] RPA habilitado - iniciando processo RPA após erro de rede');
                    window.loadRPAScript()
                      .then(() => {
                        console.log('🎯 [RPA] Script RPA carregado - executando processo após erro de rede');
                        if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                          const mainPageInstance = new window.MainPage();
                          mainPageInstance.handleFormSubmit($form[0]);
                        } else {
                          console.warn('🎯 [RPA] Função handleFormSubmit não encontrada - usando fallback');
                          $form.data('skip-validate', true);
                          if (typeof window.nativeSubmit === 'function') {
                            window.nativeSubmit($form);
                          } else {
                            $form[0].submit();
                          }
                        }
                      })
                      .catch((error) => {
                        console.error('🎯 [RPA] Erro ao carregar script RPA:', error);
                        console.log('🎯 [RPA] Fallback para processamento Webflow');
                        $form.data('skip-validate', true);
                        if (typeof window.nativeSubmit === 'function') {
                          window.nativeSubmit($form);
                        } else {
                          $form[0].submit();
                        }
                      });
                  } else {
                    console.log('🎯 [RPA] RPA desabilitado - processando apenas com Webflow');
                    $form.data('skip-validate', true);
                    if (typeof window.nativeSubmit === 'function') {
                      window.nativeSubmit($form);
                    } else {
                      $form[0].submit();
                    }
                  }
                }
              });
            });
          });
        });
        
        // 6. Webflow Equipes
        window.Webflow ||= [];
        window.Webflow.push(() => {
          const LIST = document.querySelector('#Equipes-list');
          const OUT  = document.getElementById('qtde_colaboradores');

          const isVisible = (el) => {
            const st = getComputedStyle(el);
            return el.offsetParent !== null && st.display !== 'none' && st.visibility !== 'hidden' && st.opacity !== '0';
          };

          const recalc = () => {
            const n = LIST ? [...LIST.querySelectorAll('.w-dyn-item')].filter(isVisible).length : 0;
            if (OUT) OUT.textContent = String(n);
          };

          recalc(); // na carga

          // Atualiza em mudanças (filtros/paginação/dinâmicas)
          if (LIST) new MutationObserver(recalc).observe(LIST, {
            childList: true, subtree: true, attributes: true, attributeFilter: ['style','class']
          });
          document.addEventListener('fs-cmsfilter-update', recalc);       // Finsweet
          document.addEventListener('jetboost:filter:applied', recalc);    // Jetboost
          document.addEventListener('jetboost:pagination:loaded', recalc); // Jetboost
        });
        
        // 7. Debug RPA
        console.log('🔍 [DEBUG] Iniciando verificação de injeção RPA...');

        // Função para verificar se a injeção foi bem-sucedida
        function debugRPAModule() {
          console.log('🔍 [DEBUG] === VERIFICAÇÃO DE INJEÇÃO RPA ===');
          
          // 1. Verificar se window.rpaEnabled existe
          if (typeof window.rpaEnabled !== 'undefined') {
            console.log('✅ [DEBUG] window.rpaEnabled encontrado:', window.rpaEnabled);
          } else {
            console.error('❌ [DEBUG] window.rpaEnabled NÃO encontrado!');
          }
          
          // 2. Verificar se loadRPAScript existe
          if (typeof window.loadRPAScript === 'function') {
            console.log('✅ [DEBUG] window.loadRPAScript encontrado');
          } else {
            console.error('❌ [DEBUG] window.loadRPAScript NÃO encontrado!');
          }
          
          // 3. Verificar se jQuery está disponível
          if (typeof $ !== 'undefined') {
            console.log('✅ [DEBUG] jQuery disponível:', $.fn.jquery);
          } else {
            console.error('❌ [DEBUG] jQuery NÃO disponível!');
          }
          
          // 4. Verificar se SweetAlert2 está disponível
          if (typeof Swal !== 'undefined') {
            console.log('✅ [DEBUG] SweetAlert2 disponível');
          } else {
            console.warn('⚠️ [DEBUG] SweetAlert2 NÃO disponível (pode ser carregado dinamicamente)');
          }
          
          // 5. Verificar conflitos de nomes de função
          const globalFunctions = Object.keys(window).filter(key => typeof window[key] === 'function');
          const rpaFunctions = globalFunctions.filter(func => func.toLowerCase().includes('rpa') || func.toLowerCase().includes('load'));
          console.log('🔍 [DEBUG] Funções globais relacionadas ao RPA:', rpaFunctions);
          
          // 6. Verificar se há elementos de formulário
          const forms = document.querySelectorAll('form');
          console.log('🔍 [DEBUG] Formulários encontrados:', forms.length);
          
          // 7. Verificar se há botões de submit
          const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
          console.log('🔍 [DEBUG] Botões de submit encontrados:', submitButtons.length);
          
          console.log('🔍 [DEBUG] === FIM DA VERIFICAÇÃO ===');
        }

        // Função para testar carregamento dinâmico
        function testDynamicLoading() {
          console.log('🔍 [DEBUG] Testando carregamento dinâmico...');
          
          if (typeof window.loadRPAScript === 'function') {
            console.log('🔍 [DEBUG] Tentando carregar script RPA...');
            
            window.loadRPAScript()
              .then(() => {
                console.log('✅ [DEBUG] Script RPA carregado com sucesso!');
                
                // Verificar se as classes RPA foram carregadas
                if (typeof window.MainPage !== 'undefined') {
                  console.log('✅ [DEBUG] window.MainPage disponível');
                } else {
                  console.error('❌ [DEBUG] window.MainPage NÃO disponível após carregamento');
                }
                
                if (typeof window.ProgressModalRPA !== 'undefined') {
                  console.log('✅ [DEBUG] window.ProgressModalRPA disponível');
                } else {
                  console.error('❌ [DEBUG] window.ProgressModalRPA NÃO disponível após carregamento');
                }
                
                if (typeof window.SpinnerTimer !== 'undefined') {
                  console.log('✅ [DEBUG] window.SpinnerTimer disponível');
                } else {
                  console.error('❌ [DEBUG] window.SpinnerTimer NÃO disponível após carregamento');
                }
                
              })
              .catch(error => {
                console.error('❌ [DEBUG] Erro ao carregar script RPA:', error);
              });
          } else {
            console.error('❌ [DEBUG] window.loadRPAScript não está disponível para teste');
          }
        }

        // Função para detectar conflitos
        function detectConflicts() {
          console.log('🔍 [DEBUG] === DETECÇÃO DE CONFLITOS ===');
          
          // Verificar se há múltiplas definições de funções
          const functionNames = [];
          const scripts = document.querySelectorAll('script');
          
          scripts.forEach((script, index) => {
            if (script.textContent) {
              const content = script.textContent;
              
              // Pular scripts que contêm apenas código de debug (evitar detectar a si mesmo)
              if (content.includes('detectConflicts') && content.includes('DEBUG] === DETECÇÃO DE CONFLITOS ===')) {
                return; // Pular este script
              }
              
              // Verificar se há DEFINIÇÕES reais de loadRPAScript (não apenas menções)
              if (content.includes('window.loadRPAScript =') || content.includes('function loadRPAScript(')) {
                functionNames.push(`Script ${index + 1}: loadRPAScript`);
              }
              
              // Verificar se há DEFINIÇÕES reais de rpaEnabled (não apenas menções)
              if (content.includes('window.rpaEnabled =') || content.includes('var rpaEnabled') || content.includes('let rpaEnabled') || content.includes('const rpaEnabled')) {
                functionNames.push(`Script ${index + 1}: rpaEnabled`);
              }
            }
          });
          
          if (functionNames.length > 1) {
            console.warn('⚠️ [DEBUG] Possível conflito detectado - múltiplas definições:', functionNames);
          } else {
            console.log('✅ [DEBUG] Nenhum conflito de múltiplas definições detectado');
          }
          
          // Verificar se há erros no console
          const originalError = console.error;
          const errors = [];
          console.error = function(...args) {
            errors.push(args.join(' '));
            originalError.apply(console, args);
          };
          
          setTimeout(() => {
            console.error = originalError;
            if (errors.length > 0) {
              console.warn('⚠️ [DEBUG] Erros detectados durante inicialização:', errors);
            } else {
              console.log('✅ [DEBUG] Nenhum erro detectado durante inicialização');
            }
          }, 2000);
          
          console.log('🔍 [DEBUG] === FIM DA DETECÇÃO DE CONFLITOS ===');
        }

        // Executar verificações após DOM estar pronto
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', () => {
            setTimeout(debugRPAModule, 100);
            setTimeout(detectConflicts, 200);
          });
        } else {
          setTimeout(debugRPAModule, 100);
          setTimeout(detectConflicts, 200);
        }

        // Expor funções de debug globalmente para teste manual
        window.debugRPAModule = debugRPAModule;
        window.testDynamicLoading = testDynamicLoading;
        window.detectConflicts = detectConflicts;

        console.log('🔍 [DEBUG] Funções de debug disponíveis:');
        console.log('  - window.debugRPAModule()');
        console.log('  - window.testDynamicLoading()');
        console.log('  - window.detectConflicts()');
      });
    }
    
    // Inicialização (aguarda DOM e dependências)
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        waitForDependencies(init);
      });
    } else {
      // DOM já está pronto, mas ainda precisamos verificar dependências
      waitForDependencies(init);
    }
    
  } catch (error) {
    console.error('[UNIFIED] Erro crítico no Footer Code Unificado:', error);
    console.error('[UNIFIED] Stack trace:', error.stack);
    // Não bloquear a página, mas registrar o erro
  }
})();



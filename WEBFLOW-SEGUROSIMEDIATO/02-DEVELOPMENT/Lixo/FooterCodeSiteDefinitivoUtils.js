// ====================== 
// 🛠️ FOOTER CODE UTILS - Funções Utilitárias
// Versão: 1.1 | Data: 2025-10-29
// Corrigido: Removidas tags HTML para compatibilidade com carregamento via <script src>
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


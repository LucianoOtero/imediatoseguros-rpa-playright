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
  
  // Verificar se todas as funções foram expostas corretamente
  const requiredFunctions = [
    'onlyDigits', 'toUpperNospace', 'setFieldValue', 'readCookie',
    'generateSessionId', 'nativeSubmit', 'validarEmailLocal',
    'validarCPFFormato', 'validarCPFAlgoritmo', 'validarPlacaFormato',
    'validarCelularLocal', 'aplicarMascaraPlaca', 'sha1', 'hmacSHA256',
    'extractDataFromPH3A', 'extractVehicleFromPlacaFipe',
    'preencherEnderecoViaCEP'
  ];
  
  const missing = requiredFunctions.filter(fn => typeof window[fn] !== 'function');
  if (missing.length > 0) {
    console.error('❌ [UTILS] Funções faltando:', missing);
  } else {
    console.log('✅ [UTILS] Footer Code Utils carregado - 17 funções disponíveis');
  }
})();
// ======================


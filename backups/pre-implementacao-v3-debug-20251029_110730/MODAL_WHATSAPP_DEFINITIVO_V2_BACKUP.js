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
  
  // Flag para controlar registro inicial (evitar múltiplos registros)
  let initialRegistrationAttempted = false;
  
  // ==================== VARIÁVEIS GOOGLE TAG MANAGER (Configuráveis) ====================
  
  // CONFIGURAÇÃO GTM - VARIÁVEIS (preencher depois no GTM ou no código)
  window.GTM_EVENT_NAME_INITIAL = window.GTM_EVENT_NAME_INITIAL || 'whatsapp_modal_initial_contact'; // Nome do evento GTM
  window.GTM_FORM_TYPE = window.GTM_FORM_TYPE || 'whatsapp_modal';                                   // Tipo de formulário
  window.GTM_CONTACT_STAGE = window.GTM_CONTACT_STAGE || 'initial';                                  // Estágio do contato
  window.GTM_UTM_SOURCE = window.GTM_UTM_SOURCE || null;                                            // UTM Source (auto-preenchido se null)
  window.GTM_UTM_CAMPAIGN = window.GTM_UTM_CAMPAIGN || null;                                         // UTM Campaign (auto-preenchido se null)
  window.GTM_UTM_MEDIUM = window.GTM_UTM_MEDIUM || null;                                            // UTM Medium (auto-preenchido se null)
  window.GTM_UTM_TERM = window.GTM_UTM_TERM || null;                                                // UTM Term (auto-preenchido se null)
  window.GTM_UTM_CONTENT = window.GTM_UTM_CONTENT || null;                                          // UTM Content (auto-preenchido se null)
  window.GTM_PAGE_URL = window.GTM_PAGE_URL || null;                                                // URL da página (auto-preenchido se null)
  window.GTM_PAGE_TITLE = window.GTM_PAGE_TITLE || null;                                            // Título da página (auto-preenchido se null)
  window.GTM_USER_AGENT = window.GTM_USER_AGENT || null;                                            // User Agent (auto-preenchido se null)
  
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
  
  // ==================== DETECÇÃO DE AMBIENTE ====================
  
  /**
   * Detectar se estamos em ambiente de desenvolvimento
   * @returns {boolean}
   */
  function isDevelopmentEnvironment() {
    // Opção 1: Verificar hostname
    if (window.location.hostname.includes('dev.') || 
        window.location.hostname.includes('localhost') ||
        window.location.hostname.includes('127.0.0.1')) {
      return true;
    }
    
    // Opção 2: Verificar URL
    if (window.location.href.includes('/dev/')) {
      return true;
    }
    
    // Opção 3: Parâmetro GET
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('env') === 'dev' || urlParams.get('dev') === '1') {
      return true;
    }
    
    // Opção 4: Variável global configurada
    if (typeof window.ENVIRONMENT !== 'undefined' && window.ENVIRONMENT === 'development') {
      return true;
    }
    
    return false;
  }
  
  /**
   * Obter URL do endpoint baseado no ambiente
   * @param {string} endpoint - 'travelangels' ou 'octadesk'
   * @returns {string} URL do endpoint
   */
  function getEndpointUrl(endpoint) {
    const isDev = isDevelopmentEnvironment();
    
    const endpoints = {
      travelangels: {
        dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php',
        prod: 'https://bpsegurosimediato.com.br/add_travelangels.php'
      },
      octadesk: {
        dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php',
        prod: 'https://bpsegurosimediato.com.br/add_webflow_octa.php'
      }
    };
    
    const env = isDev ? 'dev' : 'prod';
    const url = endpoints[endpoint][env];
    
    console.log(`🌍 [MODAL] Ambiente: ${env.toUpperCase()} | Endpoint ${endpoint}: ${url}`);
    
    return url;
  }
  
  // ==================== FUNÇÕES AUXILIARES ====================
  
  /**
   * Obter parâmetro UTM da URL
   * @param {string} param - Nome do parâmetro UTM
   * @returns {string}
   */
  function getUtmParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param) || '';
  }
  
  /**
   * Sanitizar dados para prevenir XSS
   * @param {Object} data - Dados a sanitizar
   * @returns {Object}
   */
  function sanitizeData(data) {
    const sanitized = {};
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string') {
        // Remover tags HTML e caracteres perigosos
        sanitized[key] = value
          .replace(/[<>]/g, '') // Remove < >
          .trim()
          .slice(0, 500); // Limitar tamanho
      } else if (value != null) {
        sanitized[key] = value;
      }
    }
    
    return sanitized;
  }
  
  /**
   * Gerar ID de sessão único
   * @returns {string}
   */
  function generateSessionId() {
    if (!window.modalSessionId) {
      window.modalSessionId = 'modal_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    return window.modalSessionId;
  }
  
  /**
   * Log de eventos estruturado
   * @param {string} eventType - Tipo do evento
   * @param {Object} data - Dados do evento
   * @param {string} severity - Nível de severidade (info, warning, error)
   */
  function logEvent(eventType, data, severity = 'info') {
    const logData = {
      event: eventType,
      timestamp: new Date().toISOString(),
      severity: severity,
      data: sanitizeData(data), // Sanitizar dados antes de logar
      session_id: generateSessionId(),
      page_url: window.location.href,
      environment: isDevelopmentEnvironment() ? 'dev' : 'prod'
    };
    
    // Log no console (sem dados sensíveis completos)
    console.log(`[${severity.toUpperCase()}] ${eventType}`, {
      has_ddd: !!data.ddd,
      has_celular: !!data.celular,
      has_cpf: !!data.cpf,
      has_nome: !!data.nome,
      environment: logData.environment
    });
    
    // Enviar para sistema de logging se disponível
    try {
      if (typeof window.logDebug === 'function') {
        window.logDebug(severity.toUpperCase(), `[MODAL] ${eventType}`, logData);
      }
    } catch (e) {
      // Falha silenciosa em logging
    }
  }
  
  /**
   * Gerenciamento de estado do lead (localStorage)
   */
  function saveLeadState(leadData) {
    const state = {
      lead_id: leadData.id || null,
      ddd: leadData.ddd,
      celular: onlyDigits(leadData.celular),
      gclid: leadData.gclid || '',
      timestamp: Date.now(),
      expires: Date.now() + (30 * 60 * 1000) // 30 minutos
    };
    
    try {
      localStorage.setItem('whatsapp_modal_lead_state', JSON.stringify(state));
      console.log('💾 [MODAL] Estado do lead salvo:', { id: state.lead_id, ddd: state.ddd });
    } catch (e) {
      console.warn('⚠️ [MODAL] Não foi possível salvar estado (localStorage indisponível)');
    }
  }
  
  function getLeadState() {
    try {
      const stored = localStorage.getItem('whatsapp_modal_lead_state');
      if (!stored) return null;
      
      const state = JSON.parse(stored);
      
      // Verificar expiração
      if (Date.now() > state.expires) {
        localStorage.removeItem('whatsapp_modal_lead_state');
        return null;
      }
      
      return state;
    } catch (e) {
      return null;
    }
  }
  
  /**
   * Rate Limiter para prevenir spam
   */
  class RateLimiter {
    constructor(maxCalls = 3, windowMs = 60000) {
      this.maxCalls = maxCalls;
      this.windowMs = windowMs;
      this.calls = new Map(); // key -> [timestamps]
    }
    
    canMakeCall(key) {
      const now = Date.now();
      const userCalls = this.calls.get(key) || [];
      
      // Remover chamadas antigas (fora da janela)
      const recentCalls = userCalls.filter(timestamp => now - timestamp < this.windowMs);
      
      if (recentCalls.length >= this.maxCalls) {
        return false;
      }
      
      recentCalls.push(now);
      this.calls.set(key, recentCalls);
      return true;
    }
  }
  
  const rateLimiter = new RateLimiter(3, 60000); // 3 chamadas por minuto
  
  /**
   * Fetch com retry para chamadas críticas
   * @param {string} url - URL do endpoint
   * @param {Object} options - Opções do fetch
   * @param {number} maxRetries - Número máximo de tentativas
   * @param {number} retryDelay - Delay entre tentativas (ms)
   * @returns {Promise}
   */
  async function fetchWithRetry(url, options, maxRetries = 2, retryDelay = 1000) {
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        // Criar AbortController para timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout
        
        const response = await fetch(url, {
          ...options,
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok || response.status < 500) {
          return { success: true, response, attempt };
        }
        
        // Retry apenas para erros 5xx (servidor) ou timeout
        if (attempt < maxRetries && (response.status >= 500 || response.status === 408)) {
          console.warn(`⚠️ [MODAL] Tentativa ${attempt + 1}/${maxRetries + 1} falhou, tentando novamente...`);
          await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1)));
          continue;
        }
        
        return { success: false, response, attempt };
        
      } catch (error) {
        // Erro de rede ou timeout - tentar retry
        if (attempt < maxRetries && (error.name === 'TypeError' || error.name === 'AbortError')) {
          console.warn(`⚠️ [MODAL] Erro de rede na tentativa ${attempt + 1}/${maxRetries + 1}, retry...`);
          await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1)));
          continue;
        }
        
        return { success: false, error, attempt };
      }
    }
  }
  
  /**
   * Funções de Loading (compatibilidade com Footer Code)
   */
  function showLoading(message) {
    if (typeof window.showLoading === 'function') {
      window.showLoading(message);
    } else {
      const overlay = document.getElementById('si-loading-overlay');
      const text = document.getElementById('si-loading-text');
      if (overlay) overlay.style.display = 'flex';
      if (text && message) text.textContent = message;
    }
  }
  
  function hideLoading() {
    if (typeof window.hideLoading === 'function') {
      window.hideLoading();
    } else {
      const overlay = document.getElementById('si-loading-overlay');
      if (overlay) overlay.style.display = 'none';
    }
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
      DDD: $(MODAL_CONFIG.fieldIds.ddd).val(),
      CELULAR: $(MODAL_CONFIG.fieldIds.celular).val(),
      CPF: $(MODAL_CONFIG.fieldIds.cpf).val() || '',
      NOME: $(MODAL_CONFIG.fieldIds.nome).val() || '',
      EMAIL: '', // Email não existe no modal atual
      CEP: $(MODAL_CONFIG.fieldIds.cep).val() || '',
      PLACA: $(MODAL_CONFIG.fieldIds.placa).val() || '',
      ENDERECO: $(MODAL_CONFIG.fieldIds.endereco).val() || '',
      MARCA: '', // Não existe no modal atual
      ANO: '', // Não existe no modal atual
      SEXO: '', // Não existe no modal atual
      DATA_NASCIMENTO: '', // Não existe no modal atual
      ESTADO_CIVIL: '', // Não existe no modal atual
      GCLID: getGCLID()
    };
  }
  
  // ==================== FUNÇÕES DE INTEGRAÇÃO ====================
  
  /**
   * Registrar primeiro contato no EspoCRM (após validação do celular)
   * @param {string} ddd - DDD do telefone
   * @param {string} celular - Número do celular
   * @param {string} gclid - GCLID dos cookies
   * @returns {Promise<Object>}
   */
  async function registrarPrimeiroContatoEspoCRM(ddd, celular, gclid) {
    // Verificar rate limiting
    const phoneKey = `${ddd}${onlyDigits(celular)}`;
    if (!rateLimiter.canMakeCall(phoneKey)) {
      console.warn('⚠️ [MODAL] Muitas tentativas recentes, aguarde...');
      return { success: false, error: 'rate_limit' };
    }
    
    const webhook_data = {
      data: {
        'DDD-CELULAR': ddd,
        'CELULAR': onlyDigits(celular),
        'GCLID_FLD': gclid || '',
        'NOME': '',
        'CPF': '',
        'CEP': '',
        'PLACA': '',
        'Email': '',
        'produto': 'seguro-auto',
        'landing_url': window.location.href,
        'utm_source': getUtmParam('utm_source'),
        'utm_campaign': getUtmParam('utm_campaign')
      },
      d: new Date().toISOString(),
      name: 'Modal WhatsApp - Primeiro Contato (V2)'
    };
    
    logEvent('whatsapp_modal_espocrm_initial_attempt', { ddd, celular: '***' }, 'info');
    
    try {
      const endpointUrl = getEndpointUrl('travelangels');
      
      const result = await fetchWithRetry(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Modal-WhatsApp-v1.0'
        },
        body: JSON.stringify(webhook_data)
      }, 2, 1000); // 2 retries, delay de 1s
      
      if (result.success && result.response) {
        try {
          const responseData = await result.response.json();
          
          if (responseData.success || result.response.ok) {
            console.log('✅ [MODAL] Lead criado no EspoCRM:', { attempt: result.attempt + 1 });
            
            const leadId = responseData.contact_id || responseData.lead_id || null;
            
            // Salvar estado
            if (leadId) {
              saveLeadState({ id: leadId, ddd, celular, gclid });
            }
            
            logEvent('whatsapp_modal_espocrm_initial_success', { lead_id: leadId }, 'info');
            
            return { success: true, id: leadId, attempt: result.attempt + 1 };
          } else {
            console.warn('⚠️ [MODAL] Erro ao criar lead no EspoCRM:', responseData);
            logEvent('whatsapp_modal_espocrm_initial_failed', { error: responseData }, 'warning');
            return { success: false, error: responseData, attempt: result.attempt + 1 };
          }
        } catch (parseError) {
          // Resposta não é JSON válido
          console.warn('⚠️ [MODAL] Resposta do EspoCRM não é JSON válido');
          logEvent('whatsapp_modal_espocrm_initial_parse_error', { error: parseError.message }, 'warning');
          return { success: result.response.ok, attempt: result.attempt + 1 };
        }
      } else {
        const errorMsg = result.error?.message || 'Erro desconhecido';
        console.error('❌ [MODAL] Erro na requisição ao EspoCRM:', errorMsg);
        logEvent('whatsapp_modal_espocrm_initial_error', { error: errorMsg, attempt: result.attempt + 1 }, 'error');
        return { success: false, error: errorMsg, attempt: result.attempt + 1 };
      }
    } catch (error) {
      console.error('❌ [MODAL] Erro inesperado ao registrar primeiro contato:', error);
      logEvent('whatsapp_modal_espocrm_initial_exception', { error: error.message }, 'error');
      return { success: false, error: error.message };
    }
  }
  
  /**
   * Atualizar lead no EspoCRM com dados completos
   * @param {Object} dados - Dados completos do formulário
   * @param {string|null} espocrmId - ID do lead criado anteriormente (se houver)
   * @returns {Promise<Object>}
   */
  async function atualizarLeadEspoCRM(dados, espocrmId = null) {
    // Tentar recuperar estado anterior se não tiver ID
    if (!espocrmId) {
      const previousState = getLeadState();
      if (previousState && previousState.lead_id) {
        espocrmId = previousState.lead_id;
        console.log('💾 [MODAL] ID recuperado do localStorage:', espocrmId);
      }
    }
    
    const webhook_data = {
      data: {
        'NOME': sanitizeData({ NOME: dados.NOME }).NOME || '',
        'DDD-CELULAR': dados.DDD || '',
        'CELULAR': onlyDigits(dados.CELULAR) || '',
        'Email': sanitizeData({ Email: dados.EMAIL }).Email || '',
        'CEP': dados.CEP || '',
        'CPF': dados.CPF || '',
        'PLACA': dados.PLACA || '',
        'MARCA': dados.MARCA || '',
        'VEICULO': dados.MARCA || '',
        'ANO': dados.ANO || '',
        'GCLID_FLD': dados.GCLID || '',
        'SEXO': dados.SEXO || '',
        'DATA-DE-NASCIMENTO': dados.DATA_NASCIMENTO || '',
        'ESTADO-CIVIL': dados.ESTADO_CIVIL || '',
        'ENDERECO': sanitizeData({ ENDERECO: dados.ENDERECO }).ENDERECO || '',
        'produto': 'seguro-auto',
        'landing_url': window.location.href,
        'utm_source': getUtmParam('utm_source'),
        'utm_campaign': getUtmParam('utm_campaign')
      },
      d: new Date().toISOString(),
      name: 'Modal WhatsApp - Dados Completos'
    };
    
    // Se tiver ID do lead criado anteriormente, incluir no payload
    if (espocrmId) {
      webhook_data.data.lead_id = espocrmId;
      webhook_data.data.contact_id = espocrmId;
    }
    
    logEvent('whatsapp_modal_espocrm_update_attempt', { 
      has_lead_id: !!espocrmId,
      has_cpf: !!dados.CPF,
      has_nome: !!dados.NOME 
    }, 'info');
    
    try {
      const endpointUrl = getEndpointUrl('travelangels');
      
      const result = await fetchWithRetry(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Modal-WhatsApp-v1.0'
        },
        body: JSON.stringify(webhook_data)
      }, 2, 1000);
      
      if (result.success && result.response) {
        try {
          const responseData = await result.response.json();
          logEvent('whatsapp_modal_espocrm_update_success', { attempt: result.attempt + 1 }, 'info');
          return { success: true, result: responseData, attempt: result.attempt + 1 };
        } catch (parseError) {
          logEvent('whatsapp_modal_espocrm_update_parse_error', { error: parseError.message }, 'warning');
          return { success: result.response.ok, attempt: result.attempt + 1 };
        }
      } else {
        const errorMsg = result.error?.message || 'Erro desconhecido';
        logEvent('whatsapp_modal_espocrm_update_error', { error: errorMsg, attempt: result.attempt + 1 }, 'error');
        return { success: false, error: errorMsg, attempt: result.attempt + 1 };
      }
    } catch (error) {
      console.error('❌ [MODAL] Erro ao atualizar lead no EspoCRM:', error);
      logEvent('whatsapp_modal_espocrm_update_exception', { error: error.message }, 'error');
      return { success: false, error: error.message };
    }
  }
  
  /**
   * Enviar mensagem inicial via Octadesk (após validação do celular)
   * @param {string} ddd - DDD do telefone
   * @param {string} celular - Número do celular
   * @param {string} gclid - GCLID dos cookies
   * @returns {Promise<Object>}
   */
  async function enviarMensagemInicialOctadesk(ddd, celular, gclid) {
    const webhook_data = {
      data: {
        'DDD-CELULAR': ddd,
        'CELULAR': onlyDigits(celular),
        'GCLID_FLD': gclid || '',
        'NOME': '',
        'CPF': '',
        'Email': '',
        'produto': 'seguro-auto',
        'landing_url': window.location.href,
        'utm_source': getUtmParam('utm_source'),
        'utm_campaign': getUtmParam('utm_campaign')
      },
      d: new Date().toISOString(),
      name: 'Modal WhatsApp - Mensagem Inicial (V2)'
    };
    
    logEvent('whatsapp_modal_octadesk_initial_attempt', { has_celular: !!celular }, 'info');
    
    try {
      const endpointUrl = getEndpointUrl('octadesk');
      
      const result = await fetchWithRetry(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Modal-WhatsApp-v2.0'
        },
        body: JSON.stringify(webhook_data)
      }, 2, 1000);
      
      if (result.success && result.response) {
        try {
          const responseData = await result.response.json();
          logEvent('whatsapp_modal_octadesk_initial_success', { attempt: result.attempt + 1 }, 'info');
          return { success: true, result: responseData, attempt: result.attempt + 1 };
        } catch (parseError) {
          logEvent('whatsapp_modal_octadesk_initial_parse_error', { error: parseError.message }, 'warning');
          return { success: result.response.ok, attempt: result.attempt + 1 };
        }
      } else {
        const errorMsg = result.error?.message || 'Erro desconhecido';
        logEvent('whatsapp_modal_octadesk_initial_error', { error: errorMsg, attempt: result.attempt + 1 }, 'error');
        return { success: false, error: errorMsg, attempt: result.attempt + 1 };
      }
    } catch (error) {
      console.error('❌ [MODAL] Erro ao enviar mensagem inicial via Octadesk:', error);
      logEvent('whatsapp_modal_octadesk_initial_exception', { error: error.message }, 'error');
      return { success: false, error: error.message };
    }
  }
  
  /**
   * Enviar mensagem via Octadesk (versão completa - usado no submit se necessário)
   * @param {Object} dados - Dados completos do formulário
   * @returns {Promise<Object>}
   */
  async function enviarMensagemOctadesk(dados) {
    const webhook_data = {
      data: {
        'NOME': sanitizeData({ NOME: dados.NOME }).NOME || '',
        'DDD-CELULAR': dados.DDD || '',
        'CELULAR': onlyDigits(dados.CELULAR) || '',
        'Email': sanitizeData({ Email: dados.EMAIL }).Email || '',
        'CEP': dados.CEP || '',
        'CPF': dados.CPF || '',
        'PLACA': dados.PLACA || '',
        'MARCA': dados.MARCA || '',
        'VEICULO': dados.MARCA || '',
        'ANO': dados.ANO || '',
        'GCLID_FLD': dados.GCLID || '',
        'SEXO': dados.SEXO || '',
        'DATA-DE-NASCIMENTO': dados.DATA_NASCIMENTO || '',
        'ESTADO-CIVIL': dados.ESTADO_CIVIL || '',
        'ENDERECO': sanitizeData({ ENDERECO: dados.ENDERECO }).ENDERECO || '',
        'produto': 'seguro-auto',
        'landing_url': window.location.href,
        'utm_source': getUtmParam('utm_source'),
        'utm_campaign': getUtmParam('utm_campaign')
      },
      d: new Date().toISOString(),
      name: 'Modal WhatsApp - Mensagem Octadesk'
    };
    
    logEvent('whatsapp_modal_octadesk_attempt', { has_celular: !!dados.CELULAR }, 'info');
    
    try {
      const endpointUrl = getEndpointUrl('octadesk');
      
      const result = await fetchWithRetry(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Modal-WhatsApp-v1.0'
        },
        body: JSON.stringify(webhook_data)
      }, 2, 1000);
      
      if (result.success && result.response) {
        try {
          const responseData = await result.response.json();
          logEvent('whatsapp_modal_octadesk_success', { attempt: result.attempt + 1 }, 'info');
          return { success: true, result: responseData, attempt: result.attempt + 1 };
        } catch (parseError) {
          logEvent('whatsapp_modal_octadesk_parse_error', { error: parseError.message }, 'warning');
          return { success: result.response.ok, attempt: result.attempt + 1 };
        }
      } else {
        const errorMsg = result.error?.message || 'Erro desconhecido';
        logEvent('whatsapp_modal_octadesk_error', { error: errorMsg, attempt: result.attempt + 1 }, 'error');
        return { success: false, error: errorMsg, attempt: result.attempt + 1 };
      }
    } catch (error) {
      console.error('❌ [MODAL] Erro ao enviar mensagem via Octadesk:', error);
      logEvent('whatsapp_modal_octadesk_exception', { error: error.message }, 'error');
      return { success: false, error: error.message };
    }
  }
  
  /**
   * Registrar conversão inicial no Google Tag Manager
   * @param {string} ddd - DDD do telefone
   * @param {string} celular - Número do celular
   * @param {string} gclid - GCLID dos cookies
   * @returns {Object} Resultado do registro
   */
  function registrarConversaoInicialGTM(ddd, celular, gclid) {
    if (typeof window.dataLayer === 'undefined') {
      console.warn('⚠️ [MODAL] dataLayer não disponível para registro de conversão inicial');
      logEvent('whatsapp_modal_gtm_initial_datalayer_unavailable', {}, 'warning');
      return { success: false, error: 'dataLayer_unavailable' };
    }
    
    // Construir dados do evento GTM usando variáveis configuráveis
    const gtmEventData = {
      'event': window.GTM_EVENT_NAME_INITIAL || 'whatsapp_modal_initial_contact',
      'form_type': window.GTM_FORM_TYPE || 'whatsapp_modal',
      'contact_stage': window.GTM_CONTACT_STAGE || 'initial',
      'phone_ddd': ddd || '',
      'phone_number': '***', // Não expor número completo por segurança
      'has_phone': !!celular,
      'gclid': gclid || '',
      'utm_source': window.GTM_UTM_SOURCE || getUtmParam('utm_source') || '',
      'utm_campaign': window.GTM_UTM_CAMPAIGN || getUtmParam('utm_campaign') || '',
      'utm_medium': window.GTM_UTM_MEDIUM || getUtmParam('utm_medium') || '',
      'utm_term': window.GTM_UTM_TERM || getUtmParam('utm_term') || '',
      'utm_content': window.GTM_UTM_CONTENT || getUtmParam('utm_content') || '',
      'page_url': window.GTM_PAGE_URL || window.location.href || '',
      'page_title': window.GTM_PAGE_TITLE || document.title || '',
      'user_agent': window.GTM_USER_AGENT || navigator.userAgent || '',
      'timestamp': new Date().toISOString(),
      'environment': isDevelopmentEnvironment() ? 'dev' : 'prod'
    };
    
    window.dataLayer.push(gtmEventData);
    
    logEvent('whatsapp_modal_gtm_initial_conversion', { 
      event_name: gtmEventData.event,
      has_gclid: !!gtmEventData.gclid
    }, 'info');
    
    console.log('📊 [MODAL] Conversão inicial registrada no GTM:', gtmEventData.event);
    
    return { success: true, eventData: gtmEventData };
  }
  
  /**
   * Registrar conversão no Google Ads (mantida para compatibilidade)
   * @param {Object} dados - Dados do formulário
   */
  function registrarConversaoGoogleAds(dados) {
    if (typeof window.dataLayer === 'undefined') {
      console.warn('⚠️ [MODAL] dataLayer não disponível para registro de conversão');
      logEvent('whatsapp_modal_googleads_datalayer_unavailable', {}, 'warning');
      return;
    }
    
    window.dataLayer.push({
      'event': 'whatsapp_modal_submit',
      'form_type': 'whatsapp_modal',
      'validation_status': 'valid',
      'phone': dados.CELULAR ? '***' : '', // Não logar telefone completo
      'has_cpf': !!dados.CPF,
      'has_placa': !!dados.PLACA,
      'has_cep': !!dados.CEP,
      'has_nome': !!dados.NOME,
      'gclid': dados.GCLID || ''
    });
    
    logEvent('whatsapp_modal_googleads_conversion', { 
      has_cpf: !!dados.CPF,
      has_placa: !!dados.PLACA 
    }, 'info');
    
    console.log('✅ [MODAL] Conversão registrada no Google Ads');
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
          
          // ✅ V2: Registrar primeiro contato (EspoCRM + Octadesk + GTM) em PARALELO
          if (!initialRegistrationAttempted) {
            initialRegistrationAttempted = true;
            const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
            const celular = $(this).val();
            const gclid = getGCLID();
            
            console.log('📞 [MODAL] Processando registro inicial (paralelo): EspoCRM + Octadesk + GTM...');
            
            // PROCESSAR EM PARALELO: EspoCRM + Octadesk + GTM
            Promise.all([
              registrarPrimeiroContatoEspoCRM(ddd, celular, gclid),
              enviarMensagemInicialOctadesk(ddd, celular, gclid),
              Promise.resolve(registrarConversaoInicialGTM(ddd, celular, gclid))
            ])
            .then(([espocrmResult, octadeskResult, gtmResult]) => {
              // Log dos resultados
              if (espocrmResult.success) {
                console.log('✅ [MODAL] Lead criado no EspoCRM:', espocrmResult.id || 'sem ID');
                if (espocrmResult.id) {
                  saveLeadState({ id: espocrmResult.id, ddd, celular, gclid });
                }
              } else {
                console.warn('⚠️ [MODAL] Erro ao criar lead (não bloqueante):', espocrmResult.error);
              }
              
              if (octadeskResult.success) {
                console.log('✅ [MODAL] Mensagem inicial enviada via Octadesk');
              } else {
                console.warn('⚠️ [MODAL] Erro ao enviar mensagem (não bloqueante):', octadeskResult.error);
              }
              
              if (gtmResult.success) {
                console.log('✅ [MODAL] Conversão inicial registrada no GTM');
              } else {
                console.warn('⚠️ [MODAL] Erro ao registrar conversão (não bloqueante):', gtmResult.error);
              }
            })
            .catch(error => {
              console.warn('⚠️ [MODAL] Erros no processamento inicial (não bloqueante):', error);
            });
          }
        }
      }).catch(_ => hideLoading());
    } else {
      // Se não houver função de API, apenas valida formato
      showFieldSuccess($(this));
      
      // ✅ V2: Registrar primeiro contato (EspoCRM + Octadesk + GTM) em PARALELO (sem API)
      if (celularDigits === 9 && dddDigits === 2 && !initialRegistrationAttempted) {
        initialRegistrationAttempted = true;
        const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
        const celular = $(this).val();
        const gclid = getGCLID();
        
        console.log('📞 [MODAL] Processando registro inicial (paralelo): EspoCRM + Octadesk + GTM (sem API)...');
        
        // PROCESSAR EM PARALELO: EspoCRM + Octadesk + GTM
        Promise.all([
          registrarPrimeiroContatoEspoCRM(ddd, celular, gclid),
          enviarMensagemInicialOctadesk(ddd, celular, gclid),
          Promise.resolve(registrarConversaoInicialGTM(ddd, celular, gclid))
        ])
        .then(([espocrmResult, octadeskResult, gtmResult]) => {
          if (espocrmResult.success) {
            console.log('✅ [MODAL] Lead criado no EspoCRM:', espocrmResult.id || 'sem ID');
            if (espocrmResult.id) {
              saveLeadState({ id: espocrmResult.id, ddd, celular, gclid });
            }
          }
          if (octadeskResult.success) {
            console.log('✅ [MODAL] Mensagem inicial enviada via Octadesk');
          }
          if (gtmResult.success) {
            console.log('✅ [MODAL] Conversão inicial registrada no GTM');
          }
        })
        .catch(error => {
          console.warn('⚠️ [MODAL] Erros no processamento inicial (não bloqueante)');
        });
      }
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
  
  $form.on('submit', async function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    console.log('🎯 [MODAL] Submit do formulário');
    
    // Validar DDD + Celular (obrigatórios)
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
    dados.DDD = ddd;
    dados.GCLID = getGCLID();
    
    console.log('📋 [MODAL] Dados coletados:', {
      has_ddd: !!dados.DDD,
      has_celular: !!dados.CELULAR,
      has_cpf: !!dados.CPF,
      has_nome: !!dados.NOME,
      has_placa: !!dados.PLACA,
      has_cep: !!dados.CEP
    });
    
    // ✅ V2: Verificar se há dados novos para atualizar
    const hasNewData = !!(dados.CPF || dados.NOME || dados.CEP || dados.PLACA);
    
    if (hasNewData) {
      // Tentar recuperar ID do lead anterior
      const previousState = getLeadState();
      const espocrmId = previousState?.lead_id || null;
      
      console.log('🔄 [MODAL] Atualizando lead com dados adicionais...');
      
      logEvent('whatsapp_modal_submit_update_attempt', {
        has_cpf: !!dados.CPF,
        has_nome: !!dados.NOME,
        has_placa: !!dados.PLACA
      }, 'info');
      
      // Atualizar lead (não bloqueante)
      atualizarLeadEspoCRM(dados, espocrmId)
        .then(result => {
          if (result.success) {
            console.log('✅ [MODAL] Lead atualizado com sucesso');
            logEvent('whatsapp_modal_espocrm_update_final_success', {}, 'info');
          } else {
            console.warn('⚠️ [MODAL] Erro ao atualizar lead (não bloqueante):', result.error);
            logEvent('whatsapp_modal_espocrm_update_final_failed', { error: result.error }, 'warning');
          }
        })
        .catch(error => {
          console.warn('⚠️ [MODAL] Erro ao atualizar lead (não bloqueante)');
          logEvent('whatsapp_modal_espocrm_update_exception', { error: error.message }, 'error');
        });
    } else {
      console.log('ℹ️ [MODAL] Nenhum dado novo para atualizar');
      logEvent('whatsapp_modal_submit_no_new_data', {}, 'info');
    }
    
    // Sempre abrir WhatsApp (não bloqueado por atualização)
    console.log('✅ [MODAL] Abrindo WhatsApp');
    
    logEvent('whatsapp_modal_submit_success', {
      has_new_data: hasNewData
    }, 'info');
    
    $modal.fadeOut(300, function() {
      openWhatsApp(dados);
    });
  });
  
  console.log('✅ [MODAL] Sistema de modal WhatsApp Definitivo inicializado');
  console.log('🌍 [MODAL] Ambiente detectado:', isDevelopmentEnvironment() ? 'DESENVOLVIMENTO' : 'PRODUÇÃO');
  console.log('📊 [MODAL] Versão: V2.0 - Fluxo Otimizado (Registro Inicial Paralelo)');
  
  logEvent('whatsapp_modal_initialized', {
    environment: isDevelopmentEnvironment() ? 'dev' : 'prod',
    version: '2.0'
  }, 'info');
  
});




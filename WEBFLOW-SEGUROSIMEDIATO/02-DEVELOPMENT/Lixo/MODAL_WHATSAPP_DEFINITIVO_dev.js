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
      email: '#EMAIL-MODAL',
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
    const hostname = window.location.hostname;
    const href = window.location.href;
    
    // SOLUÇÃO DEFINITIVA: HARDCODE para webflow.io (SEMPRE desenvolvimento)
    if (hostname.indexOf('webflow.io') !== -1) {
      console.log('✅ [ENV] Hardcode DEV: webflow.io detectado');
      return true;
    }
    
    // Verificações padrão para outros ambientes
    if (hostname.includes('dev.') || 
        hostname.includes('localhost') ||
        hostname.includes('127.0.0.1')) {
      console.log('✅ [ENV] DEV via hostname padrão');
      return true;
    }
    
    if (href.includes('/dev/')) {
      console.log('✅ [ENV] DEV via URL path');
      return true;
    }
    
    // Parâmetro GET para forçar dev
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('env') === 'dev' || urlParams.get('dev') === '1') {
      console.log('✅ [ENV] DEV via parâmetro GET');
      return true;
    }
    
    // Variável global
    if (typeof window.ENVIRONMENT !== 'undefined' && window.ENVIRONMENT === 'development') {
      console.log('✅ [ENV] DEV via variável global');
      return true;
    }
    
    console.log('❌ [ENV] PRODUÇÃO detectado');
    return false;
  }
  
  /**
   * Obter URL do endpoint baseado no ambiente
   * @param {string} endpoint - 'travelangels' ou 'octadesk'
   * @returns {string} URL do endpoint
   */
  function getEndpointUrl(endpoint) {
    const hostname = window.location.hostname;
    
    // SOLUÇÃO DEFINITIVA: FORÇAR _dev para webflow.io SEMPRE
    if (hostname.indexOf('webflow.io') !== -1) {
      console.log('✅ [ENDPOINT] FORÇANDO DEV para webflow.io');
      const devEndpoints = {
        travelangels: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
        octadesk: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php'
      };
      const url = devEndpoints[endpoint];
      console.log('🌍 [ENDPOINT] URL FORÇADA (webflow.io):', url);
      return url;
    }
    
    // Para outros ambientes, usar detecção normal
    const isDev = isDevelopmentEnvironment();
    
    const endpoints = {
      travelangels: {
        dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
        prod: 'https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php' // ✅ V2: Endpoint paralelo
      },
      octadesk: {
        dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php',
        prod: 'https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php' // ✅ V2: Endpoint paralelo
      }
    };
    
    const env = isDev ? 'dev' : 'prod';
    let url = endpoints[endpoint][env];
    
    // LOGS DETALHADOS
    console.log('🌍 [ENDPOINT] hostname:', hostname);
    console.log('🌍 [ENDPOINT] isDev:', isDev);
    console.log('🌍 [ENDPOINT] env:', env);
    console.log('🌍 [ENDPOINT] URL escolhida:', url);
    console.log('🌍 [ENDPOINT] tem _dev?', url.includes('_dev') ? 'SIM ✅' : 'NÃO ❌');
    
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
   * Sistema de logging detalhado para debug (V3)
   * @param {string} category - Categoria do log ('ESPOCRM', 'OCTADESK', 'GTM', 'STATE', 'ERROR', 'PARALLEL', 'VALIDATION')
   * @param {string} action - Ação sendo executada
   * @param {Object} data - Dados detalhados
   * @param {string} level - Nível do log ('info', 'warn', 'error', 'debug')
   */
  function debugLog(category, action, data = {}, level = 'info') {
    // Verificar se categoria está habilitada (se configurado)
    if (window.DEBUG_LOG_CONFIG && !window.DEBUG_LOG_CONFIG[category]) {
      return; // Não logar esta categoria
    }
    
    const timestamp = new Date().toISOString();
    const environment = isDevelopmentEnvironment() ? '🔧 DEV' : '🚀 PROD';
    
    // Emoji por categoria
    const categoryEmojis = {
      'ESPOCRM': '📊',
      'OCTADESK': '📱',
      'GTM': '📈',
      'STATE': '💾',
      'ERROR': '❌',
      'PARALLEL': '⚡',
      'VALIDATION': '✅'
    };
    
    const emoji = categoryEmojis[category] || '📝';
    
    // Formatar dados para exibição
    const formattedData = {
      timestamp,
      environment,
      category,
      action,
      ...data
    };
  
    // Adicionar JSON stringificado se houver objetos complexos
    if (data.payload) {
      formattedData.payload_json = JSON.stringify(data.payload, null, 2);
    }
    if (data.event_data) {
      formattedData.event_data_json = JSON.stringify(data.event_data, null, 2);
    }
    if (data.response_data) {
      formattedData.response_data_json = JSON.stringify(data.response_data, null, 2);
    }
    if (data.dados_complete || data.dados) {
      formattedData.dados_json = JSON.stringify(data.dados_complete || data.dados, null, 2);
    }
    
    // Log formatado no console
    const logMessage = `${emoji} [${category}] ${action}`;
    
    // Escolher método de log baseado no nível
    switch(level) {
      case 'error':
        console.error(logMessage, formattedData);
        break;
      case 'warn':
        console.warn(logMessage, formattedData);
        break;
      case 'debug':
        console.debug(logMessage, formattedData);
        break;
      default:
        console.log(logMessage, formattedData);
    }
    
    // Se disponível, enviar para sistema de logging
    try {
      if (typeof window.logDebug === 'function') {
        window.logDebug(level.toUpperCase(), `[MODAL V3] ${category} - ${action}`, formattedData);
      }
    } catch (e) {
      // Falha silenciosa
    }
  }
  
  // Configuração opcional de logging por categoria (padrão: todas habilitadas)
  if (typeof window.DEBUG_LOG_CONFIG === 'undefined') {
    window.DEBUG_LOG_CONFIG = {
      ESPOCRM: true,
      OCTADESK: true,
      GTM: true,
      STATE: true,
      PARALLEL: true,
      VALIDATION: true,
      ERROR: true
    };
  }
  
  /**
   * Gerenciamento de estado do lead (localStorage)
   */
  function saveLeadState(leadData) {
    const state = {
      lead_id: leadData.id || leadData.lead_id || null,
      opportunity_id: leadData.opportunity_id || leadData.opportunityId || null,
      ddd: leadData.ddd,
      celular: onlyDigits(leadData.celular),
      gclid: leadData.gclid || '',
      timestamp: Date.now(),
      expires: Date.now() + (30 * 60 * 1000) // 30 minutos
    };
    
    try {
      localStorage.setItem('whatsapp_modal_lead_state', JSON.stringify(state));
      console.log('💾 [MODAL] Estado do lead salvo:', { 
        lead_id: state.lead_id, 
        opportunity_id: state.opportunity_id,
        ddd: state.ddd 
      });
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
    const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
    const celular = $(MODAL_CONFIG.fieldIds.celular).val();
    const emailField = $(MODAL_CONFIG.fieldIds.email).val();
    
    // Gerar email automaticamente se campo estiver vazio
    let email = emailField;
    if (!email && ddd && celular) {
      email = ddd + onlyDigits(celular) + '@imediatoseguros.com.br';
    }
    
    // ✅ LOG PARA DEBUG - verificar se email está sendo gerado
    console.log('🔍 [DEBUG] Email generation:', {
      ddd: ddd,
      celular: celular,
      emailField: emailField,
      emailGenerated: email,
      hasEmail: !!email
    });
    
    // ✅ LOG ADICIONAL - verificar se função está sendo chamada
    console.log('🔍 [DEBUG] coletarTodosDados() executada - dados coletados:', {
      TELEFONE: ddd + celular,
      DDD: ddd,
      CELULAR: celular,
      EMAIL: email,
      CPF: $(MODAL_CONFIG.fieldIds.cpf).val() || '',
      NOME: $(MODAL_CONFIG.fieldIds.nome).val() || ''
    });
    
    // ✅ LOG CRÍTICO - verificar se email está sendo enviado
    console.log('🔍 [DEBUG] Email sendo enviado para EspoCRM:', email);
    
    return {
      TELEFONE: ddd + celular,
      DDD: ddd,
      CELULAR: celular,
      CPF: $(MODAL_CONFIG.fieldIds.cpf).val() || '',
      NOME: $(MODAL_CONFIG.fieldIds.nome).val() || '',
      EMAIL: email || '',
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
  
  // ==================== FUNÇÕES DE NOTIFICAÇÃO EMAIL ====================
  
  /**
   * Identifica em qual momento o modal está sendo processado
   * Baseado no payload enviado pelo modal ao add_flyingdonkeys_v2.php
   * 
   * @param {Object} payload - Payload enviado pelo modal ao add_flyingdonkeys_v2.php
   * @param {boolean} isError - Se true, indica que houve erro na chamada
   * @returns {Object} Objeto com informações do momento
   */
  function identifyModalMoment(payload, isError = false) {
    try {
      const name = payload.name || '';
      const nome = (payload.data && payload.data.NOME) || '';
      const cpf = (payload.data && payload.data.CPF) || '';
      const cep = (payload.data && payload.data.CEP) || '';
      const placa = (payload.data && payload.data.PLACA) || '';
      
      // Verificar pelo campo 'name'
      const isInitialByName = name.includes('Primeiro Contato') || name.includes('Mensagem Inicial');
      
      // Verificar pelo padrão do nome (INITIAL tem padrão especial)
      const isInitialPattern = /^\d{2}-\d{9}-NOVO CLIENTE WHATSAPP$/.test(nome);
      
      // Verificar se campos obrigatórios estão vazios (INITIAL tem apenas telefone)
      const camposVazios = !cpf && !cep && !placa;
      
      // Determinar tipo base (INITIAL ou UPDATE)
      const isInitial = isInitialByName || isInitialPattern || camposVazios;
      
      // Se houver erro, usar identificadores de erro (sem prefixo "ERRO -" na descrição)
      if (isError) {
        return {
          moment: isInitial ? 'initial_error' : 'update_error',
          emoji: isInitial ? '📞' : '❌', // Primeira mensagem: telefone azul, segunda: erro vermelho
          color: '🔴',
          color_name: 'VERMELHO',
          description: isInitial 
            ? 'Primeiro Contato - Apenas Telefone' 
            : 'Submissão Completa - Todos os Dados',
          banner_color: '#F44336'
        };
      }
      
      // Lógica de identificação (SUCESSO)
      if (isInitial) {
        // MOMENTO 1: INITIAL (SUCESSO)
        return {
          moment: 'initial',
          emoji: '📞',
          color: '🔵',
          color_name: 'AZUL',
          description: 'Primeiro Contato - Apenas Telefone',
          banner_color: '#2196F3'
        };
      } else {
        // MOMENTO 2: UPDATE (SUCESSO)
        return {
          moment: 'update',
          emoji: '✅',
          color: '🟢',
          color_name: 'VERDE',
          description: 'Submissão Completa - Todos os Dados',
          banner_color: '#4CAF50'
        };
      }
    } catch (error) {
      console.error('❌ [EMAIL] Erro ao identificar momento:', error);
      // Default: assumir UPDATE com erro (mais seguro)
      return {
        moment: 'update_error',
        emoji: '❌',
        color: '🔴',
        color_name: 'VERMELHO',
        description: 'Submissão Completa - Todos os Dados',
        banner_color: '#F44336'
      };
    }
  }
  
  /**
   * Envia notificação por email aos administradores
   * Chamada após sucesso OU erro nas respostas do add_flyingdonkeys_v2.php
   * 
   * @param {Object} modalPayload - Payload original enviado pelo modal
   * @param {Object} responseData - Resposta do add_flyingdonkeys_v2.php (pode ser sucesso ou erro)
   * @param {Object} errorInfo - Informações do erro (se houver): { message, status, code }
   * @returns {Promise<Object>} Resultado do envio de email
   */
  async function sendAdminEmailNotification(modalPayload, responseData, errorInfo = null) {
    try {
      // Identificar se houve erro
      // Regras claras:
      // 1. Se errorInfo foi passado explicitamente, é ERRO
      // 2. Se responseData existe e responseData.success === true, é SUCESSO (não erro)
      // 3. Se responseData existe e responseData.success === false, é ERRO
      // 4. Se responseData.success não está definido mas há contact_id/lead_id, é SUCESSO
      // 5. Se responseData é null/undefined e não há errorInfo explícito, assumir SUCESSO (caso padrão)
      const isError = errorInfo !== null || 
        (responseData && (
          responseData.success === false || 
          (responseData.success !== true && !responseData.contact_id && !responseData.lead_id && !responseData.id)
        ));
      
      // Identificar momento (com flag de erro)
      const modalMoment = identifyModalMoment(modalPayload, isError);
      
      // Extrair dados do payload do modal
      const data = modalPayload.data || {};
      const ddd = data['DDD-CELULAR'] || '';
      const celular = data['CELULAR'] || '';
      const nome = data['NOME'] || 'Não informado';
      const cpf = data['CPF'] || 'Não informado';
      const cep = data['CEP'] || 'Não informado';
      const placa = data['PLACA'] || 'Não informado';
      const email = data['Email'] || 'Não informado';
      const gclid = data['GCLID_FLD'] || 'Não informado';
      
      // Validar dados mínimos
      if (!ddd || !celular) {
        console.warn('📧 [EMAIL] Dados insuficientes para enviar email - DDD ou celular ausente');
        return {
          success: false,
          error: 'DDD e celular são obrigatórios'
        };
      }
      
      // Preparar dados para endpoint de email
      const emailPayload = {
        ddd: ddd,
        celular: celular,
        cpf: cpf,
        nome: nome,
        email: email,
        cep: cep,
        placa: placa,
        gclid: gclid,
        momento: modalMoment.moment,
        momento_descricao: modalMoment.description,
        momento_emoji: modalMoment.emoji,
        // Informações de erro (se houver)
        erro: errorInfo ? {
          message: errorInfo.message || 'Erro desconhecido',
          status: errorInfo.status || null,
          code: errorInfo.code || null,
          response_data: errorInfo.responseData || null
        } : null
      };
      
      // Determinar URL do endpoint (dev ou prod)
      const isDev = isDevelopmentEnvironment();
      const emailEndpoint = isDev 
        ? 'https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php'
        : 'https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php';
      
      // Log antes do envio
      console.log(`${modalMoment.emoji} [EMAIL-${modalMoment.color_name}] Enviando notificação ${modalMoment.description}`);
      
      // Fazer chamada para endpoint de email
      const response = await fetch(emailEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Modal-WhatsApp-EmailNotification-v1.0'
        },
        body: JSON.stringify(emailPayload)
      });
      
      // Verificar se a resposta é JSON válido antes de fazer parse
      let result;
      const contentType = response.headers.get('content-type');
      const responseText = await response.text();
      
      if (contentType && contentType.includes('application/json')) {
        try {
          result = responseText ? JSON.parse(responseText) : { success: false, error: 'Resposta vazia' };
        } catch (parseError) {
          console.error('❌ [EMAIL-ERRO] Erro ao parsear resposta JSON:', parseError);
          console.error('❌ [EMAIL-ERRO] Resposta recebida:', responseText.substring(0, 500));
          return {
            success: false,
            error: 'Erro ao processar resposta do servidor: ' + parseError.message
          };
        }
      } else {
        console.error(`❌ [EMAIL-ERRO] Resposta não é JSON. Status: ${response.status}, Tipo: ${contentType}, Texto: ${responseText.substring(0, 200)}`);
        return {
          success: false,
          error: `Resposta inválida do servidor (Status: ${response.status})`
        };
      }
      
      // Log do resultado
      if (result.success) {
        // Se o email foi enviado com sucesso, mas o conteúdo é sobre erro, deixar claro
        const statusTipo = isError ? 'ERRO' : 'SUCESSO';
        console.log(`📧 [EMAIL-ENVIADO] Notificação de ${statusTipo} enviada com SUCESSO: ${modalMoment.description}`);
      } else {
        console.error(`❌ [EMAIL-FALHA] Falha ao enviar notificação ${modalMoment.description}:`, result.error || 'Erro desconhecido');
      }
      
      return result;
      
    } catch (error) {
      console.error('❌ [EMAIL-EXCEPTION] Erro ao enviar notificação:', error);
      return {
        success: false,
        error: error.message
      };
    }
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
    const phoneKey = `${ddd}${onlyDigits(celular)}`;
    
    // ✅ V3: Log de rate limiting
    debugLog('ESPOCRM', 'RATE_LIMIT_CHECK', {
      phone_key: phoneKey,
      can_make_call: rateLimiter.canMakeCall(phoneKey)
    }, 'debug');
    
    if (!rateLimiter.canMakeCall(phoneKey)) {
      debugLog('ESPOCRM', 'RATE_LIMIT_EXCEEDED', {
        phone_key: phoneKey,
        message: 'Muitas tentativas recentes, aguarde...'
      }, 'warn');
      return { success: false, error: 'rate_limit' };
    }
    
    // ✅ FORMATO COMPATÍVEL COM RPA/PRODUÇÃO: estrutura com 'data' como objeto
    // Mantém compatibilidade com add_travelangels.php que processa $data['data']
    // IMPORTANTE: garantir que landing_url seja string simples, não objeto
    const landingUrl = String(window.location.href || '');
    const webhook_data = {
      data: {
        'DDD-CELULAR': String(ddd || ''),
        'CELULAR': String(onlyDigits(celular) || ''),
        'GCLID_FLD': String(gclid || ''),
        'NOME': String(`${ddd}-${onlyDigits(celular)}-NOVO CLIENTE WHATSAPP`),
        'CPF': '',
        'CEP': '',
        'PLACA': '',
        'Email': ddd && celular ? `${ddd}${onlyDigits(celular)}@imediatoseguros.com.br` : '',
        'produto': 'seguro-auto',
        'landing_url': landingUrl,
        'utm_source': String(getUtmParam('utm_source') || ''),
        'utm_campaign': String(getUtmParam('utm_campaign') || '')
      },
      d: new Date().toISOString(),
      name: 'Modal WhatsApp - Primeiro Contato (V2)'
    };
    
    // ✅ GARANTIR que 'data' seja um objeto, não string
    if (typeof webhook_data.data === 'string') {
      console.error('❌ [CRÍTICO] webhook_data.data é STRING! Corrigindo...');
      try {
        webhook_data.data = JSON.parse(webhook_data.data);
      } catch (e) {
        console.error('❌ [CRÍTICO] Erro ao parsear data:', e);
      }
    }
    
    const endpointUrl = getEndpointUrl('travelangels');
    
    // ✅ V3: LOG COMPLETO ANTES DA CHAMADA
    const jsonBodyForLog = JSON.stringify(webhook_data);
    debugLog('ESPOCRM', 'INITIAL_REQUEST_PREPARATION', {
      endpoint_url: endpointUrl,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v2.0'
      },
      payload: webhook_data,
      payload_json_stringified: jsonBodyForLog,
      input_data: {
        ddd: ddd,
        celular: '***' + onlyDigits(celular).slice(-4),
        gclid: gclid || '(vazio)',
        gclid_length: (gclid || '').length
      },
      rate_limiting: {
        phone_key: phoneKey,
        can_make_call: true
      }
    }, 'info');
    
    logEvent('whatsapp_modal_espocrm_initial_attempt', { ddd, celular: '***' }, 'info');
    
    debugLog('ESPOCRM', 'INITIAL_REQUEST_STARTING', {
      endpoint_url: endpointUrl,
      attempt: 1,
      max_retries: 2
    }, 'info');
    
    // ✅ DEBUG: Serializar JSON e verificar formato ANTES do envio
    const jsonBody = JSON.stringify(webhook_data);
    console.log('🔍 [DEBUG JSON] Objeto webhook_data original:', webhook_data);
    console.log('🔍 [DEBUG JSON] JSON serializado (JSON.stringify):', jsonBody);
    console.log('🔍 [DEBUG JSON] Tipo do campo data:', typeof webhook_data.data);
    console.log('🔍 [DEBUG JSON] Data é objeto?', webhook_data.data instanceof Object && !Array.isArray(webhook_data.data));
    console.log('🔍 [DEBUG JSON] Tamanho do JSON:', jsonBody.length, 'caracteres');
    
    // ✅ DEBUG: Validar JSON manualmente
    try {
      const testParse = JSON.parse(jsonBody);
      console.log('✅ [DEBUG JSON] JSON válido - pode fazer parse:', testParse.data ? 'Data presente' : 'Data ausente');
    } catch (e) {
      console.error('❌ [DEBUG JSON] JSON INVÁLIDO:', e.message);
    }
    
    try {
      const result = await fetchWithRetry(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Modal-WhatsApp-v2.0'
        },
        body: jsonBody
      }, 2, 1000);
      
      // ✅ V3: LOG DA RESPOSTA
      debugLog('ESPOCRM', 'INITIAL_RESPONSE_RECEIVED', {
        success: result.success,
        attempt: result.attempt + 1,
        http_status: result.response?.status || 'N/A',
        has_response_data: !!result.response,
        error: result.error || null
      }, result.success ? 'info' : 'warn');
      
      if (result.success && result.response) {
        try {
          const responseData = await result.response.json();
          
          // ✅ V3: LOG DA RESPOSTA PARSEADA
          debugLog('ESPOCRM', 'INITIAL_RESPONSE_PARSED', {
            response_data: responseData,
            lead_id: responseData.contact_id || responseData.lead_id || responseData.data?.leadIdFlyingDonkeys || null,
            success: responseData.success || result.response.ok
          }, 'info');
          
          if (responseData.success || result.response.ok) {
            const leadId = responseData.contact_id || responseData.lead_id || responseData.data?.leadIdFlyingDonkeys || null;
            const opportunityId = responseData.opportunity_id || responseData.data?.opportunityIdFlyingDonkeys || null;
            
            if (leadId) {
              saveLeadState({ 
                id: leadId, 
                lead_id: leadId,
                opportunity_id: opportunityId,
                opportunityId: opportunityId,
                ddd, 
                celular, 
                gclid 
              });
              
              // ✅ V3: LOG DO ESTADO SALVO
              debugLog('STATE', 'LEAD_STATE_SAVED', {
                lead_id: leadId,
                opportunity_id: opportunityId || '(não fornecido)',
                ddd: ddd,
                celular: '***' + onlyDigits(celular).slice(-4),
                gclid: gclid || '(vazio)',
                localStorage_key: 'whatsapp_modal_lead_state'
              }, 'info');
            }
            
            logEvent('whatsapp_modal_espocrm_initial_success', { 
              lead_id: leadId, 
              opportunity_id: opportunityId 
            }, 'info');
            
            // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS SUCESSO (INITIAL)
            // Enviar email de forma assíncrona (não bloquear o retorno)
            sendAdminEmailNotification(webhook_data, responseData)
              .catch(error => {
                console.error('❌ [EMAIL] Erro ao enviar email (não bloqueante):', error);
              });
            
            return { success: true, id: leadId, opportunity_id: opportunityId, attempt: result.attempt + 1 };
          } else {
            console.warn('⚠️ [MODAL] Erro ao criar lead no EspoCRM:', responseData);
            logEvent('whatsapp_modal_espocrm_initial_failed', { error: responseData }, 'warning');
            
            // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO (INITIAL)
            // Enviar email de forma assíncrona (não bloquear o retorno)
            sendAdminEmailNotification(webhook_data, responseData, {
              message: responseData.error || responseData.message || 'Erro ao criar lead no EspoCRM',
              status: null,
              code: null,
              responseData: responseData
            })
              .catch(error => {
                console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
              });
            
            return { success: false, error: responseData, attempt: result.attempt + 1 };
          }
        } catch (parseError) {
          debugLog('ESPOCRM', 'INITIAL_RESPONSE_PARSE_ERROR', {
            error: parseError.message,
            response_ok: result.response.ok,
            response_status: result.response.status
          }, 'warn');
          
          // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO DE PARSE (INITIAL)
          sendAdminEmailNotification(webhook_data, null, {
            message: parseError.message || 'Erro ao parsear resposta do EspoCRM',
            status: result.response?.status || null,
            code: null,
            responseData: null
          })
            .catch(error => {
              console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
            });
          
          return { success: result.response.ok, attempt: result.attempt + 1 };
        }
      } else {
        const errorMsg = result.error?.message || 'Erro desconhecido';
        debugLog('ESPOCRM', 'INITIAL_REQUEST_ERROR', {
          error: errorMsg,
          attempt: result.attempt + 1
        }, 'error');
        
        // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO DE REQUEST (INITIAL)
        sendAdminEmailNotification(webhook_data, null, {
          message: errorMsg || 'Erro desconhecido na requisição',
          status: null,
          code: null,
          responseData: null
        })
          .catch(error => {
            console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
          });
        
        return { success: false, error: errorMsg, attempt: result.attempt + 1 };
      }
    } catch (error) {
      debugLog('ERROR', 'ESPOCRM_INITIAL_EXCEPTION', {
        error_message: error.message,
        error_stack: error.stack,
        error_name: error.name
      }, 'error');
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
        
        // ✅ V3: LOG DA RECUPERAÇÃO DO ESTADO
        debugLog('STATE', 'LEAD_ID_RECOVERED', {
          lead_id: espocrmId,
          source: 'localStorage',
          previous_state: previousState
        }, 'info');
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
      
      // ✅ V4: Incluir opportunity_id se disponível no estado
      const previousState = getLeadState();
      if (previousState && previousState.opportunity_id) {
        webhook_data.data.opportunity_id = previousState.opportunity_id;
        
        debugLog('ESPOCRM', 'OPPORTUNITY_ID_INCLUDED', {
          opportunity_id: previousState.opportunity_id,
          lead_id: espocrmId
        }, 'info');
      }
    }
    
    const endpointUrl = getEndpointUrl('travelangels');
    
    // ✅ V3: LOG COMPLETO ANTES DA ATUALIZAÇÃO
    debugLog('ESPOCRM', 'UPDATE_REQUEST_PREPARATION', {
      endpoint_url: endpointUrl,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v2.0'
      },
      payload: webhook_data,
      lead_id: espocrmId || '(não fornecido)',
      has_lead_id: !!espocrmId,
      input_data_summary: {
        has_nome: !!dados.NOME,
        has_cpf: !!dados.CPF,
        has_cep: !!dados.CEP,
        has_placa: !!dados.PLACA,
        has_email: !!dados.EMAIL,
        ddd: dados.DDD || '',
        celular: dados.CELULAR ? '***' + onlyDigits(dados.CELULAR).slice(-4) : ''
      }
    }, 'info');
    
    logEvent('whatsapp_modal_espocrm_update_attempt', { 
      has_lead_id: !!espocrmId,
      has_cpf: !!dados.CPF,
      has_nome: !!dados.NOME 
    }, 'info');
    
    try {
      const result = await fetchWithRetry(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Modal-WhatsApp-v2.0'
        },
        body: JSON.stringify(webhook_data)
      }, 2, 1000);
      
      // ✅ V3: LOG DA RESPOSTA DE ATUALIZAÇÃO
      debugLog('ESPOCRM', 'UPDATE_RESPONSE_RECEIVED', {
        success: result.success,
        attempt: result.attempt + 1,
        http_status: result.response?.status || 'N/A',
        has_response_data: !!result.response,
        error: result.error || null
      }, result.success ? 'info' : 'warn');
      
      if (result.success && result.response) {
        try {
          const responseData = await result.response.json();
          
          // ✅ V3: LOG DA RESPOSTA PARSEADA DE ATUALIZAÇÃO
          debugLog('ESPOCRM', 'UPDATE_RESPONSE_PARSED', {
            response_data: responseData,
            success: result.response.ok
          }, 'info');
          
          logEvent('whatsapp_modal_espocrm_update_success', { attempt: result.attempt + 1 }, 'info');
          
          // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS SUCESSO (UPDATE)
          // Enviar email de forma assíncrona (não bloquear o retorno)
          sendAdminEmailNotification(webhook_data, responseData)
            .catch(error => {
              console.error('❌ [EMAIL] Erro ao enviar email (não bloqueante):', error);
            });
          
          return { success: true, result: responseData, attempt: result.attempt + 1 };
        } catch (parseError) {
          debugLog('ESPOCRM', 'UPDATE_RESPONSE_PARSE_ERROR', {
            error: parseError.message
          }, 'warn');
          logEvent('whatsapp_modal_espocrm_update_parse_error', { error: parseError.message }, 'warning');
          
          // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO DE PARSE (UPDATE)
          sendAdminEmailNotification(webhook_data, null, {
            message: parseError.message || 'Erro ao parsear resposta do EspoCRM',
            status: result.response?.status || null,
            code: null,
            responseData: null
          })
            .catch(error => {
              console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
            });
          
          return { success: result.response.ok, attempt: result.attempt + 1 };
        }
      } else {
        const errorMsg = result.error?.message || 'Erro desconhecido';
        debugLog('ESPOCRM', 'UPDATE_REQUEST_ERROR', {
          error: errorMsg,
          attempt: result.attempt + 1
        }, 'error');
        logEvent('whatsapp_modal_espocrm_update_error', { error: errorMsg, attempt: result.attempt + 1 }, 'error');
        
        // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO DE REQUEST (UPDATE)
        sendAdminEmailNotification(webhook_data, null, {
          message: errorMsg || 'Erro desconhecido na requisição',
          status: null,
          code: null,
          responseData: null
        })
          .catch(error => {
            console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
          });
        
        return { success: false, error: errorMsg, attempt: result.attempt + 1 };
      }
    } catch (error) {
      debugLog('ERROR', 'ESPOCRM_UPDATE_EXCEPTION', {
        error_message: error.message,
        error_stack: error.stack
      }, 'error');
      logEvent('whatsapp_modal_espocrm_update_exception', { error: error.message }, 'error');
      
      // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS EXCEÇÃO (UPDATE)
      sendAdminEmailNotification(webhook_data, null, {
        message: error.message || 'Exceção ao atualizar lead',
        status: null,
        code: null,
        responseData: null
      })
        .catch(emailError => {
          console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', emailError);
        });
      
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
    
    const endpointUrl = getEndpointUrl('octadesk');
    
    // ✅ V3: LOG COMPLETO ANTES DA CHAMADA OCTADESK
    debugLog('OCTADESK', 'INITIAL_REQUEST_PREPARATION', {
      endpoint_url: endpointUrl,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v2.0'
      },
      payload: webhook_data,
      input_data: {
        ddd: ddd,
        celular: '***' + onlyDigits(celular).slice(-4),
        gclid: gclid || '(vazio)'
      }
    }, 'info');
    
    logEvent('whatsapp_modal_octadesk_initial_attempt', { has_celular: !!celular }, 'info');
    
    debugLog('OCTADESK', 'INITIAL_REQUEST_STARTING', {
      endpoint_url: endpointUrl,
      attempt: 1,
      max_retries: 2
    }, 'info');
    
    try {
      const result = await fetchWithRetry(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Modal-WhatsApp-v2.0'
        },
        body: JSON.stringify(webhook_data)
      }, 2, 1000);
      
      // ✅ V3: LOG DA RESPOSTA OCTADESK
      debugLog('OCTADESK', 'INITIAL_RESPONSE_RECEIVED', {
        success: result.success,
        attempt: result.attempt + 1,
        http_status: result.response?.status || 'N/A',
        has_response_data: !!result.response,
        error: result.error || null
      }, result.success ? 'info' : 'warn');
      
      if (result.success && result.response) {
        try {
          const responseData = await result.response.json();
          
          // ✅ V3: LOG DA RESPOSTA PARSEADA OCTADESK
          debugLog('OCTADESK', 'INITIAL_RESPONSE_PARSED', {
            response_data: responseData,
            success: result.response.ok
          }, 'info');
          
          logEvent('whatsapp_modal_octadesk_initial_success', { attempt: result.attempt + 1 }, 'info');
          return { success: true, result: responseData, attempt: result.attempt + 1 };
        } catch (parseError) {
          debugLog('OCTADESK', 'INITIAL_RESPONSE_PARSE_ERROR', {
            error: parseError.message,
            response_ok: result.response.ok
          }, 'warn');
          logEvent('whatsapp_modal_octadesk_initial_parse_error', { error: parseError.message }, 'warning');
          return { success: result.response.ok, attempt: result.attempt + 1 };
        }
      } else {
        const errorMsg = result.error?.message || 'Erro desconhecido';
        debugLog('OCTADESK', 'INITIAL_REQUEST_ERROR', {
          error: errorMsg,
          attempt: result.attempt + 1
        }, 'error');
        logEvent('whatsapp_modal_octadesk_initial_error', { error: errorMsg, attempt: result.attempt + 1 }, 'error');
        return { success: false, error: errorMsg, attempt: result.attempt + 1 };
      }
    } catch (error) {
      debugLog('ERROR', 'OCTADESK_INITIAL_EXCEPTION', {
        error_message: error.message,
        error_stack: error.stack,
        error_name: error.name
      }, 'error');
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
    // ✅ V3: LOG ANTES DE CONSTRUIR DADOS GTM
    debugLog('GTM', 'DATA_PREPARATION_START', {
      ddd: ddd,
      celular: '***' + onlyDigits(celular).slice(-4),
      gclid: gclid || '(vazio)',
      dataLayer_available: typeof window.dataLayer !== 'undefined',
      gtm_variables: {
        GTM_EVENT_NAME_INITIAL: window.GTM_EVENT_NAME_INITIAL || '(não definido)',
        GTM_FORM_TYPE: window.GTM_FORM_TYPE || '(não definido)',
        GTM_CONTACT_STAGE: window.GTM_CONTACT_STAGE || '(não definido)',
        GTM_UTM_SOURCE: window.GTM_UTM_SOURCE || '(null - será preenchido)',
        GTM_UTM_CAMPAIGN: window.GTM_UTM_CAMPAIGN || '(null - será preenchido)',
        GTM_PAGE_URL: window.GTM_PAGE_URL || '(null - será preenchido)',
        GTM_PAGE_TITLE: window.GTM_PAGE_TITLE || '(null - será preenchido)'
      },
      utm_params_from_url: {
        utm_source: getUtmParam('utm_source') || '(vazio)',
        utm_campaign: getUtmParam('utm_campaign') || '(vazio)',
        utm_medium: getUtmParam('utm_medium') || '(vazio)',
        utm_term: getUtmParam('utm_term') || '(vazio)',
        utm_content: getUtmParam('utm_content') || '(vazio)'
      }
    }, 'info');
    
    if (typeof window.dataLayer === 'undefined') {
      debugLog('GTM', 'DATALAYER_UNAVAILABLE', {
        message: 'dataLayer não disponível para registro de conversão inicial',
        window_dataLayer: typeof window.dataLayer
      }, 'warn');
      logEvent('whatsapp_modal_gtm_initial_datalayer_unavailable', {}, 'warning');
      return { success: false, error: 'dataLayer_unavailable' };
    }
    
    // Construir dados do evento GTM usando variáveis configuráveis
    const gtmEventData = {
      'event': window.GTM_EVENT_NAME_INITIAL || 'whatsapp_modal_initial_contact',
      'form_type': window.GTM_FORM_TYPE || 'whatsapp_modal',
      'contact_stage': window.GTM_CONTACT_STAGE || 'initial',
      'phone_ddd': ddd || '',
      'phone_number': '***',
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
    
    // ✅ V3: LOG DO OBJETO COMPLETO QUE SERÁ ENVIADO AO GTM
    debugLog('GTM', 'EVENT_DATA_READY', {
      event_data: gtmEventData,
      event_name: gtmEventData.event,
      dataLayer_length_before: window.dataLayer.length
    }, 'info');
    
    // ✅ V3: LOG ANTES DO PUSH
    debugLog('GTM', 'PUSHING_TO_DATALAYER', {
      event_name: gtmEventData.event,
      dataLayer_length_before: window.dataLayer.length
    }, 'info');
    
    window.dataLayer.push(gtmEventData);
    
    // ✅ V3: LOG APÓS O PUSH
    debugLog('GTM', 'PUSHED_TO_DATALAYER', {
      event_name: gtmEventData.event,
      dataLayer_length_after: window.dataLayer.length,
      dataLayer_item: window.dataLayer[window.dataLayer.length - 1]
    }, 'info');
    
    logEvent('whatsapp_modal_gtm_initial_conversion', { 
      event_name: gtmEventData.event,
      has_gclid: !!gtmEventData.gclid
    }, 'info');
    
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
            
            <!-- CPF e Email na mesma linha -->
            <div style="display: flex; gap: 1.5%; margin-bottom: 20px; align-items: flex-start;">
            <!-- CPF -->
              <div class="field-group" style="flex: 1; min-width: 0;">
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
              
              <!-- Email -->
              <div class="field-group" style="flex: 1; min-width: 0;">
                <label for="EMAIL-MODAL" style="display: block; color: #003366; font-weight: 600; margin-bottom: 8px; font-size: 14px; font-family: 'Titillium Web', sans-serif;">Email</label>
                <input 
                  type="email" 
                  id="EMAIL-MODAL" 
                  name="EMAIL" 
                  placeholder="seu@email.com"
                  style="width: 100%; padding: 14px 16px; border: 2px solid #E0E0E0; border-radius: 10px; font-size: 16px; transition: all 0.3s ease; box-sizing: border-box; font-family: 'Titillium Web', sans-serif; color: #333333;" 
                />
                <small class="help-message" style="display: none; font-size: 12px; margin-top: 4px;"></small>
              </div>
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
    #whatsapp-modal input[type="tel"].field-error,
    #whatsapp-modal input[type="email"].field-error {
      border-color: #e74c3c !important;
      background-color: #fff5f5 !important;
    }
    
    #whatsapp-modal input[type="text"].field-warning,
    #whatsapp-modal input[type="tel"].field-warning,
    #whatsapp-modal input[type="email"].field-warning {
      border-color: #FFB300 !important;
      background-color: #fffbf0 !important;
    }
    
    #whatsapp-modal .help-message {
      color: #FFB300 !important;
    }
    
    #whatsapp-modal input[type="text"].field-success,
    #whatsapp-modal input[type="tel"].field-success,
    #whatsapp-modal input[type="email"].field-success {
      border-color: #27ae60 !important;
      background-color: #f0fff4 !important;
    }
    
    #whatsapp-modal input[type="text"]:focus,
    #whatsapp-modal input[type="tel"]:focus,
    #whatsapp-modal input[type="email"]:focus {
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
  // PLACA: Usa função utilitária padronizada
  if (typeof window.aplicarMascaraPlaca === 'function') {
    window.aplicarMascaraPlaca($(MODAL_CONFIG.fieldIds.placa));
  } else {
    // Fallback caso a função não esteja disponível (não deveria acontecer)
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
  }
  
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
            
            // ✅ V3: LOG DO INÍCIO DO PROCESSAMENTO PARALELO
            debugLog('PARALLEL', 'INITIAL_PROCESSING_START', {
              ddd: ddd,
              celular: '***' + onlyDigits(celular).slice(-4),
              gclid: gclid || '(vazio)',
              initialRegistrationAttempted: true,
              processes: ['EspoCRM', 'Octadesk', 'GTM'],
              strategy: 'Promise.all (paralelo)'
            }, 'info');
            
            // ✅ V3: LOG DO ESTADO ANTES DO PROCESSAMENTO
            const previousState = getLeadState();
            debugLog('STATE', 'STATE_BEFORE_PROCESSING', {
              localStorage_available: typeof(Storage) !== 'undefined',
              has_previous_state: !!previousState,
              previous_state: previousState || null,
              modal_session_id: generateSessionId()
            }, 'debug');
            
            console.log('📞 [MODAL] Processando registro inicial (paralelo): EspoCRM + Octadesk + GTM...');
            
            // PROCESSAR EM PARALELO: EspoCRM + Octadesk + GTM
            Promise.all([
              registrarPrimeiroContatoEspoCRM(ddd, celular, gclid),
              enviarMensagemInicialOctadesk(ddd, celular, gclid),
              Promise.resolve(registrarConversaoInicialGTM(ddd, celular, gclid))
            ])
            .then(([espocrmResult, octadeskResult, gtmResult]) => {
              // ✅ V3: LOG DOS RESULTADOS PARALELOS
              debugLog('PARALLEL', 'INITIAL_PROCESSING_COMPLETE', {
                espocrm: {
                  success: espocrmResult.success,
                  lead_id: espocrmResult.id || null,
                  attempt: espocrmResult.attempt || null,
                  error: espocrmResult.error || null
                },
                octadesk: {
                  success: octadeskResult.success,
                  attempt: octadeskResult.attempt || null,
                  error: octadeskResult.error || null
                },
                gtm: {
                  success: gtmResult.success,
                  event_name: gtmResult.eventData?.event || null,
                  error: gtmResult.error || null
                },
                overall_success: {
                  espocrm: espocrmResult.success,
                  octadesk: octadeskResult.success,
                  gtm: gtmResult.success
                }
              }, 'info');
              
              // Logs individuais detalhados
              if (espocrmResult.success) {
                console.log('✅ [MODAL] Lead criado no EspoCRM:', espocrmResult.id || 'sem ID');
                // ✅ V4: Preservar opportunity_id ao salvar estado (não sobrescrever)
                // O estado já foi salvo em registrarPrimeiroContatoEspoCRM com opportunity_id,
                // mas se precisar salvar novamente, preservar o opportunity_id do resultado
                if (espocrmResult.id) {
                  const currentState = getLeadState();
                  saveLeadState({ 
                    id: espocrmResult.id, 
                    lead_id: espocrmResult.id,
                    opportunity_id: espocrmResult.opportunity_id || currentState?.opportunity_id || null,
                    opportunityId: espocrmResult.opportunity_id || currentState?.opportunity_id || null,
                    ddd, 
                    celular, 
                    gclid 
                  });
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
              // ✅ V3: LOG DE ERRO NO PROCESSAMENTO PARALELO
              debugLog('ERROR', 'PARALLEL_PROCESSING_EXCEPTION', {
                error_message: error.message,
                error_stack: error.stack,
                error_name: error.name
              }, 'error');
              
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
        
        // ✅ V3: LOG DO INÍCIO DO PROCESSAMENTO PARALELO (sem API)
        debugLog('PARALLEL', 'INITIAL_PROCESSING_START', {
          ddd: ddd,
          celular: '***' + onlyDigits(celular).slice(-4),
          gclid: gclid || '(vazio)',
          initialRegistrationAttempted: true,
          processes: ['EspoCRM', 'Octadesk', 'GTM'],
          strategy: 'Promise.all (paralelo - sem API validation)'
        }, 'info');
        
        // ✅ V3: LOG DO ESTADO ANTES DO PROCESSAMENTO
        const previousState = getLeadState();
        debugLog('STATE', 'STATE_BEFORE_PROCESSING', {
          localStorage_available: typeof(Storage) !== 'undefined',
          has_previous_state: !!previousState,
          previous_state: previousState || null,
          modal_session_id: generateSessionId()
        }, 'debug');
        
        console.log('📞 [MODAL] Processando registro inicial (paralelo): EspoCRM + Octadesk + GTM (sem API)...');
        
        // PROCESSAR EM PARALELO: EspoCRM + Octadesk + GTM
        Promise.all([
          registrarPrimeiroContatoEspoCRM(ddd, celular, gclid),
          enviarMensagemInicialOctadesk(ddd, celular, gclid),
          Promise.resolve(registrarConversaoInicialGTM(ddd, celular, gclid))
        ])
        .then(([espocrmResult, octadeskResult, gtmResult]) => {
          // ✅ V3: LOG DOS RESULTADOS PARALELOS
          debugLog('PARALLEL', 'INITIAL_PROCESSING_COMPLETE', {
            espocrm: {
              success: espocrmResult.success,
              lead_id: espocrmResult.id || null,
              attempt: espocrmResult.attempt || null,
              error: espocrmResult.error || null
            },
            octadesk: {
              success: octadeskResult.success,
              attempt: octadeskResult.attempt || null,
              error: octadeskResult.error || null
            },
            gtm: {
              success: gtmResult.success,
              event_name: gtmResult.eventData?.event || null,
              error: gtmResult.error || null
            },
            overall_success: {
              espocrm: espocrmResult.success,
              octadesk: octadeskResult.success,
              gtm: gtmResult.success
            }
          }, 'info');
          
          if (espocrmResult.success) {
            console.log('✅ [MODAL] Lead criado no EspoCRM:', espocrmResult.id || 'sem ID');
            // ✅ V4: Preservar opportunity_id ao salvar estado (não sobrescrever)
            if (espocrmResult.id) {
              const currentState = getLeadState();
              saveLeadState({ 
                id: espocrmResult.id, 
                lead_id: espocrmResult.id,
                opportunity_id: espocrmResult.opportunity_id || currentState?.opportunity_id || null,
                opportunityId: espocrmResult.opportunity_id || currentState?.opportunity_id || null,
                ddd, 
                celular, 
                gclid 
              });
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
          // ✅ V3: LOG DE ERRO NO PROCESSAMENTO PARALELO
          debugLog('ERROR', 'PARALLEL_PROCESSING_EXCEPTION', {
            error_message: error.message,
            error_stack: error.stack,
            error_name: error.name
          }, 'error');
          
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
  
  // EMAIL → valida formato de email
  $(MODAL_CONFIG.fieldIds.email).on('blur', function() {
    const email = $(this).val();
    clearFieldStatus($(this));
    
    if (!email) return;
    
    // Regex básico - suficiente para volumes baixos (empresa pequena)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      showFieldWarning($(this), 'Email inválido');
      return;
    }
    
    showFieldSuccess($(this));
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
    
    // Validar DDD + Celular (obrigatórios)
    const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
    const celular = $(MODAL_CONFIG.fieldIds.celular).val();
    
    // ✅ V3: LOG DO INÍCIO DO SUBMIT
    debugLog('VALIDATION', 'SUBMIT_START', {
      ddd: ddd,
      celular: '***' + onlyDigits(celular).slice(-4),
      ddd_valid: onlyDigits(ddd).length === 2,
      celular_valid: onlyDigits(celular).length === 9
    }, 'info');
    
    if (!ddd || onlyDigits(ddd).length !== 2) {
      debugLog('VALIDATION', 'SUBMIT_VALIDATION_FAILED', {
        field: 'DDD',
        reason: 'DDD deve ter 2 dígitos',
        ddd_length: onlyDigits(ddd).length
      }, 'warn');
      alert('Por favor, preencha o DDD corretamente.');
      $(MODAL_CONFIG.fieldIds.ddd).focus();
      return;
    }
    
    if (!celular || onlyDigits(celular).length !== 9) {
      debugLog('VALIDATION', 'SUBMIT_VALIDATION_FAILED', {
        field: 'CELULAR',
        reason: 'Celular deve ter 9 dígitos',
        celular_length: onlyDigits(celular).length
      }, 'warn');
      alert('Por favor, preencha o celular corretamente.');
      $(MODAL_CONFIG.fieldIds.celular).focus();
      return;
    }
    
    // Coletar todos os dados
    const dados = coletarTodosDados();
    dados.DDD = ddd;
    dados.GCLID = getGCLID();
    
    // ✅ V3: LOG DOS DADOS COLETADOS
    debugLog('STATE', 'SUBMIT_DATA_COLLECTED', {
      dados_summary: {
        has_ddd: !!dados.DDD,
        has_celular: !!dados.CELULAR,
        has_cpf: !!dados.CPF,
        has_nome: !!dados.NOME,
        has_placa: !!dados.PLACA,
        has_cep: !!dados.CEP,
        has_email: !!dados.EMAIL,
        has_gclid: !!dados.GCLID
      },
      dados_complete: dados
    }, 'info');
    
    // ✅ V2: Verificar se há dados novos para atualizar
    const hasNewData = !!(dados.CPF || dados.NOME || dados.CEP || dados.PLACA);
    
    // ✅ V3: LOG DA DECISÃO DE ATUALIZAÇÃO
    debugLog('STATE', 'UPDATE_DECISION', {
      has_new_data: hasNewData,
      new_data_fields: {
        cpf: !!dados.CPF,
        nome: !!dados.NOME,
        cep: !!dados.CEP,
        placa: !!dados.PLACA
      },
      will_update: hasNewData
    }, 'info');
    
    if (hasNewData) {
      // Tentar recuperar ID do lead anterior
      const previousState = getLeadState();
      const espocrmId = previousState?.lead_id || null;
      
      debugLog('ESPOCRM', 'UPDATE_WILL_BE_CALLED', {
        has_lead_id: !!espocrmId,
        lead_id: espocrmId || '(não encontrado)'
      }, 'info');
      
      logEvent('whatsapp_modal_submit_update_attempt', {
        has_cpf: !!dados.CPF,
        has_nome: !!dados.NOME,
        has_placa: !!dados.PLACA
      }, 'info');
      
      // Atualizar lead (não bloqueante)
      atualizarLeadEspoCRM(dados, espocrmId)
        .then(result => {
          debugLog('ESPOCRM', 'UPDATE_COMPLETE', {
            success: result.success,
            error: result.error || null,
            attempt: result.attempt || null
          }, result.success ? 'info' : 'warn');
          
          if (result.success) {
            console.log('✅ [MODAL] Lead atualizado com sucesso');
            logEvent('whatsapp_modal_espocrm_update_final_success', {}, 'info');
          } else {
            console.warn('⚠️ [MODAL] Erro ao atualizar lead (não bloqueante):', result.error);
            logEvent('whatsapp_modal_espocrm_update_final_failed', { error: result.error }, 'warning');
          }
        })
        .catch(error => {
          debugLog('ERROR', 'UPDATE_EXCEPTION', {
            error_message: error.message,
            error_stack: error.stack
          }, 'error');
          
          logEvent('whatsapp_modal_espocrm_update_exception', { error: error.message }, 'error');
        });
    } else {
      debugLog('STATE', 'UPDATE_SKIPPED', {
        reason: 'Nenhum dado novo para atualizar'
      }, 'info');
      
      logEvent('whatsapp_modal_submit_no_new_data', {}, 'info');
    }
    
    // Sempre abrir WhatsApp (não bloqueado por atualização)
    debugLog('STATE', 'WHATSAPP_OPENING', {
      whatsapp_phone: MODAL_CONFIG.whatsapp.phone,
      message_built: buildWhatsAppMessage(dados)
    }, 'info');
    
    logEvent('whatsapp_modal_submit_success', {
      has_new_data: hasNewData
    }, 'info');
    
    $modal.fadeOut(300, function() {
      openWhatsApp(dados);
    });
  });
  
  console.log('✅ [MODAL] Sistema de modal WhatsApp Definitivo inicializado');
  console.log('🌍 [MODAL] Ambiente detectado:', isDevelopmentEnvironment() ? 'DESENVOLVIMENTO' : 'PRODUÇÃO');
  console.log('📊 [MODAL] Versão: V3.0 - Fluxo Otimizado + Debug Logs Detalhados');
  
  debugLog('STATE', 'MODAL_INITIALIZED', {
    environment: isDevelopmentEnvironment() ? 'dev' : 'prod',
    version: '3.0',
    debug_logging_enabled: window.DEBUG_LOG_CONFIG ? 'Sim' : 'Sim (padrão)',
    debug_config: window.DEBUG_LOG_CONFIG || 'padrão (todas habilitadas)'
  }, 'info');
  
  logEvent('whatsapp_modal_initialized', {
    environment: isDevelopmentEnvironment() ? 'dev' : 'prod',
    version: '3.0'
  }, 'info');
  
});




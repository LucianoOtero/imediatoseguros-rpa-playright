/**
 * PROJETO: UNIFICAÇÃO DE ARQUIVOS FOOTER CODE
 * INÍCIO: 30/10/2025 19:55
 * ÚLTIMA ALTERAÇÃO: 06/11/2025 10:09
 * 
 * VERSÃO: 1.6.0 - Correção Modal iOS + Detecção Dispositivo + Flag Controle
 * 
 * Arquivo unificado contendo:
 * - FooterCodeSiteDefinitivoUtils.js (Parte 1)
 * - Footer Code Site Definitivo.js (Parte 2 - modificado)
 * - Inside Head Tag Pagina.js (Parte 3 - GCLID integrado)
 * 
 * ALTERAÇÕES VERSÃO 1.6.0:
 * - ✅ Implementada detecção iOS melhorada (inclui iPad iOS 13+)
 * - ✅ Adicionada flag de controle para prevenir dupla execução
 * - ✅ Implementado handler touchstart para iOS (intercepta antes do Safari seguir link)
 * - ✅ Melhorado handler click com prevenção de dupla execução
 * - ✅ Implementado uso de passive: false apenas em iOS (otimizado para outros dispositivos)
 * - ✅ Correção do problema do modal abrindo como nova aba em dispositivos iOS
 * 
 * BASEADO EM:
 * - PESQUISA_SOLUCOES_VALIDADAS_FONTES_REFERENCIA.md
 * - MDN Web Docs, Stack Overflow, web.dev, WCAG Guidelines
 * 
 * ARQUIVOS RELACIONADOS:
 * - MODAL_WHATSAPP_DEFINITIVO_dev.js
 * - WEBFLOW-SEGUROSIMEDIATO/05-DOCUMENTATION/PESQUISA_SOLUCOES_VALIDADAS_FONTES_REFERENCIA.md
 * - WEBFLOW-SEGUROSIMEDIATO/05-DOCUMENTATION/PROJETO_CORRECAO_MODAL_IOS_NOVA_ABA.md
 * 
 * ALTERAÇÕES VERSÃO 1.5.0:
 * - ✅ Correção crítica: window.DEBUG_CONFIG não sobrescreve mais valores do Webflow Footer Code
 * - ✅ Verificação prioritária movida para primeira linha de logUnified()
 * - ✅ Bloqueio completo de logs quando enabled === false
 * - ✅ Verificações adicionais em todas as callbacks da função logDebug()
 * - ✅ Preservação de valores definidos no Webflow Footer Code usando || operator
 * - ✅ Sistema de logs agora respeita completamente window.DEBUG_CONFIG.enabled
 * 
 * ALTERAÇÕES VERSÃO 1.4.0:
 * - ✅ Sistema unificado de controle de logs implementado
 * - ✅ ~102 ocorrências de console.log/error/warn substituídas por funções unificadas
 * - ✅ Função logDebug() mantida intacta (13 logs internos preservados)
 * - ✅ Configuração global via window.DEBUG_CONFIG (nível, categorias, ambiente)
 * - ✅ Auto-detecção de ambiente (dev/prod) com cache para performance
 * - ✅ Funções de alias: logInfo(), logError(), logWarn(), logDebug()
 * - ✅ Logs categorizados: UTILS, GCLID, MODAL, FOOTER, RPA, GTM, DEBUG, etc.
 * 
 * ALTERAÇÕES VERSÃO 1.3.1:
 * - Constantes globais movidas para ANTES da verificação do Footer Code Utils
 * - Eliminado aviso "Constantes faltando" no console
 * - Sincronização com versão de produção
 * 
 * ALTERAÇÕES VERSÃO 1.3:
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
 * Localização: https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_dev.js
 * 
 * ⚠️ AMBIENTE: DESENVOLVIMENTO
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
  
  // ======================
  // CONSTANTES GLOBAIS (definir ANTES de qualquer uso)
  // ======================
  // ⚠️ AMBIENTE: DESENVOLVIMENTO
  window.USE_PHONE_API = true;
  window.APILAYER_KEY = 'dce92fa84152098a3b5b7b8db24debbc';
  window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138'; // DEV: Ticket origem correto (segurosimediato-8119bf26e77bf4ff336a58e.webflow.io)
  window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f'; // Mesmo para DEV e PROD
  window.VALIDAR_PH3A = false;
  // ======================
  
  // ======================
  // SISTEMA DE CONTROLE DE LOGS
  // ======================
  // Controle global de logs - alterar conforme necessário
  // ⚠️ IMPORTANTE: Usar || para NÃO sobrescrever se já existir (definido no Webflow Footer Code)
  window.DEBUG_CONFIG = window.DEBUG_CONFIG || {
    // Nível global: 'none' | 'error' | 'warn' | 'info' | 'debug' | 'all'
    level: 'info',
    
    // Habilitar/desabilitar logs completamente
    enabled: true,
    
    // Categorias a ignorar (array vazio = nenhuma ignorada)
    exclude: [], // Exemplo: ['DEBUG'] = ignora esta categoria
    
    // Ambiente (auto-detectado uma vez, depois cached)
    environment: 'auto' // 'auto' | 'dev' | 'prod'
  };

  // ======================
  // NÍVEIS DE AJUSTE DISPONÍVEIS
  // ======================
  // 
  // Hierarquia de níveis (ordem crescente de verbosidade):
  // 
  // 1. 'none' (Prioridade: 0)
  //    - Nenhum log é exibido
  //    - Uso: Desativar completamente todos os logs
  //    - Exemplo: window.DEBUG_CONFIG.level = 'none';
  // 
  // 2. 'error' (Prioridade: 1)
  //    - Apenas logs de erro (logError)
  //    - Uso: Produção com foco em erros críticos
  //    - Exemplo: window.DEBUG_CONFIG.level = 'error';
  // 
  // 3. 'warn' (Prioridade: 2)
  //    - Erros + Avisos (logError + logWarn)
  //    - Uso: Produção com alertas importantes
  //    - Exemplo: window.DEBUG_CONFIG.level = 'warn';
  // 
  // 4. 'info' (Prioridade: 3) ⭐ PADRÃO
  //    - Erros + Avisos + Informações (logError + logWarn + logInfo)
  //    - Uso: Desenvolvimento e produção balanceada (RECOMENDADO)
  //    - Exemplo: window.DEBUG_CONFIG.level = 'info';
  // 
  // 5. 'debug' (Prioridade: 4)
  //    - Todos os logs, incluindo debug (exceto logs internos preservados)
  //    - Uso: Depuração detalhada em desenvolvimento
  //    - Exemplo: window.DEBUG_CONFIG.level = 'debug';
  // 
  // 6. 'all' (Prioridade: 5)
  //    - Todos os logs disponíveis (máximo detalhamento)
  //    - Uso: Análise profunda e troubleshooting
  //    - Exemplo: window.DEBUG_CONFIG.level = 'all';
  // 
  // REGRA DE HIERARQUIA:
  // - Ao escolher um nível, todos os níveis abaixo dele também são exibidos
  // - Exemplo: 'info' exibe error + warn + info
  // 
  // OUTRAS CONFIGURAÇÕES:
  // 
  // enabled: true/false
  //    - Controla se o sistema de logs está ativo
  //    - Se false, nenhum log é exibido, independente do nível
  //    - Exemplo: window.DEBUG_CONFIG.enabled = false;
  // 
  // exclude: ['CATEGORIA1', 'CATEGORIA2']
  //    - Ignora logs de categorias específicas
  //    - Categorias disponíveis: 'UTILS', 'GCLID', 'MODAL', 'FOOTER', 
  //      'RPA', 'GTM', 'DEBUG', 'UNIFIED', etc.
  //    - Exemplo: window.DEBUG_CONFIG.exclude = ['DEBUG', 'RPA'];
  // 
  // environment: 'auto' | 'dev' | 'prod'
  //    - 'auto': Detecta automaticamente pelo hostname (recomendado)
  //    - 'dev': Força ambiente de desenvolvimento
  //    - 'prod': Força ambiente de produção
  //    - Em 'prod' sem nível definido, usa 'error' automaticamente
  //    - Exemplo: window.DEBUG_CONFIG.environment = 'prod';
  // 
  // EXEMPLOS PRÁTICOS:
  // 
  // Produção (apenas erros):
  //   window.DEBUG_CONFIG.level = 'error';
  //   window.DEBUG_CONFIG.environment = 'prod';
  // 
  // Desenvolvimento (todos os logs):
  //   window.DEBUG_CONFIG.level = 'all';
  //   window.DEBUG_CONFIG.environment = 'dev';
  // 
  // Desabilitar completamente:
  //   window.DEBUG_CONFIG.enabled = false;
  //   // OU
  //   window.DEBUG_CONFIG.level = 'none';
  // 
  // Ignorar categorias específicas:
  //   window.DEBUG_CONFIG.exclude = ['DEBUG', 'RPA'];
  // 
  // ======================

  // Cache para ambiente detectado (otimização de performance)
  let _envCache = null;

  // Função unificada de log
  window.logUnified = function(level, category, message, data) {
    // VERIFICAÇÃO PRIORITÁRIA: Bloquear ANTES de qualquer execução
    // Verifica se enabled existe E é explicitamente false (boolean ou string)
    if (window.DEBUG_CONFIG && 
        (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
      return; // Bloquear TODOS os logs se disabled (incluindo debug temporário)
    }
    
    // DEBUG TEMPORÁRIO - Apenas se enabled não for false
    if (!window._debugLogChecked) {
      window._debugLogChecked = true;
      console.log('[DEBUG-TEMP] window.DEBUG_CONFIG existe?', !!window.DEBUG_CONFIG);
      console.log('[DEBUG-TEMP] window.DEBUG_CONFIG:', window.DEBUG_CONFIG);
      console.log('[DEBUG-TEMP] enabled value:', window.DEBUG_CONFIG?.enabled);
      console.log('[DEBUG-TEMP] enabled === false?', window.DEBUG_CONFIG?.enabled === false);
      console.log('[DEBUG-TEMP] enabled type:', typeof window.DEBUG_CONFIG?.enabled);
    }
    
    // Fallback para objeto vazio se DEBUG_CONFIG não existir
    const config = window.DEBUG_CONFIG || {};
    
    // Auto-detectar ambiente UMA VEZ (cache para performance)
    if (config.environment === 'auto' && _envCache === null) {
      _envCache = (window.location.hostname.includes('webflow.io') || 
                   window.location.hostname.includes('localhost') ||
                   window.location.hostname.includes('dev.')) ? 'dev' : 'prod';
    }
    
    const env = (config.environment === 'auto') ? _envCache : config.environment;
    
    // Em produção, usar nível mais restritivo se não especificado
    if (env === 'prod' && !config.level) {
      config.level = 'error';
    }
    
    // Mapeamento de níveis (ordem de prioridade)
    const levels = { 'none': 0, 'error': 1, 'warn': 2, 'info': 3, 'debug': 4, 'all': 5 };
    const currentLevel = levels[config.level] || levels['info'];
    const messageLevel = levels[level] || levels['info'];
    
    // Verificar se deve exibir o log baseado no nível
    if (messageLevel > currentLevel) return;
    
    // Verificar exclusão de categoria (apenas um tipo de filtro para simplicidade)
    if (config.exclude && config.exclude.length > 0) {
      if (category && config.exclude.includes(category)) return;
    }
    
    // Formatar mensagem com categoria
    const formattedMessage = category ? `[${category}] ${message}` : message;
    
    // Escolher método de console apropriado
    switch(level) {
      case 'error':
        console.error(formattedMessage, data || '');
        break;
      case 'warn':
        console.warn(formattedMessage, data || '');
        break;
      case 'info':
      case 'debug':
      default:
        console.log(formattedMessage, data || '');
        break;
    }
  };

  // Aliases para facilitar uso
  window.logInfo = (cat, msg, data) => window.logUnified('info', cat, msg, data);
  window.logError = (cat, msg, data) => window.logUnified('error', cat, msg, data);
  window.logWarn = (cat, msg, data) => window.logUnified('warn', cat, msg, data);
  window.logDebug = (cat, msg, data) => window.logUnified('debug', cat, msg, data);
  // ======================
  
  window.logInfo('UTILS', '🔄 Carregando Footer Code Utils...');
  
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
      window.logError('UTILS', '❌ Funções de CPF não disponíveis');
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
      window.logWarn('UTILS', '⚠️ VALIDAR_PH3A não disponível, assumindo false');
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
      window.logError('UTILS', '❌ onlyDigits não disponível');
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
      window.logError('UTILS', '❌ validarPlacaFormato não disponível');
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
      window.logWarn('UTILS', '⚠️ APILAYER_KEY não disponível, usando fallback');
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
      window.logError('UTILS', '❌ validarCelularLocal não disponível');
      return Promise.resolve({ok: false, reason: 'erro_utils'});
    }
    const local = window.validarCelularLocal($DDD.val(), $CEL.val());
    if (!local.ok) return Promise.resolve({ok: false, reason: local.reason});
    
    if (typeof window.USE_PHONE_API === 'undefined') {
      window.logWarn('UTILS', '⚠️ USE_PHONE_API não disponível, assumindo false');
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
        window.logError('UTILS', '❌ sha1 ou hmacSHA256 não disponíveis');
        return null;
      }
      
      if (typeof window.SAFETY_TICKET === 'undefined' || typeof window.SAFETY_API_KEY === 'undefined') {
        window.logWarn('UTILS', '⚠️ SAFETY_TICKET ou SAFETY_API_KEY não disponíveis');
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
        window.logError('UTILS', `SafetyMails HTTP Error: ${response.status}`);
        return null;
      }
      
      const data = await response.json();
      return data.Success ? data : null;
    } catch (error) {
      window.logError('UTILS', 'SafetyMails request failed:', error);
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
    window.logError('UTILS', '❌ Funções faltando:', missing);
  } else {
    window.logInfo('UTILS', '✅ Footer Code Utils carregado - 26 funções disponíveis');
  }
  
  // ✅ Verificar se constantes estão disponíveis (recomendação do engenheiro)
  const requiredConstants = ['USE_PHONE_API', 'APILAYER_KEY', 'SAFETY_TICKET', 'SAFETY_API_KEY', 'VALIDAR_PH3A'];
  const missingConstants = requiredConstants.filter(c => typeof window[c] === 'undefined');
  if (missingConstants.length > 0) {
    window.logWarn('UTILS', '⚠️ Constantes faltando:', missingConstants);
  } else {
    window.logInfo('UTILS', '✅ Todas as constantes disponíveis');
  }
})();
// ======================

    
    // ======================
    // FIM DA PARTE 1: FOOTER CODE UTILS
    // ======================
    
    // ======================
    // PARTE 2: FOOTER CODE PRINCIPAL (modificado)
    // ======================
    // Nota: Constantes globais já foram definidas no início do Footer Code Utils (PARTE 1)
    
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
    window.logDebug('GCLID', '🔍 Iniciando captura - URL:', window.location.href);
    window.logDebug('GCLID', '🔍 window.location.search:', window.location.search);
    
    var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
    var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");
    var trackingId = gclid || gbraid;
    
    window.logDebug('GCLID', '🔍 Valores capturados:', { gclid: gclid, gbraid: gbraid, trackingId: trackingId });
    
    if (trackingId) {
      var gclsrc = getParam("gclsrc");
      window.logDebug('GCLID', '🔍 gclsrc:', gclsrc);
      
      if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
        try {
          setCookie("gclid", trackingId, 90);
          window.logInfo('GCLID', '✅ Capturado da URL e salvo em cookie:', trackingId);
          
          // Verificar se cookie foi salvo corretamente
          var cookieVerificado = readCookie("gclid");
          window.logDebug('GCLID', '🔍 Cookie verificado após salvamento:', cookieVerificado);
        } catch (error) {
          window.logError('GCLID', '❌ Erro ao salvar cookie:', error);
        }
      } else {
        window.logWarn('GCLID', '⚠️ gclsrc bloqueou salvamento:', gclsrc);
      }
    } else {
      window.logWarn('GCLID', '⚠️ Nenhum trackingId encontrado na URL');
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
          window.logError('FOOTER', '[FOOTER COMPLETO] Timeout aguardando dependências:', {
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
      window.logInfo('CONFIG', '🎯 RPA habilitado:', window.rpaEnabled);
      
      // 2.1. Gerenciamento GCLID (DOMContentLoaded)
      document.addEventListener("DOMContentLoaded", function () {
        // Tentar capturar novamente se não foi capturado antes (FALLBACK)
        var cookieExistente = window.readCookie ? window.readCookie("gclid") : null;
        
        if (!cookieExistente) {
          window.logDebug('GCLID', '🔍 Cookie não encontrado, tentando captura novamente no DOMContentLoaded...');
          var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
          var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");
          var trackingId = gclid || gbraid;
          
          if (trackingId) {
            var gclsrc = getParam("gclsrc");
            if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
              try {
                setCookie("gclid", trackingId, 90);
                window.logInfo('GCLID', '✅ Capturado no DOMContentLoaded e salvo em cookie:', trackingId);
                cookieExistente = trackingId;
              } catch (error) {
                window.logError('GCLID', '❌ Erro ao salvar cookie no DOMContentLoaded:', error);
              }
            }
          } else {
            window.logWarn('GCLID', '⚠️ Nenhum trackingId encontrado na URL no DOMContentLoaded');
          }
        } else {
          window.logInfo('GCLID', '✅ Cookie já existe:', cookieExistente);
        }
        
        // Preencher campos com nome GCLID_FLD
        const gclidFields = document.getElementsByName("GCLID_FLD");
        window.logDebug('GCLID', '🔍 Campos GCLID_FLD encontrados:', gclidFields.length);
        
        for (var i = 0; i < gclidFields.length; i++) {
          var cookieValue = window.readCookie ? window.readCookie("gclid") : cookieExistente;
          
          if (cookieValue) {
            gclidFields[i].value = cookieValue;
            window.logInfo('GCLID', '✅ Campo GCLID_FLD[' + i + '] preenchido:', cookieValue);
          } else {
            window.logWarn('GCLID', '⚠️ Campo GCLID_FLD[' + i + '] não preenchido - cookie não encontrado');
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
          window.logInfo("GCLID", "✅ CollectChatAttributes configurado:", decodeURIComponent(gclidCookie));
        }
      });
      
      // Função básica de logging para teste
      function logDebug(level, message, data = null) {
        // Verificar se logs estão desabilitados
        if (window.DEBUG_CONFIG && 
            (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
          return; // Bloquear se disabled
        }
        
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
          // Verificar enabled novamente antes de cada log
          if (window.DEBUG_CONFIG && 
              (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
            return;
          }
          console.log(`[LOG DEBUG] Status: ${response.status} ${response.statusText}`);
          console.log(`[LOG DEBUG] Headers:`, Object.fromEntries(response.headers.entries()));
          
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
          
          return response.text();
        })
        .then(text => {
          // Verificar enabled novamente antes de cada log
          if (window.DEBUG_CONFIG && 
              (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
            return;
          }
          console.log(`[LOG DEBUG] Resposta bruta:`, text);
          
          try {
            const result = JSON.parse(text);
            if (window.DEBUG_CONFIG && 
                (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
              return;
            }
            console.log(`[LOG DEBUG] Sucesso:`, result);
            
            if (result.success) {
              if (window.DEBUG_CONFIG && 
                  (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
                return;
              }
              console.log(`[LOG DEBUG] Log enviado com sucesso! ID: ${result.logged?.log_id || 'N/A'}`);
            } else {
              if (window.DEBUG_CONFIG && 
                  (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
                return;
              }
              console.error(`[LOG DEBUG] Erro no servidor:`, result.error);
            }
          } catch (parseError) {
            if (window.DEBUG_CONFIG && 
                (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
              return;
            }
            console.error(`[LOG DEBUG] Erro ao fazer parse da resposta:`, parseError);
            console.error(`[LOG DEBUG] Resposta que causou erro:`, text);
          }
        })
        .catch(error => {
          if (window.DEBUG_CONFIG && 
              (window.DEBUG_CONFIG.enabled === false || window.DEBUG_CONFIG.enabled === 'false')) {
            return;
          }
          console.error(`[LOG DEBUG] Erro na requisição:`, error);
          console.error(`[LOG DEBUG] Tipo do erro:`, error.constructor.name);
          console.error(`[LOG DEBUG] Mensagem:`, error.message);
          
          // Log adicional para debugging
          if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
            console.error(`[LOG DEBUG] Possível problema de CORS ou rede`);
          }
        });
        
        // Manter console.log para desenvolvimento local (apenas se enabled)
        if (!window.DEBUG_CONFIG || 
            (window.DEBUG_CONFIG.enabled !== false && window.DEBUG_CONFIG.enabled !== 'false')) {
          console.log(`[${level}] ${message}`, data);
        }
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
            window.logInfo('RPA', '🎯 Script RPA já carregado');
            resolve();
            return;
          }

          window.logInfo('RPA', '🎯 Carregando script RPA...');
          
          const script = document.createElement('script');
          script.src = 'https://mdmidia.com.br/webflow_injection_limpo.js';
          script.onload = () => {
            window.logInfo('RPA', '✅ Script RPA carregado com sucesso');
            resolve();
          };
          script.onerror = () => {
            window.logError('RPA', '❌ Erro ao carregar script RPA');
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
          window.logWarn('FOOTER', '⚠️ readCookie não disponível, tentando novamente...');
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

      /**
       * Detecção iOS melhorada (inclui iPad iOS 13+)
       * Baseado em: MDN, Stack Overflow, GeeksforGeeks
       * Validação: PESQUISA_SOLUCOES_VALIDADAS_FONTES_REFERENCIA.md
       */
      function isIOS() {
        // Detecção padrão
        const isStandardIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
        
        // Detecção para iPad iOS 13+ (retorna MacIntel)
        const isIPadOS13 = navigator.platform === 'MacIntel' && 
                           navigator.maxTouchPoints > 1 &&
                           'ontouchend' in document;
        
        return isStandardIOS || isIPadOS13;
      }

      // Função para carregar modal dinamicamente
      function loadWhatsAppModal() {
        if (window.whatsappModalLoaded) {
          window.logInfo('MODAL', '✅ Modal já carregado');
          return;
        }
        
        window.logInfo('MODAL', '🔄 Carregando modal de dev.bpsegurosimediato.com.br...');
        const script = document.createElement('script');
        script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js?v=24&force=' + Math.random();
        script.onload = function() {
          window.whatsappModalLoaded = true;
          window.logInfo('MODAL', '✅ Modal carregado com sucesso');
        };
        script.onerror = function() {
          window.logError('MODAL', '❌ Erro ao carregar modal');
        };
        document.head.appendChild(script);
      }
      
      /**
       * Flag de controle para prevenir dupla execução
       * Baseado em: Stack Overflow, CSS-Tricks (padrão da indústria)
       */
      let modalOpening = false;

      /**
       * Função unificada para abrir modal
       * Previne dupla execução com flag de controle
       */
      function openWhatsAppModal() {
        if (modalOpening) {
          window.logDebug('MODAL', '⚠️ Modal já está sendo aberto, ignorando chamada duplicada');
          return;
        }
        
        modalOpening = true;
        window.logDebug('MODAL', '🔄 Abrindo modal WhatsApp');
        
        // Se modal já existe, apenas abrir
        if ($('#whatsapp-modal').length) {
          $('#whatsapp-modal').fadeIn(300);
          // Resetar flag após animação completar
          setTimeout(() => {
            modalOpening = false;
          }, 500);
        } else {
          // Modal não existe, carregar
          loadWhatsAppModal();
          
          // Aguardar modal ser criado pelo script
          const checkModal = setInterval(function() {
            if ($('#whatsapp-modal').length) {
              clearInterval(checkModal);
              $('#whatsapp-modal').fadeIn(300);
              setTimeout(() => {
                modalOpening = false;
              }, 500);
            }
          }, 100);
          
          // Timeout de 3 segundos
          setTimeout(function() {
            clearInterval(checkModal);
            if ($('#whatsapp-modal').length) {
              $('#whatsapp-modal').fadeIn(300);
            }
            modalOpening = false;
          }, 3000);
        }
      }

      /**
       * Verificar suporte a passive listeners
       * Baseado em: MDN, web.dev
       */
      let passiveSupported = false;
      try {
        const opts = Object.defineProperty({}, 'passive', {
          get() { passiveSupported = true; }
        });
        window.addEventListener('test', null, opts);
        window.removeEventListener('test', null, opts);
      } catch (e) {
        // Navegador não suporta passive option
        passiveSupported = false;
      }

      // Aguardar jQuery para inicializar validações
      $(function () {
        /**
         * Configurar handlers com detecção de dispositivo iOS
         * Baseado em: PESQUISA_SOLUCOES_VALIDADAS_FONTES_REFERENCIA.md
         * 
         * Soluções implementadas:
         * 1. Detecção iOS melhorada (inclui iPad iOS 13+)
         * 2. Flag de controle para prevenir dupla execução
         * 3. Handler touchstart para iOS (intercepta antes do Safari seguir link)
         * 4. Handler click melhorado com prevenção de dupla execução
         * 5. Uso de passive: false apenas em iOS
         */
        ['whatsapplink', 'whatsapplinksucesso', 'whatsappfone1', 'whatsappfone2'].forEach(function (id) {
          var $el = $('#' + id);
          if (!$el.length) return;
          
          // Handler touchstart (apenas iOS)
          // iOS Safari processa touchstart ANTES de click
          // Precisamos interceptar touchstart para prevenir navegação
          if (isIOS()) {
            const touchOptions = passiveSupported ? { passive: false } : false;
            
            $el.on('touchstart', function (e) {
              // Se modal já está sendo aberto, prevenir evento
              if (modalOpening) {
                e.preventDefault();
                e.stopPropagation();
                return false;
              }
              
              // Prevenir comportamento padrão (navegação)
              e.preventDefault();
              e.stopPropagation();
              
              // Abrir modal
              openWhatsAppModal();
              
              // Retornar false para garantir que não segue link
              return false;
            });
            
            window.logDebug('MODAL', '✅ Handler touchstart configurado para iOS:', id);
          }
          
          // Handler click (todos os dispositivos)
          $el.on('click', function (e) {
            // Em iOS, se touchstart já executou, prevenir click
            if (isIOS() && modalOpening) {
              e.preventDefault();
              e.stopPropagation();
              return false;
            }
            
            // Prevenir comportamento padrão
            e.preventDefault();
            e.stopPropagation();
            
            // Abrir modal
            openWhatsAppModal();
            
            // Retornar false para garantir que não segue link
            return false;
          });
          
          window.logDebug('MODAL', '✅ Handler click configurado:', id);
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
            window.logError('FOOTER', '❌ validarCPFAlgoritmo não disponível');
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
              window.logError('FOOTER', 'Erro na consulta da API PH3A');
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
            window.logError('FOOTER', '❌ onlyDigits não disponível');
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
            window.logError('FOOTER', '❌ onlyDigits não disponível');
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
            window.logError('FOOTER', '❌ validarEmailLocal não disponível');
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
          window.logDebug('DEBUG', '🎯 Botão CALCULE AGORA! clicado');
          e.preventDefault(); // Bloquear submit natural para validação
          e.stopPropagation();
          
          // Encontrar o formulário e disparar validação
          const $form = $(this).closest('form');
          if ($form.length) {
            window.logDebug('DEBUG', '🔍 Disparando validação manual do formulário');
            $form.trigger('submit');
          }
        });

        // SUBMIT — revalida tudo e oferece Corrigir / Prosseguir
        $('form').each(function(){
          const $form=$(this);
          
          $form.on('submit', function(ev){
            if ($form.data('validated-ok') === true) { $form.removeData('validated-ok'); return true; }
            if ($form.data('skip-validate') === true){ $form.removeData('skip-validate');  return true; }

            window.logDebug('DEBUG', '🔍 Submit do formulário interceptado');
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
              window.logDebug('DEBUG', '🔍 Dados inválidos?', invalido);

              if (!invalido){
                window.logDebug('DEBUG', '✅ Dados válidos - verificando RPA');
                
                // 🎯 CAPTURAR CONVERSÃO GTM - DADOS VÁLIDOS
                window.logInfo('GTM', '🎯 Registrando conversão - dados válidos');
                if (typeof window.dataLayer !== 'undefined') {
                  window.dataLayer.push({
                    'event': 'form_submit_valid',
                    'form_type': 'cotacao_seguro',
                    'validation_status': 'valid'
                  });
                }
                
                if (window.rpaEnabled === true) {
                  window.logInfo('RPA', '🎯 RPA habilitado - iniciando processo RPA');
                  window.loadRPAScript()
                    .then(() => {
                      window.logInfo('RPA', '🎯 Script RPA carregado - executando processo');
                      if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                        const mainPageInstance = new window.MainPage();
                        mainPageInstance.handleFormSubmit($form[0]);
                      } else {
                        window.logWarn('RPA', '🎯 Função handleFormSubmit não encontrada - usando fallback');
                        $form.data('validated-ok', true);
                        if (typeof window.nativeSubmit === 'function') {
                          window.nativeSubmit($form);
                        } else {
                          $form[0].submit();
                        }
                      }
                    })
                    .catch((error) => {
                      window.logError('RPA', '🎯 Erro ao carregar script RPA:', error);
                      window.logInfo('RPA', '🎯 Fallback para processamento Webflow');
                      $form.data('validated-ok', true);
                      if (typeof window.nativeSubmit === 'function') {
                        window.nativeSubmit($form);
                      } else {
                        $form[0].submit();
                      }
                    });
                } else {
                  window.logInfo('RPA', '🎯 RPA desabilitado - processando apenas com Webflow');
                  $form.data('validated-ok', true);
                  if (typeof window.nativeSubmit === 'function') {
                    window.nativeSubmit($form);
                  } else {
                    $form[0].submit();
                  }
                }
              } else {
                window.logDebug('DEBUG', '❌ Dados inválidos - mostrando SweetAlert');
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
                    window.logInfo('RPA', '🎯 Usuário escolheu prosseguir com dados inválidos');
                    
                    // 🎯 CAPTURAR CONVERSÃO GTM - USUÁRIO PROSSEGUIU COM DADOS INVÁLIDOS
                    window.logInfo('GTM', '🎯 Registrando conversão - usuário prosseguiu com dados inválidos');
                    if (typeof window.dataLayer !== 'undefined') {
                      window.dataLayer.push({
                        'event': 'form_submit_invalid_proceed',
                        'form_type': 'cotacao_seguro',
                        'validation_status': 'invalid_proceed'
                      });
                    }
                    
                    if (window.rpaEnabled === true) {
                      window.logInfo('RPA', '🎯 RPA habilitado - iniciando processo RPA com dados inválidos');
                      window.loadRPAScript()
                        .then(() => {
                          window.logInfo('RPA', '🎯 Script RPA carregado - executando processo com dados inválidos');
                          if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                            const mainPageInstance = new window.MainPage();
                            mainPageInstance.handleFormSubmit($form[0]);
                          } else {
                            window.logWarn('RPA', '🎯 Função handleFormSubmit não encontrada - usando fallback');
                            $form.data('skip-validate', true);
                            if (typeof window.nativeSubmit === 'function') {
                              window.nativeSubmit($form);
                            } else {
                              $form[0].submit();
                            }
                          }
                        })
                        .catch((error) => {
                          window.logError('RPA', '🎯 Erro ao carregar script RPA:', error);
                          window.logInfo('RPA', '🎯 Fallback para processamento Webflow');
                          $form.data('skip-validate', true);
                          if (typeof window.nativeSubmit === 'function') {
                            window.nativeSubmit($form);
                          } else {
                            $form[0].submit();
                          }
                        });
                    } else {
                      window.logInfo('RPA', '🎯 RPA desabilitado - processando apenas com Webflow');
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
                  window.logInfo('RPA', '🎯 Usuário escolheu prosseguir após erro de rede');
                  
                  // 🎯 CAPTURAR CONVERSÃO GTM - USUÁRIO PROSSEGUIU APÓS ERRO DE REDE
                  window.logInfo('GTM', '🎯 Registrando conversão - usuário prosseguiu após erro de rede');
                  if (typeof window.dataLayer !== 'undefined') {
                    window.dataLayer.push({
                      'event': 'form_submit_network_error_proceed',
                      'form_type': 'cotacao_seguro',
                      'validation_status': 'network_error_proceed'
                    });
                  }
                  
                  if (window.rpaEnabled === true) {
                    window.logInfo('RPA', '🎯 RPA habilitado - iniciando processo RPA após erro de rede');
                    window.loadRPAScript()
                      .then(() => {
                        window.logInfo('RPA', '🎯 Script RPA carregado - executando processo após erro de rede');
                        if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                          const mainPageInstance = new window.MainPage();
                          mainPageInstance.handleFormSubmit($form[0]);
                        } else {
                          window.logWarn('RPA', '🎯 Função handleFormSubmit não encontrada - usando fallback');
                          $form.data('skip-validate', true);
                          if (typeof window.nativeSubmit === 'function') {
                            window.nativeSubmit($form);
                          } else {
                            $form[0].submit();
                          }
                        }
                      })
                      .catch((error) => {
                        window.logError('RPA', '🎯 Erro ao carregar script RPA:', error);
                        window.logInfo('RPA', '🎯 Fallback para processamento Webflow');
                        $form.data('skip-validate', true);
                        if (typeof window.nativeSubmit === 'function') {
                          window.nativeSubmit($form);
                        } else {
                          $form[0].submit();
                        }
                      });
                  } else {
                    window.logInfo('RPA', '🎯 RPA desabilitado - processando apenas com Webflow');
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
        window.logDebug('DEBUG', '🔍 Iniciando verificação de injeção RPA...');

        // Função para verificar se a injeção foi bem-sucedida
        function debugRPAModule() {
          window.logDebug('DEBUG', '🔍 === VERIFICAÇÃO DE INJEÇÃO RPA ===');
          
          // 1. Verificar se window.rpaEnabled existe
          if (typeof window.rpaEnabled !== 'undefined') {
            window.logDebug('DEBUG', '✅ window.rpaEnabled encontrado:', window.rpaEnabled);
          } else {
            window.logError('DEBUG', '❌ window.rpaEnabled NÃO encontrado!');
          }
          
          // 2. Verificar se loadRPAScript existe
          if (typeof window.loadRPAScript === 'function') {
            window.logDebug('DEBUG', '✅ window.loadRPAScript encontrado');
          } else {
            window.logError('DEBUG', '❌ window.loadRPAScript NÃO encontrado!');
          }
          
          // 3. Verificar se jQuery está disponível
          if (typeof $ !== 'undefined') {
            window.logDebug('DEBUG', '✅ jQuery disponível:', $.fn.jquery);
          } else {
            window.logError('DEBUG', '❌ jQuery NÃO disponível!');
          }
          
          // 4. Verificar se SweetAlert2 está disponível
          if (typeof Swal !== 'undefined') {
            window.logDebug('DEBUG', '✅ SweetAlert2 disponível');
          } else {
            window.logWarn('DEBUG', '⚠️ SweetAlert2 NÃO disponível (pode ser carregado dinamicamente)');
          }
          
          // 5. Verificar conflitos de nomes de função
          const globalFunctions = Object.keys(window).filter(key => typeof window[key] === 'function');
          const rpaFunctions = globalFunctions.filter(func => func.toLowerCase().includes('rpa') || func.toLowerCase().includes('load'));
          window.logDebug('DEBUG', '🔍 Funções globais relacionadas ao RPA:', rpaFunctions);
          
          // 6. Verificar se há elementos de formulário
          const forms = document.querySelectorAll('form');
          window.logDebug('DEBUG', '🔍 Formulários encontrados:', forms.length);
          
          // 7. Verificar se há botões de submit
          const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
          window.logDebug('DEBUG', '🔍 Botões de submit encontrados:', submitButtons.length);
          
          window.logDebug('DEBUG', '🔍 === FIM DA VERIFICAÇÃO ===');
        }

        // Função para testar carregamento dinâmico
        function testDynamicLoading() {
          window.logDebug('DEBUG', '🔍 Testando carregamento dinâmico...');
          
          if (typeof window.loadRPAScript === 'function') {
            window.logDebug('DEBUG', '🔍 Tentando carregar script RPA...');
            
            window.loadRPAScript()
              .then(() => {
                window.logDebug('DEBUG', '✅ Script RPA carregado com sucesso!');
                
                // Verificar se as classes RPA foram carregadas
                if (typeof window.MainPage !== 'undefined') {
                  window.logDebug('DEBUG', '✅ window.MainPage disponível');
                } else {
                  window.logError('DEBUG', '❌ window.MainPage NÃO disponível após carregamento');
                }
                
                if (typeof window.ProgressModalRPA !== 'undefined') {
                  window.logDebug('DEBUG', '✅ window.ProgressModalRPA disponível');
                } else {
                  window.logError('DEBUG', '❌ window.ProgressModalRPA NÃO disponível após carregamento');
                }
                
                if (typeof window.SpinnerTimer !== 'undefined') {
                  window.logDebug('DEBUG', '✅ window.SpinnerTimer disponível');
                } else {
                  window.logError('DEBUG', '❌ window.SpinnerTimer NÃO disponível após carregamento');
                }
                
              })
              .catch(error => {
                window.logError('DEBUG', '❌ Erro ao carregar script RPA:', error);
              });
          } else {
            window.logError('DEBUG', '❌ window.loadRPAScript não está disponível para teste');
          }
        }

        // Função para detectar conflitos
        function detectConflicts() {
          window.logDebug('DEBUG', '🔍 === DETECÇÃO DE CONFLITOS ===');
          
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
            window.logWarn('DEBUG', '⚠️ Possível conflito detectado - múltiplas definições:', functionNames);
          } else {
            window.logDebug('DEBUG', '✅ Nenhum conflito de múltiplas definições detectado');
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
              window.logWarn('DEBUG', '⚠️ Erros detectados durante inicialização:', errors);
            } else {
              window.logDebug('DEBUG', '✅ Nenhum erro detectado durante inicialização');
            }
          }, 2000);
          
          window.logDebug('DEBUG', '🔍 === FIM DA DETECÇÃO DE CONFLITOS ===');
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

        window.logDebug('DEBUG', '🔍 Funções de debug disponíveis:');
        window.logDebug('DEBUG', '  - window.debugRPAModule()');
        window.logDebug('DEBUG', '  - window.testDynamicLoading()');
        window.logDebug('DEBUG', '  - window.detectConflicts()');
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
    window.logError('UNIFIED', 'Erro crítico no Footer Code Unificado:', error);
    window.logError('UNIFIED', 'Stack trace:', error.stack);
    // Não bloquear a página, mas registrar o erro
  }
})();



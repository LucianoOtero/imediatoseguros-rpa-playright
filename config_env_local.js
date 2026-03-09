/**
 * CONFIG_ENV_LOCAL.JS - Variáveis de Ambiente para Testes Locais
 * 
 * Este arquivo define as variáveis de ambiente necessárias para
 * o webflow_injection_limpo.js funcionar localmente no Windows.
 * 
 * IMPORTANTE: Este arquivo DEVE ser carregado ANTES do webflow_injection_limpo.js
 * 
 * Data: 05/01/2026
 * Versão: 1.0.0
 * Ambiente: Local (Windows) - Valores DEV
 * 
 * NOTA: Este arquivo é específico para testes locais e não deve ser usado em produção.
 */

// Variáveis Obrigatórias (sem fallback) - Valores DEV verificados
window.VIACEP_BASE_URL = 'https://viacep.com.br';
window.APILAYER_BASE_URL = 'https://apilayer.net';
window.SAFETYMAILS_OPTIN_BASE = 'https://optin.safetymails.com';
window.RPA_API_BASE_URL = 'https://rpaimediatoseguros.com.br';
window.SUCCESS_PAGE_URL = 'https://bssegurosimediato.com.br/sucesso'; // Pode ser ajustado conforme necessário

// Variáveis Opcionais (com fallback)
window.SAFETYMAILS_OPTIN_PATH = window.SAFETYMAILS_OPTIN_PATH || '/main/safetyoptin/20a7a1c297e39180bd80428ac13c363e882a531f/9bab7f0c2711c5accfb83588c859dc1103844a94/';
window.WEBHOOK_SITE_URL = window.WEBHOOK_SITE_URL || null;

// Variáveis Opcionais Adicionais (podem ser úteis para testes)
window.APILAYER_KEY = window.APILAYER_KEY || 'dce92fa84152098a3b5b7b8db24debbc';
window.SAFETY_TICKET = window.SAFETY_TICKET || '05bf2ec47128ca0b917f8b955bada1bd3cadd47e';
window.SAFETY_API_KEY = window.SAFETY_API_KEY || '20a7a1c297e39180bd80428ac13c363e882a531f';
window.SAFETYMAILS_BASE_DOMAIN = window.SAFETYMAILS_BASE_DOMAIN || 'safetymails.com';

// Log de confirmação (apenas em desenvolvimento)
if (window.console && window.console.log) {
    console.log('[CONFIG_LOCAL] Variáveis de ambiente carregadas para testes locais');
    console.log('[CONFIG_LOCAL] RPA_API_BASE_URL:', window.RPA_API_BASE_URL);
    console.log('[CONFIG_LOCAL] VIACEP_BASE_URL:', window.VIACEP_BASE_URL);
    console.log('[CONFIG_LOCAL] APILAYER_BASE_URL:', window.APILAYER_BASE_URL);
}

window.APP_BASE_URL = "https://dev.bssegurosimediato.com.br";
window.APP_ENVIRONMENT = "development";

// Novas variÔö£├¡veis expostas (movidas de data-attributes do Webflow)
window.APILAYER_KEY = "dce92fa84152098a3b5b7b8db24debbc";
window.SAFETY_TICKET = "05bf2ec47128ca0b917f8b955bada1bd3cadd47e";
window.SAFETY_API_KEY = "20a7a1c297e39180bd80428ac13c363e882a531f";
window.VIACEP_BASE_URL = "https://viacep.com.br";
window.APILAYER_BASE_URL = "https://apilayer.net";
window.SAFETYMAILS_OPTIN_BASE = "https://optin.safetymails.com";
window.RPA_API_BASE_URL = "https://rpaimediatoseguros.com.br";
window.SAFETYMAILS_BASE_DOMAIN = "safetymails.com";

// VariÔö£├¡veis de ambiente para URLs dos endpoints Cloud Run (adicionadas em 10/12/2025)
// Permite compatibilidade entre ambientes Hetzner e Google Cloud Run
window.LOG_ENDPOINT_URL = "https://log-endpoint-br2qvvxwhq-rj.a.run.app";
window.CPF_VALIDATE_URL = "https://cpf-validate-br2qvvxwhq-rj.a.run.app";
window.PLACA_VALIDATE_URL = "https://placa-validate-br2qvvxwhq-rj.a.run.app";
window.SEND_EMAIL_NOTIFICATION_URL = "https://send-email-notification-br2qvvxwhq-rj.a.run.app";
window.ADD_FLYINGDONKEYS_URL = "https://add-flyingdonkeys-br2qvvxwhq-rj.a.run.app";
window.ADD_WEBFLOW_OCTA_URL = "https://add-webflow-octa-br2qvvxwhq-rj.a.run.app";

// FunÔö£┬║Ôö£├║o helper simples (opcional, para facilitar uso)
window.getEndpointUrl = function(endpoint) {
    if (!window.APP_BASE_URL) {
        // Verificar DEBUG_CONFIG antes de logar (FASE 11 - CorreÔö£┬║Ôö£├║o MÔö£├½DIA)
        if (window.DEBUG_CONFIG && 
            (window.DEBUG_CONFIG.enabled !== false && window.DEBUG_CONFIG.enabled !== 'false')) {
            if (window.console && window.console.warn) {
                console.warn('[CONFIG] APP_BASE_URL nÔö£├║o disponÔö£┬ível');
            }
        }
        return null;
    }
    return window.APP_BASE_URL + '/' + endpoint.replace(/^\//, '');
};


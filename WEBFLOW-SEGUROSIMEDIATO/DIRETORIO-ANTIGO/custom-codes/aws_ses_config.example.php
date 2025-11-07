<?php
/**
 * PROJETO: CONFIGURAÇÃO AWS SES PARA NOTIFICAÇÕES ADMINISTRADORES
 * INÍCIO: 03/11/2025
 * 
 * VERSÃO: 1.0 - Arquivo de exemplo de configuração
 * 
 * ⚠️ IMPORTANTE:
 * - Este é um arquivo de EXEMPLO
 * - Renomeie para aws_ses_config.php
 * - NÃO commitar no GitHub (adicione no .gitignore)
 * - Use as credenciais reais fornecidas
 */

// ======================
// CREDENCIAIS AWS SES
// ======================

// ⚠️ SUBSTITUIR COM AS CREDENCIAIS REAIS
define('AWS_ACCESS_KEY_ID', 'SUA_ACCESS_KEY_ID_AQUI');
define('AWS_SECRET_ACCESS_KEY', 'SUA_SECRET_ACCESS_KEY_AQUI');
define('AWS_REGION', 'sa-east-1'); // Região escolhida no SES

// ======================
// CONFIGURAÇÃO DE EMAIL
// ======================

// Email remetente (deve ser do domínio verificado)
define('EMAIL_FROM', 'noreply@bpsegurosimediato.com.br');
define('EMAIL_FROM_NAME', 'BP Seguros Imediato');

// Emails dos administradores (destinatários)
define('ADMIN_EMAILS', [
    'lrotero@gmail.com', // Email já verificado
    // Adicionar mais emails de administradores aqui
    // 'admin2@bpsegurosimediato.com.br',
]);

// ======================
// VALIDAÇÃO
// ======================

// Verificar se as credenciais estão configuradas
if (AWS_ACCESS_KEY_ID === 'SUA_ACCESS_KEY_ID_AQUI' || 
    AWS_SECRET_ACCESS_KEY === 'SUA_SECRET_ACCESS_KEY_AQUI') {
    error_log('⚠️ AWS SES: Credenciais não configuradas! Use aws_ses_config.php com credenciais reais.');
}



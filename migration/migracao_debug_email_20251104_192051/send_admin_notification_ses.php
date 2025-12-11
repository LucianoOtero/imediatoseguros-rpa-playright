<?php
/**
 * PROJETO: NOTIFICAÇÃO EMAIL ADMINISTRADORES VIA AMAZON SES
 * INÍCIO: 03/11/2025
 * 
 * VERSÃO: 1.1 - Suporte a notificações de erro
 * 
 * Função para enviar notificações para administradores
 * quando cliente preenche telefone corretamente no MODAL_WHATSAPP_DEFINITIVO
 * 
 * USO:
 * require_once 'send_admin_notification_ses.php';
 * $resultado = enviarNotificacaoAdministradores($dados);
 */

// Carregar configuração AWS SES
require_once __DIR__ . '/aws_ses_config.php';

// Carregar AWS SDK se disponível
$awsSdkAvailable = false;
if (file_exists(__DIR__ . '/vendor/autoload.php')) {
    require __DIR__ . '/vendor/autoload.php';
    $awsSdkAvailable = true;
    // Usar classes do AWS SDK apenas se disponível
    if (class_exists('Aws\Ses\SesClient')) {
        // SDK carregado com sucesso
    }
} else {
    error_log('⚠️ AWS SDK não encontrado! Execute: composer require aws/aws-sdk-php');
}

/**
 * Envia notificação para administradores via Amazon SES
 * 
 * @param array $dados Dados do cliente (DDD, celular, CPF, nome, etc.)
 * @return array Resultado do envio ['success' => bool, 'total_sent' => int, 'results' => array]
 */
function enviarNotificacaoAdministradores($dados) {
    try {
        // Verificar se AWS SDK está disponível
        global $awsSdkAvailable;
        if (!$awsSdkAvailable) {
            return [
                'success' => false,
                'error' => 'AWS SDK não instalado. Execute: composer require aws/aws-sdk-php',
                'total_sent' => 0,
                'total_failed' => 0,
                'total_recipients' => 0,
                'results' => []
            ];
        }
        
        // Validar se credenciais estão configuradas
        if (!defined('AWS_ACCESS_KEY_ID') || !defined('AWS_SECRET_ACCESS_KEY')) {
            return [
                'success' => false,
                'error' => 'Credenciais AWS não configuradas',
                'total_sent' => 0,
                'total_failed' => 0,
                'total_recipients' => 0,
                'results' => []
            ];
        }

        // Criar cliente SES
        $sesClient = new \Aws\Ses\SesClient([
            'version' => 'latest',
            'region'  => AWS_REGION,
            'credentials' => [
                'key'    => AWS_ACCESS_KEY_ID,
                'secret' => AWS_SECRET_ACCESS_KEY,
            ],
        ]);

        // Preparar dados para email
        $ddd = $dados['ddd'] ?? '';
        $celular = $dados['celular'] ?? '';
        $telefoneCompleto = !empty($ddd) && !empty($celular)
            ? '(' . $ddd . ') ' . $celular
            : 'Não informado';

        $cpf = $dados['cpf'] ?? 'Não informado';
        $nome = $dados['nome'] ?? 'Não informado';
        $emailCliente = $dados['email'] ?? 'Não informado';
        $cep = $dados['cep'] ?? 'Não informado';
        $placa = $dados['placa'] ?? 'Não informado';
        $gclid = $dados['gclid'] ?? 'Não informado';
        $dataHora = date('d/m/Y H:i:s');

        // Identificadores visuais do momento
        $momento_emoji = $dados['momento_emoji'] ?? '📧';
        $momento_descricao = $dados['momento_descricao'] ?? 'Notificação';
        $momento = $dados['momento'] ?? 'unknown';
        
        // NOVO: Verificar se há erro
        $temErro = isset($dados['erro']) && $dados['erro'] !== null;
        
        // NOVO: Cor do banner baseada em erro ou momento
        if ($temErro) {
            $bannerColor = '#F44336'; // Vermelho para erro
        } else {
            $bannerColor = ($momento === 'initial') ? '#2196F3' : '#4CAF50'; // Azul para INITIAL, Verde para UPDATE
        }

        // Assunto do email com identificador visual
        $subject = sprintf(
            '%s %s - Modal WhatsApp - %s',
            $momento_emoji,
            $momento_descricao,
            $telefoneCompleto
        );

        // Corpo do email (HTML)
        $htmlBody = '
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
                .container { max-width: 600px; margin: 20px auto; background-color: #ffffff; }
                .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }
                .header h2 { margin: 0; font-size: 20px; }
                .content { background-color: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; }
                .field { margin: 12px 0; padding: 12px; background-color: white; border-left: 4px solid #4CAF50; border-radius: 3px; }
                .label { font-weight: bold; color: #666; display: inline-block; min-width: 100px; }
                .value { color: #333; }
                .footer { margin-top: 20px; padding: 15px; text-align: center; color: #666; font-size: 12px; border-top: 1px solid #ddd; }
                .highlight { background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 15px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>📱 Novo Contato - Modal WhatsApp</h2>
                </div>
                <div class="banner" style="background-color: ' . $bannerColor . '; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 16px; margin-bottom: 20px;">
                    ' . $momento_emoji . ' ' . $momento_descricao . '
                </div>
                <div class="content">
                    <div class="highlight">
                        <p style="margin: 0; font-weight: bold;">Um cliente preencheu o telefone corretamente no modal WhatsApp.</p>
                    </div>
                    
                    <div class="field">
                        <span class="label">📞 Telefone:</span>
                        <span class="value">' . htmlspecialchars($telefoneCompleto) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">👤 Nome:</span>
                        <span class="value">' . htmlspecialchars($nome) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">🆔 CPF:</span>
                        <span class="value">' . htmlspecialchars($cpf) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">📧 Email:</span>
                        <span class="value">' . htmlspecialchars($emailCliente) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">📍 CEP:</span>
                        <span class="value">' . htmlspecialchars($cep) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">🚗 Placa:</span>
                        <span class="value">' . htmlspecialchars($placa) . '</span>
                    </div>
                    
                    <div class="field">
                        <span class="label">🔗 GCLID:</span>
                        <span class="value">' . htmlspecialchars($gclid) . '</span>
                    </div>
                    
                    ' . ($temErro ? '
                    <div class="field" style="background-color: #ffebee; border-left-color: #F44336;">
                        <span class="label" style="color: #F44336; font-weight: bold;">❌ ERRO NO ENVIO:</span>
                        <span class="value" style="color: #F44336;">' . htmlspecialchars($dados['erro']['message'] ?? 'Erro desconhecido') . '</span>
                    </div>' . 
                    (isset($dados['erro']['status']) && $dados['erro']['status'] !== null ? '
                    <div class="field" style="background-color: #ffebee; border-left-color: #F44336;">
                        <span class="label">Status HTTP:</span>
                        <span class="value" style="color: #F44336;">' . htmlspecialchars($dados['erro']['status']) . '</span>
                    </div>' : '') .
                    (isset($dados['erro']['code']) && $dados['erro']['code'] !== null ? '
                    <div class="field" style="background-color: #ffebee; border-left-color: #F44336;">
                        <span class="label">Código:</span>
                        <span class="value" style="color: #F44336;">' . htmlspecialchars($dados['erro']['code']) . '</span>
                    </div>' : '') : '') . '
                    
                    <div class="field">
                        <span class="label">🕐 Data/Hora:</span>
                        <span class="value">' . htmlspecialchars($dataHora) . '</span>
                    </div>
                </div>
                <div class="footer">
                    <p>Esta é uma notificação automática do sistema BP Seguros Imediato.</p>
                    <p>Não responda este email.</p>
                </div>
            </div>
        </body>
        </html>
        ';

        // Corpo do email (texto simples - fallback)
        $textBody = "
Novo Contato - Modal WhatsApp
============================

Um cliente preencheu o telefone corretamente no modal WhatsApp.
" . ($temErro ? "\n⚠️ ERRO: O envio ao EspoCRM falhou!\n" : "") . "

Telefone: {$telefoneCompleto}
Nome: {$nome}
CPF: {$cpf}
Email: {$emailCliente}
CEP: {$cep}
Placa: {$placa}
GCLID: {$gclid}
" . ($temErro ? "ERRO: " . ($dados['erro']['message'] ?? 'Erro desconhecido') . "\n" : "") . "
Data/Hora: {$dataHora}

---
Esta é uma notificação automática do sistema BP Seguros Imediato.
Não responda este email.
        ";

        // Enviar para cada administrador
        $results = [];
        $successCount = 0;
        $failCount = 0;
        
        foreach (ADMIN_EMAILS as $adminEmail) {
            try {
                $result = $sesClient->sendEmail([
                    'Source' => EMAIL_FROM_NAME . ' <' . EMAIL_FROM . '>',
                    'Destination' => [
                        'ToAddresses' => [$adminEmail],
                    ],
                    'Message' => [
                        'Subject' => [
                            'Data' => $subject,
                            'Charset' => 'UTF-8',
                        ],
                        'Body' => [
                            'Html' => [
                                'Data' => $htmlBody,
                                'Charset' => 'UTF-8',
                            ],
                            'Text' => [
                                'Data' => $textBody,
                                'Charset' => 'UTF-8',
                            ],
                        ],
                    ],
                    // Tags para identificação (útil para métricas)
                    'Tags' => [
                        [
                            'Name' => 'source',
                            'Value' => 'modal-whatsapp',
                        ],
                        [
                            'Name' => 'type',
                            'Value' => 'admin-notification',
                        ],
                    ],
                ]);

                $results[] = [
                    'email' => $adminEmail,
                    'success' => true,
                    'message_id' => $result['MessageId'],
                ];
                $successCount++;
                
                // Log de sucesso
                error_log("✅ SES: Email enviado com sucesso para {$adminEmail} - MessageId: {$result['MessageId']}");
                
            } catch (\Aws\Exception\AwsException $e) {
                $results[] = [
                    'email' => $adminEmail,
                    'success' => false,
                    'error' => $e->getAwsErrorMessage(),
                    'code' => $e->getAwsErrorCode(),
                ];
                $failCount++;
                
                // Log de erro
                error_log("❌ SES: Erro ao enviar para {$adminEmail} - {$e->getAwsErrorCode()}: {$e->getAwsErrorMessage()}");
            }
        }

        // Retornar resultado consolidado
        return [
            'success' => $successCount > 0,
            'total_sent' => $successCount,
            'total_failed' => $failCount,
            'total_recipients' => count(ADMIN_EMAILS),
            'results' => $results,
        ];

    } catch (\Aws\Exception\AwsException $e) {
        error_log("❌ SES: Erro na configuração/cliente - {$e->getAwsErrorCode()}: {$e->getAwsErrorMessage()}");
        return [
            'success' => false,
            'error' => $e->getAwsErrorMessage(),
            'code' => $e->getAwsErrorCode(),
        ];
    } catch (Exception $e) {
        error_log("❌ SES: Erro geral - {$e->getMessage()}");
        return [
            'success' => false,
            'error' => $e->getMessage(),
        ];
    }
}


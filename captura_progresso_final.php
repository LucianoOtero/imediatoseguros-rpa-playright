<?php
/**
 * CAPTURA PROGRESSTRACKER - VERSÃO FINAL
 * Força a exibição do JSON final
 */

class CapturaProgressoFinal {
    
    public function __construct() {
        echo "CAPTURA PROGRESSTRACKER - VERSÃO FINAL\n";
        echo "======================================\n\n";
    }
    
    /**
     * Executar RPA com visualizar_mensagens=true para capturar JSON
     */
    public function executarRPAComJSON() {
        echo "Executando RPA com JSON visível...\n";
        echo "Inicio: " . date("H:i:s") . "\n\n";
        
        // Criar configuração temporária com visualizar_mensagens=true
        $config = json_decode(file_get_contents("parametros.json"), true);
        $config["configuracao"]["visualizar_mensagens"] = true;
        
        $config_temp = "parametros_temp.json";
        file_put_contents($config_temp, json_encode($config, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        $comando = "python executar_rpa_imediato_playwright.py --config $config_temp";
        
        echo "Comando: $comando\n";
        echo "Executando...\n\n";
        
        // Usar popen para capturar output em tempo real
        $handle = popen($comando, "r");
        $output = "";
        
        if ($handle) {
            while (!feof($handle)) {
                $output .= fread($handle, 8192);
            }
            pclose($handle);
        }
        
        // Limpar arquivo temporário
        unlink($config_temp);
        
        echo "Fim: " . date("H:i:s") . "\n";
        echo "Resultado capturado!\n\n";
        
        return $output;
    }
    
    /**
     * Analisar resultado e mostrar progresso passo a passo
     */
    public function analisarProgresso($resultado_json) {
        echo "ANALISANDO PROGRESSO PASSO A PASSO\n";
        echo "=================================\n\n";
        
        if (empty($resultado_json)) {
            echo "ERRO: Resultado vazio!\n";
            return;
        }
        
        // Tentar encontrar JSON no output
        $json_start = strpos($resultado_json, "{");
        if ($json_start !== false) {
            $json_content = substr($resultado_json, $json_start);
            $resultado = json_decode($json_content, true);
        } else {
            echo "ERRO: JSON não encontrado no output!\n";
            echo "Conteúdo bruto:\n";
            echo $resultado_json . "\n";
            return;
        }
        
        if (!$resultado) {
            echo "ERRO: JSON inválido!\n";
            echo "Conteúdo bruto:\n";
            echo $resultado_json . "\n";
            return;
        }
        
        // Informações gerais
        echo "INFORMACOES GERAIS:\n";
        echo "Status: " . ($resultado["status"] ?? "N/A") . "\n";
        echo "Tempo de execucao: " . ($resultado["tempo_execucao"] ?? "N/A") . "s\n";
        echo "Erros: " . ($resultado["erros"]["total_erros"] ?? "N/A") . "\n";
        echo "Warnings: " . ($resultado["erros"]["total_warnings"] ?? "N/A") . "\n\n";
        
        // ProgressTracker (Fase 3 - em memória)
        if (isset($resultado["progresso"])) {
            $progresso = $resultado["progresso"];
            
            echo "PROGRESSTRACKER (FASE 3 - EM MEMORIA):\n";
            echo "=====================================\n";
            echo "Etapa final: " . ($progresso["etapa_atual"] ?? "N/A") . "\n";
            echo "Total de etapas: " . ($progresso["total_etapas"] ?? "N/A") . "\n";
            echo "Percentual final: " . round($progresso["percentual"] ?? 0, 2) . "%\n";
            echo "Status final: " . ($progresso["status"] ?? "N/A") . "\n";
            echo "Tempo total: " . round($progresso["tempo_decorrido"] ?? 0, 2) . "s\n";
            echo "Timestamp: " . ($progresso["timestamp"] ?? "N/A") . "\n\n";
            
            // Histórico de etapas - PASSO A PASSO
            if (isset($progresso["etapas_historico"]) && is_array($progresso["etapas_historico"])) {
                echo "HISTORICO DE ETAPAS (PASSO A PASSO):\n";
                echo "===================================\n";
                
                foreach ($progresso["etapas_historico"] as $index => $etapa) {
                    $num = $index + 1;
                    $etapa_num = $etapa["etapa"] ?? "N/A";
                    $status = $etapa["status"] ?? "N/A";
                    $timestamp = $etapa["timestamp"] ?? "N/A";
                    $tempo = round($etapa["tempo_etapa"] ?? 0, 2);
                    
                    echo ">>> ETAPA $etapa_num: $status <<<\n";
                    echo "    Tempo acumulado: {$tempo}s\n";
                    echo "    Timestamp: $timestamp\n\n";
                }
                
                echo "Total de etapas no historico: " . count($progresso["etapas_historico"]) . "\n\n";
            } else {
                echo "AVISO: Historico de etapas nao encontrado\n\n";
            }
            
            // JSON completo do progresso
            echo "JSON COMPLETO DO PROGRESSO:\n";
            echo "===========================\n";
            echo json_encode($progresso, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
            
        } else {
            echo "ERRO: PROGRESSTRACKER NAO ENCONTRADO!\n";
            echo "AVISO: Problema na implementacao da Fase 3\n\n";
        }
        
        // JSON completo do resultado
        echo "JSON COMPLETO DO RESULTADO:\n";
        echo "===========================\n";
        echo json_encode($resultado, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
    }
    
    /**
     * Executar captura completa
     */
    public function executarCaptura() {
        try {
            $resultado = $this->executarRPAComJSON();
            $this->analisarProgresso($resultado);
            
            echo "\nCAPTURA CONCLUIDA!\n";
            echo "ProgressTracker capturado com JSON visível OK\n";
            
        } catch (Exception $e) {
            echo "ERRO: " . $e->getMessage() . "\n";
        }
    }
}

// Executar se chamado diretamente
if (basename(__FILE__) == basename($_SERVER["SCRIPT_NAME"])) {
    $captura = new CapturaProgressoFinal();
    $captura->executarCaptura();
}
?>

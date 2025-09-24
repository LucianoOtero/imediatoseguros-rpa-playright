<?php
/**
 * CAPTURA PROGRESSTRACKER - VERSÃO FUNCIONAL
 * Funciona com o RPA atual (modo silencioso)
 */

class CapturaProgressoFuncional {
    
    public function __construct() {
        echo "CAPTURA PROGRESSTRACKER - VERSÃO FUNCIONAL\n";
        echo "==========================================\n\n";
    }
    
    /**
     * Executar RPA em modo silencioso
     */
    public function executarRPASilencioso() {
        echo "Executando RPA em modo silencioso...\n";
        echo "Inicio: " . date("H:i:s") . "\n\n";
        
        $comando = "python executar_rpa_imediato_playwright.py --config parametros.json";
        
        echo "Comando: $comando\n";
        echo "Executando...\n\n";
        
        // Usar exec() para capturar output
        $output = [];
        $return_var = 0;
        
        exec($comando, $output, $return_var);
        
        echo "Fim: " . date("H:i:s") . "\n";
        echo "Codigo de retorno: $return_var\n";
        echo "Linhas capturadas: " . count($output) . "\n\n";
        
        return $return_var == 0;
    }
    
    /**
     * Capturar ProgressTracker dos arquivos gerados
     */
    public function capturarProgressoDosArquivos() {
        echo "CAPTURANDO PROGRESSO DOS ARQUIVOS\n";
        echo "=================================\n\n";
        
        // Verificar arquivo de progresso
        $arquivo_progresso = "temp/progress_status.json";
        if (file_exists($arquivo_progresso)) {
            echo "Arquivo de progresso encontrado: $arquivo_progresso\n";
            
            $progresso = json_decode(file_get_contents($arquivo_progresso), true);
            if ($progresso) {
                echo "ProgressTracker capturado!\n";
                echo "Etapa final: " . ($progresso["etapa_atual"] ?? "N/A") . "\n";
                echo "Total de etapas: " . ($progresso["total_etapas"] ?? "N/A") . "\n";
                echo "Percentual final: " . round($progresso["percentual"] ?? 0, 2) . "%\n";
                echo "Status final: " . ($progresso["status"] ?? "N/A") . "\n";
                echo "Tempo total: " . round($progresso["tempo_decorrido"] ?? 0, 2) . "s\n";
                echo "Timestamp: " . ($progresso["timestamp"] ?? "N/A") . "\n\n";
                
                // JSON completo do progresso
                echo "JSON COMPLETO DO PROGRESSO:\n";
                echo "===========================\n";
                echo json_encode($progresso, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
                
                return $progresso;
            } else {
                echo "ERRO: JSON inválido no arquivo de progresso\n\n";
            }
        } else {
            echo "AVISO: Arquivo de progresso não encontrado\n";
            echo "Isso é normal na Fase 3 (usar_arquivo=False)\n\n";
        }
        
        return null;
    }
    
    /**
     * Capturar resultado final dos planos
     */
    public function capturarResultadoFinal() {
        echo "CAPTURANDO RESULTADO FINAL\n";
        echo "==========================\n\n";
        
        // Buscar arquivo de resultado mais recente
        $arquivos_resultado = glob("dados_planos_seguro_*.json");
        if (!empty($arquivos_resultado)) {
            $arquivo_mais_recente = max($arquivos_resultado);
            echo "Arquivo mais recente: $arquivo_mais_recente\n";
            
            $resultado = json_decode(file_get_contents($arquivo_mais_recente), true);
            if ($resultado) {
                echo "OK - Resultado final capturado!\n\n";
                
                // Informações gerais
                echo "INFORMACOES GERAIS:\n";
                echo "Plano recomendado: " . $resultado["plano_recomendado"]["valor"] . "\n";
                echo "Plano alternativo: " . $resultado["plano_alternativo"]["valor"] . "\n";
                echo "Franquia recomendada: " . $resultado["plano_recomendado"]["valor_franquia"] . "\n";
                echo "Franquia alternativa: " . $resultado["plano_alternativo"]["valor_franquia"] . "\n\n";
                
                // JSON completo do resultado
                echo "JSON COMPLETO DO RESULTADO:\n";
                echo "===========================\n";
                echo json_encode($resultado, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
                
                return $resultado;
            } else {
                echo "ERRO: JSON inválido no resultado final\n\n";
            }
        } else {
            echo "ERRO: Nenhum arquivo de resultado encontrado\n\n";
        }
        
        return null;
    }
    
    /**
     * Simular progresso passo a passo baseado no resultado
     */
    public function simularProgressoPassoAPasso($progresso, $resultado) {
        echo "SIMULANDO PROGRESSO PASSO A PASSO\n";
        echo "=================================\n\n";
        
        if ($progresso) {
            echo "Baseado no ProgressTracker capturado:\n";
            echo ">>> ETAPA FINAL: " . ($progresso["status"] ?? "N/A") . " <<<\n";
            echo "    Progresso: " . round($progresso["percentual"] ?? 0, 2) . "%\n";
            echo "    Tempo total: " . round($progresso["tempo_decorrido"] ?? 0, 2) . "s\n";
            echo "    Timestamp: " . ($progresso["timestamp"] ?? "N/A") . "\n\n";
        }
        
        if ($resultado) {
            echo "Baseado no resultado final:\n";
            echo ">>> EXECUCAO CONCLUIDA COM SUCESSO <<<\n";
            echo "    Plano recomendado: " . $resultado["plano_recomendado"]["valor"] . "\n";
            echo "    Plano alternativo: " . $resultado["plano_alternativo"]["valor"] . "\n";
            echo "    Status: SUCESSO\n\n";
        }
        
        echo "NOTA: Para ver progresso passo a passo em tempo real,\n";
        echo "execute o RPA no ambiente Linux (Hetzner) onde não há\n";
        echo "problemas de encoding Unicode.\n\n";
    }
    
    /**
     * Executar captura completa
     */
    public function executarCaptura() {
        try {
            if ($this->executarRPASilencioso()) {
                $progresso = $this->capturarProgressoDosArquivos();
                $resultado = $this->capturarResultadoFinal();
                $this->simularProgressoPassoAPasso($progresso, $resultado);
                
                echo "\nCAPTURA CONCLUIDA!\n";
                echo "ProgressTracker capturado dos arquivos OK\n";
            } else {
                echo "ERRO: RPA falhou na execução\n";
            }
            
        } catch (Exception $e) {
            echo "ERRO: " . $e->getMessage() . "\n";
        }
    }
}

// Executar se chamado diretamente
if (basename(__FILE__) == basename($_SERVER["SCRIPT_NAME"])) {
    $captura = new CapturaProgressoFuncional();
    $captura->executarCaptura();
}
?>

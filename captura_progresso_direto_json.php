<?php
/**
 * CAPTURA PROGRESS TRACKER DIRETO VIA JSON
 * Sem arquivos - apenas retorno direto do RPA
 */

class CapturaProgressoDireto {
    
    public function __construct() {
        echo "CAPTURA PROGRESS TRACKER DIRETO VIA JSON\n";
        echo "==========================================\n\n";
    }
    
    /**
     * Executar RPA e capturar JSON completo
     */
    public function executarRPACapturarJSON() {
        echo "Executando RPA e capturando JSON completo...\n";
        echo "Inicio: " . date('H:i:s') . "\n\n";
        
        $comando = "python executar_rpa_imediato_playwright.py --config parametros.json";
        
        echo "Comando: $comando\n";
        echo "Executando...\n\n";
        
        // Executar e capturar output completo
        $output = [];
        $return_var = 0;
        
        exec($comando, $output, $return_var);
        
        echo "Fim: " . date('H:i:s') . "\n";
        echo "Codigo de retorno: $return_var\n";
        echo "Linhas capturadas: " . count($output) . "\n\n";
        
        if ($return_var == 0) {
            return $this->processarOutput($output);
        } else {
            echo "ERRO: RPA falhou na execução\n";
            return null;
        }
    }
    
    /**
     * Processar output e extrair JSON
     */
    private function processarOutput($output) {
        echo "PROCESSANDO OUTPUT\n";
        echo "==================\n\n";
        
        // Procurar pelo JSON final
        $json_encontrado = false;
        $json_content = "";
        
        foreach ($output as $linha) {
            // Procurar por início do JSON estruturado
            if (strpos($linha, '{"status":') !== false) {
                $json_encontrado = true;
                $json_content = $linha;
                break;
            }
        }
        
        if ($json_encontrado) {
            echo "JSON encontrado!\n";
            echo "Tamanho: " . strlen($json_content) . " caracteres\n\n";
            
            $dados = json_decode($json_content, true);
            
            if ($dados) {
                echo "JSON decodificado com sucesso!\n\n";
                return $dados;
            } else {
                echo "ERRO: JSON inválido\n";
                echo "Conteúdo: " . substr($json_content, 0, 200) . "...\n\n";
                return null;
            }
        } else {
            echo "AVISO: JSON não encontrado no output\n";
            echo "Primeiras 5 linhas do output:\n";
            for ($i = 0; $i < min(5, count($output)); $i++) {
                echo "  " . ($i + 1) . ": " . $output[$i] . "\n";
            }
            echo "\n";
            return null;
        }
    }
    
    /**
     * Extrair e exibir ProgressTracker
     */
    public function exibirProgressTracker($dados) {
        echo "PROGRESS TRACKER CAPTURADO\n";
        echo "==========================\n\n";
        
        if (isset($dados['dados']['telas_executadas']['progresso'])) {
            $progresso = $dados['dados']['telas_executadas']['progresso'];
            
            echo "INFORMACOES GERAIS:\n";
            echo "  Etapa atual: " . ($progresso['etapa_atual'] ?? 'N/A') . "\n";
            echo "  Total de etapas: " . ($progresso['total_etapas'] ?? 'N/A') . "\n";
            echo "  Percentual: " . round($progresso['percentual'] ?? 0, 2) . "%\n";
            echo "  Status: " . ($progresso['status'] ?? 'N/A') . "\n";
            echo "  Tempo total: " . round($progresso['tempo_decorrido'] ?? 0, 2) . "s\n";
            echo "  Timestamp: " . ($progresso['timestamp'] ?? 'N/A') . "\n\n";
            
            // Histórico das etapas
            if (isset($progresso['etapas_historico'])) {
                echo "HISTORICO DAS ETAPAS:\n";
                echo "=====================\n";
                
                foreach ($progresso['etapas_historico'] as $etapa) {
                    echo "  Etapa " . ($etapa['etapa'] ?? 'N/A') . ": " . ($etapa['status'] ?? 'N/A') . "\n";
                    echo "    Tempo: " . round($etapa['tempo_etapa'] ?? 0, 2) . "s\n";
                    echo "    Timestamp: " . ($etapa['timestamp'] ?? 'N/A') . "\n\n";
                }
            }
            
            return $progresso;
        } else {
            echo "ERRO: ProgressTracker não encontrado no JSON\n\n";
            return null;
        }
    }
    
    /**
     * Exibir dados dos planos
     */
    public function exibirDadosPlanos($dados) {
        echo "DADOS DOS PLANOS\n";
        echo "================\n\n";
        
        if (isset($dados['dados']['dados_planos'])) {
            $planos = $dados['dados']['dados_planos'];
            
            if (isset($planos['plano_recomendado'])) {
                echo "PLANO RECOMENDADO:\n";
                echo "  Valor: " . ($planos['plano_recomendado']['valor'] ?? 'N/A') . "\n";
                echo "  Franquia: " . ($planos['plano_recomendado']['valor_franquia'] ?? 'N/A') . "\n";
                echo "  Parcelamento: " . ($planos['plano_recomendado']['parcelamento'] ?? 'N/A') . "\n\n";
            }
            
            if (isset($planos['plano_alternativo'])) {
                echo "PLANO ALTERNATIVO:\n";
                echo "  Valor: " . ($planos['plano_alternativo']['valor'] ?? 'N/A') . "\n";
                echo "  Franquia: " . ($planos['plano_alternativo']['valor_franquia'] ?? 'N/A') . "\n";
                echo "  Parcelamento: " . ($planos['plano_alternativo']['parcelamento'] ?? 'N/A') . "\n\n";
            }
        } else {
            echo "AVISO: Dados dos planos não encontrados\n\n";
        }
    }
    
    /**
     * Executar captura completa
     */
    public function executarCaptura() {
        try {
            $dados = $this->executarRPACapturarJSON();
            
            if ($dados) {
                $this->exibirProgressTracker($dados);
                $this->exibirDadosPlanos($dados);
                
                echo "\nCAPTURA CONCLUIDA COM SUCESSO!\n";
                echo "ProgressTracker capturado diretamente do JSON\n";
                echo "Sem uso de arquivos intermediários\n";
            } else {
                echo "ERRO: Falha na captura dos dados\n";
            }
            
        } catch (Exception $e) {
            echo "ERRO: " . $e->getMessage() . "\n";
        }
    }
}

// Executar se chamado diretamente
if (basename(__FILE__) == basename($_SERVER["SCRIPT_NAME"])) {
    $captura = new CapturaProgressoDireto();
    $captura->executarCaptura();
}
?>

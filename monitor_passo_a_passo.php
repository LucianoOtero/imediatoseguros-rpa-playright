<?php
/**
 * MONITOR PROGRESSTRACKER PASSO A PASSO
 * Exibe na tela cada etapa conforme é executada
 */

class MonitorProgressoPassoAPasso {
    
    private $arquivo_progresso = "temp/progress_status.json";
    private $timeout = 300; // 5 minutos
    
    public function __construct() {
        echo "MONITOR PROGRESSTRACKER PASSO A PASSO\n";
        echo "====================================\n\n";
    }
    
    /**
     * Limpar arquivo de progresso anterior
     */
    public function limparProgressoAnterior() {
        echo "Limpando progresso anterior...\n";
        if (file_exists($this->arquivo_progresso)) {
            unlink($this->arquivo_progresso);
            echo "OK - Arquivo de progresso removido\n";
        }
        echo "\n";
    }
    
    /**
     * Executar RPA em background
     */
    public function executarRPABackground() {
        echo "Executando RPA em background...\n";
        echo "Inicio: " . date("H:i:s") . "\n\n";
        
        $comando = "python executar_rpa_imediato_playwright.py --config parametros.json";
        
        // Executar em background
        if (strtoupper(substr(PHP_OS, 0, 3)) === "WIN") {
            $processo = popen("start /B $comando", "r");
        } else {
            $processo = popen("$comando &", "r");
        }
        
        if ($processo) {
            pclose($processo);
            echo "OK - RPA iniciado em background\n\n";
            return true;
        } else {
            echo "ERRO - Falha ao iniciar RPA\n\n";
            return false;
        }
    }
    
    /**
     * Monitorar progresso passo a passo
     */
    public function monitorarPassoAPasso() {
        echo "MONITORAMENTO PASSO A PASSO\n";
        echo "===========================\n\n";
        
        $start_time = time();
        $ultima_etapa = 0;
        $contador_verificacoes = 0;
        $etapas_executadas = [];
        
        while ((time() - $start_time) < $this->timeout) {
            $progresso_atual = $this->lerProgressoAtual();
            
            if ($progresso_atual) {
                $etapa_atual = $progresso_atual["etapa_atual"] ?? 0;
                $status = $progresso_atual["status"] ?? "N/A";
                $percentual = round($progresso_atual["percentual"] ?? 0, 1);
                $tempo_decorrido = round($progresso_atual["tempo_decorrido"] ?? 0, 1);
                
                // Verificar se é uma nova etapa
                if ($etapa_atual > $ultima_etapa) {
                    echo ">>> ETAPA $etapa_atual: $status <<<\n";
                    echo "    Progresso: $percentual%\n";
                    echo "    Tempo decorrido: {$tempo_decorrido}s\n";
                    echo "    Timestamp: " . date("H:i:s") . "\n";
                    
                    // Adicionar à lista de etapas executadas
                    $etapas_executadas[] = [
                        "etapa" => $etapa_atual,
                        "status" => $status,
                        "tempo" => $tempo_decorrido,
                        "timestamp" => date("H:i:s")
                    ];
                    
                    // Mostrar resumo das etapas executadas
                    echo "    Etapas executadas: ";
                    foreach ($etapas_executadas as $etapa) {
                        echo $etapa["etapa"] . " ";
                    }
                    echo "\n\n";
                    
                    $ultima_etapa = $etapa_atual;
                    
                    // Capturar estimativas (Etapa 5)
                    if ($etapa_atual == 5) {
                        $this->capturarEstimativas($progresso_atual);
                    }
                    
                    // Verificar se terminou
                    if ($etapa_atual >= 15) {
                        echo ">>> EXECUCAO CONCLUIDA! <<<\n";
                        echo "Fim: " . date("H:i:s") . "\n";
                        echo "Total de etapas: " . count($etapas_executadas) . "\n\n";
                        break;
                    }
                }
            } else {
                // Mostrar que está aguardando
                $contador_verificacoes++;
                if ($contador_verificacoes % 15 == 0) {
                    echo "Aguardando inicio do RPA... (" . date("H:i:s") . ")\n";
                }
            }
            
            sleep(2); // Verificar a cada 2 segundos
        }
        
        // Mostrar resumo final
        $this->mostrarResumoFinal($etapas_executadas);
    }
    
    /**
     * Ler progresso atual do arquivo
     */
    private function lerProgressoAtual() {
        if (file_exists($this->arquivo_progresso)) {
            $conteudo = file_get_contents($this->arquivo_progresso);
            if ($conteudo) {
                $progresso = json_decode($conteudo, true);
                if ($progresso) {
                    return $progresso;
                }
            }
        }
        return null;
    }
    
    /**
     * Capturar e exibir estimativas (Etapa 5)
     */
    private function capturarEstimativas($progresso) {
        echo ">>> CAPTURANDO ESTIMATIVAS (ETAPA 5) <<<\n";
        echo "========================================\n";
        
        if (isset($progresso["json_retorno"])) {
            echo "OK - Estimativas disponíveis!\n";
            echo "Dados das estimativas:\n";
            echo $progresso["json_retorno"] . "\n\n";
        } else {
            echo "AVISO - Estimativas não encontradas no progresso\n\n";
        }
    }
    
    /**
     * Mostrar resumo final das etapas
     */
    private function mostrarResumoFinal($etapas_executadas) {
        echo "RESUMO FINAL DAS ETAPAS\n";
        echo "=======================\n";
        
        if (!empty($etapas_executadas)) {
            foreach ($etapas_executadas as $etapa) {
                echo "Etapa {$etapa[
etapa]}: {$etapa[status]} ({$etapa[tempo]}s) - {$etapa[timestamp]}\n";
            }
            echo "\nTotal de etapas executadas: " . count($etapas_executadas) . "\n";
        } else {
            echo "Nenhuma etapa foi capturada\n";
        }
        
        // Capturar resultado final
        $this->capturarResultadoFinal();
    }
    
    /**
     * Capturar e exibir resultado final
     */
    private function capturarResultadoFinal() {
        echo "\nRESULTADO FINAL\n";
        echo "===============\n";
        
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
                
            } else {
                echo "ERRO - JSON inválido no resultado final\n\n";
            }
        } else {
            echo "ERRO - Nenhum arquivo de resultado encontrado\n\n";
        }
    }
    
    /**
     * Executar monitoramento completo
     */
    public function executarMonitoramento() {
        try {
            $this->limparProgressoAnterior();
            
            if ($this->executarRPABackground()) {
                $this->monitorarPassoAPasso();
            }
            
            echo "\nMONITORAMENTO CONCLUIDO!\n";
            echo "ProgressTracker monitorado passo a passo na tela OK\n";
            
        } catch (Exception $e) {
            echo "ERRO: " . $e->getMessage() . "\n";
        }
    }
}

// Executar se chamado diretamente
if (basename(__FILE__) == basename($_SERVER["SCRIPT_NAME"])) {
    $monitor = new MonitorProgressoPassoAPasso();
    $monitor->executarMonitoramento();
}
?>

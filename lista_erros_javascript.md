# Lista Exata de Erros para Tratamento no JavaScript

## 🔴 ERROS ESPECÍFICOS (Códigos de Erro)

### 1. Cotação Manual
- **Mensagem**: `"Cotação manual necessária"`
- **Código**: `9003`
- **Tipo**: `"COTACAO_MANUAL_NECESSARIA"`
- **Ação**: Mostrar SweetAlert informativo
- **Ícone**: `info`

### 2. Tela Final Não Detectada
- **Mensagem**: `"Tela final não detectada - cálculo manual necessário"`
- **Código**: `9004`
- **Tipo**: `"TELA_FINAL_NAO_DETECTADA"`
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

## 🔴 ERROS DE NAVEGAÇÃO (Código 9102)

### 3. Erros de Navegação Genéricos
- **Padrão**: `"Erro na navegação - {mensagem}"`
- **Código**: `9102`
- **Tipo**: `"NAVEGACAO"`
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

## 🔴 ERROS DE TELAS (Progress Tracker)

### 4. Tela 1 - Seleção de Tipo de Veículo
- **Mensagem**: `"Tela 1 falhou"`
- **Contexto**: Seleção de tipo de veículo
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 5. Tela 2 - Seleção de Veículo
- **Mensagem**: `"Tela 2 falhou"`
- **Contexto**: Seleção de veículo com placa
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 6. Tela 3 - Confirmação de Seleção
- **Mensagem**: `"Tela 3 falhou"`
- **Contexto**: Confirmação de seleção do veículo
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 7. Tela 4 - Cálculo como Novo Seguro
- **Mensagem**: `"Tela 4 falhou"`
- **Contexto**: Cálculo como novo seguro
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 8. Tela 5 - Elaboração de Estimativas
- **Mensagem**: `"Tela 5 falhou"`
- **Contexto**: Elaboração de estimativas
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 9. Tela 5.5 - Processamento Zero KM
- **Mensagem**: `"Tela Zero KM falhou"`
- **Contexto**: Processamento Zero KM
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 10. Tela 6 - Detalhes do Veículo
- **Mensagem**: `"Tela 6 falhou"`
- **Contexto**: Seleção de detalhes do veículo
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 11. Tela 7 - Local de Pernoite (CEP)
- **Mensagem**: `"Tela 7 falhou"`
- **Contexto**: Definição de local de pernoite com CEP
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 12. Tela 8 - Uso do Veículo
- **Mensagem**: `"Tela 8 falhou"`
- **Contexto**: Definição do uso do veículo
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 13. Tela 9 - Dados Pessoais
- **Mensagem**: `"Tela 9 falhou"`
- **Contexto**: Preenchimento dos dados pessoais
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 14. Tela 10 - Condutor Principal
- **Mensagem**: `"Tela 10 falhou"`
- **Contexto**: Definição do condutor principal
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 15. Tela 11 - Uso do Veículo (Segunda Vez)
- **Mensagem**: `"Tela 11 falhou"`
- **Contexto**: Definição do uso do veículo (segunda vez)
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 16. Tela 12 - Tipo de Garagem
- **Mensagem**: `"Tela 12 falhou"`
- **Contexto**: Definição do tipo de garagem
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 17. Tela 13 - Residentes
- **Mensagem**: `"Tela 13 falhou"`
- **Contexto**: Definição de residentes
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 18. Tela 14 - Corretor
- **Mensagem**: `"Tela 14 falhou"`
- **Contexto**: Definição do corretor
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 19. Tela 15 - Cálculo Completo
- **Mensagem**: `"Tela 15 falhou"`
- **Contexto**: Aguardando cálculo completo
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

## 🔴 ERROS DE CAPTURA DE DADOS

### 20. Falha na Captura de Planos
- **Mensagem**: `"Falha na captura"`
- **Contexto**: Erro na captura de dados dos planos
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

## 🔴 ERROS DE VALIDAÇÃO

### 21. Erro de Validação de Parâmetros
- **Padrão**: `"[ERRO] VALIDAÇÃO DE PARÂMETROS FALHOU: {detalhes}"`
- **Contexto**: Parâmetros inválidos detectados
- **Ação**: Mostrar SweetAlert de erro de validação
- **Ícone**: `warning`

### 22. Erro Inesperado na Validação
- **Padrão**: `"[ERRO] ERRO INESPERADO NA VALIDAÇÃO: {detalhes}"`
- **Contexto**: Erro inesperado na validação
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

## 🔴 ERROS DE PROGRESSO

### 23. Progresso Não Disponível
- **Mensagem**: `"Progresso não disponível"`
- **Contexto**: Erro ao incluir progresso
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

## 🔴 ERROS GENÉRICOS (Exceções)

### 24. Erros de Timeout
- **Padrão**: `"TimeoutError: Page.wait_for_selector: Timeout {tempo}ms exceeded"`
- **Contexto**: Timeout em operações do Playwright
- **Ação**: Mostrar SweetAlert de timeout
- **Ícone**: `warning`

### 25. Erros de Elemento Não Encontrado
- **Padrão**: `"ElementNotFoundError: Element not found"`
- **Contexto**: Elemento não encontrado na página
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 26. Erros de Navegação
- **Padrão**: `"NavigationError: {detalhes}"`
- **Contexto**: Erro na navegação da página
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 27. Erros do Playwright
- **Padrão**: `"PlaywrightError: {detalhes}"`
- **Contexto**: Erro geral do Playwright
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 28. Erros de Browser
- **Padrão**: `"BrowserError: {detalhes}"`
- **Contexto**: Erro do navegador
- **Ação**: Mostrar SweetAlert de erro técnico
- **Ícone**: `error`

### 29. Erros Genéricos
- **Padrão**: Qualquer string que não se encaixe nos padrões acima
- **Contexto**: Erro genérico não categorizado
- **Ação**: Mostrar SweetAlert de erro genérico
- **Ícone**: `error`

## 📋 RESUMO PARA IMPLEMENTAÇÃO

### Códigos de Erro Específicos:
- `9003`: Cotação manual necessária
- `9004`: Tela final não detectada
- `9102`: Erro na navegação

### Padrões de Mensagem:
- `"Tela X falhou"` (X = 1-15, Zero KM)
- `"Cotação manual necessária"`
- `"Falha na captura"`
- `"Progresso não disponível"`
- `"[ERRO] VALIDAÇÃO DE PARÂMETROS FALHOU: {detalhes}"`
- `"[ERRO] ERRO INESPERADO NA VALIDAÇÃO: {detalhes}"`
- `"TimeoutError: {detalhes}"`
- `"ElementNotFoundError: {detalhes}"`
- `"NavigationError: {detalhes}"`
- `"PlaywrightError: {detalhes}"`
- `"BrowserError: {detalhes}"`

### Ícones por Tipo:
- `info`: Cotação manual (9003)
- `warning`: Timeout, Validação de parâmetros
- `error`: Todos os demais erros

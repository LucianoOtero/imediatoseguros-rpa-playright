# 🚀 **SISTEMA DE EXCEPTION HANDLER - RPA SELENIUM**

## 📋 **Visão Geral**

Este sistema captura exceções Selenium e as formata de forma limpa para o terminal, suprimindo stacktraces técnicos e mantendo apenas informações úteis para o usuário. Todos os detalhes técnicos são registrados nos logs para debugging.

## ✨ **Benefícios**

- **Terminal Limpo**: Sem stacktraces técnicos poluindo a saída
- **Logs Completos**: Todos os detalhes técnicos preservados para debugging
- **Mensagens Profissionais**: Warnings formatados e compreensíveis
- **Compatibilidade PHP**: Saída limpa para captura por programas PHP
- **Sistema de Retry**: Mantém funcionalidade de tentativas automáticas

## 🔧 **Como Funciona**

### **ANTES (Técnico e Poluído):**
```
[WARNING] Tentativa 1 falhou: Message: element not interactable
  (Session info: chrome=139.0.7258.155)
Stacktrace:
        GetHandleVerifier [0x0x7ff6900078d5+2802725]
        GetHandleVerifier [0x0x7ff68fd6eb80+79568]
        (No symbol) [0x0x7ff68fb0bf2c]
        ...
```

### **DEPOIS (Limpo e Profissional):**
```
⚠️  [WARNING] Elemento não interativo - Campo Estado Civil
    🔄 Tentando novamente automaticamente...
    📍 Aguardando elemento ficar disponível...
```

### **LOGS (Detalhes Completos):**
```
[2025-01-31 15:30:45] WARNING: EXCEÇÃO SELENIUM DETALHADA: {
    'timestamp': '2025-01-31T15:30:45.123',
    'exception_count': 1,
    'exception_type': 'ElementNotInteractableException',
    'exception_message': 'element not interactable',
    'context': 'Campo Estado Civil',
    'traceback': 'Traceback completo...',
    'element_info': {...},
    'session_info': {...}
}
```

## 🚀 **Implementação no RPA**

### **1. Importar o Sistema**
```python
from exception_handler import (
    handle_selenium_exception,
    handle_retry_attempt,
    format_success_message,
    set_session_info
)
```

### **2. Substituir Mensagens de Erro**

**ANTES:**
```python
try:
    opcao = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(1)")
    opcao.click()
    exibir_mensagem(f"✅ Campo Estado Civil selecionado")
except Exception as e1:
    exibir_mensagem(f"⚠️ Tentativa 1 falhou: {e1}")  # ❌ Técnico e poluído
```

**DEPOIS:**
```python
try:
    opcao = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(1)")
    opcao.click()
    message = format_success_message("Campo Estado Civil selecionado")
    exibir_mensagem(message)
except Exception as e1:
    message = handle_retry_attempt(1, 3, e1, "Campo Estado Civil")
    exibir_mensagem(message)  # ✅ Limpo e profissional
```

### **3. Configurar Informações da Sessão**
```python
set_session_info({
    "tela": "Estado Civil Condutor",
    "elemento": "estadoCivilTelaCondutorPrincipal",
    "valor": estado_civil_condutor
})
```

### **4. Usar com Informações Detalhadas**
```python
element_info = {
    "selector": "button#continuar",
    "tag_name": "button",
    "text": "Continuar",
    "url": driver.current_url,
    "page_title": driver.title
}

message = handle_selenium_exception(
    exception=e,
    context="Botão Continuar",
    element_info=element_info,
    show_retry_info=True
)
```

## 📁 **Arquivos do Sistema**

- **`exception_handler.py`** - Sistema principal de captura e formatação
- **`exemplo_uso_exception_handler.py`** - Exemplos práticos de implementação
- **`rpa_exceptions.log`** - Logs detalhados de todas as exceções
- **`README_EXCEPTION_HANDLER.md`** - Esta documentação

## 🔍 **Tipos de Exceção Suportados**

- **ElementNotInteractableException** → "Elemento não interativo"
- **ElementClickInterceptedException** → "Elemento interceptado por outro"
- **StaleElementReferenceException** → "Elemento desatualizado"
- **TimeoutException** → "Tempo limite excedido"
- **NoSuchElementException** → "Elemento não encontrado"
- **WebDriverException** → "Erro do navegador"

## 📊 **Exemplo de Implementação Completa**

```python
def implementar_tela_estado_civil(driver, estado_civil_condutor):
    """Implementa seleção de Estado Civil com Exception Handler"""
    
    # Configurar contexto para logging
    set_session_info({
        "tela": "Estado Civil Condutor",
        "elemento": "estadoCivilTelaCondutorPrincipal",
        "valor": estado_civil_condutor
    })
    
    opcao_selecionada = False
    
    # Tentativa 1: CSS Selector direto
    try:
        opcao = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(1)")
        opcao.click()
        message = format_success_message("Campo Estado Civil selecionado", "CSS Selector")
        exibir_mensagem(message)
        opcao_selecionada = True
        
    except Exception as e1:
        message = handle_retry_attempt(1, 3, e1, "Campo Estado Civil")
        exibir_mensagem(message)
        
        # Tentativa 2: JavaScript click
        try:
            opcao = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(1)")
            driver.execute_script("arguments[0].click();", opcao)
            message = format_success_message("Campo Estado Civil selecionado", "JavaScript")
            exibir_mensagem(message)
            opcao_selecionada = True
            
        except Exception as e2:
            message = handle_retry_attempt(2, 3, e2, "Campo Estado Civil")
            exibir_mensagem(message)
            
            # Tentativa 3: ActionChains
            try:
                opcao = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(1)")
                ActionChains(driver).move_to_element(opcao).click().perform()
                message = format_success_message("Campo Estado Civil selecionado", "ActionChains")
                exibir_mensagem(message)
                opcao_selecionada = True
                
            except Exception as e3:
                message = handle_retry_attempt(3, 3, e3, "Campo Estado Civil")
                exibir_mensagem(message)
    
    if not opcao_selecionada:
        exibir_mensagem("❌ Todas as tentativas de seleção falharam")
    
    return opcao_selecionada
```

## 🎯 **Resultado Final**

### **Terminal (Limpo e Profissional):**
```
⚠️  [WARNING] Elemento não interativo - Campo Estado Civil
    🔄 Tentativa 1 de 3...
    📍 Aguardando elemento ficar disponível...
⚠️  [WARNING] Elemento não interativo - Campo Estado Civil
    🔄 Tentativa 2 de 3...
    📍 Aguardando elemento ficar disponível...
✅ Campo Estado Civil selecionado - ActionChains
```

### **Logs (Detalhes Completos para Debugging):**
```
[2025-01-31 15:30:45] WARNING: EXCEÇÃO SELENIUM DETALHADA: {
    'timestamp': '2025-01-31T15:30:45.123',
    'exception_count': 1,
    'exception_type': 'ElementNotInteractableException',
    'exception_message': 'element not interactable',
    'context': 'Retry 1/3 - Campo Estado Civil',
    'traceback': 'Traceback completo...',
    'tela': 'Estado Civil Condutor',
    'elemento': 'estadoCivilTelaCondutorPrincipal',
    'valor': 'Casado ou União Estável'
}
```

## 🚀 **Próximos Passos**

1. **Implementar** o sistema no seu RPA principal
2. **Substituir** todas as mensagens de erro técnicas
3. **Configurar** informações de sessão para melhor logging
4. **Testar** com diferentes cenários de erro
5. **Monitorar** logs para debugging avançado

## 📞 **Suporte**

Para dúvidas ou melhorias no sistema:
- Consulte os exemplos em `exemplo_uso_exception_handler.py`
- Verifique os logs em `rpa_exceptions.log`
- Analise o código fonte em `exception_handler.py`

---

**🎯 Resultado: Terminal limpo + Logs completos + Debugging profissional!**

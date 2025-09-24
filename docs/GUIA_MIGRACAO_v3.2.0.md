# 🚀 GUIA DE MIGRAÇÃO - v3.2.0
## RPA Tô Segurado - Playwright

---

## 📋 **VISÃO GERAL DA MIGRAÇÃO**

A **versão v3.2.0** introduz a **Tela Zero KM** como funcionalidade condicional, expandindo significativamente as capacidades do RPA. Este guia orienta a migração de versões anteriores.

### **🎯 PRINCIPAIS MUDANÇAS:**
- ✅ **Nova Tela Zero KM** (condicional)
- ✅ **Campo tipo_franquia** na captura de dados
- ✅ **Documentação completa** de parâmetros
- ✅ **Troubleshooting específico** para Zero KM
- ✅ **16 telas implementadas** (anteriormente 15)

---

## 🔄 **MIGRAÇÃO POR VERSÃO**

### **📦 De v3.1.x para v3.2.0**

#### **✅ Mudanças Automáticas:**
- Sistema detecta automaticamente a Tela Zero KM
- Campo `zero_km` já existe no `parametros.json`
- Nenhuma ação manual necessária

#### **🔧 Ações Recomendadas:**
1. **Atualizar parâmetros** (opcional):
```json
{
  "zero_km": false  // Verificar se está definido
}
```

2. **Testar nova funcionalidade**:
```bash
python executar_rpa_imediato_playwright.py
```

3. **Verificar logs**:
```bash
tail -f logs/rpa_imediato_playwright_YYYYMMDD.log
```

---

### **📦 De v3.0.x para v3.2.0**

#### **⚠️ Mudanças Importantes:**
- Nova estrutura de captura de dados
- Campo `tipo_franquia` adicionado
- Tela Zero KM implementada

#### **🔧 Ações Necessárias:**

1. **Atualizar parametros.json**:
```json
{
  "zero_km": false,  // NOVO - Adicionar este campo
  // ... outros campos existentes
}
```

2. **Verificar captura de dados**:
```python
# Verificar se tipo_franquia está sendo capturado
resultado = executar_rpa_completo(json.dumps(parametros))
if 'tipo_franquia' in resultado['data']['dados_capturados']['plano_recomendado']:
    print("✅ Campo tipo_franquia capturado!")
```

3. **Testar execução completa**:
```bash
python executar_rpa_imediato_playwright.py
```

---

### **📦 De v2.x para v3.2.0**

#### **🚨 MIGRAÇÃO MAJOR - REQUER ATENÇÃO**

#### **⚠️ Mudanças Críticas:**
- Migração completa de Selenium para Playwright
- Nova estrutura de arquivos
- Mudanças na API de retorno
- Novos campos obrigatórios

#### **🔧 Passos de Migração:**

1. **Backup completo**:
```bash
# Criar backup da versão atual
cp -r imediatoseguros-rpa-playwright/ backup_v2x_$(date +%Y%m%d)/
```

2. **Atualizar dependências**:
```bash
pip install playwright
playwright install
```

3. **Migrar parametros.json**:
```json
{
  "configuracao": {
    "log": true,
    "display": true,
    "log_rotacao_dias": 90,
    "log_nivel": "INFO",
    "tempo_estabilizacao": 0.5,
    "tempo_carregamento": 0.5,
    "tempo_estabilizacao_tela5": 2,
    "tempo_carregamento_tela5": 5,
    "tempo_estabilizacao_tela15": 3,
    "tempo_carregamento_tela15": 5,
    "inserir_log": true,
    "visualizar_mensagens": true,
    "eliminar_tentativas_inuteis": true
  },
  "autenticacao": {
    "email_login": "seu_email@exemplo.com",
    "senha_login": "sua_senha",
    "manter_login_atual": true
  },
  "url": "https://www.app.tosegurado.com.br/imediatosolucoes",
  "placa": "ABC1234",
  "marca": "TOYOTA",
  "modelo": "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
  "ano": "2009",
  "zero_km": false,  // NOVO
  "combustivel": "Flex",
  "veiculo_segurado": "Não",
  "cep": "03317-000",
  "endereco_completo": "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
  "uso_veiculo": "Pessoal",
  "nome": "NOME COMPLETO",
  "cpf": "00000000000",
  "data_nascimento": "01/01/1990",
  "sexo": "Masculino",
  "estado_civil": "Solteiro",
  "email": "email@exemplo.com",
  "celular": "11999999999",
  "endereco": "Endereço completo",
  "condutor_principal": true,
  "nome_condutor": "NOME CONDUTOR",
  "cpf_condutor": "00000000000",
  "data_nascimento_condutor": "01/01/1990",
  "sexo_condutor": "Feminino",
  "estado_civil_condutor": "Solteiro",
  "local_de_trabalho": false,
  "estacionamento_proprio_local_de_trabalho": false,
  "local_de_estudo": false,
  "estacionamento_proprio_local_de_estudo": false,
  "garagem_residencia": true,
  "portao_eletronico": "Eletronico",
  "reside_18_26": "Não",
  "sexo_do_menor": "N/A",
  "faixa_etaria_menor_mais_novo": "N/A",
  "kit_gas": false,
  "blindado": false,
  "financiado": false,
  "continuar_com_corretor_anterior": true
}
```

4. **Atualizar código de integração**:
```python
# ANTES (v2.x)
from executar_rpa_imediato import executar_todas_telas

# DEPOIS (v3.2.0)
from executar_rpa_imediato_playwright import executar_rpa_completo
```

5. **Atualizar tratamento de retorno**:
```python
# ANTES (v2.x)
if resultado['success']:
    dados = resultado['data']['dados_capturados']

# DEPOIS (v3.2.0)
if resultado['status'] == 'sucesso':
    dados = resultado['dados']['dados_capturados']
    # Novo campo disponível
    tipo_franquia = dados['plano_recomendado']['tipo_franquia']
```

---

## 🧪 **TESTES DE MIGRAÇÃO**

### **✅ Checklist de Validação:**

#### **1. Teste Básico:**
```bash
# Executar RPA completo
python executar_rpa_imediato_playwright.py

# Verificar se executa sem erros
echo $?  # Deve retornar 0
```

#### **2. Teste de Parâmetros:**
```bash
# Verificar documentação de parâmetros
python executar_rpa_imediato_playwright.py --docs params

# Deve mostrar todos os 40+ campos
```

#### **3. Teste de Tela Zero KM:**
```json
{
  "zero_km": true,
  "placa": "EYQ4J41"  // Placa que ativa Zero KM
}
```

#### **4. Teste de Captura de Dados:**
```python
# Verificar se tipo_franquia está sendo capturado
resultado = executar_rpa_completo(json.dumps(parametros))
assert 'tipo_franquia' in resultado['dados']['dados_capturados']['plano_recomendado']
```

---

## 🔧 **CONFIGURAÇÃO PÓS-MIGRAÇÃO**

### **📊 Monitoramento:**

#### **1. Logs de Execução:**
```bash
# Monitorar logs em tempo real
tail -f logs/rpa_imediato_playwright_$(date +%Y%m%d).log
```

#### **2. Métricas de Performance:**
- **Tempo médio**: 180-200 segundos (16 telas)
- **Taxa de sucesso**: 98%+
- **Tela Zero KM**: Aparece em ~30% das execuções

#### **3. Alertas Recomendados:**
```python
# Verificar se Tela Zero KM está funcionando
if 'tela_zero_km_executada' in resultado['dados']:
    print("✅ Tela Zero KM funcionando!")
```

---

## 🚨 **PROBLEMAS COMUNS DE MIGRAÇÃO**

### **❌ Erro: "Campo zero_km não encontrado"**

#### **Solução:**
```json
{
  "zero_km": false  // Adicionar ao parametros.json
}
```

### **❌ Erro: "Módulo executar_rpa_imediato não encontrado"**

#### **Solução:**
```python
# Atualizar import
from executar_rpa_imediato_playwright import executar_rpa_completo
```

### **❌ Erro: "Campo tipo_franquia não encontrado"**

#### **Solução:**
```python
# Verificar se está usando v3.2.0
print(f"Versão: {resultado['versao']}")  # Deve ser "3.2.0"
```

### **❌ Erro: "Strict Mode Violation"**

#### **Solução:**
```bash
# Atualizar para versão mais recente
git pull origin main
```

---

## 📚 **RECURSOS DE MIGRAÇÃO**

### **📖 Documentação:**
- [Documentação Técnica Zero KM](docs/DOCUMENTACAO_TELA_ZERO_KM.md)
- [Troubleshooting Zero KM](docs/TROUBLESHOOTING_TELA_ZERO_KM.md)
- [README Principal](README.md)
- [README Playwright](README_PLAYWRIGHT.md)

### **🔗 Comandos Úteis:**
```bash
# Verificar versão atual
python executar_rpa_imediato_playwright.py --docs completa

# Testar parâmetros
python executar_rpa_imediato_playwright.py --docs params

# Executar com logs detalhados
python executar_rpa_imediato_playwright.py --log
```

### **🛠️ Ferramentas de Debug:**
```python
# Verificar estrutura de retorno
import json
resultado = executar_rpa_completo(json.dumps(parametros))
print(json.dumps(resultado, indent=2, ensure_ascii=False))
```

---

## 📞 **SUPORTE À MIGRAÇÃO**

### **🆘 Quando Contatar Suporte:**

- Erro durante migração de v2.x para v3.2.0
- Campo `tipo_franquia` não sendo capturado
- Tela Zero KM não funcionando
- Problemas de performance pós-migração

### **📧 Informações para Envio:**

```
Assunto: [MIGRAÇÃO v3.2.0] Problema específico

Versão anterior: v2.x
Versão atual: v3.2.0
Erro: [mensagem completa]
Logs: [últimas 20 linhas]
Configuração: [parametros.json relevante]
```

---

## 🎯 **ROADMAP PÓS-MIGRAÇÃO**

### **📅 Próximas Versões:**

#### **v3.3.0 (Planejada):**
- [ ] Melhorias de performance
- [ ] Cache de detecção Zero KM
- [ ] Métricas avançadas

#### **v3.4.0 (Futuro):**
- [ ] Suporte a variantes da Tela Zero KM
- [ ] Sistema de sessões concorrentes
- [ ] Dashboard de monitoramento

### **🔮 Funcionalidades Futuras:**
- [ ] Suporte a múltiplos navegadores
- [ ] Execução paralela
- [ ] Integração CI/CD
- [ ] API REST

---

## ✅ **CHECKLIST FINAL DE MIGRAÇÃO**

### **📋 Validação Completa:**

- [ ] **Backup criado** da versão anterior
- [ ] **Dependências atualizadas** (Playwright)
- [ ] **parametros.json atualizado** com zero_km
- [ ] **Código de integração atualizado**
- [ ] **Teste básico executado** com sucesso
- [ ] **Tela Zero KM testada** (se aplicável)
- [ ] **Campo tipo_franquia verificado**
- [ ] **Logs monitorados** por 24h
- [ ] **Performance validada**
- [ ] **Documentação lida**

### **🎉 Migração Concluída:**

Se todos os itens acima estão marcados, sua migração para v3.2.0 foi concluída com sucesso!

---

**📅 Última Atualização**: 24/09/2025  
**👨‍💻 Desenvolvedor**: RPA Tô Segurado Team  
**🔖 Versão**: v3.2.0  
**📋 Status**: ✅ **MIGRAÇÃO DISPONÍVEL**

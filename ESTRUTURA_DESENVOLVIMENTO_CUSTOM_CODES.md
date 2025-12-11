# 🏗️ ESTRUTURA DE DESENVOLVIMENTO - CUSTOM CODES WEBFLOW

## 📋 VISÃO GERAL

Sistema de desenvolvimento controlado para os custom codes do website **segurosimediato.com.br**, com ambiente de desenvolvimento e produção separados.

---

## 🎯 OBJETIVOS

1. **Ambiente Isolado de Desenvolvimento**: Testes seguros sem afetar produção
2. **Versionamento**: Controle completo de versões e mudanças
3. **Backup Automático**: Proteção contra perdas de dados
4. **Validação Multi-Stage**: Testes rigorosos antes do deploy
5. **Documentação**: Registro de todas as alterações
6. **Rollback Rápido**: Retorno a versões anteriores em caso de falha

---

## 📁 ESTRUTURA DE DIRETÓRIOS PROPOSTA

```
C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\
│
├── custom code webflow/                    # 📂 PASTA ORIGINAL (mantida como backup)
│   ├── Footer Code Site Definitivo.js
│   ├── Head code Site.js
│   ├── Inside Head Tag Pagina.js
│   ├── webflow_injection_limpo.js
│   └── ...
│
└── custom-codes-webflow-development/        # 🆕 NOVA ESTRUTURA DE DESENVOLVIMENTO
    │
    ├── 01-BACKUP/                          # 🔐 Backups automáticos diários
    │   ├── YYYY-MM-DD/
    │   │   ├── Footer Code Site Definitivo.js
    │   │   ├── webflow_injection_limpo.js
    │   │   └── backup-log.txt
    │   └── auto-backup-last.txt            # Último backup realizado
    │
    ├── 02-DEVELOPMENT/                      # 🧪 Desenvolvimento Ativo
    │   ├── custom-codes/                   # Footer, Head, Inside Head Tags
    │   │   ├── Footer Code Site Definitivo.js
    │   │   ├── Head code Site.js
    │   │   ├── Inside Head Tag Pagina.js
    │   │   └── changelog.md                 # Registro de mudanças
    │   │
    │   ├── webflow-injection/
    │   │   ├── webflow-injection-main.js
    │   │   ├── webflow-injection-v1.0.js
    │   │   └── changelog.md
    │   │
    │   ├── modals/                         # 🆕 Modais e componentes
    │   │   ├── modal-whatsapp/
    │   │   │   ├── MODAL_WHATSAPP_DEFINITIVO.js
    │   │   │   ├── modal-whatsapp-v1.0.js
    │   │   │   └── changelog.md
    │   │   │
    │   │   └── modal-rpa/
    │   │       ├── modal-rpa-main.js
    │   │       └── changelog.md
    │   │
    │   └── components/                      # Componentes reutilizáveis
    │       ├── validators.js
    │       ├── utils.js
    │       └── constants.js
    │
    ├── 03-STAGING/                         # 🧪 Ambiente de Teste (Webflow Dev)
    │   ├── footer-code-staging.js          # Versão testada no dev
    │   ├── webflow-injection-staging.js
    │   ├── modal-whatsapp-staging.js
    │   └── staging-log.txt                 # Log de validações
    │
    ├── 04-PRODUCTION/                      # 🚀 Código em Produção
    │   ├── footer-code-production.js       # Versão ativa no site
    │   ├── webflow-injection-production.js
    │   ├── modal-whatsapp-production.js
    │   └── production-version.txt           # Versão atual em produção
    │
    ├── 05-TESTS/                           # 🧪 Arquivos de Teste
    │   ├── test-footer.html
    │   ├── test-modal-whatsapp.html
    │   ├── test-modal-rpa.html
    │   └── test-results/
    │       └── YYYY-MM-DD-results.json
    │
    ├── 06-DOCUMENTATION/                   # 📚 Documentação
    │   ├── ARCHITECTURE.md                 # Arquitetura do sistema
    │   ├── DEPLOYMENT.md                   # Guia de deployment
    │   ├── ROLLBACK_GUIDE.md              # Guia de rollback
    │   └── CHANGELOG_MASTER.md             # Registro geral de mudanças
    │
    └── 07-SCRIPTS/                         # 🛠️ Scripts Úteis
        ├── backup.js                       # Script de backup automático
        ├── deploy-dev.js                   # Deploy para desenvolvimento
        ├── deploy-prod.js                  # Deploy para produção
        ├── rollback.js                     # Rollback para versão anterior
        └── validate.js                     # Validação de código
```

---

## 🔄 FLUXO DE DESENVOLVIMENTO PROPOSTO

### **FASE 1: DESENVOLVIMENTO LOCAL** 💻
```
1. Desenvolver código em: 02-DEVELOPMENT/footer-code/footer-code-main.js
2. Testar localmente em: 05-TESTS/test-footer.html
3. Validar funcionalidades
4. Commit com mensagem descritiva
```

### **FASE 2: DEPLOY DESENVOLVIMENTO** 🧪
```
1. Copiar código para: 03-STAGING/
2. Inserir custom code no Webflow DEV: segurosimediato-8119bf26e77bf4ff336a58e.webflow.io
3. Testar funcionalidades no ambiente de dev
4. Validar em diferentes dispositivos
5. Registrar resultados em: staging-log.txt
```

### **FASE 3: VALIDAÇÃO** ✅
```
1. Checklist de validação:
   ✓ Funciona em mobile?
   ✓ Funciona em desktop?
   ✓ Não quebra outras funcionalidades?
   ✓ Performance adequada?
   ✓ Sem erros no console?
   ✓ Tracking/GTM funcionando?

2. Após validação, aprovar para produção
```

### **FASE 4: DEPLOY PRODUÇÃO** 🚀
```
1. Backup automático do código atual em: 01-BACKUP/YYYY-MM-DD/
2. Copiar código validado para: 04-PRODUCTION/
3. Inserir custom code no Webflow PROD: segurosimediato.com.br
4. Monitorar por 24-48h
5. Registrar em: production-version.txt
```

### **FASE 5: ROLLBACK (SE NECESSÁRIO)** ↩️
```
1. Identificar problema em produção
2. Executar rollback.js
3. Restaurar versão anterior de: 01-BACKUP/
4. Registrar problema em: CHANGELOG_MASTER.md
```

---

## 📊 CONTROLE DE VERSÕES

### **Sistema de Numeração**
```
v1.0 → Versão inicial
v1.1 → Correção de bugs
v1.2 → Pequenas melhorias
v2.0 → Mudança significativa de funcionalidade
```

### **Arquivo CHANGELOG.md**
```markdown
## [v1.2] - 2024-01-XX
### Adicionado
- Modal WhatsApp progressivo
- Validação de campos em tempo real

### Modificado
- Footer Code com nova estrutura
- GTM conversion tracking

### Corrigido
- Bug no foco de campos
- Erro de validação CPF

### Removido
- SweetAlerts do modal (substituído por feedback inline)
```

---

## 🛠️ SCRIPTS AUTOMATIZADOS

### **1. backup.js**
```javascript
// Backup automático diário
// Cria backup com timestamp
// Registra em backup-log.txt
// Mantém últimos 30 dias
```

### **2. deploy-dev.js**
```javascript
// Copia código de DEVELOPMENT para STAGING
// Cria arquivo staging-comparison.txt
// Alerta sobre mudanças
// Cria tag de versão
```

### **3. deploy-prod.js**
```javascript
// Backup automático antes do deploy
// Copia código de STAGING para PRODUCTION
// Valida integridade do código
// Atualiza production-version.txt
// Envia notificação (opcional)
```

### **4. rollback.js**
```javascript
// Lista versões disponíveis
// Restaura versão especificada
// Valida código restaurado
// Registra ação em CHANGELOG_MASTER.md
```

### **5. validate.js**
```javascript
// Valida sintaxe JavaScript
// Verifica dependências
// Testa compatibilidade
// Gera relatório de validação
```

---

## 📚 DOCUMENTAÇÃO

### **ARCHITECTURE.md**
Documentação técnica da arquitetura do sistema.

### **DEPLOYMENT.md**
Guia passo-a-passo para deployment.

### **ROLLBACK_GUIDE.md**
Procedimento de rollback em caso de falha.

### **CHANGELOG_MASTER.md**
Registro completo de todas as mudanças.

---

## 🔐 SEGURANÇA E BACKUP

### **Backup Automático**
- Backups diários às 23:59
- Retenção de 30 dias
- Compressão automática
- Verificação de integridade

### **Versionamento**
- Tags Git para cada versão
- Changelog detalhado
- Histórico completo de mudanças

---

## ✅ CHECKLIST DE DEPLOYMENT

### **ANTES DO DEPLOY**
- [ ] Código testado localmente
- [ ] Testes de validação passaram
- [ ] Backup criado
- [ ] Documentação atualizada
- [ ] Changelog atualizado

### **DEPLOY EM DEV**
- [ ] Código inserido no Webflow DEV
- [ ] Testado em mobile
- [ ] Testado em desktop
- [ ] GTM funcionando
- [ ] Sem erros no console

### **DEPLOY EM PROD**
- [ ] Aprovado pela equipe
- [ ] Backup de produção criado
- [ ] Código inserido no Webflow PROD
- [ ] Monitoramento ativado
- [ ] Equipe notificada

### **PÓS-DEPLOY**
- [ ] Monitoramento por 24-48h
- [ ] Feedback coletado
- [ ] Documentação finalizada
- [ ] Métricas registradas

---

## 🎯 AMBIENTES

### **🧪 DESENVOLVIMENTO**
```
URL: https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io/
Propósito: Testes e desenvolvimento
Acesso: Equipe de desenvolvimento
```

### **🚀 PRODUÇÃO**
```
URL: segurosimediato.com.br
Propósito: Site ativo para clientes
Acesso: Público
```

---

## 📞 CONTROLE DE QUALIDADE

### **Validações Obrigatórias**
1. **Sintaxe**: JavaScript válido
2. **Compatibilidade**: Navegadores modernos
3. **Performance**: Tempo de carregamento < 2s
4. **Mobile-First**: Responsive design
5. **Accessibility**: ARIA attributes
6. **Security**: XSS prevention
7. **Tracking**: GTM funcionando
8. **Integração**: RPA funcionando

---

## 🚀 PRÓXIMOS PASSOS

1. ~~**Criar estrutura de diretórios**~~ ✅ **CONCLUÍDO**
2. **Configurar scripts automatizados**
3. **Estabelecer fluxo de trabalho**
4. **Treinar equipe**
5. **Implementar monitoramento**

---

**Desenvolvido por:** Equipe de Desenvolvimento Imediato Seguros  
**Data:** 2024-01-XX  
**Versão:** 1.0




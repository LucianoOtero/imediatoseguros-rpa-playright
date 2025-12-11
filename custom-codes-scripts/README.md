# 🛠️ SCRIPTS DE AUTOMAÇÃO - CUSTOM CODES WEBFLOW

Este diretório contém scripts automatizados para gerenciar o desenvolvimento, deploy e rollback dos custom codes do website segurosimediato.com.br.

---

## 📋 SCRIPTS DISPONÍVEIS

### 1. **backup.js** 📦
Cria backup automático dos custom codes.

```bash
node backup.js
```

**Funcionalidades:**
- Cria backup diário com timestamp
- Mantém últimos 30 dias de backup
- Remove backups antigos automaticamente
- Registra log de operação

---

### 2. **deploy-dev.js** 🧪
Deploy para ambiente de desenvolvimento (Webflow DEV).

```bash
node deploy-dev.js
```

**Funcionalidades:**
- Copia código de DEVELOPMENT para STAGING
- Cria log de comparação
- Prepara código para inserção no Webflow DEV
- Alerta sobre mudanças

**Próximos passos após o script:**
1. Acessar Webflow Editor (DEV)
2. Inserir custom codes da pasta STAGING
3. Publicar e testar

---

### 3. **deploy-prod.js** 🚀
Deploy para ambiente de produção (Webflow PROD).

```bash
node deploy-prod.js
```

**ATENÇÃO:** Este script faz deploy em PRODUÇÃO!

**Funcionalidades:**
- Solicita confirmação obrigatória
- Cria backup automático antes do deploy
- Copia código de STAGING para PRODUCTION
- Valida integridade do código
- Atualiza versão de produção

**Próximos passos após o script:**
1. Acessar Webflow Editor (PROD)
2. Inserir custom codes da pasta PRODUCTION
3. Publicar alterações
4. Testar imediatamente
5. Monitorar por 24-48h

---

### 4. **rollback.js** ↩️
Reverte para versão anterior em caso de problema.

```bash
node rollback.js
```

**Funcionalidades:**
- Lista backups disponíveis
- Permite selecionar backup específico
- Restaura arquivos do backup
- Cria log de rollback

**Quando usar:**
- Problema crítico em produção
- Bug que afeta funcionalidades
- Erro de validação
- Necessidade de retorno rápido

---

## 🔄 FLUXO DE TRABALHO SUGERIDO

```
1. Desenvolver
   ↓
2. Testar localmente
   ↓
3. Fazer deploy para DEV
   ├── node deploy-dev.js
   ├── Inserir no Webflow DEV
   └── Testar funcionalidades
   ↓
4. Validar em DEV
   ├── Mobile ✓
   ├── Desktop ✓
   ├── GTM ✓
   └── Performance ✓
   ↓
5. Fazer deploy para PROD
   ├── node deploy-prod.js
   ├── Inserir no Webflow PROD
   └── Publicar
   ↓
6. Monitorar (24-48h)
   ├── Verificar métricas
   ├── Coletar feedback
   └── Se problema → node rollback.js
```

---

## 📁 ESTRUTURA DE DIRETÓRIOS

```
custom-codes-webflow-development/
├── 01-BACKUP/          # Backups automáticos
├── 02-DEVELOPMENT/     # Código em desenvolvimento
├── 03-STAGING/         # Código para Webflow DEV
├── 04-PRODUCTION/      # Código para Webflow PROD
├── 05-TESTS/          # Arquivos de teste
├── 06-DOCUMENTATION/   # Documentação
└── 07-SCRIPTS/        # Scripts (este diretório)
```

---

## ⚙️ CONFIGURAÇÃO

Os scripts já estão configurados com os diretórios padrão. Para alterar:

1. Editar `CONFIG` no início de cada script
2. Ajustar caminhos conforme necessário
3. Testar antes de usar em produção

---

## 🚨 SEGURANÇA

### **ANTES DE CADA DEPLOY:**
- [ ] Código testado localmente
- [ ] Backup criado (automático)
- [ ] Validações passaram
- [ ] Documentação atualizada

### **DURANTE O DEPLOY:**
- [ ] Confirmar visualmente
- [ ] Verificar sintaxe
- [ ] Testar imediatamente após deploy

### **APÓS O DEPLOY:**
- [ ] Monitorar por 24-48h
- [ ] Verificar métricas
- [ ] Coletar feedback
- [ ] Documentar problemas

---

## 📞 SUPORTE

Em caso de problema:
1. Verificar `rollback-log.txt`
2. Executar `rollback.js`
3. Investigar causa
4. Documentar problema
5. Criar fix e testar em DEV

---

## 🎯 EXEMPLOS DE USO

### **Backup Diário (Agendar no Windows):**
```bash
# Executar diariamente às 23:59
node custom-codes-scripts/backup.js
```

### **Deploy para Desenvolvimento:**
```bash
# Desenvolvimento ativo
node custom-codes-scripts/deploy-dev.js

# Manual: Inserir códigos no Webflow DEV
# Publicar
# Testar
```

### **Deploy para Produção:**
```bash
# Após validação em DEV
node custom-codes-scripts/deploy-prod.js

# Confirmar: DEPLOY-PROD
# Manual: Inserir códigos no Webflow PROD
# Publicar
# Monitorar
```

### **Rollback de Emergência:**
```bash
# Se problema em PROD
node custom-codes-scripts/rollback.js

# Selecionar backup
# Confirmar
# Manual: Inserir códigos no Webflow PROD
```

---

**Desenvolvido por:** Equipe de Desenvolvimento Imediato Seguros  
**Versão:** 1.0





















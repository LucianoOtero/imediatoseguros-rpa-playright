# 🔑 GUIA: CRIAR CREDENCIAIS IAM PARA AMAZON SES

**Status Atual:** ✅ Domínio e email verificados  
**Próximo Passo:** Criar credenciais para código PHP enviar emails

---

## 🎯 O QUE VOCÊ ESTÁ FAZENDO AGORA

Criar um **usuário IAM** (Identity and Access Management) que o código PHP usará para enviar emails via Amazon SES.

**Por que precisa disso?**
- O código PHP precisa de credenciais (usuário/senha) para se autenticar na AWS
- Essas credenciais são diferentes do seu login pessoal do console AWS
- É mais seguro usar credenciais específicas para o aplicativo

---

## 📋 PASSO A PASSO

### **PASSO 1: ACESSAR IAM**

1. **No console AWS**, na barra de busca superior, digite: **"IAM"**
2. Clique em **"IAM"** (Identity and Access Management)
3. Ou acesse diretamente: https://console.aws.amazon.com/iam

**Você verá:** Dashboard do IAM

---

### **PASSO 2: CRIAR USUÁRIO**

1. **No menu lateral esquerdo**, clique em **"Users"** (Usuários)
2. Você verá lista de usuários (pode estar vazia)
3. Clique no botão **"Create user"** (Criar usuário) no canto superior direito

**Você verá:** Tela de criação de usuário

---

### **PASSO 3: CONFIGURAR NOME DO USUÁRIO**

**Passo 1 - User name:**
1. No campo **"User name"**, digite: `ses-email-sender`
   - Este é o nome do usuário que criaremos
   - Pode ser qualquer nome, mas use algo descritivo
2. **NÃO marque** a opção "Provide user access to the AWS Management Console"
   - Este usuário será usado apenas por código (não precisa acesso ao console)
3. Clique em **"Next"** (Próximo)

**Você verá:** Tela de permissões

---

### **PASSO 4: ATRIBUIR PERMISSÕES**

**Passo 2 - Permissions (Permissões):**

1. Você verá opções de permissões
2. Selecionar: **"Attach policies directly"** (Anexar políticas diretamente)
   - Esta opção permite escolher permissões específicas

3. **Na caixa de busca**, digite: **"SES"**
   - Isso filtrará as políticas relacionadas ao SES

4. **Selecionar a política:**
   - Marque a checkbox de **"AmazonSESFullAccess"**
   - Esta política dá acesso total ao SES (perfeito para este caso)
   
   **Descrição:** Permite enviar emails, verificar identidades, ver métricas, etc.

5. Clique em **"Next"** (Próximo)

**Você verá:** Tela de revisão

---

### **PASSO 5: REVISAR E CRIAR**

**Passo 3 - Review and create (Revisar e criar):**

1. Você verá um resumo:
   - **User name:** `ses-email-sender`
   - **Permissions:** `AmazonSESFullAccess`

2. **Revisar** se está tudo correto

3. Clique em **"Create user"** (Criar usuário)

**Você verá:** Mensagem de sucesso "User created successfully"

---

### **PASSO 6: CRIAR ACCESS KEY**

⚠️ **IMPORTANTE:** Este é o momento crítico - você obterá as credenciais!

#### **6.1. Opção A: Se aparecer botão automaticamente**

1. Você verá um botão **"Create access key"** na tela de sucesso
2. Clique nele

#### **6.2. Opção B: Se não aparecer automaticamente**

1. Na lista de usuários, **clique no usuário** `ses-email-sender` que acabou de criar
2. Você verá detalhes do usuário
3. Vá na aba **"Security credentials"** (Credenciais de segurança)
4. Role até a seção **"Access keys"**
5. Clique em **"Create access key"**

---

### **PASSO 7: CONFIGURAR ACCESS KEY**

1. Você verá uma tela de seleção do tipo de uso
2. Selecionar: **"Application running outside AWS"** (Aplicação rodando fora da AWS)
   - Ou **"Other"** se esta opção não aparecer
3. Marque a checkbox de confirmação (se houver)
4. Clique em **"Next"** (Próximo)

**Opção de descrição (opcional):**
- Pode deixar em branco ou adicionar: "Para envio de emails via SES"
- Clique em **"Create access key"**

---

### **PASSO 8: COPIAR CREDENCIAIS**

⚠️ **MOMENTO CRÍTICO:** Esta é a ÚNICA vez que verá o Secret Key completo!

**Você verá uma tela com duas informações:**

#### **1. Access key ID:**
```
AKIAIOSFODNN7EXAMPLE
```
- ✅ **Copie e salve** em local seguro
- É uma string que começa com `AKIA`

#### **2. Secret access key:**
```
wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```
- ✅ **Copie e salve** em local seguro
- ⚠️ **Esta é a ÚNICA vez que será mostrada!**
- Se perder, precisará criar uma nova access key

---

### **PASSO 9: SALVAR CREDENCIAIS**

⚠️ **NUNCA commitar estas credenciais no GitHub!**

#### **Opção 1: Arquivo .env (Recomendada)**

No servidor, criar arquivo `.env` na raiz do projeto:

```bash
cd /var/www/html/dev/webhooks
nano .env
```

Adicionar:
```
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=sa-east-1
```

**Proteger o arquivo:**
```bash
chmod 600 .env
chown www-data:www-data .env
```

#### **Opção 2: Arquivo de Config PHP (Alternativa)**

Criar arquivo `aws_config.php`:

```php
<?php
// ⚠️ NÃO versionar este arquivo no Git!
define('AWS_ACCESS_KEY_ID', 'AKIAIOSFODNN7EXAMPLE');
define('AWS_SECRET_ACCESS_KEY', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY');
define('AWS_REGION', 'sa-east-1');
```

**Adicionar no .gitignore:**
```
aws_config.php
.env
```

---

## ✅ VERIFICAÇÃO FINAL

Você deve ter:

- ✅ **Usuário IAM criado:** `ses-email-sender`
- ✅ **Permissão:** `AmazonSESFullAccess`
- ✅ **Access Key ID:** Copiado e salvo
- ✅ **Secret Access Key:** Copiado e salvo
- ✅ **Região:** Anotada (sa-east-1 ou a que você escolheu)

---

## 📝 INFORMAÇÕES PARA O CÓDIGO PHP

Agora você tem todas as informações para usar no código:

```php
// Substituir no código que criaremos depois:
define('AWS_ACCESS_KEY_ID', 'SUA_ACCESS_KEY_ID_AQUI');
define('AWS_SECRET_ACCESS_KEY', 'SUA_SECRET_ACCESS_KEY_AQUI');
define('AWS_REGION', 'sa-east-1'); // ou a região que você escolheu
```

---

## 🔒 SEGURANÇA

### **Boas Práticas:**

✅ **Salvar credenciais em arquivo seguro:**
- Arquivo `.env` não versionado
- Permissões restritas (chmod 600)
- Apenas o servidor web tem acesso

❌ **NUNCA fazer:**
- Commitar credenciais no GitHub
- Enviar credenciais por email não seguro
- Compartilhar credenciais publicamente
- Deixar arquivo com credenciais acessível publicamente

---

## ⏭️ PRÓXIMO PASSO

Após criar as credenciais:

1. ✅ **Salvar credenciais** em arquivo seguro
2. ✅ **Instalar AWS SDK** no servidor (composer require aws/aws-sdk-php)
3. ✅ **Criar função PHP** de envio de email
4. ✅ **Integrar no webhook** quando telefone for validado

---

## ❓ TROUBLESHOOTING

### **Problema: "Create access key" não aparece**

**Soluções:**
1. Verificar se está na aba correta (Security credentials)
2. Verificar se clicou no usuário correto
3. Tentar recarregar a página
4. Verificar se já existe access key (máximo 2 por usuário)

### **Problema: Esqueci o Secret Key**

**Soluções:**
1. Não é possível recuperar (AWS não armazena)
2. Criar nova access key:
   - IAM → Users → ses-email-sender → Security credentials
   - Criar nova access key
   - ⚠️ Se criar nova, a antiga continua funcionando até você deletá-la
   - Recomendação: Deletar a antiga após configurar a nova

### **Problema: "Access Denied" ao usar credenciais**

**Soluções:**
1. Verificar se Access Key ID está correto (copiou completo?)
2. Verificar se Secret Access Key está correto (copiou completo?)
3. Verificar se usuário tem permissão `AmazonSESFullAccess`
4. Verificar se região está correta no código

---

## ✅ CHECKLIST

Após completar:

- [ ] Usuário IAM `ses-email-sender` criado
- [ ] Permissão `AmazonSESFullAccess` atribuída
- [ ] Access Key ID copiado e salvo
- [ ] Secret Access Key copiado e salvo
- [ ] Credenciais salvas em arquivo seguro (não versionado)
- [ ] Região AWS anotada

---

**Status:** 📋 **Guia Completo - Criar Credenciais IAM**  
**Tempo estimado:** 10-15 minutos  
**Dificuldade:** ⭐ Fácil

---

**Você conseguiu criar as credenciais? Se sim, já pode avançar para instalar o AWS SDK e criar o código PHP!**



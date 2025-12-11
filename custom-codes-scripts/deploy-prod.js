// ====================
// DEPLOY PARA PRODUÇÃO (WEBFLOW PROD)
// Data: 2024-01-XX
// ATENÇÃO: Este script faz deploy em PRODUÇÃO!
// ====================

const fs = require('fs');
const path = require('path');

const CONFIG = {
  STAGING_DIR: 'custom-codes-webflow-development/03-STAGING',
  PRODUCTION_DIR: 'custom-codes-webflow-development/04-PRODUCTION',
  BACKUP_DIR: 'custom-codes-webflow-development/01-BACKUP',
  COMPONENTS: {
    'footer-code': 'footer-code-staging.js',
    'webflow-injection': 'webflow-injection-staging.js',
    'modal-whatsapp': 'modal-whatsapp-staging.js'
  }
};

function requireConfirmation() {
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise(resolve => {
    console.log('\n⚠️  ⚠️  ⚠️  ATENÇÃO ⚠️  ⚠️  ⚠️');
    console.log('Você está prestes a fazer deploy em PRODUÇÃO!');
    console.log('Isso afetará o site segurosimediato.com.br');
    console.log('\nDigite "DEPLOY-PROD" para confirmar:');
    
    rl.question('> ', answer => {
      rl.close();
      resolve(answer === 'DEPLOY-PROD');
    });
  });
}

function createBackupBeforeDeploy() {
  console.log('📦 Criando backup antes do deploy...');
  
  const today = new Date();
  const dateStr = today.toISOString().split('T')[0];
  const backupPath = path.join(CONFIG.BACKUP_DIR, `pre-deploy-${dateStr}-${Date.now()}`);
  
  fs.mkdirSync(backupPath, { recursive: true });
  
  let backupsCreated = 0;
  
  for (const [component, fileName] of Object.entries(CONFIG.COMPONENTS)) {
    const prodPath = path.join(CONFIG.PRODUCTION_DIR, fileName);
    const backupFile = path.join(backupPath, fileName);
    
    if (fs.existsSync(prodPath)) {
      fs.copyFileSync(prodPath, backupFile);
      backupsCreated++;
      console.log(`✅ Backup: ${fileName}`);
    }
  }
  
  // Salvar log
  const logContent = `Backup pré-deploy criado em: ${new Date().toISOString()}\nArquivos: ${backupsCreated}\n`;
  const logPath = path.join(backupPath, 'backup-log.txt');
  fs.writeFileSync(logPath, logContent, 'utf8');
  
  console.log(`✅ Backup criado: ${backupsCreated} arquivos\n`);
  
  return backupPath;
}

function copyToProduction() {
  let totalFiles = 0;
  let successfulDeploys = 0;
  
  console.log('🚀 Copiando arquivos para PRODUCTION...\n');
  
  for (const [component, fileName] of Object.entries(CONFIG.COMPONENTS)) {
    const stagingPath = path.join(CONFIG.STAGING_DIR, fileName);
    const prodPath = path.join(CONFIG.PRODUCTION_DIR, fileName);
    
    console.log(`📦 ${component}:`);
    console.log(`   Origem: ${stagingPath}`);
    console.log(`   Destino: ${prodPath}`);
    
    try {
      if (fs.existsSync(stagingPath)) {
        const destDir = path.dirname(prodPath);
        if (!fs.existsSync(destDir)) {
          fs.mkdirSync(destDir, { recursive: true });
        }
        
        fs.copyFileSync(stagingPath, prodPath);
        console.log(`   ✅ Copiado com sucesso\n`);
        successfulDeploys++;
      } else {
        console.log(`   ⚠️  Arquivo não encontrado\n`);
      }
      
      totalFiles++;
    } catch (error) {
      console.log(`   ❌ Erro: ${error.message}\n`);
    }
  }
  
  return { totalFiles, successfulDeploys };
}

function updateProductionVersion() {
  const versionInfo = {
    version: new Date().toISOString(),
    timestamp: Date.now(),
    deployedBy: process.env.USER || 'unknown',
    components: Object.keys(CONFIG.COMPONENTS)
  };
  
  const versionPath = path.join(CONFIG.PRODUCTION_DIR, 'production-version.txt');
  const content = JSON.stringify(versionInfo, null, 2);
  fs.writeFileSync(versionPath, content, 'utf8');
  
  console.log('📝 Versão de produção atualizada\n');
}

async function deployToProduction() {
  try {
    console.log('\n' + '='.repeat(60));
    console.log('🚀 DEPLOY PARA PRODUÇÃO');
    console.log('='.repeat(60) + '\n');
    
    // Confirmação
    const confirmed = await requireConfirmation();
    
    if (!confirmed) {
      console.log('❌ Deploy cancelado pelo usuário.');
      return;
    }
    
    // Backup
    const backupPath = createBackupBeforeDeploy();
    
    // Copiar arquivos
    const { totalFiles, successfulDeploys } = copyToProduction();
    
    // Atualizar versão
    updateProductionVersion();
    
    // Resumo
    console.log('\n' + '='.repeat(60));
    console.log('✅ DEPLOY CONCLUÍDO!');
    console.log('='.repeat(60));
    console.log(`Total de arquivos: ${totalFiles}`);
    console.log(`Deploy realizado: ${successfulDeploys}/${totalFiles}`);
    console.log(`📁 Backup: ${backupPath}`);
    console.log(`\n⚠️  PRÓXIMOS PASSOS (CRÍTICO):`);
    console.log('1. Acessar Webflow Editor (PROD)');
    console.log('2. Inserir custom codes da pasta 04-PRODUCTION');
    console.log('3. Publicar alterações');
    console.log('4. TESTAR imediatamente após publicação');
    console.log('5. Monitorar por 24-48h');
    console.log('6. Verificar logs e métricas');
    console.log('\n📞 Suporte: disponível para rollback se necessário\n');
    
  } catch (error) {
    console.error('❌ Erro no deploy:', error.message);
    process.exit(1);
  }
}

// Executar
deployToProduction();





















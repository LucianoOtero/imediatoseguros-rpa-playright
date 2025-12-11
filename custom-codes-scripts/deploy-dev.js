// ====================
// DEPLOY PARA DESENVOLVIMENTO (WEBFLOW DEV)
// Data: 2024-01-XX
// ====================

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const CONFIG = {
  DEVELOPMENT_DIR: 'custom-codes-webflow-development/02-DEVELOPMENT',
  STAGING_DIR: 'custom-codes-webflow-development/03-STAGING',
  COMPONENTS: {
    'footer-code': {
      dev: 'footer-code/footer-code-main.js',
      staging: 'footer-code-staging.js'
    },
    'webflow-injection': {
      dev: 'webflow-injection/webflow-injection-main.js',
      staging: 'webflow-injection-staging.js'
    },
    'modal-whatsapp': {
      dev: 'modals/modal-whatsapp/MODAL_WHATSAPP_DEFINITIVO.js',
      staging: 'modal-whatsapp-staging.js'
    }
  }
};

function getFileHash(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return crypto.createHash('md5').update(content).digest('hex');
  } catch (error) {
    return null;
  }
}

function copyFile(source, dest) {
  try {
    if (fs.existsSync(source)) {
      // Criar diretório de destino se não existir
      const destDir = path.dirname(dest);
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
      }
      
      fs.copyFileSync(source, dest);
      return { success: true, message: '✅ Copiado com sucesso' };
    } else {
      return { success: false, message: '⚠️ Arquivo não encontrado' };
    }
  } catch (error) {
    return { success: false, message: `❌ Erro: ${error.message}` };
  }
}

function createComparisonLog(component, sourcePath, destPath) {
  const sourceHash = getFileHash(sourcePath);
  const destHash = getFileHash(destPath);
  
  const log = {
    component: component,
    timestamp: new Date().toISOString(),
    sourceFile: sourcePath,
    destinationFile: destPath,
    sourceHash: sourceHash,
    destinationHash: destHash,
    hasChanged: sourceHash !== destHash
  };
  
  return log;
}

function deployToStaging() {
  try {
    console.log('🚀 Iniciando deploy para STAGING (Webflow DEV)...\n');
    
    const logs = [];
    let totalFiles = 0;
    let successfulDeploys = 0;
    
    for (const [component, paths] of Object.entries(CONFIG.COMPONENTS)) {
      const devPath = path.join(CONFIG.DEVELOPMENT_DIR, paths.dev);
      const stagingPath = path.join(CONFIG.STAGING_DIR, paths.staging);
      
      console.log(`📦 Deployando: ${component}`);
      console.log(`   Origem: ${devPath}`);
      console.log(`   Destino: ${stagingPath}`);
      
      const result = copyFile(devPath, stagingPath);
      console.log(`   ${result.message}\n`);
      
      logs.push(createComparisonLog(component, devPath, stagingPath));
      
      totalFiles++;
      if (result.success) successfulDeploys++;
    }
    
    // Salvar log de comparação
    const logPath = path.join(CONFIG.STAGING_DIR, `staging-deploy-${Date.now()}.json`);
    fs.writeFileSync(logPath, JSON.stringify(logs, null, 2), 'utf8');
    
    // Resumo
    console.log('\n' + '='.repeat(50));
    console.log('📊 RESUMO DO DEPLOY');
    console.log('='.repeat(50));
    console.log(`Total de componentes: ${totalFiles}`);
    console.log(`Deploy realizado: ${successfulDeploys}/${totalFiles}`);
    console.log(`\n✅ Código disponível para inserção no Webflow DEV`);
    console.log(`📁 Diretório: ${CONFIG.STAGING_DIR}`);
    console.log('\n⚠️  PRÓXIMOS PASSOS:');
    console.log('1. Acessar Webflow Editor (DEV)');
    console.log('2. Inserir custom codes da pasta STAGING');
    console.log('3. Publicar e testar');
    console.log('4. Validar funcionalidades');
    
  } catch (error) {
    console.error('❌ Erro no deploy:', error.message);
    process.exit(1);
  }
}

// Executar
deployToStaging();





















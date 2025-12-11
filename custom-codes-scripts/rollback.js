// ====================
// ROLLBACK - RETORNA A VERSÃO ANTERIOR
// Data: 2024-01-XX
// ====================

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const CONFIG = {
  BACKUP_DIR: 'custom-codes-webflow-development/01-BACKUP',
  PRODUCTION_DIR: 'custom-codes-webflow-development/04-PRODUCTION',
  COMPONENTS: [
    'footer-code-staging.js',
    'webflow-injection-staging.js',
    'modal-whatsapp-staging.js'
  ]
};

function listAvailableBackups() {
  console.log('📁 Buscando backups disponíveis...\n');
  
  if (!fs.existsSync(CONFIG.BACKUP_DIR)) {
    console.log('❌ Pasta de backup não encontrada!');
    return [];
  }
  
  const folders = fs.readdirSync(CONFIG.BACKUP_DIR)
    .filter(folder => folder.match(/^\d{4}-\d{2}-\d{2}/))
    .sort()
    .reverse(); // Mais recente primeiro
  
  if (folders.length === 0) {
    console.log('⚠️  Nenhum backup encontrado!');
    return [];
  }
  
  console.log('Backups disponíveis:');
  folders.forEach((folder, index) => {
    const folderPath = path.join(CONFIG.BACKUP_DIR, folder);
    const logPath = path.join(folderPath, 'backup-log.txt');
    
    if (fs.existsSync(logPath)) {
      const logContent = fs.readFileSync(logPath, 'utf8');
      const dateMatch = logContent.match(/Data: (.+)/);
      console.log(`\n[${index + 1}] ${folder}`);
      if (dateMatch) console.log(`    Data: ${dateMatch[1]}`);
    } else {
      console.log(`\n[${index + 1}] ${folder}`);
    }
  });
  
  return folders;
}

function selectBackup(backups) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise(resolve => {
    console.log('\nDigite o número do backup para restaurar (0 para cancelar):');
    rl.question('> ', answer => {
      rl.close();
      const index = parseInt(answer) - 1;
      if (index >= 0 && index < backups.length) {
        resolve(backups[index]);
      } else {
        resolve(null);
      }
    });
  });
}

function restoreFromBackup(backupFolder) {
  console.log(`\n🔄 Restaurando backup: ${backupFolder}\n`);
  
  const backupPath = path.join(CONFIG.BACKUP_DIR, backupFolder);
  let restored = 0;
  
  CONFIG.COMPONENTS.forEach(fileName => {
    const backupFile = path.join(backupPath, fileName);
    
    if (fs.existsSync(backupFile)) {
      const prodPath = path.join(CONFIG.PRODUCTION_DIR, fileName);
      const destDir = path.dirname(prodPath);
      
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
      }
      
      fs.copyFileSync(backupFile, prodPath);
      console.log(`✅ Restaurado: ${fileName}`);
      restored++;
    } else {
      console.log(`⚠️  Não encontrado: ${fileName}`);
    }
  });
  
  return restored;
}

function logRollback(backupFolder, restoredFiles) {
  const rollbackPath = path.join(CONFIG.PRODUCTION_DIR, 'rollback-log.txt');
  const content = [
    `=== ROLLBACK REALIZADO ===`,
    `Data: ${new Date().toISOString()}`,
    `Backup restaurado: ${backupFolder}`,
    `Arquivos restaurados: ${restoredFiles}`,
    `\nPRÓXIMOS PASSOS:`,
    `1. Inserir códigos restaurados no Webflow`,
    `2. Testar funcionalidades`,
    `3. Monitorar por problemas`,
    ``
  ].join('\n');
  
  fs.writeFileSync(rollbackPath, content, 'utf8');
}

async function rollback() {
  try {
    console.log('\n' + '='.repeat(60));
    console.log('↩️  ROLLBACK - RESTAURAR VERSÃO ANTERIOR');
    console.log('='.repeat(60) + '\n');
    
    // Listar backups
    const backups = listAvailableBackups();
    
    if (backups.length === 0) {
      console.log('\n❌ Não há backups disponíveis para rollback.');
      return;
    }
    
    // Selecionar backup
    const selectedBackup = await selectBackup(backups);
    
    if (!selectedBackup) {
      console.log('\n❌ Operação cancelada.');
      return;
    }
    
    // Confirmar
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    console.log(`\n⚠️  Você confirma a restauração do backup: ${selectedBackup}? (sim/não)`);
    const confirmed = await new Promise(resolve => {
      rl.question('> ', answer => {
        rl.close();
        resolve(answer.toLowerCase() === 'sim');
      });
    });
    
    if (!confirmed) {
      console.log('\n❌ Operação cancelada.');
      return;
    }
    
    // Restaurar
    const restored = restoreFromBackup(selectedBackup);
    
    // Log
    logRollback(selectedBackup, restored);
    
    // Resumo
    console.log('\n' + '='.repeat(60));
    console.log('✅ ROLLBACK CONCLUÍDO!');
    console.log('='.repeat(60));
    console.log(`Backup: ${selectedBackup}`);
    console.log(`Arquivos restaurados: ${restored}/${CONFIG.COMPONENTS.length}`);
    console.log(`\n⚠️  PRÓXIMOS PASSOS:`);
    console.log('1. Inserir códigos restaurados no Webflow');
    console.log('2. Publicar alterações');
    console.log('3. Testar funcionalidades');
    console.log('4. Verificar se problema foi resolvido');
    console.log('\n📁 Arquivos disponíveis em: 04-PRODUCTION\n');
    
  } catch (error) {
    console.error('❌ Erro no rollback:', error.message);
    process.exit(1);
  }
}

// Executar
rollback();





















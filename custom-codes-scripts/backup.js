// ====================
// BACKUP AUTOMÁTICO - CUSTOM CODES WEBFLOW
// Data: 2024-01-XX
// ====================

const fs = require('fs');
const path = require('path');

const CONFIG = {
  SOURCE_DIR: 'C:/Users/Luciano/OneDrive - Imediato Soluções em Seguros/Imediato/custom code webflow',
  BACKUP_DIR: 'C:/Users/Luciano/OneDrive - Imediato Soluções em Seguros/Imediato/custom-codes-webflow-development/01-BACKUP',
  FILES_TO_BACKUP: [
    'Footer Code Site Definitivo.js',
    'webflow_injection_limpo.js'
  ],
  RETENTION_DAYS: 30
};

function createBackupFolder() {
  const today = new Date();
  const dateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
  const backupPath = path.join(CONFIG.BACKUP_DIR, dateStr);
  
  if (!fs.existsSync(backupPath)) {
    fs.mkdirSync(backupPath, { recursive: true });
    console.log(`✅ Pasta de backup criada: ${backupPath}`);
  }
  
  return backupPath;
}

function backupFiles() {
  try {
    console.log('🔄 Iniciando backup automático...\n');
    
    // Criar pasta de backup
    const backupPath = createBackupFolder();
    
    // Criar log de backup
    const logContent = [];
    logContent.push(`=== BACKUP AUTOMÁTICO ===\n`);
    logContent.push(`Data: ${new Date().toISOString()}\n`);
    logContent.push(`Origem: ${CONFIG.SOURCE_DIR}\n`);
    logContent.push(`Destino: ${backupPath}\n\n`);
    
    let filesBackedUp = 0;
    
    // Fazer backup de cada arquivo
    CONFIG.FILES_TO_BACKUP.forEach(fileName => {
      const sourcePath = path.join(CONFIG.SOURCE_DIR, fileName);
      const destPath = path.join(backupPath, fileName);
      
      if (fs.existsSync(sourcePath)) {
        fs.copyFileSync(sourcePath, destPath);
        filesBackedUp++;
        logContent.push(`✅ ${fileName} → ${destPath}\n`);
        console.log(`✅ ${fileName}`);
      } else {
        logContent.push(`⚠️ ${fileName} não encontrado\n`);
        console.log(`⚠️ ${fileName} não encontrado`);
      }
    });
    
    // Salvar log
    logContent.push(`\nTotal de arquivos: ${filesBackedUp}/${CONFIG.FILES_TO_BACKUP.length}\n`);
    logContent.push(`Status: ${filesBackedUp === CONFIG.FILES_TO_BACKUP.length ? 'SUCESSO' : 'PARCIAL'}\n`);
    
    const logPath = path.join(backupPath, 'backup-log.txt');
    fs.writeFileSync(logPath, logContent.join(''), 'utf8');
    
    // Atualizar último backup
    const lastBackupPath = path.join(CONFIG.BACKUP_DIR, 'auto-backup-last.txt');
    fs.writeFileSync(lastBackupPath, `Último backup: ${new Date().toISOString()}\nPasta: ${backupPath}`, 'utf8');
    
    console.log(`\n✅ Backup concluído!\n📁 Local: ${backupPath}`);
    console.log(`📊 Arquivos copiados: ${filesBackedUp}/${CONFIG.FILES_TO_BACKUP.length}`);
    
    // Limpeza de backups antigos
    cleanupOldBackups();
    
  } catch (error) {
    console.error('❌ Erro no backup:', error.message);
    process.exit(1);
  }
}

function cleanupOldBackups() {
  try {
    const folders = fs.readdirSync(CONFIG.BACKUP_DIR);
    const today = new Date();
    
    folders.forEach(folder => {
      if (folder.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const folderDate = new Date(folder);
        const daysDiff = (today - folderDate) / (1000 * 60 * 60 * 24);
        
        if (daysDiff > CONFIG.RETENTION_DAYS) {
          const folderPath = path.join(CONFIG.BACKUP_DIR, folder);
          fs.rmSync(folderPath, { recursive: true, force: true });
          console.log(`🗑️ Backup antigo removido: ${folder}`);
        }
      }
    });
  } catch (error) {
    console.error('⚠️ Erro na limpeza:', error.message);
  }
}

// Executar
backupFiles();





















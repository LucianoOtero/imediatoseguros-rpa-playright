# Script para criar estrutura de desenvolvimento
$base = "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\custom-codes-webflow-development"

$dirs = @(
    "01-BACKUP",
    "02-DEVELOPMENT\footer-code",
    "02-DEVELOPMENT\webflow-injection",
    "02-DEVELOPMENT\modals\modal-whatsapp",
    "02-DEVELOPMENT\components",
    "03-STAGING",
    "04-PRODUCTION",
    "05-TESTS",
    "06-DOCUMENTATION",
    "07-SCRIPTS"
)

foreach ($dir in $dirs) {
    $fullPath = Join-Path $base $dir
    New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
    Write-Host "Criado: $dir"
}

Write-Host "`n✅ Estrutura criada com sucesso!"





















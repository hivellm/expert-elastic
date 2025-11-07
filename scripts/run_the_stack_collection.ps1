# Script para coletar The Stack
# Requer token HuggingFace (configure via variável de ambiente ou huggingface-cli login)

$ErrorActionPreference = "Stop"

# Verificar se token está configurado
if (-not $env:HF_TOKEN -and -not $env:HUGGINGFACE_TOKEN) {
    Write-Host "[ERRO] Token HuggingFace não encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Configure o token usando um dos métodos:"
    Write-Host "  1. Variável de ambiente: `$env:HF_TOKEN = 'seu_token_aqui'"
    Write-Host "  2. Use huggingface-cli login"
    Write-Host ""
    Write-Host "Obtenha seu token em: https://huggingface.co/settings/tokens"
    Write-Host "Aceite os termos do dataset em: https://huggingface.co/datasets/bigcode/the-stack"
    exit 1
}

Write-Host "========================================================================"
Write-Host "Coletando The Stack Dataset"
Write-Host "========================================================================"

$python = "F:/Node/hivellm/expert/cli/venv_windows/Scripts/python.exe"
$script = "scripts/collect_the_stack_elasticsearch.py"
$limit = 50000

Write-Host "Executando: $python $script --limit $limit"
Write-Host ""

& $python $script --limit $limit

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================================================"
    Write-Host "Coleta concluida com sucesso!"
    Write-Host "========================================================================"
    
    $outputFile = "datasets/raw/the_stack_elasticsearch/the_stack_elasticsearch.jsonl"
    if (Test-Path $outputFile) {
        $lineCount = (Get-Content $outputFile | Measure-Object -Line).Lines
        $fileSize = (Get-Item $outputFile).Length / 1MB
        Write-Host "Arquivo gerado: $outputFile"
        Write-Host "Total de exemplos: $lineCount"
        Write-Host "Tamanho: $([math]::Round($fileSize, 2)) MB"
    }
} else {
    Write-Host ""
    Write-Host "========================================================================"
    Write-Host "Erro na coleta. Verifique os logs acima."
    Write-Host "========================================================================"
}


<#
Loads environment variables from a `.env` file into the current PowerShell session.

Usage (dot-source so variables persist in your session):
. .\set_mysql_env.ps1

Then run Django management commands normally.
#>

$envFile = Join-Path $PSScriptRoot '.env'
if (-Not (Test-Path $envFile)) {
    Write-Error ".env file not found. Copy .env.example to .env and edit it first."
    exit 1
}

Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith('#')) {
        $parts = $line -split '=', 2
        if ($parts.Length -eq 2) {
            $name = $parts[0].Trim()
            $value = $parts[1].Trim().Trim("'\"")
            Set-Item -Path Env:\$name -Value $value
            Write-Host "Set $name"
        }
    }
}

Write-Host "Environment variables loaded from .env"

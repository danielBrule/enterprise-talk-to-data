#!/usr/bin/env pwsh
# Talk-to-Data Delivery Blueprint - build tasks (PowerShell 7+, cross-platform).
# Invoked by the Makefile, or directly:  pwsh scripts/build.ps1 -Target pdf
param(
    [ValidateSet("help", "env", "pdf", "clean")]
    [string]$Target = "help"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
$Venv = Join-Path $Root ".venv"
$OnWindows = $IsWindows -or ($env:OS -eq "Windows_NT")
$VenvPython = if ($OnWindows) { Join-Path $Venv "Scripts/python.exe" } else { Join-Path $Venv "bin/python" }

function Test-Tool([string]$Name, [string]$Hint) {
    if (Get-Command $Name -ErrorAction SilentlyContinue) {
        Write-Host "  ok   $Name"
    } else {
        Write-Warning "missing $Name  ->  $Hint"
    }
}

switch ($Target) {
    "help" {
        Write-Host "Targets:"
        Write-Host "  env    create .venv, install requirements.txt, check PDF toolchain"
        Write-Host "  pdf    generate docs/pdf/*.pdf from the Markdown"
        Write-Host "  clean  remove generated PDFs"
    }
    "env" {
        if (-not (Test-Path $VenvPython)) {
            Write-Host "Creating virtual environment (.venv) ..."
            python -m venv $Venv
        }
        & $VenvPython -m pip install --upgrade pip | Out-Null
        & $VenvPython -m pip install -r (Join-Path $Root "requirements.txt")
        Write-Host "`nChecking PDF toolchain (system tools, not pip):"
        Test-Tool "pandoc"      "https://pandoc.org/installing.html"
        Test-Tool "wkhtmltopdf" "https://wkhtmltopdf.org/downloads.html"
        Test-Tool "mmdc"        "npm install -g @mermaid-js/mermaid-cli"
        Write-Host "`nEnvironment ready."
    }
    "pdf" {
        $py = if (Test-Path $VenvPython) { $VenvPython } else { "python" }
        & $py (Join-Path $Root "scripts/build_pdfs.py") (Join-Path $Root "docs")
    }
    "clean" {
        $pdfDir = Join-Path $Root "docs/pdf"
        if (Test-Path $pdfDir) {
            Remove-Item (Join-Path $pdfDir "*.pdf") -Force -ErrorAction SilentlyContinue
        }
        Write-Host "Removed generated PDFs."
    }
}

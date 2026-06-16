# Talk-to-Data Delivery Blueprint - task runner.
# Logic lives in scripts/build.ps1.
#
# Picks the available PowerShell automatically:
#   Windows -> powershell (Windows PowerShell 5.1, always present)
#   macOS/Linux -> pwsh (PowerShell 7)
# Override with:  make env PWSH=pwsh
#
# On Windows, `make` itself must be installed (e.g. `choco install make`
# or `winget install GnuWin32.Make`).

ifeq ($(OS),Windows_NT)
    PWSH ?= powershell
else
    PWSH ?= pwsh
endif

PS = $(PWSH) -NoProfile -ExecutionPolicy Bypass -File scripts/build.ps1 -Target

.PHONY: help env pdf clean

help:   ## list targets
	@$(PS) help

env:    ## create .venv, install requirements, check the PDF toolchain
	@$(PS) env

pdf:    ## generate docs/pdf/*.pdf from the Markdown
	@$(PS) pdf

clean:  ## remove generated PDFs
	@$(PS) clean
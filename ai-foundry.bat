@echo off
REM =====================================================================
REM  AI Foundry v0.9 - Windows launcher
REM  (ASCII-only comments to avoid codepage issues on GBK cmd)
REM =====================================================================
REM  Deployment notes:
REM   * Working directory is locked to script parent folder via %~dp0.
REM   * Prepends per-user Python Scripts dir to PATH so `ai-foundry.exe`
REM     is found even when Python 3.14 user site is not on global PATH.
REM   * Tries py launcher first, falls back to python.exe.
REM   * Tries installed ai-foundry.exe first, otherwise runs
REM     `python -m ai_foundry` (works without pip install).
REM =====================================================================

setlocal

REM Step 0: add user Scripts to PATH (handles pip --user install warning)
for /f "delims=" %%i in ('python -c "import site,os,sys; print(os.path.join(site.getusersitepackages().replace('site-packages','Scripts')))" 2^>nul') do (
    if exist "%%~i\ai-foundry.exe" set "PATH=%%~i;%PATH%"
)

REM Step 1: cd to the folder where this .bat lives (critical)
cd /d "%~dp0"

REM Step 2: choose Python interpreter
where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py -3"
) else (
    set "PY=python"
)

REM Step 3: prefer the installed console-script EXE (not .bat/.cmd!),
REM         otherwise fall back to module mode, which is always available.
where ai-foundry.exe >nul 2>nul
if %errorlevel%==0 (
    ai-foundry.exe %*
    goto :done
)

%PY% -m ai_foundry %*

:done
endlocal
exit /b %errorlevel%

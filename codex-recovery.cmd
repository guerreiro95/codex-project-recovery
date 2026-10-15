@echo off
setlocal
where py >nul 2>nul
if errorlevel 1 (
  python "%~dp0codex_recovery.py" %*
) else (
  py -3 "%~dp0codex_recovery.py" %*
)
set "recovery_exit=%errorlevel%"
echo.
pause
exit /b %recovery_exit%

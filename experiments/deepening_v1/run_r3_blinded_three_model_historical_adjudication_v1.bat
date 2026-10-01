@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0run_r3_blinded_three_model_historical_adjudication_v1.ps1"
exit /b %ERRORLEVEL%

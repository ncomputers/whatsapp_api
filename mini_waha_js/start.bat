@echo off
cd /d %~dp0
where python >nul 2>&1 && (set PY=python) || (set PY=py)
%PY% -m pip install -r python\requirements.txt >nul
%PY% python\app.py

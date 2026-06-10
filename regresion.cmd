@echo off
setlocal
REM Ensure running from repository root (script dir)
cd /d %~dp0
REM Activate virtual environment if present
if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
)
echo Running ruff (excluding legacy)...
python -m ruff check src/IS2_T3_C5_IA/IS2_T3_C5_IA/backlog_calculator.py src/IS2_T3_C5_IA/IS2_T3_C5_IA/tests || (echo ruff failed & exit /b 1)

echo Formatting with black (targeted)...
black src/IS2_T3_C5_IA/IS2_T3_C5_IA --exclude legacy || (echo black formatting failed & exit /b 1)
black script || (echo black formatting failed & exit /b 1)

echo Running ruff --fix (targeted)...
python -m ruff check src/IS2_T3_C5_IA/IS2_T3_C5_IA --fix --exclude src/IS2_T3_C5_IA/IS2_T3_C5_IA/legacy || (echo ruff --fix failed & exit /b 1)
python -m ruff check src/IS2_T3_C5_IA/IS2_T3_C5_IA/tests --fix || (echo ruff --fix failed & exit /b 1)
python -m ruff check src/IS2_T3_C5_IA/IS2_T3_C5_IA --exclude src/IS2_T3_C5_IA/IS2_T3_C5_IA/legacy || (echo ruff failed & exit /b 1)

echo Running pydocstyle...
pydocstyle src/IS2_T3_C5_IA/IS2_T3_C5_IA/backlog_calculator.py src/IS2_T3_C5_IA/IS2_T3_C5_IA/__init__.py src/IS2_T3_C5_IA/IS2_T3_C5_IA/tests/conftest.py || (echo pydocstyle failed & exit /b 1)

echo Running mypy (targeted, excluding legacy)...
mypy src/IS2_T3_C5_IA/IS2_T3_C5_IA --exclude src/IS2_T3_C5_IA/IS2_T3_C5_IA/legacy || (echo mypy failed & exit /b 1)
n:: PyRight is optional; run if available
where pyright >nul 2>nul
if %errorlevel% equ 0 (
  echo Running PyRight...
  pyright src/IS2_T3_C5_IA/IS2_T3_C5_IA || (echo pyright failed & exit /b 1)
) else (
  echo pyright not found, skipping
)

echo Running bandit...
bandit -r src/IS2_T3_C5_IA/IS2_T3_C5_IA -x src/IS2_T3_C5_IA/IS2_T3_C5_IA/legacy -ll || (echo bandit failed & exit /b 1)

echo Running multimetric (optional)...
where multimetric >nul 2>nul
if %errorlevel% equ 0 (
  multimetric src/IS2_T3_C5_IA/IS2_T3_C5_IA || (echo multimetric failed & exit /b 1)
) else (
  echo multimetric not found, skipping
)

echo Running tests with coverage (fail if coverage < 90)...
pytest -q --cov=src/IS2_T3_C5_IA/IS2_T3_C5_IA --cov-fail-under=90 || (echo pytest/coverage failed & exit /b 1)

echo All checks passed.
endlocal
exit /b 0

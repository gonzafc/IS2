@echo off
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt

echo Virtualenv created and dependencies installed.

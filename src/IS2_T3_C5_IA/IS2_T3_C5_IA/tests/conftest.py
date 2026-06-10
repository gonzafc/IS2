"""Pytest conftest for setting up import path for tests."""
import sys
from pathlib import Path

# Ensure project package root is on sys.path so tests can import modules by filename
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

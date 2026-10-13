#!/usr/bin/env python3
"""
Set up the dev environment.

Usage: python setup_env.py (or python3 setup_env.py)
"""

import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
IS_WINDOWS = os.name == "nt"
VENV_PYTHON = VENV_DIR / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")

MIN_PYTHON = (3, 8)


def run(*args):
    print(f"  $ {' '.join(args)}")
    try:
        subprocess.run(args, check=True, cwd=ROOT)
    except subprocess.CalledProcessError as exc:
        sys.exit(f"Command failed with error: {exc}")


def create_venv():
    if VENV_PYTHON.exists():
        print(f"Virtual environment exists at {VENV_DIR.name}/")

    print(f"Creating virtual environment in {VENV_DIR.name}/")
    venv.EnvBuilder(with_pip=True).create(VENV_DIR)


def install_dependencies():
    pip = [str(VENV_PYTHON), "-m", "pip"]

    print("Upgrading pip...")
    run(*pip, "install", "--upgrade", "pip")

    requirements = ROOT / "requirements.txt"
    if requirements.exists():
        print("Installing requirements...")
        run(*pip, "install", "-r", str(requirements))


def ensure_env_file():
    env_file = ROOT / ".env"
    example_file = ROOT / ".env.example"

    if not env_file.exists():
        shutil.copyfile(example_file, env_file)
        print("Created .env from .env.example. Edit it and add real values")


def main():
    if sys.version_info < MIN_PYTHON:
        sys.exit(f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required.")

    create_venv()
    install_dependencies()
    ensure_env_file()
    print("\nSetup complete. Activate the virtual environment and start coding...\n")


if __name__ == "__main__":
    main()

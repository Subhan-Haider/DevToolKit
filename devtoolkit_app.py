"""
Entry point for PyInstaller / standalone .exe builds.
This file is used when building: pyinstaller --onefile devtoolkit_app.py
"""
from devtoolkit.cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())

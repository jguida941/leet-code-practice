#!/usr/bin/env python3
"""
PyQt6 Learning Labs Launcher
Quick launcher script for the algorithm learning application
"""

import sys
import os
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed"""
    missing = []

    try:
        import PyQt6
        print("  PyQt6 is installed")
    except ImportError:
        print("  PyQt6 is not installed")
        missing.append("PyQt6>=6.4.0")

    try:
        import pyqtgraph
        print("  pyqtgraph is installed")
    except ImportError:
        print("  pyqtgraph is not installed (optional, will use fallback)")

    if missing:
        print("\nInstalling missing dependencies...")
        for package in missing:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    check=True,
                    capture_output=True
                )
                print(f"    Installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"    Failed to install {package}: {e}")
                return False

    return True


def launch_app():
    """Launch the PyQt6 Learning Labs application"""
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    print("\n" + "*" * 50)
    print("       Launching PyQt6 Learning Labs...")
    print("*" * 50 + "\n")

    # Run the main application
    result = subprocess.run([sys.executable, "-m", "pyqt6_learning_labs.main"])
    return result.returncode


def main():
    print("""
+-----------------------------------------------+
|       PyQt6 Learning Labs Auto Launcher       |
|    Interactive Algorithm Learning Platform    |
|                     v2.1                      |
+-----------------------------------------------+
    """)

    print("Checking dependencies...")

    # Check and install dependencies if needed
    if not check_dependencies():
        print("\nFailed to install required dependencies.")
        print("Please install manually: pip install PyQt6>=6.4.0")
        sys.exit(1)

    # Launch the application
    exit_code = launch_app()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

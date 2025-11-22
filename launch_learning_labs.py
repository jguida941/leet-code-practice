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
    try:
        import PyQt6
        print("✓ PyQt6 is installed")
    except ImportError:
        print("✗ PyQt6 is not installed")
        print("Installing PyQt6...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6>=6.4.0"])

    try:
        import pyqtgraph
        print("✓ pyqtgraph is installed")
    except ImportError:
        print("✗ pyqtgraph is not installed (optional)")
        print("Note: Installing pyqtgraph for better graph visualizations...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyqtgraph>=0.13.3"])
        except:
            print("Could not install pyqtgraph - app will use fallback graphs")

def launch_app():
    """Launch the PyQt6 Learning Labs application"""
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    print("\n" + "*"*50)
    print("       Launching PyQt6 Learning Labs...")
    print("*"*50 + "\n")

    # Run the main application
    subprocess.run([sys.executable, "-m", "pyqt6_learning_labs.main"])

def main():
    print("""
╔═══════════════════════════════════════════════╗
║       PyQt6 Learning Labs Auto Launcher       ║
║    Interactive Algorithm Learning Platform    ║
║                     v2.0                      ║
╚═══════════════════════════════════════════════╝
    """)

    # Check and install dependencies if needed
    check_dependencies()

    # Launch the application
    launch_app()

if __name__ == "__main__":
    main()
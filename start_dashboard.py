#!/usr/bin/env python3
"""
Cross-platform startup script for AI Data Team Dashboard.
Run: python start_dashboard.py
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n▶️  {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🤖  AI Data Team - Streamlit Dashboard")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Create virtual environment if needed
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("\n📦 Creating virtual environment...")
        os.system(f"{sys.executable} -m venv .venv")
    
    # Get Python executable in venv
    if sys.platform == "win32":
        venv_python = str(venv_path / "Scripts" / "python.exe")
        pip_cmd = f"{venv_path / 'Scripts' / 'pip.exe'} install -r requirements.txt"
    else:
        venv_python = str(venv_path / "bin" / "python")
        pip_cmd = f"{venv_path / 'bin' / 'pip'} install -r requirements.txt"
    
    # Install dependencies
    if not run_command(pip_cmd, "Installing dependencies"):
        print("\n⚠️  Dependency installation may have issues")
    
    # Start dashboard
    print("\n" + "=" * 50)
    print("✅ Starting Dashboard...")
    print("=" * 50)
    print("\n📱 Dashboard URL: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Run streamlit
    streamlit_cmd = f"{venv_python} -m streamlit run streamlit_app.py"
    os.system(streamlit_cmd)

if __name__ == "__main__":
    main()

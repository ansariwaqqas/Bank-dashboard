"""
Convenience launcher for the Bank Management System Web Portal.
Allows starting the server directly from the project root:
    python run.py
"""

import sys
import subprocess
from pathlib import Path

if __name__ == "__main__":
    backend_script = Path(__file__).resolve().parent / "backend" / "app.py"
    port_arg = [sys.argv[1]] if len(sys.argv) > 1 else []
    sys.exit(subprocess.call([sys.executable, str(backend_script)] + port_arg))

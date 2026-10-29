"""
Database seeder shortcut in backend.
Delegates to the dedicated database seeder in database/seed_db.py.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.seed_db import reset_and_seed

if __name__ == "__main__":
    reset_and_seed()

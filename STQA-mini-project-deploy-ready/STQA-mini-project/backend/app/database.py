"""
Database Management Module (Backend Adapter).
Re-exports functionality from the dedicated /database package at project root.
Preserves backwards compatibility with existing imports: `from app.database import ...`
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path so database package can be resolved
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.database import (
    DEFAULT_DB_PATH,
    get_connection,
    init_db,
    create_account,
    get_account,
    update_balance,
    get_balance,
)

__all__ = [
    "DEFAULT_DB_PATH",
    "get_connection",
    "init_db",
    "create_account",
    "get_account",
    "update_balance",
    "get_balance",
]

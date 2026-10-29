"""
Database package for Bank Management System.
Exposes database initialization and CRUD operations.
"""

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

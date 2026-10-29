"""
Database Management Module for Bank Management System.
Handles SQLite database connection, table initialization, and CRUD operations for accounts.
"""

import sqlite3
from pathlib import Path
from typing import Optional

# Path to database directory & default SQLite database file
DATABASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = str(DATABASE_DIR / "bank.db")


def get_connection(db_name: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """
    Establish and return a SQLite database connection with row factory enabled.
    """
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_name: str = DEFAULT_DB_PATH) -> None:
    """
    Initialize SQLite database and create 'accounts' table if it does not already exist.
    Schema:
        - id: INTEGER PRIMARY KEY AUTOINCREMENT
        - name: TEXT NOT NULL
        - balance: REAL NOT NULL DEFAULT 0.0
    """
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0
            );
            """
        )
        conn.commit()


def create_account(name: str, initial_balance: float = 0.0, db_name: str = DEFAULT_DB_PATH) -> int:
    """
    Create a new bank account in the database.

    Args:
        name: Name of the account holder.
        initial_balance: Initial balance to seed the account with (default 0.0).
        db_name: Target SQLite database file or connection string.

    Returns:
        int: The auto-generated ID of the newly created account.

    Raises:
        ValueError: If initial_balance is negative or name is empty.
    """
    if not name or not name.strip():
        raise ValueError("Account holder name cannot be empty.")
    if initial_balance < 0.0:
        raise ValueError("Initial balance cannot be negative.")

    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO accounts (name, balance)
            VALUES (?, ?);
            """,
            (name.strip(), float(initial_balance)),
        )
        conn.commit()
        return cursor.lastrowid


def update_balance(account_id: int, new_balance: float, db_name: str = DEFAULT_DB_PATH) -> bool:
    """
    Update the balance for an existing account.

    Args:
        account_id: ID of the account to update.
        new_balance: The updated balance amount.
        db_name: Target SQLite database file.

    Returns:
        bool: True if the account was found and updated, False otherwise.
    """
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE id = ?;
            """,
            (float(new_balance), account_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def get_balance(account_id: int, db_name: str = DEFAULT_DB_PATH) -> Optional[float]:
    """
    Fetch the current balance of an account by its ID.

    Args:
        account_id: ID of the account to inspect.
        db_name: Target SQLite database file.

    Returns:
        Optional[float]: The balance if account exists, None otherwise.
    """
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE id = ?;
            """,
            (account_id,),
        )
        row = cursor.fetchone()
        if row is not None:
            return float(row["balance"])
        return None


def get_account(account_id: int, db_name: str = DEFAULT_DB_PATH) -> Optional[dict]:
    """
    Retrieve full account details as a dictionary.

    Args:
        account_id: ID of the account.
        db_name: Target SQLite database file.

    Returns:
        Optional[dict]: Account record {'id': ..., 'name': ..., 'balance': ...} or None.
    """
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, balance
            FROM accounts
            WHERE id = ?;
            """,
            (account_id,),
        )
        row = cursor.fetchone()
        if row is not None:
            return {"id": row["id"], "name": row["name"], "balance": float(row["balance"])}
        return None

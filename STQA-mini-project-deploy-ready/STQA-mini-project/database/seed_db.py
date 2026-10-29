"""
Utility script to reset and seed the SQLite database with test accounts.
Operates on database/bank.db.
"""

import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.database import get_connection, create_account, init_db, DEFAULT_DB_PATH


def reset_and_seed(db_name: str = DEFAULT_DB_PATH):
    init_db(db_name)
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts;")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts';")
        conn.commit()

    test_accounts = [
        ("Alice Johnson", 5000.00),
        ("Bob Smith", 1250.00),
        ("Charlie Brown", 250.00),
        ("Diana Prince", 0.00),
    ]

    print(f"[*] Target Database: {db_name}")
    print("[*] Database cleared. Seeding test accounts...")
    for name, balance in test_accounts:
        acc_id = create_account(name=name, initial_balance=balance, db_name=db_name)
        print(f" [✓] Created Account #{acc_id}: {name} (Balance: ${balance:,.2f})")

    print("\n[+] Database successfully seeded with 4 test accounts!")


if __name__ == "__main__":
    reset_and_seed()

"""
Command Line Interface (CLI) for Bank Management System.
Allows interactive execution of banking operations (account creation, deposit, withdrawal, balance check).
"""

import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import init_db, create_account, get_balance, update_balance, get_account
from app.bank_logic import BankAccount


def print_menu() -> None:
    print("\n" + "=" * 40)
    print("      BANK MANAGEMENT SYSTEM (CLI)")
    print("=" * 40)
    print("1. Create New Account")
    print("2. Check Balance")
    print("3. Deposit Funds")
    print("4. Withdraw Funds")
    print("5. View Account Details")
    print("6. Exit")
    print("=" * 40)


def handle_create_account() -> None:
    name = input("Enter account holder name: ").strip()
    if not name:
        print("[!] Error: Name cannot be empty.")
        return

    bal_input = input("Enter initial deposit amount [default 0.0]: ").strip()
    initial_balance = float(bal_input) if bal_input else 0.0

    try:
        acc_id = create_account(name=name, initial_balance=initial_balance)
        print(f"[✓] Success: Account created! Your Account ID is: {acc_id}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def handle_check_balance() -> None:
    try:
        acc_id = int(input("Enter Account ID: ").strip())
        balance = get_balance(account_id=acc_id)
        if balance is None:
            print("[!] Error: Account not found.")
        else:
            print(f"[✓] Account #{acc_id} Balance: ${balance:.2f}")
    except ValueError:
        print("[!] Error: Invalid Account ID.")


def handle_deposit() -> None:
    try:
        acc_id = int(input("Enter Account ID: ").strip())
        balance = get_balance(account_id=acc_id)
        if balance is None:
            print("[!] Error: Account not found.")
            return

        acc_details = get_account(account_id=acc_id)
        account = BankAccount(account_id=acc_id, name=acc_details["name"], balance=balance)

        amount = float(input("Enter deposit amount: ").strip())
        new_balance = account.deposit(amount)
        update_balance(acc_id, new_balance)
        print(f"[✓] Deposit successful! New Balance: ${new_balance:.2f}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def handle_withdraw() -> None:
    try:
        acc_id = int(input("Enter Account ID: ").strip())
        balance = get_balance(account_id=acc_id)
        if balance is None:
            print("[!] Error: Account not found.")
            return

        acc_details = get_account(account_id=acc_id)
        account = BankAccount(account_id=acc_id, name=acc_details["name"], balance=balance)

        amount = float(input("Enter withdrawal amount: ").strip())
        new_balance = account.withdraw(amount)
        update_balance(acc_id, new_balance)
        print(f"[✓] Withdrawal successful! New Balance: ${new_balance:.2f}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def handle_view_account() -> None:
    try:
        acc_id = int(input("Enter Account ID: ").strip())
        account = get_account(account_id=acc_id)
        if account is None:
            print("[!] Error: Account not found.")
        else:
            print("\n--- Account Information ---")
            print(f"Account ID : {account['id']}")
            print(f"Holder Name: {account['name']}")
            print(f"Balance    : ${account['balance']:.2f}")
    except ValueError:
        print("[!] Error: Invalid Account ID.")


def main() -> None:
    init_db()
    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            handle_create_account()
        elif choice == "2":
            handle_check_balance()
        elif choice == "3":
            handle_deposit()
        elif choice == "4":
            handle_withdraw()
        elif choice == "5":
            handle_view_account()
        elif choice == "6":
            print("\nThank you for using Bank Management System. Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid choice. Please select an option between 1 and 6.")


if __name__ == "__main__":
    main()

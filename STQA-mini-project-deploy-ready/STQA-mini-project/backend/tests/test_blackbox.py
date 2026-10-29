"""
Black-Box Integration Tests for Bank Management System.

Software Testing (STQA) Context:
Black-box testing (Functional / Specification-based testing) tests software behavior
from an external user's perspective, without requiring knowledge of internal code
structures, data representations, or internal branching logic.

Key Principles Demonstrated:
1. Requirements-Driven: Focus on user requirements (Create Account, Deposit, Check Balance).
2. End-to-End Integration: Verifies seamless interaction between the business logic layer
   (app.bank_logic) and the persistence layer (app.database).
3. State & Persistence Verification: Confirms that valid operations yield the expected
   persistent system state in the SQLite database.
4. Test Isolation: Uses temporary database instances per test session to avoid state leakage.
"""

import pytest
from app.database import init_db, create_account, update_balance, get_balance, get_account
from app.bank_logic import BankAccount


@pytest.fixture
def test_db_path(tmp_path) -> str:
    """
    Fixture providing an isolated SQLite database file per test function.
    Initializes required tables prior to test execution.
    """
    db_file = str(tmp_path / "test_bank.db")
    init_db(db_file)
    return db_file


# ============================================================================
# Integration Test 1: Account Creation, Deposit Workflow, and DB State Verification
# ============================================================================
def test_user_account_creation_deposit_and_persistence(test_db_path: str):
    """
    [Black-Box Integration: User Story - Open Account & Deposit]
    Scenario:
      1. User requests to open an account with initial deposit of $200.00.
      2. System registers the account and assigns a unique Account ID.
      3. User later deposits an additional $150.00 into this account.
      4. System persists the updated balance to the database.

    Verification (Black-Box Oracle):
      - Querying the database solely via public fetch methods returns $350.00.
      - Confirms data integrity and persistence across system layers.
    """
    user_name = "Bob Smith"
    initial_deposit = 200.0
    additional_deposit = 150.0

    # Step 1: External Action - Create account through database interface
    account_id = create_account(name=user_name, initial_balance=initial_deposit, db_name=test_db_path)
    assert account_id is not None
    assert isinstance(account_id, int)

    # Step 2: External Action - Fetch current balance, load into logic, and execute deposit
    current_db_balance = get_balance(account_id=account_id, db_name=test_db_path)
    assert current_db_balance == initial_deposit

    account_session = BankAccount(account_id=account_id, name=user_name, balance=current_db_balance)
    new_balance = account_session.deposit(additional_deposit)
    assert new_balance == 350.0

    # Step 3: Persist updated state to SQLite database
    is_updated = update_balance(account_id=account_id, new_balance=new_balance, db_name=test_db_path)
    assert is_updated is True

    # Step 4: Verification - Query the database black-box to verify final state
    persisted_balance = get_balance(account_id=account_id, db_name=test_db_path)
    account_record = get_account(account_id=account_id, db_name=test_db_path)

    assert persisted_balance == 350.0
    assert account_record["name"] == user_name
    assert account_record["balance"] == 350.0


# ============================================================================
# Integration Test 2: Multi-Transaction Workflow with Multiple User Accounts
# ============================================================================
def test_multiple_accounts_isolated_transactions_and_balance_verification(test_db_path: str):
    """
    [Black-Box Integration: Multi-User Workflow & State Isolation]
    Scenario:
      1. Create Account A (Charlie, $500.00) and Account B (Diana, $1000.00).
      2. Perform a deposit on Account A ($250.00).
      3. Perform a withdrawal on Account B ($400.00).
      4. Commit both updated balances to the database.

    Verification (Black-Box Oracle):
      - Account A balance is updated to $750.00.
      - Account B balance is updated to $600.00.
      - Neither user's transaction pollutes or affects the other account's balance in storage.
    """
    # Step 1: Create multiple accounts
    id_a = create_account(name="Charlie", initial_balance=500.0, db_name=test_db_path)
    id_b = create_account(name="Diana", initial_balance=1000.0, db_name=test_db_path)

    # Step 2: Process transaction for Account A
    user_a = BankAccount(account_id=id_a, name="Charlie", balance=get_balance(id_a, test_db_path))
    new_bal_a = user_a.deposit(250.0)
    update_balance(id_a, new_bal_a, test_db_path)

    # Step 3: Process transaction for Account B
    user_b = BankAccount(account_id=id_b, name="Diana", balance=get_balance(id_b, test_db_path))
    new_bal_b = user_b.withdraw(400.0)
    update_balance(id_b, new_bal_b, test_db_path)

    # Step 4: Black-Box Verification of both database entities
    final_balance_a = get_balance(id_a, test_db_path)
    final_balance_b = get_balance(id_b, test_db_path)

    assert final_balance_a == 750.0
    assert final_balance_b == 600.0

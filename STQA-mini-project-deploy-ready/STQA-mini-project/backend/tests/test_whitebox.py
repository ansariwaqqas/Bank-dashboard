"""
White-Box Unit Tests for app.bank_logic.BankAccount.

Software Testing (STQA) Context:
White-box testing (Structural Testing / Glass-box testing) tests the internal logic,
control flow, decision branches, and statement coverage of the software.
Testers have complete visibility into the source code and design test cases to:
1. Achieve 100% Statement Coverage (executing every line of code).
2. Achieve 100% Branch / Decision Coverage (evaluating True and False outcomes of every 'if').
3. Verify Boundary Conditions on internal variables (e.g. amount == 0, amount == balance).
"""

import pytest
from app.bank_logic import BankAccount


@pytest.fixture
def standard_account() -> BankAccount:
    """
    Test fixture providing a clean BankAccount instance seeded with $100.00.
    """
    return BankAccount(account_id=1, name="Alice", balance=100.0)


# ============================================================================
# Test 1: Statement & Path Coverage - Successful Deposit
# ============================================================================
def test_successful_deposit(standard_account: BankAccount):
    """
    [White-Box: Happy Path / Branch Coverage]
    Evaluates:
      - Branch: `amount <= 0.0` evaluates to FALSE.
      - Statement: `self.balance += float(amount)` executes.
      - Return: Returns updated balance accurately.
    """
    deposit_amount = 50.0
    initial_balance = standard_account.balance

    updated_balance = standard_account.deposit(deposit_amount)

    # Verify both the returned value and internal state mutation
    assert updated_balance == initial_balance + deposit_amount
    assert standard_account.balance == 150.0


# ============================================================================
# Test 2: Statement & Path Coverage - Successful Withdrawal & Boundary
# ============================================================================
def test_successful_withdrawal(standard_account: BankAccount):
    """
    [White-Box: Branch & Boundary Condition Coverage]
    Evaluates:
      - Branch 1: `amount <= 0.0` evaluates to FALSE.
      - Branch 2: `amount > self.balance` evaluates to FALSE.
      - Statement: `self.balance -= float(amount)` executes.
      - Boundary Case: Withdrawing exact balance (amount == balance) leaves 0.0.
    """
    # Step A: Partial withdrawal
    updated_balance = standard_account.withdraw(40.0)
    assert updated_balance == 60.0
    assert standard_account.balance == 60.0

    # Step B: Boundary test - Withdrawing remaining balance down to 0
    final_balance = standard_account.withdraw(60.0)
    assert final_balance == 0.0
    assert standard_account.balance == 0.0


# ============================================================================
# Test 3: Decision / Negative Branch Coverage - Invalid Deposit Amounts
# ============================================================================
@pytest.mark.parametrize("invalid_amount", [-50.0, -0.01, 0.0])
def test_deposit_invalid_amount_raises_value_error(standard_account: BankAccount, invalid_amount: float):
    """
    [White-Box: Negative Branch Coverage & Boundary Value Analysis]
    Evaluates:
      - Branch: `amount <= 0.0` evaluates to TRUE for negative numbers and zero boundary.
      - Exception path: Ensures `ValueError` is raised with descriptive message.
      - Internal state integrity: Confirms state `self.balance` remains unmodified after error.
    """
    initial_balance = standard_account.balance

    with pytest.raises(ValueError) as exc_info:
        standard_account.deposit(invalid_amount)

    assert "Deposit amount must be positive" in str(exc_info.value)
    # Ensure no partial state mutation occurred
    assert standard_account.balance == initial_balance


# ============================================================================
# Test 4: Decision Coverage - Insufficient Funds & Negative Withdrawal Guard
# ============================================================================
def test_withdraw_insufficient_funds_and_invalid_amount_raise_value_error(standard_account: BankAccount):
    """
    [White-Box: Error Branch Coverage on Multiple Decision Points]
    Evaluates:
      - Branch 1 (TRUE): Non-positive amount (`amount <= 0.0`) raises ValueError.
      - Branch 2 (TRUE): Insufficient funds (`amount > self.balance`) raises ValueError.
      - Boundary check: `balance + 0.01` triggers insufficient funds path.
    """
    initial_balance = standard_account.balance

    # Test Sub-branch 1: Zero / Negative amount
    with pytest.raises(ValueError) as exc_negative:
        standard_account.withdraw(0.0)
    assert "Withdrawal amount must be positive" in str(exc_negative.value)

    # Test Sub-branch 2: Insufficient funds (Boundary: 1 cent more than balance)
    overdraft_amount = initial_balance + 0.01
    with pytest.raises(ValueError) as exc_overdraft:
        standard_account.withdraw(overdraft_amount)

    assert "Insufficient funds" in str(exc_overdraft.value)
    # Verify account balance remains unmodified
    assert standard_account.balance == initial_balance

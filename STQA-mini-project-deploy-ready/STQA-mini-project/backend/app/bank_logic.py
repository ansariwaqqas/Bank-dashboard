"""
Bank Business Logic Module.
Contains the BankAccount entity that encapsulates business rules for deposits and withdrawals,
including domain validation and error handling for invalid financial operations.
"""


class BankAccount:
    """
    Represents a bank account with basic transaction rules.

    White-Box Testing Reference:
    - Path 1: Successful deposit (amount > 0)
    - Path 2: Invalid deposit (amount <= 0 -> raises ValueError)
    - Path 3: Successful withdrawal (0 < amount <= balance)
    - Path 4: Non-positive withdrawal (amount <= 0 -> raises ValueError)
    - Path 5: Insufficient balance withdrawal (amount > balance -> raises ValueError)
    """

    def __init__(self, account_id: int, name: str, balance: float = 0.0) -> None:
        """
        Initialize a BankAccount instance.

        Args:
            account_id: Unique account identifier.
            name: Name of the account holder.
            balance: Initial account balance (must be non-negative).

        Raises:
            ValueError: If initial balance is negative.
        """
        if balance < 0.0:
            raise ValueError("Initial balance cannot be negative.")

        self.account_id = account_id
        self.name = name
        self.balance = float(balance)

    def deposit(self, amount: float) -> float:
        """
        Deposit funds into the account.

        Business Rule & Decision Branch:
        - Condition: amount <= 0 -> INVALID
        - Condition: amount > 0  -> VALID

        Args:
            amount: Positive amount to deposit.

        Returns:
            float: Updated account balance after deposit.

        Raises:
            ValueError: If the deposit amount is zero or negative.
        """
        # Branch 1: Guard condition for negative or zero amounts
        if amount <= 0.0:
            raise ValueError(f"Deposit amount must be positive. Received: {amount}")

        # Branch 2: Happy path execution
        self.balance += float(amount)
        return self.balance

    def withdraw(self, amount: float) -> float:
        """
        Withdraw funds from the account.

        Business Rules & Decision Branches:
        - Condition 1: amount <= 0 -> INVALID (non-positive)
        - Condition 2: amount > self.balance -> INVALID (insufficient funds)
        - Condition 3: 0 < amount <= self.balance -> VALID

        Args:
            amount: Amount to withdraw.

        Returns:
            float: Updated account balance after withdrawal.

        Raises:
            ValueError: If withdrawal amount <= 0 or exceeds current balance.
        """
        # Branch 1: Guard condition for non-positive withdrawal amount
        if amount <= 0.0:
            raise ValueError(f"Withdrawal amount must be positive. Received: {amount}")

        # Branch 2: Guard condition for insufficient funds
        if amount > self.balance:
            raise ValueError(
                f"Insufficient funds. Requested: {amount}, Available balance: {self.balance}"
            )

        # Branch 3: Happy path execution
        self.balance -= float(amount)
        return self.balance

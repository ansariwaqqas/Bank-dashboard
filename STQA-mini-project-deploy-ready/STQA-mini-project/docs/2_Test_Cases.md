# Test Case Specification

**Project Title:** Bank Management System (CLI)  
**Course:** Software Testing and Quality Assurance (STQA) – Laboratory Practice IV  
**Academic Body:** Savitribai Phule Pune University (SPPU)  
**Document Ref:** STQA-TC-001  
**Version:** 1.0.0  

---

## 1. Test Suite Overview

This document details the test scenarios, pre-conditions, input parameters, expected outcomes, and actual execution results for both **White-Box Structural Tests** and **Black-Box Functional Integration Tests**.

### Traceability Matrix Summary
- **White-Box Target:** [`app/bank_logic.py`](file:///e:/STQA-mini-project/app/bank_logic.py) (`BankAccount` unit logic)
- **Black-Box Target:** [`app/database.py`](file:///e:/STQA-mini-project/app/database.py) integrated with `BankAccount` and SQLite storage

---

## 2. Test Cases Specification Table

| Test Case ID | Test Scenario / Description | Testing Type | Pre-conditions | Test Steps / Input Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_WB_001** | Verify successful deposit computation and balance update. | **White-Box** (Statement / Branch Coverage) | `BankAccount` initialized with `balance = 100.0`. | 1. Call `deposit(50.0)`.<br>2. Inspect returned balance.<br>3. Inspect internal state `self.balance`. | Branch `amount <= 0.0` is False; balance increments to `150.0`; returns `150.0`. | Balance incremented to `150.0`; return value is `150.0`. | **PASS** |
| **TC_WB_002** | Verify successful partial withdrawal computation. | **White-Box** (Branch Coverage) | `BankAccount` initialized with `balance = 100.0`. | 1. Call `withdraw(40.0)`.<br>2. Check returned balance.<br>3. Check internal `self.balance`. | Both guard branches evaluate to False; balance decrements to `60.0`; returns `60.0`. | Balance decremented to `60.0`; return value is `60.0`. | **PASS** |
| **TC_WB_003** | Verify boundary withdrawal down to exact zero balance. | **White-Box** (Boundary Value Analysis) | `BankAccount` with current balance of `60.0`. | 1. Call `withdraw(60.0)` where `amount == self.balance`. | Condition `amount > balance` evaluates to False; balance becomes `0.0`; returns `0.0`. | Balance reduced to `0.0`; return value is `0.0`. | **PASS** |
| **TC_WB_004** | Verify rejection of negative deposit amount. | **White-Box** (Negative Branch Coverage) | `BankAccount` initialized with `balance = 100.0`. | 1. Call `deposit(-50.0)`.<br>2. Intercept raised exception.<br>3. Verify `self.balance`. | Guard branch `amount <= 0.0` triggers `ValueError("Deposit amount must be positive...")`; balance remains `100.0`. | `ValueError` raised with expected message; balance unchanged at `100.0`. | **PASS** |
| **TC_WB_005** | Verify rejection of boundary zero deposit. | **White-Box** (Boundary Value Analysis) | `BankAccount` initialized with `balance = 100.0`. | 1. Call `deposit(0.0)`.<br>2. Intercept exception.<br>3. Verify balance stability. | Guard branch `amount <= 0.0` triggers `ValueError`; balance unchanged at `100.0`. | `ValueError` raised; balance remained `100.0`. | **PASS** |
| **TC_WB_006** | Verify rejection of fractional negative deposit. | **White-Box** (Boundary Testing) | `BankAccount` initialized with `balance = 100.0`. | 1. Call `deposit(-0.01)`.<br>2. Intercept exception. | Guard branch triggers `ValueError`; internal balance unaltered. | `ValueError` raised; balance preserved. | **PASS** |
| **TC_WB_007** | Verify rejection of non-positive withdrawal requests. | **White-Box** (Guard Branch Testing) | `BankAccount` initialized with `balance = 100.0`. | 1. Call `withdraw(0.0)`.<br>2. Intercept exception. | Guard branch `amount <= 0.0` triggers `ValueError("Withdrawal amount must be positive...")`. | `ValueError` raised with matching error text; balance unchanged. | **PASS** |
| **TC_WB_008** | Verify rejection of overdraft when withdrawal exceeds balance. | **White-Box** (Decision Branch & Boundary) | `BankAccount` with `balance = 100.0`. | 1. Call `withdraw(100.01)` (1 cent higher than balance).<br>2. Verify balance state. | Guard branch `amount > balance` evaluates to True; triggers `ValueError("Insufficient funds...")`; balance remains `100.0`. | `ValueError` raised with "Insufficient funds"; balance remained `100.0`. | **PASS** |
| **TC_BB_001** | Verify user account creation, deposit, and database persistence. | **Black-Box** (End-to-End Integration) | Clean SQLite database table `accounts` initialized. | 1. Call `create_account("Bob Smith", 200.0)`.<br>2. Load account into `BankAccount`.<br>3. Execute `deposit(150.0)`.<br>4. Call `update_balance(acc_id, 350.0)`.<br>5. Query `get_balance(acc_id)`. | Account created with valid integer ID; final persistent database balance strictly equals `$350.0`. | Account ID assigned; query confirmed persisted balance `$350.0`. | **PASS** |
| **TC_BB_002** | Verify multi-user transaction isolation and independent persistence. | **Black-Box** (State Isolation & Concurrency) | Clean SQLite database table `accounts` initialized. | 1. Create Account A ("Charlie", `$500.0`).<br>2. Create Account B ("Diana", `$1000.0`).<br>3. Deposit `$250.0` to A -> Update DB.<br>4. Withdraw `$400.0` from B -> Update DB.<br>5. Query both accounts independently. | Account A balance equals `$750.0`; Account B balance equals `$600.0`; no cross-account state pollution. | DB records show Account A: `$750.0` and Account B: `$600.0`. Zero cross-contamination. | **PASS** |
| **TC_BB_003** | Verify rejection of invalid initial balance during account creation. | **Black-Box** (Input Validation) | SQLite database accessible. | 1. Call `create_account("Eve", -100.0)`.<br>2. Intercept exception. | `ValueError` raised indicating initial balance cannot be negative; no record inserted. | `ValueError` raised; no database row added. | **PASS** |
| **TC_BB_004** | Verify query behavior for non-existent account ID. | **Black-Box** (Robustness / Edge Case) | Database initialized; ID `9999` does not exist. | 1. Call `get_balance(9999)`.<br>2. Call `get_account(9999)`. | Returns `None` gracefully without throwing database unhandled exceptions. | Both queries returned `None` as expected. | **PASS** |

---

## 3. White-Box Logic Coverage Analysis

```mermaid
flowchart TD
    StartDeposit([Start deposit(amount)]) --> CondDep{amount <= 0.0?}
    CondDep -- True --> RaiseDepErr[Raise ValueError: Deposit amount must be positive]
    CondDep -- False --> ExecDep[self.balance += amount]
    ExecDep --> ReturnDep([Return self.balance])

    StartWithdraw([Start withdraw(amount)]) --> CondW1{amount <= 0.0?}
    CondW1 -- True --> RaiseW1Err[Raise ValueError: Withdrawal amount must be positive]
    CondW1 -- False --> CondW2{amount > self.balance?}
    CondW2 -- True --> RaiseW2Err[Raise ValueError: Insufficient funds]
    CondW2 -- False --> ExecW[self.balance -= amount]
    ExecW --> ReturnW([Return self.balance])
```

- **Branch Coverage Achieved:** $4 / 4$ branches ($100\%$)
- **Statement Coverage Achieved:** $100\%$
- **Boundary Conditions Tested:** Minimal positive unit ($0.01$), zero ($0.0$), exact balance equivalence ($amount == balance$), and minimal overdraft ($balance + 0.01$).

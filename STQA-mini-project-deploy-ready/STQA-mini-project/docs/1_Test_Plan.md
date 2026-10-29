# Software Test Plan (STP)

**Project Title:** Bank Management System (CLI)  
**Course:** Software Testing and Quality Assurance (STQA) – Laboratory Practice IV  
**Academic Body:** Savitribai Phule Pune University (SPPU)  
**Standard:** IEEE 829 Standard for Software Test Documentation  
**Version:** 1.0.0  
**Date:** October 2026  

---

## 1. Introduction and Objectives

### 1.1 Document Purpose
This Software Test Plan (STP) specifies the overall test strategy, verification environment, test deliverables, resource allocation, and quality risk management for the Python-based **Command Line Interface (CLI) Bank Management System**. The primary objective is to validate both structural logic (White-Box testing) and functional system integration with local SQLite persistence (Black-Box testing) to satisfy SPPU LP-IV engineering laboratory benchmarks.

### 1.2 Testing Objectives
1. **Structural Integrity:** Validate that all internal decision paths, condition evaluations, and exception guards in [`app/bank_logic.py`](file:///e:/STQA-mini-project/app/bank_logic.py) achieve 100% statement and branch coverage.
2. **Functional Correctness:** Ensure business rules (non-negative balances, positive transaction amounts, prevention of overdrafts) are strictly enforced.
3. **Data Persistence & ACID Adherence:** Verify that account creation, balance updates, and transaction sequences are accurately committed to the SQLite database without state leakage between accounts.
4. **Resilience & Error Handling:** Validate that unauthorized inputs raise explicit, well-defined exceptions (`ValueError`) without corrupting stored data or terminating the process ungracefully.

---

## 2. Scope of Testing

### 2.1 Features to be Tested
- **Account Onboarding:** Creation of bank accounts with unique auto-incremented identifiers, non-empty holder names, and initial non-negative balances.
- **Deposit Mechanism:** Acceptance of positive credits, accurate state computation, and database update.
- **Withdrawal Mechanism:** Successful debit within available funds, boundary condition where balance reaches exact zero, and rejection of negative/zero requests.
- **Overdraft Guard:** Rejection of withdrawals exceeding current balance with informative error messages.
- **Data Persistence:** Consistency of SQLite database transactions, schema validation, and retrieval of balance/account metadata.
- **Input Validation:** Rejection of invalid data types, zero amounts, negative numbers, and empty names.

### 2.2 Features Not to be Tested (Out of Scope)
- **Multi-Currency Conversion:** Forex transactions and foreign exchange rate conversions (system is fixed to single-currency fiat model).
- **Online Payment Gateways:** External integrations (e.g., Stripe, PayPal, UPI) as this is a standalone desktop CLI application.
- **Distributed Database Synchronization:** Multi-node replication, network partition tolerance, or distributed two-phase locking.
- **Multi-Factor Authentication (MFA):** Biometric or SMS OTP authentication workflows.
- **Concurrent Multi-Threading:** High-concurrency race condition testing across multiple write threads on a single SQLite lock file.

---

## 3. Test Environment and Infrastructure

| Component | Specification |
| :--- | :--- |
| **Operating System** | Windows 11 / Linux (Ubuntu 22.04 LTS compatible) |
| **Runtime Environment** | Python 3.13+ 64-bit |
| **Database Engine** | SQLite 3.x (Embedded via Python standard library `sqlite3`) |
| **Test Framework** | Pytest 8.x / 9.x |
| **Test Isolation** | Pytest built-in `tmp_path` fixture for per-test dynamic database creation |
| **Version Control** | Git |

---

## 4. Test Strategy and Methodologies

```
┌────────────────────────────────────────────────────────┐
│               STQA DUAL TESTING PYRAMID                │
├────────────────────────────────────────────────────────┤
│                                                        │
│   ▲  BLACK-BOX INTEGRATION TESTING (`test_blackbox.py`)│
│  ───  - User stories (Account Creation -> Deposit)     │
│       - SQLite database state verification             │
│       - Multi-account state isolation                  │
│                                                        │
│   ▲  WHITE-BOX UNIT TESTING (`test_whitebox.py`)       │
│  ───  - 100% Branch / Decision Coverage                │
│       - Statement Coverage of `BankAccount` methods    │
│       - Boundary Value Analysis (0.0, balance + 0.01)   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 4.1 White-Box Testing (Structural / Glass-Box)
- **Scope:** Unit-level verification of [`app/bank_logic.py`](file:///e:/STQA-mini-project/app/bank_logic.py).
- **Methodology:** The tester uses full knowledge of source code structures.
  - **Statement Coverage:** Guarantees every single line of code in `deposit()`, `withdraw()`, and `__init__()` executes at least once.
  - **Branch / Decision Coverage:** Evaluates both `True` and `False` paths for all conditional statements:
    - Decision 1: `if amount <= 0.0:` in `deposit()`
    - Decision 2: `if amount <= 0.0:` in `withdraw()`
    - Decision 3: `if amount > self.balance:` in `withdraw()`
  - **Exception Verification:** Using `pytest.raises(ValueError)` to verify that exceptional states are raised with appropriate error strings.

### 4.2 Black-Box Testing (Functional / Specification-Based)
- **Scope:** Integration testing across [`app/database.py`](file:///e:/STQA-mini-project/app/database.py) and [`app/bank_logic.py`](file:///e:/STQA-mini-project/app/bank_logic.py).
- **Methodology:** Testing based purely on software requirements specifications without examining internal branching.
  - **Equivalence Partitioning (EP):** Partitioning transaction amounts into valid equivalence classes ($> 0$) and invalid equivalence classes ($\le 0$).
  - **Boundary Value Analysis (BVA):** Testing boundary values such as exact balance withdrawal ($A = B$) and marginal overdraft ($A = B + 0.01$).
  - **State Transition & Persistence Testing:** Verifying that database state transitions from uninitialized to initialized, and balances accurately persist after consecutive commits.

---

## 5. Defect Taxonomy and Classification

Defects identified during test execution are categorized according to the following standardized matrix:

| Defect Category | Description | Severity | Priority | Typical Example |
| :--- | :--- | :--- | :--- | :--- |
| **Functional Defect** | The system fails to compute balance accurately or fails to update records. | **Critical** | **P1 (Immediate)** | Balance does not increment after deposit, or debit calculation is mathematically incorrect. |
| **Boundary / Input Validation** | System permits out-of-range, negative, or zero financial transactions. | **Major** | **P1 (High)** | System accepts a negative deposit (`-$50.00`) and reduces account balance instead of raising `ValueError`. |
| **Database Integrity Defect** | Data fails to persist, foreign keys break, or cross-account state leakage occurs. | **Critical** | **P2 (High)** | Withdrawing from Account A inadvertently modifies the persisted balance of Account B. |
| **UI / Error Handling Defect** | Cryptic error messages, unhandled stack traces, or missing user prompts in CLI. | **Minor** | **P3 (Medium)** | Application crashes with raw `sqlite3.OperationalError` instead of user-friendly message. |

### Severity Definitions
- **Critical:** System crash, data loss, mathematical corruption of financial ledgers.
- **Major:** Core business rule violation without system crash (e.g., negative deposit permitted).
- **Moderate:** Non-critical functionality defect; viable workaround exists.
- **Minor:** Cosmetic, formatting, or minor messaging discrepancies.

---

## 6. Suspension and Resumption Criteria

- **Suspension Criteria:** Testing is halted if test environment setup fails, if the database schema fails to initialize, or if critical dependencies cannot be imported.
- **Resumption Criteria:** Testing resumes once the database initialization script [`init_db()`](file:///e:/STQA-mini-project/app/database.py#L22) passes and all syntax linter errors are resolved.

---

## 7. Test Deliverables
1. **Software Test Plan:** [`docs/1_Test_Plan.md`](file:///e:/STQA-mini-project/docs/1_Test_Plan.md)
2. **Test Cases Specification:** [`docs/2_Test_Cases.md`](file:///e:/STQA-mini-project/docs/2_Test_Cases.md)
3. **Software Test Execution Report:** [`docs/3_Test_Report.md`](file:///e:/STQA-mini-project/docs/3_Test_Report.md)
4. **Automated Pytest Test Suites:** [`tests/test_whitebox.py`](file:///e:/STQA-mini-project/tests/test_whitebox.py) and [`tests/test_blackbox.py`](file:///e:/STQA-mini-project/tests/test_blackbox.py)

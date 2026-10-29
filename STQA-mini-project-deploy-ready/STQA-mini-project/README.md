# CLI Bank Management System (STQA Mini-Project)

A Python-based Command Line Interface (CLI) Bank Management System built to demonstrate **Software Testing and Quality Assurance (STQA)** principles, specifically contrasting **White-Box Testing** and **Black-Box Integration Testing**.

---

## 📁 Project Structure

```text
STQA-mini-project/
├── frontend/                 # Client-side presentation layer
│   ├── index.html            # NextGen Cyber-Fintech UI Dashboard
│   ├── style.css             # Modern Cyber-Fintech Glassmorphism Design
│   └── app.js                # Interactive Client Logic, Testing Lab & Docs Viewer
├── backend/                  # Server-side logic, API & test suite
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py       # Database proxy/adapter (preserves app.database imports)
│   │   └── bank_logic.py     # BankAccount class with business logic & validations
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_whitebox.py  # White-box unit tests (Branch & Decision coverage)
│   │   └── test_blackbox.py  # Black-box integration tests (E2E User flows & DB state)
│   ├── app.py                # Unified REST API & HTTP Application Server
│   ├── main.py               # Interactive CLI Application
│   ├── seed_db.py            # Backend seed shortcut
│   ├── pytest.ini            # Pytest configuration (backend)
│   └── requirements.txt      # Backend dependencies
├── database/                 # Dedicated database management layer
│   ├── __init__.py           # Database package exports
│   ├── database.py           # Core SQLite connection & CRUD operations
│   ├── schema.sql            # Table schema definition (accounts)
│   ├── seed_db.py            # Database seeder utility
│   └── bank.db               # SQLite database file
├── docs/                     # University documentation & STQA artifacts
│   ├── 1_Test_Plan.md        # SPPU Standard Test Plan & Bug Taxonomy
│   ├── 2_Test_Cases.md       # White-box & Black-box Test Cases with procedures
│   └── 3_Test_Report.md      # Test Execution Report & Traceability Matrix
├── run.py                    # Root quick-launcher (starts backend server & frontend UI)
├── pytest.ini                # Pytest configuration (root)
├── requirements.txt          # Project dependencies (root)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup and Execution

### 1. Environment Setup
```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows Command Prompt:
.\.venv\Scripts\activate.bat
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Running Tests
Run the entire Pytest test suite with verbose output:
```bash
pytest -v
```

Run only White-Box tests:
```bash
pytest backend/tests/test_whitebox.py -v
```

Run only Black-Box tests:
```bash
pytest backend/tests/test_blackbox.py -v
```

*(Note: You can also `cd backend` and run `pytest -v` directly)*

### 3. Running the CLI Application
```bash
python backend/main.py
```

### 4. Running the NextGen Web Dashboard & API Server
From the project root:
```bash
python run.py
```
Or directly from the backend folder:
```bash
python backend/app.py
```
*(Automatically starts the server and opens `http://localhost:5000` in your default browser)*



---

## 🧪 Testing Methodology & STQA Principles

| Aspect | White-Box Testing (`tests/test_whitebox.py`) | Black-Box Testing (`tests/test_blackbox.py`) |
| :--- | :--- | :--- |
| **Focus** | Internal code structure, logic branches, and statements | System requirements, user interactions, and external state |
| **Knowledge Needed** | Full visibility into `app/bank_logic.py` source code | No internal knowledge needed; uses public database & account APIs |
| **Techniques Used** | Statement Coverage, Decision/Branch Coverage, Guard Check testing | Equivalence Partitioning, Integration Testing, Database State Verification |
| **Scope** | Unit-level (`BankAccount` methods) | Subsystem integration (`database.py` + `bank_logic.py` + SQLite) |
| **Isolation** | Fixtures instantiating in-memory `BankAccount` objects | Isolated temporary SQLite database per test (`tmp_path`) |


## 🌐 Live Deployment

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for the step-by-step instructions to publish this project on Render. A `render.yaml` Blueprint is included and the server reads the platform's `PORT` environment variable automatically.

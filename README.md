# STQA Mini-Project: Bank Management System

A Python-based Bank Management System developed as a **Software Testing and Quality Assurance (STQA)** mini-project. It includes a browser-based dashboard, a Python HTTP/REST API server, SQLite data storage, and automated white-box and black-box tests.

> **Academic demo only:** This project simulates basic banking operations. It is not intended for real banking, real payments, or storage of real personal or financial information.

## Features

- Browser-based dashboard built with HTML, CSS, and JavaScript
- Python server and REST API using Python's standard library
- SQLite database for sample account records and balances
- Account creation, balance viewing, deposits, and withdrawals
- Input validation for invalid amounts and insufficient funds
- STQA Testing Lab and project test documentation
- Automated tests with `pytest`
- Render deployment configuration in `render.yaml`

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3 |
| HTTP/API server | Python standard library (`http.server`) |
| Database | SQLite |
| Automated testing | pytest |
| Deployment configuration | Render Blueprint |

## Project Structure

```text
STQA-mini-project/
├── frontend/
│   ├── index.html          # Web dashboard
│   ├── style.css           # Dashboard styling
│   └── app.js              # Frontend behavior and testing lab
├── backend/
│   ├── app/
│   │   ├── database.py     # Database adapter
│   │   └── bank_logic.py   # Account operations and validation
│   ├── tests/
│   │   ├── test_whitebox.py
│   │   └── test_blackbox.py
│   ├── app.py              # HTTP server and REST API
│   ├── main.py             # CLI application
│   └── requirements.txt
├── database/
│   ├── database.py         # SQLite operations
│   ├── schema.sql          # Database schema
│   ├── seed_db.py          # Sample-data seeder
│   └── bank.db             # Sample SQLite database
├── docs/
│   ├── 1_Test_Plan.md      # Test plan
│   ├── 2_Test_Cases.md     # Test cases and procedures
│   └── 3_Test_Report.md    # Test execution report
├── render.yaml             # Render service configuration
├── requirements.txt        # Root Python dependencies
├── pytest.ini              # pytest configuration
├── run.py                  # Local quick launcher
├── DEPLOYMENT.md           # Deployment instructions
└── README.md
```

## Requirements

- Python 3.10 or newer recommended
- `pip`
- A modern web browser

## Run Locally

1. Clone or download this repository and open a terminal in the project root.
2. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Windows Command Prompt**
   ```bat
   python -m venv .venv
   .\.venv\Scripts\activate.bat
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the web application from the project root:

   ```bash
   python run.py
   ```

   If needed, start the server directly:

   ```bash
   python backend/app.py
   ```

5. Open **http://localhost:5000** in your browser when running locally. If you start the server directly, use the address and port printed by the server or configured by your environment.

### Run the CLI version

```bash
python backend/main.py
```

## Run the Automated Tests

Run all tests from the project root:

```bash
pytest -v
```

Run white-box tests only:

```bash
pytest backend/tests/test_whitebox.py -v
```

Run black-box tests only:

```bash
pytest backend/tests/test_blackbox.py -v
```

The packaged project has a documented baseline of **8 passing tests**. Run the tests in your own environment to confirm the current result.

## STQA Testing Approach

### White-box testing
Tests internal business logic and decision paths in the account operations. The suite checks valid transactions, invalid amounts, and insufficient-funds handling.

### Black-box / integration testing
Tests workflows through the database and account logic, including account creation, transaction updates, persisted balances, and isolation between accounts.

### Project documentation
The `docs/` directory contains the test plan, test cases, and test execution report. These documents are included as academic project artifacts; actual test results should be reproduced in the environment used for submission.

## Deployment

A Render Blueprint configuration is included in `render.yaml`.

1. Push this repository to GitHub.
2. Sign in to [Render](https://dashboard.render.com/).
3. Choose **New → Blueprint** and connect this GitHub repository.
4. Review the service configuration and deploy.
5. Open the public `onrender.com` URL after the service reports that it is live.

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for the detailed steps.

### Deployment notes

- The service uses the platform-provided `PORT` environment variable.
- On free hosting, the service may sleep while idle and take time to wake up.
- A local SQLite database on an ephemeral hosting filesystem may be reset after a restart, redeploy, or spin-down. Do not rely on it for permanent data storage.
- The demo does not provide production-grade authentication or security. Use sample data only.

## Future Enhancements

- Add authentication and role-based access
- Add transaction history and audit logging
- Use managed persistent database storage
- Add CI workflow to run automated tests on every push
- Expand test coverage and publish coverage reports

## Authors

Add your team members' names, class/division, roll numbers, and institute details here before submitting the project.

## License

This repository is intended for educational use. Add a license file if you want to specify reuse and distribution terms.

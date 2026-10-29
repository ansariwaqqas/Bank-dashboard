"""
NextGen Bank Portal - Unified HTTP & REST API Application Server.
Zero-dependency server using Python standard library (http.server).
Serves the modern HTML5/CSS3/JS Fintech Web Application and provides
REST API endpoints directly wired to app.database and app.bank_logic.
Automatically launches default web browser on startup.
"""

import json
import os
import subprocess
import sys
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Ensure backend and project root are in sys.path
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import (
    DEFAULT_DB_PATH,
    init_db,
    create_account,
    get_account,
    update_balance,
    get_balance,
    get_connection,
)
from app.bank_logic import BankAccount

# Initialize SQLite database
init_db()

FRONTEND_DIR = PROJECT_ROOT / "frontend" if (PROJECT_ROOT / "frontend").exists() else BACKEND_DIR / "frontend"
DOCS_DIR = PROJECT_ROOT / "docs" if (PROJECT_ROOT / "docs").exists() else BACKEND_DIR / "docs"


class BankRequestHandler(SimpleHTTPRequestHandler):
    """Handles HTTP requests for static assets and REST API operations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response with CORS and cache control headers."""
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(response_bytes)

    def _read_json_body(self) -> dict:
        """Parse incoming JSON payload from request body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        return json.loads(body.decode("utf-8"))

    def do_OPTIONS(self):
        """Handle CORS pre-flight checks."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Handle static files and GET API routes."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # API: System Overview & Stats
        if path == "/api/stats":
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*), COALESCE(SUM(balance), 0.0) FROM accounts;")
                    total_acc, total_bal = cursor.fetchone()
                self._send_json({
                    "total_accounts": int(total_acc),
                    "total_liquidity": float(total_bal),
                    "status": "online",
                    "engine": "SQLite3 + Pytest"
                })
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # API: List all accounts
        if path == "/api/accounts":
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, name, balance FROM accounts ORDER BY id DESC;")
                    rows = cursor.fetchall()
                    accounts = [{"id": r["id"], "name": r["name"], "balance": float(r["balance"])} for r in rows]
                self._send_json({"accounts": accounts})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # API: Get single account details `/api/account?id=1`
        if path == "/api/account":
            query = parse_qs(parsed_url.query)
            acc_id = query.get("id", [None])[0]
            if not acc_id or not acc_id.isdigit():
                self._send_json({"error": "Invalid or missing account ID parameter."}, 400)
                return

            account = get_account(int(acc_id))
            if account:
                self._send_json({"account": account})
            else:
                self._send_json({"error": f"Account #{acc_id} not found."}, 404)
            return

        # API: Run Automated STQA Tests (White-Box / Black-Box / All)
        if path == "/api/run-tests":
            query = parse_qs(parsed_url.query)
            test_type = query.get("type", ["all"])[0].lower()

            cmd = [sys.executable, "-m", "pytest", "-v"]
            if test_type == "whitebox":
                cmd.append("tests/test_whitebox.py")
            elif test_type == "blackbox":
                cmd.append("tests/test_blackbox.py")

            try:
                res = subprocess.run(cmd, cwd=str(BACKEND_DIR), capture_output=True, text=True)
                output = res.stdout or res.stderr

                # Parse lines to extract individual test case results
                cases = []
                for line in output.splitlines():
                    if "PASSED" in line or "FAILED" in line:
                        parts = line.split()
                        test_name = parts[0]
                        status = "PASSED" if "PASSED" in line else "FAILED"
                        cases.append({"name": test_name, "status": status})

                passed_count = sum(1 for c in cases if c["status"] == "PASSED")
                failed_count = sum(1 for c in cases if c["status"] == "FAILED")
                total_count = len(cases)
                pass_rate = 100.0 if total_count > 0 and failed_count == 0 else (0.0 if total_count == 0 else round((passed_count / total_count) * 100, 1))

                self._send_json({
                    "success": res.returncode == 0,
                    "test_type": test_type,
                    "total": total_count,
                    "passed": passed_count,
                    "failed": failed_count,
                    "pass_rate": f"{pass_rate:.1f}%",
                    "cases": cases,
                    "output": output
                })
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # API: Fetch University Documentation (Test Plan, Test Cases, Test Report)
        if path == "/api/docs":
            query = parse_qs(parsed_url.query)
            doc_type = query.get("type", ["plan"])[0].lower()
            doc_map = {
                "plan": DOCS_DIR / "1_Test_Plan.md",
                "cases": DOCS_DIR / "2_Test_Cases.md",
                "report": DOCS_DIR / "3_Test_Report.md"
            }
            target_file = doc_map.get(doc_type, doc_map["plan"])
            if target_file.exists():
                self._send_json({
                    "title": target_file.name,
                    "content": target_file.read_text(encoding="utf-8")
                })
            else:
                self._send_json({"error": "Documentation file not found."}, 404)
            return

        # Otherwise serve static files from /web/
        if path == "/" or not path:
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        """Handle POST API routes."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        try:
            body = self._read_json_body()
        except Exception:
            self._send_json({"error": "Malformed JSON body."}, 400)
            return

        # API: Create Account
        if path == "/api/accounts":
            name = body.get("name", "")
            initial_balance = float(body.get("initial_balance", 0.0))
            try:
                new_id = create_account(name=name, initial_balance=initial_balance)
                self._send_json({
                    "success": True,
                    "message": "Account created successfully.",
                    "account": {
                        "id": new_id,
                        "name": name.strip(),
                        "balance": initial_balance
                    }
                }, 201)
            except ValueError as ve:
                self._send_json({"error": str(ve)}, 400)
            except Exception as e:
                self._send_json({"error": f"Internal error: {e}"}, 500)
            return

        # API: Deposit Funds
        if path == "/api/deposit":
            acc_id = body.get("account_id")
            amount = float(body.get("amount", 0.0))

            if not acc_id:
                self._send_json({"error": "Missing account_id."}, 400)
                return

            acc_data = get_account(int(acc_id))
            if not acc_data:
                self._send_json({"error": f"Account #{acc_id} does not exist."}, 404)
                return

            try:
                # Business Logic Execution
                account = BankAccount(
                    account_id=acc_data["id"],
                    name=acc_data["name"],
                    balance=acc_data["balance"]
                )
                old_balance = account.balance
                new_balance = account.deposit(amount)

                # SQLite Persistence
                update_balance(acc_data["id"], new_balance)

                self._send_json({
                    "success": True,
                    "account_id": acc_data["id"],
                    "name": acc_data["name"],
                    "old_balance": old_balance,
                    "amount": amount,
                    "new_balance": new_balance,
                    "message": f"Successfully deposited ${amount:,.2f}."
                })
            except ValueError as ve:
                self._send_json({"error": str(ve)}, 400)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # API: Withdraw Funds
        if path == "/api/withdraw":
            acc_id = body.get("account_id")
            amount = float(body.get("amount", 0.0))

            if not acc_id:
                self._send_json({"error": "Missing account_id."}, 400)
                return

            acc_data = get_account(int(acc_id))
            if not acc_data:
                self._send_json({"error": f"Account #{acc_id} does not exist."}, 404)
                return

            try:
                # Business Logic Execution
                account = BankAccount(
                    account_id=acc_data["id"],
                    name=acc_data["name"],
                    balance=acc_data["balance"]
                )
                old_balance = account.balance
                new_balance = account.withdraw(amount)

                # SQLite Persistence
                update_balance(acc_data["id"], new_balance)

                self._send_json({
                    "success": True,
                    "account_id": acc_data["id"],
                    "name": acc_data["name"],
                    "old_balance": old_balance,
                    "amount": amount,
                    "new_balance": new_balance,
                    "message": f"Successfully withdrew ${amount:,.2f}."
                })
            except ValueError as ve:
                self._send_json({"error": str(ve)}, 400)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        self._send_json({"error": "Endpoint not found."}, 404)


def open_browser(port: int = 5000):
    """Wait briefly for the server to bind, then automatically open the browser."""
    time.sleep(1.0)
    webbrowser.open(f"http://localhost:{port}")


def run_server(port: int = 5000, launch_browser: bool = True):
    """Start the multi-threaded HTTP server and optionally open browser."""
    if launch_browser:
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, BankRequestHandler)
    print("\n" + "=" * 55)
    print(" [+] NextGen Bank Portal Web Server Running!")
    print(f" [*] Access at: http://localhost:{port}")
    print(f" [*] Serving UI from: {FRONTEND_DIR}")
    print(f" [*] Connected to SQLite: {DEFAULT_DB_PATH}")
    print("=" * 55 + "\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server stopped by user.")
        httpd.server_close()


if __name__ == "__main__":
    # Cloud platforms such as Render provide the listening port in PORT.
    # Retain the CLI argument and localhost default for local development.
    port_value = os.environ.get("PORT") or (sys.argv[1] if len(sys.argv) > 1 else "5000")
    port = int(port_value)
    # A hosted service must not attempt to open a browser on the server machine.
    run_server(port, launch_browser=not bool(os.environ.get("RENDER") or os.environ.get("PORT")))

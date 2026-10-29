/**
 * NextGen Bank Portal - Modern Vanilla Frontend Application
 * Handles API orchestration, 3D card tilt physics, reactive state, and modals.
 */

class BankApp {
    constructor() {
        this.apiBase = "";
        this.currentAccount = null;
        this.accounts = [];
        this.init();
    }

    async init() {
        this.bindEvents();
        this.init3DTilt();
        await this.loadInitialData();
        if (window.lucide) {
            lucide.createIcons();
        }
    }

    // =========================================================================
    // API Helper Methods
    // =========================================================================
    async apiFetch(endpoint, options = {}) {
        try {
            const res = await fetch(endpoint, {
                headers: { "Content-Type": "application/json" },
                ...options,
            });
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error || `HTTP error ${res.status}`);
            }
            return data;
        } catch (err) {
            console.error(`API Error on ${endpoint}:`, err);
            throw err;
        }
    }

    async loadInitialData() {
        try {
            await Promise.all([this.fetchStats(), this.fetchAccounts()]);
        } catch (err) {
            this.showToast("error", "Connection Error", "Failed to reach SQLite backend server.");
        }
    }

    async fetchStats() {
        try {
            const data = await this.apiFetch("/api/stats");
            document.getElementById("kpi-total-accounts").textContent = data.total_accounts;
            document.getElementById("kpi-total-liquidity").textContent = `$${data.total_liquidity.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        } catch (err) {
            console.warn("Could not load stats", err);
        }
    }

    async fetchAccounts() {
        try {
            const data = await this.apiFetch("/api/accounts");
            this.accounts = data.accounts || [];
            this.renderAccountSelect();
            this.renderAccountsTable();

            // Set active account to the first one or maintain selection
            if (this.accounts.length > 0) {
                const existingId = this.currentAccount ? this.currentAccount.id : null;
                const matched = this.accounts.find(a => a.id === existingId);
                this.setActiveAccount(matched || this.accounts[0]);
            } else {
                this.setActiveAccount(null);
            }
        } catch (err) {
            console.warn("Could not load accounts", err);
        }
    }

    setActiveAccount(account) {
        this.currentAccount = account;
        if (!account) {
            document.getElementById("vc-acc-number").textContent = "•••• •••• •••• ----";
            document.getElementById("vc-holder-name").textContent = "NO ACCOUNT SELECTED";
            document.getElementById("vc-balance").textContent = "$0.00";
            document.getElementById("kpi-active-balance").textContent = "$0.00";
            document.getElementById("spec-id").textContent = "#--";
            document.getElementById("spec-name").textContent = "--";
            document.getElementById("withdraw-available-bal").textContent = "$0.00";
            return;
        }

        // Format virtual card
        const paddedId = String(account.id).padStart(4, "0");
        document.getElementById("vc-acc-number").textContent = `4532  ••••  ••••  ${paddedId}`;
        document.getElementById("vc-holder-name").textContent = account.name.toUpperCase();
        
        const formattedBal = `$${account.balance.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        document.getElementById("vc-balance").textContent = formattedBal;
        document.getElementById("kpi-active-balance").textContent = formattedBal;

        // Spec Panel
        document.getElementById("spec-id").textContent = `#${account.id}`;
        document.getElementById("spec-name").textContent = account.name;
        document.getElementById("withdraw-available-bal").textContent = formattedBal;

        // Sync inputs
        const depAccInput = document.getElementById("deposit-target-account");
        if (depAccInput) depAccInput.value = account.id;

        const wAccInput = document.getElementById("withdraw-target-account");
        if (wAccInput) wAccInput.value = account.id;

        // Sync dropdown
        const select = document.getElementById("active-account-select");
        if (select && select.value !== String(account.id)) {
            select.value = String(account.id);
        }
    }

    renderAccountSelect() {
        const select = document.getElementById("active-account-select");
        select.innerHTML = "";

        if (this.accounts.length === 0) {
            const opt = document.createElement("option");
            opt.value = "";
            opt.textContent = "No Accounts Found";
            select.appendChild(opt);
            return;
        }

        this.accounts.forEach(acc => {
            const opt = document.createElement("option");
            opt.value = acc.id;
            opt.textContent = `#${acc.id} - ${acc.name} ($${acc.balance.toFixed(2)})`;
            select.appendChild(opt);
        });

        if (this.currentAccount) {
            select.value = String(this.currentAccount.id);
        }
    }

    renderAccountsTable() {
        const tbody = document.getElementById("accounts-table-body");
        tbody.innerHTML = "";

        if (this.accounts.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:#94a3b8;">No registered bank accounts found. Create one above!</td></tr>`;
            return;
        }

        this.accounts.forEach(acc => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td class="mono">#${acc.id}</td>
                <td><b>${acc.name}</b></td>
                <td class="mono text-cyan">$${acc.balance.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                <td><span class="badge-status">Active</span></td>
                <td>
                    <button class="btn-ghost" onclick="app.selectAccountById(${acc.id})">
                        Select
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    selectAccountById(id) {
        const acc = this.accounts.find(a => a.id === id);
        if (acc) {
            this.setActiveAccount(acc);
            this.switchTab("tab-overview");
            this.showToast("success", "Account Selected", `Loaded #${acc.id} (${acc.name})`);
        }
    }

    // =========================================================================
    // Tab Navigation & UI Events
    // =========================================================================
    switchTab(tabId) {
        document.querySelectorAll(".view-panel").forEach(p => p.classList.remove("active"));
        document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));

        const targetPanel = document.getElementById(tabId);
        if (targetPanel) {
            targetPanel.classList.add("active");
            if (window.lucide) {
                lucide.createIcons();
            }
        }

        const activeNavBtn = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
        if (activeNavBtn) {
            activeNavBtn.classList.add("active");
        }

        if (tabId === "tab-docs") {
            this.loadDoc("plan");
        }
    }

    bindEvents() {
        // Tab switching
        document.querySelectorAll(".nav-item").forEach(btn => {
            btn.addEventListener("click", () => {
                const tab = btn.getAttribute("data-tab");
                this.switchTab(tab);
            });
        });

        // Account select change
        document.getElementById("active-account-select").addEventListener("change", (e) => {
            const selectedId = parseInt(e.target.value, 10);
            this.selectAccountById(selectedId);
        });

        // Refresh table button
        document.getElementById("btn-refresh-accounts").addEventListener("click", async () => {
            await this.loadInitialData();
            this.showToast("success", "Ledger Synchronized", "Refreshed live SQLite tables.");
        });

        // Quick Preset Chips for Deposit
        document.querySelectorAll(".preset-chip").forEach(chip => {
            chip.addEventListener("click", () => {
                const amount = chip.getAttribute("data-amount");
                document.getElementById("deposit-amount").value = amount;
            });
        });

        // Forms & Labs
        this.bindDepositForm();
        this.bindWithdrawForm();
        this.bindCreateAccountForm();
        this.bindSTQAModal();
        this.bindSTQALab();
    }

    bindDepositForm() {
        const form = document.getElementById("form-deposit");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const accId = parseInt(document.getElementById("deposit-target-account").value, 10);
            const amount = parseFloat(document.getElementById("deposit-amount").value);

            if (isNaN(accId) || isNaN(amount)) {
                this.showToast("error", "Validation Error", "Please provide a valid Account ID and Amount.");
                return;
            }

            try {
                const res = await this.apiFetch("/api/deposit", {
                    method: "POST",
                    body: JSON.stringify({ account_id: accId, amount: amount }),
                });

                this.showToast("success", "Deposit Successful", res.message);
                document.getElementById("deposit-amount").value = "";
                await this.loadInitialData();
                this.selectAccountById(accId);
            } catch (err) {
                this.showToast("error", "Deposit Rejected", err.message);
            }
        });
    }

    bindWithdrawForm() {
        const form = document.getElementById("form-withdraw");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const accId = parseInt(document.getElementById("withdraw-target-account").value, 10);
            const amount = parseFloat(document.getElementById("withdraw-amount").value);

            if (isNaN(accId) || isNaN(amount)) {
                this.showToast("error", "Validation Error", "Please provide a valid Account ID and Amount.");
                return;
            }

            try {
                const res = await this.apiFetch("/api/withdraw", {
                    method: "POST",
                    body: JSON.stringify({ account_id: accId, amount: amount }),
                });

                this.showToast("success", "Withdrawal Approved", res.message);
                document.getElementById("withdraw-amount").value = "";
                await this.loadInitialData();
                this.selectAccountById(accId);
            } catch (err) {
                this.showToast("error", "Withdrawal Rejected (Guard Clause)", err.message);
            }
        });
    }

    bindCreateAccountForm() {
        const form = document.getElementById("form-create-account");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("create-name").value.trim();
            const initialDeposit = parseFloat(document.getElementById("create-initial-deposit").value);

            if (!name) {
                this.showToast("error", "Validation Error", "Account holder name cannot be empty.");
                return;
            }

            try {
                const res = await this.apiFetch("/api/accounts", {
                    method: "POST",
                    body: JSON.stringify({ name: name, initial_balance: initialDeposit }),
                });

                this.showToast("success", "Account Issued", `Account #${res.account.id} created for ${res.account.name}!`);
                form.reset();
                await this.loadInitialData();
                this.selectAccountById(res.account.id);
                this.switchTab("tab-overview");
            } catch (err) {
                this.showToast("error", "Registration Failed", err.message);
            }
        });
    }

    // =========================================================================
    // STQA Test Runner Modal
    // =========================================================================
    bindSTQAModal() {
        const modal = document.getElementById("stqa-modal");
        const openBtn = document.getElementById("btn-stqa-modal");
        const closeBtn = document.getElementById("btn-close-modal");
        const runBtn = document.getElementById("btn-run-tests-live");
        const terminal = document.getElementById("terminal-output");
        const spinner = document.getElementById("test-run-spinner");

        openBtn.addEventListener("click", () => modal.classList.add("active"));
        closeBtn.addEventListener("click", () => modal.classList.remove("active"));
        modal.addEventListener("click", (e) => {
            if (e.target === modal) modal.classList.remove("active");
        });

        runBtn.addEventListener("click", async () => {
            terminal.textContent = "Executing Pytest test runner (tests/test_whitebox.py & tests/test_blackbox.py)...";
            spinner.classList.remove("hidden");
            runBtn.disabled = true;

            try {
                const res = await this.apiFetch("/api/run-tests");
                terminal.textContent = res.output;
                if (res.success) {
                    this.showToast("success", "STQA Tests Passed", "All white-box and black-box tests verified!");
                } else {
                    this.showToast("error", "Test Failures", "Some test assertions did not pass.");
                }
            } catch (err) {
                terminal.textContent = `Error running tests: ${err.message}`;
            } finally {
                spinner.classList.add("hidden");
                runBtn.disabled = false;
            }
        });
    }

    // =========================================================================
    // STQA Testing Lab & Dynamic Report Generator
    // =========================================================================
    bindSTQALab() {
        const btnWhite = document.getElementById("btn-lab-run-whitebox");
        const btnBlack = document.getElementById("btn-lab-run-blackbox");
        const btnAll = document.getElementById("btn-lab-run-all");

        if (btnWhite) {
            btnWhite.addEventListener("click", () => this.runTestsAndRenderReport("whitebox"));
        }
        if (btnBlack) {
            btnBlack.addEventListener("click", () => this.runTestsAndRenderReport("blackbox"));
        }
        if (btnAll) {
            btnAll.addEventListener("click", () => this.runTestsAndRenderReport("all"));
        }
    }

    async runTestsAndRenderReport(testType) {
        const reportSection = document.getElementById("lab-report-section");
        const titleEl = document.getElementById("report-title");
        const timestampEl = document.getElementById("report-timestamp");
        const kpiTotal = document.getElementById("report-kpi-total");
        const kpiPassed = document.getElementById("report-kpi-passed");
        const kpiFailed = document.getElementById("report-kpi-failed");
        const kpiRate = document.getElementById("report-kpi-rate");
        const tbody = document.getElementById("report-cases-tbody");
        const statementEl = document.getElementById("acceptance-statement");
        const rawOutput = document.getElementById("lab-raw-output");
        const badgeVerdict = document.getElementById("report-verdict-badge");

        let displayTitle = "STQA Automated Test Execution Report";
        if (testType === "whitebox") {
            displayTitle = "White-Box Structural Test Report (tests/test_whitebox.py)";
        } else if (testType === "blackbox") {
            displayTitle = "Black-Box Integration Test Report (tests/test_blackbox.py)";
        } else {
            displayTitle = "STQA Comprehensive Test Execution Report (Combined Suite)";
        }

        this.showToast("info", "Executing Test Suite", `Running ${testType} test verification...`);

        try {
            const res = await this.apiFetch(`/api/run-tests?type=${testType}`);

            titleEl.textContent = displayTitle;
            timestampEl.textContent = `Generated on ${new Date().toLocaleTimeString()} · Engine: Pytest 9.x`;
            kpiTotal.textContent = res.total;
            kpiPassed.textContent = res.passed;
            kpiFailed.textContent = res.failed;
            kpiRate.textContent = res.pass_rate;
            rawOutput.textContent = res.output;

            if (res.success) {
                badgeVerdict.textContent = `VERIFIED · ${res.pass_rate} PASS RATE`;
                badgeVerdict.className = "status-badge-verified";
                statementEl.textContent = `The ${testType.toUpperCase()} test suite successfully satisfied all IEEE 829 Software Quality Assurance acceptance criteria with zero regressions or defect triggers.`;
            } else {
                badgeVerdict.textContent = `FAILED · REGRESSIONS DETECTED`;
                badgeVerdict.className = "status-badge-verified text-rose";
                statementEl.textContent = "Defects or assertion failures were detected during test execution. Please review the terminal log.";
            }

            // Populate table rows
            tbody.innerHTML = "";
            if (res.cases && res.cases.length > 0) {
                res.cases.forEach(c => {
                    const tr = document.createElement("tr");
                    const isWhite = c.name.includes("whitebox");
                    const typeLabel = isWhite ? "White-Box (Unit)" : "Black-Box (Integration)";
                    const isPassed = c.status === "PASSED";
                    const badgeClass = isPassed ? "badge-test-passed" : "badge-test-failed";

                    tr.innerHTML = `
                        <td class="mono"><b>${c.name}</b></td>
                        <td><span class="test-type-pill ${isWhite ? 'cyan' : 'purple'}">${typeLabel}</span></td>
                        <td><span class="${badgeClass}">${c.status}</span></td>
                    `;
                    tbody.appendChild(tr);
                });
            } else {
                tbody.innerHTML = `<tr><td colspan="3" style="text-align:center; color:#94a3b8;">No test cases identified in output.</td></tr>`;
            }

            // Reveal report card
            reportSection.classList.remove("hidden");
            if (window.lucide) {
                lucide.createIcons();
            }

            // Smooth scroll into report
            reportSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
            this.showToast("success", "Report Generated", `${res.total} test cases evaluated successfully.`);
        } catch (err) {
            this.showToast("error", "Test Runner Error", err.message);
        }
    }

    // =========================================================================
    // 3D Card Interactive Tilt Physics
    // =========================================================================
    init3DTilt() {
        const cardWrapper = document.getElementById("card-3d");
        const card = cardWrapper ? cardWrapper.querySelector(".virtual-card") : null;
        if (!cardWrapper || !card) return;

        cardWrapper.addEventListener("mousemove", (e) => {
            const rect = cardWrapper.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -12;
            const rotateY = ((x - centerX) / centerX) * 14;

            card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });

        cardWrapper.addEventListener("mouseleave", () => {
            card.style.transform = "rotateX(0deg) rotateY(0deg) translateY(0)";
        });
    }

    // =========================================================================
    // Toast Notification System
    // =========================================================================
    showToast(type, title, message) {
        const container = document.getElementById("toast-container");
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;

        const iconName = type === "success" ? "check-circle" : "alert-triangle";
        toast.innerHTML = `
            <div class="toast-icon"><i data-lucide="${iconName}"></i></div>
            <div class="toast-content">
                <h5>${title}</h5>
                <p>${message}</p>
            </div>
        `;

        container.appendChild(toast);
        if (window.lucide) {
            lucide.createIcons();
        }

        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateX(100%)";
            toast.style.transition = "all 0.3s ease";
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // =========================================================================
    // University Documentation Viewer
    // =========================================================================
    async loadDoc(type) {
        document.querySelectorAll(".doc-switcher-btns .btn-ghost").forEach(b => b.classList.remove("active"));
        const activeBtn = document.getElementById(`btn-doc-${type}`);
        if (activeBtn) activeBtn.classList.add("active");

        const titleEl = document.getElementById("doc-viewer-title");
        const bodyEl = document.getElementById("doc-content-body");

        titleEl.textContent = `Loading ${type}...`;
        bodyEl.textContent = "Fetching markdown document from server...";

        try {
            const data = await this.apiFetch(`/api/docs?type=${type}`);
            titleEl.textContent = `docs/${data.title}`;
            bodyEl.textContent = data.content;
        } catch (err) {
            titleEl.textContent = "Error loading document";
            bodyEl.textContent = err.message;
        }
    }
}

// Instantiate Global App
const app = new BankApp();
window.app = app;

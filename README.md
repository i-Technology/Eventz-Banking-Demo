# 🏦 Eventz Banking Demo

This project demonstrates a simplified distributed banking system using the Eventz methodology:  
**`y = F(Y, e)`** — where each function `F` processes a new event `e` and the archive `Y` to produce a new immutable result `y`.

---

## 🚀 What It Does

Simulates a basic banking system with:

- ✅ Customers, Accounts, Cards
- 💰 Deposits and Withdrawals
- 💳 Card Payments
- 🔒 Blocked Accounts and Cards
- 📊 Live Ledger GUI with user-specific views
- 📄 Stakeholder PDF reporting
- 📁 Immutable audit trail in `Y_archive.tsv`

---

## 🧾 Interactive Ledger GUI (`ledger_gui.py`)

- Users log in with their `customer_uuid`
- If no account exists, the system prompts to create one
- Transactions are filtered per user (based on `account_uuid`)
- GUI shows:

| Date | Payee | Amount | Balance |
|------|--------|--------|---------|

- Color-coded: 🟢 Green for credits, 🔴 Red for debits
- Add new transactions interactively
- Hit Enter or click ➕ to submit
- Logout button returns to login screen

```bash
python3 ledger_gui.py
```

---

## 📝 Reports and Exports

- `F_report_bank_summary.py`: summarizes all TransactionApproved and TransactionDeclined events
- Generates `Y_summary_report.md`
- `run.sh` converts it to a polished `Y_summary_report.pdf`

---

## 📂 Project Structure

```
F_deposit.py                # Deposit rule
F_withdrawal.py             # Withdrawal rule
F_card_payment.py           # Card payment logic
F_block_account.py          # Account blocking
F_block_card.py             # Card blocking
F_report_bank_summary.py    # Summary report logic
eventzAPI.py                # Core API: publish(), export_tsv(), etc.
main.py                     # Simulation runner
ledger_gui.py               # Stakeholder GUI with login/logout
Y_archive.tsv               # Immutable archive of all events
Y_summary_report.pdf        # Stakeholder-readable PDF (generated)
README.md
run.sh
```

---

## 📄 License

MIT License

---

## 🙋 Author

[Steve Jackson](https://www.linkedin.com/in/steve-jackson-b8675431/)  
📧 Steve.Jackson@IEEE.org  
Inventor of Eventz – a lean, event-driven architecture for digital transformation

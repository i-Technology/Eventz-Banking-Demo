import tkinter as tk
from tkinter import ttk, messagebox
import csv
import uuid
from datetime import datetime

TSV_PATH = "Y_archive.tsv"

def get_account_uuid(customer_uuid):
    try:
        with open(TSV_PATH, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if row.get("event_type") == "AccountOpened" and row.get("customer_uuid") == customer_uuid:
                    return row.get("account_uuid")
    except FileNotFoundError:
        pass
    return None

def open_account_for(customer_uuid):
    account_uuid = str(uuid.uuid4())
    event = {
        "uuid": str(uuid.uuid4()),
        "event_type": "AccountOpened",
        "customer_uuid": customer_uuid,
        "account_uuid": account_uuid,
        "balance": "0.00",
        "status": "open",
        "timestamp": datetime.now().isoformat()
    }

    # Ensure headers match or are written
    try:
        with open(TSV_PATH, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            header_fields = reader.fieldnames or []
    except FileNotFoundError:
        header_fields = list(event.keys())

    with open(TSV_PATH, "a") as f:
        writer = csv.DictWriter(f, fieldnames=header_fields, delimiter="\t", extrasaction="ignore")
        writer.writerow(event)

    print(f"✅ Opened new account {account_uuid} for customer {customer_uuid}")



def load_ledger_data(account_uuid):
    entries = []
    balance = 0.0
    try:
        with open(TSV_PATH, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if row.get("event_type") != "TransactionApproved":
                    continue
                if row.get("account_uuid") != account_uuid:
                    continue

                amount = float(row.get("amount", "0") or 0)
                payee = row.get("reason", "") or row.get("event_type", "")
                timestamp = row.get("timestamp", "")[:19]

                balance += amount
                signed_amount = f"{amount:+.2f}"
                entries.append((timestamp, payee, signed_amount, f"{balance:.2f}"))
    except FileNotFoundError:
        pass
    return entries

def append_transaction(payee, debit, credit, account_uuid):
    amount = 0.0
    if debit:
        amount = -abs(float(debit))
    elif credit:
        amount = abs(float(credit))
    else:
        return

    now = datetime.now().isoformat()
    new_entry = {
        "uuid": str(uuid.uuid4()),
        "event_type": "TransactionApproved",
        "account_uuid": account_uuid,
        "amount": f"{amount:.2f}",
        "reason": payee,
        "timestamp": now
    }

    try:
        with open(TSV_PATH, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            header_fields = reader.fieldnames or []
    except FileNotFoundError:
        header_fields = new_entry.keys()

    with open(TSV_PATH, "a") as f:
        writer = csv.DictWriter(f, fieldnames=header_fields, delimiter="\t", extrasaction='ignore')
        writer.writerow(new_entry)

def submit_transaction(payee_entry, debit_entry, credit_entry, tree, account_uuid):
    payee = payee_entry.get()
    debit = debit_entry.get()
    credit = credit_entry.get()
    append_transaction(payee, debit, credit, account_uuid)

    payee_entry.delete(0, tk.END)
    debit_entry.delete(0, tk.END)
    credit_entry.delete(0, tk.END)

    for row in tree.get_children():
        tree.delete(row)
    for row in load_ledger_data(account_uuid):
        amount = float(row[2])
        tag = "credit" if amount > 0 else "debit" if amount < 0 else ""
        tree.insert("", "end", values=row, tags=(tag,))

def display_ledger(customer_uuid):
    account_uuid = get_account_uuid(customer_uuid)
    if not account_uuid:
        print("No account found.")
        return

    root = tk.Tk()
    root.title(f"📘 Eventz Ledger – {customer_uuid}")

    cols = ("Date", "Payee", "Amount", "Balance")
    tree = ttk.Treeview(root, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True)

    for row in load_ledger_data(account_uuid):
        amount = float(row[2])
        tag = "credit" if amount > 0 else "debit" if amount < 0 else ""
        tree.insert("", "end", values=row, tags=(tag,))

    tree.tag_configure("credit", foreground="green")
    tree.tag_configure("debit", foreground="red")

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Payee").grid(row=0, column=0)
    payee_entry = tk.Entry(input_frame)
    payee_entry.grid(row=1, column=0)

    tk.Label(input_frame, text="Debit").grid(row=0, column=1)
    debit_entry = tk.Entry(input_frame)
    debit_entry.grid(row=1, column=1)

    tk.Label(input_frame, text="Credit").grid(row=0, column=2)
    credit_entry = tk.Entry(input_frame)
    credit_entry.grid(row=1, column=2)

    submit_btn = tk.Button(
        input_frame,
        text="➕ Add Transaction",
        command=lambda: submit_transaction(payee_entry, debit_entry, credit_entry, tree, account_uuid)
    )
    submit_btn.grid(row=1, column=3, padx=10)

    def bind_enter(widget):
        widget.bind("<Return>", lambda event: submit_btn.invoke())

    for entry in (payee_entry, debit_entry, credit_entry):
        bind_enter(entry)

    def logout():
        root.destroy()
        login_window()

    logout_btn = tk.Button(root, text="Logout", command=logout)
    logout_btn.pack(pady=10)

    root.mainloop()


def login_window():
    login = tk.Tk()
    login.title("Eventz Ledger – Sign In")

    tk.Label(login, text="Enter Customer UUID:").pack(padx=20, pady=10)
    customer_entry = tk.Entry(login)
    customer_entry.pack(padx=20, pady=5)

    def submit():
        customer_uuid = customer_entry.get().strip()
        if not customer_uuid:
            return

        account_uuid = get_account_uuid(customer_uuid)
        if account_uuid:
            login.destroy()
            display_ledger(customer_uuid)
        else:
            create_new = messagebox.askyesno("Account Not Found", f"No account found for '{customer_uuid}'.\\nCreate a new account?")
            if create_new:
                open_account_for(customer_uuid)
                login.destroy()
                display_ledger(customer_uuid)

    customer_entry.bind("<Return>", lambda event: submit())
    tk.Button(login, text="Login", command=submit).pack(pady=10)
    login.mainloop()

if __name__ == "__main__":
    login_window()

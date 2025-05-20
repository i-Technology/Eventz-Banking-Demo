import sys
import os

# Ensure current directory is in import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from eventzAPI import publish
from F_deposit import F_deposit
from F_withdrawal import F_withdrawal
from F_card_payment import F_card_payment
from F_block_account import F_block_account
from F_block_card import F_block_card

# --- SETUP DATA ---

# 1. Open an account
publish("AccountOpened", {
    "customer_uuid": "cust001",
    "account_uuid": "acct001",
    "balance": 200.0,
    "status": "open"
})

# 2. Issue a card for the account
publish("CardIssued", {
    "account_uuid": "acct001",
    "card_uuid": "card001",
    "status": "active"
})

# --- SCENARIOS ---

# 3. Deposit $100
print("\n--- Deposit $100 ---")
F_deposit({
    "account_uuid": "acct001",
    "amount": 100.0
})

# 4. Withdraw $50 (should succeed)
print("\n--- Withdraw $50 ---")
F_withdrawal({
    "account_uuid": "acct001",
    "amount": 50.0
})

# 5. Card payment $300 (should fail - insufficient funds)
print("\n--- Card Payment $300 (should fail) ---")
F_card_payment({
    "card_uuid": "card001",
    "amount": 300.0,
    "merchant": "SuperMart"
})

# 6. Block the account
print("\n--- Blocking Account ---")
F_block_account({
    "account_uuid": "acct001"
})

# 7. Attempt withdrawal after block (should fail)
print("\n--- Withdraw $10 after block (should fail) ---")
F_withdrawal({
    "account_uuid": "acct001",
    "amount": 10.0
})

# 8. Block the card
print("\n--- Blocking Card ---")
F_block_card({
    "card_uuid": "card001"
})

# 9. Attempt card payment after card block (should fail)
print("\n--- Card Payment $10 after card block (should fail) ---")
F_card_payment({
    "card_uuid": "card001",
    "amount": 10.0,
    "merchant": "CoffeeShop"
})

from eventzAPI import export_tsv

print("\n--- Exporting immutable archive to Y_archive.tsv ---")
export_tsv()

from eventzAPI import export_markdown
export_markdown()

from F_report_bank_summary import F_report_bank_summary
from eventzAPI import export_tsv, export_markdown

# Export archive
export_tsv()
export_markdown()

# Generate custom business report
F_report_bank_summary()

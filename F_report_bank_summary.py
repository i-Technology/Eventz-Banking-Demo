import csv
from datetime import datetime

def F_report_bank_summary(tsv_path="Y_archive.tsv", md_path="Y_summary_report.md"):
    with open(tsv_path, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        records = list(reader)

    # Filter: Only relevant event types
    filtered = [r for r in records if r["event_type"] in ("TransactionApproved", "TransactionDeclined")]

    # Define report fields
    fields = ["event_type", "account_uuid", "amount", "reason", "timestamp"]

    # Start Markdown report
    with open(md_path, "w") as f:
        f.write("# Banking Transaction Summary Report\n")
        f.write(f"_Generated: {datetime.now().isoformat()}_\n\n")

        # Table header
        f.write("| " + " | ".join(fields) + " |\n")
        f.write("|" + "|".join(["---"] * len(fields)) + "|\n")

        # Table rows
        for row in filtered:
            f.write("| " + " | ".join(row.get(field, "") for field in fields) + " |\n")

    print(f"Markdown summary written to {md_path}")

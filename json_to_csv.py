import os
import csv
import json
from datetime import date

# === File paths ===
json_file = "C:\\Users\\Admin\\PycharmProjects\\loanrates (2)\\loanrates\\output\\bankrate.json"
csv_file = "C:\\Users\\Admin\\PycharmProjects\\loanrates (2)\\loanrates\\output\\bankrate.csv"

# === Required Fields ===
FIELDS = ["loan_product", "interest_rate", "apr", "loan_term_years", "lender_name", "updated_date", "mortgageType"]

def main():
    if not os.path.exists(json_file):
        print("JSON file missing; nothing to append.")
        return

    # === Load JSON Records ===
    with open(json_file, "r", encoding="utf-8") as f:
        if os.path.getsize(json_file) > 0:
            try:
                records = json.load(f)
                if isinstance(records, dict):
                    records = [records]
            except json.JSONDecodeError:
                print("Invalid JSON format.")
                return
        else:
            records = []

    if not records:
        print("JSON file is empty.")
        return

    # === Filter Valid Today's Records ===
    today = date.today().isoformat()
    valid_records = [
        r for r in records
        if r.get("updated_date") == today and all(k in r and r[k] for k in FIELDS)
    ]

    if not valid_records:
        print("No valid records for today to append.")
        return

    # === Get Existing CSV Keys ===
    existing_keys = set()
    if os.path.exists(csv_file):
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_keys.add((row["loan_product"], row["updated_date"]))

    # === Filter New Records Not in CSV ===
    new_records = []
    for r in valid_records:
        key = (r["loan_product"], r["updated_date"])
        if key not in existing_keys:
            new_records.append(r)

    if not new_records:
        print("No new (non-duplicate) records to append.")
        return

    # === Append to CSV ===
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    write_header = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        cleaned = [{k: r[k] for k in FIELDS} for r in new_records]
        writer.writerows(cleaned)

    print(f"Appended {len(new_records)} new record(s) to CSV.")
    print("JSON file was NOT modified (remains as is).")

if __name__ == "__main__":
    main()

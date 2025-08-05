import json
import os
import pandas as pd

# === File Paths ===
json_file = "C:\\Users\\Admin\\PycharmProjects\\loanrates (2)\\loanrates\\output\\bankrate.json"
xlsx_file = "C:\\Users\\Admin\\PycharmProjects\\loanrates (2)\\loanrates\\output\\bankrate.xlsx"

# === Load JSON Data ===
if not os.path.exists(json_file):
    print(f"[ERROR] JSON file not found: {json_file}")
    exit()

with open(json_file, "r", encoding="utf-8") as f:
    try:
        data = json.load(f)
        if isinstance(data, dict):
            data = [data]
    except json.JSONDecodeError as e:
        print("[ERROR] Failed to parse JSON:", e)
        exit()

if not data:
    print("[INFO] JSON file is empty.")
    exit()

# === Convert to DataFrame and Remove Duplicates ===
df = pd.DataFrame(data)

# Drop duplicates based on 'loan_product' and 'updated_date'
df_clean = df.drop_duplicates(subset=["loan_product", "updated_date"])

# === Write to Excel using xlsxwriter ===
df_clean.to_excel(xlsx_file, index=False, engine="xlsxwriter")

print(f"[OK] Wrote {len(df_clean)} unique record(s) to Excel: {xlsx_file}")

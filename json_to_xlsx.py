import json
import os
import pandas as pd

# === File Paths ===
json_file = r"C:\Users\Admin\PycharmProjects\loanrates (2)\loanrates\output\bankrate.json"
xlsx_file = r"C:\Users\Admin\PycharmProjects\loanrates (2)\loanrates\output\bankrate.xlsx"

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

# Convert new JSON data to DataFrame
df_new = pd.DataFrame(data)

# === Load Existing Excel Data if available ===
if os.path.exists(xlsx_file) and os.path.getsize(xlsx_file) > 0:
    try:
        df_existing = pd.read_excel(xlsx_file, engine="openpyxl")
    except Exception:
        df_existing = pd.DataFrame()
else:
    df_existing = pd.DataFrame()

# === Merge (Override if same loan_product + updated_date) ===
if not df_existing.empty:
    # Remove old rows with same key from existing
    merged_df = df_existing[
        ~df_existing.set_index(["loan_product", "updated_date"]).index.isin(
            df_new.set_index(["loan_product", "updated_date"]).index
        )
    ]
    # Append new rows
    final_df = pd.concat([merged_df, df_new], ignore_index=True)
else:
    final_df = df_new

# Drop duplicates again for safety
final_df = final_df.drop_duplicates(subset=["loan_product", "updated_date"], keep="last")

# === Save Back to Excel ===
final_df.to_excel(xlsx_file, index=False, engine="xlsxwriter")

print(f"[OK] Updated Excel with {len(df_new)} new/updated record(s).")
print(f"[TOTAL] Excel now contains {len(final_df)} record(s).")

import subprocess
import logging
import os
from datetime import datetime

# === Log Setup ===
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Create logs/ directory if not present
log_file = os.path.join(log_dir, "scrapy_run.log")

# Create empty log file if it doesn't exist
if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        f.write('')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(message):
    print(message)
    logging.info(message)

def run_spider():
    log_and_print("Running Scrapy spider: bankrate_loans")
    result = subprocess.run(
        ["scrapy", "crawl", "bankrate_loans"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    if result.returncode == 0:
        log_and_print("Scrapy spider completed successfully.")
    else:
        logging.error(" Scrapy spider failed.")
        logging.error(result.stderr)
        print("Error running spider. Check log for details.")
        return False
    return True

def run_json_to_csv():
    log_and_print("Converting JSON to CSV...")
    result = subprocess.run(
        ["python", "json_to_csv.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"  #  Fix
    )
    if result.returncode == 0:
        log_and_print("JSON to CSV transformation completed.")
    else:
        logging.error("JSON to CSV conversion failed.")
        logging.error(result.stderr)
        print("Error during JSON to CSV conversion. Check log for details.")
        return False
    return True

if __name__ == "__main__":
    log_and_print("\n=== Starting Scrapy + CSV Job ===")

    if run_spider():
        run_json_to_csv()

    log_and_print("Job completed.")

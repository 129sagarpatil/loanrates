import subprocess
import logging
import os
from datetime import datetime
import sys

# === Setup Directories ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "scrapy_run.log")

# === Configure Logging ===
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Logging Helper ===
def log_and_print(message):
    print(message)
    logging.info(message)

# === Error Logging Helper ===
def log_and_print_error(message, stderr=None):
    print(message)
    logging.error(message)
    if stderr:
        print(stderr.strip())
        logging.error(stderr.strip())

# === Script Runner ===
def run_script(command, name):
    log_and_print(f" Running: {name}")
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=BASE_DIR,
            encoding="utf-8"
        )

        if result.returncode == 0:
            log_and_print(f" {name} completed successfully.")
            return True
        else:
            log_and_print_error(f" {name} failed.", result.stderr)
            return False

    except Exception as e:
        log_and_print_error(f" Exception while running {name}: {str(e)}")
        return False

# === Task Runners ===
def run_spider():
    return run_script(["scrapy", "crawl", "bankrate_loans"], "Scrapy Spider")

def run_json_to_csv():
    return run_script([sys.executable, "json_to_csv.py"], "JSON to CSV")

def run_json_to_xlsx():
    return run_script([sys.executable, "json_to_xlsx.py"], "JSON to XLSX")


# === Main Execution ===
if __name__ == "__main__":
    log_and_print(" Job started at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log_and_print("===  Starting Full Scrapy → CSV → XLSX Job ===")

    if run_spider():
        success_csv = run_json_to_csv()
        success_excel = run_json_to_xlsx()

        if success_csv and success_excel:
            log_and_print(" All steps completed successfully.")
        else:
            log_and_print("️ One or more transformation steps failed.")
    else:
        log_and_print(" Spider failed. Skipping transformation steps.")

    log_and_print(" Job ended at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log_and_print("=" * 50)

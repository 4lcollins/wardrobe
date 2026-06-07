import argparse
import os
import sys
from pathlib import Path
import importlib.util

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Run a Wardrobe automation script."
)
parser.add_argument(
    "automation",
    help="Name of the script to execute from the automations directory."
)
parser.add_argument(
    "-e",
    "--email",
    required=True,
    help="Recipient email address."
)

args = parser.parse_args()

AUTOMATION_NAME = args.automation
EMAIL = args.email

# Determine repository location
EXPECTED_REPO_DIR = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "Wardrobe"

if "__file__" in globals():
    SCRIPT_DIR = Path(__file__).resolve().parent
    REPO_DIR = SCRIPT_DIR.parent
else:
    REPO_DIR = EXPECTED_REPO_DIR

if (
    not (REPO_DIR / "src" / "core").exists()
    and (EXPECTED_REPO_DIR / "src" / "core").exists()
):
    REPO_DIR = EXPECTED_REPO_DIR

os.chdir(REPO_DIR)

# Configure Python import paths
SRC_DIR = REPO_DIR / "src"

if str(REPO_DIR) not in sys.path:
    sys.path.insert(0, str(REPO_DIR))

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Load and run the automation module
automation_script = REPO_DIR / "src" / "automations" / f"{AUTOMATION_NAME}.py"
if automation_script.exists():
    spec = importlib.util.spec_from_file_location(AUTOMATION_NAME, automation_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.run(email=EMAIL)
else:
    print(f"Error: {automation_script} not found.")
    sys.exit(1)
import os
import sys
from pathlib import Path

# Get action name from command line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <action_name>")
    sys.exit(1)

# Original path detection logic restored
EXPECTED_REPO_DIR = Path("/Users/landon/Desktop/Wardrobe")

if "__file__" in globals():
    SCRIPT_DIR = Path(__file__).resolve().parent
    REPO_DIR = SCRIPT_DIR.parent
else:
    REPO_DIR = EXPECTED_REPO_DIR

if not (REPO_DIR / "src" / "core").exists() and (EXPECTED_REPO_DIR / "src" / "core").exists():
    REPO_DIR = EXPECTED_REPO_DIR

os.chdir(REPO_DIR)

# Original sys.path logic restored
SRC_DIR = REPO_DIR / "src"
if str(REPO_DIR) not in sys.path:
    sys.path.insert(0, str(REPO_DIR))
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Build path to the target script in the scripts folder
action_script = REPO_DIR / "scripts" / f"{sys.argv[1]}.py"

# Execute the script
if action_script.exists():
    with open(action_script, "r") as f:
        exec(compile(f.read(), action_script, "exec"), globals())
else:
    print(f"Error: {action_script} not found.")
    sys.exit(1)
from pka.persistance import safe_write
from pathlib import Path
import json

TEST_FILE = Path("data/test_notes.json")

# Step 1: create a known-good starting file
with open(TEST_FILE, "w") as f:
    json.dump({"status": "original safe data 2"}, f)

print("Before crash test:", TEST_FILE.read_text())

# Step 2: simulate a crash DURING the write
try:
    with safe_write(TEST_FILE) as f:
        f.write('{"status": "half-writ')  # deliberately incomplete JSON
        raise RuntimeError("Simulated crash mid-write!")
except RuntimeError as e:
    print("Caught simulated crash:", e)

# Step 3: check the file survived untouched
print("After crash test:", TEST_FILE.read_text())
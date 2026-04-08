import json
import os

# Get directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

training_pairs_path = os.path.join(current_dir, "training_pairs.json")
new_batch_path = os.path.join(current_dir, "new_batch.json")

# Load existing pairs
try:
    with open(training_pairs_path, "r") as f:
        existing = json.load(f)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    print("training_pairs.json is empty or missing. Starting fresh.")
    existing = []

# Load new batch from Gemini
with open(new_batch_path, "r") as f:
    new_batch = json.load(f)

# Merge
combined = existing + new_batch
print(f"Total pairs now: {len(combined)}")

# Save
with open(training_pairs_path, "w") as f:
    json.dump(combined, f, indent=2)
import sqlite3
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer

# ── Paths ────────────────────────────────────────────────────────
base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
db_path = os.path.join(data_dir, 'training_data.db')
vectors_path = os.path.join(data_dir, 'db_vectors.npy')
ids_path = os.path.join(data_dir, 'db_ids.npy')
metadata_path = os.path.join(data_dir, 'db_metadata.json')

# ── Load Pre-trained Model ───────────────────────────────────────
print("Downloading/Loading Sentence Transformer...")
# This downloads a highly accurate, lightweight model automatically
model = SentenceTransformer('all-MiniLM-L6-v2') 
print("Model loaded ✓")

# ── Load database ────────────────────────────────────────────────
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT id, project_name, project_abstract FROM projects")
rows = cursor.fetchall()
conn.close()

print(f"Loaded {len(rows)} projects")

# ── Embed every project ──────────────────────────────────────────
embeddings = {}
metadata   = {}

for id, name, abstract in rows:
    # Combine name and abstract into one clean string
    text = f"{name}. {abstract if abstract else ''}"
    
    # The transformer handles the tokenization, padding, and embedding instantly
    vector = model.encode(text) 
    
    embeddings[id] = vector
    metadata[str(id)] = name
    print(f"  [{id}] {name}")

# ── Save ─────────────────────────────────────────────────────────
ids     = list(embeddings.keys())
vectors = np.array([embeddings[i] for i in ids])

np.save(vectors_path, vectors)
np.save(ids_path, np.array(ids))

with open(metadata_path, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"\nVector shape: {vectors.shape}")
print("Database Re-embedded successfully ✓")
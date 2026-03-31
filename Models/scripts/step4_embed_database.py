import sqlite3
import json
import torch
import numpy as np
import sys
import os

# Add Models/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.tokenizer import tokenize
from model.encoder import ProjectEncoder

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
vocab_path = os.path.join(base_dir, 'vocab.json')
db_path = os.path.join(data_dir, 'training_data.db')

with open(vocab_path, "r") as f:
    vocab = json.load(f)

vocab_size = len(vocab)
model = ProjectEncoder(vocab_size=vocab_size)
model.eval()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT id, project_name, project_abstract FROM projects")
rows = cursor.fetchall()
conn.close()

print(f"Loaded {len(rows)} projects from {db_path}")

embeddings = {}
metadata = {}

with torch.no_grad():
    for id, name, abstract in rows:
        tokens = tokenize(name, abstract)
        tensor = torch.tensor([tokens], dtype=torch.long)
        vector = model(tensor).squeeze(0).numpy()
        
        embeddings[id] = vector
        metadata[id] = name
        print(f"  Embedded [{id}] {name}")

ids = list(embeddings.keys())
vectors = np.array([embeddings[i] for i in ids])

vec_path = os.path.join(data_dir, 'db_vectors.npy')
ids_path = os.path.join(data_dir, 'db_ids.npy')
meta_path = os.path.join(data_dir, 'db_metadata.json')

np.save(vec_path, vectors)
np.save(ids_path, np.array(ids))

with open(meta_path, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"\nSaved {len(ids)} vectors to {vec_path} ✓")
print(f"Saved {ids_path} ✓")
print(f"Saved {meta_path} ✓")
print(f"Vector shape: {vectors.shape}")

import sqlite3
import torch
import torch.nn as nn
import numpy as np
import json
import re

# ── Load vocab ───────────────────────────────────────────────────
import os
base_dir = os.path.dirname(os.path.dirname(__file__))
vocab_path = os.path.join(base_dir, 'vocab.json')
model_path = os.path.join(base_dir, 'model', 'model.pth')
data_dir = os.path.join(base_dir, 'data')
db_path = os.path.join(data_dir, 'training_data.db')
vectors_path = os.path.join(data_dir, 'db_vectors.npy')
ids_path = os.path.join(data_dir, 'db_ids.npy')
metadata_path = os.path.join(data_dir, 'db_metadata.json')

with open(vocab_path, "r") as f:
    vocab = json.load(f)

def clean_text(text):
    if text is None: return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()

def tokenize(name, abstract="", max_len=64):
    tokens = clean_text(name) + clean_text(abstract)
    indices = [vocab.get(w, 1) for w in tokens]
    if len(indices) < max_len:
        indices += [0] * (max_len - len(indices))
    else:
        indices = indices[:max_len]
    return indices

# ── Load TRAINED model ───────────────────────────────────────────
class ProjectEncoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=128, output_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm      = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc        = nn.Linear(hidden_dim * 2, output_dim)
        self.relu      = nn.ReLU()

    def forward(self, x):
        embedded    = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        pooled      = lstm_out.mean(dim=1)
        return self.relu(self.fc(pooled))

checkpoint = torch.load(model_path)
model = ProjectEncoder(vocab_size=checkpoint["vocab_size"])
model.load_state_dict(checkpoint["model_state"])
model.eval()

print("Trained model loaded ✓")

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

with torch.no_grad():
    for id, name, abstract in rows:
        tokens = tokenize(name, abstract)
        tensor = torch.tensor([tokens], dtype=torch.long)
        vector = model(tensor).squeeze(0).numpy()
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
print("Saved db_vectors.npy ✓")
print("Saved db_ids.npy ✓")
print("Saved db_metadata.json ✓")
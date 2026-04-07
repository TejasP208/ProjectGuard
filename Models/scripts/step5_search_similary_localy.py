import torch
import numpy as np
import json
import re
import os
import torch.nn as nn

base_dir = os.path.dirname(os.path.dirname(__file__))
vocab_path = os.path.join(base_dir, 'vocab.json')
data_dir = os.path.join(base_dir, 'data')
metadata_path = os.path.join(data_dir, 'db_metadata.json')
vectors_path = os.path.join(data_dir, 'db_vectors.npy')
ids_path = os.path.join(data_dir, 'db_ids.npy')
model_path = os.path.join(base_dir, 'model', 'model.pth')

# ── Load Everything ──────────────────────────────────────────────
with open(vocab_path, "r") as f:
    vocab = json.load(f)

with open(metadata_path, "r") as f:
    metadata = json.load(f)

db_vectors = np.load(vectors_path)   # (N, 128)
db_ids     = np.load(ids_path)       # (N,)

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

print("Everything loaded ✓")

# ── Tokenizer ────────────────────────────────────────────────────
def clean_text(text):
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()

def tokenize(name, abstract="", max_len=64):
    tokens = clean_text(name) + clean_text(abstract)
    indices = [vocab.get(word, 1) for word in tokens]
    if len(indices) < max_len:
        indices += [0] * (max_len - len(indices))
    else:
        indices = indices[:max_len]
    return indices

# ── Cosine Similarity ────────────────────────────────────────────
def cosine_similarity(vec_a, vec_b):
    dot    = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

# ── Search Function ──────────────────────────────────────────────
def search(query_name, query_abstract="", threshold=0.75, top_k=3):
    # Embed the query
    tokens = tokenize(query_name, query_abstract)
    tensor = torch.tensor([tokens], dtype=torch.long)
    
    with torch.no_grad():
        query_vec = model(tensor).squeeze(0).numpy()   # (128,)

    # Compare against every DB vector
    results = []
    for i, db_vec in enumerate(db_vectors):
        score = cosine_similarity(query_vec, db_vec)
        proj_id   = str(db_ids[i])
        proj_name = metadata.get(proj_id, "Unknown")
        results.append((score, proj_id, proj_name))

    # Sort by score high → low
    results.sort(reverse=True)

    # ── Output ───────────────────────────────────────────────────
    best_score, best_id, best_name = results[0]

    print(f"\nQuery: '{query_name}'")
    print(f"─────────────────────────────────")

    if best_score >= threshold:
        print(f"✅ EXISTS — similar project found!")
        print(f"   Match : {best_name}")
        print(f"   Score : {best_score:.4f}")
    else:
        print(f"🆕 NEW — no similar project found")
        print(f"   Closest: {best_name}")
        print(f"   Score  : {best_score:.4f}")

    print(f"\nTop {top_k} matches:")
    for score, pid, pname in results[:top_k]:
        bar = "█" * int(score * 20)
        print(f"  [{score:.4f}] {bar} {pname}")

    return best_score >= threshold

# ── Try it! ──────────────────────────────────────────────────────
# Test these one by one
search("blockchain voting", "decentralized secure election system using blockchain")
search("online exam portal", "web platform for conducting online tests with auto grading")# should be NEW  # something totally new
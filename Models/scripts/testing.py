import torch
import torch.nn as nn
import json
import re

import os

base_dir = os.path.dirname(os.path.dirname(__file__))
vocab_path = os.path.join(base_dir, "vocab.json")
pairs_path = os.path.join(base_dir, "data", "training_pairs.json")
model_path = os.path.join(base_dir, "model", "model.pth")

# Load everything same as before
with open(vocab_path, "r") as f:
    vocab = json.load(f)

with open(pairs_path, "r") as f:
    pairs = json.load(f)

def clean_text(text):
    if text is None: return ""
    text = text.lower()
    import re
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

# Load trained model
checkpoint = torch.load(model_path)
model = ProjectEncoder(vocab_size=checkpoint["vocab_size"])
model.load_state_dict(checkpoint["model_state"])
model.eval()

# ── Test 3 positive pairs (should be HIGH similarity) ────────────
print("POSITIVE PAIRS (similar projects — expect score > 0.7):")
print("─" * 60)
positives = [p for p in pairs if p["label"] == 1][:3]
for p in positives:
    t_a = torch.tensor([tokenize(p["name_a"], p["abstract_a"])], dtype=torch.long)
    t_b = torch.tensor([tokenize(p["name_b"], p["abstract_b"])], dtype=torch.long)
    with torch.no_grad():
        v_a = model(t_a)
        v_b = model(t_b)
        score = nn.functional.cosine_similarity(v_a, v_b).item()
    print(f"  {score:.4f} | {p['name_a'][:35]} vs {p['name_b'][:35]}")

# ── Test 3 negative pairs (should be LOW similarity) ─────────────
print("\nNEGATIVE PAIRS (different projects — expect score < 0.3):")
print("─" * 60)
negatives = [p for p in pairs if p["label"] == 0][:3]
for p in negatives:
    t_a = torch.tensor([tokenize(p["name_a"], p["abstract_a"])], dtype=torch.long)
    t_b = torch.tensor([tokenize(p["name_b"], p["abstract_b"])], dtype=torch.long)
    with torch.no_grad():
        v_a = model(t_a)
        v_b = model(t_b)
        score = nn.functional.cosine_similarity(v_a, v_b).item()
    print(f"  {score:.4f} | {p['name_a'][:35]} vs {p['name_b'][:35]}")
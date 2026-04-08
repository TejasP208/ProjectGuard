import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import json
import re

# ── Load Vocab ───────────────────────────────────────────────────
import os
base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
model_dir = os.path.join(base_dir, 'model')
vocab_path = os.path.join(base_dir, 'vocab.json')
pairs_path = os.path.join(data_dir, 'training_pairs.json')
model_path = os.path.join(model_dir, 'model.pth')

with open(vocab_path, "r") as f:
    vocab = json.load(f)

with open(pairs_path, "r") as f:
    pairs = json.load(f)

print(f"Vocab size: {len(vocab)}")
print(f"Training pairs: {len(pairs)}")

# ── Tokenizer ────────────────────────────────────────────────────
def clean_text(text):
    if text is None:
        return ""
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

# ── Dataset ──────────────────────────────────────────────────────
class ProjectPairDataset(Dataset):
    def __init__(self, pairs):
        self.pairs = pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        p = self.pairs[idx]
        tokens_a = tokenize(p["name_a"], p["abstract_a"])
        tokens_b = tokenize(p["name_b"], p["abstract_b"])
        label    = float(p["label"])
        return (
            torch.tensor(tokens_a, dtype=torch.long),
            torch.tensor(tokens_b, dtype=torch.long),
            torch.tensor(label,    dtype=torch.float)
        )

dataset    = ProjectPairDataset(pairs)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# ── Model ────────────────────────────────────────────────────────
class ProjectEncoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=128, output_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm      = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc        = nn.Linear(hidden_dim * 2, output_dim)
        self.relu      = nn.ReLU()

    def forward(self, x):
        embedded  = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        pooled    = lstm_out.max(dim=1)[0]
        return self.relu(self.fc(pooled))

model     = ProjectEncoder(vocab_size=len(vocab))
optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)

# ── Contrastive Loss ─────────────────────────────────────────────
class ContrastiveLoss(nn.Module):
    def __init__(self, margin=1.0):
        super().__init__()
        self.margin = margin

    def forward(self, vec_a, vec_b, label):
        cos_sim  = nn.functional.cosine_similarity(vec_a, vec_b)
        distance = 1 - cos_sim
        loss = (
            label * distance ** 2 +
            (1 - label) * torch.clamp(self.margin - distance, min=0) ** 2
        )
        return loss.mean()

criterion = ContrastiveLoss(margin=1.0)


# ── Training Loop ────────────────────────────────────────────────
EPOCHS = 50

print("\nStarting training...")
print("─" * 40)

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for batch_a, batch_b, labels in dataloader:
        optimizer.zero_grad()
        vec_a = model(batch_a)
        vec_b = model(batch_b)
        loss  = criterion(vec_a, vec_b, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader)

    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1:3d}/{EPOCHS}  |  Loss: {avg_loss:.4f}")

print("─" * 40)
print("Training complete ✓")

# ── Save Model ───────────────────────────────────────────────────
import os
os.makedirs(model_dir, exist_ok=True)
torch.save({
    "model_state": model.state_dict(),
    "vocab_size":  len(vocab),
    "embed_dim":   64,
    "hidden_dim":  128,
    "output_dim":  128,
}, model_path)

print(f"Saved {model_path} ✓")
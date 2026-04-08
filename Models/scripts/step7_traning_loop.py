import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import json
import re
import os

# ── Load Vocab ───────────────────────────────────────────────────
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
print(f"Total training pairs: {len(pairs)}")

# ── Tokenizer ────────────────────────────────────────────────────
def clean_text(text):
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()

# Increased max_len to 128 to capture more of the abstract
def tokenize(name, abstract="", max_len=128):
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
        tokens_a = tokenize(p["name_a"], p.get("abstract_a", ""))
        tokens_b = tokenize(p["name_b"], p.get("abstract_b", ""))
        label    = float(p["label"])
        return (
            torch.tensor(tokens_a, dtype=torch.long),
            torch.tensor(tokens_b, dtype=torch.long),
            torch.tensor(label,    dtype=torch.float)
        )

dataset = ProjectPairDataset(pairs)

# Train/Validation Split (80/20)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

# Set seed for reproducibility
generator = torch.Generator().manual_seed(42)
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size], generator=generator)

print(f"Training on {len(train_dataset)} pairs | Validating on {len(val_dataset)} pairs")

# Increased batch size to 32 for efficiency and more stable contrastive gradients
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)


# ── Model ────────────────────────────────────────────────────────
class ProjectEncoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=128, output_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm      = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        # Added Dropout layer to prevent memorization
        self.dropout   = nn.Dropout(0.3)
        self.fc        = nn.Linear(hidden_dim * 2, output_dim)
        self.relu      = nn.ReLU()

    def forward(self, x):
        embedded    = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        pooled      = lstm_out.mean(dim=1)
        pooled      = self.dropout(pooled) # Apply dropout before final dense layer
        output      = self.relu(self.fc(pooled))
        return nn.functional.normalize(output, p=2, dim=1)

model     = ProjectEncoder(vocab_size=len(vocab))
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)

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
EPOCHS = 40
PATIENCE = 5  # Stop if validation loss doesn't improve for 5 epochs

print("\nStarting training...")
print("─" * 60)

best_val_loss = float('inf')
epochs_no_improve = 0
os.makedirs(model_dir, exist_ok=True)

for epoch in range(EPOCHS):
    # Training phase
    model.train()
    total_train_loss = 0

    for batch_a, batch_b, labels in train_loader:
        optimizer.zero_grad()
        vec_a = model(batch_a)
        vec_b = model(batch_b)
        loss  = criterion(vec_a, vec_b, labels)
        loss.backward()
        optimizer.step()
        total_train_loss += loss.item()

    avg_train_loss = total_train_loss / len(train_loader)

    # Validation phase
    model.eval()
    total_val_loss = 0
    with torch.no_grad():
        for batch_a, batch_b, labels in val_loader:
            vec_a = model(batch_a)
            vec_b = model(batch_b)
            loss  = criterion(vec_a, vec_b, labels)
            total_val_loss += loss.item()
            
    avg_val_loss = total_val_loss / len(val_loader)
    scheduler.step(avg_val_loss)          

    print(f"Epoch {epoch+1:3d}/{EPOCHS}  |  Train Loss: {avg_train_loss:.4f}  |  Val Loss: {avg_val_loss:.4f}")

    # Early stopping and model checkpointing
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        epochs_no_improve = 0
        # Save the best model
        torch.save({
            "model_state": model.state_dict(),
            "vocab_size":  len(vocab),
            "embed_dim":   64,
            "hidden_dim":  128,
            "output_dim":  128,
        }, model_path)
    else:
        epochs_no_improve += 1
        if epochs_no_improve >= PATIENCE:
            print(f"\nEarly stopping triggered! Model stopped improving.")
            break

print("─" * 60)
print(f"Training complete ✓")
print(f"Best Validation Loss recorded: {best_val_loss:.4f}")
print(f"Best model saved to: {model_path}")
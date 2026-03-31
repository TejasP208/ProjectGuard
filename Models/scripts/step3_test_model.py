import sys
import os
import torch
import json

# Add Models/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.encoder import ProjectEncoder

base_dir = os.path.dirname(os.path.dirname(__file__))
vocab_path = os.path.join(base_dir, 'vocab.json')

with open(vocab_path, "r") as f:
    vocab = json.load(f)

vocab_size = len(vocab)
model = ProjectEncoder(vocab_size=vocab_size)
print("Model built ✓")
print(f"Total parameters: {sum(p.numel() for p in model.parameters())}")

dummy_input = torch.randint(0, vocab_size, (2, 64))
output = model(dummy_input)

print(f"Input shape:  {dummy_input.shape}")
print(f"Output shape: {output.shape}") 

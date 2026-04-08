import json
import re
from collections import Counter
import os
import sys

# Add Models/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.tokenizer import clean_text

base_dir = os.path.dirname(os.path.dirname(__file__))
pairs_path = os.path.join(base_dir, 'data', 'training_pairs.json')
vocab_path = os.path.join(base_dir, 'vocab.json')

with open(pairs_path, "r", encoding="utf-8") as f:
    pairs = json.load(f)

print(f"Loaded {len(pairs)} pairs from training_pairs.json")

all_tokens = []

for p in pairs:
    tokens_a = clean_text(p.get("name_a", "")) + clean_text(p.get("abstract_a", ""))
    tokens_b = clean_text(p.get("name_b", "")) + clean_text(p.get("abstract_b", ""))
    all_tokens.extend(tokens_a)
    all_tokens.extend(tokens_b)

word_counts = Counter(all_tokens)
print(f"Total unique words found: {len(word_counts)}")

vocab = {"<PAD>": 0, "<UNK>": 1}

for word, count in word_counts.most_common():
    vocab[word] = len(vocab)

print(f"Vocabulary size: {len(vocab)}")

with open(vocab_path, "w") as f:
    json.dump(vocab, f, indent=2)

print(f"Saved {vocab_path} ✓")

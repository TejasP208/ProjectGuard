import torch
import numpy as np
import json
import sys
import os

# Add Models/ to sys.path so we can import utils and model
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils.tokenizer import tokenize
from model.encoder import ProjectEncoder

base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, 'data')

vocab_path = os.path.join(base_dir, "vocab.json")
meta_path = os.path.join(data_dir, "db_metadata.json")
vec_path = os.path.join(data_dir, "db_vectors.npy")
ids_path = os.path.join(data_dir, "db_ids.npy")

with open(vocab_path, "r") as f:
    vocab = json.load(f)

with open(meta_path, "r") as f:
    metadata = json.load(f)

db_vectors = np.load(vec_path)
db_ids = np.load(ids_path)

model = ProjectEncoder(vocab_size=len(vocab))
model.eval()

print("Everything loaded ✓")

def cosine_similarity(vec_a, vec_b):
    dot = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def search(query_name, query_abstract="", threshold=0.85, top_k=3):
    tokens = tokenize(query_name, query_abstract)
    tensor = torch.tensor([tokens], dtype=torch.long)
    
    with torch.no_grad():
        query_vec = model(tensor).squeeze(0).numpy()

    results = []
    for i, db_vec in enumerate(db_vectors):
        score = cosine_similarity(query_vec, db_vec)
        proj_id = str(db_ids[i])
        proj_name = metadata.get(proj_id, "Unknown")
        results.append((score, proj_id, proj_name))

    results.sort(reverse=True)
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
        bar = "█" * int(max(0, score) * 20)
        print(f"  [{score:.4f}] {bar} {pname}")

    return best_score >= threshold

if __name__ == "__main__":
    search("AI based crop disease detection")
    search("online examination system for students")
    search("blockchain based voting system")
    search("recipe recommendation app")

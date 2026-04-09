import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer, util

# --- Path Configuration ---
# Since this file is in the root of 'Models', we look directly into the 'data' folder
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

metadata_path = os.path.join(data_dir, 'db_metadata.json')
vectors_path  = os.path.join(data_dir, 'db_vectors.npy')
ids_path      = os.path.join(data_dir, 'db_ids.npy')

# Global model variable (Lazy Loading)
_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading Sentence Transformer...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def semantic_search(name, abstract="", threshold=0.60, top_k=3):
    """
    Core search function for ProjectGuard. 
    Returns True if a similar project exists, along with match details.
    """
    # 1. Load the database index
    db_vectors = np.load(vectors_path)
    db_ids     = np.load(ids_path)
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    # 2. Encode the query
    model = get_model()
    query_text = f"{name}. {abstract if abstract else ''}"
    query_vec  = model.encode(query_text)

    # 3. Calculate similarities
    scores = util.cos_sim(query_vec, db_vectors)[0].numpy()
    
    # Get the top matches
    results = []
    for i, score in enumerate(scores):
        proj_id   = str(db_ids[i])
        proj_name = metadata.get(proj_id, "Unknown")
        results.append({"name": proj_name, "score": float(score)})

    # Sort high -> low
    results.sort(key=lambda x: x["score"], reverse=True)

    best_match = results[0]
    exists = best_match["score"] >= threshold

    return {
        "exists": exists,
        "best_match": best_match,
        "top_k": results[:top_k]
    }

# --- Quick Test Execution ---
if __name__ == "__main__":
    test_query = "AI based crop disease detection"
    result = semantic_search(test_query)
    
    print(f"\nQuery: '{test_query}'")
    print(f"─────────────────────────────────")
    if result["exists"]:
        print(f"✅ EXISTS: {result['best_match']['name']} ({result['best_match']['score']:.4f})")
    else:
        print(f"🆕 NEW Project Idea!")
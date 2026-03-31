import sqlite3
import json
import re
from collections import Counter
import os
import sys

# Add Models/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.tokenizer import clean_text

base_dir = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'data', 'training_data.db')
setup_sql_path = os.path.join(base_dir, 'data', 'setup.sql')
vocab_path = os.path.join(base_dir, 'vocab.json')

is_new_db = not os.path.exists(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

if is_new_db:
    print(f"Database '{db_path}' not found. Regenerating from setup.sql...")
    with open(setup_sql_path, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    conn.commit()

cursor.execute("SELECT project_name, project_abstract FROM projects")
rows = cursor.fetchall()
conn.close()

print(f"Loaded {len(rows)} projects from database")

all_tokens = []

for name, abstract in rows:
    tokens = clean_text(name) + clean_text(abstract)
    all_tokens.extend(tokens)

word_counts = Counter(all_tokens)
print(f"Total unique words found: {len(word_counts)}")

vocab = {"<PAD>": 0, "<UNK>": 1}

for word, count in word_counts.most_common():
    vocab[word] = len(vocab)

print(f"Vocabulary size: {len(vocab)}")

with open(vocab_path, "w") as f:
    json.dump(vocab, f, indent=2)

print(f"Saved {vocab_path} ✓")

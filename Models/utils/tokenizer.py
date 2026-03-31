import re
import json
import os

_vocab = None
def load_vocab():
    try:
        # Assuming the root execution might be from Models or ProjectGuard.
        # It's safer to resolve relative to this file's location.
        vocab_path = os.path.join(os.path.dirname(__file__), '..', 'vocab.json')
        with open(vocab_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def clean_text(text):
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()

def tokenize(name, abstract='', max_len=64):
    global _vocab
    if _vocab is None:
        _vocab = load_vocab()
    
    tokens = clean_text(name) + clean_text(abstract)
    indices = [_vocab.get(word, 1) for word in tokens]
    if len(indices) < max_len:
        indices += [0] * (max_len - len(indices))
    else:
        indices = indices[:max_len]
    return indices

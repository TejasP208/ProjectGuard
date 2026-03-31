import sys
import os

# Add Models/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.tokenizer import tokenize

test_name = "AI based crop disease detection"
test_abstract = "A system that detects diseases in crops using image processing"

result = tokenize(test_name, test_abstract)

print(f"Output length: {len(result)}")   # should always be 64
print(f"First 10 values: {result[:10]}")

import json
import os

def remove_duplicates(target_file):
    print(f"Processing '{target_file}' to remove duplicates...")
    
    # Resolve relative paths based on the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(script_dir, target_file)
    
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find '{target_path}'.")
        return
    except json.JSONDecodeError:
        print(f"Error: '{target_path}' is not a valid JSON file.")
        return
        
    unique_pairs = []
    seen = set()
    
    for item in data:
        # Create a stable, hashable representation of the dictionary
        # Sorting keys ensures we identify duplicates even if key order differs
        item_tuple = tuple(sorted(item.items()))
        if item_tuple not in seen:
            seen.add(item_tuple)
            unique_pairs.append(item)
            
    original_size = len(data)
    final_size = len(unique_pairs)
    removed_count = original_size - final_size
            
    print(f"Original pairs count: {original_size}")
    print(f"Duplicates removed:   {removed_count}")
    
    # Write back to the same file
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(unique_pairs, f, indent=2)
    
    print(f"Successfully updated '{target_file}'")
    print(f"Final length of '{target_file}': {final_size}")

if __name__ == "__main__":
    # Target the original file
    filename = 'training_pairs.json'
    
    # Fallback to the typo if needed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(script_dir, filename)) and os.path.exists(os.path.join(script_dir, 'traning_paris.json')):
        filename = 'traning_paris.json'
    
    remove_duplicates(filename)

import json

# Step 1: Load the JSON file
with open('qa_pairs.json', 'r') as json_file:
    qa_pairs = json.load(json_file)

# Define your filter criteria
def filter_criteria(pair, exclude_keywords = ['example']):
    # Example criterion: exclude items that contain the keyword 'example' in the question
    for keyword in exclude_keywords:
        if keyword.lower() in pair['question'].lower():
            return False
    return True

# Step 2: Filter the items based on the criteria
exclude_keywords = ['example']

filtered_qa_pairs = [pair for pair in qa_pairs if filter_criteria(pair, exclude_keywords)]

# Step 3: Save the filtered items back to a JSON file
with open('filtered_qa_pairs.json', 'w') as json_file:
    json.dump(filtered_qa_pairs, json_file, indent=4)

print(f"Filtered {len(qa_pairs) - len(filtered_qa_pairs)} items out of {len(qa_pairs)}.")

import pandas as pd
import json

# Function to convert list of strings to comma-separated string
def convert_keywords(keywords):
    if isinstance(keywords, list):
        return ', '.join(keywords)
    return keywords

def convert_solutions(keywords):
    if isinstance(keywords, list):
        return '\n'.join(keywords)
    return keywords

def format_id(id_value):
    try:
        # Convert to float first to handle cases like '101893.0'
        id_float = float(id_value)
        # Convert to int to remove any decimal part
        id_int = int(id_float)
        # Return as zero-padded string (adjust padding as needed)
        return f"{id_int:09d}"
    except ValueError:
        # If conversion fails, return the original value as string
        return str(id_value)
    
# create message instruction from data
def data_create(
        id:str,question:str = '',
        answer:str = '',
        keywords:str = '',
        instruction:str = 'Give me the solution of the following problem.'
        ):
    return {"messages": [
  {"role": "user", "content": f"Instruct: {instruction}\n{question}"},
  {"role": "assistant", "content": f"{answer}\nID: {id}\nKeywords: {keywords}"},
]}

def main(input_file:str = 'results/test.json', output_file:str = 'results/train.jsonl'):

    # load JSON file
    data = pd.read_json(input_file)

    # Apply the function to the columns
    data['ID'] = data['ID'].astype(str)
    data["ID"] = data['ID'].apply(format_id)
    data['Keywords'] = data['Keywords'].apply(convert_keywords)
    data['Solutions'] = data['Solutions'].apply(convert_solutions)

    # extract the id, problem statement, soluction, and keywords
    ids = list(data["ID"])
    problems = list(data['Problem Statement'])
    solutions = list(data["Solutions"])
    keywords = list(data["Keywords"])

    # convert extracted to train dataset
    train_data = [data_create(id, question, answer, keyword) for id, question, answer, keyword in zip(ids, problems, solutions, keywords)]

    # save dataset as jsonl format
    with open(output_file, "w") as fid:
        for t in train_data:
            json.dump(t, fid)
            fid.write("\n")


if __name__ == "__main__":
    main('results/test.json', 'results/train.jsonl')

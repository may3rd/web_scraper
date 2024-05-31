import re

def parse_context(context):
    sections = {
        'id': None,
        'problem_statement': None,
        'solution': None,
        'keywords': None,
        'reference': None
    }
    
    id_match = re.search(r'ID:\s*(\d+)', context)
    if id_match:
        sections['id'] = id_match.group(1)
    
    problem_match = re.search(r'Problem Statement\s*(.*?)\s*(?=(Solution|Keywords|Reference|$))', context, re.DOTALL)
    if problem_match:
        sections['problem_statement'] = problem_match.group(1).strip()
    
    solution_match = re.search(r'Solution\s*(.*?)\s*(?=(Problem Statement|Keywords|Reference|$))', context, re.DOTALL)
    if solution_match:
        sections['solution'] = solution_match.group(1).strip()
    
    keywords_match = re.search(r'Keywords\s*(.*?)\s*(?=(Problem Statement|Solution|Reference|$))', context, re.DOTALL)
    if keywords_match:
        sections['keywords'] = keywords_match.group(1).strip()
    
    reference_match = re.search(r'Reference\s*(.*?)\s*(?=(Problem Statement|Solution|Keywords|$))', context, re.DOTALL)
    if reference_match:
        sections['reference'] = reference_match.group(1).strip()
    
    return sections

def parse_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
    contexts = content.split('--------------------------')
    parsed_contexts = []
    
    for context in contexts:
        context = context.strip()
        if context:
            parsed_context = parse_context(context)
            if parse_context['id']:
                parsed_contexts.append(parsed_context)
    
    return parsed_contexts

    # Example usage:
    file_path = 'context.txt'
    parsed_contexts = parse_file(file_path)
    for context in parsed_contexts:
        print(context)

import json

# Define a custom dataset class
class MyCustomDataset():
    def __init__(self, txt_file):
        # Load the CSV file into a Pandas DataFrame
        with open(txt_file, 'r') as file:
            content = file.read()
        
        contexts = content.split('--------------------------')
        parsed_contexts = []
        
        for context in contexts:
            context = context.strip()
            if context:
                parsed_context = parse_context(context)
                if not parsed_context['id'] is None and not parsed_context['problem_statement'] is None and not parsed_context['solution'] is None:
                    parsed_contexts.append(parsed_context)
        
        self.data = parsed_contexts

    def __len__(self):
        # Return the total number of samples in the dataset
        return len(self.data)

    def getitem(self, idx):
        # Return a dictionary containing the problem, solution, keyword, and reference for each sample
        problem = self.data[idx]['problem']
        solution = self.data[idx]['solution']
        keyword = self.data[idx]['keyword']
        reference = self.data[idx]['reference']

        return {
            'problem': problem,
            'solution': solution,
            'keyword': keyword,
            'reference': reference
        }

dataset = MyCustomDataset(txt_file='save_output.txt')

print(len(dataset))

with open('dataset.json', 'w') as file:
    json.dump(dataset.data, file)

exit()

# Load the pre-trained LLaMA-3 model and tokenizer
model_name = 'llaama/llaama-3'
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize the Trainer with your custom dataset and hyperparameters
trainer = Trainer(
    model=model,
    args={
        'output_dir': '.',  # Output directory for the trained model
        'max_train_steps': 1000,  # Maximum number of training steps
        'per_device_train_batch_size': 16,  # Batch size per device during training
    },
    train_dataset=MyCustomDataset(csv_file='your_custom_dataset.csv'),  # Load your custom dataset
    compute_metrics=lambda pred: {'accuracy': torch.sum(pred.label_ids == pred.predictions).item()}
)

# Fine-tune the model using your custom dataset
trainer.train()
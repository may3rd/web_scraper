import ollama

def parse_context(system_content, context):

    prompt_text = [{'role': 'system', 'content': system_content}, {'role':'user', 'content': context}]

    response = ollama.chat(model='llama3:8b', messages=prompt_text)

    return response['message']['content']

txt_file = 'save_output.txt'

with open(txt_file, 'r') as file:
    content = file.read()

contexts = content.split('-----------------------------------------------------------------------------------------------------')
parsed_contexts = []

system_content = """You are the text scraper. I will provide you a context and you will capture it contents by the following sections:
1. ID, the id of the context, 
2. Problem Statement, it might be in the section of Problem Statment or Problem or description, 
3. Solution, could be solutions or workaround, you have to capture all the text in this section, 
4. Keywords, 
The output format I want is JSON with string value. You should show only output in the JSON format without any comment or explanation."""

i = 0

with open('results/ollama_20240529.json', 'w') as json_file:
    for context in contexts:
        context = context.strip()
        if context:
            parsed_context = parse_context(system_content, context)
            json_file.write(parsed_context)
            json_file.write(',')
            print(i)
            i += 1


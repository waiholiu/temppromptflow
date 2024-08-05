
from promptflow.client import load_flow
from promptflow.core import tool

import time
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

def split_into_chunks(text, max_size):
    """
    Splits the text into chunks based on lines that do not exceed max_size.
    
    Parameters:
    text (str): The text to be split.
    max_size (int): The maximum size of each chunk.
    
    Returns:
    list: A list of text chunks.
    """
    lines = text.splitlines()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for line in lines:
        line_length = len(line)
        # Check if adding this line would exceed the max_size
        if current_size + line_length + (1 if current_chunk else 0) > max_size:
            # Join the current_chunk into one string and add it to chunks
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]  # Start a new chunk with the current line
            current_size = line_length
        else:
            current_chunk.append(line)
            current_size += line_length + (1 if current_chunk else 0)  # Add 1 for the newline character
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks



def process_file(file_path, flow_path):
    """
    Opens a text file, splits its content based on a max token size, and feeds each chunk into load_flow.
    
    Parameters:
    file_path (str): The path to the text file.
    flow_path (str): The path to the flow DAG definition file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    max_token_size = 4000
    chunks = split_into_chunks(text, max_token_size)
    
    f = load_flow(source=flow_path)
    
    results = [] 
    
    for chunk in chunks[:2]:
        result = f(question=chunk)
        results.append(result) 
        # time.sleep(60)
        print(result)
        
    # After processing all chunks, append the results to a text file
    with open('results.txt', 'a', encoding='utf-8') as results_file:
        for result in results:

            answer = result['answer']
            results_file.write(answer + '\n')

# f = load_flow(source=flow_path)
# result = f(url='hello')

# print(result)

file_path = 'helloworldprmoptflow/input.txt'
flow_path = 'helloworldprmoptflow/flow.dag.yaml'
process_file(file_path, flow_path)




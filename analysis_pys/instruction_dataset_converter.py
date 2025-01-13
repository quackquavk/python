import json
import random

def create_instruction_template(question_data):
    # Create instruction templates based on different parameters
    templates = [
        f"Generate a {question_data['complexity_level']} difficulty {question_data['question_type']} question worth {question_data['marks']} marks from the chapter '{question_data['chapter']}'.",
        
        f"Create a {question_data['marks']}-mark question on {question_data['chapter']} that tests {question_data['question_type']} skills. The difficulty should be {question_data['complexity_level']}.",
        
        f"Design a {question_data['complexity_level']}-level {question_data['question_type']} question from '{question_data['chapter']}' chapter that carries {question_data['marks']} marks."
    ]
    
    return random.choice(templates)

def convert_to_instruction_format(input_file, output_file):
    instruction_data = []
    
    with open(input_file, 'r') as f:
        for line in f:
            question_data = json.loads(line)
            
            instruction_example = {
                "instruction": create_instruction_template(question_data),
                "input": "",  # Can be empty for this use case
                "output": question_data["question"],
                "metadata": {  # Optional metadata for tracking
                    "chapter": question_data["chapter"],
                    "marks": question_data["marks"],
                    "question_type": question_data["question_type"],
                    "pattern_frequency": question_data["pattern_frequency"],
                    "complexity_level": question_data["complexity_level"]
                }
            }
            
            instruction_data.append(instruction_example)
    
    # Write to JSONL format
    with open(output_file, 'w') as f:
        for example in instruction_data:
            f.write(json.dumps(example) + '\n')

# Convert the dataset
convert_to_instruction_format('marks_.jsonl', 'instruction_dataset.jsonl') 
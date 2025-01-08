import json

def create_enhanced_instruction_dataset(jsonl_file, output_file):
    instructions = []
    
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            
            # Get appropriate instruction template
            instruction = INSTRUCTION_TEMPLATES.get(
                data.get("question_type", "theoretical")
            )
            
            instruction_data = {
                "instruction": instruction,
                "input": {
                    "question": data["question"],
                    "marks_allocated": data.get("marks", ""),
                    "chapter": data["chapter"]
                },
                "output": {
                    "solution_structure": "Let's solve this step by step:",
                    "key_points": [
                        "Understanding the question",
                        "Relevant formulas/concepts",
                        "Step-by-step solution",
                        "Final answer/conclusion"
                    ],
                    "complexity": data.get("complexity_level", "medium"),
                    "pattern_frequency": data.get("pattern_frequency", "occasional")
                }
            }
            
            instructions.append(instruction_data)
    
    with open(output_file, 'w') as f:
        json.dump(instructions, f, indent=2)

# Usage
create_enhanced_instruction_dataset('marks_.jsonl', 'enhanced_instruction_dataset.json') 
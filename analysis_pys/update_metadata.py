import os
import json
import random
from typing import List, Dict

def get_year_range() -> List[str]:
    """Return a list of years from 2014 to 2023."""
    return [str(year) for year in range(2014, 2024)]

def assign_year_by_frequency(pattern_frequency: str, available_years: List[str]) -> str:
    """Assign a year based on the pattern frequency."""
    if not available_years:
        return random.choice(get_year_range())
        
    # Probability of assigning a year based on frequency
    probabilities = {
        "yearly": 0.95,      # Almost certain to get a year
        "frequent": 0.7,     # High chance
        "occasional": 0.4,   # Lower chance
        "rare": 0.2         # Very low chance
    }
    
    # Default to occasional if frequency not found
    prob = probabilities.get(pattern_frequency.lower(), 0.4)
    
    # Randomly decide whether to assign a year based on probability
    if random.random() < prob:
        return random.choice(available_years)
    else:
        # If we don't assign from available years, pick from full range
        return random.choice(get_year_range())

def update_jsonl_with_year(jsonl_path: str, output_path: str):
    """Update JSONL file with year information based on pattern frequency."""
    print("Updating JSONL file with years based on pattern frequency...")
    
    # Get available years
    available_years = get_year_range()
    
    # Track assigned years for each frequency to maintain distribution
    frequency_years: Dict[str, List[str]] = {
        "yearly": [],
        "frequent": [],
        "occasional": [],
        "rare": []
    }
    
    updated_lines = []
    updated_count = 0
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            
            if 'metadata' in entry:
                pattern_frequency = entry['metadata'].get('pattern_frequency', 'occasional')
                
                # Get years already used for this frequency
                used_years = frequency_years.get(pattern_frequency, [])
                
                # Get available years (excluding overused ones)
                available = [y for y in available_years if y not in used_years]
                if not available:
                    available = available_years  # Reset if all years used
                
                # Assign year based on frequency
                year = assign_year_by_frequency(pattern_frequency, available)
                
                # Update metadata
                entry['metadata']['previous_years'] = year
                updated_count += 1
                
                # Track assigned year
                if pattern_frequency in frequency_years:
                    frequency_years[pattern_frequency].append(year)
                    # Keep only last few assignments to allow reuse after some time
                    frequency_years[pattern_frequency] = frequency_years[pattern_frequency][-3:]
            
            updated_lines.append(json.dumps(entry, ensure_ascii=False))
    
    # Write updated content
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in updated_lines:
            f.write(line + '\n')
    
    print(f"\nUpdated {updated_count} entries with year information")
    
    # Print distribution statistics
    print("\nYear distribution by frequency:")
    for freq, years in frequency_years.items():
        year_counts = {}
        for y in years:
            year_counts[y] = year_counts.get(y, 0) + 1
        print(f"{freq}: {dict(sorted(year_counts.items()))}")

def main():
    # Configure these paths according to your setup
    jsonl_path = 'instruction_dataset.jsonl'
    output_path = 'updated_instruction_dataset.jsonl'
    
    update_jsonl_with_year(jsonl_path, output_path)
    print(f"\nUpdated dataset saved to {output_path}")

if __name__ == "__main__":
    main() 
import json
from collections import defaultdict, Counter
from typing import Dict, List
import matplotlib.pyplot as plt
from pprint import pprint

def load_jsonl(file_path: str) -> List[dict]:
    """Load JSONL file and return list of entries."""
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            entries.append(json.loads(line.strip()))
    return entries

def analyze_dataset(entries: List[dict]):
    """Perform comprehensive analysis of the dataset."""
    
    # Initialize counters
    year_freq = defaultdict(int)
    pattern_freq = defaultdict(int)
    chapter_freq = defaultdict(int)
    question_types = defaultdict(int)
    complexity_levels = defaultdict(int)
    marks_dist = defaultdict(int)
    
    # Year distribution by pattern frequency
    year_by_pattern = defaultdict(lambda: defaultdict(int))
    
    # Chapter distribution by year
    chapter_by_year = defaultdict(lambda: defaultdict(int))
    
    # Analyze each entry
    for entry in entries:
        metadata = entry.get('metadata', {})
        
        # Extract fields
        year = metadata.get('previous_years')
        pattern = metadata.get('pattern_frequency')
        chapter = metadata.get('chapter')
        q_type = metadata.get('question_type')
        complexity = metadata.get('complexity_level')
        marks = metadata.get('marks')
        
        # Update counters
        if year:
            year_freq[year] += 1
            if pattern:
                year_by_pattern[pattern][year] += 1
            if chapter:
                chapter_by_year[year][chapter] += 1
        
        if pattern:
            pattern_freq[pattern] += 1
        if chapter:
            chapter_freq[chapter] += 1
        if q_type:
            question_types[q_type] += 1
        if complexity:
            complexity_levels[complexity] += 1
        if marks:
            marks_dist[marks] += 1
    
    # Print analysis results
    print("\n=== Dataset Analysis ===\n")
    
    print("1. Overall Year Distribution:")
    pprint(dict(sorted(year_freq.items())))
    
    print("\n2. Pattern Frequency Distribution:")
    pprint(dict(sorted(pattern_freq.items())))
    
    print("\n3. Year Distribution by Pattern Frequency:")
    for pattern, years in year_by_pattern.items():
        print(f"\n{pattern}:")
        pprint(dict(sorted(years.items())))
    
    print("\n4. Question Types Distribution:")
    pprint(dict(sorted(question_types.items())))
    
    print("\n5. Complexity Levels Distribution:")
    pprint(dict(sorted(complexity_levels.items())))
    
    print("\n6. Marks Distribution:")
    pprint(dict(sorted(marks_dist.items())))
    
    print("\n7. Top Chapters:")
    top_chapters = sorted(chapter_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    for chapter, count in top_chapters:
        print(f"{chapter}: {count}")
    
    # Plot year distribution
    plt.figure(figsize=(12, 6))
    years = sorted(year_freq.keys())
    counts = [year_freq[year] for year in years]
    plt.bar(years, counts)
    plt.title('Distribution of Questions by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Questions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('year_distribution.png')
    
    # Plot pattern frequency distribution
    plt.figure(figsize=(10, 6))
    patterns = list(pattern_freq.keys())
    counts = [pattern_freq[pattern] for pattern in patterns]
    plt.bar(patterns, counts)
    plt.title('Distribution of Pattern Frequencies')
    plt.xlabel('Pattern')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('pattern_distribution.png')

def main():
    # Load and analyze the dataset
    entries = load_jsonl('updated_instruction_dataset.jsonl')
    analyze_dataset(entries)
    print("\nAnalysis complete! Check year_distribution.png and pattern_distribution.png for visualizations.")

if __name__ == "__main__":
    main() 
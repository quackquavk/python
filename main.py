import json
from question_pattern_analyzer import QuestionPatternAnalyzer
from question_generator import QuestionGenerator

def main():
    # Initialize analyzer and generator
    analyzer = QuestionPatternAnalyzer()
    analyzer.analyze_patterns('marks_.jsonl')
    
    generator = QuestionGenerator(analyzer)
    
    # Generate new question paper
    question_paper = []
    
    # Example generation rules based on analyzed patterns
    for chapter, patterns in analyzer.chapter_patterns.items():
        most_common_type = max(set(p['question_type'] for p in patterns), 
                             key=lambda x: sum(1 for p in patterns if p['question_type'] == x))
        
        typical_marks = max(set(p['marks'] for p in patterns), 
                          key=lambda x: sum(1 for p in patterns if p['marks'] == x))
        
        new_question = generator.generate_question(
            chapter=chapter,
            question_type=most_common_type,
            marks=typical_marks
        )
        
        question_paper.append({
            "chapter": chapter,
            "question": new_question,
            "marks": typical_marks,
            "question_type": most_common_type
        })
    
    # Save generated questions
    with open('generated_questions.json', 'w') as f:
        json.dump(question_paper, f, indent=2)

if __name__ == "__main__":
    main() 
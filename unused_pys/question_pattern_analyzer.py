import json
from collections import defaultdict

class QuestionPatternAnalyzer:
    def __init__(self):
        self.chapter_patterns = defaultdict(list)
        self.complexity_distribution = defaultdict(int)
        self.marks_distribution = defaultdict(int)
        self.question_types = defaultdict(int)
        self.frequency_patterns = defaultdict(int)
        
    def analyze_patterns(self, jsonl_file):
        with open(jsonl_file, 'r') as file:
            for line in file:
                question = json.loads(line)
                
                # Store chapter-wise question patterns
                self.chapter_patterns[question['chapter']].append({
                    'question_type': question.get('question_type'),
                    'marks': question.get('marks'),
                    'complexity': question.get('complexity_level'),
                    'pattern': self._extract_question_pattern(question['question'])
                })
                
                # Analyze distributions
                self.complexity_distribution[question.get('complexity_level')] += 1
                self.marks_distribution[question.get('marks')] += 1
                self.question_types[question.get('question_type')] += 1
                self.frequency_patterns[question.get('pattern_frequency')] += 1
    
    def _extract_question_pattern(self, question):
        """Extract pattern templates from questions"""
        # Common question starters
        starters = {
            'design': ['Design', 'Implement', 'Construct', 'Draw'],
            'explain': ['Explain', 'Describe', 'What is', 'Define'],
            'convert': ['Convert', 'Transform', 'Change'],
            'compare': ['Compare', 'Differentiate', 'Contrast'],
            'analyze': ['Analyze', 'Examine', 'Investigate']
        }
        
        for pattern_type, keywords in starters.items():
            if any(question.startswith(word) for word in keywords):
                return pattern_type
        return 'other' 
import random

class QuestionGenerator:
    def __init__(self, pattern_analyzer):
        self.analyzer = pattern_analyzer
        self.templates = self._load_templates()
        self.components_by_type = self._init_components()
    
    def _load_templates(self):
        return {
            'design': [
                "Design a {}-bit {} using {}",
                "Implement a {} using {}",
                "Draw the circuit diagram for {} using {}"
            ],
            'theoretical': [
                "Explain the working principle of {}",
                "What is {}? Describe its operation",
                "State and prove {} for digital circuits"
            ],
            'numerical': [
                "Convert {} to {}",
                "Perform {} using {}",
                "Simplify the Boolean function: {}"
            ],
            'analysis': [
                "Analyze the {} circuit",
                "Examine the behavior of {}",
                "Investigate the properties of {}"
            ]
        }
    
    def _init_components(self):
        return {
            'design': {
                'bits': ['2', '3', '4', '8'],
                'components': ['counter', 'register', 'adder', 'decoder', 'multiplexer'],
                'technologies': ['T flip-flops', 'JK flip-flops', 'D flip-flops', 'NAND gates', 'NOR gates']
            },
            'theoretical': {
                'concepts': ['flip-flop', 'Boolean algebra', 'sequential circuit', 'combinational logic',
                           'master-slave flip-flop', 'synchronous counter', 'asynchronous counter'],
                'operations': ['truth table', 'characteristic equation', 'state diagram']
            },
            'numerical': {
                'number_systems': ['binary', 'octal', 'decimal', 'hexadecimal', 'BCD'],
                'operations': ['addition', 'subtraction', 'conversion'],
                'methods': ["1's complement", "2's complement", "r's complement"]
            }
        }

    def _fill_template(self, template, components, marks):
        """Fill template with appropriate components based on question type"""
        try:
            if 'design' in components['pattern']:
                if '{}' in template:
                    if template.count('{}') == 3:
                        bits = random.choice(self.components_by_type['design']['bits'])
                        component = random.choice(self.components_by_type['design']['components'])
                        technology = random.choice(self.components_by_type['design']['technologies'])
                        return template.format(bits, component, technology)
                    else:
                        component = random.choice(self.components_by_type['design']['components'])
                        technology = random.choice(self.components_by_type['design']['technologies'])
                        return template.format(component, technology)
            
            elif 'numerical' in components['pattern']:
                if template.count('{}') == 2:
                    num_system1 = random.choice(self.components_by_type['numerical']['number_systems'])
                    num_system2 = random.choice(self.components_by_type['numerical']['number_systems'])
                    while num_system1 == num_system2:
                        num_system2 = random.choice(self.components_by_type['numerical']['number_systems'])
                    return template.format(num_system1, num_system2)
                else:
                    return template.format(random.choice(self.components_by_type['numerical']['operations']))
            
            else:  # theoretical or other
                concept = random.choice(self.components_by_type['theoretical']['concepts'])
                return template.format(concept)
                
        except (KeyError, IndexError):
            return f"Generate a {marks}-mark question about {components.get('pattern', 'topic')}"
    
    def _extract_components(self, patterns):
        """Extract common components from similar questions"""
        if not patterns:
            return {'pattern': 'theoretical'}
            
        # Get the most common pattern type
        pattern_types = [p['pattern'] for p in patterns if 'pattern' in p]
        if pattern_types:
            most_common = max(set(pattern_types), key=pattern_types.count)
            return {'pattern': most_common}
        return {'pattern': 'theoretical'}
    
    def generate_question(self, chapter, question_type, marks):
        """Generate a new question based on patterns"""
        if question_type not in self.templates:
            question_type = 'theoretical'  # default to theoretical if type not found
            
        template = random.choice(self.templates[question_type])
        
        # Get common components from chapter patterns
        chapter_patterns = self.analyzer.chapter_patterns[chapter]
        components = self._extract_components(chapter_patterns)
        
        question = self._fill_template(template, components, marks)
        return f"{question} [{marks} marks]" 
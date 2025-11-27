from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

class PromptStage(Enum):
    ZERO_SHOT = "zero_shot"
    FEW_SHOT = "few_shot" 
    COT = "chain_of_thought"
    PERSONA = "persona_enhanced"
    HYBRID = "cot_persona_combined"

@dataclass
class ProgressivePromptConfig:
    base_instruction: str
    examples: List[Dict] = None
    cot_reasoning: str = None
    persona: str = None
    reasoning_depth: str = "basic"  # basic, intermediate, advanced

class ProgressivePromptEnhancer:
    def __init__(self):
        self.personas = {
            "senior_engineer": "You are a senior Java engineer with 10+ years of enterprise experience.",
            "academic": "You are a computer science professor specializing in algorithms and data structures.", 
            "architect": "You are a software architect focused on clean, maintainable, and scalable code.",
            "security_expert": "You are a security-focused developer who prioritizes secure coding practices."
        }
        
    def generate_progressive_prompts(self, problem: Dict, config: ProgressivePromptConfig) -> Dict[PromptStage, str]:
        """Generate all prompt stages for comparative analysis."""
        prompts = {}
        
        # Zero-shot (baseline)
        prompts[PromptStage.ZERO_SHOT] = self._create_zero_shot(problem, config)
        
        # Few-shot with examples
        prompts[PromptStage.FEW_SHOT] = self._create_few_shot(problem, config)
        
        # CoT reasoning
        prompts[PromptStage.COT] = self._create_cot(problem, config)
        
        # Persona-enhanced
        prompts[PromptStage.PERSONA] = self._create_persona(problem, config)
        
        # Hybrid (CoT + Persona) - Novel combination
        prompts[PromptStage.HYBRID] = self._create_hybrid(problem, config)
        
        return prompts
    
    def _create_cot(self, problem: Dict, config: ProgressivePromptConfig) -> str:
        reasoning_templates = {
            "basic": """
Think step by step:
1. Understand the problem requirements
2. Identify input/output constraints  
3. Choose appropriate data structures
4. Design the algorithm logic
5. Implement with proper error handling
""",
            "intermediate": """
Let me break this down systematically:
1. Problem Analysis: What exactly needs to be solved?
2. Constraint Analysis: What are the time/space complexity requirements?
3. Edge Case Identification: What corner cases should be handled?
4. Algorithm Selection: Which approach is most suitable?
5. Implementation Strategy: How to structure the code for maintainability?
6. Testing Strategy: How to verify correctness?
""",
            "advanced": """
I'll approach this using systematic software engineering principles:
1. Requirements Analysis: Parse the problem specification thoroughly
2. Design Considerations: Evaluate multiple algorithmic approaches
3. Complexity Analysis: Determine optimal time/space trade-offs
4. Architecture Planning: Structure code for extensibility and maintenance
5. Implementation with Defensive Programming: Handle all edge cases and errors
6. Code Quality Assurance: Ensure readability, documentation, and best practices
"""
        }
        
        base_prompt = config.base_instruction
        reasoning = reasoning_templates.get(config.reasoning_depth, reasoning_templates["basic"])
        
        return f"{reasoning}\n\nProblem: {problem['description']}\nConstraints: {problem.get('constraints', '')}\n\nProvide a complete Java solution."

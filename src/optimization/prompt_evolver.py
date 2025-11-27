class PromptEvolutionEngine:
    def __init__(self):
        self.improvement_strategies = {
            "low_compilation_rate": "Add more specific syntax examples",
            "poor_error_handling": "Emphasize robust error handling in persona",
            "inefficient_algorithms": "Include complexity requirements in CoT",
            "poor_readability": "Enhance persona focus on code clarity"
        }
    
    def evolve_prompt(self, prompt: str, performance_metrics: Dict) -> str:
        """Automatically improve prompts based on generation results."""
        improvements = []
        
        if performance_metrics.get('compilation_success_rate', 1.0) < 0.8:
            improvements.append(self._add_syntax_guidance())
            
        if performance_metrics.get('functional_correctness', 1.0) < 0.7:
            improvements.append(self._enhance_logic_guidance())
            
        return self._apply_improvements(prompt, improvements)

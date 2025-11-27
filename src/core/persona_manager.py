class PersonaManager:
    def __init__(self):
        self.persona_profiles = {
            "enterprise_developer": {
                "description": "Senior enterprise Java developer with focus on maintainability",
                "priorities": ["code_reusability", "documentation", "error_handling"],
                "style_preferences": ["verbose_naming", "extensive_comments", "defensive_programming"]
            },
            "performance_engineer": {
                "description": "Performance-focused engineer optimizing for speed and efficiency", 
                "priorities": ["time_complexity", "memory_optimization", "algorithmic_efficiency"],
                "style_preferences": ["concise_code", "technical_comments", "optimization_focus"]
            },
            "security_specialist": {
                "description": "Security-conscious developer prioritizing safe coding practices",
                "priorities": ["input_validation", "secure_coding", "vulnerability_prevention"],
                "style_preferences": ["paranoid_validation", "security_comments", "defensive_coding"]
            }
        }
    
    def generate_persona_variations(self, base_problem: str) -> List[str]:
        """Generate multiple persona-enhanced prompts for comparative analysis."""
        variations = []
        for persona_name, profile in self.persona_profiles.items():
            prompt = self._create_persona_prompt(base_problem, profile)
            variations.append({
                "persona_type": persona_name,
                "prompt": prompt,
                "expected_characteristics": profile["priorities"]
            })
        return variations

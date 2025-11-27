import yaml
from pathlib import Path
from typing import Dict, List

class DynamicPromptManager:
    def __init__(self):
        self.custom_prompts = []
    
    def add_prompt_from_input(self) -> Dict:
        """Interactive prompt creation."""
        print("\n=== Add Custom Prompt ===")
        
        name = input("Prompt name: ")
        strategy = input("Strategy (basic/detailed/step_by_step/etc.): ")
        
        print("Enter your prompt template (use {problem_description} and {constraints} as variables):")
        print("Press Ctrl+Z (Windows) or Ctrl+D (Linux/Mac) then Enter when done:")
        
        template_lines = []
        try:
            while True:
                line = input()
                template_lines.append(line)
        except EOFError:
            pass
        
        template = "\n".join(template_lines)
        
        expected_tokens = int(input("Expected tokens (default 200): ") or "200")
        complexity = input("Complexity level (simple/intermediate/advanced): ") or "intermediate"
        
        prompt_data = {
            "name": name,
            "strategy": strategy,
            "template": template,
            "variables": ["problem_description", "constraints"],
            "expected_tokens": expected_tokens,
            "complexity_level": complexity
        }
        
        return prompt_data
    
    def save_custom_prompt(self, prompt_data: Dict, filename: str = "custom_prompts.yaml"):
        """Save custom prompt to file."""
        filepath = Path(f"config/prompts/{filename}")
        
        if filepath.exists():
            with open(filepath, 'r') as f:
                existing = yaml.safe_load(f) or {"prompts": []}
        else:
            existing = {"prompts": []}
        
        existing["prompts"].append(prompt_data)
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            yaml.safe_dump(existing, f, default_flow_style=False, indent=2)
        
        print(f"✅ Prompt saved to {filepath}")

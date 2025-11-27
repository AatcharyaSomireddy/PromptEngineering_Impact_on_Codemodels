from enum import Enum
from dataclasses import dataclass
from typing import Dict, List
import yaml

class PromptStrategy(Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    STEP_BY_STEP = "step_by_step"
    ZERO_SHOT = "zero_shot"
    COT = "cot"
    FEW_SHOT = "few_shot"
    PERSONA = "persona"
    TEMPLATE = "template"

@dataclass
class PromptTemplate:
    name: str
    strategy: PromptStrategy
    template: str
    variables: List[str]
    expected_tokens: int = 200
    complexity_level: str = "simple"

class PromptManager:
    def __init__(self, config_path: str):
        self.prompts: Dict[str, PromptTemplate] = self._load_prompts(config_path)

    def _load_prompts(self, path: str) -> Dict[str, PromptTemplate]:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        prompts = {}
        for p in data['prompts']:
            template = PromptTemplate(
                name=p['name'],
                strategy=PromptStrategy(p['strategy']),
                template=p['template'],
                variables=p['variables'],
                expected_tokens=p.get('expected_tokens', 200),
                complexity_level=p.get('complexity_level', 'simple')
            )
            prompts[template.name] = template
        
        return prompts

    def get_prompt(self, name: str, **kwargs) -> str:
        template = self.prompts[name]
        return template.template.format(**kwargs)

    def list_strategies(self) -> List[PromptStrategy]:
        return list(set(prompt.strategy for prompt in self.prompts.values()))

    def get_prompts_by_strategy(self, strategy: PromptStrategy) -> List[PromptTemplate]:
        return [p for p in self.prompts.values() if p.strategy == strategy]

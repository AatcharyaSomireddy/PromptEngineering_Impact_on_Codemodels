"""High-level evaluator that fuses generation + analysis"""
from typing import Dict
from src.analysis.java_analyzer import JavaAnalyzer
from src.core.code_generator import GenerationResult

class Evaluator:
    def __init__(self):
        self.analyzer = JavaAnalyzer()

    def evaluate(self, gen: GenerationResult) -> Dict:
        if not gen.success:
            return {"score": 0, "compilation_success": False}
        metrics = self.analyzer.analyze_code(gen.generated_code)
        score = (
            metrics.test_pass_rate * 0.5
            + metrics.compilation_success * 0.3
            + (1 / (1 + metrics.cyclomatic_complexity)) * 0.2
        )
        return {"score": score, "metrics": metrics}

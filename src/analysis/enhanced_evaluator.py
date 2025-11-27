from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import List, Dict, Any
import numpy as np

class EnhancedCodeEvaluator:
    """Enhanced evaluator with classification metrics for code generation."""
    
    def __init__(self):
        pass
    
    def evaluate_generation_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Calculate classification metrics for code generation results."""
        
        # Extract binary labels (1=success, 0=failure)
        predictions = [1 if r['success'] else 0 for r in results]
        
        # For code generation, we assume all attempts should ideally succeed
        # So ground truth is all 1s (perfect expectation)
        ground_truth = [1] * len(predictions)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(ground_truth, predictions),
            'precision': precision_score(ground_truth, predictions, zero_division=0),
            'recall': recall_score(ground_truth, predictions, zero_division=0),
            'f1_score': f1_score(ground_truth, predictions, zero_division=0),
            'total_attempts': len(predictions),
            'successful_generations': sum(predictions),
            'success_rate': sum(predictions) / len(predictions) if predictions else 0
        }
        
        return metrics
    
    def evaluate_by_strategy(self, results: List[Dict]) -> Dict[str, Dict]:
        """Calculate metrics grouped by prompt strategy."""
        strategy_groups = {}
        
        # Group results by strategy
        for result in results:
            strategy = result['request']['strategy']
            if strategy not in strategy_groups:
                strategy_groups[strategy] = []
            strategy_groups[strategy].append(result)
        
        # Calculate metrics for each strategy
        strategy_metrics = {}
        for strategy, group_results in strategy_groups.items():
            strategy_metrics[strategy] = self.evaluate_generation_results(group_results)
        
        return strategy_metrics
    
    def evaluate_by_model(self, results: List[Dict]) -> Dict[str, Dict]:
        """Calculate metrics grouped by model."""
        model_groups = {}
        
        # Group results by model
        for result in results:
            model = result['request']['model_name']
            if model not in model_groups:
                model_groups[model] = []
            model_groups[model].append(result)
        
        # Calculate metrics for each model
        model_metrics = {}
        for model, group_results in model_groups.items():
            model_metrics[model] = self.evaluate_generation_results(group_results)
        
        return model_metrics

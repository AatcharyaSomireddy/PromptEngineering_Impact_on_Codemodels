"""
Dataset loading utilities for standard code generation benchmarks
"""
from typing import Dict, List, Any

def load_humaneval_problems():
    """Load HumanEval dataset problems"""
    from datasets import load_dataset
    dataset = load_dataset("openai/openai_humaneval")
    
    problems = []
    for item in dataset["test"]:
        problems.append({
            "id": item["task_id"],
            "title": f"HumanEval Problem {item['task_id']}",
            "description": item["prompt"],
            "constraints": "Follow the function signature and docstring requirements",
            "canonical_solution": item["canonical_solution"],
            "test_cases": item["test"],
            "entry_point": item["entry_point"]
        })
    return {"problems": problems}

def load_mbpp_problems():
    """Load MBPP dataset problems"""
    from datasets import load_dataset
    dataset = load_dataset("google-research-datasets/mbpp")
    
    problems = []
    for item in dataset["test"]:
        problems.append({
            "id": f"MBPP_{item['task_id']}",
            "title": f"MBPP Problem {item['task_id']}",
            "description": item["text"],
            "constraints": "Write efficient and readable Python code",
            "canonical_solution": item["code"],
            "test_cases": item["test_list"]
        })
    return {"problems": problems}

def save_dataset_as_json(dataset_func, filename: str, limit: int = None):
    """Save dataset to JSON file for use with existing benchmark system"""
    import json
    import os
    
    # Load dataset
    data = dataset_func()
    
    # Limit number of problems if specified
    if limit:
        data["problems"] = data["problems"][:limit]
    
    # Ensure directory exists
    os.makedirs("data/input/problem_sets", exist_ok=True)
    
    # Save to JSON
    filepath = f"data/input/problem_sets/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(data['problems'])} problems to {filepath}")
    return filepath

if __name__ == "__main__":
    # Generate dataset files when run directly
    print("Generating HumanEval dataset...")
    save_dataset_as_json(load_humaneval_problems, "humaneval_full.json", limit=10)
    
    print("Generating MBPP dataset...")
    save_dataset_as_json(load_mbpp_problems, "mbpp_full.json", limit=20)

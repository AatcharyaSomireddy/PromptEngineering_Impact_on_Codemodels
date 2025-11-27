import json
from pathlib import Path

# Debug your exact problem loading process
set_name = "basic"
problems_dir = Path("data/input/problem_sets")
path = problems_dir / f"{set_name}.json"

print(f" File path: {path}")
print(f" File exists: {path.exists()}")

# Load exactly like your benchmark_runner.py does
if path.exists():
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f" Data type: {type(data)}")
    print(f" Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
    
    if "problems" in data:
        problems_list = data["problems"]
        print(f" Problems type: {type(problems_list)}")
        print(f" Problems count: {len(problems_list)}")
        
        if problems_list:
            first_problem = problems_list[0]
            print(f" First problem type: {type(first_problem)}")
            print(f" First problem: {first_problem}")
            
            # This is where the error happens - test if it's a dict
            if isinstance(first_problem, dict):
                print(" First problem IS a dictionary")
                print(f" Keys: {list(first_problem.keys())}")
            else:
                print(" First problem is NOT a dictionary - THIS IS THE ISSUE!")
                print(f" It's a: {type(first_problem)}")
    else:
        print(" No 'problems' key found in data!")
else:
    print(" File doesn't exist!")

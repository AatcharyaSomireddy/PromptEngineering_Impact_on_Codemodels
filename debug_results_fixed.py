import sys
import os
sys.path.append("src")
from src.core.benchmark_runner import BenchmarkRunner
import json
import asyncio

async def debug_results():
    print(" Starting debug analysis...")
    
    # Pass config path as string, not dict
    config_path = "config/research_config.json"
    
    # Create benchmark runner with path
    runner = BenchmarkRunner(config_path)
    
    # Load problems
    problems = runner._load_problem_set("basic")["problems"]
    print(f" Loaded {len(problems)} problems")
    
    # Build just a few requests for debugging
    requests = runner._build_requests(problems[:1])  # Just first problem
    print(f" Generated {len(requests)} requests")
    
    if len(requests) > 0:
        # Examine the request structure
        first_request = requests[0]
        print(f"\n REQUEST STRUCTURE:")
        print(f"   Type: {type(first_request)}")
        print(f"   Attributes: {dir(first_request)}")
        if hasattr(first_request, '__dict__'):
            print(f"   Request Data: {first_request.__dict__}")
        
        # Generate results for debugging  
        print(f"\n Generating results...")
        results = await runner.gen.batch_generate(requests[:3])  # Just 3 for debugging
        
        print(f"\n Generated {len(results)} results")
        
        for i, result in enumerate(results):
            print(f"\n RESULT {i} STRUCTURE:")
            print(f"   Type: {type(result)}")
            print(f"   Attributes: {sorted(dir(result))}")
            
            if hasattr(result, '__dict__'):
                print(f"   Result Data Keys: {list(result.__dict__.keys())}")
                for key, value in result.__dict__.items():
                    print(f"     {key}: {value}")
            
            # Check common attribute names
            common_attrs = ['strategy', 'model_name', 'problem_id', 'execution_time', 
                          'generated_code', 'success', 'time_s', 'model', 'prompt_strategy']
            
            print(f"   Checking common attributes:")
            for attr in common_attrs:
                if hasattr(result, attr):
                    value = getattr(result, attr)
                    print(f"      {attr}: {value}")
                else:
                    print(f"      {attr}: NOT FOUND")

# Run the debug
if __name__ == "__main__":
    asyncio.run(debug_results())

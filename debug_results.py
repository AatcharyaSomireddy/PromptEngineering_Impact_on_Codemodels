import sys
sys.path.append("src")
from src.core.benchmark_runner import BenchmarkRunner
import json
import asyncio

async def debug_results():
    # Load your config
    with open("config/research_config.json", "r") as f:
        config = json.load(f)
    
    # Create benchmark runner
    runner = BenchmarkRunner(config)
    
    # Load problems
    problems = runner._load_problem_set("basic")["problems"]
    
    # Build just a few requests for debugging
    requests = runner._build_requests(problems[:1])  # Just first problem
    
    print(f"📊 Found {len(requests)} requests")
    
    # Generate results for debugging
    if len(requests) > 0:
        # Take first request and examine it
        first_request = requests[0]
        print(f"\n🔍 REQUEST OBJECT:")
        print(f"   Type: {type(first_request)}")
        print(f"   Attributes: {dir(first_request)}")
        if hasattr(first_request, '__dict__'):
            print(f"   Data: {first_request.__dict__}")
        
        # Generate one result
        results = await runner.gen.batch_generate(requests[:3])  # Just 3 for debugging
        
        print(f"\n Found {len(results)} results")
        
        for i, result in enumerate(results):
            print(f"\n RESULT {i} OBJECT:")
            print(f"   Type: {type(result)}")
            print(f"   Attributes: {dir(result)}")
            if hasattr(result, '__dict__'):
                print(f"   Data: {result.__dict__}")
            
            # Try to find strategy and model info
            print(f"   Looking for strategy info...")
            for attr in dir(result):
                if 'strategy' in attr.lower() or 'prompt' in attr.lower():
                    value = getattr(result, attr, None)
                    print(f"     {attr}: {value}")
            
            print(f"   Looking for model info...")
            for attr in dir(result):
                if 'model' in attr.lower() or 'generator' in attr.lower():
                    value = getattr(result, attr, None)
                    print(f"     {attr}: {value}")

# Run the debug
asyncio.run(debug_results())

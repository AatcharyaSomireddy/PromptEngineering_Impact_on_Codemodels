import asyncio
import argparse
import yaml
from pathlib import Path
from src.core.benchmark_runner import BenchmarkRunner

async def _main(problem_set: str, cfg: str):
    """Run the benchmark."""
    runner = BenchmarkRunner(cfg)
    await runner.run(problem_set)

def add_custom_prompt():
    """Interactive prompt addition."""
    print("\n=== Add Custom Prompt ===")
    
    name = input("Prompt name: ")
    
    print("Available strategies:", ["basic", "detailed", "step_by_step", "constraint_focused", "pattern_based", "few_shot"])
    strategy = input("Strategy: ")
    
    print("Enter your prompt template:")
    print("Use {problem_description} and {constraints} as placeholders")
    print("Press Enter twice when done:\n")
    
    template_lines = []
    while True:
        line = input()
        if line == "" and len(template_lines) > 0 and template_lines[-1] == "":
            break
        template_lines.append(line)
    
    # Remove the extra empty line at the end
    if template_lines and template_lines[-1] == "":
        template_lines.pop()
    
    template = "\n".join(template_lines)
    
    expected_tokens = input("Expected tokens (default 200): ") or "200"
    complexity = input("Complexity (simple/intermediate/advanced, default intermediate): ") or "intermediate"
    
    # Create prompt data
    new_prompt = {
        "name": name,
        "strategy": strategy,
        "template": template,
        "variables": ["problem_description", "constraints"],
        "expected_tokens": int(expected_tokens),
        "complexity_level": complexity
    }
    
    # Load existing prompts
    yaml_file = Path("config/prompts/combined_prompts.yaml")
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Add new prompt
    data['prompts'].append(new_prompt)
    
    # Save updated file
    with open(yaml_file, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False, indent=2)
    
    print(f"\n✅ Prompt '{name}' added successfully!")
    print("Run 'python main.py --problem-set basic' to test it.")

def main():
    parser = argparse.ArgumentParser(description="Java Code Generation Benchmark")
    parser.add_argument("--problem-set", help="Problem set to run benchmark on")
    parser.add_argument("--config", default="config/benchmark_config.json", help="Config file path")
    parser.add_argument("--add-prompt", action="store_true", help="Add new prompt interactively")
    
    args = parser.parse_args()
    
    if args.add_prompt:
        add_custom_prompt()
        return
    
    if not args.problem_set:
        parser.error("--problem-set is required when not using --add-prompt")
    
    asyncio.run(_main(args.problem_set, args.config))

if __name__ == "__main__":
    main()

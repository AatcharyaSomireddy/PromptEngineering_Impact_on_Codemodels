from src.core.prompt_manager import PromptStrategy

print('Available strategies:')
for strategy in PromptStrategy:
    print(f'  {strategy.name} = {strategy.value}')

# Test specific values
try:
    zero_shot = PromptStrategy("zero_shot")
    print(f'zero_shot works: {zero_shot}')
except ValueError as e:
    print(f'zero_shot error: {e}')

try:
    cot = PromptStrategy("cot")
    print(f'cot works: {cot}')
except ValueError as e:
    print(f'cot error: {e}')

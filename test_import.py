try:
    from src.core.prompt_manager import PromptManager, PromptStrategy
    print("✅ PromptManager imported successfully!")
    print("✅ PromptStrategy imported successfully!")
    
    # Test enum values
    for strategy in PromptStrategy:
        print(f"  - {strategy.name} = {strategy.value}")
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")

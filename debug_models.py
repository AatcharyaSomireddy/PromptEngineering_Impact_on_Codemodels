import sys
import os
sys.path.append(os.getcwd())

print("=== Model Registry Diagnostic ===")

try:
    from src.core.model_registry import MODEL_REGISTRY, create_model
    print(" Model registry imported successfully")
    print(f"Available models: {list(MODEL_REGISTRY.keys())}")
except Exception as e:
    print(f" Registry import failed: {e}")
    exit(1)

print("\n=== Testing Model Creation ===")
for model_name in MODEL_REGISTRY.keys():
    try:
        model = create_model(model_name)
        print(f" {model_name}: Created - {type(model).__name__}")
    except Exception as e:
        print(f" {model_name}: Failed - {e}")

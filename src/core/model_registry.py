"""Model registry for real AI models."""
from src.models.local_stub import LocalStub
from src.models.codet5_small import CodeT5Small
from src.models.starcoder_1b import StarCoder1B

MODEL_REGISTRY = {
    "local-stub": LocalStub,
    "codet5-small": CodeT5Small,
    "starcoder-1b": StarCoder1B
}

def create_model(model_name, settings=None):
    """Create a model instance by name."""
    if model_name in MODEL_REGISTRY:
        return MODEL_REGISTRY[model_name](settings)
    else:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_REGISTRY.keys())}")

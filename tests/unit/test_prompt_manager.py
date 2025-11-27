from src.core.prompt_manager import PromptManager, PromptStrategy

def test_load():
    pm = PromptManager("config/prompts/basic_prompts.yaml")
    assert "basic_java_generation" in pm.prompts
    assert PromptStrategy.BASIC in pm.list_strategies()

import asyncio
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, Any

class StarCoder1B:
    def __init__(self, settings=None):
        self.settings = settings or {}
        # FIXED: Use correct model name that exists
        self.model_name = "bigcode/tiny_starcoder"
        self.model = None
        self.tokenizer = None
        
    def _load_model(self):
        if self.model is None:
            print(f"Loading {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                trust_remote_code=True
            )
            self.model.eval()
            
    async def generate_code(self, prompt: str, **kwargs) -> str:
        try:
            self._load_model()
            
            # Better prompt format for StarCoder
            formatted_prompt = f"// Task: {prompt}\n// Solution:\n"
            
            inputs = self.tokenizer(
                formatted_prompt, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True
            )
                
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=kwargs.get('max_tokens', 200),
                    temperature=kwargs.get('temperature', 0.7),
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode only new tokens
            generated_tokens = outputs[0][inputs['input_ids'].shape[1]:]
            generated_code = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            return generated_code.strip() if generated_code.strip() else "// Could not generate valid code"
            
        except Exception as e:
            return f"// Error generating code: {str(e)}"
    
    async def close(self):
        if self.model is not None:
            del self.model
            del self.tokenizer

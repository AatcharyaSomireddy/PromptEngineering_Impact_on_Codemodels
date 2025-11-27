import asyncio
import torch
from transformers import T5ForConditionalGeneration, AutoTokenizer
from typing import Dict, Any

class CodeT5Small:
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.model_name = "Salesforce/codet5-small"
        self.model = None
        self.tokenizer = None
        
    def _load_model(self):
        if self.model is None:
            print(f"Loading {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            self.model.eval()
            
    async def generate_code(self, prompt: str, **kwargs) -> str:
        try:
            self._load_model()
            
            # Better prompt format for CodeT5
            formatted_prompt = f"translate English to Java: {prompt}"
            
            inputs = self.tokenizer(
                formatted_prompt, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True,
                padding=True
            )
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=kwargs.get('max_tokens', 200),
                    temperature=kwargs.get('temperature', 0.7),
                    do_sample=True,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            generated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up the output
            if "translate English to Java:" in generated_code:
                generated_code = generated_code.replace("translate English to Java:", "").strip()
                
            return generated_code if generated_code else "// Could not generate valid code"
            
        except Exception as e:
            return f"// Error generating code: {str(e)}"
    
    async def close(self):
        if self.model is not None:
            del self.model
            del self.tokenizer

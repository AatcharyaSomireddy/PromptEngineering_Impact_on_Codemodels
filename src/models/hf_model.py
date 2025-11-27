import torch, asyncio, random, transformers
from dataclasses import dataclass

@dataclass
class HFSettings:
    repo: str            # e.g. "Salesforce/codegen-350M-mono"
    max_new_tokens: int = 256
    temperature: float = 0.2
    device: str = "auto"  # "cuda" | "cpu" | "auto"

class HuggingFaceModel:
    """
    Thin wrapper so the rest of the pipeline can call generate_code().
    """

    def __init__(self, cfg: HFSettings):
        self.cfg = cfg
        device = "cuda" if cfg.device == "auto" and torch.cuda.is_available() else "cpu"
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(cfg.repo)
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            cfg.repo,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            low_cpu_mem_usage=True,
        ).to(device)
        self.device = device

    async def generate_code(self, prompt: str, max_tokens: int, temperature: float):
        # run in a thread so we don't block the asyncio loop
        loop = asyncio.get_event_loop()
        output = await loop.run_in_executor(
            None,
            self._sync_generate,
            prompt,
            max_tokens,
            temperature,
        )
        return output

    def _sync_generate(self, prompt, max_tokens, temperature):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                do_sample=True,
                max_new_tokens=max_tokens,
                temperature=temperature,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        full = self.tokenizer.decode(out[0], skip_special_tokens=True)
        # take only the new portion
        generated = full[len(prompt):].strip()
        return {"code": generated, "token_count": len(out)}

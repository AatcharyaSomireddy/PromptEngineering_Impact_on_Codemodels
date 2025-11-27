# src/core/benchmark_runner.py
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from src.core.prompt_manager     import PromptManager
from src.core.code_generator     import CodeGenerator, GenerationRequest
from src.utils.logger            import Logger
from src.utils.report_generator  import ReportGenerator

# -- model clients -------------------------------------------------
from src.models.local_stub       import LocalStub
from src.models.codet5_small     import CodeT5Small
from src.models.starcoder_1b     import StarCoder1B

from src.models.hf_model         import HuggingFaceModel, HFSettings
# Uncomment if/when you want to use OpenAI again
# from src.models.openai_client    import OpenAIClient

logger = Logger().get()


class BenchmarkRunner:
    def __init__(self, cfg_path: str):
        # ------------------------------------------------------------------
        # load benchmark-level config
        # ------------------------------------------------------------------
        with open(cfg_path, "r", encoding="utf-8") as f:
            self.cfg: Dict = json.load(f)

        # ------------------------------------------------------------------
        # prompt templates
        # ------------------------------------------------------------------
        self.prompt_mgr = PromptManager(self.cfg["prompts_path"])

        # ------------------------------------------------------------------
        # model clients dictionary
        # keys must match names in config["models"]
        # ------------------------------------------------------------------
        self.gen = CodeGenerator(
    {
       "local-stub":   LocalStub(),
    "codet5-small": CodeT5Small(),
    "starcoder-1b": StarCoder1B(),
    "codegen-350m": HuggingFaceModel(HFSettings("Salesforce/codegen-350M-mono")),
    }
)


        self.reporter = ReportGenerator()

    # ----------------------------------------------------------------------
    # helpers
    # ----------------------------------------------------------------------
    def _load_problem_set(self, name: str):
        path = Path(f"data/input/problem_sets/{name}.json")
        return json.loads(path.read_text(encoding="utf-8"))

    def _build_requests(self, problems) -> List[GenerationRequest]:
        reqs: List[GenerationRequest] = []
        for pb in problems:
            for strat in self.prompt_mgr.list_strategies():
                for tmpl in self.prompt_mgr.get_prompts_by_strategy(strat):
                    prompt = self.prompt_mgr.get_prompt(
                        tmpl.name,
                        problem_description=pb["description"],
                        constraints=pb.get("constraints", ""),
                        example_input=pb.get("example_input", ""),
                        example_output=pb.get("example_output", ""),
                    )
                    for model in self.cfg["models"]:
                        reqs.append(
                            GenerationRequest(
                                prompt=prompt,
                                strategy=strat.value,
                                problem_id=pb["id"],
                                model_name=model,
                            )
                        )
        return reqs

    # ----------------------------------------------------------------------
    # public API
    # ----------------------------------------------------------------------
    async def run(self, set_name: str):
        problems  = self._load_problem_set(set_name)["problems"]
        requests  = self._build_requests(problems)
        logger.info("Total requests %d", len(requests))

        results   = await self.gen.batch_generate(requests)

        ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path  = Path(f"data/results/{set_name}_{ts}.json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps([r.__dict__ for r in results], default=str, indent=2),
            encoding="utf-8",
        )
        logger.info("Saved raw results to %s", out_path)

        self.reporter.generate_comprehensive_report(results, set_name)

Prompt Engineering Impact on Generative Code Models
End-to-end benchmark to study how different prompt strategies affect Java code generation quality, speed, and token usage for open‑source code LLMs (StarCoder‑1B, CodeT5‑Small).

🚀 Features
Multiple prompt strategies:

Zero‑Shot

Chain‑of‑Thought (CoT)

Persona‑Based

Few‑Shot

Template‑Based

Multiple Java coding problems (recursion, trees, graphs, caching, matrix operations, etc.).

Supports open‑source models (e.g., bigcode/starcoder, Salesforce/codet5-small).

Automatic:

Experiment orchestration (problem × model × strategy)

Execution time measurement

Token counting

Aggregated CSV reports

Publication‑ready charts (bar plots + heatmaps)

Reproducible, configuration‑driven design (JSON/YAML).

📂 Project Structure
.
├── config/
│ ├── ai_models_only.json – which models + strategies to run
│ └── problems_config.json – which problem set to use
├── problems/
│ └── *.json – problem descriptions + constraints
├── src/
│ ├── core/
│ │ ├── benchmark_runner.py – main experiment loop
│ │ ├── prompt_manager.py – prompt templates and strategies
│ │ └── model_interface.py – StarCoder / CodeT5 wrappers
│ ├── utils/
│ │ ├── results_io.py – CSV/JSON read–write
│ │ ├── visualization.py – plots (bar charts, heatmaps)
│ │ └── reporting.py – text summary (key insights)
├── outputs/
│ ├── csv/ – raw metrics per run
│ ├── figures/ – PNG charts for each problem
│ └── reports/ – text summaries
├── main.py – CLI entry point for running benchmarks
└── README.md

(Adjust names/paths to match your actual repo.)

✅ Requirements
Python 3.10+

A GPU is recommended (but small runs can work on CPU).

Typical Python dependencies:

pip install -r requirements.txt

Example requirements.txt:

torch
transformers
accelerate
datasets
pandas
numpy
matplotlib
seaborn
pyyaml
tqdm

⚙️ Quick Start
Clone the repository

git clone https://github.com/<your-username>/prompt-engineering-java-benchmark.git
cd prompt-engineering-java-benchmark

Install dependencies

pip install -r requirements.txt

Configure models and strategies

Edit config/ai_models_only.json (example):

{
"models": ["starcoder-1b", "codet5-small"],
"strategies": ["zero_shot", "cot", "persona", "few_shot", "template"],
"problem_set": "algorithms_all",
"max_concurrent_requests": 1
}

Run the benchmark

python main.py --problem-set algorithms_all --config config/ai_models_only.json

View results

Raw metrics: outputs/csv/

Charts (per problem): outputs/figures/

Text summaries: outputs/reports/

🧠 Prompt Strategies
All strategies are implemented as reusable templates in src/core/prompt_manager.py:

Zero‑Shot – minimal prompt with only the problem description and constraints.

Chain‑of‑Thought (CoT) – step‑by‑step reasoning instructions before requesting code.

Persona‑Based – model acts as a senior Java developer producing clean, efficient code.

Few‑Shot – 2–3 example problem–solution pairs before the target problem.

Template‑Based – Java skeleton with TODO comments for the model to fill in.

You can modify or add strategies by editing templates in prompt_manager.py.

🧪 Evaluation Metrics
For each (problem, model, strategy) combination, the framework records:

Generation time (seconds) – latency from prompt to code completion

Token count – number of output tokens (verbosity / potential API cost)

Generation success – whether the model produced a non‑empty output without errors

Aggregated statistics – per‑strategy and per‑model averages, plus performance range

These metrics are stored in CSV files and used to generate:

Strategy performance bar charts (lower time is better)

Model performance bar charts

Token efficiency bar charts (lower tokens is better)

Model × strategy heatmaps (execution time encoded as color)

📊 Example Command and Output
python main.py --problem-set bst_problems --config config/ai_models_only.json

Produces, for example:

outputs/csv/bst_problems_metrics.csv

outputs/figures/bst_problems_strategy_performance.png

outputs/figures/bst_problems_model_vs_strategy_heatmap.png

outputs/reports/bst_problems_summary.txt

Each summary report typically includes:

Fastest strategy

Fastest model

Most token‑efficient strategy

Overall generation success rate

Performance range between best and worst combinations

🔧 Configuration
Main CLI options:

python main.py
--problem-set <name>
--config config/ai_models_only.json
--out-dir outputs/

Key config fields:

models – list of model IDs (Hugging Face names or local aliases)

strategies – list of strategy identifiers (must match enum/keys in code)

problem_set – which logical problem group to run (must exist in problem config)

max_concurrent_requests – concurrency limit (1 recommended for stable timing)

📚 Extending the Benchmark
Add a new problem:

Create a JSON file in problems/, e.g. problems/valid_parentheses.json:

{
"id": "valid_parentheses",
"title": "Valid Parentheses",
"description": "Check if a string of brackets is valid.",
"constraints": "Only characters '()[]{}'; return boolean.",
"examples": [
{ "input": ""()[]{}"", "output": "true" },
{ "input": ""(]"", "output": "false" }
]
}

Register it in config/problems_config.json under the appropriate problem set.

Add a new model:

Implement or reuse a wrapper in src/core/model_interface.py.

Add the model name to the models list in your config file.

Add a new strategy:

Define a new strategy template in src/core/prompt_manager.py.

Add its name to the strategy enum/strategy registry.

Reference it in your configuration file under strategies.

🧾 Academic Use and Citation
If you use this benchmark in academic work, please cite:

Aatcharya Somireddy,Thotamsetty Sreehitha, Srirangam Varshitha, “Empirical Evaluation of Prompt Engineering Strategies for Open‑Source Neural Code Generation Models,” 2025.

(Adjust citation details once your paper is published.)




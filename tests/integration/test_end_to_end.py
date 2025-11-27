import asyncio
from src.core.benchmark_runner import BenchmarkRunner

async def test_small_run():
    runner = BenchmarkRunner("config/benchmark_config.json")
    await runner.run("basic")

def test_async():
    asyncio.run(test_small_run())

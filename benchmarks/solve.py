"""Run this file like python benchmarks/solve.py

It will print out results to the console and open web browser windows.
"""
import anyio
from pyinstrument.profiler import Profiler  # type: ignore[import]

from benchmarks.utils import GraphSize, SleepTimes, generate_dag
from di import Container, Dependant
from di.executors import ConcurrentAsyncExecutor, SyncExecutor

INTERVAL = 10e-6  # 10 us


async def async_bench(sleep: SleepTimes, graph: GraphSize, iters: int) -> None:
    container = Container()
    solved = container.solve(Dependant(generate_dag(graph, sync=False, sleep=sleep)))
    executor = ConcurrentAsyncExecutor()
    p = Profiler()
    async with container.enter_scope(None):
        await container.execute_async(solved, executor=executor)
    p.start()
    for _ in range(iters):
        async with container.enter_scope(None):
            await container.execute_async(solved, executor=executor)
    p.stop()
    p.print()
    p.open_in_browser()


def sync_bench(sleep: SleepTimes, graph: GraphSize, iters: int) -> None:
    container = Container()
    solved = container.solve(Dependant(generate_dag(graph, sync=True, sleep=sleep)))
    executor = SyncExecutor()
    p = Profiler()
    with container.enter_scope(None):
        container.execute_sync(solved, executor=executor)
    p.start()
    for _ in range(iters):
        with container.enter_scope(None):
            container.execute_sync(solved, executor=executor)
    p.stop()
    p.print()
    p.open_in_browser()


LARGE_GRAPH = GraphSize(25, 5, 5)
SMALL_GRAPH = GraphSize(1, 1, 1)
FAST_DEPS = SleepTimes(0, 0)
SLOW_DEPS = SleepTimes(1e-3, 1e-3)


if __name__ == "__main__":
    anyio.run(async_bench, FAST_DEPS, SMALL_GRAPH, 1_000)
    anyio.run(async_bench, FAST_DEPS, LARGE_GRAPH, 1_000)
    anyio.run(async_bench, SLOW_DEPS, SMALL_GRAPH, 1_000)
    anyio.run(async_bench, SLOW_DEPS, LARGE_GRAPH, 100)
    sync_bench(FAST_DEPS, SMALL_GRAPH, iters=1_000)
    sync_bench(FAST_DEPS, LARGE_GRAPH, iters=1_000)
    sync_bench(SLOW_DEPS, SMALL_GRAPH, iters=1_000)
    sync_bench(SLOW_DEPS, LARGE_GRAPH, iters=10)

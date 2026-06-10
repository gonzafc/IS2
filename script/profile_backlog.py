"""Profile backlog planning operations and write a simple report.

Usage: python script/profile_backlog.py path/to/backlog.json
"""
import cProfile
import pstats
import sys
from pathlib import Path
from backlog_calculator import load_backlog, select_plan, compute_score


def profile(path: str, out_path: str = "profile_stats.txt") -> None:
    data = load_backlog(path)
    items = data["items"]
    budget = data["budget"]

    profiler = cProfile.Profile()
    profiler.enable()
    # Workload: compute scores and plan several times to get stable measurements
    for _ in range(50):
        _ = {it.id: compute_score(it) for it in items}
        _ = select_plan(items, budget)
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats("cumtime")
    with open(out_path, "w", encoding="utf-8") as f:
        stats.stream = f
        stats.print_stats(50)

    print(f"Profile written to: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: profile_backlog.py path/to/backlog.json")
        sys.exit(2)
    profile(sys.argv[1])

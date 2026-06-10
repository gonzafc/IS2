"""Refactored backlog calculator module.

Implements a safe, testable API and CLI entrypoint. Based on CONTEXT.md requirements:
- No mutable globals
- JSON parsing only
- Dataclass for items
- Pure functions for scoring and planning
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
import argparse


@dataclass(frozen=True)
class BacklogItem:
    id: str
    value: float
    effort: float
    risk: float
    deps: List[str]


def parse_deps(raw: Any) -> List[str]:
    """Normalize dependencies field into a list of strings."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    if isinstance(raw, str):
        return [p.strip() for p in raw.split(",") if p.strip()]
    return [str(raw)]


def load_backlog(path: str) -> Dict[str, Any]:
    """Load backlog JSON file and return budget and list of BacklogItem.

    Expected JSON structure:
    {"budget": 10, "items": [{"id": "A", "value": 5, "effort": 2, "risk": 1, "deps": "B"}, ...]}
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    budget = float(data.get("budget", 0))
    items_raw = data.get("items", [])
    items: List[BacklogItem] = []
    for it in items_raw:
        items.append(
            BacklogItem(
                id=str(it.get("id")),
                value=float(it.get("value", 0)),
                effort=float(it.get("effort", 1)),
                risk=float(it.get("risk", 0)),
                deps=parse_deps(it.get("deps", [])),
            )
        )
    return {"budget": budget, "items": items}


def compute_score(item: BacklogItem) -> float:
    """Compute priority score for an item.

    Formula preserved from legacy: (value + value * risk / 10) / effort
    Items with zero effort are considered highest priority (represented by +inf).
    A penalty of 2.0 per dependency is applied.
    """
    try:
        if item.effort == 0:
            base = float("inf")
        else:
            base = (item.value + (item.value * item.risk / 10.0)) / item.effort
        penalty = 2.0 * len(item.deps)
        if base == float("inf"):
            return base
        return base - penalty
    except Exception:
        return float("-inf")


def select_plan(items: List[BacklogItem], budget: float) -> List[BacklogItem]:
    """Greedy planner: sort by score descending, pick items whose deps are satisfied and fit the budget."""
    scored = sorted(items, key=compute_score, reverse=True)
    chosen: List[BacklogItem] = []
    spent = 0.0
    chosen_ids = set()

    for it in scored:
        if not all(d in chosen_ids for d in it.deps):
            continue
        if spent + it.effort <= budget:
            chosen.append(it)
            chosen_ids.add(it.id)
            spent += it.effort
    return chosen


def plan_from_file(path: str) -> List[Dict[str, Any]]:
    """Convenience API: load file and return serializable plan with original short keys."""
    data = load_backlog(path)
    budget = data["budget"]
    items: List[BacklogItem] = data["items"]
    plan_items = select_plan(items, budget)
    return [
        {
            "id": it.id,
            "v": it.value,
            "e": it.effort,
            "r": it.risk,
            "d": ",".join(it.deps),
        }
        for it in plan_items
    ]


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Calculate backlog plan within a budget"
    )
    parser.add_argument("path", help="Path to backlog JSON file")
    args = parser.parse_args(argv)

    plan = plan_from_file(args.path)
    print(json.dumps(plan, ensure_ascii=False))


if __name__ == "__main__":
    main()

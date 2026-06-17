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
import sys
from json import JSONDecodeError


@dataclass(frozen=True)
class BacklogItem:
    """Representación inmutable de un ítem del backlog.

    Atributos:
        id: Identificador del ítem.
        value: Valor estimado del ítem.
        effort: Esfuerzo estimado (unidades de capacidad).
        risk: Riesgo estimado (escala 0..n).
        deps: Lista de ids de ítems de los que depende.

    """

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


def load_backlog(path: Optional[str]) -> Dict[str, Any]:
    """Load backlog JSON from a file or stdin and return budget and list of BacklogItem.

    If path is None or '-' the JSON is read from stdin. Expected JSON structure:
    {"budget": 10, "items": [{"id": "A", "value": 5, "effort": 2, "risk": 1, "deps": "B"}, ...]}
    """
    try:
        if path is None or path == "-":
            # Read JSON from stdin
            raw = sys.stdin.read()
            data = json.loads(raw)
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
    except FileNotFoundError as e:
        raise ValueError(f"Backlog file not found: {path}") from e
    except JSONDecodeError as e:
        source = "stdin" if path in (None, "-") else path
        raise ValueError(f"Backlog file is not valid JSON: {source}") from e

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
    """Greedy planner optimized: compute scores once and sort using them.

    This reduces repeated score calculations when the scoring function is
    non-trivial. Maintains the same selection logic (deps must be satisfied)
    and budget constraint.
    """
    # Precompute scores to avoid repeated computation
    scores = {it.id: compute_score(it) for it in items}
    # Sort items by precomputed score (fall back to id for stability)
    scored = sorted(
        items, key=lambda it: (scores.get(it.id, float("-inf")), it.id), reverse=True
    )

    chosen: List[BacklogItem] = []
    spent = 0.0
    chosen_ids = set()

    for it in scored:
        # Fast dependency check using set
        if not all(d in chosen_ids for d in it.deps):
            continue
        if spent + it.effort <= budget:
            chosen.append(it)
            chosen_ids.add(it.id)
            spent += it.effort
    return chosen


def plan_from_file(path: str) -> List[Dict[str, Any]]:
    """Load a file and return a serializable plan with original short keys.

    This is a convenience wrapper that delegates to load_backlog and select_plan.
    """
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
    """CLI entrypoint.

    Parse arguments from argv (or sys.argv when None) and print JSON plan to stdout.
    Errors are reported to stderr and the process exits with a non-zero code.
    """
    parser = argparse.ArgumentParser(
        description="Calculate backlog plan within a budget"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="-",
        help="Path to backlog JSON file or '-' to read JSON from stdin",
    )
    args = parser.parse_args(argv)

    # If the user requested stdin ('-' default) but nothing is piped, avoid blocking.
    if args.path == "-" and sys.stdin.isatty():
        parser.print_help()
        print(
            "\nNo input detected on stdin. Provide a file path or pipe JSON and use '-'.",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        # plan_from_file delegates to load_backlog which now supports stdin when path is '-'
        plan = plan_from_file(args.path)
        print(json.dumps(plan, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

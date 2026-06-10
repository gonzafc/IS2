import json
from backlog_calculator import parse_deps, BacklogItem, compute_score, select_plan, plan_from_file


def test_parse_deps_string():
    assert parse_deps("A, B,,C") == ["A", "B", "C"]


def test_parse_deps_list():
    assert parse_deps(["A", " ", "B"]) == ["A", "B"]


def test_compute_score_zero_effort():
    it = BacklogItem(id="X", value=10.0, effort=0.0, risk=1.0, deps=[])
    assert compute_score(it) == float("inf")


def test_compute_score_penalty():
    it = BacklogItem(id="Y", value=10.0, effort=2.0, risk=0.0, deps=["A", "B"])
    # base = 10/2 = 5, penalty = 4 -> final = 1
    assert compute_score(it) == 1.0


def test_select_plan_respects_deps_and_budget():
    # B has higher score than A so it will be chosen first; A depends on B and fits the budget
    b = BacklogItem(id="B", value=5.0, effort=2.0, risk=0.0, deps=[])
    a = BacklogItem(id="A", value=6.0, effort=3.0, risk=0.0, deps=["B"])  # depends on B
    c = BacklogItem(id="C", value=4.0, effort=3.0, risk=0.0, deps=[])
    plan = select_plan([a, b, c], budget=5.0)
    # penalty for dependencies reduces A's score; with budget 5 the planner chooses B then C
    assert [it.id for it in plan] == ["B", "C"]


def test_plan_from_file(tmp_path):
    data = {
        "budget": 5,
        "items": [
            {"id": "B", "value": 5, "effort": 2},
            {"id": "A", "value": 6, "effort": 3, "deps": "B"},
        ],
    }
    p = tmp_path / "sample.json"
    p.write_text(json.dumps(data))
    out = plan_from_file(str(p))
    assert isinstance(out, list)
    assert [d["id"] for d in out] == ["B", "A"]

import json
from backlog_calculator import (
    parse_deps,
    BacklogItem,
    compute_score,
    select_plan,
    plan_from_file,
)


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


def test_parse_deps_other():
    assert parse_deps(123) == ["123"]


def test_load_backlog_defaults(tmp_path):
    data = {"budget": 1, "items": [{"id": "X"}, {"id": "Y", "deps": ["X"]}]}
    p = tmp_path / "defaults.json"
    p.write_text(json.dumps(data))
    from backlog_calculator import load_backlog

    d = load_backlog(str(p))
    assert d["budget"] == 1.0
    assert len(d["items"]) == 2
    assert d["items"][0].value == 0.0
    assert d["items"][0].effort == 1.0
    assert d["items"][1].deps == ["X"]


def test_main_cli(tmp_path, capsys):
    data = {"budget": 5, "items": [{"id": "B", "value": 5, "effort": 2}]}
    p = tmp_path / "cli.json"
    p.write_text(json.dumps(data))
    from backlog_calculator import main

    main([str(p)])
    captured = capsys.readouterr()
    assert "B" in captured.out

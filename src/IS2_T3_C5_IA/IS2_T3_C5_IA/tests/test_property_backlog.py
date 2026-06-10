from hypothesis import given, strategies as st
from backlog_calculator import BacklogItem, compute_score, select_plan


@st.composite
def backlog_items(draw):
    id_ = draw(st.text(min_size=1, max_size=3))
    value = draw(st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False))
    effort = draw(st.floats(min_value=0, max_value=20, allow_nan=False, allow_infinity=False))
    risk = draw(st.floats(min_value=0, max_value=10, allow_nan=False, allow_infinity=False))
    deps = draw(st.lists(st.text(min_size=1, max_size=3), max_size=3))
    return BacklogItem(id=id_, value=value, effort=effort, risk=risk, deps=deps)


@given(st.lists(backlog_items(), min_size=1, max_size=6), st.floats(min_value=0, max_value=50))
def test_select_plan_budget_and_deps(items, budget):
    # plan must not exceed budget
    plan = select_plan(items, budget)
    total_effort = sum(it.effort for it in plan)
    assert total_effort <= budget + 1e-6
    # every chosen item's deps must be subset of chosen ids
    chosen_ids = {it.id for it in plan}
    for it in plan:
        assert set(it.deps).issubset(chosen_ids)


@given(backlog_items())
def test_compute_score_finite_or_inf(item):
    s = compute_score(item)
    assert s == float("inf") or isinstance(s, float)

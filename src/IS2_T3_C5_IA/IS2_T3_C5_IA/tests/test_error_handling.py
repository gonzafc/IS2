import pytest
from backlog_calculator import load_backlog, main


def test_load_backlog_invalid_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("not a json")
    with pytest.raises(ValueError):
        load_backlog(str(p))


def test_main_invalid_json_exits_nonzero(tmp_path, capsys):
    p = tmp_path / "bad.json"
    p.write_text("not a json")
    with pytest.raises(SystemExit) as exc:
        main([str(p)])
    assert exc.value.code == 1

import json
from pathlib import Path

from seed.context import Context, load_context


def test_load_context(tmp_path):
    context = Context({"keep": "yes", "overwrite": "old"})
    json_data = {"overwrite": "new", "added": 123}
    json_file: Path = tmp_path / "context.json"
    json_file.write_text(json.dumps(json_data), encoding="utf-8")

    load_context(json_file, context)  # act

    assert context["keep"] == "yes"
    assert context["overwrite"] == "new"
    assert context["added"] == 123

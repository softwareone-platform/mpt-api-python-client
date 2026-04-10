from mpt_api_client.http.query_options import QueryOptions


def test_default_options() -> None:
    result = QueryOptions()

    assert result.render is False


def test_render_true() -> None:
    result = QueryOptions(render=True)

    assert result.render is True

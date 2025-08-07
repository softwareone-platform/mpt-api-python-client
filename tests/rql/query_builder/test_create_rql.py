from mpt_api_client.rql.query_builder import RQLQuery


def test_create():
    query = RQLQuery()

    assert query.op == RQLQuery.EXPRESSION
    assert query.children == []
    assert query.negated is False


def test_create_with_field():
    query = RQLQuery("field")

    query.eq("value")

    assert query.op == RQLQuery.EXPRESSION
    assert str(query) == "eq(field,value)"


def test_create_single_kwarg():
    query = RQLQuery(id="ID")

    assert query.op == RQLQuery.EXPRESSION
    assert str(query) == "eq(id,ID)"
    assert query.children == []
    assert query.negated is False


def test_create_multiple_kwargs():  # noqa: WPS218
    query = RQLQuery(id="ID", status__in=("a", "b"), ok=True)

    assert query.op == RQLQuery.AND
    assert str(query) == "and(eq(id,ID),in(status,(a,b)),eq(ok,true))"
    assert len(query.children) == 3
    assert query.children[0].op == RQLQuery.EXPRESSION
    assert query.children[0].children == []
    assert str(query.children[0]) == "eq(id,ID)"
    assert query.children[1].op == RQLQuery.EXPRESSION
    assert query.children[1].children == []
    assert str(query.children[1]) == "in(status,(a,b))"
    assert query.children[2].op == RQLQuery.EXPRESSION
    assert query.children[2].children == []
    assert str(query.children[2]) == "eq(ok,true)"


def test_new_empty():
    query = RQLQuery.new()

    assert query.op == RQLQuery.EXPRESSION
    assert query.children == []
    assert query.negated is False


def test_new_with_parameters():
    project_rql = RQLQuery.new("project=rql")
    status_not_done = RQLQuery.new("status=done", negated=True)

    query = RQLQuery.new(
        op=RQLQuery.AND,
        children=[project_rql, status_not_done],
    )

    assert str(query) == "and(project=rql,not(status=done))"


def test_new_with_set():
    project_rql = RQLQuery.new("project=rql")
    status_not_done = RQLQuery.new("status=done", negated=True)

    query = RQLQuery.new(
        op=RQLQuery.AND,
        children={project_rql, status_not_done},
    )

    assert isinstance(query.children, list)
    assert len(query.children) == 2
    assert project_rql in query.children
    assert status_not_done in query.children

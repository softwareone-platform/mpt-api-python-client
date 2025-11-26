from mpt_api_client.rql.query_builder import RQLQuery


def test_create():
    result = RQLQuery()

    assert result.op == RQLQuery.OP_EXPRESSION
    assert result.children == []
    assert result.negated is False


def test_create_with_field():
    query = RQLQuery("field")

    query.eq("value")  # act

    assert query.op == RQLQuery.OP_EXPRESSION
    assert str(query) == "eq(field,value)"


def test_create_single_kwarg():
    result = RQLQuery(id="ID")

    assert result.op == RQLQuery.OP_EXPRESSION
    assert str(result) == "eq(id,ID)"
    assert result.children == []
    assert result.negated is False


def test_create_multiple_kwargs():  # noqa: WPS218
    result = RQLQuery(id="ID", status__in=("a", "b"), ok=True)

    assert result.op == RQLQuery.OP_AND
    assert str(result) == "and(eq(id,ID),in(status,(a,b)),eq(ok,true))"
    assert len(result.children) == 3
    assert result.children[0].op == RQLQuery.OP_EXPRESSION
    assert result.children[0].children == []
    assert str(result.children[0]) == "eq(id,ID)"
    assert result.children[1].op == RQLQuery.OP_EXPRESSION
    assert result.children[1].children == []
    assert str(result.children[1]) == "in(status,(a,b))"
    assert result.children[2].op == RQLQuery.OP_EXPRESSION
    assert result.children[2].children == []
    assert str(result.children[2]) == "eq(ok,true)"


def test_new_empty():
    result = RQLQuery.new()

    assert result.op == RQLQuery.OP_EXPRESSION
    assert result.children == []
    assert result.negated is False


def test_new_with_parameters():
    project_rql = RQLQuery.new("project=rql")
    status_not_done = RQLQuery.new("status=done", negated=True)

    result = RQLQuery.new(op=RQLQuery.OP_AND, children=[project_rql, status_not_done])

    assert str(result) == "and(project=rql,not(status=done))"


def test_new_with_set():
    project_rql = RQLQuery.new("project=rql")
    status_not_done = RQLQuery.new("status=done", negated=True)

    result = RQLQuery.new(op=RQLQuery.OP_AND, children={project_rql, status_not_done})

    assert isinstance(result.children, list)
    assert len(result.children) == 2
    assert project_rql in result.children
    assert status_not_done in result.children

import pytest

from seed.context import Context
from seed.helper import ResourceRequiredError, init_resource, require_context_id


def test_require_context_id_returns_value():
    context = Context()
    context["catalog.product.id"] = "prod-123"

    result = require_context_id(context, "catalog.product.id", "creating product")

    assert result == "prod-123"


def test_require_context_id_raises_when_missing():
    context = Context()
    key = "catalog.product.id"
    action = "creating product"

    with pytest.raises(ResourceRequiredError) as exc_info:
        require_context_id(context, key, action)

    assert exc_info.value.key == key
    assert exc_info.value.action == action
    assert exc_info.value.context is context
    assert str(exc_info.value) == f"Missing required resource '{key}' before {action}."


async def test_init_resource_existing_id(mocker):
    context = Context()
    context["catalog.product.id"] = "prod-123"
    factory = mocker.AsyncMock()

    result = await init_resource("catalog.product.id", factory, context)

    assert result == "prod-123"
    factory.assert_not_called()


async def test_init_resource_creates(mocker):
    context = Context()
    resource = mocker.Mock(id="new-456")
    factory = mocker.AsyncMock(return_value=resource)

    result = await init_resource("catalog.product.id", factory, context)

    assert result == "new-456"
    factory.assert_awaited_once()
    assert context.get_string("catalog.product.id") == "new-456"

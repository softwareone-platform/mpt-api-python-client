from mpt_api_client.resources.catalog.products_parameters import Parameter


def test_parameter_properties_getters():  # noqa: WPS218
    parameter_data = {
        "id": "PAR-1",
        "scope": "Order",
        "phase": "Order",
        "context": "Purchase",
        "options": {"label": "Email"},
        "multiple": True,
        "constraints": {"required": True},
        "group": {"id": "GRP-1"},
        "externalId": "ext-1",
        "status": "Active",
    }

    result = Parameter(parameter_data)

    assert result.id == "PAR-1"
    assert result.scope == "Order"
    assert result.phase == "Order"
    assert result.context == "Purchase"
    assert result.options == {"label": "Email"}
    assert result.multiple is True
    assert result.constraints == {"required": True}
    assert result.group == {"id": "GRP-1"}
    assert result.external_id == "ext-1"
    assert result.status == "Active"


def test_parameter_properties_setters():  # noqa: WPS218
    parameter = Parameter()
    parameter.scope = "Agreement"
    parameter.phase = "Configuration"
    parameter.context = "None"
    parameter.type_ = "Text"
    parameter.options = {"label": "Name"}
    parameter.multiple = False
    parameter.constraints = {"required": False}
    parameter.group = {"id": "GRP-2"}
    parameter.external_id = "ext-2"
    parameter.status = "Inactive"

    result = parameter

    assert result.scope == "Agreement"
    assert result.phase == "Configuration"
    assert result.context == "None"
    assert result.type_ == "Text"
    assert result.options == {"label": "Name"}
    assert result.multiple is False
    assert result.constraints == {"required": False}
    assert result.group == {"id": "GRP-2"}
    assert result.external_id == "ext-2"
    assert result.status == "Inactive"
    result_dict = result.to_dict()
    assert result_dict["scope"] == "Agreement"
    assert result_dict["externalId"] == "ext-2"
    assert result_dict["scope"] == "Agreement"
    assert result_dict["externalId"] == "ext-2"


def test_parameter_default_values():  # noqa: WPS218
    result = Parameter()

    assert not result.id
    assert not result.scope
    assert not result.phase
    assert not result.context
    assert result.options == {}
    assert result.multiple is False
    assert result.constraints == {}
    assert result.group == {}
    assert not result.external_id
    assert not result.status

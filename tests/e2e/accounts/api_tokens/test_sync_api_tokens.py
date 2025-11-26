import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_api_token(mpt_vendor, api_token_factory):
    new_api_token_request_data = api_token_factory()
    created_api_token = mpt_vendor.accounts.api_tokens.create(new_api_token_request_data)

    yield created_api_token

    try:
        mpt_vendor.accounts.api_tokens.delete(created_api_token.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete api token: {error.title}")  # noqa: WPS421


def test_get_api_token_by_id(mpt_vendor, api_token_id):
    result = mpt_vendor.accounts.api_tokens.get(api_token_id)

    assert result is not None


def test_list_api_tokens(mpt_vendor):
    limit = 10

    result = mpt_vendor.accounts.api_tokens.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_api_token_by_id_not_found(mpt_vendor, invalid_api_token_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_vendor.accounts.api_tokens.get(invalid_api_token_id)


def test_filter_api_tokens(mpt_vendor, api_token_id):
    select_fields = ["-name"]
    filtered_api_tokens = (
        mpt_vendor.accounts.api_tokens.filter(RQLQuery(id=api_token_id))
        .filter(RQLQuery(name="E2E Seeded Token"))
        .select(*select_fields)
    )

    result = list(filtered_api_tokens.iterate())

    assert len(result) == 1


def test_create_api_token(created_api_token):
    result = created_api_token

    assert result is not None


def test_delete_api_token(mpt_vendor, created_api_token):
    mpt_vendor.accounts.api_tokens.delete(created_api_token.id)  # act


def test_delete_api_token_not_found(mpt_vendor, invalid_api_token_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_vendor.accounts.api_tokens.delete(invalid_api_token_id)


def test_update_api_token(mpt_vendor, api_token_factory, created_api_token):
    updated_api_token_data = api_token_factory(name="E2E Updated API Token")

    result = mpt_vendor.accounts.api_tokens.update(created_api_token.id, updated_api_token_data)

    assert result is not None


def test_update_api_token_not_found(mpt_vendor, api_token_factory, invalid_api_token_id):
    updated_api_token_data = api_token_factory(name="Nonexistent API Token")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_vendor.accounts.api_tokens.update(invalid_api_token_id, updated_api_token_data)


def test_api_token_disable(mpt_vendor, created_api_token):
    result = mpt_vendor.accounts.api_tokens.disable(created_api_token.id)

    assert result is not None


def test_api_token_disable_not_found(mpt_vendor, invalid_api_token_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_vendor.accounts.api_tokens.disable(invalid_api_token_id)


def test_api_token_enable(mpt_vendor, created_api_token):
    mpt_vendor.accounts.api_tokens.disable(created_api_token.id)

    result = mpt_vendor.accounts.api_tokens.enable(created_api_token.id)

    assert result is not None


def test_api_token_enable_not_found(mpt_vendor, invalid_api_token_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_vendor.accounts.api_tokens.enable(invalid_api_token_id)

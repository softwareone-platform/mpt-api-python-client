import pytest

from mpt_api_client import MPTClient
from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.http import Service
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_licensee(mpt_client, licensee_factory, account_icon):
    new_licensee_request_data = licensee_factory(name="E2E Created licensee")

    new_licensee = mpt_client.accounts.licensees.create(
        new_licensee_request_data, logo=account_icon
    )

    yield new_licensee

    try:
        mpt_client.accounts.licensees.delete(new_licensee.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete licensee: {error.title}")  # noqa: WPS421


@pytest.mark.parametrize(
    "resource_path",
    ["accounts.licensees"],
)
class TestGenericResource:
    def get_resource(self, mpt_client: MPTClient, resource_path) -> Service:
        resource = mpt_client
        for path_element in resource_path.split("."):
            resource = getattr(resource, path_element)
        return resource

    def test_get_by_id(self, mpt_client, licensee_id, resource_path):
        resource = self.get_resource(mpt_client, resource_path)

        licensee = resource.get(licensee_id)
        assert licensee is not None

    def test_get_by_id_not_found(self, resource_path, mpt_client, invalid_licensee_id):
        resource = self.get_resource(mpt_client, resource_path)

        with pytest.raises(MPTAPIError, match=r"404 Not Found"):
            resource.get(invalid_licensee_id)

    def test_list(self, mpt_client, resource_path):
        resource = self.get_resource(mpt_client, resource_path)

        limit = 10
        licensees = resource.fetch_page(limit=limit)
        assert len(licensees) > 0

    def test_filter(self, resource_path, mpt_client, licensee_id):
        resource = self.get_resource(mpt_client, resource_path)

        select_fields = ["-address"]

        filtered_licensees = (
            resource.filter(RQLQuery(id=licensee_id))
            .filter(RQLQuery(name="E2E Seeded Licensee"))
            .select(*select_fields)
        )

        licensees = list(filtered_licensees.iterate())

        assert len(licensees) == 1

    def test_create(self, resource_path, created_licensee):
        assert created_licensee is not None

    def test_delete(self, resource_path, mpt_client, created_licensee):
        resource = self.get_resource(mpt_client, resource_path)

        resource.delete(created_licensee.id)

    def test_delete_not_found(self, resource_path, mpt_client, invalid_licensee_id):
        resource = self.get_resource(mpt_client, resource_path)

        with pytest.raises(MPTAPIError, match=r"404 Not Found"):
            resource.delete(invalid_licensee_id)

    def test_update(
        self, resource_path, mpt_client, licensee_factory, account_icon, created_licensee
    ):
        resource = self.get_resource(mpt_client, resource_path)

        updated_licensee_data = licensee_factory(name="E2E Updated Licensee")

        updated_licensee = resource.update(
            created_licensee.id, updated_licensee_data, logo=account_icon
        )

        assert updated_licensee is not None

    def test_update_not_found(
        self, resource_path, mpt_client, licensee_factory, account_icon, invalid_licensee_id
    ):
        resource = self.get_resource(mpt_client, resource_path)

        updated_licensee_data = licensee_factory(name="Nonexistent Licensee")

        with pytest.raises(MPTAPIError, match=r"404 Not Found"):
            resource.update(invalid_licensee_id, updated_licensee_data, logo=account_icon)

    def test_disable(self, resource_path, mpt_client, created_licensee):
        resource = self.get_resource(mpt_client, resource_path)

        disabled_licensee = resource.disable(created_licensee.id)

        assert disabled_licensee is not None

    def test_disable_not_found(self, resource_path, mpt_client, invalid_licensee_id):
        resource = self.get_resource(mpt_client, resource_path)

        with pytest.raises(MPTAPIError, match=r"404 Not Found"):
            resource.disable(invalid_licensee_id)

    def test_enable(self, resource_path, mpt_client, created_licensee):
        resource = self.get_resource(mpt_client, resource_path)

        resource.disable(created_licensee.id)

        enabled_licensee = resource.enable(created_licensee.id)

        assert enabled_licensee is not None

    def test_enable_not_found(self, resource_path, mpt_client, invalid_licensee_id):
        resource = self.get_resource(mpt_client, resource_path)

        with pytest.raises(MPTAPIError, match=r"404 Not Found"):
            resource.enable(invalid_licensee_id)

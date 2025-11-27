import json
import os
import pathlib

import pytest

from mpt_api_client import MPTClient
from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.http import Service
from mpt_api_client.rql.query_builder import RQLQuery
from tests.e2e.accounts.licensees.conftest import licensee_factory

pytestmark = [pytest.mark.flaky]
licensee_factory = licensee_factory()


def e2e_config():
    filename = os.getenv("TEST_CONFIG_FILE", "e2e_config.test.json")
    file_path = pathlib.Path(__file__).parent.parent.parent.joinpath(filename)
    return json.loads(file_path.read_text())


@pytest.mark.parametrize(
    ("resource_path", "existing_id", "data"),
    [
        (
            "accounts.licensees",
            e2e_config("accounts.licensee.id"),
            {
                "name": "Test E2E Licensee",
                "address": {
                    "addressLine1": "456 Licensee St",
                    "city": "Los Angeles",
                    "state": "CA",
                    "postCode": "67890",
                    "country": "US",
                },
                "useBuyerAddress": False,
                "seller": {"id": "seller_id"},
                "buyer": {"id": "buyer_id"},
                "account": {"id": "licensee_account_id"},
                "eligibility": {"client": True, "partner": False},
                "groups": ["user_group_factory(user_group_account_id=licensee_account_id)"],
                "type": "Client",
                "status": "Enabled",
                "defaultLanguage": "en-US",
            },
        )
    ],
)
class TestGenericResource:
    def get_resource(self, mpt_client: MPTClient, resource_path) -> Service:
        resource = mpt_client
        for path_element in resource_path.split("."):
            resource = getattr(resource, path_element)
        return resource

    def create(self, resource, request_data, account_icon):
        return resource.create(request_data, logo=account_icon)

    def delete(self, resource, id):
        try:
            resource.delete(id)
        except MPTAPIError as error:
            print(f"TEARDOWN - Unable to delete licensee: {error.title}")  # noqa: WPS421

    def test_create_delete(self, resource_path, mpt_client, account_icon):
        resource = self.get_resource(mpt_client, resource_path)
        created = self.create(resource, licensee_factory(), account_icon)

        assert created is not None

        self.delete(self.get_resource(self.mpt_client, resource_path), created.id)

    def test_get_by_id(self, resource_path, existing_id, mpt_client):
        resource = self.get_resource(mpt_client, resource_path)

        licensee = resource.get(existing_id)
        assert licensee is not None

    def test_get_by_id_not_found(self, resource_path, mpt_client):
        resource = self.get_resource(mpt_client, resource_path)

        with pytest.raises(MPTAPIError, match=r"404 Not Found"):
            resource.get("invalid_id")

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

    def test_delete_not_found(self, resource_path, mpt_client):
        resource = self.get_resource(mpt_client, resource_path)

        with pytest.raises(MPTAPIError, match=r"404 Not Found"):
            resource.delete("invalid_id")

    def test_update(self, resource_path, mpt_client, account_icon):
        resource = self.get_resource(mpt_client, resource_path)
        created = self.create(resource, licensee_factory(), account_icon)

        updated_licensee_data = licensee_factory(name="E2E Updated Licensee")

        updated_licensee = resource.update(created.id, updated_licensee_data, logo=account_icon)

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

    def test_enable(self, resource_path, mpt_client, account_icon):
        resource = self.get_resource(mpt_client, resource_path)
        created = self.create(resource, licensee_factory(), account_icon)

        resource.disable(created.id)

        enabled_licensee = resource.enable(created.id)

        assert enabled_licensee is not None

    def test_enable_not_found(self, resource_path, mpt_client):
        resource = self.get_resource(mpt_client, resource_path)

        with pytest.raises(MPTAPIError, match=r"404 Not Found"):
            resource.enable("invalid_id")

import pytest

from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_get_installation(installations_service, installation_id):
    result = installations_service.get(installation_id)

    assert result.id == installation_id


def test_filter_installations(installations_service, installation_id):
    assert_service_filter_with_iterate(installations_service, installation_id, None)  # act


@pytest.mark.skip(reason="creates real resources; run manually only")
def test_create_installation(created_installation, installation_data):
    result = created_installation.extension

    assert result.id == installation_data["extension"]["id"]


@pytest.mark.skip(reason="modifies real resources; run manually only")
def test_invite_installation(installations_service, created_installation):
    result = installations_service.invite(created_installation.id)

    assert result.status == "Invited"


@pytest.mark.skip(reason="modifies real resources; run manually only")
def test_install_installation(installations_service, created_installation):
    result = installations_service.install(created_installation.id)

    assert result.status == "Installed"


@pytest.mark.skip(reason="modifies real resources; run manually only")
def test_uninstall_installation(installations_service, created_installation):
    result = installations_service.uninstall(created_installation.id)

    assert result.status == "Uninstalled"


@pytest.mark.skip(reason="modifies real resources; run manually only")
def test_expire_installation(installations_service, created_installation):
    result = installations_service.expire(created_installation.id)

    assert result.status == "Expired"


@pytest.mark.skip(reason="deletes real resources; run manually only")
def test_delete_installation(installations_service, created_installation):
    installations_service.delete(created_installation.id)  # act

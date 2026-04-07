import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="creates real resources; run manually only")
def test_create_installation(async_created_installation, installation_data):
    result = async_created_installation.extension

    assert result.id == installation_data["extension"]["id"]


async def test_get_installation(async_installations_service, installation_id):
    result = await async_installations_service.get(installation_id)

    assert result.id == installation_id


async def test_filter_installations(async_installations_service, installation_id):
    await assert_async_service_filter_with_iterate(
        async_installations_service, installation_id, None
    )  # act


@pytest.mark.skip(reason="modifies real resources; run manually only")
async def test_invite_installation(async_installations_service, async_created_installation):
    result = await async_installations_service.invite(async_created_installation.id)

    assert result.status == "Invited"


@pytest.mark.skip(reason="modifies real resources; run manually only")
async def test_install_installation(async_installations_service, async_created_installation):
    result = await async_installations_service.install(async_created_installation.id)

    assert result.status == "Installed"


@pytest.mark.skip(reason="modifies real resources; run manually only")
async def test_uninstall_installation(async_installations_service, async_created_installation):
    result = await async_installations_service.uninstall(async_created_installation.id)

    assert result.status == "Uninstalled"


@pytest.mark.skip(reason="modifies real resources; run manually only")
async def test_expire_installation(async_installations_service, async_created_installation):
    result = await async_installations_service.expire(async_created_installation.id)

    assert result.status == "Expired"


@pytest.mark.skip(reason="deletes real resources; run manually only")
async def test_delete_installation(async_installations_service, async_created_installation):
    await async_installations_service.delete(async_created_installation.id)  # act

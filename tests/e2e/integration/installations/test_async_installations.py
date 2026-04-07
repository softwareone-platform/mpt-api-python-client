import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate
from tests.e2e.integration.installations.helper import decode_invitation_payload

pytestmark = [pytest.mark.flaky]


def test_create_installation(async_created_installation, installation_data):
    result = async_created_installation.extension

    assert result.id == installation_data["extension"]["id"]


async def test_get_installation(async_installations_service, async_created_installation):
    result = await async_installations_service.get(async_created_installation.id)

    assert result.id == async_created_installation.id


async def test_filter_installations(async_installations_service, async_created_installation):
    await assert_async_service_filter_with_iterate(
        async_installations_service, async_created_installation.id, None
    )  # act


async def test_redeem_installation(
    async_installations_service,
    async_created_installation_invite,
    installation_modules,
):
    invitation_payload = decode_invitation_payload(
        async_created_installation_invite.invitation.url,
    )
    if not invitation_payload.get("installationId") == async_created_installation_invite.id:
        raise ValueError(
            f"Installation ID mismatch: expected {async_created_installation_invite.id}, "
            f"got {invitation_payload.get('installationId')}"
        )

    redeem_invitation_data = {
        "code": invitation_payload["code"],
        "modules": installation_modules,
    }

    result = await async_installations_service.redeem(
        async_created_installation_invite.id,
        redeem_invitation_data,
    )

    assert result.id == async_created_installation_invite.id


async def test_delete_installation(async_installations_service, async_created_installation):
    await async_installations_service.delete(async_created_installation.id)  # act

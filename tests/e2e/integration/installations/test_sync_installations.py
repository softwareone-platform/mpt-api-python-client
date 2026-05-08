import pytest

from tests.e2e.helper import assert_service_filter_with_iterate
from tests.e2e.integration.installations.helper import decode_invitation_payload

pytestmark = [
    pytest.mark.flaky,
]


def test_get_installation(installations_service, created_installation_invite):
    result = installations_service.get(created_installation_invite.id)

    assert result.id == created_installation_invite.id


def test_filter_installations(installations_service, created_installation_invite):
    assert_service_filter_with_iterate(
        installations_service, created_installation_invite.id, None
    )  # act


def test_create_installation(created_installation, created_installation_invite, invite_data):
    result = created_installation.extension

    assert result.id == invite_data["extension"]["id"]


def test_redeem_installation(
    installations_service,
    created_installation_invite,
    installation_modules,
):
    invitation_payload = decode_invitation_payload(created_installation_invite.invitation.url)
    if invitation_payload.get("installationId") != created_installation_invite.id:
        raise ValueError(
            f"Installation ID mismatch: expected {created_installation_invite.id}, "
            f"got {invitation_payload.get('installationId')}"
        )
    redeem_invitation_data = {
        "code": invitation_payload["code"],
        "modules": installation_modules,
    }

    result = installations_service.redeem(
        created_installation_invite.id,
        redeem_invitation_data,
    )

    assert result.id == created_installation_invite.id


def test_delete_installation(installations_service, created_installation):
    installations_service.delete(created_installation.id)  # act

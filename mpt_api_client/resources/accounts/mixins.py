from urllib.parse import urljoin

from mpt_api_client.http.types import FileTypes
from mpt_api_client.models import ResourceData


class ActivatableMixin[Model]:
    """Activatable mixin for activating, enabling, disabling and deactivating resources."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Activate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "activate", json=resource_data
        )

    def deactivate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Deactivate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )


class EnablableMixin[Model]:
    """Enablable mixin for enabling and disabling resources."""

    def enable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enable a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "enable", json=resource_data
        )

    def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Disable a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "disable", json=resource_data
        )


class ValidateMixin[Model]:
    """Validate mixin adds the ability to validate a resource."""

    def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Validate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be validated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "validate", json=resource_data
        )


class BlockableMixin[Model]:
    """Blockable mixin for blocking and unblocking resources."""

    def block(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Block a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "block", json=resource_data
        )

    def unblock(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unblock a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "unblock", json=resource_data
        )


class InvitableMixin[Model]:
    """Invitable mixin for sending and managing invites for resources."""

    def accept_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept an invite for a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept-invite", json=resource_data
        )

    def resend_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Resend an invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "resend-invite", json=resource_data
        )

    def send_new_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Send a new invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "send-new-invite", json=resource_data
        )


class CreateFileMixin[Model]:
    """Create file mixin."""

    _upload_file_key = "file"
    _upload_data_key = "data"

    def create(self, resource_data: ResourceData, file: FileTypes | None = None) -> Model:  # noqa: WPS110
        """Create logo.

        Create a file resource by specifying a file image.

        Args:
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Created resource.
        """
        files = {}

        if file:
            files[self._upload_file_key] = file

        response = self.http_client.request(  # type: ignore[attr-defined]
            "post",
            self.path,  # type: ignore[attr-defined]
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class UpdateFileMixin[Model]:
    """Update file mixin."""

    _upload_file_key = "file"
    _upload_data_key = "data"

    def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        file: FileTypes | None = None,  # noqa: WPS110
    ) -> Model:
        """Update file.

        Update a file resource by specifying a file.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Updated resource.
        """
        files = {}

        url = urljoin(f"{self.path}/", resource_id)  # type: ignore[attr-defined]

        if file:
            files[self._upload_file_key] = file

        response = self.http_client.request(  # type: ignore[attr-defined]
            "put",
            url,
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AccountMixin[Model](
    CreateFileMixin[Model],
    UpdateFileMixin[Model],
    ActivatableMixin[Model],
    EnablableMixin[Model],
    ValidateMixin[Model],
):
    """Account mixin."""

    _upload_file_key = "logo"
    _upload_data_key = "account"


class BuyerMixin[Model](
    CreateFileMixin[Model],
    UpdateFileMixin[Model],
    ActivatableMixin[Model],
    EnablableMixin[Model],
    ValidateMixin[Model],
):
    """Buyer mixin."""

    _upload_file_key = "logo"
    _upload_data_key = "buyer"


class LicenseeMixin[Model](
    CreateFileMixin[Model],
    UpdateFileMixin[Model],
    EnablableMixin[Model],
):
    """Licensee mixin."""

    _upload_file_key = "logo"
    _upload_data_key = "licensee"


class AsyncActivatableMixin[Model]:
    """Async activatable mixin for activating, enabling, disabling and deactivating resources."""

    async def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Activate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "activate", json=resource_data
        )

    async def deactivate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Deactivate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )


class AsyncEnablableMixin[Model]:
    """Asynchronous Enablable mixin for enabling and disabling resources."""

    async def enable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enable a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "enable", json=resource_data
        )

    async def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Disable a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "disable", json=resource_data
        )


class AsyncValidateMixin[Model]:
    """Asynchronous Validate mixin adds the ability to validate a resource."""

    async def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Validate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be validated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "validate", json=resource_data
        )


class AsyncBlockableMixin[Model]:
    """Asynchronous Blockable mixin for blocking and unblocking resources."""

    async def block(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Block a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "block", json=resource_data
        )

    async def unblock(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unblock a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "unblock", json=resource_data
        )


class AsyncInvitableMixin[Model]:
    """Asynchronous Invitable mixin for sending and managing invites for resources."""

    async def accept_invite(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Accept an invite for a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept-invite", json=resource_data
        )

    async def resend_invite(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Resend an invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "resend-invite", json=resource_data
        )

    async def send_new_invite(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Send a new invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "send-new-invite", json=resource_data
        )


class AsyncCreateFileMixin[Model]:
    """Asynchronous Create file mixin."""

    _upload_file_key = "file"
    _upload_data_key = "data"

    async def create(self, resource_data: ResourceData, file: FileTypes | None = None) -> Model:  # noqa: WPS110
        """Create file.

        Create a file resource by specifying a file.

        Args:
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Created resource.
        """
        files = {}

        if file:
            files[self._upload_file_key] = file

        response = await self.http_client.request(  # type: ignore[attr-defined]
            "post",
            self.path,  # type: ignore[attr-defined]
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncUpdateFileMixin[Model]:
    """Asynchronous Update file mixin."""

    _upload_file_key = "file"
    _upload_data_key = "data"

    async def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        file: FileTypes | None = None,  # noqa: WPS110
    ) -> Model:
        """Update file.

        Update a file resource by specifying a file.

        Args:
            resource_id: Resource ID.
            resource_data: Resource data.
            file: File image.

        Returns:
            Model: Updated resource.
        """
        files = {}

        url = urljoin(f"{self.path}/", resource_id)  # type: ignore[attr-defined]

        if file:
            files[self._upload_file_key] = file

        response = await self.http_client.request(  # type: ignore[attr-defined]
            "put",
            url,
            json=resource_data,
            files=files,
            json_file_key=self._upload_data_key,
            force_multipart=True,
        )

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncAccountMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncUpdateFileMixin[Model],
    AsyncActivatableMixin[Model],
    AsyncEnablableMixin[Model],
    AsyncValidateMixin[Model],
):
    """Asynchronous Account mixin."""

    _upload_file_key = "logo"
    _upload_data_key = "account"


class AsyncBuyerMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncUpdateFileMixin[Model],
    AsyncActivatableMixin[Model],
    AsyncEnablableMixin[Model],
    AsyncValidateMixin[Model],
):
    """Asynchronous Buyer mixin."""

    _upload_file_key = "logo"
    _upload_data_key = "buyer"


class AsyncLicenseeMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncUpdateFileMixin[Model],
    AsyncEnablableMixin[Model],
):
    """Asynchronous Licensee mixin."""

    _upload_file_key = "logo"
    _upload_data_key = "licensee"

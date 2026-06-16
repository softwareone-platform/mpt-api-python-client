from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.types import QueryParam
from mpt_api_client.models import Model


class InstallationsToken(Model):
    """Integration installations token resource.

    Attributes:
        token: The installation or account-scoped token.
    """

    token: str | None


class InstallationsTokenServiceConfig:
    """Installations token service configuration."""

    _endpoint = "/public/v1/integration/installations/-/token"
    _model_class = InstallationsToken


class InstallationsTokenService(
    Service[InstallationsToken],
    InstallationsTokenServiceConfig,
):
    """Sync service for the /public/v1/integration/installations/-/token endpoint."""

    def token(self, account_id: str | None = None) -> InstallationsToken:
        """Request an installation token, optionally scoped to an account.

        Args:
            account_id: When provided, request a token scoped to this account
                (sent as the ``account.id`` query parameter).

        Returns:
            The token resource.
        """
        query_params: QueryParam | None = {"account.id": account_id} if account_id else None
        response = self.http_client.request("post", self.path, query_params=query_params)
        return self._model_class.from_response(response)  # type: ignore[return-value]


class AsyncInstallationsTokenService(
    AsyncService[InstallationsToken],
    InstallationsTokenServiceConfig,
):
    """Async service for the /public/v1/integration/installations/-/token endpoint."""

    async def token(self, account_id: str | None = None) -> InstallationsToken:
        """Request an installation token, optionally scoped to an account.

        Args:
            account_id: When provided, request a token scoped to this account
                (sent as the ``account.id`` query parameter).

        Returns:
            The token resource.
        """
        query_params: QueryParam | None = {"account.id": account_id} if account_id else None
        response = await self.http_client.request("post", self.path, query_params=query_params)
        return self._model_class.from_response(response)  # type: ignore[return-value]

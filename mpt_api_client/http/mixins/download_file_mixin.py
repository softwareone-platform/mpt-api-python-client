from mpt_api_client.exceptions import MPTError
from mpt_api_client.http.types import Response
from mpt_api_client.models import FileModel


class DownloadFileMixin[Model]:
    """Download file mixin."""

    def download(self, resource_id: str, accept: str | None = None) -> FileModel:
        """Download the file for the given resource ID.

        Args:
            resource_id: Resource ID.
            accept: The content type expected for the file.
                If not provided, the content type will be fetched from the resource.

        Returns:
            File model containing the downloaded file.
        """
        if not accept:
            resource: Model = self._resource_action(resource_id, method="GET")  # type: ignore[attr-defined]
            accept = resource.content_type  # type: ignore[attr-defined]
            if not accept:
                raise MPTError("Unable to download file. Content type not found in resource")
        response: Response = self._resource_do_request(  # type: ignore[attr-defined]
            resource_id, method="GET", headers={"Accept": accept}
        )
        return FileModel(response)


class AsyncDownloadFileMixin[Model]:
    """Download file mixin."""

    async def download(self, resource_id: str, accept: str | None = None) -> FileModel:
        """Download the file for the given resource ID.

        Args:
            resource_id: Resource ID.
            accept: The content type expected for the file.
                If not provided, the content type will be fetched from the resource.

        Returns:
            File model containing the downloaded file.
        """
        if not accept:
            resource: Model = await self._resource_action(resource_id, method="GET")  # type: ignore[attr-defined]
            accept = resource.content_type  # type: ignore[attr-defined]
            if not accept:
                raise MPTError("Unable to download file. Content type not found in resource")
        response = await self._resource_do_request(  # type: ignore[attr-defined]
            resource_id, method="GET", headers={"Accept": accept}
        )
        return FileModel(response)

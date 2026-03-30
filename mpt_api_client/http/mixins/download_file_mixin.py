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
        accessor = self._resource(resource_id)  # type: ignore[attr-defined]
        if not accept:
            resource: Model = accessor.get()
            accept = resource.content_type  # type: ignore[attr-defined]
            if not accept:
                raise MPTError("Unable to download file. Content type not found in resource")
        response: Response = accessor.do_request("GET", headers={"Accept": accept})
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
        accessor = self._resource(resource_id)  # type: ignore[attr-defined]
        if not accept:
            resource: Model = await accessor.get()
            accept = resource.content_type  # type: ignore[attr-defined]
            if not accept:
                raise MPTError("Unable to download file. Content type not found in resource")
        response = await accessor.do_request("GET", headers={"Accept": accept})
        return FileModel(response)

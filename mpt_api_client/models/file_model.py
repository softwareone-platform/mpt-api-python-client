import re

from mpt_api_client.http.types import Response


class FileModel:
    """File resource."""

    def __init__(self, response: Response):
        self.response = response

    @property
    def filename(self) -> str | None:
        """Filename from Content-Disposition header.

        Returns:
            The filename if found in the Content-Disposition header, None otherwise.
        """
        content_disposition = self.response.headers.get("content-disposition")
        if not content_disposition:
            return None

        filename_match = re.search(
            r'filename\*=(?:UTF-8\'\')?([^;]+)|filename=(?:"([^"]+)"|([^;]+))',
            content_disposition,
            re.IGNORECASE,
        )

        if filename_match:
            return filename_match.group(1) or filename_match.group(2) or filename_match.group(3)

        return None

    @property
    def file_contents(self) -> bytes:
        """Returns the content of the attachment.

        Returns:
            The content of the attachment in bytes

        Raises:
            ResponseNotRead()

        """
        return self.response.content

    @property
    def content_type(self) -> str | None:
        """Returns the content type of the attachment.

        Returns:
            The content type of the attachment.
        """
        ctype = self.response.headers.get("content-type", "")
        return str(ctype)

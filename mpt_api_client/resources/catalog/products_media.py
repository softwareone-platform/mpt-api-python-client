import json
from typing import override

from httpx import Response
from httpx._types import FileTypes

from mpt_api_client.http import AsyncService, CreateMixin, DeleteMixin, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    UpdateMixin,
)
from mpt_api_client.models import FileModel, Model, ResourceData
from mpt_api_client.resources.catalog.mixins import AsyncPublishableMixin, PublishableMixin


def _json_to_file_payload(resource_data: ResourceData) -> bytes:
    return json.dumps(
        resource_data, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


class Media(Model):
    """Media resource."""


class MediaServiceConfig:
    """Media service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/media"
    _model_class = Media
    _collection_key = "data"


class MediaService(
    CreateMixin[Media],
    DeleteMixin,
    UpdateMixin[Media],
    PublishableMixin[Media],
    Service[Media],
    MediaServiceConfig,
):
    """Media service."""

    @override
    def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
    ) -> Media:
        """Create Media resource.

        Currently are two types of media resources available image and video.

        Video:
            resource_data:
                {
                  "name": "SomeMediaFile",
                  "description":"Some media description",
                  "mediaType": "Video",
                  "url": http://www.somemedia.com/somevideo.avi,
                  "displayOrder": 1
                }
            files: Add an image with the video thumbnail

        Image:
            resource_data:
                {
                  "name": "SomeMediaFile",
                  "description":"Some media description",
                  "mediaType": "Video",
                  "displayOrder": 1
                }
            files: The image itself

        Args:
            resource_data: Resource data.
            files: Files data.

        Returns:
            Media resource.
        """
        files = files or {}

        # Note: This is a workaround to fulfill MPT API request format
        #
        # HTTPx does not support sending json and files in the same call
        # currently only supports sending form-data and files in the same call.
        # https://www.python-httpx.org/quickstart/#sending-multipart-file-uploads
        #
        # MPT API expects files and data to be submitted in a multipart form-data upload.
        #
        # Current workaround is to send the json data as an unnamed file.
        # This ends adding the json as payload multipart data.
        #
        # json.dumps is setup using the same params of httpx json encoder to produce the same
        # encodings.

        if resource_data:
            files["_media_data"] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = self.http_client.post(self.endpoint, files=files)
        response.raise_for_status()
        return Media.from_response(response)

    def download(self, media_id: str) -> FileModel:
        """Download the media file for the given media ID.

        Args:
            media_id: Media ID.

        Returns:
            Media file.
        """
        response: Response = self._resource_do_request(
            media_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)


class AsyncMediaService(
    AsyncCreateMixin[Media],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Media],
    AsyncPublishableMixin[Media],
    AsyncService[Media],
    MediaServiceConfig,
):
    """Media service."""

    @override
    async def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
    ) -> Media:
        """Create Media resource.

        Args:
            resource_data: Resource data.
            files: Files data.

        Returns:
            Media resource.
        """
        files = files or {}

        # Note: This is a workaround to fulfill MPT API request format
        #
        # HTTPx does not support sending json and files in the same call
        # currently only supports sending form-data and files in the same call.
        # https://www.python-httpx.org/quickstart/#sending-multipart-file-uploads
        #
        # MPT API expects files and data to be submitted in a multipart form-data upload.
        #
        # Current workaround is to send the json data as an unnamed file.
        # This ends adding the json as payload multipart data.
        #
        # json.dumps is setup using the same params of httpx json encoder to produce the same
        # encodings.

        if resource_data:
            files["_media_data"] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = await self.http_client.post(self.endpoint, files=files)
        response.raise_for_status()
        return Media.from_response(response)

    async def download(self, media_id: str) -> FileModel:
        """Download the media file for the given media ID.

        Args:
            media_id: Media ID.

        Returns:
            Media file.
        """
        response = await self._resource_do_request(media_id, method="GET", headers={"Accept": "*"})
        return FileModel(response)

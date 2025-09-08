import json

from httpx import Response
from httpx._types import FileTypes

from mpt_api_client.http import AsyncDeleteMixin, AsyncService, DeleteMixin, Service
from mpt_api_client.models import FileModel, Model, ResourceData


def _json_to_file_payload(resource_data: ResourceData) -> bytes:
    return json.dumps(
        resource_data, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


class AgreementAttachment(Model):
    """Agreement attachment resource."""


class AgreementsAttachmentServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/agreements/{agreement_id}/attachments"
    _model_class = AgreementAttachment
    _collection_key = "data"


class AgreementsAttachmentService(
    DeleteMixin, Service[AgreementAttachment], AgreementsAttachmentServiceConfig
):
    """Attachments service."""

    def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
    ) -> AgreementAttachment:
        """Create AgreementAttachment resource.

        Args:
            resource_data: Resource data.
            files: Files data.

        Returns:
            AgreementAttachment resource.
        """
        files = files or {}

        # Note: This is a workaround to fulfill MPT API request format
        #
        # HTTPx does not support sending json and files in the same call
        # currently only supports sending form-data and files in the same call.
        # https://www.python-httpx.org/quickstart/#sending-multipart-file-uploads
        #
        # MPT API expects files and data to be submitted in a multipart form-data upload.
        # https://softwareone.atlassian.net/wiki/spaces/mpt/pages/5212079859/Commerce+API#Create-Agreement-Attachment
        #
        # Current workaround is to send the json data as an unnamed file.
        # This ends adding the json as payload multipart data.
        #
        # json.dumps is setup using the same params of httpx json encoder to produce the same
        # encodings.

        if resource_data:
            files["_attachment_data"] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = self.http_client.post(self.endpoint, files=files)
        response.raise_for_status()
        return AgreementAttachment.from_response(response)

    def download(self, agreement_id: str) -> FileModel:
        """Renders the template for the given Agreement id.

        Args:
            agreement_id: Agreement ID.

        Returns:
            Agreement template.
        """
        response: Response = self._resource_do_request(
            agreement_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)


class AsyncAgreementsAttachmentService(
    AsyncDeleteMixin, AsyncService[AgreementAttachment], AgreementsAttachmentServiceConfig
):
    """Attachments service."""

    async def create(
        self,
        resource_data: ResourceData | None = None,
        files: dict[str, FileTypes] | None = None,  # noqa: WPS221
    ) -> AgreementAttachment:
        """Create AgreementAttachment resource.

        Args:
            resource_data: Resource data.
            files: Files data.

        Returns:
            AgreementAttachment resource.
        """
        files = files or {}

        # Note: This is a workaround to fulfill MPT API request format
        #
        # HTTPx does not support sending json and files in the same call
        # currently only supports sending form-data and files in the same call.
        # https://www.python-httpx.org/quickstart/#sending-multipart-file-uploads
        #
        # MPT API expects files and data to be submitted in a multipart form-data upload.
        # https://softwareone.atlassian.net/wiki/spaces/mpt/pages/5212079859/Commerce+API#Create-Agreement-Attachment
        #
        # Current workaround is to send the json data as an unnamed file.
        # This ends adding the json as payload multipart data.
        #
        # json.dumps is setup using the same params of httpx json encoder to produce the same
        # encodings.

        if resource_data:
            files["_attachment_data"] = (
                None,
                _json_to_file_payload(resource_data),
                "application/json",
            )

        response = await self.http_client.post(self.endpoint, files=files)
        response.raise_for_status()
        return AgreementAttachment.from_response(response)

    async def download(self, agreement_id: str) -> FileModel:
        """Renders the template for the given Agreement id.

        Args:
            agreement_id: Agreement ID.

        Returns:
            Agreement template.
        """
        response = await self._resource_do_request(
            agreement_id, method="GET", headers={"Accept": "*"}
        )
        return FileModel(response)

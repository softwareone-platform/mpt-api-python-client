import io

import httpx
import pytest
import respx

from mpt_api_client.resources.commerce.agreements_attachments import (
    AgreementsAttachmentService,
    AsyncAgreementsAttachmentService,
)


@pytest.fixture
def attachment_service(http_client):
    return AgreementsAttachmentService(
        http_client=http_client, endpoint_params={"agreement_id": "AGR-123"}
    )


@pytest.fixture
def async_attachment_service(async_http_client):
    return AsyncAgreementsAttachmentService(
        http_client=async_http_client, endpoint_params={"agreement_id": "AGR-123"}
    )


async def test_async_create(async_attachment_service):
    attachment_data = {"id": "ATT-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/agreements/AGR-123/attachments"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=attachment_data,
            )
        )
        files = {"attachment": ("test.txt", io.BytesIO(b"Hello"), "text/plain")}
        new_attachment = await async_attachment_service.create({"name": "Upload test"}, files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="_attachment_data"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Upload test"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="attachment"; filename="test.txt"\r\n'
        b"Content-Type: text/plain\r\n\r\n"
        b"Hello\r\n" in request.content
    )
    assert new_attachment.to_dict() == attachment_data


async def test_async_create_no_data(async_attachment_service):
    attachment_data = {"id": "ATT-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/agreements/AGR-123/attachments"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=attachment_data,
            )
        )
        files = {"attachment": ("test.txt", io.BytesIO(b"Hello"), "text/plain")}
        new_attachment = await async_attachment_service.create(files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="attachment"; filename="test.txt"\r\n'
        b"Content-Type: text/plain\r\n\r\n"
        b"Hello\r\n" in request.content
    )
    assert new_attachment.to_dict() == attachment_data


async def test_async_download(async_attachment_service):
    attachment_content = b"PDF file content or binary data"

    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/commerce/agreements/AGR-123/attachments/ATT-456"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": 'form-data; name="file"; filename="test.txt.pdf"',
                },
                content=attachment_content,
            )
        )

        downloaded_file = await async_attachment_service.download("ATT-456")
        request = mock_route.calls[0].request
        accept_header = (b"Accept", b"*")
        assert accept_header in request.headers.raw
        assert mock_route.call_count == 1
        assert downloaded_file.file_contents == attachment_content
        assert downloaded_file.content_type == "application/octet-stream"
        assert downloaded_file.filename == "test.txt.pdf"


def test_download(attachment_service):
    attachment_content = b"PDF file content or binary data"

    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/commerce/agreements/AGR-123/attachments/ATT-456"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": 'form-data; name="file"; filename="test.txt.pdf"',
                },
                content=attachment_content,
            )
        )

        downloaded_file = attachment_service.download("ATT-456")
        request = mock_route.calls[0].request
        accept_header = (b"Accept", b"*")
        assert accept_header in request.headers.raw
        assert mock_route.call_count == 1
        assert downloaded_file.file_contents == attachment_content
        assert downloaded_file.content_type == "application/octet-stream"
        assert downloaded_file.filename == "test.txt.pdf"


def test_create(attachment_service):
    attachment_data = {"id": "ATT-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/agreements/AGR-123/attachments"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=attachment_data,
            )
        )
        files = {"attachment": ("test.txt", io.BytesIO(b"Hello"), "text/plain")}
        new_attachment = attachment_service.create({"name": "Upload test"}, files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="_attachment_data"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Upload test"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="attachment"; filename="test.txt"\r\n'
        b"Content-Type: text/plain\r\n\r\n"
        b"Hello\r\n" in request.content
    )
    assert new_attachment.to_dict() == attachment_data


def test_create_no_data(attachment_service):
    attachment_data = {"id": "ATT-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/agreements/AGR-123/attachments"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                json=attachment_data,
            )
        )
        files = {"attachment": ("test.txt", io.BytesIO(b"Hello"), "text/plain")}
        new_attachment = attachment_service.create(files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="attachment"; filename="test.txt"\r\n'
        b"Content-Type: text/plain\r\n\r\n"
        b"Hello\r\n" in request.content
    )
    assert new_attachment.to_dict() == attachment_data


@pytest.mark.parametrize("method", ["get", "create", "delete", "download"])
def test_mixins_present(attachment_service, method):
    assert hasattr(attachment_service, method)


@pytest.mark.parametrize("method", ["get", "create", "delete", "download"])
def test_async_mixins_present(async_attachment_service, method):
    assert hasattr(async_attachment_service, method)

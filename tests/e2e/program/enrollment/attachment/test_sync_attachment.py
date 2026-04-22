import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_enrollment_attachment(mpt_vendor, enrollment_attachment_factory, enrollment_id, pdf_fd):
    new_enrollment_attachment_request_data = enrollment_attachment_factory(
        name="E2E Created Program Enrollment Attachment",
    )
    enrollment_attachments = mpt_vendor.program.enrollments.attachments(enrollment_id)

    created_enrollment_attachment = enrollment_attachments.create(
        new_enrollment_attachment_request_data, file=pdf_fd
    )

    yield created_enrollment_attachment

    try:
        enrollment_attachments.delete(created_enrollment_attachment.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete enrollment attachment: {error.title}")  # noqa: WPS421


@pytest.fixture
def enrollment_attachments(mpt_vendor, enrollment_id):
    return mpt_vendor.program.enrollments.attachments(enrollment_id)


def test_get_enrollment_attachment_by_id(enrollment_attachments, attachment_id):
    result = enrollment_attachments.get(attachment_id)

    assert result is not None


def test_get_enrollment_attachment_not_found(enrollment_attachments, invalid_attachment_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        enrollment_attachments.get(invalid_attachment_id)


def test_list_enrollment_attachments(enrollment_attachments):
    limit = 10

    result = enrollment_attachments.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_enrollment_attachments(enrollment_attachments, attachment_id):
    select_fields = ["-description"]
    filtered_attachments = (
        enrollment_attachments
        .filter(RQLQuery(id=attachment_id))
        .filter(RQLQuery(name="E2E Seeded Program Enrollment Attachment"))
        .select(*select_fields)
    )

    result = list(filtered_attachments.iterate())

    assert len(result) == 1


def test_create_enrollment_attachment(created_enrollment_attachment):
    result = created_enrollment_attachment

    assert result is not None


def test_update_enrollment_attachment(enrollment_attachments, created_enrollment_attachment):
    updated_data = {
        "name": "E2E Updated Program Enrollment Attachment",
        "description": "E2E Updated Program Enrollment Attachment",
    }

    result = enrollment_attachments.update(created_enrollment_attachment.id, updated_data)

    assert result is not None


def test_delete_enrollment_attachment(enrollment_attachments, created_enrollment_attachment):
    result = created_enrollment_attachment

    enrollment_attachments.delete(result.id)


def test_download_enrollment_attachment(enrollment_attachments, attachment_id):
    result = enrollment_attachments.download(attachment_id)

    assert result.file_contents is not None

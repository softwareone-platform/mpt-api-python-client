import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_enrollment(mpt_client, enrollment_data):
    enrollment = mpt_client.program.enrollments.create(enrollment_data)

    yield enrollment

    try:
        mpt_client.program.enrollments.delete(enrollment.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete enrollment {enrollment.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
def submitted_enrollment(created_enrollment, mpt_client):
    return mpt_client.program.enrollments.submit(created_enrollment.id)


@pytest.fixture
def queried_enrollment(
    submitted_enrollment, mpt_vendor, status_flow_enrollment_data_factory, query_template_id
):
    query_enrollment_data = status_flow_enrollment_data_factory(
        enrollment_id=submitted_enrollment.id,
        template_id=query_template_id,
    )
    return mpt_vendor.program.enrollments.query(submitted_enrollment.id, query_enrollment_data)


@pytest.fixture
def processed_enrollment(
    mpt_vendor, queried_enrollment, status_flow_enrollment_data_factory, process_template_id
):
    process_enrollment_data = status_flow_enrollment_data_factory(
        enrollment_id=queried_enrollment.id,
        template_id=process_template_id,
    )
    return mpt_vendor.program.enrollments.process(queried_enrollment.id, process_enrollment_data)


def test_get_enrollment_by_id(mpt_client, enrollment_id):
    result = mpt_client.program.enrollments.get(enrollment_id)

    assert result is not None


def test_list_enrollments(mpt_client):
    limit = 10

    result = mpt_client.program.enrollments.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_enrollment_by_id_not_found(mpt_client, invalid_enrollment_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.program.enrollments.get(invalid_enrollment_id)


def test_filter_enrollments(mpt_client, enrollment_id):
    filtered_enrollments = mpt_client.program.enrollments.filter(RQLQuery(id=enrollment_id)).filter(
        RQLQuery(status="Completed")
    )

    result = list(filtered_enrollments.iterate())

    assert len(result) == 1


def test_create_enrollment(created_enrollment):
    result = created_enrollment

    assert result is not None


def test_delete_enrollment(mpt_client, created_enrollment):
    enrollment_data = created_enrollment

    result = mpt_client.program.enrollments

    result.delete(enrollment_data.id)


def test_update_enrollment(mpt_vendor, submitted_enrollment, assignee_enrollment_data_factory):
    update_data = assignee_enrollment_data_factory(submitted_enrollment.id)

    result = mpt_vendor.program.enrollments.update(submitted_enrollment.id, update_data)

    assert result is not None


def test_submit_enrollment(mpt_client, created_enrollment):
    result = mpt_client.program.enrollments.submit(created_enrollment.id)

    assert result is not None


def test_validate_enrollment(mpt_client, submitted_enrollment, enrollment_status_message_factory):
    status_message_data = enrollment_status_message_factory(submitted_enrollment.id)

    result = mpt_client.program.enrollments.validate(submitted_enrollment.id, status_message_data)

    assert result is not None


def test_query_enrollment(queried_enrollment):
    result = queried_enrollment

    assert result is not None


def test_process_enrollment(processed_enrollment):
    result = processed_enrollment

    assert result is not None


def test_fail_enrollment(mpt_vendor, queried_enrollment, enrollment_status_message_factory):
    status_message_data = enrollment_status_message_factory(queried_enrollment.id)

    result = mpt_vendor.program.enrollments.fail(queried_enrollment.id, status_message_data)

    assert result is not None


def test_complete_enrollment(
    mpt_vendor, submitted_enrollment, status_flow_enrollment_data_factory, complete_template_id
):
    complete_enrollment_data = status_flow_enrollment_data_factory(
        enrollment_id=submitted_enrollment.id,
        template_id=complete_template_id,
    )

    result = mpt_vendor.program.enrollments.complete(
        submitted_enrollment.id, complete_enrollment_data
    )

    assert result is not None

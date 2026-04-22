import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_enrollment(async_mpt_client, enrollment_data):
    enrollment = await async_mpt_client.program.enrollments.create(enrollment_data)

    yield enrollment

    try:
        await async_mpt_client.program.enrollments.delete(enrollment.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete enrollment {enrollment.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def submitted_enrollment(created_enrollment, async_mpt_client):
    return await async_mpt_client.program.enrollments.submit(created_enrollment.id)


@pytest.fixture
async def queried_enrollment(
    submitted_enrollment, async_mpt_vendor, status_flow_enrollment_data_factory, query_template_id
):
    query_enrollment_data = status_flow_enrollment_data_factory(
        enrollment_id=submitted_enrollment.id,
        template_id=query_template_id,
    )
    return await async_mpt_vendor.program.enrollments.query(
        submitted_enrollment.id, query_enrollment_data
    )


@pytest.fixture
async def processed_enrollment(
    async_mpt_vendor, queried_enrollment, status_flow_enrollment_data_factory, process_template_id
):
    process_enrollment_data = status_flow_enrollment_data_factory(
        enrollment_id=queried_enrollment.id,
        template_id=process_template_id,
    )
    return await async_mpt_vendor.program.enrollments.process(
        queried_enrollment.id, process_enrollment_data
    )


async def test_get_enrollment_by_id(async_mpt_client, enrollment_id):
    result = await async_mpt_client.program.enrollments.get(enrollment_id)

    assert result is not None


async def test_list_enrollments(async_mpt_client):
    limit = 10

    result = await async_mpt_client.program.enrollments.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_enrollment_by_id_not_found(async_mpt_client, invalid_enrollment_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.program.enrollments.get(invalid_enrollment_id)


async def test_filter_enrollments(async_mpt_client, enrollment_id):
    filtered_enrollments = async_mpt_client.program.enrollments.filter(
        RQLQuery(id=enrollment_id)
    ).filter(RQLQuery(status="Completed"))

    result = [enrollment async for enrollment in filtered_enrollments.iterate()]

    assert len(result) == 1


def test_create_enrollment(created_enrollment):
    result = created_enrollment

    assert result is not None


async def test_delete_enrollment(async_mpt_client, created_enrollment):
    enrollment_data = created_enrollment

    result = async_mpt_client.program.enrollments

    await result.delete(enrollment_data.id)


async def test_update_enrollment(
    async_mpt_vendor, submitted_enrollment, assignee_enrollment_data_factory
):
    update_data = assignee_enrollment_data_factory(submitted_enrollment.id)

    result = await async_mpt_vendor.program.enrollments.update(submitted_enrollment.id, update_data)

    assert result is not None


async def test_submit_enrollment(async_mpt_client, created_enrollment):
    result = await async_mpt_client.program.enrollments.submit(created_enrollment.id)

    assert result is not None


async def test_validate_enrollment(
    async_mpt_client, submitted_enrollment, enrollment_status_message_factory
):
    status_message_data = enrollment_status_message_factory(submitted_enrollment.id)

    result = await async_mpt_client.program.enrollments.validate(
        submitted_enrollment.id, status_message_data
    )

    assert result is not None


def test_query_enrollment(queried_enrollment):
    result = queried_enrollment

    assert result is not None


def test_process_enrollment(processed_enrollment):
    result = processed_enrollment

    assert result is not None


async def test_fail_enrollment(
    async_mpt_vendor, queried_enrollment, enrollment_status_message_factory
):
    status_message_data = enrollment_status_message_factory(queried_enrollment.id)

    result = await async_mpt_vendor.program.enrollments.fail(
        queried_enrollment.id, status_message_data
    )

    assert result is not None


async def test_complete_enrollment(
    async_mpt_vendor,
    submitted_enrollment,
    status_flow_enrollment_data_factory,
    complete_template_id,
):
    complete_enrollment_data = status_flow_enrollment_data_factory(
        enrollment_id=submitted_enrollment.id,
        template_id=complete_template_id,
    )

    result = await async_mpt_vendor.program.enrollments.complete(
        submitted_enrollment.id, complete_enrollment_data
    )

    assert result is not None

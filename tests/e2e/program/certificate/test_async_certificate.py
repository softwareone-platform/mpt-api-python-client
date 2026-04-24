import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_certificate(
    async_mpt_ops, async_mpt_vendor, certificate_data, terminated_certificate_data_factory
):
    certificate = await async_mpt_ops.program.certificates.create(certificate_data)
    terminated_certificate_data = terminated_certificate_data_factory(certificate.id)

    yield certificate

    try:
        await async_mpt_vendor.program.certificates.terminate(
            certificate.id, terminated_certificate_data
        )
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to terminate certificate {certificate.id}: {error.title}")  # noqa: WPS421


async def test_get_certificate_by_id(async_mpt_vendor, certificate_id):
    result = await async_mpt_vendor.program.certificates.get(certificate_id)

    assert result is not None


async def test_get_certificate_by_invalid_id(async_mpt_vendor, invalid_certificate_id):
    with pytest.raises(MPTAPIError):
        await async_mpt_vendor.program.certificates.get(invalid_certificate_id)


async def test_list_certificates(async_mpt_vendor):
    limit = 10

    result = await async_mpt_vendor.program.certificates.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_certificates(async_mpt_vendor, certificate_id):
    select_fields = ["-audit", "-parameters"]
    filtered_certificates = (
        async_mpt_vendor.program.certificates
        .filter(RQLQuery(id=certificate_id))
        .filter(RQLQuery(status="Active"))
        .select(*select_fields)
    )

    result = [certificate async for certificate in filtered_certificates.iterate()]

    assert len(result) == 1


def test_create_certificate(created_certificate):
    result = created_certificate

    assert result is not None


async def test_update_certificate(async_mpt_client, created_certificate):
    updated_name = "E2E Updated Certificate Name"
    update_data = {"id": created_certificate.id, "name": updated_name}

    result = await async_mpt_client.program.certificates.update(created_certificate.id, update_data)

    assert result is not None


async def test_terminate_certificate(
    async_mpt_vendor, created_certificate, terminated_certificate_data_factory
):
    terminated_certificate_data = terminated_certificate_data_factory(created_certificate.id)

    result = await async_mpt_vendor.program.certificates.terminate(
        created_certificate.id, terminated_certificate_data
    )

    assert result is not None

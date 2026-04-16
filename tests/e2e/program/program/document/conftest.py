import pytest


@pytest.fixture
def document_id(e2e_config):
    return e2e_config["program.document.file.id"]


@pytest.fixture
def invalid_document_id(e2e_config):
    return "PDM-0000-0000-0000"


@pytest.fixture
def document_data_factory():
    def factory(
        document_type: str = "File",
    ):
        return {
            "name": "E2E Created Program Document",
            "description": "E2E Created Program Document",
            "type": document_type,
            "language": "en-us",
            "url": "",
            "documentType": document_type,
        }

    return factory


@pytest.fixture
def vendor_document_service(mpt_vendor, program_id):
    return mpt_vendor.program.programs.documents(program_id)


@pytest.fixture
def async_vendor_document_service(async_mpt_vendor, program_id):
    return async_mpt_vendor.program.programs.documents(program_id)

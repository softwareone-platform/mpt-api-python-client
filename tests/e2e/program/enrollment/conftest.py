import pytest


@pytest.fixture
def enrollment_id(e2e_config):
    return e2e_config["program.enrollment.id"]


@pytest.fixture
def invalid_enrollment_id():
    return "ENR-0000-0000-0000"


@pytest.fixture
def query_template_id(e2e_config):
    return e2e_config["program.enrollment.query.template.id"]


@pytest.fixture
def process_template_id(e2e_config):
    return e2e_config["program.enrollment.process.template.id"]


@pytest.fixture
def complete_template_id(e2e_config):
    return e2e_config["program.enrollment.complete.template.id"]


@pytest.fixture
def assignee_id(e2e_config):
    return e2e_config["program.enrollment.assignee.id"]


@pytest.fixture
def enrollment_data(program_id, licensee_id):
    return {
        "program": {"id": program_id},
        "parameters": {"ordering": []},
        "certificant": {"id": licensee_id},
        "licensee": {"id": licensee_id},
    }


@pytest.fixture
def status_flow_enrollment_data_factory():
    def factory(enrollment_id: str, template_id: str):
        return {
            "id": enrollment_id,
            "template": {
                "id": template_id,
                "content": "TEMPLATE_CONTENT",
            },
        }

    return factory


@pytest.fixture
def enrollment_status_message_factory():
    def factory(enrollment_id: str):
        return {
            "id": enrollment_id,
            "statusNotes": {
                "message": "Failing enrollment for E2E test",
            },
        }

    return factory


@pytest.fixture
def assignee_enrollment_data_factory(assignee_id):
    def factory(enrollment_id: str):
        return {
            "id": enrollment_id,
            "assignee": {"id": assignee_id},
        }

    return factory

import pytest


@pytest.fixture
def secondary_template_variant_data(short_uuid):
    return {
        "languageCode": "de-DE",
        "subject": f"e2e secondary template variant {short_uuid}",
        "body": f"e2e secondary template variant body {short_uuid}",
    }

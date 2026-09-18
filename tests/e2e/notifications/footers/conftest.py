import pytest

from tests.e2e.helper import (
    async_create_first_free_fixture_and_delete,
    create_first_free_fixture_and_delete,
)

# The platform allows one active footer per language and per account and only accepts the
# cultures it ships with. The create call is the claim on a language: a run tries these
# supported codes in order and moves on when the platform reports the language as taken, so
# concurrent runs sharing the operations account cannot both win the same code.
FOOTER_LANGUAGE_CODES = ("hu-HU", "nb-NO", "pt-PT", "ja-JP", "nl-NL", "it-IT", "fr-FR", "cs-CZ")


def _is_language_taken(error):
    return "already exists" in str(error)


@pytest.fixture
def footers_service(mpt_ops):
    return mpt_ops.notifications.footers


@pytest.fixture
def async_footers_service(async_mpt_ops):
    return async_mpt_ops.notifications.footers


@pytest.fixture
def footer_data(short_uuid):
    return {"content": f"e2e footer - please delete {short_uuid}"}


@pytest.fixture
def footer_candidates(footer_data):
    return [{**footer_data, "languageCode": code} for code in FOOTER_LANGUAGE_CODES]


@pytest.fixture
def created_footer(footers_service, footer_candidates):
    with create_first_free_fixture_and_delete(
        footers_service, footer_candidates, _is_language_taken
    ) as footer:
        yield footer


@pytest.fixture
async def async_created_footer(async_footers_service, footer_candidates):
    async with async_create_first_free_fixture_and_delete(
        async_footers_service, footer_candidates, _is_language_taken
    ) as footer:
        yield footer

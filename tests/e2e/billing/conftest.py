import asyncio
import pathlib
import time

import pytest

from mpt_api_client.exceptions import MPTError

# A journal accepts DELETE only in these states; the API answers 400 for any other.
DELETABLE_STATUSES = frozenset(("Draft", "Validated", "Error", "Enquiring"))
# Uploading charges moves a journal through Validating for a second or so before it
# settles. A journal that has been accepted and completed never becomes deletable.
TRANSIENT_STATUSES = frozenset(("Validating", "Generating"))
# A test that deletes the journal itself leaves nothing for the fixture to clean up.
ALREADY_GONE_STATUSES = frozenset(("Deleted",))
SETTLE_TIMEOUT_SECONDS = 10
POLL_INTERVAL_SECONDS = 0.5


def _report_teardown(message):
    print(f"TEARDOWN - {message}")  # noqa: WPS421


def _settled_status(journals_service, journal_id):
    deadline = time.monotonic() + SETTLE_TIMEOUT_SECONDS
    status = journals_service.get(journal_id).status
    while status in TRANSIENT_STATUSES and time.monotonic() < deadline:
        time.sleep(POLL_INTERVAL_SECONDS)
        status = journals_service.get(journal_id).status

    return status


def _delete_journal(journals_service, journal_id):
    try:
        status = _settled_status(journals_service, journal_id)
    except MPTError as error:
        _report_teardown(f"could not read billing journal {journal_id}: {error}")
        return

    if status in ALREADY_GONE_STATUSES:
        return

    if status not in DELETABLE_STATUSES:
        _report_teardown(f"billing journal {journal_id} not deletable in status {status}")
        return

    try:
        journals_service.delete(journal_id)
    except MPTError as error:
        _report_teardown(f"could not delete billing journal {journal_id}: {error}")


async def _async_settled_status(journals_service, journal_id):
    deadline = time.monotonic() + SETTLE_TIMEOUT_SECONDS
    journal = await journals_service.get(journal_id)
    while journal.status in TRANSIENT_STATUSES and time.monotonic() < deadline:
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
        journal = await journals_service.get(journal_id)

    return journal.status


async def _async_delete_journal(journals_service, journal_id):
    try:
        status = await _async_settled_status(journals_service, journal_id)
    except MPTError as error:
        _report_teardown(f"could not read billing journal {journal_id}: {error}")
        return

    if status in ALREADY_GONE_STATUSES:
        return

    if status not in DELETABLE_STATUSES:
        _report_teardown(f"billing journal {journal_id} not deletable in status {status}")
        return

    try:
        await journals_service.delete(journal_id)
    except MPTError as error:
        _report_teardown(f"could not delete billing journal {journal_id}: {error}")


@pytest.fixture
def delete_billing_journal():
    return _delete_journal


@pytest.fixture
def async_delete_billing_journal():
    return _async_delete_journal


@pytest.fixture
def billing_journal_fd():
    file_path = pathlib.Path("tests/data/test_billing_journal.jsonl").resolve()
    fd = file_path.open("rb")
    try:
        yield fd
    finally:
        fd.close()


@pytest.fixture
def billing_journal_id(e2e_config):
    return e2e_config["billing.journal.id"]

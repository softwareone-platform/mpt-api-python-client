import pathlib

import pytest


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

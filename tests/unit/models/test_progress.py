import datetime as dt
import io

import pytest

from mpt_api_client.models import (
    AsyncConsoleLoggerProgress,
    AsyncProgress,
    ConsoleLoggerProgress,
    Progress,
)


class FakeClock:
    """Deterministic monotonic clock advanced manually by tests."""

    def __init__(self):
        self.now: float = 0

    def __call__(self):
        return self.now


@pytest.fixture
def output():
    return io.StringIO()


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def console_progress(output, clock):
    return ConsoleLoggerProgress(interval=dt.timedelta(seconds=5), output=output, clock=clock)


@pytest.fixture
def async_console_progress(output, clock):
    return AsyncConsoleLoggerProgress(interval=dt.timedelta(seconds=5), output=output, clock=clock)


def test_console_progress_satisfies_protocol(console_progress):
    result = isinstance(console_progress, Progress)

    assert result is True


def test_async_console_progress_is_protocol(async_console_progress):
    result = isinstance(async_console_progress, AsyncProgress)

    assert result is True


def test_console_progress_default_clock(output):
    progress = ConsoleLoggerProgress(output=output)

    progress.item_processed()  # act

    assert output.getvalue() == "Fetched 1 of 0 - 0%\r"


def test_console_progress_first_item_writes(console_progress, output):
    console_progress.set_total_items(4)

    console_progress.item_processed()  # act

    assert output.getvalue() == "Fetched 1 of 4 - 25%\r"


def test_console_progress_throttles_in_interval(console_progress, output, clock):
    console_progress.set_total_items(4)
    console_progress.item_processed()
    clock.now = 4.9

    console_progress.item_processed()  # act

    assert output.getvalue() == "Fetched 1 of 4 - 25%\r"


def test_console_progress_writes_after_interval(console_progress, output, clock):
    console_progress.set_total_items(4)
    console_progress.item_processed()
    clock.now = 5.0

    console_progress.item_processed()  # act

    assert output.getvalue() == "Fetched 1 of 4 - 25%\rFetched 2 of 4 - 50%\r"


def test_console_progress_unknown_total(console_progress, output):
    console_progress.item_processed()  # act

    assert output.getvalue() == "Fetched 1 of 0 - 0%\r"


def test_console_progress_completed_always_writes(console_progress, output):
    console_progress.set_total_items(2)
    console_progress.item_processed()
    console_progress.item_processed()

    console_progress.completed()  # act

    assert output.getvalue() == "Fetched 1 of 2 - 50%\rFetched 2 of 2 - 100%\n"


async def test_async_console_progress_writes(async_console_progress, output):
    await async_console_progress.set_total_items(2)
    await async_console_progress.item_processed()

    await async_console_progress.completed()

    assert output.getvalue() == "Fetched 1 of 2 - 50%\rFetched 1 of 2 - 50%\n"

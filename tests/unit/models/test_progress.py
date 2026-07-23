import datetime as dt
import io

import pytest

from mpt_api_client.models import (
    AsyncBatchProgressReport,
    AsyncConsoleProgress,
    AsyncProgress,
    AsyncTimeProgressReport,
    BatchProgressReport,
    ConsoleProgress,
    Progress,
    TimeProgressReport,
)


class FakeClock:
    """Deterministic monotonic clock advanced manually by tests."""

    def __init__(self):
        self.now: float = 0

    def __call__(self):
        return self.now


class RecordingTimeProgress(TimeProgressReport):
    """Concrete time-based report recording every `report()` call."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reports = []

    def report(self, current, total, *, completed):
        self.reports.append((current, total, completed))


class RecordingBatchProgress(BatchProgressReport):
    """Concrete batch-based report recording every `report()` call."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reports = []

    def report(self, current, total, *, completed):
        self.reports.append((current, total, completed))


class AsyncRecordingTimeProgress(AsyncTimeProgressReport):
    """Concrete async time-based report recording every `report()` call."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reports = []

    async def report(self, current, total, *, completed):
        self.reports.append((current, total, completed))


class AsyncRecordingBatchProgress(AsyncBatchProgressReport):
    """Concrete async batch-based report recording every `report()` call."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reports = []

    async def report(self, current, total, *, completed):
        self.reports.append((current, total, completed))


@pytest.fixture
def output():
    return io.StringIO()


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def console_progress(output, clock):
    return ConsoleProgress(interval=dt.timedelta(seconds=5), output=output, clock=clock)


@pytest.fixture
def async_console_progress(output, clock):
    return AsyncConsoleProgress(interval=dt.timedelta(seconds=5), output=output, clock=clock)


@pytest.fixture
def time_progress(clock):
    return RecordingTimeProgress(interval=dt.timedelta(seconds=5), clock=clock)


@pytest.fixture
def batch_progress():
    return RecordingBatchProgress(batch_size=2)


def test_console_progress_satisfies_protocol(console_progress):
    result = isinstance(console_progress, Progress)

    assert result is True


def test_batch_progress_satisfies_protocol(batch_progress):
    result = isinstance(batch_progress, Progress)

    assert result is True


def test_async_console_progress_is_protocol(async_console_progress):
    result = isinstance(async_console_progress, AsyncProgress)

    assert result is True


def test_time_progress_first_item_reports(time_progress):
    time_progress.set_total_items(4)

    time_progress.item_processed()  # act

    assert time_progress.reports == [(1, 4, False)]


def test_time_progress_throttles_in_interval(time_progress, clock):
    time_progress.set_total_items(4)
    time_progress.item_processed()
    clock.now = 4.9

    time_progress.item_processed()  # act

    assert time_progress.reports == [(1, 4, False)]


def test_time_progress_reports_after_interval(time_progress, clock):
    time_progress.set_total_items(4)
    time_progress.item_processed()
    clock.now = 5.0

    time_progress.item_processed()  # act

    assert time_progress.reports == [(1, 4, False), (2, 4, False)]


def test_time_progress_completed_always_reports(time_progress):
    time_progress.set_total_items(2)
    time_progress.item_processed()
    time_progress.item_processed()

    time_progress.completed()  # act

    assert time_progress.reports == [(1, 2, False), (2, 2, True)]


def test_batch_progress_reports_every_batch(batch_progress):
    batch_progress.set_total_items(5)
    batch_progress.item_processed()
    batch_progress.item_processed()
    batch_progress.item_processed()

    batch_progress.item_processed()  # act

    assert batch_progress.reports == [(2, 5, False), (4, 5, False)]


def test_batch_progress_completed_always_reports(batch_progress):
    batch_progress.set_total_items(3)
    batch_progress.item_processed()

    batch_progress.completed()  # act

    assert batch_progress.reports == [(1, 3, True)]


def test_console_progress_default_clock(output):
    progress = ConsoleProgress(output=output)

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


async def test_async_time_progress_reports(clock):
    progress = AsyncRecordingTimeProgress(interval=dt.timedelta(seconds=5), clock=clock)
    await progress.set_total_items(2)
    await progress.item_processed()

    await progress.completed()  # act

    assert progress.reports == [(1, 2, False), (1, 2, True)]


async def test_async_batch_progress_reports():
    progress = AsyncRecordingBatchProgress(batch_size=2)
    await progress.set_total_items(4)
    await progress.item_processed()

    await progress.item_processed()  # act

    assert progress.reports == [(2, 4, False)]


async def test_async_console_progress_writes(async_console_progress, output):
    await async_console_progress.set_total_items(2)
    await async_console_progress.item_processed()

    await async_console_progress.completed()  # act

    assert output.getvalue() == "Fetched 1 of 2 - 50%\rFetched 1 of 2 - 50%\n"

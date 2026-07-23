import abc
import datetime as dt
import sys
import time
from collections.abc import Callable
from typing import Protocol, TextIO, override, runtime_checkable

DEFAULT_PROGRESS_INTERVAL = dt.timedelta(seconds=5)
DEFAULT_PROGRESS_BATCH_SIZE = 100


@runtime_checkable
class Progress(Protocol):
    """Receives iteration progress events from sync `iterate()` and `stream()`."""

    def set_total_items(self, total: int) -> None:
        """Called after each page fetch with the current pagination total."""

    def item_processed(self) -> None:
        """Called once per record, just before it is yielded."""

    def completed(self) -> None:
        """Called once when iteration finishes normally."""


@runtime_checkable
class AsyncProgress(Protocol):
    """Receives iteration progress events from async `iterate()` and `stream()`."""

    async def set_total_items(self, total: int) -> None:
        """Called after each page fetch with the current pagination total."""

    async def item_processed(self) -> None:
        """Called once per record, just before it is yielded."""

    async def completed(self) -> None:
        """Called once when iteration finishes normally."""


class _TimeThrottle:
    """Allows the first report and then at most one report per interval."""

    def __init__(self, interval: dt.timedelta, clock: Callable[[], float] | None) -> None:
        self._interval_seconds = interval.total_seconds()
        self._clock = clock or time.monotonic
        self._last_report: float | None = None

    def should_report(self) -> bool:
        now = self._clock()
        if self._last_report is None or now - self._last_report >= self._interval_seconds:
            self._last_report = now
            return True
        return False


def _write_progress(output: TextIO, current: int, total: int, *, completed: bool) -> None:
    """Write one `Fetched X of Y - P%` line; a total of 0 renders as 0%."""
    pct: float = 0
    if total:
        pct = 100 * current / total
    end = "\n" if completed else "\r"
    output.write(f"Fetched {current} of {total} - {pct:.0f}%{end}")
    output.flush()


class ProgressReport(abc.ABC):
    """Base `Progress` implementation that throttles calls to `report()`.

    Tracks the record count and pagination total, and calls the abstract
    `report()` whenever the throttling policy (`_should_report`) allows it.
    `completed()` always reports, with `completed=True`.
    """

    def __init__(self) -> None:
        """Initialize the count and total to zero."""
        self._total = 0
        self._count = 0

    def set_total_items(self, total: int) -> None:
        """Store the current pagination total."""
        self._total = total

    def item_processed(self) -> None:
        """Count the record and report when the throttling policy allows it."""
        self._count += 1
        if self._should_report():
            self.report(self._count, self._total, completed=False)

    def completed(self) -> None:
        """Report the final progress state."""
        self.report(self._count, self._total, completed=True)

    @abc.abstractmethod
    def report(self, current: int, total: int, *, completed: bool) -> None:
        """Render one progress update.

        Args:
            current: Number of records processed so far.
            total: Current pagination total, 0 when unknown.
            completed: True only for the final report emitted by `completed()`.
        """

    @abc.abstractmethod
    def _should_report(self) -> bool:
        """Decide whether `item_processed` should report now."""


class TimeProgressReport(ProgressReport, abc.ABC):
    """Abstract `ProgressReport` reporting at most once per time interval.

    The first processed record always reports.
    """

    def __init__(
        self,
        interval: dt.timedelta = DEFAULT_PROGRESS_INTERVAL,
        clock: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the time-based progress report.

        Args:
            interval: Minimum time between two reports.
            clock: Monotonic time source in seconds, injectable for testing.
                Defaults to `time.monotonic` when not provided.
        """
        super().__init__()
        self._throttle = _TimeThrottle(interval, clock)

    @override
    def _should_report(self) -> bool:
        return self._throttle.should_report()


class BatchProgressReport(ProgressReport, abc.ABC):
    """Abstract `ProgressReport` reporting once every `batch_size` records."""

    def __init__(self, batch_size: int = DEFAULT_PROGRESS_BATCH_SIZE) -> None:
        """Initialize the batch-based progress report.

        Args:
            batch_size: Number of records between two reports.
        """
        super().__init__()
        self._batch_size = batch_size

    @override
    def _should_report(self) -> bool:
        return self._count % self._batch_size == 0


class AsyncProgressReport(abc.ABC):
    """Async counterpart of `ProgressReport` for async `iterate()` and `stream()`."""

    def __init__(self) -> None:
        """Initialize the count and total to zero."""
        self._total = 0
        self._count = 0

    async def set_total_items(self, total: int) -> None:
        """Store the current pagination total."""
        self._total = total

    async def item_processed(self) -> None:
        """Count the record and report when the throttling policy allows it."""
        self._count += 1
        if self._should_report():
            await self.report(self._count, self._total, completed=False)

    async def completed(self) -> None:
        """Report the final progress state."""
        await self.report(self._count, self._total, completed=True)

    @abc.abstractmethod
    async def report(self, current: int, total: int, *, completed: bool) -> None:
        """Render one progress update.

        Args:
            current: Number of records processed so far.
            total: Current pagination total, 0 when unknown.
            completed: True only for the final report emitted by `completed()`.
        """

    @abc.abstractmethod
    def _should_report(self) -> bool:
        """Decide whether `item_processed` should report now."""


class AsyncTimeProgressReport(AsyncProgressReport, abc.ABC):
    """Abstract `AsyncProgressReport` reporting at most once per time interval.

    The first processed record always reports.
    """

    def __init__(
        self,
        interval: dt.timedelta = DEFAULT_PROGRESS_INTERVAL,
        clock: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the async time-based progress report.

        Args:
            interval: Minimum time between two reports.
            clock: Monotonic time source in seconds, injectable for testing.
                Defaults to `time.monotonic` when not provided.
        """
        super().__init__()
        self._throttle = _TimeThrottle(interval, clock)

    @override
    def _should_report(self) -> bool:
        return self._throttle.should_report()


class AsyncBatchProgressReport(AsyncProgressReport, abc.ABC):
    """Abstract `AsyncProgressReport` reporting once every `batch_size` records."""

    def __init__(self, batch_size: int = DEFAULT_PROGRESS_BATCH_SIZE) -> None:
        """Initialize the async batch-based progress report.

        Args:
            batch_size: Number of records between two reports.
        """
        super().__init__()
        self._batch_size = batch_size

    @override
    def _should_report(self) -> bool:
        return self._count % self._batch_size == 0


class ConsoleProgress(TimeProgressReport):
    """Time-throttled progress printing `Fetched X of Y - P%` to a text stream."""

    def __init__(
        self,
        interval: dt.timedelta = DEFAULT_PROGRESS_INTERVAL,
        output: TextIO = sys.stderr,
        clock: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the console progress.

        Args:
            interval: Minimum time between two progress lines.
            output: Text stream the progress lines are written to.
            clock: Monotonic time source in seconds, injectable for testing.
                Defaults to `time.monotonic` when not provided.
        """
        super().__init__(interval=interval, clock=clock)
        self._output = output

    @override
    def report(self, current: int, total: int, *, completed: bool) -> None:
        """Write one progress line, newline-terminated on completion."""
        _write_progress(self._output, current, total, completed=completed)


class AsyncConsoleProgress(AsyncTimeProgressReport):
    """Async counterpart of `ConsoleProgress` for async `iterate()` and `stream()`."""

    def __init__(
        self,
        interval: dt.timedelta = DEFAULT_PROGRESS_INTERVAL,
        output: TextIO = sys.stderr,
        clock: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the async console progress.

        Args:
            interval: Minimum time between two progress lines.
            output: Text stream the progress lines are written to.
            clock: Monotonic time source in seconds, injectable for testing.
                Defaults to `time.monotonic` when not provided.
        """
        super().__init__(interval=interval, clock=clock)
        self._output = output

    @override
    async def report(self, current: int, total: int, *, completed: bool) -> None:
        """Write one progress line, newline-terminated on completion."""
        _write_progress(self._output, current, total, completed=completed)

import datetime as dt
import sys
import time
from collections.abc import Callable
from typing import Protocol, TextIO, runtime_checkable

DEFAULT_PROGRESS_INTERVAL = dt.timedelta(seconds=5)


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


class ConsoleLoggerProgress:
    """Progress implementation printing `Fetched X of Y - P%`, throttled by an interval.

    `item_processed` writes at most once per `interval` (the first item always
    writes); `completed` always writes a final newline-terminated line. A total of
    0 is treated as unknown and rendered as 0%.
    """

    def __init__(
        self,
        interval: dt.timedelta = DEFAULT_PROGRESS_INTERVAL,
        output: TextIO = sys.stderr,
        clock: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the console progress logger.

        Args:
            interval: Minimum time between two progress lines.
            output: Text stream the progress lines are written to.
            clock: Monotonic time source in seconds, injectable for testing.
                Defaults to `time.monotonic` when not provided.
        """
        self._interval_seconds = interval.total_seconds()
        self._output = output
        self._clock = clock or time.monotonic
        self._total = 0
        self._count = 0
        self._last_write: float | None = None

    def set_total_items(self, total: int) -> None:
        """Store the current pagination total."""
        self._total = total

    def item_processed(self) -> None:
        """Count the record and write a progress line when the interval elapsed."""
        self._count += 1
        now = self._clock()
        if self._last_write is None or now - self._last_write >= self._interval_seconds:
            self._last_write = now
            self._write_progress("\r")

    def completed(self) -> None:
        """Write the final progress line."""
        self._write_progress("\n")

    def _write_progress(self, end: str) -> None:
        pct: float = 0
        if self._total:
            pct = 100 * self._count / self._total
        message = f"Fetched {self._count} of {self._total} - {pct:.0f}%"
        self._output.write(message + end)
        self._output.flush()


class AsyncConsoleLoggerProgress:
    """Async counterpart of `ConsoleLoggerProgress` for async `iterate()` and `stream()`."""

    def __init__(
        self,
        interval: dt.timedelta = DEFAULT_PROGRESS_INTERVAL,
        output: TextIO = sys.stderr,
        clock: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the async console progress logger.

        Args:
            interval: Minimum time between two progress lines.
            output: Text stream the progress lines are written to.
            clock: Monotonic time source in seconds, injectable for testing.
                Defaults to `time.monotonic` when not provided.
        """
        self._progress = ConsoleLoggerProgress(interval=interval, output=output, clock=clock)

    async def set_total_items(self, total: int) -> None:
        """Store the current pagination total."""
        self._progress.set_total_items(total)

    async def item_processed(self) -> None:
        """Count the record and write a progress line when the interval elapsed."""
        self._progress.item_processed()

    async def completed(self) -> None:
        """Write the final progress line."""
        self._progress.completed()

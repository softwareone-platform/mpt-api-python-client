import json
import string
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, NoReturn

from mpt_api_client.constants import (
    MPT_DATA_FIELD,
    MPT_META_FIELD,
    MPT_PAGINATION_FIELD,
    MPT_PAGINATION_TOTAL_FIELD,
)
from mpt_api_client.models.model import Resource

# The four characters JSON calls insignificant whitespace. A streaming response emits them
# between tokens as keep-alives while the server builds the result set, so they carry no
# information and are consumed as part of tokenizing.
JSON_WHITESPACE = " \t\n\r"

# Characters that can extend an already-decodable number: a fraction or an exponent.
NUMBER_CONTINUATIONS = ".eE"

# Every character a JSON value may begin with: a string, object, array, number, or one of
# the three literals. Anything else cannot become a value however much body follows, so it
# is a malformed envelope rather than a token still arriving.
VALUE_STARTS = '"{[-0123456789tfn'

# Failure messages the decoder reports for a token the buffer ran out inside: an open
# string absorbs any character until its closing quote arrives, and a \uXXXX escape is
# judged by the hex digits that have arrived rather than by the failure alone.
UNTERMINATED_STRING_MESSAGE = "Unterminated string starting at"
UNICODE_ESCAPE_MESSAGE = r"Invalid \uXXXX escape"

# Number of hex digits a \uXXXX escape carries after the `u`.
UNICODE_ESCAPE_DIGITS = 4

# Tokens a failed decode may be an unfinished prefix of: the three JSON literals, and a
# lone minus sign that only a number's digits can follow.
INCOMPLETE_VALUE_PREFIXES = ("null", "true", "false", "-")

# A number cut at the buffer end inside its fraction or exponent: the decoder stops the
# number before the continuation character, so inside a container the failure surfaces
# as a delimiter error whose remainder is exactly one of these tails.
NUMBER_CONTINUATION_TAILS = (".", "e", "E", "e+", "e-", "E+", "E-")

_DECODER = json.JSONDecoder()


@dataclass(frozen=True)
class StreamedRecord:
    """One record read from the envelope record array.

    Attributes:
        record: Deserialized record, still to be turned into a model or a deletion stub.
    """

    record: Resource


@dataclass(frozen=True)
class StreamedTotal:
    """The record total the envelope reported in ``$meta.pagination.total``.

    Attributes:
        total: Number of records the stream carries, the capped ``min(matches, N)``
            under a bounded ``limit=N``.
    """

    total: int


type StreamEvent = StreamedRecord | StreamedTotal


class _NeedMoreDataError(Exception):
    """Raised inside the parser when the buffer holds no complete token yet."""


class _State(Enum):
    ENVELOPE_START = auto()
    MEMBER_KEY_OR_END = auto()
    MEMBER_KEY = auto()
    MEMBER_COLON = auto()
    MEMBER_VALUE = auto()
    ARRAY_START = auto()
    ELEMENT_OR_END = auto()
    ELEMENT = auto()
    ELEMENT_SEPARATOR = auto()
    MEMBER_SEPARATOR = auto()
    ENVELOPE_END = auto()


def reported_total(meta_member: Any) -> StreamedTotal | None:
    """Read the record total out of an envelope ``$meta`` member.

    Args:
        meta_member: Deserialized ``$meta`` member of the envelope.

    Returns:
        The reported total, or None when the member declares no usable total.
    """
    if not isinstance(meta_member, dict):
        return None
    pagination = meta_member.get(MPT_PAGINATION_FIELD)
    if not isinstance(pagination, dict):
        return None
    total = pagination.get(MPT_PAGINATION_TOTAL_FIELD)
    # `bool` is a subclass of `int`, so a `true` total would otherwise report as 1. A
    # negative one is rejected the same way the MPT-Item-Count header rejects it, except
    # that an unusable total is ignored rather than raised: it is not a completeness signal.
    if isinstance(total, bool) or not isinstance(total, int) or total < 0:
        return None
    return StreamedTotal(total)


class JSONEnvelopeParser:
    """Incremental parser of the standard ``{$meta, data}`` list envelope.

    Feeding the response body chunk by chunk emits each record as soon as its closing
    brace arrives, so a consumer reads the head of a large export while its tail is
    still on the wire, and the whole body is never held in memory. Insignificant
    whitespace between tokens — the keep-alives a streaming response emits while the
    server works — is consumed while tokenizing and produces no events. A body that can
    no longer become a valid envelope is rejected at the chunk that proves it, rather
    than buffered until the stream ends.

    The envelope members may arrive in any order, so the reported total is emitted
    whenever ``$meta`` arrives, which is before the first record only if the server
    puts ``$meta`` first.
    """

    def __init__(self, data_field: str = MPT_DATA_FIELD) -> None:
        """Initialize an envelope parser holding no buffered body.

        Args:
            data_field: Envelope member carrying the record array, the same member the
                paged read path deserializes.
        """
        self._data_field = data_field
        self._buffer = ""
        self._position = 0
        self._member_key = ""
        self._state = _State.ENVELOPE_START
        self._decode_error: json.JSONDecodeError | None = None
        self._readers: dict[_State, Callable[[], StreamEvent | None]] = {
            _State.ENVELOPE_START: self._read_envelope_start,
            _State.MEMBER_KEY_OR_END: self._read_member_key_or_end,
            _State.MEMBER_KEY: self._read_member_key,
            _State.MEMBER_COLON: self._read_member_colon,
            _State.MEMBER_VALUE: self._read_member_value,
            _State.ARRAY_START: self._read_array_start,
            _State.ELEMENT_OR_END: self._read_element_or_end,
            _State.ELEMENT: self._read_element,
            _State.ELEMENT_SEPARATOR: self._read_element_separator,
            _State.MEMBER_SEPARATOR: self._read_member_separator,
        }

    def feed(self, chunk: str) -> Iterator[StreamEvent]:
        """Parse one body chunk, yielding the events it completed.

        Args:
            chunk: Next chunk of the response body, in arrival order.

        Yields:
            One event per record read from the record array, and one for the total the
            envelope reports.

        Raises:
            JSONDecodeError: If the chunk breaks the envelope, or if anything but
                insignificant whitespace follows a closed one.
        """
        self._buffer = self._buffer[self._position :] + chunk
        self._position = 0
        while self._state is not _State.ENVELOPE_END:
            try:
                event = self._readers[self._state]()
            except _NeedMoreDataError:
                return
            if event is not None:
                yield event
        self._reject_trailing_content()

    def close(self) -> None:
        """Verify the fed body closed the envelope and ended there.

        Raises:
            JSONDecodeError: If the body ended before the envelope was closed — either
                because it is malformed or because it was cut short — or if anything but
                insignificant whitespace follows the closed envelope.
        """
        if self._state is _State.ENVELOPE_END:
            self._reject_trailing_content()
            return
        if self._decode_error is not None:
            raise self._decode_error
        raise self._malformed_envelope("Unterminated JSON envelope")

    def _reject_trailing_content(self) -> None:
        """Reject anything but whitespace after the envelope, and drop what is left.

        The envelope is the whole body, so a suffix is a malformed response rather than
        something to ignore — but keep-alives may still land after the closing brace, and
        those are whitespace. Discarding the checked remainder keeps a tail of keep-alives
        from accumulating in the buffer.

        Raises:
            JSONDecodeError: If a non-whitespace suffix follows the envelope.
        """
        trailing = self._buffer[self._position :].strip(JSON_WHITESPACE)
        if trailing:
            raise self._malformed_envelope("Trailing content after the JSON envelope")
        self._position = len(self._buffer)

    def _read_envelope_start(self) -> None:
        self._expect("{")
        self._state = _State.MEMBER_KEY_OR_END

    def _read_member_key_or_end(self) -> None:
        if self._peek() == "}":
            self._take()
            self._state = _State.ENVELOPE_END
            return
        self._read_member_key()

    def _read_member_key(self) -> None:
        member_key = self._decode()
        if not isinstance(member_key, str):
            raise self._malformed_envelope("Envelope member name must be a string")
        self._member_key = member_key
        self._state = _State.MEMBER_COLON

    def _read_member_colon(self) -> None:
        self._expect(":")
        if self._member_key == self._data_field:
            self._state = _State.ARRAY_START
        else:
            self._state = _State.MEMBER_VALUE

    def _read_member_value(self) -> StreamEvent | None:
        member = self._decode()
        self._state = _State.MEMBER_SEPARATOR
        if self._member_key != MPT_META_FIELD:
            return None
        return reported_total(member)

    def _read_array_start(self) -> None:
        self._expect("[")
        self._state = _State.ELEMENT_OR_END

    def _read_element_or_end(self) -> StreamEvent | None:
        if self._peek() == "]":
            self._take()
            self._state = _State.MEMBER_SEPARATOR
            return None
        return self._read_element()

    def _read_element(self) -> StreamEvent:
        record = self._decode()
        if not isinstance(record, dict):
            raise self._malformed_envelope("Envelope record must be an object")
        self._state = _State.ELEMENT_SEPARATOR
        return StreamedRecord(record)

    def _read_element_separator(self) -> None:
        self._state = self._read_separator("]", _State.ELEMENT, _State.MEMBER_SEPARATOR)

    def _read_member_separator(self) -> None:
        self._state = self._read_separator("}", _State.MEMBER_KEY, _State.ENVELOPE_END)

    def _read_separator(self, closing: str, next_state: _State, end_state: _State) -> _State:
        separator = self._take()
        if separator == ",":
            return next_state
        if separator == closing:
            return end_state
        raise self._malformed_envelope(f"Expected ',' or '{closing}'")

    def _decode(self) -> Any:
        self._skip_whitespace()
        try:
            decoded, end = _DECODER.raw_decode(self._buffer, self._position)
        except json.JSONDecodeError as decode_error:
            self._defer_or_reject(decode_error)
        if isinstance(decoded, int | float) and self._number_may_continue(end):
            raise _NeedMoreDataError
        self._position = end
        self._decode_error = None
        return decoded

    def _defer_or_reject(self, decode_error: json.JSONDecodeError) -> NoReturn:
        """Defer a value the buffer ran out inside, or reject one that can never decode.

        An unfinished value and an impossible one raise the same error type, so the
        failure itself decides: wait only while a later chunk could still turn the
        buffered prefix into a value, and fail the moment it cannot — otherwise one bad
        token would buffer the whole remaining body for ``close()`` to reject.

        Args:
            decode_error: Failure ``raw_decode`` reported for the buffered prefix.

        Raises:
            JSONDecodeError: If the buffered text can never become a JSON value.
            _NeedMoreDataError: If the value may still be completed by a later chunk.
        """
        token = self._buffer[self._position]
        if token not in VALUE_STARTS:
            raise self._malformed_envelope(f"Expected a JSON value, found '{token}'")
        if not self._value_may_complete(decode_error):
            raise decode_error
        self._decode_error = decode_error
        raise _NeedMoreDataError from decode_error

    def _value_may_complete(self, decode_error: json.JSONDecodeError) -> bool:
        """Tell whether a later chunk could still complete the value that failed to decode.

        The check errs on the side of waiting: a continuation that can never arrive is
        still rejected, by ``close()``, when the body ends without completing it.

        Args:
            decode_error: Failure ``raw_decode`` reported for the buffered prefix.

        Returns:
            True when the failure means the buffered body ran out inside the token, so it
            is still in flight; False when the buffered text can never become a value,
            however much body follows.
        """
        if decode_error.pos >= len(self._buffer):
            return True
        if decode_error.msg.startswith(UNTERMINATED_STRING_MESSAGE):
            return True
        if decode_error.msg.startswith(UNICODE_ESCAPE_MESSAGE):
            return self._escape_may_complete(decode_error.pos)
        remainder = self._buffer[decode_error.pos :]
        if remainder in NUMBER_CONTINUATION_TAILS:
            return True
        return any(prefix.startswith(remainder) for prefix in INCOMPLETE_VALUE_PREFIXES)

    def _escape_may_complete(self, error_position: int) -> bool:
        r"""Tell whether a ``\uXXXX`` escape that failed to decode is still arriving.

        The decoder points this failure at the ``u`` of the escape and raises it even
        for four valid hex digits ending exactly at the buffer end, so the escape may
        still be completed only while every arrived digit is a hex digit and the escape
        reaches the end of the buffered body.

        Args:
            error_position: Failure position, at the ``u`` of the escape.

        Returns:
            True when the escape must wait for the next chunk.
        """
        digits_end = error_position + 1 + UNICODE_ESCAPE_DIGITS
        digits = self._buffer[error_position + 1 : digits_end]
        if digits_end < len(self._buffer):
            return False
        return all(digit in string.hexdigits for digit in digits)

    def _number_may_continue(self, end: int) -> bool:
        """Tell whether more body could still extend a number decoded up to ``end``.

        A number is the one JSON token a later chunk can lengthen, and `raw_decode` reads
        the longest prefix it can: `12` may become `1234`, `12.` a fraction, `1e` an
        exponent — and in the two latter cases the decoder stops *before* the leftover
        character rather than at the buffer end. Every other token type is
        self-terminating, so a prefix of one cannot decode at all.

        Args:
            end: Buffer offset the decoder stopped at.

        Returns:
            True when the number must wait for the next chunk.
        """
        if end >= len(self._buffer):
            return True
        return self._buffer[end] in NUMBER_CONTINUATIONS

    def _skip_whitespace(self) -> None:
        while self._position < len(self._buffer):
            if self._buffer[self._position] not in JSON_WHITESPACE:
                return
            self._position += 1
        raise _NeedMoreDataError

    def _peek(self) -> str:
        self._skip_whitespace()
        return self._buffer[self._position]

    def _take(self) -> str:
        token = self._peek()
        self._position += 1
        return token

    def _expect(self, expected: str) -> None:
        token = self._take()
        if token != expected:
            raise self._malformed_envelope(f"Expected '{expected}'")

    def _malformed_envelope(self, message: str) -> json.JSONDecodeError:
        return json.JSONDecodeError(message, self._buffer, self._position)

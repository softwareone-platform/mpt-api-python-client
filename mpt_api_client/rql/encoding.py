from urllib.parse import quote

VALUE_SAFE_CHARS = "*"
SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'


def rql_encode_value(raw_value: str) -> str:
    """Percent-encode an RQL value so that reserved characters travel as data.

    Every octet outside the unreserved set is percent-encoded, so characters that are
    delimiters in a URI query component (`&`, `#`, `+`, `%`) reach the server as part of
    the value instead of splitting or truncating the query. The RQL string-literal quote
    is encoded as well, so a value can no longer terminate its own literal and alter the
    surrounding expression.

    The `like`/`ilike` wildcard `*` is left literal: it is RQL pattern syntax rather than
    data, and it is a legal sub-delimiter in a query component.

    Args:
        raw_value: The already stringified value to encode.

    Returns:
        str: The percent-encoded value.
    """
    return quote(raw_value, safe=VALUE_SAFE_CHARS)


def rql_quote_value(raw_value: str) -> str:
    """Render a percent-encoded value as an RQL string literal, choosing the delimiter.

    An RQL literal may be delimited by `'` or `"`, and inside it every character is data
    except the delimiter itself. The delimiter is therefore chosen per value: percent-encoding
    cannot protect it, because the server decodes the query parameter before parsing the RQL
    expression, so an encoded quote reaches the parser as a quote and would end the literal
    early.

    Args:
        raw_value: The value before percent-encoding, used to pick the delimiter.

    Returns:
        str: The quoted, percent-encoded literal.

    Raises:
        ValueError: If the value contains both quote characters, which no RQL literal can
            express.
    """
    encoded = rql_encode_value(raw_value)
    if SINGLE_QUOTE not in raw_value:
        return f"{SINGLE_QUOTE}{encoded}{SINGLE_QUOTE}"
    if DOUBLE_QUOTE not in raw_value:
        return f"{DOUBLE_QUOTE}{encoded}{DOUBLE_QUOTE}"
    raise ValueError(
        "An RQL value cannot contain both a single and a double quote, because either "
        f"would end the string literal: {raw_value!r}",
    )


def rql_encode_field(field: str) -> str:
    """Percent-encode an RQL field path, preserving the dot nesting separator.

    Args:
        field: Field path, with nested fields separated by dots.

    Returns:
        str: The field path with every segment percent-encoded.
    """
    segments = field.split(".")
    return ".".join(quote(segment, safe="") for segment in segments)

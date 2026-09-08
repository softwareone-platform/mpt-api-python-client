APPLICATION_JSON = "application/json"
APPLICATION_JSONL = "application/jsonl"
APPLICATION_X_NDJSON = "application/x-ndjson"
MIMETYPE_EXCEL_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

MPT_STREAMING_HEADER = "MPT-Streaming"
MPT_STREAMING_ENABLED = "true"
MPT_ITEM_COUNT_HEADER = "MPT-Item-Count"

MPT_META_FIELD = "$meta"
MPT_META_DELETED_FIELD = "deleted"
MPT_META_OMITTED_FIELD = "omitted"
MPT_DATA_FIELD = "data"
MPT_PAGINATION_FIELD = "pagination"
MPT_PAGINATION_TOTAL_FIELD = "total"

CONTENT_TYPE_HEADER = "Content-Type"

# The byte order mark some producers still put in front of UTF-8 text. json.loads on raw
# bytes — how the paged read path parses a body — strips one before parsing, while httpx's
# iter_text decodes plain utf-8 and hands it through, so the streamed readers of both wire
# formats drop it themselves.
UTF8_BOM = "\ufeff"

# The four characters JSON calls insignificant whitespace: RFC 8259 fixes the set at
# ws = %x20 / %x09 / %x0A / %x0D. A streaming response emits them between tokens, and as
# whole lines, as keep-alives while the server builds the result set, so they carry no
# information and are consumed rather than reported. Nothing else is whitespace outside a
# JSON string value — U+00A0, U+2028, U+0085 and their kin are ordinary characters there —
# so a line made of anything else is malformed, not ignorable.
JSON_WHITESPACE = " \t\n\r"

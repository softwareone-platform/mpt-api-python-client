APPLICATION_JSON = "application/json"
APPLICATION_JSONL = "application/jsonl"
MIMETYPE_EXCEL_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

MPT_STREAMING_HEADER = "MPT-Streaming"
MPT_STREAMING_ENABLED = "true"
MPT_ITEM_COUNT_HEADER = "MPT-Item-Count"

MPT_META_FIELD = "$meta"
MPT_META_DELETED_FIELD = "deleted"
MPT_DATA_FIELD = "data"
MPT_PAGINATION_FIELD = "pagination"
MPT_PAGINATION_TOTAL_FIELD = "total"

CONTENT_TYPE_HEADER = "Content-Type"

# The byte order mark some producers still put in front of UTF-8 text. json.loads on raw
# bytes — how the paged read path parses a body — strips one before parsing, while httpx's
# iter_text decodes plain utf-8 and hands it through, so the streamed readers of both wire
# formats drop it themselves.
UTF8_BOM = "\ufeff"

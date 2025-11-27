def get_iso_dt_str(dt_obj) -> str:
    """Convert datetime to ISO 8601 string."""
    return dt_obj.isoformat(timespec="milliseconds").replace("+00:00", "Z")

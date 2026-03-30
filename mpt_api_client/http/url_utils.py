def join_url_path(base: str, *segments: str) -> str:
    """Join *segments* onto *base* as literal path components.

    Unlike :func:`urllib.parse.urljoin`, this function **never** interprets a
    segment as an absolute path or URL it always appends.

    Args:
        base: The base URL path (e.g. ``/public/v1/billing/journals``).
        *segments: One or more path segments to append
            (e.g. ``"JRN-123"``, ``"upload"``).

    Returns:
        The joined path with exactly one ``/`` between each part and no
        trailing slash.

    Examples:
        >>> join_url_path("/api/v1/orders", "ORD-001")
        '/api/v1/orders/ORD-001'
        >>> join_url_path("/api/v1/orders", "ORD-001", "complete")
        '/api/v1/orders/ORD-001/complete'
        >>> join_url_path("/api/v1/orders/", "/ORD-001/")
        '/api/v1/orders/ORD-001'
    """
    parts = [base.rstrip("/")]
    parts.extend(seg.strip("/") for seg in segments if seg)
    return "/".join(parts)

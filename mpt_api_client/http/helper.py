from mpt_api_client.http.types import QueryParam


def prepare_query_params(query_params: QueryParam | None) -> dict[str, str] | None:
    """
    Prepare and clean the query params dict.

    Converts all params to string and removes any value that is None.

    Args:
        query_params: dict of query params.

    Returns:
        dict or None if the params were not present.

    """
    if not query_params:
        return None
    clean_params = {
        param_name: str(param_value)
        for param_name, param_value in query_params.items()
        if param_value is not None
    }
    return clean_params or None

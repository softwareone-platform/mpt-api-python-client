from mpt_api_client.constants import APPLICATION_JSON
from mpt_api_client.http.async_client import AsyncHTTPClient
from mpt_api_client.http.client import HTTPClient
from mpt_api_client.http.query_options import QueryOptions
from mpt_api_client.http.types import QueryParam, Response
from mpt_api_client.http.url_utils import join_url_path
from mpt_api_client.models.collection import ResourceList
from mpt_api_client.models.model import Model, ResourceData  # NOSONAR

_JsonPayload = ResourceData | ResourceList | None


class ResourceAccessor[ResourceModel: Model]:  # NOSONAR
    """Synchronous accessor bound to a single resource URL.

    Provides ``.get()``, ``.post()``, ``.put()``, ``.delete()`` helpers that
    deserialize the response into a ``Model``, and a ``.do_request()`` escape
    hatch that returns the raw ``Response``.
    """

    def __init__(
        self,
        http_client: HTTPClient,
        resource_url: str,
        model_class: type[ResourceModel],
    ) -> None:
        self._http_client = http_client
        self._resource_url = resource_url
        self._model_class = model_class

    # -- raw request ---------------------------------------------------------

    def do_request(  # noqa: WPS211
        self,
        method: str,
        action: str | None = None,
        *,
        json: _JsonPayload = None,
        query_params: QueryParam | None = None,
        headers: dict[str, str] | None = None,
        options: QueryOptions | None = None,
    ) -> Response:
        """Perform an HTTP request and return the raw ``Response``.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE …).
            action: Optional sub-path appended after the resource id.
            json: JSON body payload.
            query_params: Query-string parameters.
            headers: Extra HTTP headers.
            options: Query options.
        """
        url = join_url_path(self._resource_url, action) if action else self._resource_url
        return self._http_client.request(
            method, url, json=json, query_params=query_params, headers=headers, options=options
        )

    # -- model-returning helpers ---------------------------------------------

    def get(
        self,
        action: str | None = None,
        *,
        query_params: QueryParam | None = None,
        options: QueryOptions | None = None,
    ) -> ResourceModel:
        """``GET`` the resource (optionally with a sub-action)."""
        return self._action("GET", action, query_params=query_params, options=options)

    def post(
        self,
        action: str | None = None,
        *,
        json: _JsonPayload = None,
        query_params: QueryParam | None = None,
    ) -> ResourceModel:
        """``POST`` to the resource (optionally with a sub-action)."""
        return self._action("POST", action, json=json, query_params=query_params)

    def put(
        self,
        action: str | None = None,
        *,
        json: _JsonPayload = None,
        query_params: QueryParam | None = None,
    ) -> ResourceModel:
        """``PUT`` to the resource (optionally with a sub-action)."""
        return self._action("PUT", action, json=json, query_params=query_params)

    def delete(self) -> None:
        """``DELETE`` the resource."""
        self.do_request("DELETE")

    def _action(
        self,
        method: str,
        action: str | None = None,
        *,
        json: _JsonPayload = None,
        query_params: QueryParam | None = None,
        options: QueryOptions | None = None,
    ) -> ResourceModel:
        response = self.do_request(
            method,
            action,
            json=json,
            query_params=query_params,
            headers={"Accept": APPLICATION_JSON},
            options=options,
        )
        return self._model_class.from_response(response)


class AsyncResourceAccessor[ResourceModel: Model]:  # NOSONAR
    """Asynchronous accessor bound to a single resource URL.

    Async counterpart of :class:`ResourceAccessor`.
    """

    def __init__(
        self,
        http_client: AsyncHTTPClient,
        resource_url: str,
        model_class: type[ResourceModel],
    ) -> None:
        self._http_client = http_client
        self._resource_url = resource_url
        self._model_class = model_class

    # -- raw request ---------------------------------------------------------

    async def do_request(  # noqa: WPS211
        self,
        method: str,
        action: str | None = None,
        *,
        json: _JsonPayload = None,
        query_params: QueryParam | None = None,
        headers: dict[str, str] | None = None,
        options: QueryOptions | None = None,
    ) -> Response:
        """Perform an HTTP request and return the raw ``Response``.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE …).
            action: Optional sub-path appended after the resource id.
            json: JSON body payload.
            query_params: Query-string parameters.
            headers: Extra HTTP headers.
            options: Additional options for the request.
        """
        url = join_url_path(self._resource_url, action) if action else self._resource_url
        return await self._http_client.request(
            method, url, json=json, query_params=query_params, headers=headers, options=options
        )

    # -- model-returning helpers ---------------------------------------------

    async def get(
        self,
        action: str | None = None,
        *,
        query_params: QueryParam | None = None,
        options: QueryOptions | None = None,
    ) -> ResourceModel:
        """``GET`` the resource (optionally with a sub-action)."""
        return await self._action("GET", action, query_params=query_params, options=options)

    async def post(
        self,
        action: str | None = None,
        *,
        json: _JsonPayload = None,
        query_params: QueryParam | None = None,
    ) -> ResourceModel:
        """``POST`` to the resource (optionally with a sub-action)."""
        return await self._action("POST", action, json=json, query_params=query_params)

    async def put(
        self,
        action: str | None = None,
        *,
        json: _JsonPayload = None,
        query_params: QueryParam | None = None,
    ) -> ResourceModel:
        """``PUT`` to the resource (optionally with a sub-action)."""
        return await self._action("PUT", action, json=json, query_params=query_params)

    async def delete(self) -> None:
        """``DELETE`` the resource."""
        await self.do_request("DELETE")

    async def _action(
        self,
        method: str,
        action: str | None = None,
        *,
        json: _JsonPayload = None,
        query_params: QueryParam | None = None,
        options: QueryOptions | None = None,
    ) -> ResourceModel:
        response = await self.do_request(
            method,
            action,
            json=json,
            query_params=query_params,
            headers={"Accept": APPLICATION_JSON},
            options=options,
        )
        return self._model_class.from_response(response)

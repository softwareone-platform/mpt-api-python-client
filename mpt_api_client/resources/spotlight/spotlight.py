from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.spotlight.objects import (
    AsyncSpotlightObjectsService,
    SpotlightObjectsService,
)
from mpt_api_client.resources.spotlight.queries import (
    AsyncSpotlightQueriesService,
    SpotlightQueriesService,
)


class Spotlight:
    """Spotlight MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def objects(self) -> SpotlightObjectsService:  # noqa: WPS110
        """Spotlight Objects service."""
        return SpotlightObjectsService(http_client=self.http_client)

    @property
    def queries(self) -> SpotlightQueriesService:  # noqa: WPS110
        """Spotlight Queries service."""
        return SpotlightQueriesService(http_client=self.http_client)


class AsyncSpotlight:
    """Spotlight MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def objects(self) -> AsyncSpotlightObjectsService:  # noqa: WPS110
        """Spotlight Objects service."""
        return AsyncSpotlightObjectsService(http_client=self.http_client)

    @property
    def queries(self) -> AsyncSpotlightQueriesService:  # noqa: WPS110
        """Spotlight Queries service."""
        return AsyncSpotlightQueriesService(http_client=self.http_client)

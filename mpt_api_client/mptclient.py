from mpt_api_client.http.client import HTTPClient
from mpt_api_client.registry import Registry, commerce
from mpt_api_client.resources import OrderCollectionClientBase


class MPTClientBase:
    """MPT API Client Base."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        registry: Registry | None = None,
        http_client: HTTPClient | None = None,
    ):
        self.http_client = http_client or HTTPClient(base_url=base_url, api_token=api_key)
        self.registry: Registry = registry or Registry()

    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        return self.registry.get(name)(http_client=self.http_client)


class MPTClient(MPTClientBase):
    """MPT API Client."""

    @property
    def commerce(self) -> "CommerceMpt":
        """Commerce MPT API Client.

        The Commerce API provides a comprehensive set of endpoints
        for managing agreements, requests, subscriptions, and orders
        within a vendor-client-ops ecosystem.
        """
        return CommerceMpt(http_client=self.http_client, registry=commerce)


class CommerceMpt(MPTClientBase):
    """Commerce MPT API Client."""

    @property
    def orders(self) -> OrderCollectionClientBase:
        """Orders MPT API collection.

        The Orders API provides a comprehensive set of endpoints
        for creating, updating, and retrieving orders.



        Returns: Order collection

        Examples:
            active=RQLQuery("status=active")
            for order in mpt.orders.filter(active).iterate():
               [...]

        """
        return self.registry.get("orders")(http_client=self.http_client)  # type: ignore[return-value]

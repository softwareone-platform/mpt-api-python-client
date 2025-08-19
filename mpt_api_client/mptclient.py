from mpt_api_client.http.client import HTTPClient
from mpt_api_client.registry import Registry, commerce
from mpt_api_client.resources import OrderCollectionClient


class MPTClient:
    """MPT API Client."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        registry: Registry | None = None,
        mpt_client: HTTPClient | None = None,
    ):
        self.mpt_client = mpt_client or HTTPClient(base_url=base_url, api_token=api_key)
        self.registry: Registry = registry or Registry()

    def __getattr__(self, name):  # type: ignore[no-untyped-def]
        return self.registry.get(name)(client=self.mpt_client)

    @property
    def commerce(self) -> "CommerceMpt":
        """Commerce MPT API Client.

        The Commerce API provides a comprehensive set of endpoints
        for managing agreements, requests, subscriptions, and orders
        within a vendor-client-ops ecosystem.
        """
        return CommerceMpt(mpt_client=self.mpt_client, registry=commerce)


class CommerceMpt(MPTClient):
    """Commerce MPT API Client."""

    @property
    def orders(self) -> OrderCollectionClient:
        """Orders MPT API collection.

        The Orders API provides a comprehensive set of endpoints
        for creating, updating, and retrieving orders.



        Returns: Order collection

        Examples:
            active=RQLQuery("status=active")
            for order in mpt.orders.filter(active).iterate():
               [...]

        """
        return self.registry.get("orders")(client=self.mpt_client)  # type: ignore[return-value]

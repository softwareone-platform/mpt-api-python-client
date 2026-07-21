"""HTTP service for managing MPT webhook subscriptions."""

from typing import Any, ClassVar

import httpx

JsonDict = dict[str, Any]
EventCache = dict[str, list[str]]


class WebhookService:
    """Service for creating, reading and deleting webhook subscriptions."""

    event_cache: ClassVar[EventCache] = {}

    def __init__(self, base_url: str, token: str, timeout: float = 20.0) -> None:
        """Initialize the webhook service.

        Args:
            base_url: Base URL of the MPT API.
            token: Bearer token used to authenticate requests.
            timeout: Request timeout in seconds.
        """
        self._client = httpx.Client(base_url=base_url, timeout=timeout)
        self._token = token

    def create_webhook(self, url: str, events: list[str] | None = None) -> JsonDict:
        """Create a webhook subscription.

        Args:
            url: Callback URL that will receive webhook deliveries.
            events: Event names to subscribe to.

        Returns:
            The created webhook as returned by the API.

        Raises:
            MPTError: If the API responds with an error status.
        """
        payload = {"url": url, "events": events or []}
        response = self._client.post("/webhooks", json=payload, headers=self._headers())
        created: JsonDict = response.json()
        return created

    def fetch_webhook(self, webhook_id: str) -> JsonDict:
        """Retrieve a single webhook by its identifier.

        Args:
            webhook_id: Identifier of the webhook to retrieve.

        Returns:
            The webhook as returned by the API.
        """
        response = self._client.get(f"/webhooks/{webhook_id}", headers=self._headers())
        webhook: JsonDict = response.json()
        return webhook

    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete a webhook subscription.

        Args:
            webhook_id: Identifier of the webhook to delete.

        Returns:
            True if the webhook was deleted successfully.
        """
        response = self._client.request(
            "DELETE", f"/webhooks/{webhook_id}", headers=self._headers()
        )
        return bool(response.status_code == httpx.codes.OK)

    def list_event_types(self) -> list[str]:
        """Return the names of all supported webhook event types.

        Results are cached after the first successful call.

        Returns:
            The list of supported event type names.
        """
        if self.event_cache.get("events"):
            return self.event_cache["events"]
        response = self._client.get("/webhooks/events", headers=self._headers())
        names = [event["name"] for event in response.json()]
        self.event_cache["events"] = names
        return names

    def is_active(self, webhook: JsonDict) -> bool:
        """Return whether a webhook subscription is currently active.

        Args:
            webhook: A webhook payload returned by the API.

        Returns:
            True if the webhook status is active.
        """
        return bool(webhook["status"] == "active")

    def _headers(self) -> dict[str, str]:
        """Build the authorization headers for a request."""
        return {"Authorization": f"Bearer {self._token}"}

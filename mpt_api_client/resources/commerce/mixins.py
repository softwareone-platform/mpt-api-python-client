import httpx

from mpt_api_client.models import ResourceData


class ValidateMixin[BaseModel]:
    """Validate mixin."""

    def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> BaseModel:
        """Switch order to validate state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "validate", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class ProcessMixin[BaseModel]:
    """Process mixin."""

    def process(self, resource_id: str, resource_data: ResourceData | None = None) -> BaseModel:
        """Switch order to process state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "process", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class QueryMixin[BaseModel]:
    """Query mixin."""

    def query(self, resource_id: str, resource_data: ResourceData | None = None) -> BaseModel:
        """Switch order to query state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "query", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class CompleteMixin[BaseModel]:
    """Complete mixin."""

    def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> BaseModel:
        """Switch order to complete state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "complete", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class FailMixin[BaseModel]:
    """Fail mixin."""

    def fail(self, resource_id: str, resource_data: ResourceData | None = None) -> BaseModel:
        """Switch order to fail state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource_action(resource_id, "POST", "fail", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class TemplateMixin:
    """Template mixin."""

    def template(self, resource_id: str) -> str:
        """Render order template.

        Args:
            resource_id: Order resource ID

        Returns:
            Order template text in markdown format.
        """
        response: httpx.Response = self._resource_do_request(resource_id, "GET", "template")  # type: ignore[attr-defined]
        return response.text


class AsyncValidateMixin[BaseModel]:
    """Async Validate Mixin."""

    async def validate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> BaseModel:
        """Switch order to validate state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "validate", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncProcessMixin[BaseModel]:
    """Async Process Mixin."""

    async def process(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> BaseModel:
        """Switch order to process state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "process", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncQueryMixin[BaseModel]:
    """Async Query Mixin."""

    async def query(self, resource_id: str, resource_data: ResourceData | None = None) -> BaseModel:
        """Switch order to query state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "query", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncCompleteMixin[BaseModel]:
    """Async Complete Mixin."""

    async def complete(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> BaseModel:
        """Switch order to complete state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "complete", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncFailMixin[BaseModel]:
    """Async Fail Mixin."""

    async def fail(self, resource_id: str, resource_data: ResourceData | None = None) -> BaseModel:
        """Switch order to fail state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource_action(resource_id, "POST", "fail", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncTemplateMixin:
    """Async Template Mixin."""

    async def template(self, resource_id: str) -> str:
        """Render order template.

        Args:
            resource_id: Order resource ID

        Returns:
            Order template text in markdown format.
        """
        response: httpx.Response = await self._resource_do_request(resource_id, "GET", "template")  # type: ignore[attr-defined]
        return response.text

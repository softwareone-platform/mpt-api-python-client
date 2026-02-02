from mpt_api_client.http.mixins.create_mixin import AsyncCreateMixin, CreateMixin
from mpt_api_client.http.mixins.delete_mixin import AsyncDeleteMixin, DeleteMixin
from mpt_api_client.http.mixins.get_mixin import AsyncGetMixin, GetMixin
from mpt_api_client.http.mixins.update_mixin import AsyncUpdateMixin, UpdateMixin


class ModifiableResourceMixin[Model](GetMixin[Model], UpdateMixin[Model], DeleteMixin):
    """Editable resource mixin allows to read and update a resource resources."""


class AsyncModifiableResourceMixin[Model](
    AsyncGetMixin[Model], AsyncUpdateMixin[Model], AsyncDeleteMixin
):
    """Editable resource mixin allows to read and update a resource resources."""


class ManagedResourceMixin[Model](CreateMixin[Model], ModifiableResourceMixin[Model]):
    """Managed resource mixin allows to read, create, update and delete a resource resources."""


class AsyncManagedResourceMixin[Model](
    AsyncCreateMixin[Model], AsyncModifiableResourceMixin[Model]
):
    """Managed resource mixin allows to read, create, update and delete a resource resources."""

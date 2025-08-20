from mpt_api_client.http.collection import CollectionBaseClient
from mpt_api_client.models import Collection, Resource
from mpt_api_client.registry import commerce


class Order(Resource):
    """Order resource."""


@commerce("orders")
class OrderCollectionClient(CollectionBaseClient[Order]):
    """Orders client."""

    _endpoint = "/public/v1/commerce/orders"
    _resource_class = Order
    _collection_class = Collection[Order]

from mpt_api_client.http.collection import CollectionBaseClient
from mpt_api_client.models import Collection, Resource
from mpt_api_client.register import mpt


class Order(Resource):
    """Order resource."""


@mpt("orders")
class OrderCollectionClient(CollectionBaseClient[Order]):
    """Orders client."""

    _endpoint = "/api/v1/orders"
    _resource_class = Order
    _collection_class = Collection[Order]

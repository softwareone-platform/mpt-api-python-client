from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    AsyncStreamJSONLMixin,
    CollectionMixin,
    GetMixin,
    StreamJSONLMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class StatementCharge(Model):
    """Statement Charge resource.

    Attributes:
        revision: Charge revision number.
        external_ids: External identifiers associated with the charge.
        search: Search-related details for the charge.
        period: Period during which the charge is applicable.
        quantity: Quantity associated with the charge.
        price: Pricing details for the charge.
        description: Description of the charge, if applicable.
        attributes: Additional attributes for the charge.
        billing_type: Billing type of the charge.
        statement_type: Type of statement associated with the charge.
        journal: Reference to the journal.
        ledger: Reference to the ledger.
        custom_ledger: Reference to the custom ledger.
        parent: Reference to the parent charge.
        upload: Upload status and details, visible to vendors or operations.
        processing: Processing status and details, visible to operations.
        licensee: Reference to the licensee.
        agreement: Reference to the agreement.
        subscription: Reference to the subscription.
        line: Agreement line associated with the charge, if applicable.
        order: Reference to the order.
        asset: Reference to the asset.
        item: Reference to the product item.
        authorization: Reference to the authorization.
        statement: Reference to the statement.
        buyer: Reference to the buyer.
        vendor: Reference to the vendor account.
        seller: Reference to the seller.
        erp_data: ERP-related data for the charge.
        split: Details about the charge split, if applicable.
        reconciliation: Reconciliation information for the charge.
        audit: Container for audit-related events for the charge.
    """

    revision: int | None
    external_ids: BaseModel | None
    search: BaseModel | None
    period: BaseModel | None
    quantity: float | None
    price: BaseModel | None
    description: BaseModel | None
    attributes: BaseModel | None
    billing_type: str | None
    statement_type: str | None
    journal: BaseModel | None
    ledger: BaseModel | None
    custom_ledger: BaseModel | None
    parent: BaseModel | None
    upload: BaseModel | None
    processing: BaseModel | None
    licensee: BaseModel | None
    agreement: BaseModel | None
    subscription: BaseModel | None
    line: BaseModel | None
    order: BaseModel | None
    asset: BaseModel | None
    item: BaseModel | None
    authorization: BaseModel | None
    statement: BaseModel | None
    buyer: BaseModel | None
    vendor: BaseModel | None
    seller: BaseModel | None
    erp_data: BaseModel | None
    split: BaseModel | None
    reconciliation: BaseModel | None
    audit: BaseModel | None


class StatementChargesServiceConfig:
    """Statement Charges service configuration."""

    _endpoint = "/public/v1/billing/statements/{statement_id}/charges"
    _model_class = StatementCharge
    _collection_key = "data"


class StatementChargesService(
    StreamJSONLMixin[StatementCharge],
    GetMixin[StatementCharge],
    CollectionMixin[StatementCharge],
    Service[StatementCharge],
    StatementChargesServiceConfig,
):
    """Statement Charges service."""


class AsyncStatementChargesService(
    AsyncStreamJSONLMixin[StatementCharge],
    AsyncGetMixin[StatementCharge],
    AsyncCollectionMixin[StatementCharge],
    AsyncService[StatementCharge],
    StatementChargesServiceConfig,
):
    """Async Statement Charges service."""

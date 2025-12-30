import pytest


@pytest.fixture
def credit_memo_id(e2e_config):
    return e2e_config["billing.credit_memo.id"]


@pytest.fixture
def invalid_credit_memo_id():
    return "CMO-0000-0000"


@pytest.fixture
def credit_memo_factory(
    agreement_id,
    licensee_id,
    buyer_account_id,
    seller_account_id,
    commerce_product_id,
    account_id,
):
    def factory(
        document_number: str = "e2e-credit-memo-001",
    ):
        return {
            "agreement": {"id": agreement_id},
            "licensee": {"id": licensee_id},
            "client": {"id": buyer_account_id},
            "vendor": {"id": account_id},
            "seller": {"id": seller_account_id},
            "status": "Issued",
            "lines": [{}],
            "documentNo": document_number,
            "product": {"id": commerce_product_id},
            "price": {
                "currency": "USD",
                "margin": 10,
                "totalPP": 100,
                "totalSP": 100,
                "totalST": 5,
                "totalGT": 5,
            },
            "erpData": {
                "addresses": {},
                "documentNo": document_number,
                "navisionCountryCode": "US",
                "postingDate": "2025-12-01T10:00:00.000Z",
            }
        }

    return factory

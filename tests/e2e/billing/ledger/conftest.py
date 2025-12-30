import pytest


@pytest.fixture
def ledger_id(e2e_config):
    return e2e_config["billing.ledger.id"]


@pytest.fixture
def invalid_ledger_id():
    return "LED-0000-0000"


@pytest.fixture
def invoice_factory(
    billing_journal_id,
    commerce_authorization_id,
    seller_account_id,
    commerce_product_id,
):
    def factory():
        return {
            "journal": {"id": billing_journal_id},
            "authorization": {"id": commerce_authorization_id},
            "seller": {"id": seller_account_id},
            "product": {"id": commerce_product_id},
            "owner": {},
            "assignee": {},
            "price": {
                "markup": 5,
                "margin": 10,
                "totalPP": 100,
                "totalSP": 100,
                "currency": "USD",
            },
        }

    return factory

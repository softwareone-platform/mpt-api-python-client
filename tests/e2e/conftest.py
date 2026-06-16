import json
import logging
import os
import pathlib
import uuid

import pytest
from reportportal_client import RPLogger

from mpt_api_client import AsyncMPTClient, BearerTokenAuthentication, MPTClient
from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("MPT_API_BASE_URL")


@pytest.fixture(scope="session")
def vendor_token():
    token = os.getenv("MPT_API_TOKEN_VENDOR")
    if not token:
        raise RuntimeError("Required environment variable 'MPT_API_TOKEN_VENDOR' is not set")
    return token


@pytest.fixture(scope="session")
def operations_token():
    token = os.getenv("MPT_API_TOKEN_OPERATIONS")
    if not token:
        raise RuntimeError("Required environment variable 'MPT_API_TOKEN_OPERATIONS' is not set")
    return token


@pytest.fixture(scope="session")
def client_token():
    token = os.getenv("MPT_API_TOKEN_CLIENT")
    if not token:
        raise RuntimeError("Required environment variable 'MPT_API_TOKEN_CLIENT' is not set")
    return token


@pytest.fixture
def extension_secret():
    secret = os.getenv("MPT_API_TOKEN_EXTENSION")
    if not secret:
        pytest.skip("MPT_API_TOKEN_EXTENSION not set")
    return secret


@pytest.fixture
def installation_account_id(mpt_vendor, e2e_config):
    installations_service = mpt_vendor.integration.installations
    installation = installations_service.create({
        "extension": {"id": e2e_config["integration.extension.id"]},
        "modules": [
            {"id": "MOD-0478"},
            {"id": "MOD-1239"},
            {"id": "MOD-1756"},
            {"id": "MOD-4525"},
            {"id": "MOD-8352"},
            {"id": "MOD-8743"},
            {"id": "MOD-9042"},
        ],
    })

    yield installation.account.id

    try:
        installations_service.delete(installation.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete installation {installation.id}: {error.title}")  # noqa: WPS421


@pytest.fixture(scope="session")
def api_timeout():
    return float(os.getenv("MPT_API_TIMEOUT", "60.0"))


@pytest.fixture
def mpt_vendor(base_url, api_timeout, vendor_token):
    return MPTClient.from_config(
        authentication=BearerTokenAuthentication(vendor_token),
        base_url=base_url,
        timeout=api_timeout,
    )


@pytest.fixture
def async_mpt_vendor(base_url, api_timeout, vendor_token):
    return AsyncMPTClient.from_config(
        authentication=BearerTokenAuthentication(vendor_token),
        base_url=base_url,
        timeout=api_timeout,
    )


@pytest.fixture
def mpt_ops(base_url, api_timeout, operations_token):
    return MPTClient.from_config(
        authentication=BearerTokenAuthentication(operations_token),
        base_url=base_url,
        timeout=api_timeout,
    )


@pytest.fixture
def async_mpt_ops(base_url, api_timeout, operations_token):
    return AsyncMPTClient.from_config(
        authentication=BearerTokenAuthentication(operations_token),
        base_url=base_url,
        timeout=api_timeout,
    )


@pytest.fixture
def mpt_client(base_url, api_timeout, client_token):
    return MPTClient.from_config(
        authentication=BearerTokenAuthentication(client_token),
        base_url=base_url,
        timeout=api_timeout,
    )


@pytest.fixture
def async_mpt_client(base_url, api_timeout, client_token):
    return AsyncMPTClient.from_config(
        authentication=BearerTokenAuthentication(client_token),
        base_url=base_url,
        timeout=api_timeout,
    )


@pytest.fixture(scope="module")
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)
    return logger


@pytest.fixture(scope="session")
def logger():
    return logging.getLogger("E2E")


@pytest.fixture(scope="session")
def project_root_path():
    return pathlib.Path(__file__).parent.parent.parent


@pytest.fixture
def pdf_fd():
    icon_path = pathlib.Path(__file__).parent / "empty.pdf"
    with pathlib.Path.open(icon_path, "rb") as fd:
        yield fd


@pytest.fixture(scope="session")
def pdf_url():
    return "https://sample-files.com/downloads/documents/pdf/basic-text.pdf"


@pytest.fixture(scope="session")
def jpg_url():
    return "https://sample-files.com/downloads/images/jpg/color_test_800x600_118kb.jpg"


@pytest.fixture(scope="session")
def video_url():
    return "https://www.youtube.com/watch?v=DUMMY1_0000"


@pytest.fixture(scope="session")
def e2e_config(project_root_path):
    filename = os.getenv("TEST_CONFIG_FILE", "e2e_config.test.json")
    file_path = project_root_path.joinpath(filename)
    return json.loads(file_path.read_text())


@pytest.fixture(scope="session")
def product_id(e2e_config):
    return e2e_config["catalog.product.id"]


@pytest.fixture
def short_uuid():
    return uuid.uuid4().hex[:8]


@pytest.fixture
def uuid_str():
    return str(uuid.uuid4())


@pytest.fixture
def logo_fd(project_root_path):
    file_path = project_root_path / "tests/data/logo.png"
    with file_path.open("rb") as fb:
        yield fb


@pytest.fixture(scope="session")
def user_id(e2e_config):
    return e2e_config["accounts.user.id"]


@pytest.fixture(scope="session")
def account_id(e2e_config):
    return e2e_config["accounts.account.id"]


@pytest.fixture(scope="session")
def seller_id(e2e_config):
    return e2e_config["accounts.seller.id"]


@pytest.fixture(scope="session")
def buyer_id(e2e_config):
    return e2e_config["accounts.buyer.id"]


@pytest.fixture(scope="session")
def buyer_account_id(e2e_config):
    return e2e_config["accounts.buyer.account.id"]


@pytest.fixture(scope="session")
def licensee_id(e2e_config):
    return e2e_config["accounts.licensee.id"]


@pytest.fixture(scope="session")
def authorization_id(e2e_config):
    return e2e_config["commerce.authorization.id"]


@pytest.fixture(scope="session")
def price_list_id(e2e_config):
    return e2e_config["catalog.price_list.id"]


@pytest.fixture(scope="session")
def user_group_id(e2e_config):
    return e2e_config["accounts.user_group.id"]


@pytest.fixture(scope="session")
def commerce_product_id(e2e_config):
    return e2e_config["commerce.product.id"]


@pytest.fixture
def certificate_id(e2e_config):
    return e2e_config["program.certificate.id"]

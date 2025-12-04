import json
import logging
import os
import pathlib
import uuid

import pytest
from reportportal_client import RPLogger

from mpt_api_client import AsyncMPTClient, MPTClient


@pytest.fixture
def base_url():
    return os.getenv("MPT_API_BASE_URL")


@pytest.fixture
def mpt_vendor(base_url):
    return MPTClient.from_config(api_token=os.getenv("MPT_API_TOKEN_VENDOR"), base_url=base_url)  # type: ignore


@pytest.fixture
def async_mpt_vendor(base_url):
    return AsyncMPTClient.from_config(
        api_token=os.getenv("MPT_API_TOKEN_VENDOR"), base_url=base_url
    )  # type: ignore


@pytest.fixture
def mpt_ops(base_url):
    return MPTClient.from_config(api_token=os.getenv("MPT_API_TOKEN_OPERATIONS"), base_url=base_url)  # type: ignore


@pytest.fixture
def async_mpt_ops(base_url):
    return AsyncMPTClient.from_config(
        api_token=os.getenv("MPT_API_TOKEN_OPERATIONS"), base_url=base_url
    )  # type: ignore


@pytest.fixture
def mpt_client(base_url):
    return MPTClient.from_config(api_token=os.getenv("MPT_API_TOKEN_CLIENT"), base_url=base_url)  # type: ignore


@pytest.fixture
def async_mpt_client(base_url):
    return AsyncMPTClient.from_config(
        api_token=os.getenv("MPT_API_TOKEN_CLIENT"), base_url=base_url
    )  # type: ignore


@pytest.fixture
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)
    return logger


@pytest.fixture
def logger():
    return logging.getLogger("E2E")


@pytest.fixture
def project_root_path():
    return pathlib.Path(__file__).parent.parent.parent


@pytest.fixture
def pdf_fd():
    icon_path = pathlib.Path(__file__).parent / "empty.pdf"
    return pathlib.Path.open(icon_path, "rb")


@pytest.fixture
def pdf_url():
    return "https://sample-files.com/downloads/documents/pdf/basic-text.pdf"


@pytest.fixture
def jpg_url():
    return "https://sample-files.com/downloads/images/jpg/color_test_800x600_118kb.jpg"


@pytest.fixture
def e2e_config(project_root_path):
    filename = os.getenv("TEST_CONFIG_FILE", "e2e_config.test.json")
    file_path = project_root_path.joinpath(filename)
    return json.loads(file_path.read_text())


@pytest.fixture
def product_id(e2e_config):
    return e2e_config["catalog.product.id"]


@pytest.fixture
def short_uuid():
    return uuid.uuid4().hex[:8]


@pytest.fixture
def uuid_str():
    return str(uuid.uuid4())


@pytest.fixture
def logo_fd():
    file_path = pathlib.Path("tests/data/logo.png").resolve()
    return file_path.open("rb")


@pytest.fixture
def user_id(e2e_config):
    return e2e_config["accounts.user.id"]


@pytest.fixture
def account_id(e2e_config):
    return e2e_config["accounts.account.id"]


@pytest.fixture
def seller_id(e2e_config):
    return e2e_config["accounts.seller.id"]


@pytest.fixture
def buyer_id(e2e_config):
    return e2e_config["accounts.buyer.id"]


@pytest.fixture
def licensee_id(e2e_config):
    return e2e_config["accounts.licensee.id"]


@pytest.fixture
def authorization_id(e2e_config):
    return e2e_config["commerce.authorization.id"]

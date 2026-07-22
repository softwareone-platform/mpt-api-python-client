import json

import httpx
import pytest

from mpt_api_client.auth import CLIAccountAuthentication, CLIAccountError
from mpt_api_client.auth.cli_account import CLIAccount
from mpt_api_client.http import HTTPClient
from tests.unit.conftest import API_URL


@pytest.fixture
def active_account():
    return {
        "id": "ACC-0000-0001",
        "name": "SoftwareOne",
        "type": "Operations",
        "token": "idt:TKN-0000-0001:active-secret",
        "token_id": "TKN-0000-0001",
        "environment": "https://api.example.com/public/v1",
        "is_active": True,
    }


@pytest.fixture
def inactive_account():
    return {
        "id": "ACC-0000-0002",
        "name": "Vendor",
        "type": "Vendor",
        "token": "idt:TKN-0000-0002:inactive-secret",
        "token_id": "TKN-0000-0002",
        "environment": "https://api.other.example.com/public/v1",
        "is_active": False,
    }


def write_accounts_file(tmp_path, accounts):
    file_path = tmp_path / "accounts.json"
    file_path.write_text(json.dumps(accounts))
    return file_path


def create_authentication(tmp_path, accounts, account_id=None):
    file_path = write_accounts_file(tmp_path, accounts)
    return CLIAccountAuthentication(file_path=file_path, account_id=account_id)


def test_active_account_sets_bearer_header(tmp_path, active_account, inactive_account):
    authentication = create_authentication(tmp_path, [inactive_account, active_account])
    request = httpx.Request("GET", f"{API_URL}/")

    sent = next(authentication.auth_flow(request))  # act

    assert sent.headers["Authorization"] == "Bearer idt:TKN-0000-0001:active-secret"


def test_exposes_account_and_environment(tmp_path, active_account):
    authentication = create_authentication(tmp_path, [active_account])  # act

    assert authentication.account == CLIAccount(**active_account)
    assert authentication.environment == "https://api.example.com/public/v1"


def test_selects_account_by_id(tmp_path, active_account, inactive_account):
    authentication = create_authentication(  # act
        tmp_path,
        [active_account, inactive_account],
        account_id="ACC-0000-0002",
    )

    assert authentication.account.token == "idt:TKN-0000-0002:inactive-secret"


def test_file_missing_raises_error(tmp_path):
    file_path = tmp_path / "missing.json"

    with pytest.raises(CLIAccountError, match="not found"):
        CLIAccountAuthentication(file_path=file_path)  # act


def test_invalid_json_raises_error(tmp_path):
    file_path = tmp_path / "accounts.json"
    file_path.write_text("not-json{")

    with pytest.raises(CLIAccountError, match="not valid JSON"):
        CLIAccountAuthentication(file_path=file_path)  # act


def test_non_list_payload_raises_error(tmp_path):
    with pytest.raises(CLIAccountError, match="JSON list"):
        create_authentication(tmp_path, {"id": "ACC-0000-0001"})  # act


def test_no_active_account_raises_error(tmp_path, inactive_account):
    with pytest.raises(CLIAccountError, match="No active account"):
        create_authentication(tmp_path, [inactive_account])  # act


def test_multiple_active_accounts_raise_error(tmp_path, active_account, inactive_account):
    accounts = [active_account, {**inactive_account, "is_active": True}]

    with pytest.raises(CLIAccountError, match="Multiple active accounts"):
        create_authentication(tmp_path, accounts)  # act


@pytest.mark.parametrize("missing_field", ["token", "environment"])
def test_missing_required_field_raises_error(tmp_path, active_account, missing_field):
    active_account.pop(missing_field)

    with pytest.raises(CLIAccountError, match="missing its token or environment"):
        create_authentication(tmp_path, [active_account])  # act


def test_unknown_account_id_raises_error(tmp_path, active_account):
    with pytest.raises(CLIAccountError, match="'ACC-9999-9999' not found"):
        create_authentication(tmp_path, [active_account], account_id="ACC-9999-9999")  # act


def test_unknown_extra_fields_are_tolerated(tmp_path, active_account):
    accounts = [{**active_account, "extra": "field"}]

    authentication = create_authentication(tmp_path, accounts)  # act

    assert authentication.account.id == "ACC-0000-0001"


def test_configure_warns_on_host_mismatch(tmp_path, active_account):
    authentication = create_authentication(tmp_path, [active_account])

    with pytest.warns(UserWarning, match="differs from the CLI account"):
        HTTPClient(base_url="https://api.elsewhere.com", authentication=authentication)  # act


def test_configure_does_not_warn_on_matching_host(tmp_path, active_account, recwarn):
    authentication = create_authentication(tmp_path, [active_account])

    HTTPClient(  # act
        base_url="https://api.example.com/public/v1",
        authentication=authentication,
    )

    user_warnings = [warning for warning in recwarn if warning.category is UserWarning]
    assert not user_warnings


def test_default_path_reads_home_swocli(tmp_path, active_account, mocker):
    swocli_dir = tmp_path / ".swocli"
    swocli_dir.mkdir()
    (swocli_dir / "accounts.json").write_text(json.dumps([active_account]))
    mocker.patch(
        "mpt_api_client.auth.cli_account.DEFAULT_ACCOUNTS_FILE_PATH",
        swocli_dir / "accounts.json",
    )

    authentication = CLIAccountAuthentication()  # act

    assert authentication.account.id == "ACC-0000-0001"

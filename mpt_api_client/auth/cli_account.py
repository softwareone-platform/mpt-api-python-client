"""Authentication using accounts managed by the SoftwareOne Marketplace CLI.

The `mpt-cli` tool stores its accounts in ``~/.swocli/accounts.json``. This provider reads
that file and authenticates with the stored bearer token of the active account (or of an
explicitly selected account), so scripts can reuse the CLI login without copying tokens.
"""

import json
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import override
from urllib.parse import urlsplit

from mpt_api_client.auth.base import BearerTokenAuthentication
from mpt_api_client.exceptions import MPTError

DEFAULT_ACCOUNTS_FILE_PATH = Path.home() / ".swocli" / "accounts.json"


class CLIAccountError(MPTError):
    """Raised when the CLI accounts file is missing, invalid, or has no usable account."""


@dataclass(frozen=True)
class CLIAccount:
    """Account entry stored by the SoftwareOne Marketplace CLI."""

    id: str  # noqa: WPS125
    name: str
    type: str  # noqa: WPS125
    token: str
    token_id: str
    environment: str
    is_active: bool


class CLIAccountAuthentication(BearerTokenAuthentication):
    """Authenticate with the bearer token of an account stored by the marketplace CLI.

    By default the active account (``is_active: true``) from ``~/.swocli/accounts.json``
    is used; pass ``account_id`` to select a specific account instead. The accounts file
    is read once, eagerly, at construction time.

    The account's API URL is exposed as :attr:`environment` so callers can wire the client
    base URL from the same source:

        >>> authentication = CLIAccountAuthentication()
        >>> client = MPTClient.from_config(
        ...     authentication=authentication,
        ...     base_url=authentication.environment,
        ... )
    """

    def __init__(
        self,
        file_path: Path | str | None = None,
        account_id: str | None = None,
    ) -> None:
        """Load the account and initialize the bearer token.

        Args:
            file_path: Accounts file to read. Defaults to ``~/.swocli/accounts.json``.
            account_id: When set, select this account instead of the active one.

        Raises:
            CLIAccountError: If the file is missing or invalid, or no usable account
                matches the selection.
        """
        path = Path(file_path) if file_path else DEFAULT_ACCOUNTS_FILE_PATH
        accounts = _load_accounts(path)
        self._account = _select_account(accounts, account_id, path)
        super().__init__(self._account.token)

    @property
    def account(self) -> CLIAccount:
        """The selected CLI account."""
        return self._account

    @property
    def environment(self) -> str:
        """The API base URL stored with the selected account."""
        return self._account.environment

    @override
    def configure(self, *, base_url: str, timeout: float, retries: int) -> None:
        """Warn when the owning client targets a different host than the account.

        Args:
            base_url: Resolved base URL of the owning client.
            timeout: HTTP request timeout in seconds.
            retries: Number of retries configured on the owning client.
        """
        client_host = urlsplit(base_url).hostname
        account_host = urlsplit(self._account.environment).hostname
        account_id = self._account.id
        if client_host != account_host:
            message = (
                f"The client base URL host ({client_host}) differs from the CLI account "
                f"'{account_id}' environment host ({account_host}); the account token "
                "may not be valid there."
            )
            warnings.warn(message, UserWarning, stacklevel=2)


def _load_accounts(path: Path) -> list[dict[str, object]]:
    """Read and validate the raw accounts list from the accounts file.

    Args:
        path: Accounts file to read.

    Returns:
        The raw account entries.

    Raises:
        CLIAccountError: If the file is missing, is not valid JSON, or is not a list.
    """
    try:
        raw_content = path.read_text(encoding="utf-8")
    except OSError:
        raise CLIAccountError(
            f"CLI accounts file not found at {path}. "
            "Log in with the marketplace CLI (`mpt-cli accounts add`) first.",
        ) from None
    try:
        accounts = json.loads(raw_content)
    except json.JSONDecodeError as decode_error:
        raise CLIAccountError(
            f"CLI accounts file {path} is not valid JSON: {decode_error}.",
        ) from decode_error
    if not isinstance(accounts, list):
        raise CLIAccountError(f"CLI accounts file {path} must contain a JSON list of accounts.")
    return accounts


def _select_account(
    accounts: list[dict[str, object]],
    account_id: str | None,
    path: Path,
) -> CLIAccount:
    """Select the requested account entry and parse it.

    Args:
        accounts: Raw account entries from the accounts file.
        account_id: When set, select this account; otherwise select the active one.
        path: Accounts file the entries were read from, used in error messages.

    Returns:
        The selected account.

    Raises:
        CLIAccountError: If no account (or more than one active account) matches.
    """
    if account_id is not None:
        matches = [entry for entry in accounts if entry.get("id") == account_id]
        if not matches:
            raise CLIAccountError(f"Account '{account_id}' not found in {path}.")
        return _parse_account(matches[0], path)
    active = [entry for entry in accounts if entry.get("is_active")]
    if not active:
        raise CLIAccountError(
            f"No active account found in {path}. "
            "Activate one with the marketplace CLI (`mpt-cli accounts activate <id>`).",
        )
    if len(active) > 1:
        active_ids = ", ".join(str(entry.get("id")) for entry in active)
        raise CLIAccountError(f"Multiple active accounts found in {path}: {active_ids}.")
    return _parse_account(active[0], path)


def _parse_account(entry: dict[str, object], path: Path) -> CLIAccount:
    """Build a ``CLIAccount`` from a raw entry, requiring token and environment.

    Args:
        entry: Raw account entry.
        path: Accounts file the entry was read from, used in error messages.

    Returns:
        The parsed account.

    Raises:
        CLIAccountError: If the entry is missing ``token`` or ``environment``.
    """
    account_id = str(entry.get("id", ""))
    token = entry.get("token")
    environment = entry.get("environment")
    if not token or not environment:
        raise CLIAccountError(
            f"Account '{account_id}' in {path} is missing its token or environment.",
        )
    return CLIAccount(
        id=account_id,
        name=str(entry.get("name", "")),
        type=str(entry.get("type", "")),
        token=str(token),
        token_id=str(entry.get("token_id", "")),
        environment=str(environment),
        is_active=bool(entry.get("is_active")),
    )

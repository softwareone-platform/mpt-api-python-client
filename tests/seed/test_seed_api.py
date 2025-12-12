import pathlib

import pytest

from seed.context import Context
from seed.seed_api import seed_api


@pytest.fixture
def mock_context(mocker):
    context = mocker.Mock(spec=Context)
    context.load = mocker.Mock()
    context.save = mocker.Mock()
    return context


@pytest.fixture
def context_file_path(tmp_path):
    return tmp_path / "context.json"


async def test_seed_api_success(mock_context, mocker):
    mock_seed_catalog = mocker.patch("seed.seed_api.seed_catalog", autospec=True)
    mock_seed_accounts = mocker.patch("seed.seed_api.seed_accounts", autospec=True)
    mock_context_file = mocker.patch("seed.seed_api.context_file")
    load = mocker.patch("seed.seed_api.load_context")
    save = mocker.patch("seed.seed_api.save_context")

    mock_seed_catalog.return_value = None
    mock_context_file.return_value = pathlib.Path("test_context.json")

    await seed_api(context=mock_context)

    load.assert_called_once()
    mock_seed_catalog.assert_awaited_once()
    mock_seed_accounts.assert_awaited_once()
    save.assert_called_once()

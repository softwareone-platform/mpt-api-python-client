import pathlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from seed.context import Context
from seed.seed_api import seed_api


@pytest.fixture
def mock_context():
    context = MagicMock(spec=Context)
    context.load = MagicMock()
    context.save = MagicMock()
    return context


@pytest.fixture
def context_file_path(tmp_path):
    return tmp_path / "context.json"


async def test_seed_api_success(mock_context):
    with (
        patch("seed.seed_api.seed_catalog", new_callable=AsyncMock) as mock_seed_catalog,
        patch("seed.seed_api.seed_commerce", new_callable=AsyncMock) as mock_seed_commerce,
        patch("seed.seed_api.context_file") as mock_context_file,
        patch("seed.seed_api.load_context") as load,
        patch("seed.seed_api.save_context") as save,
    ):
        mock_seed_catalog.return_value = None
        mock_context_file.return_value = pathlib.Path("test_context.json")

        await seed_api(context=mock_context)

        load.assert_called_once()
        mock_seed_catalog.assert_called_once()
        mock_seed_commerce.assert_called_once()
        save.assert_called_once()

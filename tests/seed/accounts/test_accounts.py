from seed.accounts.accounts import seed_accounts


async def test_seed_accounts(mocker):  # noqa: WPS210
    mock_seed_seller = mocker.patch(
        "seed.accounts.accounts.seed_seller", new_callable=mocker.AsyncMock
    )
    mock_seed_buyer = mocker.patch(
        "seed.accounts.accounts.seed_buyer", new_callable=mocker.AsyncMock
    )
    mock_seed_module = mocker.patch(
        "seed.accounts.accounts.seed_module", new_callable=mocker.AsyncMock
    )
    mock_seed_api_token = mocker.patch(
        "seed.accounts.accounts.seed_api_token", new_callable=mocker.AsyncMock
    )
    mock_seed_user_group = mocker.patch(
        "seed.accounts.accounts.seed_user_group", new_callable=mocker.AsyncMock
    )
    mock_seed_licensee = mocker.patch(
        "seed.accounts.accounts.seed_licensee", new_callable=mocker.AsyncMock
    )
    await seed_accounts()  # act
    mocks = [
        mock_seed_seller,
        mock_seed_buyer,
        mock_seed_module,
        mock_seed_api_token,
        mock_seed_user_group,
        mock_seed_licensee,
    ]
    for mock in mocks:
        mock.assert_called_once()

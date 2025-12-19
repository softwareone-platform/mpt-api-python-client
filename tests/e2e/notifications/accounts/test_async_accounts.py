async def test_async_accounts(async_mpt_ops, account_id, category_id):
    iterator = async_mpt_ops.notifications.accounts(
        account_id=account_id, category_id=category_id
    ).iterate()

    result = [contact async for contact in iterator]

    assert isinstance(result, list)

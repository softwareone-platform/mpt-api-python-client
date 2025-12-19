def test_accounts(mpt_ops, account_id, category_id):
    iterator = mpt_ops.notifications.accounts(
        account_id=account_id, category_id=category_id
    ).iterate()

    result = list(iterator)

    assert isinstance(result, list)

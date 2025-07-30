from mpt_api_client.client import some_function_to_test


def test_some_function_to_test_false():
    assert not some_function_to_test("some")


def test_some_function_to_test_true():
    assert some_function_to_test("test")

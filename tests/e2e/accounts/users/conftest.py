import pytest


@pytest.fixture
def user_factory(uuid_str):
    def _user(  # noqa: WPS430
        email: str | None = None,  # Must be unique in Marketplace
        first_name: str = "E2E Created",
        last_name: str = "User",
    ):
        if not email:
            email = f"e2e_{uuid_str}@dummy.com"

        return {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "status": "Invited",
            "settings": {
                "cultureCode": "en-US",
                "languageCode": "en-US",
            },
        }

    return _user

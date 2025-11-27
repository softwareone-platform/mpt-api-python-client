import datetime as dt

from freezegun import freeze_time

from mpt_api_client.utils import get_iso_dt_str


@freeze_time("2025-11-14T09:00:00.000Z")
def test_get_iso_dt_str():
    dt_obj = dt.datetime.now(tz=dt.UTC)
    iso_str = get_iso_dt_str(dt_obj)
    assert iso_str == "2025-11-14T09:00:00.000Z"

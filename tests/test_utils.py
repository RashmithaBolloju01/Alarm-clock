from alarms.utils import parse_time_str, seconds_until
import datetime
import pytest

def test_parse_time_str_valid():
    t = parse_time_str("12:34:56")
    assert t.hour == 12 and t.minute == 34 and t.second == 56

def test_parse_time_str_invalid():
    with pytest.raises(ValueError):
        parse_time_str("99:99:99")

def test_seconds_until_future():
    now = datetime.datetime.now()
    future = (now + datetime.timedelta(minutes=1)).time().strftime("%H:%M:%S")
    secs = seconds_until(parse_time_str(future))
    assert 0 < secs <= 61

import datetime
import random
import time


from czo import DateTimeUtils

TZ = time.tzname[time.daylight]


class TestDateTimeUtils:
    def test_current_datetime(self):
        assert DateTimeUtils.current_datetime().strftime(
            "%Y-%m-%d %H:%M:%S"
        ) == datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def test_current_date(self):
        assert DateTimeUtils.current_date().strftime(
            "%Y-%m-%d"
        ) == datetime.datetime.now().strftime("%Y-%m-%d")

    def test_current_ymd(self):
        parts = datetime.datetime.now().strftime("%Y-%m-%d").split("-")
        cleaned = [part.lstrip("0") for part in parts]
        assert DateTimeUtils.current_ymd() == cleaned

    def test_timestamp_to_date(self):
        if TZ == "CST":
            assert DateTimeUtils.timestamp_to_date(1640995200) == "2022-01-01 08:00:00"
            assert (
                DateTimeUtils.timestamp_to_date(1640995200000) == "2022-01-01 08:00:00"
            )
        elif TZ == "UTC":
            assert DateTimeUtils.timestamp_to_date(1640995200) == "2022-01-01 00:00:00"
            assert (
                DateTimeUtils.timestamp_to_date(1640995200000) == "2022-01-01 00:00:00"
            )

    def test_date_to_timestamp(self):
        if TZ == "CST":
            assert DateTimeUtils.date_to_timestamp("2022-01-01 12:00:00") == 1641009600
            assert (
                DateTimeUtils.date_to_timestamp("2022-01-01 12:00:00", True)
                == 1641009600000
            )
        elif TZ == "UTC":
            assert DateTimeUtils.date_to_timestamp("2022-01-01 12:00:00") == 1641038400
            assert (
                DateTimeUtils.date_to_timestamp("2022-01-01 12:00:00", True)
                == 1641038400000
            )

    def test_yesterday_zero_point_timestamp(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        ms = int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d"))) * 1000
        s = int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d")))
        assert DateTimeUtils.yesterday_zero_point_timestamp(2) == s
        assert DateTimeUtils.yesterday_zero_point_timestamp(2, True) == ms

    def test_difference_time_two(self):
        assert (
            DateTimeUtils.difference_time_two(
                "2022-01-01 10:00:00", "2022-01-01 12:00:00"
            )
            == 7200
        )
        assert (
            DateTimeUtils.difference_time_two(
                "2022-01-01 10:00:00", "2022-01-01 12:00:00", True
            )
            == -7200
        )

    def test_date_before_minutes(self):
        now_time = datetime.datetime.now()
        now_time = now_time - datetime.timedelta(minutes=int(60))
        assert DateTimeUtils.date_before_minutes(60) == now_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def test_date_before_hours(self):
        now_time = datetime.datetime.now()
        now_time = now_time - datetime.timedelta(hours=int(24))
        assert DateTimeUtils.date_before_hours(24) == now_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def test_date_before_days(self):
        today = datetime.datetime.now()
        offset = datetime.timedelta(days=-7)
        assert DateTimeUtils.date_before_days(7) == (today + offset).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def test_time_handler(self):
        date = datetime.datetime.strptime(
            "2022-01-01T12:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        local_time = date + datetime.timedelta(hours=8)
        assert DateTimeUtils.time_handler(
            "2022-01-01T12:00:00.000Z"
        ) == local_time.strftime("%Y-%m-%d %H:%M:%S")

    def test_http_header_time_to_str(self):
        parsed_date = datetime.datetime.strptime(
            "Sat, 01 Jan 2022 12:00:00 GMT", "%a, %d %b %Y %H:%M:%S %Z"
        )
        parsed_date = parsed_date + datetime.timedelta(hours=8)
        assert DateTimeUtils.http_header_time_to_str(
            "Sat, 01 Jan 2022 12:00:00 GMT"
        ) == parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    def test_now_start_end(self):
        now = datetime.datetime.now()
        start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        end_of_day = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

        timestamp_tuple = int(start_of_day.timestamp()), int(end_of_day.timestamp())
        date_tuple = str(start_of_day), str(end_of_day)

        assert DateTimeUtils.now_start_end() == date_tuple
        assert DateTimeUtils.now_start_end(True) == timestamp_tuple

    def test_fmt_date(self):
        a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        assert DateTimeUtils.fmt_date() == a

    def test_generate_random_date_and_timestamp(self):
        start = datetime.datetime.strptime("2023-01-01 07:08:16", "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime("2023-01-10 07:08:16", "%Y-%m-%d %H:%M:%S")

        start_timestamp = int(start.timestamp())
        end_timestamp = int(end.timestamp())

        random_timestamp = random.randint(start_timestamp, end_timestamp)

        random_date = datetime.datetime.fromtimestamp(random_timestamp)
        date, timestamp = DateTimeUtils.generate_random_date_and_timestamp(
            "2023-01-11 07:08:16", "2023-01-12 07:08:16"
        )
        assert random_date.__str__() < date.__str__()
        assert random_timestamp < timestamp

import datetime
import ipaddress
import shutil
import time
import warnings
from pathlib import Path

import pytest

from czo import DateTime, Faker, Net, Paths, Rand, Timer


def test_net_parse_cidr_ipv4_and_invalid_input():
    info = Net.parse_cidr("192.168.0.0", 24)

    assert info["host_count"] == 254
    assert info["range"] == "192.168.0.1-192.168.0.254"
    assert info["network_address"] == "192.168.0.0"
    assert info["broadcast_address"] == "192.168.0.255"
    assert info["netmask"] == "255.255.255.0"
    assert info["prefixlen"] == 24

    with pytest.raises(ValueError):
        Net.parse_cidr("999.1.1.1", 24)


def test_net_ipaddress_generator_ipv6_batches():
    gen = Net.ipaddress_generator(
        2,
        max=3,
        is_ipv6=True,
        a=0x2001,
        b=0x0DB8,
        c=0,
        d=0x42,
        e=0,
        f=0,
        g=0,
        h=1,
    )

    first_batch = next(gen)
    second_batch = next(gen)

    assert first_batch == ["2001:db8:0:42::1", "2001:db8:0:42::2"]
    assert second_batch == ["2001:db8:0:42::3"]


def test_rand_hash_helpers_and_ip_generators():
    assert len(Rand.random_hash()) == 32
    assert len(Rand.random_hash(8)) == 8
    assert len(Rand.random_hash_by_uuid4(12)) == 12
    assert "@" in Rand.random_email()
    assert Rand.random_url().startswith("https://")

    cidr_v4 = Rand.generate_ip_with_netmask(netmask=16)
    cidr_v6 = Rand.generate_ip_with_netmask(netmask=64, v6=True)

    ipaddress.ip_network(cidr_v4, strict=False)
    ipaddress.ip_network(cidr_v6, strict=False)

    range_v4 = Rand.generate_ip_with_range()
    start_v4, end_v4 = range_v4.split("-")
    ipaddress.ip_address(start_v4)
    ipaddress.ip_address(end_v4)

    range_v6 = Rand.generate_ip_with_range(is_ipv6=True)
    start_v6, end_v6 = range_v6.split("-")
    ipaddress.ip_address(start_v6)
    ipaddress.ip_address(end_v6)


def test_paths_is_none_then_mkdir_and_get_dir_file_list():
    base_dir = Path("tests") / "_tmp_paths"
    target_dir = base_dir / "nested" / "child"

    try:
        created = Paths.is_none_then_mkdir(target_dir)
        assert created.exists()

        file_path = created / "sample.txt"
        file_path.write_text("hello")

        file_list = Paths.get_dir_file_list(str(base_dir))
        assert str(file_path) in file_list
    finally:
        if base_dir.exists():
            shutil.rmtree(base_dir)


def test_datetime_get_dates_offset_by_days_with_explicit_now():
    past, today = DateTime.get_dates_offset_by_days(-7, "2024-12-20 00:02:00")
    assert past == "2024-12-13 00:02:00"
    assert today == "2024-12-20 00:02:00"

    past_date, today_date = DateTime.get_dates_offset_by_days(
        -1, "2024-12-20 00:02:00", date_ok=True
    )
    assert past_date == "2024-12-19"
    assert today_date == "2024-12-20"

    parsed = DateTime.parse_iso8601("2024-12-20T00:02:00Z")
    assert parsed.tzinfo is not None
    shifted = DateTime.to_timezone(parsed, 8)
    assert shifted.utcoffset() == datetime.timedelta(hours=8)
    assert DateTime.is_workday("2024-12-20T00:02:00Z") is True
    assert DateTime.is_workday("2024-12-22T00:02:00Z") is False


def test_datetime_generate_random_date_and_timestamp_swaps_order():
    start = datetime.datetime(2024, 2, 1, tzinfo=datetime.timezone.utc)
    end = datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        random_date, random_ts = DateTime.generate_random_date_and_timestamp(
            start, end
        )

    assert caught and any("早于结束时间" in str(w.message) for w in caught)
    assert isinstance(random_date, datetime.datetime)
    assert end.timestamp() <= random_ts <= start.timestamp()


def test_timer_records_durations():
    timer = Timer()
    time.sleep(0.001)
    first = timer.stop()
    timer.start()
    time.sleep(0.001)
    second = timer.stop()

    assert len(timer.times) == 2
    assert first > 0
    assert second > 0
    assert timer.sum() == pytest.approx(first + second)
    assert timer.avg() == pytest.approx((first + second) / 2)
    assert timer.cumsum() == pytest.approx([first, first + second])


def test_faker_profile_structure_and_basic_values():
    faker = Faker()
    profile = faker.profile(zh=True)

    required_keys = {
        "姓名",
        "性别",
        "年龄",
        "职业",
        "民族",
        "学校",
        "宗教信仰",
        "手机号",
        "地址",
        "居住地",
        "身份证",
        "MAC",
        "邮箱",
        "学历",
        "车牌号",
    }

    assert required_keys.issubset(set(profile.keys()))
    assert isinstance(profile["年龄"], int) and profile["年龄"] > 0
    assert len(str(profile["身份证"])) == 18
    assert profile["MAC"].count(":") == 5
    assert "@" in profile["邮箱"]

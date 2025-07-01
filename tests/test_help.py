from czo import (
    DateTimeUtils,
    PathUtils,
    NetworkUtils,
    FakeDataUtils,
    RandomUtils,
)


def test_RandomUtils(capsys):
    RandomUtils.help()

    captured = capsys.readouterr()

    assert "RandomUtils" in captured.out and "help" in captured.out


def test_FakeDataUtils(capsys):
    FakeDataUtils.help()

    captured = capsys.readouterr()

    assert "FakeDataUtils" in captured.out and "help" in captured.out


def test_NetworkUtils(capsys):
    NetworkUtils.help()

    captured = capsys.readouterr()

    assert "NetworkUtils" in captured.out and "help" in captured.out


def test_PathUtils(capsys):
    PathUtils.help()

    captured = capsys.readouterr()

    assert "PathUtils" in captured.out and "help" in captured.out


def test_DateTimeUtils(capsys):
    DateTimeUtils.help()

    captured = capsys.readouterr()

    assert "DateTimeUtils" in captured.out and "help" in captured.out

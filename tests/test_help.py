from czo import (
    DateTime,
    Faker,
    Net,
    Paths,
    Rand,
)


def test_Rand(capsys):
    Rand.help()

    captured = capsys.readouterr()

    assert "Rand" in captured.out and "help" in captured.out


def test_Faker(capsys):
    Faker.help()

    captured = capsys.readouterr()

    assert "Faker" in captured.out and "help" in captured.out


def test_Net(capsys):
    Net.help()

    captured = capsys.readouterr()

    assert "Net" in captured.out and "help" in captured.out


def test_Paths(capsys):
    Paths.help()

    captured = capsys.readouterr()

    assert "Paths" in captured.out and "help" in captured.out


def test_DateTime(capsys):
    DateTime.help()

    captured = capsys.readouterr()

    assert "DateTime" in captured.out and "help" in captured.out

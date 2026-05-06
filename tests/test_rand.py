from czo import Rand


def test_rand_mac():
    a = Rand.random_mac()
    b = Rand.random_mac()
    assert a != b


def test_rand_hostname():
    a = Rand.random_hostname()
    b = Rand.random_hostname()
    assert a != b

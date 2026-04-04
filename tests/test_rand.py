from czo import Rand


def test_rand_mac():
    a = Rand.random_mac()
    b = Rand.random_mac()
    assert a != b

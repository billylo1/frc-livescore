from testCommon import processYear


def test_2022():
    error = processYear(2022)
    assert not error

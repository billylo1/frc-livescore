from testCommon import processYear


def test_2019():
    error = processYear(2019, debug=False)
    assert not error


# Allow users to run the test without pytest
if __name__ == "__main__":
    test_2019()
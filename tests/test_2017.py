from testCommon import processYear


def test_2017():
    error = processYear(2017, debug=False)
    assert not error


# Allow users to run the test without pytest
if __name__ == "__main__":
    test_2017()
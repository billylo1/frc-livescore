from testCommon import processYear


def test_2018():
    error = processYear(2018, debug=False)
    assert not error


# Allow users to run the test without pytest
if __name__ == "__main__":
    test_2018()
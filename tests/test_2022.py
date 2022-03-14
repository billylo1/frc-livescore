from testCommon import processYear


def test_2022():
    error = processYear(2022, debug=True)
    assert not error


# Allow users to run the test without pytest
if __name__ == "__main__":
    test_2022()

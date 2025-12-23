from boardgame_tracker_backend.main import square

def test_square():
    assert square(3) == 9
    assert square(-4) == 16
    assert square(0) == 0
import pytest


@pytest.fixture
def repeater(request):
    from app.repeater import Repeater
    from csv import reader
    f = open("test/datasets/sample_dataset.csv", "r")
    r = reader(f)

    def fin():
        f.close()

    request.addfinalizer(fin)
    return Repeater(r)


def test_diffLists(repeater):
    l1 = [0, 0, 0, 0, 0]
    l2 = [0, 0, 1, 1, 1]
    assert repeater.diffLists(l1, l2) == [(2, 0, 1),
                                          (3, 0, 1),
                                          (4, 0, 1)]


def test_diffLists_not_same_size(repeater):
    l1 = [0, 0, 0, 0, 0]
    l2 = [0, 0, 1, 1, 1, 1]
    with pytest.raises(ValueError):
        repeater.diffLists(l1, l2)


def test_diffLists_empty(repeater):
    l1 = []
    l2 = []
    with pytest.raises(ValueError):
        repeater.diffLists(l1, l2)


def test_diffLists_wrong_type_args(repeater):
    t1 = (1, 2, 3)
    t2 = (1, 2, 3)
    d1 = {"1": 1, "2": 2}
    d2 = {"1": 1, "2": 2}
    with pytest.raises(TypeError):
        repeater.diffLists(t1, t2)
        repeater.diffLists(d1, d2)

from mini_pandas.vec import Vec


def test_add():
    v1 = Vec([1, 2, 3, 4])
    v2 = Vec([-4, -3, -2, -1])

    assert v1 + v2 == [-3, -1, 1, 3]
    assert v1 + 1 == [2, 3, 4, 5]

    assert Vec(["abc", "def"]) + "x" == ["abcx", "defx"]


def test_iadd():
    v1 = Vec([-4, -3, -2, -1])

    v1 += 5
    assert v1 == [1, 2, 3, 4]


def test_sub():
    v1 = Vec([1, 2, 3, 4])
    v2 = Vec([-4, -3, -2, -1])

    assert v1 - v2 == [5, 5, 5, 5]
    assert v1 - 1 == [0, 1, 2, 3]


def test_mul():
    v1 = Vec([1, 2, 3, 4])
    v2 = Vec([-4, -3, -2, -1])

    assert v1 * v2 == [-4, -6, -6, -4]
    assert v1 * 0 == [0, 0, 0, 0]


def test_div():
    v1 = Vec([1, 2, 3, 4])
    v2 = Vec([-4, -3, -2, -1])

    assert v1 / 1 == v1
    assert v1 / v2 == [-0.25, -2 / 3, -1.5, -4]

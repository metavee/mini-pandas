from mini_pandas.vec import Vec


def test_add():
    v1 = Vec([1, 2, 3, 4])
    v2 = Vec([-4, -3, -2, -1])

    assert (v1 + v2 == [-3, -1, 1, 3]).all()
    assert (v1 + 1 == [2, 3, 4, 5]).all()

    assert (Vec(["abc", "def"]) + "x" == ["abcx", "defx"]).all()


def test_iadd():
    v1 = Vec([-4, -3, -2, -1])

    v1 += 5
    assert (v1 == [1, 2, 3, 4]).all()


def test_sub():
    v1 = Vec([1, 2, 3, 4])
    v2 = Vec([-4, -3, -2, -1])

    assert (v1 - v2 == [5, 5, 5, 5]).all()
    assert (v1 - 1 == [0, 1, 2, 3]).all()


def test_mul():
    v1 = Vec([1, 2, 3, 4])
    v2 = Vec([-4, -3, -2, -1])

    assert (v1 * v2 == [-4, -6, -6, -4]).all()
    assert (v1 * 0 == [0, 0, 0, 0]).all()


def test_div():
    v1 = Vec([1, 2, 3, 4])
    v2 = Vec([-4, -3, -2, -1])

    assert (v1 / 1 == v1).all()
    assert (v1 / v2 == [-0.25, -2 / 3, -1.5, -4]).all()


def test_any_all():
    alltrue = Vec([True, True, True])
    assert alltrue.all()
    assert alltrue.any()

    sometrue = Vec([True, False, True])
    assert not sometrue.all()
    assert sometrue.any()

    notrue = Vec([False, False, False])
    assert not notrue.all()
    assert not notrue.any()


def test_binary_mask():
    v1 = Vec([1, 2, 3, 4])

    mask = v1 % 2 == 0

    masked = v1[mask]
    assert (masked == [2, 4]).all()

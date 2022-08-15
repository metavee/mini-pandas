import pytest

from mini_pandas.df import DF
from mini_pandas.vec import Vec


def test_df():
    df = DF()
    df["Name"] = Vec(["Xavier", "Atticus", "Claude"])
    df["Age"] = [1, 2, 3]

    assert df.columns == ["Name", "Age"]
    assert (df[0] == ["Xavier", 1]).all()
    assert df.drow(1) == {"Name": "Atticus", "Age": 2}


def test_df_dims():
    df = DF()
    df["Name"] = Vec(["Xavier", "Atticus", "Claude"])
    df["Age"] = [1, 2, 3]

    assert len(df) == 3
    assert df.shape == (3, 2)


def test_multicolumn_select():
    df = DF()
    df["Name"] = Vec(["Xavier", "Atticus", "Claude"])
    df["Age"] = Vec([1, 2, 3])
    df["ID"] = Vec([5, 15, 100])

    reordered = df[["Age", "ID", "Name"]]
    assert isinstance(reordered, DF)

    assert reordered.columns == ["Age", "ID", "Name"]

    assert (reordered["Age"] == [1, 2, 3]).all()
    assert (reordered["Name"] == ["Xavier", "Atticus", "Claude"]).all()
    assert (reordered["ID"] == [5, 15, 100]).all()


def test_multirow_select():
    df = DF()
    df["Name"] = Vec(["Xavier", "Atticus", "Claude"])
    df["Age"] = Vec([1, 2, 3])
    df["ID"] = Vec([5, 15, 100])

    skiprow = df[1:]
    assert skiprow.columns == ["Name", "Age", "ID"]
    assert (skiprow["Name"] == ["Atticus", "Claude"]).all()


def test_2d_select():
    df = DF()
    df["Name"] = Vec(["Xavier", "Atticus", "Claude"])
    df["Age"] = Vec([1, 2, 3])
    df["ID"] = Vec([5, 15, 100])

    subset = df[1:, ["Name", "ID"]]
    assert subset.columns == ["Name", "ID"]
    assert (subset["Name"] == ["Atticus", "Claude"]).all()
    assert (subset["ID"] == [15, 100]).all()


def test_setter():
    df = DF()
    df["Name"] = ["Xavier", "Atticus", "Claude"]
    df["Age"] = -1

    assert type(df["Name"]) == Vec

    assert (df["Age"] == [-1, -1, -1]).all()

    with pytest.raises(IndexError):
        df["Extra"] = [1, 2, 3, 4, 5]

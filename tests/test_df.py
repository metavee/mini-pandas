from mini_pandas.df import DF
from mini_pandas.vec import Vec


def test_df():
    df = DF()
    df["Name"] = Vec(["Xavier", "Atticus", "Claude"])
    df["Age"] = [1, 2, 3]

    assert df.columns == ["Name", "Age"]
    assert (df.row(0) == ["Xavier", 1]).all()
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


def test_setter():
    df = DF()
    df["Name"] = ["Xavier", "Atticus", "Claude"]
    df["Age"] = -1

    assert type(df["Name"]) == Vec

    assert (df["Age"] == [-1, -1, -1]).all()

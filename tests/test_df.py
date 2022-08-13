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

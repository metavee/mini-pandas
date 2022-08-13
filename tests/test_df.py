from mini_pandas.df import DF
from mini_pandas.vec import Vec


def test_df():
    df = DF()
    df["Name"] = Vec(["Xavier", "Atticus", "Claude"])
    df["Age"] = [1, 2, 3]

    assert df.columns == ["Name", "Age"]
    assert df.row(0) == ["Xavier", 1]
    assert df.drow(1) == {"Name": "Atticus", "Age": 2}

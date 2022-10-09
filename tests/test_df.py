import csv
import pytest

from mini_pandas.df import DF, read_csv, vstack
from mini_pandas.vec import Vec


def test_df():
    df = DF()
    df["Name"] = Vec(["Xavier", "Atticus", "Claude"])
    df["Age"] = [1, 2, 3]

    assert df.columns == ["Name", "Age"]
    assert (df[0] == ["Xavier", 1]).all()
    assert df.drow(1) == {"Name": "Atticus", "Age": 2}

    del df["Name"]
    assert df.columns == ["Age"]
    assert (df["Age"] == [1, 2, 3]).all()


def test_dict_constructor():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": [1, 2, 3],
        }
    )

    assert df.shape == (3, 2)
    assert df.columns == ["Name", "Age"]
    assert (df["Name"] == ["Xavier", "Atticus", "Claude"]).all()
    assert type(df["Name"]) == Vec
    assert (df["Age"] == [1, 2, 3]).all()
    assert type(df["Age"]) == Vec


def test_df_dims():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": [1, 2, 3],
        }
    )

    assert len(df) == 3
    assert df.shape == (3, 2)


def test_multicolumn_select():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": [1, 2, 3],
            "ID": [5, 15, 100],
        }
    )

    reordered = df[["Age", "ID", "Name"]]
    assert isinstance(reordered, DF)

    assert reordered.columns == ["Age", "ID", "Name"]

    assert (reordered["Age"] == [1, 2, 3]).all()
    assert (reordered["Name"] == ["Xavier", "Atticus", "Claude"]).all()
    assert (reordered["ID"] == [5, 15, 100]).all()


def test_multirow_select():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": [1, 2, 3],
            "ID": [5, 15, 100],
        }
    )

    skiprow = df[1:]
    assert skiprow.columns == ["Name", "Age", "ID"]
    assert (skiprow["Name"] == ["Atticus", "Claude"]).all()


def test_multirow_mask_select():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": [1, 2, 3],
            "ID": [5, 15, 100],
        }
    )

    mask = df["ID"] < 20
    subset = df[mask]

    assert subset.shape == (2, 3)
    assert (subset["Name"] == ["Xavier", "Atticus"]).all()
    assert (subset["Age"] == [1, 2]).all()
    assert (subset["ID"] == [5, 15]).all()


def test_2d_select():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": [1, 2, 3],
            "ID": [5, 15, 100],
        }
    )

    subset = df[1:, ["Name", "ID"]]
    assert subset.columns == ["Name", "ID"]
    assert (subset["Name"] == ["Atticus", "Claude"]).all()
    assert (subset["ID"] == [15, 100]).all()


def test_iterrows():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": [1, 2, 3],
            "ID": [5, 15, 100],
        }
    )

    all_rows = list(df.iterrows())

    assert len(all_rows) == 3

    for i in range(3):
        assert (all_rows[i] == df[i]).all()
        assert isinstance(all_rows[i], Vec)


def test_setter():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": -1,
        }
    )

    assert type(df["Name"]) == Vec

    assert (df["Age"] == [-1, -1, -1]).all()

    with pytest.raises(IndexError):
        df["Extra"] = [1, 2, 3, 4, 5]


def test_distinct():
    df = DF(
        {
            "1": [1, 2, 1],
            "2": [1, 2, 1],
            "3": ["a", "b", "c"],
        }
    )

    df123 = df.distinct()
    assert df123.shape == (3, 3)
    assert (df123["1"] == [1, 2, 1]).all()
    assert (df123["2"] == [1, 2, 1]).all()
    assert (df123["3"] == ["a", "b", "c"]).all()

    df12 = df[["1", "2"]].distinct()
    assert df12.shape == (2, 2)
    assert (df12["1"] == [1, 2]).all()
    assert (df12["2"] == [1, 2]).all()


def test_vstack():
    df1 = DF(
        {
            "1": [1, 2, 1],
            "2": [1, 2, 1],
        }
    )

    df2 = DF(
        {
            "1": [5, 4, 3],
            "2": [2, 1, 0],
        }
    )

    df = vstack(df1, df2)
    assert df.shape == (6, 2)
    assert (df["1"] == [1, 2, 1, 5, 4, 3]).all()
    assert (df["2"] == [1, 2, 1, 2, 1, 0]).all()


def test_dropna():
    df = DF({"a": [1, None, 3], "b": [None, None, 3], "c": [1, None, 3]})

    res_any = df.dropna()
    assert len(res_any) == 1
    assert (res_any[0] == [3, 3, 3]).all()

    res_all = df.dropna(True)
    assert len(res_all) == 2
    assert (res_all[0] == [1, None, 1]).all()
    assert (res_all[1] == [3, 3, 3]).all()


def test_fillna():
    df = DF({"a": [1, None, 3], "b": [None, None, 3], "c": [1, None, 3]})

    res = df.fillna(-1)
    assert len(res) == 3
    assert (res["a"] == [1, -1, 3]).all()
    assert (res["b"] == [-1, -1, 3]).all()
    assert (res["c"] == [1, -1, 3]).all()


def test_groupby_count_column():
    df = DF(
        {
            "flag": [True, True, True, False, False, False],
            "name": ["Alice", "Bob", None, "Carol", None, None],
        }
    )

    res = df.groupby("flag").count("name").agg()

    assert (res[res["flag"] == True, "count(name)"] == [2]).all()
    assert (res[res["flag"] == False, "count(name)"] == [1]).all()


def test_groupby_agg():
    df = DF(
        {
            "tier": [1, 2, 2, 3, 3, 3],
            "flag": [True, False, True, False, True, False],
            "amount": [1, 2, 4, 8, 16, 32],
        }
    )

    gb = df.groupby("tier", "flag")
    res = gb.count().sum("amount").min("amount").max("amount").agg()

    assert "tier" in res.columns
    assert "flag" in res.columns
    assert "count(*)" in res.columns
    assert "sum(amount)" in res.columns

    assert res.shape == (5, 6)

    assert (
        res[
            ((res["tier"] == 1)) & (res["flag"] == True),
            ["count(*)", "sum(amount)", "min(amount)", "max(amount)"],
            0,
        ]
        == [1, 1, 1, 1]
    ).all()

    assert (
        res[
            ((res["tier"] == 2)) & (res["flag"] == True),
            ["count(*)", "sum(amount)", "min(amount)", "max(amount)"],
            0,
        ]
        == [1, 4, 4, 4]
    ).all()

    assert (
        res[
            ((res["tier"] == 2)) & (res["flag"] == False),
            ["count(*)", "sum(amount)", "min(amount)", "max(amount)"],
            0,
        ]
        == [1, 2, 2, 2]
    ).all()

    assert (
        res[
            ((res["tier"] == 3)) & (res["flag"] == True),
            ["count(*)", "sum(amount)", "min(amount)", "max(amount)"],
            0,
        ]
        == [1, 16, 16, 16]
    ).all()

    assert (
        res[
            ((res["tier"] == 3)) & (res["flag"] == False),
            ["count(*)", "sum(amount)", "min(amount)", "max(amount)"],
            0,
        ]
        == [2, 40, 8, 32]
    ).all()


def test_df_append():
    df = DF(
        {
            "Name": ["Xavier", "Atticus", "Claude"],
            "Age": [1, 2, 3],
        }
    )

    with pytest.raises(ValueError):
        df.append(["d", 4, 9])

    df.append(["d", 4])

    assert (df["Name"] == ["Xavier", "Atticus", "Claude", "d"]).all()
    assert (df["Age"] == [1, 2, 3, 4]).all()

    with pytest.raises(ValueError):
        df.append({"name": "e", "age": 5})

    df.append({"Name": "e", "Age": 5})

    assert (df["Name"] == ["Xavier", "Atticus", "Claude", "d", "e"]).all()
    assert (df["Age"] == [1, 2, 3, 4, 5]).all()


def test_to_csv(tmp_path):
    df = DF(
        {
            "Name": ["Xavier", None, "Claude"],
            "Age": [1, 2, 3],
        }
    )

    filename = tmp_path / "test_to.csv"

    df.to_csv(filename)

    with open(filename, "r") as ifile:
        reader = csv.DictReader(ifile)

        rows = [row for row in reader]

        assert len(rows) == 3

        # note: DictReader doesn't do any type casting
        assert rows[0] == {"Name": "Xavier", "Age": "1"}
        assert rows[1] == {"Name": "", "Age": "2"}
        assert rows[2] == {"Name": "Claude", "Age": "3"}


def test_read_csv(tmp_path):
    df = DF(
        {
            "Name": ["Xavier", None, "Claude"],
            "Age": [1, 2, 3],
        }
    )

    filename = tmp_path / "test_read_csv"
    df.to_csv(filename)

    df2 = read_csv(filename)

    assert df2.shape == df.shape

    assert (df["Name"] == df2["Name"]).all()
    assert (df["Age"] == df2["Age"]).all()

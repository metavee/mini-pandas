import itertools
import functools

from . import vec


class DF(dict):
    """Dataframe, or two-dimensional table."""

    @property
    def columns(self):
        return list(self.keys())

    @columns.setter
    def columns(self, value):
        # not safe if we swap names - probably need to create a new dict
        assert len(value) == len(self.keys())
        for old_name, new_name in zip(list(self.keys()), value):
            self[new_name] = self.pop(old_name)

    def drow(self, i):
        return {name: col[i] for name, col in self.items()}

    def __len__(self):
        if len(self.columns) == 0:
            return 0

        return len(self[self.columns[0]])

    @property
    def shape(self):
        return (len(self), len(self.columns))

    def __setitem__(self, key: str, value):
        length = len(self)

        if not isinstance(key, str):
            raise TypeError(f"Column name must be string. Got {type(key)}.")

        if isinstance(value, list) or isinstance(value, tuple):
            value = vec.Vec(value)
        elif isinstance(value, vec.Vec):
            pass
        else:
            # scalar?
            if length == 0:
                length = 1

            value = vec.Vec([value] * length)

        if len(value) != length and length != 0:
            raise IndexError(
                f"Length must match existing data. Got {len(value)}, expected {length}."
            )

        return super().__setitem__(key, value)

    def __getitem__(self, key):
        if isinstance(key, int):
            # single row select
            # return as Vec
            return vec.Vec([col[key] for col in self.values()])
        elif isinstance(key, list) and type(key[0]) == str:
            # multi-column select
            # create new DF with selected columns
            df = DF()
            for column in key:
                df[column] = self[column]

            return df
        elif isinstance(key, slice) or (isinstance(key, list) and type(key[0]) == bool):
            # multi-row select
            # create new DF with selected rows
            df = DF()
            for column in self.columns:
                df[column] = self[column][key]

            return df
        elif isinstance(key, tuple):
            # recursively peel off indexes from tuple
            if len(key) == 0:
                return self

            return self[key[0]][key[1:]]

        # default: fall back to dict behaviour - single column select
        return super().__getitem__(key)

    def groupby(self, *columns):
        uniques = [self[c].distinct() for c in columns]

        subsets = []

        for column_values in itertools.product(*uniques):
            conditions = [self[c] == v for c, v in zip(columns, column_values)]
            condition = functools.reduce(lambda a, b: a & b, conditions)

            subset_df = self[condition]
            if len(subset_df) == 0:
                continue

            subsets.append((column_values, subset_df))

        return GroupBy(columns, subsets)

    def distinct(self):
        seen_rows = set()
        unseen_flags = []

        for i in range(len(self)):
            row = self[i]
            row_tup = tuple(row)

            unseen_flags.append(row_tup not in seen_rows)

            seen_rows.add(row_tup)

        return self[unseen_flags]


def vstack(*dfs):
    final_df = DF()
    for c in dfs[0].columns:
        final_df[c] = vec.Vec(sum([df[c] for df in dfs], []))

    return final_df


class GroupBy:
    def __init__(self, keys, subsets):
        self.keys = keys
        self.subsets = subsets
        self.agg_cols = []

    def count(self):
        for key_values, subset in self.subsets:
            subset["count(*)"] = len(subset)

        self.agg_cols.append("count(*)")

        return self

    def sum(self, column):
        for key_values, subset in self.subsets:
            subset[f"sum({column})"] = sum(subset[column])

        self.agg_cols.append(f"sum({column})")

        return self

    def agg(self):
        return vstack(
            *[s[1][list(self.keys) + self.agg_cols].distinct() for s in self.subsets]
        )

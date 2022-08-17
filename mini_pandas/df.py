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

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

    def row(self, i):
        return vec.Vec([col[i] for col in self.values()])

    def drow(self, i):
        return {name: col[i] for name, col in self.items()}

    def __len__(self):
        if len(self.columns) == 0:
            return 0

        return len(self[self.columns[0]])

    @property
    def shape(self):
        return (len(self), len(self.columns))

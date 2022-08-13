import operator


class Vec(list):
    """One-dimensional array."""

    def _op(self, other, op):
        if isinstance(other, list):
            assert len(self) == len(other)
            return Vec([op(val1, val2) for val1, val2 in zip(self, other)])
        else:
            return Vec([op(val1, other) for val1 in self])

    def _iop(self, other, op):
        result = self._op(other, op)
        for i, val in enumerate(result):
            self[i] = val

        return self

    def __add__(self, other):
        return self._op(other, operator.add)

    def __iadd__(self, other):
        return self._iop(other, operator.add)

    def __sub__(self, other):
        return self._op(other, operator.sub)

    def __isub__(self, other):
        return self._iop(other, operator.sub)

    def __mul__(self, other):
        return self._op(other, operator.mul)

    def __imul(self, other):
        return self._iop(other, operator.mul)

    def __truediv__(self, other):
        return self._op(other, operator.truediv)

    def __itruediv(self, other):
        return self._iop(other, operator.truediv)

    def __mod__(self, other):
        return self._op(other, operator.mod)

    def __imod__(self, other):
        return self._iop(other, operator.mod)

    def __eq__(self, other):
        return self._op(other, operator.eq)

    def __ne__(self, other):
        return self._op(other, operator.ne)

    def __bool__(self):
        raise TypeError("Use .any() or .all() to get scalar boolean.")

    def all(self):
        return all([bool(x) for x in self])

    def any(self):
        return any([bool(x) for x in self])
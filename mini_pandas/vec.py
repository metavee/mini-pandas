import math
import operator


class Vec(list):
    """One-dimensional array."""

    def __repr__(self):
        return f"Vec({[v for v in self]})"

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

    def _unary_op(self, op):
        return Vec([op(val) for val in self])

    def __add__(self, other):
        return self._op(other, operator.add)

    def __iadd__(self, other):
        return self._iop(other, operator.add)

    def __sub__(self, other):
        return self._op(other, operator.sub)

    def __isub__(self, other):
        return self._iop(other, operator.sub)

    def __pos__(self):
        return self._unary_op(operator.pos)

    def __neg__(self):
        return self._unary_op(operator.neg)

    def __abs__(self):
        return self._unary_op(abs)

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

    def __lt__(self, other):
        return self._op(other, operator.lt)

    def __le__(self, other):
        return self._op(other, operator.le)

    def __gt__(self, other):
        return self._op(other, operator.gt)

    def __ge__(self, other):
        return self._op(other, operator.ge)

    def __bool__(self):
        raise TypeError("Use .any() or .all() to get scalar boolean.")

    def __and__(self, other):
        return self._op(other, operator.and_)

    def __iand__(self, other):
        return self._iop(other, operator.and_)

    def __or__(self, other):
        return self._op(other, operator.or_)

    def __ior__(self, other):
        return self._iop(other, operator.or_)

    def __xor__(self, other):
        return self._op(other, operator.xor)

    def __ixor__(self, other):
        return self._iop(other, operator.xor)

    def __invert__(self):
        return self._unary_op(operator.not_)

    def all(self):
        return all([bool(x) for x in self])

    def any(self):
        return any([bool(x) for x in self])

    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 0:
            return self

        # binary masks
        if isinstance(key, list):
            assert len(key) == len(self)

            # cast to bool
            mask = [bool(x) for x in key]

            return Vec([x for x, keepx in zip(self, mask) if keepx])

        # default: defer to list implementation
        return super().__getitem__(key)

    def distinct(self):
        return Vec(sorted(set(self)))

    def mean(self):
        return sum(self) / len(self)

    def isnull(self):
        return Vec([i is None or (type(i) == float and math.isnan(i)) for i in self])

    def dropna(self):
        return self[~self.isnull()]

    def apply(self, fxn):
        return Vec([fxn(x) for x in self])

    def fillna(self, default):
        nulls = self.isnull()

        return Vec([val if not isnull else default for val, isnull in zip(self, nulls)])

from array import array
import reprlib
import numbers
import functools
import operator
import math
import itertools
from fractions import Fraction


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        classname = type(self).__name__
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return classname + '({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        """实现切片"""
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))

    def __eq__(self, other):
        """和基本序列类型比较时应该返回False"""
        if isinstance(other, type(self)):
            return (len(self) == len(other) and
                    all(a == b for a, b in zip(self, other)))
        else:
            return NotImplemented

    def __hash__(self):
        hashes = (hash(h) for h in self)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __pos__(self):
        cls = type(self)
        return cls(self)

    def __neg__(self):
        cls = type(self)
        return cls(-x for x in self)

    def __add__(self, other):
        """当两个向量长度不一致时,将较短的向量补全0"""
        cls = type(self)
        pairs = itertools.zip_longest(self, other,fillvalue=0.0)
        return cls(a + b for a, b in pairs)

    def __radd__(self, other):
        """反向运算符：+调用__add__返回NotImplemented后掉转入参并调用__radd__"""
        return self + other

    def __mul__(self, scalar):
        cls = type(self)
        return cls(x * scalar for x in self)

    def __rmul__(self, scalar):
        return self * scalar

v1 = Vector([9, 8, 7 ,6])
v2 = Vector([2, 2, 2, 2])
v3 = Vector((11, 22))
print(v1)
print(v1[1:3])
print(v1 == v2)
for v in v1:
    print(v)

print(-v1 + v3)
print({3, 4} + v3)
print(Fraction(1, 4) * v3)
print([11, 22] == v3)
print((11, 22) == [11, 22])
v3 += v1
v3 *= Fraction(1, 10)
print(v3)

from __future__ import absolute_import, division, print_function

import operator
from datashape import dshape
from dateutil.parser import parse as dt_parse
from .core import Scalar, BinOp, UnaryOp
from ..core import Expr
from ...dispatch import dispatch
from ...compatibility import _strtypes
from datashape import coretypes as ct
from .boolean import *


@dispatch(ct.Date, _strtypes)
def scalar_coerce(_, val):
    return dt_parse(val).date()

@dispatch(ct.DateTime, _strtypes)
def scalar_coerce(_, val):
    return dt_parse(val)

@dispatch(ct.DataShape, object)
def scalar_coerce(dtype, val):
    return scalar_coerce(dtype[0], val)

@dispatch(object, object)
def scalar_coerce(dtype, val):
    return val


class NumberInterface(Scalar):
    def __eq__(self, other):
        return Eq(self, scalar_coerce(self.dshape, other))

    def __ne__(self, other):
        return NE(self, scalar_coerce(self.dshape, other))

    def __lt__(self, other):
        return LT(self, scalar_coerce(self.dshape, other))

    def __le__(self, other):
        return LE(self, scalar_coerce(self.dshape, other))

    def __gt__(self, other):
        return GT(self, scalar_coerce(self.dshape, other))

    def __ge__(self, other):
        return GE(self, scalar_coerce(self.dshape, other))

    def __neg__(self):
        return Neg(self)

    def __add__(self, other):
        return Add(self, scalar_coerce(self.dshape, other))

    def __radd__(self, other):
        return Add(scalar_coerce(self.dshape, other), self)

    def __mul__(self, other):
        return Mul(self, scalar_coerce(self.dshape, other))

    def __rmul__(self, other):
        return Mul(scalar_coerce(self.dshape, other), self)

    def __div__(self, other):
        return Div(self, scalar_coerce(self.dshape, other))

    __truediv__ = __div__

    def __rdiv__(self, other):
        return Div(scalar_coerce(self.dshape, other), self)

    def __sub__(self, other):
        return Sub(self, scalar_coerce(self.dshape, other))

    def __rsub__(self, other):
        return Sub(scalar_coerce(self.dshape, other), self)

    def __pow__(self, other):
        return Pow(self, scalar_coerce(self.dshape, other))

    def __rpow__(self, other):
        return Pow(scalar_coerce(self.dshape, other), self)

    def __mod__(self, other):
        return Mod(self, scalar_coerce(self.dshape, other))

    def __rmod__(self, other):
        return Mod(scalar_coerce(self.dshape, other), self)


class Number(NumberInterface):
    __hash__ = Expr.__hash__


class Arithmetic(BinOp, Number):
    """ Super class for arithmetic operators like add or mul """
    @property
    def dshape(self):
        # TODO: better inference.  e.g. int + int -> int
        return dshape('real')


class Add(Arithmetic):
    symbol = '+'
    op = operator.add


class Mul(Arithmetic):
    symbol = '*'
    op = operator.mul


class Sub(Arithmetic):
    symbol = '-'
    op = operator.sub


class Div(Arithmetic):
    symbol = '/'
    op = operator.truediv


class Pow(Arithmetic):
    symbol = '**'
    op = operator.pow


class Mod(Arithmetic):
    symbol = '%'
    op = operator.mod


class Neg(UnaryOp, Number):
    op = operator.neg

    def __str__(self):
        return '-%s' % self.parent

    @property
    def dshape(self):
        # TODO: better inference.  -uint -> int
        return self.parent.dshape



# Here follows a large number of unary operators.  These were selected by
# taking the intersection of the functions in ``math`` and ``numpy``

class RealMath(Number, UnaryOp):
    """ Mathematical unary operator with real valued dshape like sin, or exp """
    @property
    def dshape(self):
        return dshape('real')


class sqrt(RealMath): pass

class sin(RealMath): pass
class sinh(RealMath): pass
class cos(RealMath): pass
class cosh(RealMath): pass
class tan(RealMath): pass
class tanh(RealMath): pass

class exp(RealMath): pass
class expm1(RealMath): pass
class log(RealMath): pass
class log10(RealMath): pass
class log1p(RealMath): pass

class acos(RealMath): pass
class acosh(RealMath): pass
class asin(RealMath): pass
class asinh(RealMath): pass
class atan(RealMath): pass
class atanh(RealMath): pass

class radians(RealMath): pass
class degrees(RealMath): pass


class IntegerMath(Number, UnaryOp):
    """ Mathematical unary operator with int valued dshape like ceil, floor """
    @property
    def dshape(self):
        return dshape('int')


class ceil(IntegerMath): pass
class floor(IntegerMath): pass
class trunc(IntegerMath): pass


class BooleanMath(Number, UnaryOp):
    """ Mathematical unary operator with bool valued dshape like isnan """
    @property
    def dshape(self):
        return dshape('bool')


class isnan(BooleanMath): pass

from dataclasses import dataclass
from dynamicCtx import DynamicContext


class Node:
    def __add__(self, other):
        exp = ('+', self, other)
        return exp

    def __mul__(self, other):
        exp = ('*', self, other)
        return exp

    def __ilshift__(self, other):
        stmt = ('assign', self, other)
        DynamicContext.addStatment(stmt)
        return self


@dataclass
class Lit(Node):
    value: int

    def match(self, matcher):
        return matcher.lit(self)


@dataclass
class Var(Node):
    name: str = '<unknown>'
    owner: type = None

    def match(self, matcher):
        return matcher.var(self)


@dataclass
class Ref(Node):
    ref: object
    visitor: type

    def match(self, matcher):
        return matcher.ref(self)

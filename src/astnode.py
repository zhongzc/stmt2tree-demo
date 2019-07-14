from dataclasses import dataclass
from dynamicCtx import DynamicContext

# 定义少量语法树节点
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
    v: int


@dataclass
class Var(Node):
    v: str = '<unknown>'

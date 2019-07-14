from astnode import Var
from dynamicCtx import DynamicContext


def inferConponents(clazz):
    cpon = {}

    for name, c in clazz.__dict__.items():
        if isinstance(c, Var):
            if c.v == '<unknown>':
                c.v = name
            cpon[name] = c
        if hasattr(c, 'tag') and c.tag == 'Module':
            cpon[name] = c

    clazz.components = cpon


def transformModClass(clazz):
    inferConponents(clazz)
    return DynamicContext.catchStatments(clazz)


class MetaModule(type):
    def __new__(cls, name, bases, dct):
        Clazz = super().__new__(cls, name, bases, dct)
        Clazz.tag = 'Module'
        NewClazz = transformModClass(Clazz)
        return NewClazz


class Module(metaclass=MetaModule):
    statements = []

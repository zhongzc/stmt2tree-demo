from astnode import Var, Ref, Node
from dynamicCtx import DynamicContext


def inferComponents(clazz):
    result = {}
    changes = (set(), [], [])

    for name in list(clazz.__dict__.keys()):
        v = getattr(clazz, name)

        def refresh(new):
            result[name] = new
            changes[0].add(name)
            changes[1].append(v)
            changes[2].append(new)

        if isinstance(v, Var):
            if v.name == '<unknown>':
                newVar = Var(name, clazz)
            elif v.owner is None:
                newVar = Var(v.name, clazz)
            else:
                newVar = Ref(v, clazz)
            refresh(newVar)

        if hasattr(v, 'tag') and v.tag == 'Module':
            wrapped = Ref(v, clazz)
            refresh(wrapped)

    return result, changes


def mapStatements(clazz, changes, statements):
    def getNewValueOrElse(oldValue, default):
        for i, v in enumerate(changes[1]):
            if id(v) == id(oldValue):
                return changes[2][i]
        return default

    for k, v in clazz.__dict__.items():
        if k in changes[0]:
            setattr(clazz, k, getNewValueOrElse(v, v))

    class matcher:
        @staticmethod
        def ref(r):
            return Ref(r.obj, clazz)
        @staticmethod
        def lit(l):
            return l
        @staticmethod
        def var(v):
            var = getNewValueOrElse(v, v)
            if isinstance(var, Ref):
                return Ref(var.ref, clazz)
            if isinstance(var, Var) and var.owner != clazz:
                return Ref(var, clazz)
            else:
                return var

    def k(n):
        if isinstance(n, tuple):
            return tuple(map(k, n))
        elif isinstance(n, Node):
            return n.match(matcher)
        else:
            return n

    newStatements = list(map(k, statements))
    return newStatements


def transformModuleClass(clazz):
    components, changes = inferComponents(clazz)
    statements = DynamicContext.catchStatments(clazz.statements)
    newStatements = mapStatements(clazz, changes, statements)

    clazz.components = components
    clazz.statements = newStatements
    return clazz





class MetaModule(type):
    def __new__(cls, name, bases, dct):
        Clazz = super().__new__(cls, name, bases, dct)
        Clazz.tag = 'Module'
        NewClazz = transformModuleClass(Clazz)
        return NewClazz


class Module(metaclass=MetaModule):
    statements = []

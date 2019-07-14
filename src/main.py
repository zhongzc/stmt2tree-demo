from astnode import Var, Lit
from module import Module

class SomeAdd(Module):
    a = Var()
    b = Var()

    a <<= Lit(1) + Lit(2)
    b <<= Lit(3) + a

class SomeMul(Module):
    c = Var()
    d = Var()

    c <<= Lit(1) * Lit(2)
    d <<= c * Lit(2)

class MoreAdd(Module):
    add = SomeAdd
    mul = SomeMul
    add.b <<= mul.d


if __name__ == '__main__':
    assert SomeAdd.statements == [('assign', Var('a'), ('+', Lit(1), Lit(2))), ('assign', Var('b'), ('+', Lit(3), Var('a')))]
    assert SomeMul.statements == [('assign', Var('c'), ('*', Lit(1), Lit(2))), ('assign', Var('d'), ('*', Var('c'), Lit(2)))]
    assert MoreAdd.statements == [('assign', Var('b'), Var('d'))]

    assert SomeAdd.components == {'a': Var(v='a'), 'b': Var(v='b')}
    assert SomeMul.components == {'c': Var(v='c'), 'd': Var(v='d')}
    assert MoreAdd.components == {'add': SomeAdd, 'mul': SomeMul}

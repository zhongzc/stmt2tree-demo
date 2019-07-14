from astnode import Var, Lit, Ref
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


class RefAddMul(Module):
    add = SomeAdd
    mul = SomeMul
    add.b <<= mul.d


class MoreRef(Module):
    k = RefAddMul.mul.ref.c
    a = SomeAdd.b

    a <<= Lit(2) + k * Lit(10)


if __name__ == '__main__':
    assert SomeAdd.components == {
        'a': Var('a', owner=SomeAdd),
        'b': Var('b', owner=SomeAdd)
    }
    assert SomeMul.components == {
        'c': Var('c', owner=SomeMul),
        'd': Var('d', owner=SomeMul)
    }
    assert RefAddMul.components == {
        'add': Ref(SomeAdd, visitor=RefAddMul),
        'mul': Ref(SomeMul, visitor=RefAddMul)
    }
    assert MoreRef.components == {
        'k': Ref(Var('c', owner=SomeMul), visitor=MoreRef),
        'a': Ref(Var('b', owner=SomeAdd), visitor=MoreRef)
    }

    assert SomeAdd.statements == [
        ('assign', Var('a', owner=SomeAdd), ('+', Lit(1), Lit(2))),
        ('assign', Var('b', owner=SomeAdd), ('+', Lit(3), Var('a', owner=SomeAdd)))
    ]
    assert SomeMul.statements == [
        ('assign', Var('c', owner=SomeMul), ('*', Lit(1), Lit(2))),
        ('assign', Var('d', owner=SomeMul), ('*', Var('c', owner=SomeMul), Lit(2)))
    ]
    assert RefAddMul.statements == [
        ('assign', Ref(Var('b', owner=SomeAdd), visitor=RefAddMul), Ref(Var('d', owner=SomeMul), visitor=RefAddMul))
    ]
    assert MoreRef.statements == [
        ('assign', Ref(Var('b', owner=SomeAdd), visitor=MoreRef),
                   ('+', Lit(2), ('*', Ref(Var('c', owner=SomeMul), visitor=MoreRef), Lit(10))))
    ]

from astnode import Var, Lit
from transform import transformMod

class SomeAdd:
    a = Var()
    b = Var()

    def hcl(self):
        SomeAdd.a <<= Lit(1) + Lit(2)
        SomeAdd.b <<= Lit(3) + SomeAdd.a

class SomeMul:
    c = Var()
    d = Var()

    def hcl(self):
        SomeMul.c <<= Lit(1) * Lit(2)
        SomeMul.d <<= SomeMul.c * Lit(2)

if __name__ == '__main__':
    # 通过返回值取得转化成功的语法树节点
    stmts = transformMod(SomeAdd)
    assert stmts == [('assign', Var('a'), ('+', Lit(1), Lit(2))), ('assign', Var('b'), ('+', Lit(3), Var('a')))]

    stmts = transformMod(SomeMul)
    assert stmts == [('assign', Var('c'), ('*', Lit(1), Lit(2))), ('assign', Var('d'), ('*', Var('c'), Lit(2)))]

    # 语句转化成功后，语法树节点可直接从类属性中获取
    assert SomeAdd.stmts == [('assign', Var('a'), ('+', Lit(1), Lit(2))), ('assign', Var('b'), ('+', Lit(3), Var('a')))]
    assert SomeMul.stmts == [('assign', Var('c'), ('*', Lit(1), Lit(2))), ('assign', Var('d'), ('*', Var('c'), Lit(2)))]

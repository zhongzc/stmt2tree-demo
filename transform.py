from astnode import Var
from dynamicCtx import DynamicContext


def enrichMod(clazz):
    for name, var in clazz.__dict__.items():
        if isinstance(var, Var) and var.v == '<unknown>':
            var.v = name


# 将原始的模块转化成最终的模块，并返回语法树节点
def transformMod(clazz):
    enrichMod(clazz)
    stmts = DynamicContext.withMod(clazz)
    return stmts

class GlobalMod(object):
    stmts = []


# 实现将Python语句转化成语法树的核心部件
class DynamicContext:
    __stmts = GlobalMod.stmts

    @staticmethod
    def addStatment(stmt):
        DynamicContext.__stmts.append(stmt)

    @staticmethod
    def withMod(modClazz):
        # 将上下文切换至所给模块类
        setattr(modClazz, 'stmts', [])
        DynamicContext.__stmts = getattr(modClazz, 'stmts')

        # 调用模块中的 hcl 函数
        #
        # obj.hcl 函数是模块需要实现的函数，其中包含待转换的
        # 语句。DynamicContext 完成上下文切换工作，使得不同的
        # 模块的互相隔离，转化过程互不影响，进而提高了组合性。
        object.__new__(modClazz).hcl()

        # 标志位 clazz.sealed 表示该模块类已完成语句转化
        # TODO: 下一步可以通过 sealed 标志位判断模块类是否已经
        # TODO: 转化过，进而减少重复的转化操作
        setattr(modClazz, 'sealed', True)

        result = DynamicContext.__stmts[:]

        # 将上下文切换回全局模块
        DynamicContext.__stmts = GlobalMod.stmts

        return result
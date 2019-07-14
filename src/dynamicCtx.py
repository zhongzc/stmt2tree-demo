class DynamicContext:
    __stmts = []

    @staticmethod
    def addStatment(statment):
        DynamicContext.__stmts.append(statment)

    @staticmethod
    def catchStatments(ModClass):
        parentStmts = ModClass.statements[:]
        DynamicContext.__stmts.extend(parentStmts)

        ModClass.statements = DynamicContext.__stmts
        DynamicContext.__stmts = []

        return ModClass
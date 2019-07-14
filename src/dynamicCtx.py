class DynamicContext:
    __stmts = []

    @staticmethod
    def addStatment(statment):
        DynamicContext.__stmts.append(statment)

    @staticmethod
    def catchStatments(oldStmts):
        DynamicContext.__stmts.extend(oldStmts[:])
        result = DynamicContext.__stmts
        DynamicContext.__stmts = []
        return result
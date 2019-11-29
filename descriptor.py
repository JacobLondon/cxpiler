import sys
from typing import List

class StatementBlock:
    def __init__(self):
        self.statements = []
    def __str__(self):
        result = "{"
        for statement in self.statements:
            result += str(statement)
        return result + "}\n"
    def __getitem__(self, key):
        return self.statements[key]
    def __setitem__(self, key, value):
        self.statements[key] = value
    def push(self, statement):
        self.statements.append(statement)

class StatementAssign:
    def __init__(self, name: str, expr):
        self.name = name
        self.expr = expr
    def __str__(self):
        if self.expr:
            return f"{self.name} = {self.expr};"
        else:
            print("Error: Invalid assignment statement:", self.expr, file=sys.stderr)

class StatementInst:
    def __init__(self, dtype: str, name: str):
        self.dtype: str = dtype
        self.name: str = name
    def __str__(self):
        return f"{self.dtype} {self.name};"

class StatementInit:
    def __init__(self, dtype: str, name: str, expr):
        self.dtype: str = dtype
        self.name: str = name
        self.expr = expr
    def __str__(self):
        if self.expr:
            return f"{self.dtype} {self.name} = {self.expr};"
        else:
            print("Error: Invalid initialization statement:", self.expr, file=sys.stderr)
            exit(-1)

class StatementControl:
    def __init__(self, ctrl: str, expr=None):
        self.ctrl = ctrl
        self.expr = expr
    def __str__(self):
        if self.ctrl == "return":
            if self.expr:
                return f"return {str(self.expr)};"
            else:
                return "return;"
        elif self.ctrl == "break":
            return "break;"
        elif self.ctrl == "continue":
            return "continue;"
        else:
            print("Error: Invalid control flow statement:", self.ctrl, file=sys.stderr)
            exit(-1)

class StatementIf:
    def __init__(self, check: str):
        self.check = check
        self.block = StatementBlock()
    def __str__(self):
        result = f"if ({self.check})"
        result += str(self.block)
        return result

class StatementFor:
    def __init__(self, init: str, check: str, inc: str):
        self.init  = init
        self.check = check
        self.inc   = inc
        self.block = StatementBlock()
    def __str__(self):
        result = f"for ({self.init}; {self.check}; {self.inc})"
        result += str(self.block)
        return result

class StatementWhile:
    def __init__(self, check: str):
        self.check = check
        self.block = StatementBlock()
    def __str__(self):
        result = f"while ({self.check})"
        result += str(self.block)
        return result

class FuncDef:
    def __init__(self, dtype: str, name: str):
        self.dtype: str = dtype
        self.name: str  = name
        self.args: List[str] = []
        self.block = StatementBlock()
    def __str__(self):
        result = f"{self.dtype} {self.name} ("
        for arg in self.args:
            result += f"{str(arg)}, "
        # remove last ", "
        result = result[:-2]
        result += ")" + str(self.block)
        return result

class Program:
    def __init__(self):
        self.blocks = []
    def __str__(self):
        result = ""
        for block in self.blocks:
            result += str(block)
        return result

p = Program()
f = FuncDef("int", "main")
f.args = ("int argc", "char **argv")
f.block.push(StatementInst("float", "a"))
f.block.push(StatementInit("int", "b", "10"))
f.block.push(StatementAssign("a", "5.0"))
f.block.push(StatementFor("int i = 0", "i < 10", "i++"))
f.block[-1].block.push(StatementIf("i < 6"))
f.block[-1].block[-1].block.push("printf(\"%d\\n\", i);")
f.block.push(StatementControl("return", "0"))

p.blocks.append("#include <stdio.h>\n")
p.blocks.append(f)
print(str(p))

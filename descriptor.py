import sys
from typing import List

class Block:
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
    def append(self, statement):
        self.statements.append(statement)

class StatementVar:
    def __init__(self, name: str, dtype=None, expr=None):
        self.name = name
        self.dtype = dtype
        self.expr = expr
    def __str__(self):
        result = ""
        if self.dtype:
            result += f"{str(self.dtype)} "
        result += str(self.name)
        if self.expr:
            result += f" = {str(self.expr)}"
        result += ";"
        return result

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

class StatementBlock:
    def __init__(self, name: str, args, sep=","):
        self.name = name
        self.args = args
        self.block = Block()
        self.sep = sep
    def __str__(self):
        result = ""
        if isinstance(self.name, str):
            result += str(self.name)
        elif isinstance(self.name, tuple) or isinstance(self.name, list):
            for desc in self.name:
                result += f"{str(desc)} "
        elif isinstance(self.name, dict):
            for t, ident in self.name:
                result += f"{str(t)} {str(ident)}"
        else:
            print(f"Error - unexpected type Statement.name: {type(self.name)}", file=sys.stderr)
            exit(-1)

        result += "("

        if isinstance(self.args, str):
            result += str(self.args)
        elif isinstance(self.args, tuple) or isinstance(self.args, list):
            for arg in self.args:
                result += f"{str(arg)}{self.sep} "
            result = result[:-2]
        elif isinstance(self.args, dict):
            for t, ident in self.args:
                result += f"{str(t)} {str(ident)}{self.sep} "
            result = result[:-2]
        else:
            print(f"Error - unexpected type Statement.args: {type(self.args)}", file=sys.stderr)
            exit(-1)
        
        result += ")\n"
        result += str(self.block)
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
p.blocks.append("#include <stdio.h>\n")
f = StatementBlock(["int", "main"], ["int argc", "char **argv"])
f.block.append(StatementVar("a", "int"))
f.block.append(StatementVar("b", "float", "10"))
f.block.append(StatementVar("a", expr="5"))
f.block.append(StatementBlock("for", ["int i = 0", "i < 10", "i++"], sep=";"))
f.block[-1].block.append("printf(\"%d\\n\", i);")
p.blocks.append(f)

print(str(p))

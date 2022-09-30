from typing import List
from decorators.visitor import visitor
from expr import Binary, Expr, Grouping, Literal, Unary


def _parenthesize(name: str, *exprs: Expr):
    visitor = AstVisitor()
    sb: List[str] = []
    sb.append(f"({name}")
    for expr in exprs:
        sb.append(f" {expr.accept(visitor)}")
    sb.append(")")
    return "".join(sb)


class AstVisitor(object):
    @visitor(Binary)
    def visit(self, expr: Binary):
        return _parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @visitor(Grouping)
    def visit(self, expr: Grouping):
        return _parenthesize("group", expr.expression)

    @visitor(Literal)
    def visit(self, expr: Literal):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    @visitor(Unary)
    def visit(self, expr: Unary):
        return _parenthesize(expr.operator.lexeme, expr.right)

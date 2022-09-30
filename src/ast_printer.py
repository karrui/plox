from ast_visitor import AstVisitor
from expr import Binary, Expr, Grouping, Literal, Unary
from _token import Token
from token_type import TokenType


class AstPrinter:
    def print(self, expr: Expr):
        visitor = AstVisitor()
        return expr.accept(visitor)


# Test method to see if AST processes correctly.
# if __name__ == "__main__":
#     expr = Binary(Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
#                   Token(TokenType.STAR, "*", None, 1),
#                   Grouping(Literal(45.67))
#                   )
#     print(AstPrinter().print(expr))

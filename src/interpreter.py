from decorators.visitor import visitor
from expr import Binary, Expr, Grouping, Literal, Unary
from token_type import TokenType as T
from utils.equality import is_equal
from utils.truthy import is_truthy


class Interpreter:
    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    @visitor(Literal)
    def visit(self, expr: Literal):
        return expr.value

    @visitor(Grouping)
    def visit(self, expr: Grouping):
        return self._evaluate(expr.expression)

    @visitor(Unary)
    def visit(self, expr: Unary):
        right = self._evaluate(expr.right)

        match expr.operator.type:
            case T.MINUS:
                return -float(right)
            case T.BANG:
                return not is_truthy(right)

        # Unreachable
        return None

    @visitor(Binary)
    def visit(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        match (expr.operator.type):
            case T.GREATER:
                return float(left) > float(right)
            case T.GREATER_EQUAL:
                return float(left) >= float(right)
            case T.LESS:
                return float(left) < float(right)
            case T.LESS_EQUAL:
                return float(left) <= float(right)
            case T.MINUS:
                return float(left) - float(right)
            case T.SLASH:
                return float(left) / float(right)
            case T.STAR:
                return float(left) * float(right)
            case T.PLUS:
                # Only perform actions when both left and right instances are of the same type.
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
            case T.BANG_EQUAL:
                return not is_equal(left, right)
            case T.EQUAL_EQUAL:
                return is_equal(left, right)

        # Unreachable
        return None

from typing import List
from decorators.visitor import visitor
from expr import Binary, Expr, Grouping, Literal, Unary
from stmt import Expression, Print, Stmt
from _token import Token
from token_type import TokenType as T
from utils.equality import is_equal
from utils.strings import stringify
from utils.truthy import is_truthy
from error import Error, LoxRuntimeError


def check_number_operands(operator: Token, *operands: object):
    for operand in operands:
        if not isinstance(operand, float):
            err_msg = "Operand must be a number" if len(
                operands) == 1 else "Operands must be numbers"
            raise LoxRuntimeError(operator, err_msg)


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
                check_number_operands(expr.operator, right)
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
                check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case T.GREATER_EQUAL:
                check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case T.LESS:
                check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case T.LESS_EQUAL:
                check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case T.MINUS:
                check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case T.SLASH:
                check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case T.STAR:
                check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case T.PLUS:
                # Only perform actions when both left and right instances are of the same type.
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                raise LoxRuntimeError(
                    expr.operator, "Operands must be two numbers or two strings.")
            case T.BANG_EQUAL:
                return not is_equal(left, right)
            case T.EQUAL_EQUAL:
                return is_equal(left, right)
        # Unreachable
        return None

    @visitor(Expression)
    def visit(self, stmt: Expression):
        self._evaluate(stmt.expression)
        return None

    @visitor(Print)
    def visit(self, stmt: Print):
        value = self._evaluate(stmt.expression)
        print(stringify(value))
        return None

    def _execute(self, stmt: Stmt):
        stmt.accept(self)

    def interpret(self, statements: List[Stmt]):
        try:
            for statement in statements:
                self._execute(statement)
        except LoxRuntimeError as err:
            Error.runtime_error(err)

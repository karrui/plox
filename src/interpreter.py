from typing import List
from decorators.visitor import visitor
from environment import Environment
from expr import Assign, Binary, Expr, Grouping, Literal, Logical, Unary, Variable
from stmt import Block, Expression, If, Print, Stmt, Var
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
    _environment = Environment()

    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    def _execute(self, stmt: Stmt):
        stmt.accept(self)

    def _execute_block(self, statements: List[Stmt], environment: Environment):
        previous = self._environment
        try:
            self._environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self._environment = previous

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

    @visitor(Variable)
    def visit(self, expr: Variable):
        return self._environment.get(expr.name)

    @visitor(Assign)
    def visit(self, expr: Assign):
        value = self._evaluate(expr.value)
        self._environment.assign(expr.name, value)
        return value

    @visitor(Logical)
    def visit(self, expr: Logical):
        left = self._evaluate(expr.left)
        if expr.operator.type == T.OR:
            # Short circuit if truthy.
            if is_truthy(left):
                return left
        else:
            if not is_truthy(left):
                return left
        # Evaluate right if left is not truthy.
        return self._evaluate(expr.right)

    @visitor(Expression)
    def visit(self, stmt: Expression):
        self._evaluate(stmt.expression)
        return None

    @visitor(Print)
    def visit(self, stmt: Print):
        value = self._evaluate(stmt.expression)
        print(stringify(value))
        return None

    @visitor(Var)
    def visit(self, stmt: Var):
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self._environment.define(stmt.name.lexeme, value)
        return None

    @visitor(Block)
    def visit(self, stmt: Block):
        self._execute_block(stmt.statements, Environment(self._environment))
        return None

    @visitor(If)
    def visit(self, stmt: If):
        if is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)
        return None

    def interpret(self, statements: List[Stmt]):
        try:
            for statement in statements:
                self._execute(statement)
        except LoxRuntimeError as err:
            Error.runtime_error(err)

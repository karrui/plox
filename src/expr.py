from abc import abstractclassmethod
import typing
from dataclasses import dataclass
from _token import Token


class Expr:
    @abstractclassmethod
    def accept() -> typing.Any:
        pass


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit(self)


@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visit(self)


@dataclass(frozen=True)
class Literal(Expr):
    value: typing.Any

    def accept(self, visitor):
        return visitor.visit(self)


@dataclass(frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit(self)

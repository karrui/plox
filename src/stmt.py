from abc import abstractclassmethod
import typing
from dataclasses import dataclass
from _token import Token
from expr import Expr


class Stmt:
    @abstractclassmethod
    def accept() -> typing.Any:
        pass


@dataclass(frozen=True)
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor):
        return visitor.visit(self)


@dataclass(frozen=True)
class Print(Stmt):
    expression: Expr

    def accept(self, visitor):
        return visitor.visit(self)


@dataclass(frozen=True)
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor):
        return visitor.visit(self)

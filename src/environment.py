from _token import Token
from error import LoxRuntimeError


class Environment:
    values = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object):
        # Assignment not allowed to create new variable.
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

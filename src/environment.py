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

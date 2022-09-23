from _token import Token
from error import Error
from token_type import TokenType as T


class Scanner:
    def __init__(self, source: str) -> None:
        self.start = 0
        self.current = 0
        self.line = 1
        self.source = source
        self.tokens = []

    def scan_tokens(self) -> list[str]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(T.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: T) -> None:
        self._add_token(type, None)

    def _add_token(self, type: T, literal: object) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def scan_token(self) -> None:
        c = self.advance()
        match c:
            case '(':
                self.add_token(T.LEFT_PAREN)
            case ')':
                self.add_token(T.RIGHT_PAREN)
            case '{':
                self.add_token(T.LEFT_BRACE)
            case '}':
                self.add_token(T.RIGHT_BRACE)
            case ',':
                self.add_token(T.COMMA)
            case '.':
                self.add_token(T.DOT)
            case '-':
                self.add_token(T.MINUS)
            case '+':
                self.add_token(T.PLUS)
            case ';':
                self.add_token(T.SEMICOLON)
            case '*':
                self.add_token(T.STAR)
            case '!':
                self.add_token(T.BANG_EQUAL if self.match('=') else T.BANG)
            case '=':
                self.add_token(T.EQUAL_EQUAL if self.match('=') else T.EQUAL)
            case '<':
                self.add_token(T.LESS_EQUAL if self.match('=') else T.LESS)
            case '>':
                self.add_token(
                    T.GREATER_EQUAL if self.match('=') else T.GREATER)
            case _:
                Error.error(self.line, "Unexpected character.")

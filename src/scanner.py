from _token import Token
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

    def scan_token(self):
        pass

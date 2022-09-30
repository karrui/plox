from typing import List
from _token import Token
from error import Error
from utils.strings import is_alnum
from token_type import TokenType as T, KEYWORDS_DICT


class Scanner:
    def __init__(self, source: str) -> None:
        self._start = 0
        self._current = 0
        self._line = 1
        self._source = source
        self._tokens: List[Token] = []

    def scan_tokens(self) -> list[str]:
        while not self._is_at_end():
            self._start = self._current
            self.scan_token()

        self._tokens.append(Token(T.EOF, "", None, self._line))
        return self._tokens

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def _advance(self) -> str:
        next_char = self._source[self._current]
        self._current += 1
        return next_char

    def _add_token(self, type: T) -> None:
        self._add_token_literal(type, None)

    def _add_token_literal(self, type: T, literal: object) -> None:
        text = self._source[self._start:self._current]
        self._tokens.append(Token(type, text, literal, self._line))

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self._source[self._current] != expected:
            return False
        self._current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return '\0'
        return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return '\0'
        return self._source[self._current + 1]

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '\n':
                self._line += 1
            self._advance()
        if self._is_at_end():
            Error.error(self._line, "Unterminated string")
            return
        # The closing `"`.
        self._advance()
        # Trim the surrounding quotes.
        value = self._source[self._start+1:self._current - 1]
        self._add_token_literal(T.STRING, value)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        # Look for a fractional part.
        # TODO: Fix bug where double dot causes invalid parsing, e.g.
        # 1234.52890.4 -> [NUMBER 1234.52890, DOT, NUMBER 4.0]
        if self._peek() == '.' and self._peek_next().isdigit():
            # Consume the "."
            self._advance()
            while self._peek().isdigit():
                self._advance()
        self._add_token_literal(T.NUMBER, float(
            self._source[self._start: self._current]))

    def _identifier(self) -> None:
        while is_alnum(self._peek()):
            self._advance()

        text = self._source[self._start:self._current]
        token_type = KEYWORDS_DICT.get(text)
        if token_type == None:
            token_type = T.IDENTIFIER
        self._add_token(token_type)

    def scan_token(self) -> None:
        c = self._advance()
        match c:
            case '(':
                self._add_token(T.LEFT_PAREN)
            case ')':
                self._add_token(T.RIGHT_PAREN)
            case '{':
                self._add_token(T.LEFT_BRACE)
            case '}':
                self._add_token(T.RIGHT_BRACE)
            case ',':
                self._add_token(T.COMMA)
            case '.':
                self._add_token(T.DOT)
            case '-':
                self._add_token(T.MINUS)
            case '+':
                self._add_token(T.PLUS)
            case ';':
                self._add_token(T.SEMICOLON)
            case '*':
                self._add_token(T.STAR)
            case '!':
                self._add_token(T.BANG_EQUAL if self._match('=') else T.BANG)
            case '=':
                self._add_token(T.EQUAL_EQUAL if self._match('=') else T.EQUAL)
            case '<':
                self._add_token(T.LESS_EQUAL if self._match('=') else T.LESS)
            case '>':
                self._add_token(
                    T.GREATER_EQUAL if self._match('=') else T.GREATER)
            case '/':
                if self._match('/'):
                    # A comment goes until the end of the line
                    while self._peek() != '\n' and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(T.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self._line += 1
            case '"':
                self._string()
            case c if c.isdigit():
                self._number()
            case c if c.isalpha():
                self._identifier()
            case _:
                Error.error(self._line, "Unexpected character.")

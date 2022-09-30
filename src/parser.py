from typing import List
from error import Error
from _token import Token
from expr import Binary, Expr, Grouping, Literal, Unary
from token_type import TokenType as T


class ParseError(RuntimeError):
    '''raise this when there's a parse error'''


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self._tokens = tokens
        self._current = 0

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == T.EOF

    def _check(self, type: T) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _match(self, *types: T) -> bool:
        for type in types:
            if (self._check(type)):
                self._advance()
                return True
        return False

    def _synchronise(self):
        self._advance()
        while not self._is_at_end():
            if self._previous().type == T.SEMICOLON:
                return
            match self._peek().type:
                case T.CLASS | T.FUN | T.VAR | T.FOR | T.IF | T.WHILE | T.PRINT | T.RETURN:
                    return
            self._advance()

    def _error(self, token: Token, err_msg: str):
        Error.parse_error(token, err_msg)
        return ParseError()

    def _consume(self, type: T, err_msg: str):
        if self._check(type):
            return self._advance()
        raise self._error(self._peek(), err_msg)

    def _primary(self) -> Expr:
        if self._match(T.FALSE):
            return Literal(False)
        if self._match(T.TRUE):
            return Literal(True)
        if self._match(T.NIL):
            return Literal(None)

        if self._match(T.NUMBER, T.STRING):
            return Literal(self._previous().literal)

        if self._match(T.LEFT_PAREN):
            expr = self._expression()
            self._consume(T.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _unary(self) -> Expr:
        while self._match(T.BANG, T.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        return self._primary()

    def _factor(self) -> Expr:
        expr = self._unary()
        while self._match(T.SLASH, T.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while self._match(T.MINUS, T.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self) -> Expr:
        expr = self._term()
        while self._match(T.GREATER, T.GREATER_EQUAL, T.LESS, T.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)
        return expr

    def _equality(self) -> Expr:
        expr = self._comparison()
        while self._match(T.BANG_EQUAL, T.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _expression(self) -> Expr:
        return self._equality()

    # Finally public functions
    def parse(self):
        try:
            return self._expression()
        except ParseError:
            return None

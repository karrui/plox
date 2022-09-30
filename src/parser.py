from typing import List
from error import Error
from _token import Token
from expr import Assign, Binary, Expr, Grouping, Literal, Unary, Variable
from stmt import Expression, Print, Stmt, Var
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

    def _primary(self):
        if self._match(T.FALSE):
            return Literal(False)
        if self._match(T.TRUE):
            return Literal(True)
        if self._match(T.NIL):
            return Literal(None)

        if self._match(T.IDENTIFIER):
            return Variable(self._previous())

        if self._match(T.NUMBER, T.STRING):
            return Literal(self._previous().literal)

        if self._match(T.LEFT_PAREN):
            expr = self._expression()
            self._consume(T.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _unary(self):
        while self._match(T.BANG, T.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        return self._primary()

    def _factor(self):
        expr = self._unary()
        while self._match(T.SLASH, T.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)
        return expr

    def _term(self):
        expr = self._factor()
        while self._match(T.MINUS, T.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match(T.GREATER, T.GREATER_EQUAL, T.LESS, T.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)
        return expr

    def _equality(self):
        expr = self._comparison()
        while self._match(T.BANG_EQUAL, T.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _assignment(self):
        expr = self._equality()

        if self._match(T.EQUAL):
            equals = self._previous()
            value = self._assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self._error(equals, "Invalid assignment target.")
        return expr

    def _expression(self):
        return self._assignment()

    def _print_statement(self):
        value = self._expression()
        self._consume(T.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def _expression_statement(self):
        expr = self._expression()
        self._consume(T.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def _statement(self):
        if self._match(T.PRINT):
            return self._print_statement()
        return self._expression_statement()

    def _var_declaration(self):
        name = self._consume(T.IDENTIFIER, "Expect variable name.")

        initializer: Expr = None
        if self._match(T.EQUAL):
            initializer = self._expression()
        self._consume(T.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def _declaration(self):
        try:
            if self._match(T.VAR):
                return self._var_declaration()
            return self._statement()
        except ParseError:
            self._synchronise()
            return None

    # Finally public functions
    def parse(self) -> List[Stmt]:
        statements: List[Stmt] = []
        while not self._is_at_end():
            statements.append(self._declaration())
        return statements

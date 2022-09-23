from enum import Enum, auto


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'

    EOF = auto()


KEYWORDS_DICT = {
    TokenType.AND.value: TokenType.AND,
    TokenType.CLASS.value: TokenType.CLASS,
    TokenType.ELSE.value: TokenType.ELSE,
    TokenType.FALSE.value: TokenType.FALSE,
    TokenType.FOR.value: TokenType.FOR,
    TokenType.FUN.value: TokenType.FUN,
    TokenType.IF.value: TokenType.IF,
    TokenType.NIL.value: TokenType.NIL,
    TokenType.OR.value: TokenType.OR,
    TokenType.PRINT.value: TokenType.PRINT,
    TokenType.RETURN.value: TokenType.RETURN,
    TokenType.SUPER.value: TokenType.SUPER,
    TokenType.THIS.value: TokenType.THIS,
    TokenType.TRUE.value: TokenType.TRUE,
    TokenType.VAR.value: TokenType.VAR,
    TokenType.WHILE.value: TokenType.WHILE,
}

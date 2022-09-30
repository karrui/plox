from _token import TokenType, Token


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token


class Error:
    had_error = False
    had_runtime_error = False

    def runtime_error(err: LoxRuntimeError):
        print(f"{str(err)}\n[line {err.token.line}]")
        Error.had_runtime_error = True

    def parse_error(token: Token, message: str):
        if (token.type == TokenType.EOF):
            Error.report(token.line, " at end", message)
        else:
            Error.report(token.line, " at ", token.lexeme + "'")

    def error(line, message):
        Error.report(line, "", message)

    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        Error.had_error = True

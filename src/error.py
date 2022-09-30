from _token import TokenType, Token


class Error:
    had_error = False

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

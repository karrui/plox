class Error:
    had_error = False

    def error(line, message):
        Error.report(line, "", message)

    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        Error.had_error = True

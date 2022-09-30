import sys
from ast_printer import AstPrinter
from interpreter import Interpreter
from parser import Parser

from scanner import Scanner
from error import Error


class Plox:
    interpreter = Interpreter()

    def __init__(self) -> None:

        # 1st element of sys.argv is always invoked file
        if len(sys.argv) > 2:
            print('Usage: plox [script]')
            sys.exit(64)
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()

    def run_file(self, file_path: str) -> None:
        with open(file_path) as file:
            file_data = file.read()
            self.run(file_data)
            if Error.had_error:
                sys.exit(65)
            if Error.had_runtime_error:
                sys.exit(70)

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()

        # Stop if there was a syntax error.
        if Error.had_error:
            return

        self.interpreter.interpret(statements)

    def run_prompt(self) -> None:
        while True:
            try:
                line = input("> ")
                if line == "":
                    break
                self.run(line)
                Error.had_error = False  # Reset errors if any in prompt
            except EOFError:
                break


if __name__ == "__main__":
    plox = Plox()

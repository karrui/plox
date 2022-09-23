import sys

from scanner import Scanner


class Plox:
    def __init__(self) -> None:
        self.had_error = False

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
            if (self.had_error):
                sys.exit(65)

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def run_prompt(self) -> None:
        while True:
            try:
                line = input("> ")
                if line == "":
                    break
                self.run(line)
                self.had_error = False  # Reset errors if any in prompt
            except EOFError:
                break

    def error(self, line: int, message: str) -> None:
        self.report(line, '', message)

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True


if __name__ == "__main__":
    plox = Plox()

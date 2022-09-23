import sys

from scanner import Scanner


class Plox:
    def __init__(self) -> None:
        print(sys.argv)
        # 1st element of sys.argv is always invoked file
        if len(sys.argv) > 2:
            print('Usage: plox [script]')
            sys.exit(64)
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()

    def run_file(self, file_path: str):
        with open(file_path) as file:
            file_data = file.read()
            self.run(file_data)
            # TODO: Handle error

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def run_prompt(self):
        while True:
            try:
                line = input("> ")
                if line == "":
                    break
                self.run(line)
            except EOFError:
                break


if __name__ == "__main__":
    plox = Plox()

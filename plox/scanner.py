class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source

    def scan_tokens(self) -> list[str]:
        return list(self.source)

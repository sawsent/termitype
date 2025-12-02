
class RunReport:
    def __init__(self, wpm: float, time_ns: float, word_amount: int, expected_text: str, typed_text: str, accuracy: int):
        self.wpm: float = wpm
        self.time_ns: float = time_ns
        self.time_s: float = time_ns / 1000000000
        self.word_amount: int = word_amount
        self.expected_text: str = expected_text
        self.typed_text: str = typed_text
        self.accuracy: int = accuracy


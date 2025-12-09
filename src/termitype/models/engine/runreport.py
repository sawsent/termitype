from typing import Dict, Self

class RunReport:
    def __init__(self, wpm: float, start_time: float, end_time: float, time_ns: float, word_amount: int, expected_text: str, typed_text: str, accuracy: int):
        self.wpm: float = wpm
        self.time_ns: float = time_ns
        self.time_s: float = time_ns / 1000000000
        self.word_amount: int = word_amount
        self.expected_text: str = expected_text
        self.typed_text: str = typed_text
        self.accuracy: int = accuracy
        self.start_time: float = start_time
        self.end_time: float = end_time

    @property
    def as_dict(self) -> Dict:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "time_ns": self.time_ns,
            "time_s": self.time_s,
            "typed": self.typed_text,
            "expected": self.expected_text,
            "wpm": self.wpm,
            "accuracy": self.accuracy,
            "word_amount": self.word_amount
        }

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        return cls(
            wpm = d["wpm"],
            start_time = d["start_time"],
            end_time = d["end_time"],
            time_ns = d["time_ns"],
            word_amount = d["word_amount"],
            expected_text = d["expected"],
            typed_text = d["typed"],
            accuracy = d["accuracy"]
        )


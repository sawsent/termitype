from enum import Enum
import time
from typing import List, Optional, Self


class SegmentType(Enum):
    CORRECT = 1
    INCORRECT = 2
    TO_BE_TYPED = 3
    MISSED = 4

class RunSegment:
    @classmethod
    def SPACE(cls) -> Self:
        return cls(SegmentType.CORRECT, " ")

    @classmethod
    def CORRECT(cls, text: str) -> Self:
        return cls(SegmentType.CORRECT, text)

    @classmethod
    def INCORRECT(cls, text: str) -> Self:
        return cls(SegmentType.INCORRECT, text)

    @classmethod
    def TO_BE_TYPED(cls, text: str) -> Self:
        return cls(SegmentType.TO_BE_TYPED, text)

    @classmethod
    def MISSED(cls, text: str) -> Self:
        return cls(SegmentType.MISSED, text)

    def __init__(self, segment_type: SegmentType, text: str) -> None:
        self.segment_type: SegmentType = segment_type
        self.text: str = text

class Run:
    def __init__(self, word_list: List[str]) -> None:
        self.start_time_ns: Optional[int] = None
        self.end_time_ns: Optional[int] = None
        self.word_list: List[str] = word_list
        self.words_typed: List[str] = []
        self.current_word: str = ""

    def start(self) -> None:
        self.start_time_ns = time.time_ns()

    def finish(self) -> None:
        self.end_time_ns = time.time_ns()

    def type_char(self, char: str) -> None:
        match char:
            case " " if self.current_word is not "":
                self.words_typed.append(self.current_word)
                self.current_word = ""
            case " ":
                pass
            case _: self.current_word += char

    def backspace(self) -> None:
        if self.current_word != "":
            self.current_word = self.current_word[:-1]
        elif self.current_word == "" and len(self.words_typed) >= 1:
            self.current_word = self.words_typed.pop()


    @property
    def in_play(self) -> bool:
        return self.started and not self.finished

    @property
    def started(self) -> bool:
        return self.start_time_ns is not None

    @property
    def run_time(self) -> Optional[int]:
        if self.start_time_ns is not None and self.end_time_ns is not None:
            return self.end_time_ns - self.start_time_ns
        else:
            return None

    @property
    def finished(self) -> bool:
        return self.start_time_ns is not None and self.end_time_ns is not None

    def get_segments(self) -> List[List[RunSegment]]:
        return self.__get_segments()

    def __get_segments(self) -> List[List[RunSegment]]:
        typed_words: List[List[RunSegment]] = []

        last_word_idx = len(self.words_typed)
        last_word: str = self.current_word
        
        for (typed, expected) in zip(self.words_typed, self.word_list):
            typed_words.append(self.get_segments_for_word(typed, expected))
            
        last_word_segments = self.get_segments_for_last_word(last_word, self.word_list[last_word_idx])
        typed_words.append(last_word_segments)

        untyped_words = [ [RunSegment.TO_BE_TYPED(word)] for word in self.word_list[last_word_idx + 1:] ]

        return typed_words + untyped_words

    def get_segments_for_last_word(self, typed: str, expected: str) -> List[RunSegment]:
        if len(typed) < len(expected):
            typed_segments = [RunSegment.CORRECT(typed[idx]) if t == e else RunSegment.INCORRECT(typed[idx]) for idx, (t, e) in enumerate(zip(typed, expected))]
            return typed_segments + [RunSegment.TO_BE_TYPED(expected[len(typed):])]
        elif len(typed) == len(expected):
            typed_segments = [RunSegment.CORRECT(typed[idx]) if t == e else RunSegment.INCORRECT(typed[idx]) for idx, (t, e) in enumerate(zip(typed, expected))]
            return typed_segments
        else:
            typed_segments = [RunSegment.CORRECT(typed[idx]) if t == e else RunSegment.INCORRECT(typed[idx]) for idx, (t, e) in enumerate(zip(typed, expected))]
            return typed_segments + [RunSegment.INCORRECT(typed[len(expected):])]

    def get_segments_for_word(self, typed: str, expected: str) -> List[RunSegment]:
        if len(typed) < len(expected):
            typed_segments = [RunSegment.CORRECT(typed[idx]) if t == e else RunSegment.INCORRECT(typed[idx]) for idx, (t, e) in enumerate(zip(typed, expected))]
            return typed_segments + [RunSegment.MISSED(expected[len(typed):])]
        elif len(typed) == len(expected):
            typed_segments = [RunSegment.CORRECT(typed[idx]) if t == e else RunSegment.INCORRECT(typed[idx]) for idx, (t, e) in enumerate(zip(typed, expected))]
            return typed_segments
        else:
            typed_segments = [RunSegment.CORRECT(typed[idx]) if t == e else RunSegment.INCORRECT(typed[idx]) for idx, (t, e) in enumerate(zip(typed, expected))]
            return typed_segments + [RunSegment.INCORRECT(typed[len(expected):])]



    def merge_segments(self, segments: List[RunSegment]) -> List[RunSegment]:
        if not segments:
            return []

        merged = []
        current_type = segments[0].segment_type
        current_text = segments[0].text

        for seg in segments[1:]:
            if seg.segment_type == current_type:
                current_text += seg.text
            else:
                merged.append(RunSegment(current_type, current_text))
                current_type = seg.segment_type
                current_text = seg.text

        merged.append(RunSegment(current_type, current_text))
        return merged



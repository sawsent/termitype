from typing import List

from termitype.utils.color import visible_len


def chunk_words(text: str, size: int) -> List[str]:
        text = text.strip()
        if not text:
            return []

        words = text.split()
        lines: List[str] = []
        current_line = ""

        for word in words:
            if not current_line:
                current_line = word
            elif visible_len(current_line) + 1 + visible_len(word) <= size:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

def pad(text: str, l: int = 0, r: int = 0, pad_char: str = " ") -> str:
    return f"{pad_char * l}{text}{pad_char * r}"


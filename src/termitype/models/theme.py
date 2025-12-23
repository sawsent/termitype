from typing import Dict, Self
from termitype.utils.color import Color


class Theme:
    def __init__(
        self,
        base_color: Color,
        typed_correctly_color: Color,
        untyped_color: Color,
        typed_incorrectly_color: Color,
        missed_color: Color,
        extra_color: Color
    ) -> None:
        self.base_color: Color = base_color
        self.typed_correctly_color: Color = typed_correctly_color
        self.untyped_color: Color = untyped_color
        self.typed_incorrectly_color: Color = typed_incorrectly_color
        self.missed_color: Color = missed_color
        self.extra_color: Color = extra_color

    @classmethod
    def default(cls) -> Self:
        return cls(
            base_color = Color.WHITE,
            typed_correctly_color = Color.WHITE,
            untyped_color = Color.BRIGHT_BLACK,
            typed_incorrectly_color = Color.RED,
            missed_color = Color.GREEN,
            extra_color = Color.CYAN
        )

    @classmethod
    def from_dict(cls, d: Dict) -> Self:
        default = cls.default()
        return cls(
            base_color = Color.from_string(d.get("base", default.base_color.name)),
            typed_correctly_color = Color.from_string(d.get("typed_correctly", default.typed_correctly_color.name)),
            untyped_color = Color.from_string(d.get("untyped", default.untyped_color.name)),
            typed_incorrectly_color = Color.from_string(d.get("typed_incorrectly", default.typed_incorrectly_color.name)),
            missed_color = Color.from_string(d.get("missed", default.missed_color.name)),
            extra_color = Color.from_string(d.get("extra", default.extra_color.name)),
        )


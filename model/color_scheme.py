from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple

# ---------- Enums ----------


class RGB(NamedTuple):
    r: int
    g: int
    b: int

    @classmethod
    def from_hex(cls, value: str) -> Self:
        h = value.lstrip("#")
        return cls(*(int(h[i : i + 2], 16) for i in (0, 2, 4)))

    @property
    def hex(self) -> str:
        return "#{:02x}{:02x}{:02x}".format(*self)

    @property
    def css(self) -> str:
        return f"rgb({self.r}, {self.g}, {self.b})"


class Colors(NamedTuple):
    text: RGB
    bg: RGB


class ColorEnum(StrEnum):
    """StrEnum whose members carry a (text, bg) RGB pair."""

    colors: Colors

    def __new__(cls, value: str, text: tuple[int, int, int], bg: tuple[int, int, int]):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.colors = Colors(RGB(*text), RGB(*bg))
        return obj


class Theme(ColorEnum):
    LIGHT = "light", (62, 62, 66), (230, 230, 250)
    DARK = "dark", (230, 230, 250), (62, 62, 66)
    DIM = "dim", (244, 244, 244), (36, 52, 71)
    SOLARIZED_LIGHT = "solarized-light", (0, 43, 54), (253, 246, 227)
    SOLARIZED_DARK = "solarized-dark", (253, 246, 227), (0, 43, 54)
    MUTED = "muted", (237, 227, 241), (26, 26, 46)
    OCEAN = "ocean", (220, 231, 243), (27, 49, 86)
    NEBULA = "nebula", (175, 199, 255), (2, 0, 59)
    ASTROPHAGE = "astrophage", (239, 239, 239), (0, 0, 0)
    MIDNIGHT = "midnight", (226, 232, 240), (15, 23, 42)
    GRAPHITE = "graphite", (239, 231, 235), (24, 24, 27)
    FOREST = "forest", (220, 252, 231), (5, 46, 22)
    PLUM = "plum", (243, 232, 255), (59, 7, 100)


class Accent(ColorEnum):
    DEFAULT = "default", (182, 2, 112), (0, 56, 168)
    WHITE = "white", (255, 255, 255), (0, 0, 0)
    GREEN = "green", (9, 121, 105), (11, 23, 42)
    PINK = "pink", (245, 169, 184), (91, 206, 250)
    RED = "red", (222, 49, 99), (11, 23, 42)
    DARKRED = "darkred", (151, 24, 61), (11, 23, 42)
    PURPLE = "purple", (100, 67, 130), (20, 20, 36)
    BLUE = "blue", (102, 179, 255), (21, 39, 68)
    DARKBLUE = "darkblue", (103, 145, 255), (1, 0, 47)
    DARKPINK = "darkpink", (219, 39, 119), (157, 23, 77)
    EARTH = "earth", (234, 129, 29), (154, 65, 0)
    CYAN = "cyan", (6, 182, 212), (14, 116, 144)
    TEAL = "teal", (20, 184, 166), (15, 118, 110)
    SKY = "sky", (14, 165, 233), (3, 105, 161)
    VIOLET = "violet", (139, 92, 246), (109, 40, 217)
    AMBER = "amber", (245, 158, 11), (180, 83, 9)
    YELLOW = "yellow", (234, 179, 8), (161, 98, 7)
    LIME = "lime", (132, 204, 22), (77, 124, 15)
    ORANGE = "orange", (249, 115, 22), (194, 65, 12)


@dataclass(frozen=True)
class Colorscheme:
    theme: Theme
    accent: Accent

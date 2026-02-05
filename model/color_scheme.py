from typing import NamedTuple
from enum import StrEnum
from dataclasses import dataclass


# ---------- Enums ----------


class Theme(StrEnum):
    LIGHT = "light"
    DARK = "dark"
    DIM = "dim"
    SOLARIZED_LIGHT = "solarized-light"
    SOLARIZED_DARK = "solarized-dark"
    MUTED = "muted"
    OCEAN = "ocean"
    NEBULA = "nebula"


class Accent(StrEnum):
    DEFAULT = "default"
    WHITE = "white"
    GREEN = "green"
    PINK = "pink"
    RED = "red"
    DARKRED = "darkred"
    PURPLE = "purple"
    BLUE = "blue"
    DARKBLUE = "darkblue"


# ---------- NamedTuple Types ----------

class ThemeColors(NamedTuple):
    text: str
    bg: str


class AccentColors(NamedTuple):
    text: str
    bg: str


# ---------- Theme Colors ----------

THEME_COLORS = {
    Theme.LIGHT: ThemeColors("#3e3e42", "#e6e6fa"),
    Theme.DARK: ThemeColors("#e6e6fa", "#3e3e42"),
    Theme.DIM: ThemeColors("#f4f4f4", "#243447"),
    Theme.SOLARIZED_LIGHT: ThemeColors("#002b36", "#fdf6e3"),
    Theme.SOLARIZED_DARK: ThemeColors("#fdf6e3", "#002b36"),
    Theme.MUTED: ThemeColors("#EDE3F1", "#1a1a2e"),
    Theme.OCEAN: ThemeColors("#dce7f3", "#1b3156"),
    Theme.NEBULA: ThemeColors("#afc7ff", "#02003b"),
}


# ---------- Accent Colors ----------

ACCENT_COLORS = {
    Accent.DEFAULT: AccentColors("#B60270", "#0038A8"),
    Accent.GREEN: AccentColors("#097969", "#0B172A"),
    Accent.RED: AccentColors("#DE3163", "#0B172A"),
    Accent.PINK: AccentColors("#F5A9B8", "#5BCEFA"),
    Accent.WHITE: AccentColors("#FFFFFF", "#000000"),
    Accent.DARKRED: AccentColors("#97183D", "#0B172A"),
    Accent.PURPLE: AccentColors("#644382", "#141424"),
    Accent.BLUE: AccentColors("#66b3ff", "#152744"),
    Accent.DARKBLUE: AccentColors("#6791ff", "#01002f"),
}

# ---------- Helpers ----------


def get_theme_colors(theme: Theme) -> dict[str, str]:
    return THEME_COLORS[theme]


def get_accent_colors(accent: Accent) -> dict[str, str]:
    return ACCENT_COLORS[accent]


@dataclass(frozen=True)
class Colorscheme:
    theme: Theme
    accent: Accent

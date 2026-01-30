from enum import Enum


class SizeType(str, Enum):
    thumbnail = "thumbnail"
    small = "small"
    medium = "medium"
    large = "large"
    print = "print"


class PlotSize(Enum):
    THUMBNAIL = ((6, 3), 100)
    SMALL = ((12, 6), 100)
    MEDIUM = ((16, 8), 120)
    LARGE = ((20, 10), 150)
    PRINT = ((24, 12), 300)

    @property
    def figsize(self):
        return self.value[0]

    @property
    def dpi(self):
        return self.value[1]


_SIZE_MAP = {
    SizeType.thumbnail: PlotSize.THUMBNAIL,
    SizeType.small:     PlotSize.SMALL,
    SizeType.medium:    PlotSize.MEDIUM,
    SizeType.large:     PlotSize.LARGE,
    SizeType.print:     PlotSize.PRINT,
}


def plot_size(size: SizeType) -> PlotSize:
    return _SIZE_MAP[size]

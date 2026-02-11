from enum import Enum

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types#image_types
# image/png: Portable Network Graphics (PNG)
# image/svg+xml: Scalable Vector Graphics (SVG)


class ImageFormat(str, Enum):
    svg = "svg"
    png = "png"

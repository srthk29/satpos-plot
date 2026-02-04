from enum import Enum


class Feature(str, Enum):
    borders = "BORDERS"
    coastline = "COASTLINE"
    lakes = "LAKES"
    land = "LAND"
    ocean = "OCEAN"
    rivers = "RIVERS"
    states = "STATES"

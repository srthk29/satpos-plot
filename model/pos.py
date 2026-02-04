from typing import List
from pydantic import BaseModel

from model.plot_type import PlotType
from model.size_type import SizeType
from model.image_format import ImageFormat
from model.color_scheme import Colorscheme
from model.location import Location
from model.feature import Feature


class SatellitePlot(BaseModel):
    norad: int
    plot_types: List[PlotType]
    size_type: SizeType
    image_format: ImageFormat
    color_scheme: Colorscheme
    locations: List[Location]
    now_location: Location
    icon: bool
    nightshade: bool
    features: List[Feature]


'''
{
  "plot_types": ["PlateCarree"],
  "size_type": "medium",
  "image_format": "svg",
  "color_scheme": "default",
  "locations": [
    {
      "latitude": 12.97,
      "longitude": 77.59,
      "altitude": 400
    },
    "icon": true,
    "nightshade": true
  ]
}
'''

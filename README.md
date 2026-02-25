# LEO Satellite's Position Plot

using cartopy

## _run_
```bash
uv run fastapi run
```

## _sample request_
```json
{
  "norad": 25544,
  "plot_types": [
    "NearsidePerspective",
    "PlateCarree"
  ],
  "size_type": "medium",
  "image_format": "png",
  "color_scheme": {
    "theme": "light",
    "accent": "default"
  },
  "locations": [
    {
      "latitude": -15.30259985887203,
      "longitude": 142.7955459162778,
      "altitude": 430.7310667105221
    },
    {
      "latitude": -12.313218411965993,
      "longitude": 145.08614612351087,
      "altitude": 429.72526626464605
    },
    {
      "latitude": -9.299444431485888,
      "longitude": 147.3203066093599,
      "altitude": 428.77700991741585
    },
    {
      "latitude": -6.267520478647882,
      "longitude": 149.512792266868,
      "altitude": 427.89547364148166
    },
    {
      "latitude": -3.223361567711878,
      "longitude": 151.6777451935282,
      "altitude": 427.088253338874
    },
  ],
  "now_location": {
    "latitude": 39.54907868936153,
    "longitude": -169.0424530688017,
    "altitude": 423.918016833647
  },
  "icon": true,
  "nightshade": true,
  "features": []
}
```

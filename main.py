import io
import base64
from datetime import datetime, timezone
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
import cartopy.feature as cfeature

from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse

from model.pos import SatellitePlot
from model.location import Location
from model.size_type import plot_size
from typing import List

from helper import plot_custom_svg

app = FastAPI()


def encode_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def plot_svg(locs: List[Location]) -> bytes:
    fig = plt.figure(figsize=(16, 8))
    plt.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax = plt.axes(projection=ccrs.PlateCarree())
    # ax.coastlines()
    ax.add_feature(
        cfeature.LAND,
        edgecolor='lime',
        facecolor='forestgreen',
        zorder=0)

    ax.add_feature(
        cfeature.LAKES,
        edgecolor='black',
        linewidth=0.2,
        facecolor='blue')

    ax.add_feature(
        cfeature.OCEAN,
        facecolor='darkblue')

    ax.add_feature(
        cfeature.COASTLINE,
        edgecolor='lime',
        # facecolor='forestgreen',
        zorder=0)

    # https://cartopy.readthedocs.io/v0.25.0.post2/gallery/lines_and_polygons/nightshade.html#sphx-glr-gallery-lines-and-polygons-nightshade-py
    # UTC Time
    date = datetime.now(timezone.utc)
    ax.add_feature(Nightshade(date, alpha=0.25))

    if locs:
        # lons = [loc.longitude for loc in locations]
        # lats = [loc.latitude for loc in locations]
        lons, lats = zip(*[(loc.longitude, loc.latitude) for loc in locs])

        plt.plot(lons, lats,
                 color='darkgreen',
                 linewidth=1.5,
                 marker='x',
                 transform=ccrs.Geodetic())

    ax.set_global()
    ax.set_extent([-180, 180, -90, 90])
    ax.margins(0)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="svg", bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    buffer.seek(0)
    return buffer.getvalue()


def plot_svg_nearside() -> bytes:
    fig = plt.figure(figsize=(10, 10))
    plt.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax = plt.axes(projection=ccrs.NearsidePerspective(
        central_latitude=28.341,
        central_longitude=-54.7046,
        satellite_height=416145000))
    # ax.stock_img()
    # ax.coastlines(resolution='110m')
    # ax.gridlines()

    ax.add_feature(
        cfeature.LAND,
        edgecolor='lime',
        facecolor='forestgreen',
        zorder=0)

    ax.add_feature(
        cfeature.LAKES,
        edgecolor='lime',
        linewidth=0.2,
        facecolor='blue')

    ax.add_feature(
        cfeature.OCEAN,
        facecolor='darkblue')

    ax.add_feature(
        cfeature.COASTLINE,
        edgecolor='lime',
        # facecolor='forestgreen',
        zorder=0)

    ax.add_feature(
        cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_0_countries',
            scale='110m',
            facecolor='none',
            edgecolor='black',
            linewidth=0.2))

    date = datetime.now(timezone.utc)
    ax.add_feature(Nightshade(date, alpha=0.25))

    gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1,
                      color='black', alpha=0.5)

    # Manipulate latitude and longitude gridline numbers and spacing
    gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 20))
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 20))

    ax.set_global()
    # ax.set_extent([-180, 180, -90, 90])
    ax.margins(0)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="svg", bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    buffer.seek(0)
    return buffer.getvalue()


@app.get("/plot")
async def get_plot():
    return JSONResponse({
        "image_type": "svg",
        "encoding": "base64",
        "data": encode_base64(plot_svg()),
    })


@app.get("/plot/svg")
async def get_plot_svg():
    return Response(
        media_type="image/svg+xml",
        content=plot_svg()
    )


@app.get("/plot/nearside")
async def get_plot_nearside():
    return JSONResponse({
        "image_type": "svg",
        "encoding": "base64",
        "data": encode_base64(plot_svg_nearside()),
    })


@app.get("/plot/svg/nearside")
async def get_plot_svg_nearside():
    return Response(
        media_type="image/svg+xml",
        content=plot_svg_nearside()
    )


@app.post("/custom/plot")
async def get_plot_req(req: SatellitePlot):
    # result = {**req.dict()}
    # return result
    # return req.model_dump()

    return Response(
        media_type="image/svg+xml",
        content=plot_custom_svg(
            req.norad,
            req.plot_types[0],
            plot_size(req.size_type),
            req.image_format,
            req.color_scheme,
            req.locations,
            req.now_location,
            req.icon,
            req.nightshade
        )
    )

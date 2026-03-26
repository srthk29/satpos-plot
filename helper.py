import base64
import io
from datetime import datetime, timezone
from typing import List

import matplotlib
import numpy as np

matplotlib.use("Agg")

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from cartopy.feature.nightshade import Nightshade
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.transforms import Affine2D

from model.color_scheme import Colorscheme, get_accent_colors, get_theme_colors
from model.image_format import ImageFormat
from model.location import Location
from model.plot_type import PlotType
from model.size_type import PlotSize


def encode_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


projection_PlateCarree = ccrs.PlateCarree()
transform_Geodetic = ccrs.Geodetic()

iss_img = mpimg.imread("iss.png")  # transparent background
sat_img = mpimg.imread("sat.png")  # transparent background


def plot_custom_svg(
    norad: int,
    type: PlotType,
    size: PlotSize,
    format: ImageFormat,
    colorscheme: Colorscheme,
    locs: List[Location],
    now: Location,
    icon: bool,
    nightshade: bool,
) -> bytes:

    fig = plt.figure(figsize=size.figsize, dpi=size.dpi)
    # https://stackoverflow.com/questions/4581504/how-to-set-opacity-of-background-colour-of-graph-with-matplotlib
    fig.patch.set_visible(False)
    fig.patch.set_alpha(0.0)
    # fig = plt.figure(figsize=(16, 8), dpi=300)
    plt.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    if type == type.PlateCarree:
        projection = projection_PlateCarree
    else:
        if now:
            cen_lat = now.latitude
            cen_lon = now.longitude
            h = now.altitude * 1000_000
        else:
            cen_lat = 0.0
            cen_lon = 0.0
            h = 35785831

        projection = ccrs.NearsidePerspective(
            central_latitude=cen_lat, central_longitude=cen_lon, satellite_height=h
        )

    ax = plt.axes(projection=projection)
    # ax.coastlines()
    ax.set_frame_on(False)
    ax.patch.set_visible(False)
    # Features with a higher zorder value are drawn on
    # top of features with a lower zorder value.

    txt, _ = get_accent_colors(colorscheme.accent)
    _, bg = get_theme_colors(colorscheme.theme)

    # ax.add_feature(cfeature.LAND, edgecolor='lime', facecolor='forestgreen')
    ax.add_feature(cfeature.LAND, edgecolor=txt, facecolor=bg)

    # ax.add_feature(cfeature.COASTLINE, edgecolor='lime')
    ax.add_feature(cfeature.COASTLINE, edgecolor=txt)

    # ax.add_feature(cfeature.LAKES, facecolor='blue')
    ax.add_feature(cfeature.LAKES, edgecolor=txt, facecolor=bg)

    # ax.add_feature(cfeature.OCEAN, facecolor='darkblue')
    ax.add_feature(cfeature.OCEAN, facecolor=bg)

    # https://cartopy.readthedocs.io/v0.25.0.post2/gallery/lines_and_polygons/nightshade.html#sphx-glr-gallery-lines-and-polygons-nightshade-py
    # UTC Time
    if nightshade:
        date = datetime.now(timezone.utc)
        ax.add_feature(Nightshade(date, alpha=0.25))

    if type == type.NearsidePerspective:
        gl = ax.gridlines(
            crs=projection_PlateCarree, linewidth=1, color="black", alpha=0.5
        )

        # Manipulate latitude and longitude gridline numbers and spacing
        gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 20))
        gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 20))

    if locs:
        # lons = [loc.longitude for loc in locations]
        # lats = [loc.latitude for loc in locations]
        lons, lats = zip(*[(loc.longitude, loc.latitude) for loc in locs])

        plt.plot(
            lons,
            lats,
            color="dimgray",
            linewidth=2,
            linestyle="dashed",
            # marker='_',
            transform=transform_Geodetic,
        )

    if now:
        if icon:
            # Load ISS image
            if norad == 25544:
                img = iss_img  # transparent background
            else:
                img = sat_img  # transparent background

            imagebox = OffsetImage(img, zoom=0.02)
            imagebox.image.axes = ax
            imagebox.image.set_transform(Affine2D() + ax.transData)

            ab = AnnotationBbox(
                imagebox,
                (now.longitude, now.latitude),
                xycoords=projection_PlateCarree._as_mpl_transform(ax),
                frameon=False,
            )

            ax.add_artist(ab)
        else:
            plt.plot(
                now.longitude,
                now.latitude,
                marker="D",
                markersize=12,
                markerfacecolor="red",
                markeredgecolor="black",
                linestyle="None",
                transform=transform_Geodetic,
            )

    ax.set_global()
    if type == type.PlateCarree:
        ax.set_extent([-180, 180, -90, 90])
    ax.margins(0)
    ax.set_position([0, 0, 1, 1])

    buffer = io.BytesIO()
    plt.savefig(buffer, format=format, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    buffer.seek(0)
    return buffer.getvalue()


def plot_svg_nearside() -> bytes:
    fig = plt.figure(figsize=(10, 10))
    plt.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax = plt.axes(
        projection=ccrs.NearsidePerspective(
            central_latitude=28.341,
            central_longitude=-54.7046,
            satellite_height=416145000,
        )
    )
    # ax.stock_img()
    # ax.coastlines(resolution='110m')
    # ax.gridlines()

    ax.add_feature(cfeature.LAND, edgecolor="lime", facecolor="forestgreen", zorder=0)

    ax.add_feature(cfeature.LAKES, edgecolor="lime", linewidth=0.2, facecolor="blue")

    ax.add_feature(cfeature.OCEAN, facecolor="darkblue")

    ax.add_feature(
        cfeature.COASTLINE,
        edgecolor="lime",
        # facecolor='forestgreen',
        zorder=0,
    )

    ax.add_feature(
        cfeature.NaturalEarthFeature(
            category="cultural",
            name="admin_0_countries",
            scale="110m",
            facecolor="none",
            edgecolor="black",
            linewidth=0.2,
        )
    )

    date = datetime.now(timezone.utc)
    ax.add_feature(Nightshade(date, alpha=0.25))

    gl = ax.gridlines(crs=projection_PlateCarree, linewidth=1, color="black", alpha=0.5)

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


def plot_svg(locs: List[Location]) -> bytes:
    fig = plt.figure(figsize=(16, 8))
    plt.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax = plt.axes(projection=ccrs.PlateCarree())
    # ax.coastlines()
    ax.add_feature(cfeature.LAND, edgecolor="lime", facecolor="forestgreen", zorder=0)

    ax.add_feature(cfeature.LAKES, edgecolor="black", linewidth=0.2, facecolor="blue")

    ax.add_feature(cfeature.OCEAN, facecolor="darkblue")

    ax.add_feature(
        cfeature.COASTLINE,
        edgecolor="lime",
        # facecolor='forestgreen',
        zorder=0,
    )

    # https://cartopy.readthedocs.io/v0.25.0.post2/gallery/lines_and_polygons/nightshade.html#sphx-glr-gallery-lines-and-polygons-nightshade-py
    # UTC Time
    date = datetime.now(timezone.utc)
    ax.add_feature(Nightshade(date, alpha=0.25))

    if locs:
        # lons = [loc.longitude for loc in locations]
        # lats = [loc.latitude for loc in locations]
        lons, lats = zip(*[(loc.longitude, loc.latitude) for loc in locs])

        plt.plot(
            lons,
            lats,
            color="darkgreen",
            linewidth=1.5,
            marker="x",
            transform=ccrs.Geodetic(),
        )

    ax.set_global()
    ax.set_extent([-180, 180, -90, 90])
    ax.margins(0)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="svg", bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    buffer.seek(0)
    return buffer.getvalue()

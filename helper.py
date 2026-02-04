import io
from datetime import datetime, timezone
import numpy as np

from typing import List

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
import cartopy.feature as cfeature

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D

from model.plot_type import PlotType
from model.size_type import PlotSize
from model.image_format import ImageFormat
from model.color_scheme import Colorscheme
from model.location import Location


def plot_custom_svg(
        norad: int,
        type: PlotType,
        size: PlotSize,
        format: ImageFormat,
        colorscheme: Colorscheme,
        locs: List[Location],
        now: Location,
        icon: bool,
        nightshade: bool) -> bytes:

    fig = plt.figure(figsize=size.figsize, dpi=size.dpi)
    # fig = plt.figure(figsize=(16, 8), dpi=300)
    plt.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    if type == type.PlateCarree:
        projection = ccrs.PlateCarree()
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
            central_latitude=cen_lat,
            central_longitude=cen_lon,
            satellite_height=h)

    ax = plt.axes(projection=projection)
    # ax.coastlines()

    # Features with a higher zorder value are drawn on
    # top of features with a lower zorder value.

    ax.add_feature(
        cfeature.LAND,
        edgecolor='lime',
        facecolor='forestgreen')

    ax.add_feature(
        cfeature.LAKES,
        facecolor='blue')

    ax.add_feature(
        cfeature.COASTLINE,
        edgecolor='lime')

    ax.add_feature(
        cfeature.OCEAN,
        facecolor='darkblue')

    # https://cartopy.readthedocs.io/v0.25.0.post2/gallery/lines_and_polygons/nightshade.html#sphx-glr-gallery-lines-and-polygons-nightshade-py
    # UTC Time
    if nightshade:
        date = datetime.now(timezone.utc)
        ax.add_feature(Nightshade(date, alpha=0.25))

    if type == type.NearsidePerspective:
        gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1,
                          color='black', alpha=0.5)

        # Manipulate latitude and longitude gridline numbers and spacing
        gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 20))
        gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 20))

    if locs:
        # lons = [loc.longitude for loc in locations]
        # lats = [loc.latitude for loc in locations]
        lons, lats = zip(*[(loc.longitude, loc.latitude) for loc in locs])

        plt.plot(lons, lats,
                 color='dimgray',
                 linewidth=2,
                 linestyle='dashed',
                 # marker='_',
                 transform=ccrs.Geodetic())

    if now:
        if icon:
            # Load ISS image
            if norad == 25544:
                iss_img = mpimg.imread("iss.png")  # transparent background
            else:
                iss_img = mpimg.imread("sat.png")  # transparent background

            imagebox = OffsetImage(iss_img, zoom=0.04)

            imagebox.image.axes = ax
            imagebox.image.set_transform(Affine2D() + ax.transData)

            ab = AnnotationBbox(
                imagebox,
                (now.longitude, now.latitude),
                xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                frameon=False,
            )

            ax.add_artist(ab)
        else:
            plt.plot(now.longitude, now.latitude,
                     marker='D',
                     markersize=12,
                     markerfacecolor='red',
                     markeredgecolor='black',
                     linestyle='None',
                     transform=ccrs.Geodetic())

    ax.set_global()
    if type == type.PlateCarree:
        ax.set_extent([-180, 180, -90, 90])
    ax.margins(0)

    buffer = io.BytesIO()
    plt.savefig(buffer, format=format, bbox_inches="tight", pad_inches=0)
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

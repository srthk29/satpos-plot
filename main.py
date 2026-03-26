import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from helper import encode_base64, plot_custom_svg, plot_svg, plot_svg_nearside
from model.pos import SatellitePlot
from model.size_type import plot_size

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # Log the response time along with the request path and status code
    logger.info(
        f"Request: {request.url.path} | Status: {response.status_code} | Process Time: {
            process_time:.4f}s"
    )

    return response


class Plot(BaseModel):
    media_type: str
    plot_type: str
    # content: bytes
    content: str


# @app.get("/plot")
async def get_plot():
    return JSONResponse(
        {
            "image_type": "svg",
            "encoding": "base64",
            "data": encode_base64(plot_svg()),
        }
    )


# @app.get("/plot/svg")
async def get_plot_svg():
    return Response(media_type="image/svg+xml", content=plot_svg())


# @app.get("/plot/nearside")
async def get_plot_nearside():
    return JSONResponse(
        {
            "image_type": "svg",
            "encoding": "base64",
            "data": encode_base64(plot_svg_nearside()),
        }
    )


# @app.get("/plot/svg/nearside")
async def get_plot_svg_nearside():
    return Response(media_type="image/svg+xml", content=plot_svg_nearside())


@app.post("/custom/plot")
async def get_plot_req(req: SatellitePlot, response_model=list[Plot]):
    # result = {**req.dict()}
    # return result
    # return req.model_dump()

    plots = []
    for plot_type in req.plot_types:
        plots.append(
            Plot(
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types#image_types
                media_type=req.image_format,
                plot_type=plot_type,
                content=encode_base64(
                    plot_custom_svg(
                        req.norad,
                        plot_type,
                        plot_size(req.size_type),
                        req.image_format,
                        req.color_scheme,
                        req.locations,
                        req.now_location,
                        req.icon,
                        req.nightshade,
                    )
                ),
            )
        )
    return plots

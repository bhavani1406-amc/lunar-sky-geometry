from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import spiceypy as spice
from sky import sun_earth_sky

app = FastAPI(title="Lunar Sky Geometry")

# Lets the Next.js frontend call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/sky")
def sky(lat: float, lon: float, time: str):
    """Sun and Earth az/el at a lunar site. lon is east-positive, time is UTC."""
    return sun_earth_sky(lat, lon, time)


@app.get("/sky/series")
def sky_series(
    lat: float,
    lon: float,
    start: str,
    hours: int = 720,
    step_minutes: int = 60
):
    """Sun/Earth az/el over time. Default: 30 days at hourly steps."""
    n = min(hours * 60 // step_minutes, 5000)
    et0 = spice.str2et(start)
    out = []
    for i in range(n + 1):
        utc = spice.et2utc(et0 + i * step_minutes * 60, "ISOC", 0)
        out.append({"time": utc, **sun_earth_sky(lat, lon, utc)})
    return out
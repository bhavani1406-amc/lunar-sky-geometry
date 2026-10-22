import os
import numpy as np
import spiceypy as spice

BASE = os.path.dirname(os.path.abspath(__file__))
KERNELS = [
    "naif0012.tls",
    "de440s.bsp",
    "pck00011.tpc",
    "moon_pa_de440_200625.bpc",
    "moon_de440_250416.tf",
]

for k in KERNELS:
    spice.furnsh(os.path.join(BASE, k))  # Removed "kernels" subfolder from path

R_MOON = 1737.4  # km


def sky_position(body, lat_deg, lon_deg, utc):
    et = spice.str2et(utc)
    lat, lon = np.radians(lat_deg), np.radians(lon_deg)

    # Body position relative to Moon center, in the Moon-fixed frame
    pos, _ = spice.spkpos(body, et, "MOON_ME", "LT+S", "MOON")

    # Site position and local East-North-Up basis, all in MOON_ME
    site = R_MOON * np.array([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat)
    ])
    east = np.array([-np.sin(lon), np.cos(lon), 0.0])
    north = np.array([
        -np.sin(lat) * np.cos(lon),
        -np.sin(lat) * np.sin(lon),
        np.cos(lat)
    ])
    up = np.array([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat)
    ])

    v = pos - site
    d = np.linalg.norm(v)
    return {
        "elevation_deg": float(np.degrees(np.arcsin((v @ up) / d))),
        "azimuth_deg": float(np.degrees(np.arctan2(v @ east, v @ north)) % 360),
        "distance_km": float(d),
    }


def sun_earth_sky(lat_deg, lon_deg, utc):
    return {
        "sun": sky_position("SUN", lat_deg, lon_deg, utc),
        "earth": sky_position("EARTH", lat_deg, lon_deg, utc),
    }
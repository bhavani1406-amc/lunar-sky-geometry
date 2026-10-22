from sky import sun_earth_sky

t = "2026-10-21 12:00:00 UTC"

print("Sub-Earth point (lat -0.2, lon -5.5):")
print(sun_earth_sky(-0.2, -5.5, t)["earth"])

print("\nSub-solar point (lat -1.35, lon 52.7):")
print(sun_earth_sky(-1.35, 52.7, t)["sun"])

print("\nSouth pole site (lat -89.9, lon 0):")
print(sun_earth_sky(-89.9, 0.0, t))
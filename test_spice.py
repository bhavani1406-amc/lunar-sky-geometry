import spiceypy as spice

spice.furnsh("C:/Users/pramo/OneDrive/Desktop/lunar/meta.tm")
et = spice.str2et("2026-10-21 12:00:00 UTC")

sun, _ = spice.spkpos("SUN", et, "MOON_ME", "LT+S", "MOON")
earth, _ = spice.spkpos("EARTH", et, "MOON_ME", "LT+S", "MOON")

print("Sun   (km):", sun)
print("Earth (km):", earth)
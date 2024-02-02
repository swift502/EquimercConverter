import sys
import os
from PIL import Image
from pathlib import Path
import math

def clamp(value, minValue, maxValue):
    return min(max(value, minValue), maxValue)

def equi_to_merc(u: float, v: float):
    # uv to equirectangular
    lat: float = u * 2 * math.pi    # from 0 to 2PI
    lon: float = (v - 0.5) * math.pi  # from -PI to PI

    # equirectangular to mercator
    x: float = lat
    maxLon = 2 * math.atan(math.pow(math.e, math.pi)) - math.pi * 0.5
    lon = clamp(lon, -maxLon, maxLon)
    tan = math.tan(math.pi / 4 + lon / 2)
    # print(lat, lon, tan)
    y: float = math.log(tan)

    # bring x,y into [0,1] range
    x = clamp(x / (2 * math.pi), 0, 1)
    y = clamp((y + math.pi) / (2 * math.pi), 0, 1)

    return (x, y)


# if len(sys.argv) == 1:
#     print("No image parameter supplied. Exiting.")
#     os.system('pause')
#     exit()

# path = Path(sys.argv[1])
path = Path("equi.png")

print(f"\nProcessing \"{path.name}\"")
image = Image.open(path)
newImage = Image.new(image.mode, (image.width, int(image.height * math.pi * 0.5)))

pixels = image.load()
newPixels = newImage.load()

for x in range(image.width):
    for y in range(image.height):
        (mercX, mercY) = equi_to_merc(x / image.width, y / image.height)
        newX = mercX * (newImage.width - 2)
        newY = mercY * (newImage.height - 2)
        newPixels[newX, newY] = pixels[x, y]
        # print(mercX, mercY)

split = str(path).split(".")
split[-2] += "_processed"
newPath = '.'.join(split)
newImage.save(newPath)

print(f"\033[32mConverted!\033[0m")
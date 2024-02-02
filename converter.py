import sys
import os
from PIL import Image
from pathlib import Path
import math

def remap(value, oldMin, oldMax, newMin, newMax):
    return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin

def clamp(value, minValue, maxValue):
    return min(max(value, minValue), maxValue)

maxLon = 2 * math.atan(math.pow(math.e, math.pi)) - math.pi * 0.5

def equi_to_merc(u, v):
    # uv to equirectangular
    lat = remap(u, 0, 1, 0, 2 * math.pi)
    lon = remap(v, 0, 1, -math.pi * 0.5, math.pi * 0.5)

    # equirectangular to mercator
    x = lat
    lon = clamp(lon, -maxLon, maxLon)
    tan = math.tan(math.pi / 4 + lon / 2)
    y = math.log(tan)

    # mercator to uv
    x = remap(x, 0, 2 * math.pi, 0, 1)
    y = remap(y, -math.pi, math.pi, 0, 1)

    # clamp
    x = clamp(x, 0, 1)
    y = clamp(y, 0, 1)

    return (x, y)

def merc_to_equi(u, v):
    # uv to mercator
    lat = remap(u, 0, 1, 0, 2 * math.pi)
    lon = remap(v, 0, 1, -math.pi, math.pi)

    # equirectangular to mercator
    x = lat
    y = math.pow(math.e, lon)
    y = math.atan(y)
    y = y * 2 - math.pi / 2
    # lon = clamp(lon, -maxLon, maxLon)
    # tan = math.tan(math.pi / 4 + lon / 2)
    # y = math.log(tan)

    # equirectangular to uv
    x = remap(x, 0, 2 * math.pi, 0, 1)
    y = remap(y, -math.pi * 0.5, math.pi * 0.5, 0, 1)

    # clamp
    x = clamp(x, 0, 1)
    y = clamp(y, 0, 1)

    return (x, y)

def progressBar(iteration, total, decimals = 1, length = 50):
    # Call in a loop to create terminal progress bar
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + ' ' * (length - filledLength)
    print(f'\rProgress:  {bar} {percent}%', end = "")

    # Print New Line on Complete
    if iteration == total: 
        print()

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

# total = image.width * image.height
# progress = 0
# for x in range(image.width):
#     for y in range(image.height):
#         (mercX, mercY) = equi_to_merc(x / image.width, y / image.height)
#         newX = mercX * (newImage.width - 1)
#         newY = mercY * (newImage.height - 1)
#         newPixels[newX, newY] = pixels[x, y]
#         progress += 1
#     progressBar(progress, total)

total = newImage.width * newImage.height
progress = 0
for x in range(newImage.width):
    for y in range(newImage.height):
        (equiX, equiY) = merc_to_equi(x / newImage.width, y / newImage.height)
        sampleX = equiX * (image.width - 1)
        sampleY = equiY * (image.height - 1)
        newPixels[x, y] = pixels[sampleX, sampleY]
        progress += 1
    progressBar(progress, total)

split = str(path).split(".")
split[-2] += "_processed2"
newPath = '.'.join(split)
newImage.save(newPath)

print(f"\033[32mConverted!\033[0m")
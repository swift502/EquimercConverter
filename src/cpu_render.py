from PIL import Image
import math
from .enums import CONVERSION

MERC_MAX_LON = 2 * math.atan(math.pow(math.e, math.pi)) - math.pi * 0.5

def remap(value, oldMin, oldMax, newMin, newMax):
    return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin

def clamp(value, minValue, maxValue):
    return min(max(value, minValue), maxValue)

def equi_to_merc(u, v):
    # uv to equirectangular
    lat = remap(u, 0, 1, 0, 2 * math.pi)
    lon = remap(v, 0, 1, -math.pi * 0.5, math.pi * 0.5)

    # equirectangular to mercator
    x = lat
    lon = clamp(lon, -MERC_MAX_LON, MERC_MAX_LON)
    y = math.log(math.tan(math.pi / 4 + lon / 2))

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

    # mercator to equirectangular
    x = lat
    y = 2 * math.atan(math.pow(math.e, lon)) - math.pi * 0.5

    # equirectangular to uv
    x = remap(x, 0, 2 * math.pi, 0, 1)
    y = remap(y, -math.pi * 0.5, math.pi * 0.5, 0, 1)

    # clamp
    x = clamp(x, 0, 1)
    y = clamp(y, 0, 1)

    return (x, y)

def render(image: Image.Image, conversion: CONVERSION):
    if conversion == CONVERSION.TO_MERCATOR:
        newImage = Image.new(image.mode, (image.width, 2 * image.height))
    else:
        newImage = Image.new(image.mode, (2 * image.width, image.height))

    pixels = image.load()
    newPixels = newImage.load()

    total = newImage.width
    progress = 0
    for x in range(newImage.width):
        for y in range(newImage.height):
            if conversion == CONVERSION.TO_MERCATOR:
                # Running through a merc image, we need to sample equi
                (u, v) = merc_to_equi(x / newImage.width, y / newImage.height)
            else:
                # Running through an equi image, we need to sample merc
                (u, v) = equi_to_merc(x / newImage.width, y / newImage.height)
            sampleX = round(u * (image.width - 1))
            sampleY = round(v * (image.height - 1))
            newPixels[x, y] = pixels[sampleX, sampleY]
        
        progress += 1
        if progress % 20 == 0 or progress == total:
            progressBar(progress, total)
    
    return newImage

def progressBar(iteration, total, length = 50):
    # Progress bar
    progress = iteration / total
    percent = "{0:.1f}".format(100 * progress)
    filledLength = int(length * progress)
    bar = '█' * filledLength + ' ' * (length - filledLength)
    print(f'\rProgress: {bar} {percent}%', end = "")

    # Print New Line on Complete
    if iteration == total: 
        print()
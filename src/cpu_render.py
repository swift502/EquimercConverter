from PIL import Image
import math
from .enums import CONVERSION

# Max longitude in the equirectangular projection
EQUI_LON = 2 * math.atan(math.pow(math.e, math.pi)) - math.pi * 0.5

def clamp01(value):
    return max(0, min(1, value))

def remap(value, oldMin, oldMax, newMin, newMax):
    return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin

def equi_to_merc(u, v):
    # uv to equirectangular
    lon = remap(v, 0, 1, -EQUI_LON, EQUI_LON)

    # equirectangular to mercator
    y = math.log(math.tan(math.pi / 4 + lon / 2))

    # mercator to uv
    y = remap(y, -math.pi, math.pi, 0, 1)

    # clamp
    y = clamp01(y)

    return (u, y)

def merc_to_equi(u, v):
    # uv to mercator
    lon = remap(v, 0, 1, -math.pi, math.pi)

    # mercator to equirectangular
    y = 2 * math.atan(math.pow(math.e, lon)) - math.pi * 0.5

    # equirectangular to uv
    y = remap(y, -EQUI_LON, EQUI_LON, 0, 1)

    # clamp
    y = clamp01(y)

    return (u, y)

def render(image: Image.Image, conversion: CONVERSION):
    # Create new image
    if conversion == CONVERSION.TO_MERCATOR:
        newImage = Image.new(image.mode, (image.width, 2 * image.height))
    else:
        newImage = Image.new(image.mode, (2 * image.width, image.height))

    # Load
    pixels = image.load()
    newPixels = newImage.load()

    # Image bounds
    maxX = newImage.width - 1
    maxY = newImage.height - 1

    progress = 0
    total = newImage.width
    for x in range(newImage.width):
        for y in range(newImage.height):
            # UV conversion
            if conversion == CONVERSION.TO_MERCATOR:
                # Writing into a blank merc image, we need to sample equi
                (u, v) = merc_to_equi(x / maxX, y / maxY)
            else:
                # Writing into a blank equi image, we need to sample merc
                (u, v) = equi_to_merc(x / maxX, y / maxY)

            # Resample original image using converted UVs
            sampleX = min(math.floor(u * image.width), image.width - 1)
            sampleY = min(math.floor(v * image.height), image.height - 1)
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
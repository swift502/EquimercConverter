import sys
import os
from PIL import Image
from pathlib import Path
import math
from enum import Enum

class ConversionType(Enum):
    TO_EQUIRECTANGULAR = 1
    TO_MERCATOR = 2

class Converter:

    MERC_MAX_LON = 2 * math.atan(math.pow(math.e, math.pi)) - math.pi * 0.5

    def remap(value, oldMin, oldMax, newMin, newMax):
        return ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin

    def clamp(value, minValue, maxValue):
        return min(max(value, minValue), maxValue)

    def equi_to_merc(u, v):
        # uv to equirectangular
        lat = Converter.remap(u, 0, 1, 0, 2 * math.pi)
        lon = Converter.remap(v, 0, 1, -math.pi * 0.5, math.pi * 0.5)

        # equirectangular to mercator
        x = lat
        lon = Converter.clamp(lon, -Converter.MERC_MAX_LON, Converter.MERC_MAX_LON)
        tan = math.tan(math.pi / 4 + lon / 2)
        y = math.log(tan)

        # mercator to uv
        x = Converter.remap(x, 0, 2 * math.pi, 0, 1)
        y = Converter.remap(y, -math.pi, math.pi, 0, 1)

        # clamp
        x = Converter.clamp(x, 0, 1)
        y = Converter.clamp(y, 0, 1)

        return (x, y)

    def merc_to_equi(u, v):
        # uv to mercator
        lat = Converter.remap(u, 0, 1, 0, 2 * math.pi)
        lon = Converter.remap(v, 0, 1, -math.pi, math.pi)

        # equirectangular to mercator
        x = lat
        y = math.atan(math.pow(math.e, lon)) * 2 - math.pi / 2

        # equirectangular to uv
        x = Converter.remap(x, 0, 2 * math.pi, 0, 1)
        y = Converter.remap(y, -math.pi * 0.5, math.pi * 0.5, 0, 1)

        # clamp
        x = Converter.clamp(x, 0, 1)
        y = Converter.clamp(y, 0, 1)

        return (x, y)

    # path = Path(sys.argv[1])
    def convert(input: str, output: str, mode: ConversionType):
        file = Path(input)

        print(f"\nProcessing \"{file.name}\"")
        image = Image.open(file)
        newImage = Image.new(image.mode, (image.width, int(image.height * math.pi * 0.5)))

        pixels = image.load()
        newPixels = newImage.load()

        total = newImage.width * newImage.height
        progress = 0
        for x in range(newImage.width):
            for y in range(newImage.height):
                (equiX, equiY) = Converter.merc_to_equi(x / newImage.width, y / newImage.height)
                sampleX = round(equiX * (image.width - 1))
                sampleY = round(equiY * (image.height - 1))
                newPixels[x, y] = pixels[sampleX, sampleY]
                progress += 1
            Converter.progressBar(progress, total)

        # split = str(file).split(".")
        # split[-2] += "_processed2"
        # newPath = '.'.join(split)
        newImage.save(output)

        print(f"\033[32mConverted!\033[0m")
    
    def progressBar(iteration, total, length = 50):
        # Call in a loop to create terminal progress bar
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = '█' * filledLength + ' ' * (length - filledLength)
        print(f'\rProgress:  {bar} {percent}%', end = "")

        # Print New Line on Complete
        if iteration == total: 
            print()
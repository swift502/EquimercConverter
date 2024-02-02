import sys
from PIL import Image
from pathlib import Path
import math
from enum import Enum

class Converter:

    class MODE(Enum):
        TO_EQUIRECTANGULAR = 1
        TO_MERCATOR = 2

    # https://paulbourke.net/panorama/webmerc2sphere/index.html
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
        y = math.log(math.tan(math.pi / 4 + lon / 2))

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

        # mercator to equirectangular
        x = lat
        y = math.atan(math.pow(math.e, lon)) * 2 - math.pi / 2

        # equirectangular to uv
        x = Converter.remap(x, 0, 2 * math.pi, 0, 1)
        y = Converter.remap(y, -math.pi * 0.5, math.pi * 0.5, 0, 1)

        # clamp
        x = Converter.clamp(x, 0, 1)
        y = Converter.clamp(y, 0, 1)

        return (x, y)

    def convert(input: str, output: str, mode: MODE):
        try:
            file = Path(input)

            if mode == Converter.MODE.TO_EQUIRECTANGULAR:
                print(f"\nConverting \"{file.name}\" to equirectangular.")
            else:
                print(f"\nConverting \"{file.name}\" to mercator.")

            image = Image.open(file)

            if mode == Converter.MODE.TO_EQUIRECTANGULAR:
                newImage = Image.new(image.mode, (int(image.width * math.pi * 0.5), image.height))
            else:
                newImage = Image.new(image.mode, (image.width, int(image.height * math.pi * 0.5)))

            pixels = image.load()
            newPixels = newImage.load()

            total = newImage.width * newImage.height
            progress = 0
            for x in range(newImage.width):
                for y in range(newImage.height):
                    if mode == Converter.MODE.TO_EQUIRECTANGULAR:
                        # Running through an equi image, we need to sample merc
                        (sampleX, sampleY) = Converter.equi_to_merc(x / newImage.width, y / newImage.height)
                    else:
                        # Running through a merc image, we need to sample equi
                        (sampleX, sampleY) = Converter.merc_to_equi(x / newImage.width, y / newImage.height)
                    newPixels[x, y] = pixels[sampleX * (image.width - 1), sampleY * (image.height - 1)]
                    progress += 1
                Converter.progressBar(progress, total)

            newImage.save(output)
            print(f"\033[32mSuccess!\033[0m")

        except Exception as e:
            print("\033[31mError:\033[0m")
            print(e)
    
    def progressBar(iteration, total, length = 50):
        # Call in a loop to create terminal progress bar
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = '█' * filledLength + ' ' * (length - filledLength)
        print(f'\rProgress:  {bar} {percent}%', end = "")

        # Print New Line on Complete
        if iteration == total: 
            print()
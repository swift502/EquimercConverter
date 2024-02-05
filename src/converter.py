import sys
from PIL import Image
from pathlib import Path
import math
import enums

import cpu_render
import gpu_render

class Converter:
    def convert(input: str, output: str, format: enums.FORMAT, mode: enums.RENDER_MODE = enums.RENDER_MODE.GPU):
        try:
            file = Path(input)

            if format == enums.FORMAT.TO_EQUIRECTANGULAR:
                print(f"\nConverting \"{file.name}\" to equirectangular.")
            else:
                print(f"\nConverting \"{file.name}\" to mercator.")

            image = Image.open(file)
            
            if mode == enums.RENDER_MODE.CPU:
                newImage: Image.Image = cpu_render.render(image, format)
            else:
                newImage: Image.Image = gpu_render.render(image, format)
            
            newImage.save(output)
            print(f"\033[32mSuccess!\033[0m")

        except Exception as e:
            print("\033[31mError:\033[0m")
            print(e)
    
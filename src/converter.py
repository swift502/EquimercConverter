import os
from PIL import Image
from pathlib import Path
from .enums import FORMAT, RENDER_MODE, SAMPLING
from . import cpu_render, gpu_render

class Converter:
    def convert(input: str, output: str, format: FORMAT, mode: RENDER_MODE = RENDER_MODE.GPU, sampling: SAMPLING = SAMPLING.LINEAR):
        try:
            file = Path(input)

            if format == FORMAT.TO_EQUIRECTANGULAR:
                print(f"\nConverting \"{file.name}\" to equirectangular.")
            else:
                print(f"\nConverting \"{file.name}\" to mercator.")

            image = Image.open(file)
            
            if mode == RENDER_MODE.GPU:
                newImage: Image.Image = gpu_render.render(image, format, sampling)
            else:
                newImage: Image.Image = cpu_render.render(image, format)
            
            directory = os.path.dirname(output)
            if not os.path.exists(directory):
                os.makedirs(directory)

            newImage.save(output)
            print(f"\033[32mSuccess!\033[0m")

        except Exception as e:
            print("\033[31mError:\033[0m")
            print(e)
    
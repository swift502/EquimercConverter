import os
from PIL import Image
from pathlib import Path
from .enums import CONVERSION, DEVICE, SAMPLING
from . import cpu_render, gpu_render

class Converter:
    def convert(input: str, output: str, conversion: CONVERSION, device: DEVICE = DEVICE.GPU, sampling: SAMPLING = SAMPLING.LINEAR):
        try:
            file = Path(input)

            if conversion == CONVERSION.TO_MERCATOR:
                print(f"\nConverting \"{file.name}\" to mercator.")
            else:
                print(f"\nConverting \"{file.name}\" to equirectangular.")

            Image.MAX_IMAGE_PIXELS = None
            image = Image.open(file)
            
            if device == DEVICE.GPU:
                newImage: Image.Image = gpu_render.render(image, conversion, sampling)
            else:
                newImage: Image.Image = cpu_render.render(image, conversion)
            
            outFile = Path(output)
            directory = os.path.dirname(outFile)
            if len(directory) > 0 and not os.path.exists(directory):
                os.makedirs(directory)

            print(f"Saving {outFile.absolute()}")
            newImage.save(outFile)
            print(f"\033[32mSuccess!\033[0m")

        except Exception as e:
            print(f"\033[31mError:\033[0m {e}")
    